#!/usr/bin/env python3
"""Run pre-registered Covid Test 1 on the decision host.

This script executes the pinned commands and the decision rule in
tests/TEST-01-genome-classification.md. It does not change that rule.
It must be pointed at already-downloaded, accession-pinned FASTA files.
"""

from __future__ import annotations

import json
import os
import shutil
import subprocess
import sys
from collections import defaultdict
from pathlib import Path

PROTOCOL_EVALUE = 1e-5
COVERAGE_THRESHOLD = 0.50
GAP_FRACTION = 0.50
MIN_COLUMNS = 200
MIN_IDENTITY = 0.30
UFBOOT_MIN = 95
SHALRT_MIN = 80
SPACER = "N" * 10
SEED = "12345"
THREADS = "1"


def read_fa(path: Path):
    seqs, name, buf = [], None, []
    for line in path.read_text().splitlines():
        if line.startswith(">"):
            if name is not None:
                seqs.append((name, "".join(buf)))
            name, buf = line[1:].split()[0], []
        else:
            buf.append(line.strip())
    if name is not None:
        seqs.append((name, "".join(buf)))
    return seqs


def write_fa(path: Path, records):
    path.parent.mkdir(parents=True, exist_ok=True)
    lines = []
    for name, seq in records:
        lines.append(f">{name}")
        for i in range(0, len(seq), 70):
            lines.append(seq[i : i + 70])
    path.write_text("\n".join(lines) + "\n")


def merge_intervals(intervals):
    """Merge 1-based inclusive intervals; ignore empty."""
    norm = []
    for a, b in intervals:
        lo, hi = (a, b) if a <= b else (b, a)
        if lo < 1:
            lo = 1
        if hi < lo:
            continue
        norm.append((lo, hi))
    if not norm:
        return []
    norm.sort()
    out = [norm[0]]
    for lo, hi in norm[1:]:
        plo, phi = out[-1]
        if lo <= phi + 1:
            out[-1] = (plo, max(phi, hi))
        else:
            out.append((lo, hi))
    return out


def covered_bases(intervals):
    return sum(hi - lo + 1 for lo, hi in merge_intervals(intervals))


def extract_trimmed(seq: str, intervals):
    """Return trimmed sequence for one segment, 10 N between disjoint kept intervals.

    intervals are 1-based inclusive, already in deposited orientation.
    """
    merged = merge_intervals(intervals)
    if not merged:
        return ""
    parts = [seq[lo - 1 : hi] for lo, hi in merged]
    return SPACER.join(parts)


def run(cmd, cwd, log_fh, extra_env=None):
    env = os.environ.copy()
    if extra_env:
        env.update(extra_env)
    # Apply nice 19 once. Some callers already prefix the argv with nice;
    # do not double-prefix. Log the argv that is actually executed.
    if cmd and cmd[0] == "nice":
        full = list(cmd)
    else:
        full = ["nice", "-n", "19", *cmd]
    log_fh.write("$ " + " ".join(full) + f"\n# cwd={cwd}\n")
    log_fh.flush()
    proc = subprocess.run(
        full,
        cwd=str(cwd),
        env=env,
        text=True,
        capture_output=True,
    )
    if proc.stdout:
        log_fh.write(proc.stdout)
        if not proc.stdout.endswith("\n"):
            log_fh.write("\n")
    if proc.stderr:
        log_fh.write(proc.stderr)
        if not proc.stderr.endswith("\n"):
            log_fh.write("\n")
    log_fh.write(f"# exit={proc.returncode}\n")
    log_fh.flush()
    if proc.returncode != 0:
        raise SystemExit(
            f"command failed ({proc.returncode}): {' '.join(cmd)}\n{proc.stderr}"
        )
    return proc


def parse_blast_tsv(path: Path):
    """Parse the pinned outfmt 6 table."""
    # qseqid sacc sseqid pident length evalue bitscore qcovs qstart qend sstart send qlen slen
    rows = []
    if not path.exists() or path.stat().st_size == 0:
        return rows
    for line in path.read_text().splitlines():
        if not line.strip() or line.startswith("#"):
            continue
        parts = line.split("\t")
        if len(parts) < 14:
            raise SystemExit(f"unexpected BLAST row in {path}: {line!r}")
        rows.append(
            {
                "qseqid": parts[0],
                "sacc": parts[1],
                "sseqid": parts[2],
                "pident": float(parts[3]),
                "length": int(parts[4]),
                "evalue": float(parts[5]),
                "bitscore": float(parts[6]),
                "qcovs": float(parts[7]),
                "qstart": int(parts[8]),
                "qend": int(parts[9]),
                "sstart": int(parts[10]),
                "send": int(parts[11]),
                "qlen": int(parts[12]),
                "slen": int(parts[13]),
            }
        )
    return rows


def resolve_subject(row, accessions):
    """Map BLAST sacc/sseqid onto a pinned accession.version.

    BLAST -outfmt sacc omits the version when -parse_seqids is used;
    sseqid still carries ref|ACCESSION.VERSION|. Unique base-accession
    match, or a unique accession.version found in sseqid. Ambiguous
    matches return None. This is a parser fix, not a change to the
    pinned blastn command or the decision rule.
    """
    sacc = row.get("sacc") or ""
    sseqid = row.get("sseqid") or ""
    accs = list(accessions)
    if sacc in accs:
        return sacc
    base_hits = [acc for acc in accs if acc == sacc or acc.startswith(sacc + ".")]
    if len(base_hits) == 1:
        return base_hits[0]
    exact_in_sseqid = [acc for acc in accs if acc in sseqid]
    if len(base_hits) > 1:
        return exact_in_sseqid[0] if len(exact_in_sseqid) == 1 else None
    if len(exact_in_sseqid) == 1:
        return exact_in_sseqid[0]
    return None


def resolve_blast_table(rows, accessions):
    """Rewrite each row's sacc to the pinned accession.version when it resolves.

    Unresolved rows keep their raw sacc and set sacc_resolved to None.
    The original BLAST token is preserved as sacc_raw.
    """
    out = []
    for r in rows:
        r2 = dict(r)
        r2["sacc_raw"] = r.get("sacc")
        acc = resolve_subject(r, accessions)
        r2["sacc_resolved"] = acc
        if acc is not None:
            r2["sacc"] = acc
        out.append(r2)
    return out


def genome_accessions(genomes):
    accs = []
    for g in genomes:
        for s in g["segs"]:
            accs.append(s["accession"])
    return accs


def genome_hit(query_acc, rows, genome, ev_cutoff=PROTOCOL_EVALUE):
    """Qualifying hit of one query record against one reference genome (step 5)."""
    # Map accession -> segment and slen
    acc_to_seg = {s["accession"]: s for s in genome["segs"]}
    hsps = []
    for r in rows:
        if r["evalue"] > ev_cutoff:
            continue
        acc = r.get("sacc_resolved")
        if not acc:
            acc = resolve_subject(r, acc_to_seg)
        if acc is None or acc not in acc_to_seg:
            continue
        r = dict(r)
        r["sacc_resolved"] = acc
        r["sacc"] = acc  # use versioned accession for interval grouping
        hsps.append(r)
    q_iv = [(r["qstart"], r["qend"]) for r in hsps]
    covered_q = covered_bases(q_iv)
    # subject intervals merged within each segment, then summed
    by_seg = defaultdict(list)
    slens = {}
    for r in hsps:
        seg = acc_to_seg[r["sacc"]]["segment"]
        # 1-based inclusive; convert to a positive interval if opposite strand
        a, b = r["sstart"], r["send"]
        if a > b:
            a, b = b, a
        by_seg[seg].append((a, b))
        slens[r["sacc"]] = r["slen"]
    covered_s = 0
    for seg, ivs in by_seg.items():
        covered_s += covered_bases(ivs)
    # Glen = sum of lengths of that reference genome's segments
    # prefer slen from BLAST when present, else opened length
    glen = 0
    for s in genome["segs"]:
        if s["accession"] in slens:
            glen += slens[s["accession"]]
        else:
            glen += int(s["length"])
    qlen = None
    for r in rows:
        if r["qseqid"] == query_acc or r["qseqid"].startswith(query_acc):
            qlen = r["qlen"]
            break
    # If this query had no row at all against this genome, we still need qlen
    # from any row of this query, or from the opened length later.
    if qlen is None:
        for r in rows:
            qlen = r["qlen"]
            break
    result = {
        "genome": genome["org"],
        "n_hsps": len(hsps),
        "covered_query_bases": covered_q,
        "covered_subject_bases": covered_s,
        "Qlen": qlen,
        "Glen": glen,
        "bitscore_max": max((r["bitscore"] for r in hsps), default=None),
        "pident_of_max_bitscore": None,
        "qualifying": False,
        "shorter_molecule_coverage": None,
        "L_short": None,
        "covered_bases_on_shorter": None,
    }
    if hsps:
        best = max(hsps, key=lambda r: r["bitscore"])
        result["pident_of_max_bitscore"] = best["pident"]
    if qlen is None or glen is None or qlen <= 0 or glen <= 0:
        return result
    L_short = min(qlen, glen)
    if qlen < glen:
        covered_short = covered_q
    elif glen < qlen:
        covered_short = covered_s
    else:
        covered_short = min(covered_q, covered_s)
    cov = covered_short / L_short
    result["L_short"] = L_short
    result["covered_bases_on_shorter"] = covered_short
    result["shorter_molecule_coverage"] = cov
    result["qualifying"] = cov >= COVERAGE_THRESHOLD
    return result


def best_of_set(hits):
    """Best qualifying genome in a set: highest bitscore; ties left tied."""
    qual = [h for h in hits if h["qualifying"] and h["bitscore_max"] is not None]
    if not qual:
        return None, False
    best_score = max(h["bitscore_max"] for h in qual)
    tops = [h for h in qual if h["bitscore_max"] == best_score]
    return tops, len(tops) > 1


def repo_root() -> Path:
    return Path(__file__).resolve().parents[1]


def main(argv=None):
    argv = list(sys.argv[1:] if argv is None else argv)
    root = Path(os.environ.get("TEST01_ROOT", repo_root()))
    if len(argv) >= 2:
        root = Path(argv[1])
    raw = root / "data/raw/test-01"
    results = root / "results/test-01"
    work = raw / "work"
    work.mkdir(parents=True, exist_ok=True)
    manifest_path = Path(
        os.environ.get("TEST01_SELECTION", results / "selection.json")
    )
    if len(argv) >= 1:
        manifest_path = Path(argv[0])
    sel = json.loads(manifest_path.read_text())
    # outgroup may have been updated in that file
    query_acc = sel["query"]
    # This runner implements the one-record, unsegmented-Q path used by Test 1.
    # Segmented or multi-record Q needs the protocol's per-segment aggregation
    # and C-mixed logic, which are not implemented here. Refuse those cases.
    if not isinstance(query_acc, str) or not query_acc.strip():
        raise SystemExit("Q must be a single accession.version string.")
    if sel.get("query_segs") or isinstance(sel.get("query"), list):
        raise SystemExit(
            "This runner does not implement segmented or multi-record Q "
            "(per-segment aggregation / C-mixed). Refusing to continue."
        )
    outgroup_acc = sel["outgroup"]
    flu_genomes = sel["flu_a"] + sel["flu_b"]
    cov_accs = list(sel["cov"].values())
    # Build genome objects for S_cov and outgroup (unsegmented = one "segment")
    def unseg(org, acc, length=None):
        # length filled from fasta
        return {
            "org": org,
            "subtype": None,
            "segs": [{"segment": 1, "accession": acc, "length": length}],
            "concat_header": acc,
        }

    cov_genomes = [
        unseg(label, acc) for label, acc in sel["cov"].items()
    ]
    outgroup_genome = unseg("outgroup", outgroup_acc)
    for g in flu_genomes:
        g["concat_header"] = g["segs"][0]["accession"]  # first in increasing segment number

    # Load sequences
    seqs = {}
    for p in (raw / "fasta/by-accession").glob("*.fasta"):
        recs = read_fa(p)
        if len(recs) != 1:
            raise SystemExit(f"expected one record in {p}")
        acc = p.stem
        seqs[acc] = recs[0][1]
    needed = [query_acc, outgroup_acc] + cov_accs
    for g in flu_genomes:
        needed.extend(s["accession"] for s in g["segs"])
    missing = [a for a in needed if a not in seqs]
    if missing:
        raise SystemExit(f"missing FASTA: {missing}")
    # fill lengths
    for g in flu_genomes + cov_genomes + [outgroup_genome]:
        for s in g["segs"]:
            s["length"] = len(seqs[s["accession"]])

    # Write BLAST input FASTA with accession.version headers
    q_fa = work / "Q.fa"
    sflu_fa = work / "S_flu.fa"
    scov_fa = work / "S_cov.fa"
    og_fa = work / "outgroup.fa"
    write_fa(q_fa, [(query_acc, seqs[query_acc])])
    write_fa(
        sflu_fa,
        [(s["accession"], seqs[s["accession"]]) for g in flu_genomes for s in g["segs"]],
    )
    write_fa(scov_fa, [(acc, seqs[acc]) for acc in cov_accs])
    write_fa(og_fa, [(outgroup_acc, seqs[outgroup_acc])])

    blast_dir = results / "blast"
    blast_dir.mkdir(parents=True, exist_ok=True)
    cmdlog = results / "run-logs" / "commands.log"
    cmdlog.parent.mkdir(parents=True, exist_ok=True)
    log_fh = cmdlog.open("a")
    log_fh.write(f"\n# BLAST/analysis commands start\n")

    bindir = Path("/opt/covid-tools/bin")
    makeblastdb = str(bindir / "makeblastdb")
    blastn = str(bindir / "blastn")
    mafft = str(bindir / "mafft")
    iqtree = str(bindir / "iqtree3")

    db_dir = work / "blast-db"
    if db_dir.exists():
        shutil.rmtree(db_dir)
    db_dir.mkdir()

    dbs = {"S_flu": sflu_fa, "S_cov": scov_fa, "outgroup": og_fa}
    for name, fa in dbs.items():
        run(
            [makeblastdb, "-in", str(fa), "-dbtype", "nucl", "-parse_seqids", "-out", name],
            cwd=db_dir,
            log_fh=log_fh,
        )

    blast_tables = {}
    for name in ("S_flu", "S_cov", "outgroup"):
        out = blast_dir / f"{query_acc}.{name}.tsv"
        run(
            [
                blastn,
                "-task",
                "blastn",
                "-query",
                str(q_fa),
                "-db",
                str(db_dir / name),
                "-evalue",
                "1e-5",
                "-max_target_seqs",
                "1000",
                "-max_hsps",
                "20",
                "-outfmt",
                "6 qseqid sacc sseqid pident length evalue bitscore qcovs qstart qend sstart send qlen slen",
                "-out",
                str(out),
            ],
            cwd=work,
            log_fh=log_fh,
        )
        raw_rows = parse_blast_tsv(out)
        if name == "S_flu":
            accs = genome_accessions(flu_genomes)
        elif name == "S_cov":
            accs = genome_accessions(cov_genomes)
        else:
            accs = genome_accessions([outgroup_genome])
        blast_tables[name] = resolve_blast_table(raw_rows, accs)

    # If sacc is empty/weird because of parse_seqids, fall back is not allowed;
    # report what we got.
    summary = {
        "query": query_acc,
        "outgroup": outgroup_acc,
        "S_flu_hits": [],
        "S_cov_hits": [],
        "outgroup_hits": [],
    }
    for g in flu_genomes:
        summary["S_flu_hits"].append(genome_hit(query_acc, blast_tables["S_flu"], g))
    for g in cov_genomes:
        summary["S_cov_hits"].append(genome_hit(query_acc, blast_tables["S_cov"], g))
    summary["outgroup_hits"].append(
        genome_hit(query_acc, blast_tables["outgroup"], outgroup_genome)
    )

    qlen_fa = len(seqs[query_acc])
    for group in ("S_flu_hits", "S_cov_hits", "outgroup_hits"):
        for h in summary[group]:
            if h.get("Qlen") is None:
                h["Qlen"] = qlen_fa

    flu_best, flu_tie = best_of_set(summary["S_flu_hits"])
    cov_best, cov_tie = best_of_set(summary["S_cov_hits"])
    q_has_flu = any(h["qualifying"] for h in summary["S_flu_hits"])
    q_has_cov = any(h["qualifying"] for h in summary["S_cov_hits"])
    q_has_og = any(h["qualifying"] for h in summary["outgroup_hits"])

    summary["q_has_qualifying_S_flu"] = q_has_flu
    summary["q_has_qualifying_S_cov"] = q_has_cov
    summary["q_has_qualifying_outgroup"] = q_has_og
    summary["S_flu_best"] = flu_best
    summary["S_cov_best"] = cov_best
    summary["S_flu_best_tied"] = flu_tie
    summary["S_cov_best_tied"] = cov_tie

    # Step 7
    combined_allowed = q_has_flu and q_has_cov
    one_sided = (q_has_flu and not q_has_cov) or (q_has_cov and not q_has_flu)
    summary["combined_alignment_allowed"] = combined_allowed
    summary["one_sided"] = one_sided

    letter = None
    subcode = None
    notes = []

    if not q_has_flu and not q_has_cov:
        letter, subcode = "C", "C-neither"
        notes.append("Query has no qualifying BLAST hit in either reference set.")
    elif one_sided and q_has_flu and not q_has_cov:
        letter, subcode = "A-blast", None
        notes.append("Each query has a qualifying hit in S_flu and no qualifying hit in S_cov. Combined tree not built.")
    elif one_sided and q_has_cov and not q_has_flu:
        letter, subcode = "B-blast", None
        notes.append("Each query has a qualifying hit in S_cov and no qualifying hit in S_flu. Combined tree not built.")
    elif combined_allowed:
        notes.append("Query has a qualifying hit in both S_flu and S_cov; combined alignment path is allowed.")
        if flu_tie or cov_tie:
            notes.append("A qualifying-bitscore tie is present; tree may still be built, but a bitscore bullet for A or B cannot pass if the compared best scores are tied.")
        if not q_has_og:
            notes.append("Outgroup homology gate failed (no qualifying hit from Q to the outgroup). Tree monophyly tests cannot be used. A-blast/B-blast do not hold because both sets have qualifying hits.")
            # Still report BLAST; C for tree. We may still attempt trim? Protocol says
            # do not use the outgroup to assess monophyly, apply C for the tree decision.
            # BLAST-only outcomes may still be used — but they don't hold here.
            letter, subcode = "C", "C-unrooted"
        else:
            # Site-homology trim, then maybe MAFFT / IQ-TREE
            letter, subcode = run_combined(
                query_acc,
                outgroup_acc,
                seqs,
                flu_genomes,
                cov_genomes,
                outgroup_genome,
                blast_tables,
                work,
                results,
                log_fh,
                mafft,
                iqtree,
                notes,
                flu_best,
                cov_best,
                flu_tie,
                cov_tie,
            )

    summary["decision_letter"] = letter
    summary["decision_subcode"] = subcode
    summary["notes"] = notes
    (results / "BLAST-SUMMARY.json").write_text(json.dumps(summary, indent=2, default=str))
    log_fh.close()
    print(f"DECISION {letter}" + (f" ({subcode})" if subcode else ""))
    print(f"qualifying S_flu={q_has_flu} S_cov={q_has_cov} outgroup={q_has_og}")
    return 0


def run_combined(
    query_acc,
    outgroup_acc,
    seqs,
    flu_genomes,
    cov_genomes,
    outgroup_genome,
    blast_tables,
    work,
    results,
    log_fh,
    mafft,
    iqtree,
    notes,
    flu_best,
    cov_best,
    flu_tie,
    cov_tie,
):
    ev = PROTOCOL_EVALUE
    # Intervals per accession (segment-level)
    keep = defaultdict(list)
    # Q: query intervals from HSPs against S_flu, S_cov, and outgroup
    for setname in ("S_flu", "S_cov", "outgroup"):
        for r in blast_tables[setname]:
            if r["evalue"] <= ev:
                keep[query_acc].append((r["qstart"], r["qend"]))
    # References and outgroup: subject intervals from HSPs against Q
    acc_to_setrow = {}
    for g in flu_genomes:
        for s in g["segs"]:
            acc_to_setrow[s["accession"]] = "S_flu"
    for g in cov_genomes:
        for s in g["segs"]:
            acc_to_setrow[s["accession"]] = "S_cov"
    acc_to_setrow[outgroup_acc] = "outgroup"
    for setname, rows in blast_tables.items():
        for r in rows:
            if r["evalue"] <= ev and r["sacc"] in acc_to_setrow:
                a, b = r["sstart"], r["send"]
                if a > b:
                    a, b = b, a
                keep[r["sacc"]].append((a, b))

    def genome_trimmed(genome):
        # Kept bases are the nucleotides in the merged BLAST intervals, not
        # counting the ten-N spacers inserted between disjoint intervals or
        # between segments.
        kept_strict = 0
        segs_out = []
        for s in genome["segs"]:
            acc = s["accession"]
            merged = merge_intervals(keep.get(acc, []))
            kept_strict += covered_bases(merged)
            segs_out.append(extract_trimmed(seqs[acc], keep.get(acc, [])))
        # Concatenate segments in increasing segment number with 10 N between segments
        # (empty segments: still follow spacer rule — a segment with zero kept bases
        # is an empty part; we do not drop the genome unless the whole genome is empty.)
        # If a middle segment is empty, joining with spacers can introduce extra N.
        # Protocol: "Write the trimmed sequence in the existing segment order, inserting
        # a spacer of ten N characters between disjoint kept intervals on the same
        # segment and between segments as already specified."
        # Only include empty as nothing between spacers if we still concat all segments.
        # Safer reading: concatenate the (possibly empty) per-segment trimmed strings
        # with 10 N between segments. If a segment is empty, that can yield leading/
        # extra N, which the gap filter will drop. Zero kept bases is determined
        # from interval coverage, not from N.
        trimmed = SPACER.join(segs_out)
        header = genome["concat_header"]
        return header, trimmed, kept_strict

    required = []
    required.append(("Q", {"org": "Q", "segs": [{"segment": 1, "accession": query_acc}], "concat_header": query_acc}))
    for g in flu_genomes:
        required.append(("S_flu", g))
    for g in cov_genomes:
        required.append(("S_cov", g))
    required.append(("outgroup", outgroup_genome))

    trimmed_recs = []
    zero = []
    trim_info = []
    for kind, g in required:
        header, trimmed, kept = genome_trimmed(g)
        trim_info.append({"kind": kind, "org": g.get("org"), "header": header, "kept_bases": kept, "trimmed_len": len(trimmed)})
        if kept == 0:
            zero.append({"kind": kind, "org": g.get("org"), "header": header})
        trimmed_recs.append((header, trimmed))

    (results / "TRIM-INFO.json").write_text(json.dumps({"intervals_note": "kept bases exclude N spacers", "zero": zero, "genomes": trim_info}, indent=2))
    if zero:
        notes.append(
            "Site-homology trim left zero kept bases in at least one required genome; "
            "MAFFT and IQ-TREE were not run (C-homology). Zero genomes: "
            + ", ".join(f"{z['kind']}:{z['org']}:{z['header']}" for z in zero)
        )
        return "C", "C-homology"

    in_fa = work / "combined.trimmed.fa"
    write_fa(in_fa, trimmed_recs)
    aln_fa = work / "aln.fa"
    # Pinned MAFFT command. stdout is the alignment.
    env = os.environ.copy()
    proc = subprocess.run(
        ["nice", "-n", "19", mafft, "--auto", "--maxiterate", "1000", "--thread", "1", str(in_fa)],
        cwd=str(work),
        env=env,
        text=True,
        capture_output=True,
    )
    log_fh.write(f"$ {mafft} --auto --maxiterate 1000 --thread 1 {in_fa}\n")
    log_fh.write(proc.stderr)
    log_fh.write(f"# exit={proc.returncode}\n")
    log_fh.flush()
    if proc.returncode != 0:
        raise SystemExit(f"mafft failed: {proc.stderr}")
    aln_fa.write_text(proc.stdout)

    # Column filter: drop columns whose gap fraction > 0.50
    aln = read_fa(aln_fa)
    if not aln:
        notes.append("MAFFT produced an empty alignment.")
        return "C", "C-alignment"
    L = {len(s) for _, s in aln}
    if len(L) != 1:
        notes.append("MAFFT alignment sequences have different lengths.")
        return "C", "C-alignment"
    alen = L.pop()
    keep_cols = []
    for i in range(alen):
        gap = sum(1 for _, s in aln if s[i] == "-") / len(aln)
        if gap <= GAP_FRACTION:
            keep_cols.append(i)
    filtered = [(n, "".join(s[i] for i in keep_cols)) for n, s in aln]
    aln_filtered = work / "aln.filtered.fa"
    write_fa(aln_filtered, filtered)
    n_cols = len(keep_cols)
    notes.append(f"Column filter: {alen} aligned columns, {n_cols} remaining after dropping gap fraction > 0.50.")
    if n_cols < MIN_COLUMNS:
        notes.append(f"Fewer than {MIN_COLUMNS} columns remain; alignment is not informative.")
        return "C", "C-alignment"

    ident_script = Path("/workspace/covid/results/test-01/run-logs/identity-gate-script.py")
    ident_out = work / "identity-gate.txt"
    proc = subprocess.run(
        ["nice", "-n", "19", sys.executable, str(ident_script), str(aln_filtered)],
        cwd=str(work),
        text=True,
        capture_output=True,
    )
    log_fh.write(f"$ {sys.executable} {ident_script} {aln_filtered}\n")
    log_fh.write(proc.stdout)
    log_fh.write(proc.stderr)
    log_fh.write(f"# exit={proc.returncode}\n")
    log_fh.flush()
    ident_out.write_text(proc.stdout + proc.stderr)
    if proc.returncode != 0:
        notes.append(f"Identity-gate script failed or reported no pairs: {proc.stdout.strip()} {proc.stderr.strip()}")
        return "C", "C-alignment"
    # parse MEAN_PAIRWISE_IDENTITY=
    mean_id = None
    for tok in proc.stdout.split():
        if tok.startswith("MEAN_PAIRWISE_IDENTITY="):
            val = tok.split("=", 1)[1]
            if val != "NA":
                mean_id = float(val)
    notes.append(f"Identity gate output: {proc.stdout.strip()}")
    if mean_id is None or mean_id < MIN_IDENTITY:
        notes.append(f"Mean pairwise identity {mean_id} is below {MIN_IDENTITY:.0%} or NA.")
        return "C", "C-alignment"

    # IQ-TREE in a new empty directory
    iq_dir = results / "iqtree-attempt-1"
    if iq_dir.exists():
        raise SystemExit(f"IQ-TREE directory already exists: {iq_dir}")
    iq_dir.mkdir()
    # copy alignment into that directory so the run is self-contained (alignment also stays in work)
    aln_copy = iq_dir / "aln.filtered.fa"
    # .fa will be gitignored under results/test-01; that is intended.
    shutil.copy2(aln_filtered, aln_copy)
    cmd = [
        iqtree,
        "-s",
        str(aln_copy),
        "-m",
        "MFP",
        "--ufboot",
        "1000",
        "--alrt",
        "1000",
        "--seed",
        SEED,
        "-T",
        THREADS,
        "-o",
        outgroup_acc,
        "-pre",
        "test01",
    ]
    run(cmd, cwd=iq_dir, log_fh=log_fh)
    notes.append(f"IQ-TREE ran in {iq_dir} with --seed {SEED} -T {THREADS} -o {outgroup_acc}.")

    treefile = iq_dir / "test01.treefile"
    report = iq_dir / "test01.iqtree"
    if not treefile.exists() or not report.exists():
        notes.append("IQ-TREE did not write the expected treefile or report.")
        return "C", "C-alignment"

    # Parse support and topology from the treefile (Newick with UFBoot/SH-aLRT labels)
    tree_text = treefile.read_text().strip()
    (results / "iqtree-attempt-1-treefile-copy.nwk.txt").write_text(tree_text + "\n")

    decision, sub, tree_notes = apply_tree_rule(
        tree_text,
        report.read_text(),
        query_acc,
        outgroup_acc,
        flu_genomes,
        cov_genomes,
        flu_best,
        cov_best,
        flu_tie,
        cov_tie,
    )
    notes.extend(tree_notes)
    return decision, sub


def parse_newick_bipartitions(newick: str):
    """Parse a Newick string with numeric support labels; return (clade_set, support) list.

    Supports IQ-TREE labels of the form )85.4/98 or )98 or )85.4. Leaves are tokens
    before ':' or ',' or ')'. The outgroup-rooting split is just another bipartition.
    """
    s = newick.strip()
    if s.endswith(";"):
        s = s[:-1]
    i = 0
    n = len(s)
    stack = [[]]  # list of leaf-name lists
    supports = []  # (frozenset(leaves in clade), label_string, size)

    def read_name(j):
        start = j
        while j < n and s[j] not in ",():;":
            j += 1
        return s[start:j].strip(), j

    while i < n:
        c = s[i]
        if c == "(":
            stack.append([])
            i += 1
        elif c == ",":
            i += 1
        elif c == ")":
            i += 1
            label = ""
            if i < n and s[i] not in ",():;":
                label, i = read_name(i)
            if i < n and s[i] == ":":
                i += 1
                # skip branch length
                while i < n and s[i] not in ",():;":
                    i += 1
            clade = stack.pop()
            if not stack:
                raise SystemExit("Newick parse underflow")
            stack[-1].extend(clade)
            supports.append((frozenset(clade), label, len(clade)))
        elif c == ":":
            # branch length after a leaf
            i += 1
            while i < n and s[i] not in ",():;":
                i += 1
        else:
            name, i = read_name(i)
            if name:
                # strip quotes
                if (name.startswith("'") and name.endswith("'")) or (
                    name.startswith('"') and name.endswith('"')
                ):
                    name = name[1:-1]
                stack[-1].append(name)
            if i < n and s[i] == ":":
                i += 1
                while i < n and s[i] not in ",():;":
                    i += 1
    all_leaves = frozenset(stack[0])
    return all_leaves, supports


def parse_support_label(label: str):
    """Return (sh_alrt, ufboot) as floats, or (None, None) if unusable.

    IQ-TREE with --alrt and --ufboot typically prints SH-aLRT/UFBoot on branches.
    """
    if not label:
        return None, None
    label = label.strip()
    if "/" in label:
        a, b = label.split("/", 1)
        try:
            return float(a), float(b)
        except ValueError:
            return None, None
    try:
        return None, float(label)
    except ValueError:
        return None, None


def apply_tree_rule(
    newick,
    report_text,
    query_acc,
    outgroup_acc,
    flu_genomes,
    cov_genomes,
    flu_best,
    cov_best,
    flu_tie,
    cov_tie,
):
    notes = []
    if "UNROOTED" in report_text:
        notes.append("IQ-TREE report contains the string UNROOTED (informational under a reversible model; not by itself C-unrooted).")
    leaves, parts = parse_newick_bipartitions(newick)
    notes.append(f"Parsed {len(leaves)} leaves from the treefile: {', '.join(sorted(leaves))}.")

    flu_headers = {g["concat_header"] for g in flu_genomes}
    cov_headers = {g["concat_header"] for g in cov_genomes}
    expected = {query_acc, outgroup_acc} | flu_headers | cov_headers
    if leaves != expected:
        notes.append(
            f"Treefile leaf set does not exactly match the required taxa. "
            f"missing={sorted(expected-leaves)} extra={sorted(leaves-expected)}"
        )
        return "C", "C-alignment", notes

    # Outgroup must form a single split from all other taxa
    ingroup = leaves - {outgroup_acc}
    og_ok = False
    for clade, label, _ in parts:
        other = leaves - clade
        if clade == {outgroup_acc} or other == {outgroup_acc}:
            og_ok = True
            notes.append(f"Outgroup split found with label {label!r}.")
            break
    if not og_ok:
        notes.append("Outgroup does not form a single split from all other taxa.")
        return "C", "C-unrooted", notes

    def support_for(group_a, group_b):
        """Find the bipartition {group_a} | {group_b union maybe already complete}.

        Critical branch for A is {Q ∪ S_flu} | {S_cov ∪ outgroup}.
        """
        want = frozenset(group_a)
        other = frozenset(group_b)
        if want | other != leaves:
            return None, None, None
        for clade, label, _ in parts:
            if clade == want or (leaves - clade) == want:
                sh, uf = parse_support_label(label)
                return sh, uf, label
        return None, None, None

    group_a = {query_acc} | flu_headers
    group_b = cov_headers | {outgroup_acc}
    sh_a, uf_a, lab_a = support_for(group_a, group_b)
    group_b_only = {query_acc} | cov_headers
    group_a_only = flu_headers | {outgroup_acc}
    sh_b, uf_b, lab_b = support_for(group_b_only, group_a_only)

    def pass_support(sh, uf, lab, name):
        notes.append(f"Critical branch {name}: label={lab!r} SH-aLRT={sh} UFBoot={uf}.")
        if sh is None or uf is None:
            notes.append(f"Could not parse both SH-aLRT and UFBoot for {name}.")
            return False
        ok = (uf >= UFBOOT_MIN) and (sh >= SHALRT_MIN)
        if not ok:
            notes.append(f"{name} support below thresholds (need UFBoot >= {UFBOOT_MIN} and SH-aLRT >= {SHALRT_MIN}).")
        return ok

    topo_a = sh_a is not None or (lab_a is not None)
    # support_for returns None label if bipartition absent
    has_a = lab_a is not None
    has_b = lab_b is not None
    notes.append(f"Bipartition {{Q ∪ S_flu}} | {{S_cov ∪ outgroup}} present={has_a}.")
    notes.append(f"Bipartition {{Q ∪ S_cov}} | {{S_flu ∪ outgroup}} present={has_b}.")

    # Bitscores
    def best_score(best, tie):
        if not best:
            return None, tie
        return best[0]["bitscore_max"], tie

    flu_score, _ = best_score(flu_best, flu_tie)
    cov_score, _ = best_score(cov_best, cov_tie)
    notes.append(f"Best qualifying bitscores: S_flu={flu_score} (tied={flu_tie}), S_cov={cov_score} (tied={cov_tie}).")

    # The rule compares each query's best S_flu bitscore with its best S_cov
    # bitscore. A tie among genomes inside one set is reported and is not
    # broken by judgment, but it does not block a strict cross-set comparison.
    a_bits = flu_score is not None and cov_score is not None and flu_score > cov_score
    b_bits = flu_score is not None and cov_score is not None and cov_score > flu_score
    if flu_score is not None and cov_score is not None and flu_score == cov_score:
        notes.append("Best qualifying bitscores are tied.")

    a_tree = has_a and pass_support(sh_a, uf_a, lab_a, "A")
    b_tree = has_b and pass_support(sh_b, uf_b, lab_b, "B")

    # A-nested if A holds
    def nested_ok():
        # supported clade containing Q and a proper nonempty subset of S_flu,
        # excluding at least one other S_flu genome
        if len(flu_headers) < 2:
            notes.append("A-nested cannot be reached: fewer than two S_flu genomes.")
            return False
        found = False
        for clade, label, _ in parts:
            # consider both sides? The clade that contains Q
            for side in (clade, leaves - clade):
                if query_acc not in side:
                    continue
                if outgroup_acc in side:
                    continue
                # may or may not include cov; nesting test: contains Q and proper nonempty subset of S_flu
                # and excludes at least one other S_flu. The protocol: "a supported clade that
                # contains Q and a proper, non-empty subset of S_flu and that excludes at least
                # one other S_flu genome".
                flu_in = side & flu_headers
                if not flu_in or flu_in == flu_headers:
                    continue
                # proper nonempty subset already implied
                sh, uf = parse_support_label(label)
                if sh is None or uf is None:
                    continue
                if uf >= UFBOOT_MIN and sh >= SHALRT_MIN:
                    notes.append(
                        f"A-nested candidate clade {sorted(side)} label={label!r} SH-aLRT={sh} UFBoot={uf}."
                    )
                    found = True
                    return True
        if not found:
            notes.append("No supported A-nested clade was found.")
        return False

    if a_tree and a_bits and not b_tree:
        if nested_ok():
            return "A-nested", None, notes
        return "A", None, notes
    if b_tree and b_bits and not a_tree:
        return "B", None, notes
    if (a_tree and b_tree) or (a_tree and not a_bits) or (b_tree and not b_bits):
        notes.append("Tree topology and BLAST bitscores disagree, or both A and B topologies were supported.")
        return "C", "C-BLAST", notes
    if not a_tree and not b_tree:
        # groups with neither, or support missing
        if not has_a and not has_b:
            notes.append("Supported rooted topology places Q with neither {{Q+S_flu}} nor {{Q+S_cov}}, or those splits are absent.")
            return "C", "C-neither", notes
        return "C", "C-support", notes
    return "C", None, notes


if __name__ == "__main__":
    sys.exit(main())
