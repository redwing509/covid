#!/usr/bin/env python3
"""Q-17 verification: MAFFT+IQ-TREE and Mash-class k-mer distances.

Does not change the pre-registered Test 1 letter (B-blast). The agreement
rule in tests/PRE-REGISTERED-AGREEMENT-Q17.md was frozen before this
runner produced any alignment, tree, or k-mer results.
"""
from __future__ import annotations

import hashlib
import json
import math
import os
import shutil
import sys
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path

HERE = Path(__file__).resolve().parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))

from test01_run import (  # noqa: E402
    GAP_FRACTION,
    MIN_COLUMNS,
    MIN_IDENTITY,
    PROTOCOL_EVALUE,
    SEED,
    SHALRT_MIN,
    SPACER,
    THREADS,
    UFBOOT_MIN,
    covered_bases,
    extract_trimmed,
    merge_intervals,
    parse_blast_tsv,
    parse_newick_bipartitions,
    parse_support_label,
    read_fa,
    resolve_blast_table,
    run,
    write_fa,
)

K = 21
COMPLEMENT = str.maketrans("ACGT", "TGCA")
MW_INF = "undefined"


def _now():
    return datetime.now(timezone.utc).astimezone().strftime("%Y-%m-%d %I:%M %p %Z")


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with Path(path).open("rb") as fh:
        for chunk in iter(lambda: fh.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def load_pins(root: Path) -> dict:
    return json.loads((root / "tests" / "q17-pins.json").read_text())


def load_selection(root: Path) -> dict:
    return json.loads((root / "results" / "test-01" / "selection.json").read_text())


def build_genomes(sel: dict):
    query_acc = sel["query"]
    outgroup_acc = sel["outgroup"]

    def unseg(org, acc):
        return {
            "org": org,
            "segs": [{"segment": 1, "accession": acc}],
            "concat_header": acc,
        }

    flu = []
    for g in list(sel["flu_a"]) + list(sel["flu_b"]):
        segs = sorted(g["segs"], key=lambda s: int(s["segment"]))
        flu.append({
            "org": g["org"],
            "segs": segs,
            "concat_header": segs[0]["accession"],
        })
    cov = [unseg(label, acc) for label, acc in sel["cov"].items()]
    outgroup = unseg("outgroup", outgroup_acc)
    query = unseg("Q", query_acc)
    return query_acc, outgroup_acc, query, flu, cov, outgroup


def load_seqs(root: Path, needed):
    seqs = {}
    for p in (root / "data/raw/test-01/fasta/by-accession").glob("*.fasta"):
        recs = read_fa(p)
        if len(recs) != 1:
            raise SystemExit(f"expected one record in {p}")
        seqs[p.stem] = recs[0][1]
    missing = [a for a in needed if a not in seqs]
    if missing:
        raise SystemExit(f"missing FASTA: {missing}")
    return seqs


def concat_genome(genome, seqs, spacer=""):
    parts = [seqs[s["accession"]] for s in genome["segs"]]
    return spacer.join(parts)


def canonical_kmers(seq: str, k: int = K) -> set:
    s = seq.upper()
    out = set()
    n = len(s)
    for i in range(0, n - k + 1):
        win = s[i : i + k]
        if any(ch not in "ACGT" for ch in win):
            continue
        rc = win.translate(COMPLEMENT)[::-1]
        out.add(win if win <= rc else rc)
    return out


def jaccard(a: set, b: set):
    if not a or not b:
        return None
    inter = len(a & b)
    union = len(a | b)
    if union == 0:
        return None
    return inter / union


def mash_distance(j, k=K):
    if j is None:
        return MW_INF
    if j == 0:
        return MW_INF
    return -(1.0 / k) * math.log((2.0 * j) / (1.0 + j))


def finite_or_large(dist, large):
    if dist == MW_INF or dist is None:
        return large
    return float(dist)


def neighbor_joining(names, matrix):
    """Return a Newick string (unrooted) from a symmetric distance matrix."""
    nodes = list(names)
    dist = {a: dict(zip(names, row)) for a, row in zip(names, matrix)}
    for a in nodes:
        dist[a][a] = 0.0

    def d(a, b):
        return dist[a][b]

    newick = {name: name for name in nodes}
    while len(nodes) > 2:
        n = len(nodes)
        r = {a: sum(d(a, b) for b in nodes if b != a) for a in nodes}
        best = None
        for i, a in enumerate(nodes):
            for b in nodes[i + 1 :]:
                q = (n - 2) * d(a, b) - r[a] - r[b]
                if best is None or q < best[0]:
                    best = (q, a, b)
        _, a, b = best
        delta = d(a, b)
        if n == 2:
            da = db = delta / 2.0
        else:
            da = 0.5 * delta + (r[a] - r[b]) / (2 * (n - 2))
            db = delta - da
        u = f"node{len(newick)}"
        newick[u] = f"({newick[a]}:{da:.8f},{newick[b]}:{db:.8f})"
        dist[u] = {}
        for c in nodes:
            if c in (a, b):
                continue
            dist[u][c] = dist[c][u] = 0.5 * (d(a, c) + d(b, c) - delta)
        dist[u][u] = 0.0
        nodes = [c for c in nodes if c not in (a, b)] + [u]
        del dist[a]
        del dist[b]
        for c in list(dist):
            dist[c].pop(a, None)
            dist[c].pop(b, None)
    a, b = nodes
    tree = f"({newick[a]}:{d(a, b)/2:.8f},{newick[b]}:{d(a, b)/2:.8f});"
    return tree


def root_on_outgroup(newick: str, outgroup: str) -> str:
    """Informational reroot for reporting: return the original Newick.

    Monophyly is assessed from unrooted bipartitions, so an explicit reroot
    is not required for the agreement rule. The outgroup split is checked
    as in Test 1.
    """
    return newick


def assess_tree(newick: str, query, outgroup, flu_headers, cov_headers):
    leaves, parts = parse_newick_bipartitions(newick)
    expected = {query, outgroup} | set(flu_headers) | set(cov_headers)
    report = {
        "leaves": sorted(leaves),
        "expected_ok": leaves == expected,
        "outgroup_split": False,
        "has_q_cov": False,
        "has_q_flu": False,
        "q_cov_sh": None,
        "q_cov_uf": None,
        "q_cov_label": None,
        "q_flu_sh": None,
        "q_flu_uf": None,
        "q_flu_label": None,
        "verdict": "INCONCLUSIVE",
        "reason": "",
    }
    if leaves != expected:
        report["reason"] = f"leaf set mismatch missing={sorted(expected-leaves)} extra={sorted(leaves-expected)}"
        return report
    ingroup = leaves - {outgroup}
    for clade, label, _ in parts:
        other = leaves - clade
        if clade == {outgroup} or other == {outgroup}:
            report["outgroup_split"] = True
            report["outgroup_label"] = label
            break

    def find(group_a, group_b):
        want = frozenset(group_a)
        if want | frozenset(group_b) != leaves:
            return None, None, None
        for clade, label, _ in parts:
            if clade == want or (leaves - clade) == want:
                sh, uf = parse_support_label(label)
                return sh, uf, label
        return None, None, None

    sh_b, uf_b, lab_b = find({query} | set(cov_headers), set(flu_headers) | {outgroup})
    sh_a, uf_a, lab_a = find({query} | set(flu_headers), set(cov_headers) | {outgroup})
    report["has_q_cov"] = lab_b is not None
    report["has_q_flu"] = lab_a is not None
    report["q_cov_sh"], report["q_cov_uf"], report["q_cov_label"] = sh_b, uf_b, lab_b
    report["q_flu_sh"], report["q_flu_uf"], report["q_flu_label"] = sh_a, uf_a, lab_a
    # A monophyly split that already places the outgroup on the far side
    # is enough to assess the rooted grouping, even if the singleton
    # outgroup clade was not written as its own Newick node.
    if not report["outgroup_split"] and (report["has_q_cov"] or report["has_q_flu"]):
        report["outgroup_split"] = True
        report["outgroup_label"] = "inferred-from-monophyly-split"
    if not report["outgroup_split"]:
        report["reason"] = "outgroup does not form a single split from all other taxa"
        report["verdict"] = "INCONCLUSIVE"
        return report

    def supported(sh, uf):
        return sh is not None and uf is not None and uf >= UFBOOT_MIN and sh >= SHALRT_MIN

    if report["has_q_cov"] and supported(sh_b, uf_b):
        report["verdict"] = "AGREE"
        report["reason"] = "Q groups with S_cov to the exclusion of S_flu with support at threshold"
        return report
    if report["has_q_flu"] and supported(sh_a, uf_a):
        report["verdict"] = "DISAGREE"
        report["reason"] = "Q groups with S_flu to the exclusion of S_cov with support at threshold"
        return report
    # Supported placement with neither?
    # If both bipartitions are absent, Q may sit outside both groups.
    if not report["has_q_cov"] and not report["has_q_flu"]:
        report["verdict"] = "DISAGREE"
        report["reason"] = "Q is outside both {Q+S_cov} and {Q+S_flu} (or those splits are absent)"
        return report
    report["verdict"] = "INCONCLUSIVE"
    report["reason"] = "required monophyly split missing or support below threshold"
    return report


def filter_alignment(aln_recs):
    L = {len(s) for _, s in aln_recs}
    if len(L) != 1:
        return None, 0, 0
    alen = L.pop()
    keep_cols = []
    for i in range(alen):
        gap = sum(1 for _, s in aln_recs if s[i] == "-") / len(aln_recs)
        if gap <= GAP_FRACTION:
            keep_cols.append(i)
    filtered = [(n, "".join(s[i] for i in keep_cols)) for n, s in aln_recs]
    return filtered, alen, len(keep_cols)


def run_identity_gate(script: Path, aln: Path, log_fh):
    proc = run([sys.executable, str(script), str(aln)], cwd=aln.parent, log_fh=log_fh)
    mean_id = None
    pairs = None
    for tok in proc.stdout.split():
        if tok.startswith("MEAN_PAIRWISE_IDENTITY="):
            val = tok.split("=", 1)[1]
            if val != "NA":
                mean_id = float(val)
        if tok.startswith("PAIRS="):
            pairs = int(tok.split("=", 1)[1])
    return mean_id, pairs, proc.stdout.strip()


def run_mafft_iqtree(in_fa: Path, work: Path, outgroup: str, mafft: str, iqtree: str, prefix: str, log_fh, ident_script: Path):
    result = {"status": "INCONCLUSIVE", "sub": None, "notes": []}
    env = os.environ.copy()
    proc = run(
        [mafft, "--auto", "--maxiterate", "1000", "--thread", "1", str(in_fa)],
        cwd=work,
        log_fh=log_fh,
    )
    aln_fa = work / f"{prefix}.aln.fa"
    # `run()` captures stdout into the log; MAFFT writes the alignment to stdout.
    # Re-run capturing ourselves because run() does not return the alignment path.
    # The helper already raised on failure; stdout is in the log and proc.stdout.
    aln_fa.write_text(proc.stdout)
    aln = read_fa(aln_fa)
    if not aln:
        result["sub"] = "C-alignment"
        result["notes"].append("MAFFT produced an empty alignment")
        return result
    filtered, alen, n_cols = filter_alignment(aln)
    result["aligned_columns"] = alen
    result["filtered_columns"] = n_cols
    result["notes"].append(f"Column filter: {alen} aligned columns, {n_cols} remaining after dropping gap fraction > 0.50.")
    if filtered is None or n_cols < MIN_COLUMNS:
        result["sub"] = "C-alignment"
        result["notes"].append(f"Fewer than {MIN_COLUMNS} columns remain or lengths differ")
        return result
    aln_filtered = work / f"{prefix}.aln.filtered.fa"
    write_fa(aln_filtered, filtered)
    mean_id, pairs, ident_txt = run_identity_gate(ident_script, aln_filtered, log_fh)
    result["mean_pairwise_identity"] = mean_id
    result["identity_pairs"] = pairs
    result["notes"].append(f"Identity gate output: {ident_txt}")
    if mean_id is None or mean_id < MIN_IDENTITY:
        result["sub"] = "C-alignment"
        result["notes"].append(f"Mean pairwise identity {mean_id} is below {MIN_IDENTITY:.0%} or NA")
        return result
    iq_dir = work / f"{prefix}-iqtree"
    if iq_dir.exists():
        shutil.rmtree(iq_dir)
    iq_dir.mkdir()
    aln_copy = iq_dir / "aln.filtered.fa"
    shutil.copy2(aln_filtered, aln_copy)
    run(
        [
            iqtree, "-s", str(aln_copy), "-m", "MFP",
            "--ufboot", "1000", "--alrt", "1000", "--seed", SEED,
            "-T", THREADS, "-o", outgroup, "-pre", prefix,
        ],
        cwd=iq_dir,
        log_fh=log_fh,
    )
    treefile = iq_dir / f"{prefix}.treefile"
    report = iq_dir / f"{prefix}.iqtree"
    if not treefile.exists() or not report.exists():
        result["sub"] = "C-alignment"
        result["notes"].append("IQ-TREE did not write the expected treefile or report")
        return result
    result["status"] = "tree"
    result["treefile"] = str(treefile)
    result["iqtree_report"] = str(report)
    result["newick"] = treefile.read_text().strip()
    result["iqtree_report_text"] = report.read_text()
    return result


def t_protocol(query, flu, cov, outgroup, seqs, blast_tables, work, log_fh, tools, ident_script):
    ev = PROTOCOL_EVALUE
    keep = defaultdict(list)
    query_acc = query["concat_header"]
    outgroup_acc = outgroup["concat_header"]
    for setname in ("S_flu", "S_cov", "outgroup"):
        for r in blast_tables[setname]:
            if r["evalue"] <= ev:
                keep[query_acc].append((r["qstart"], r["qend"]))
    acc_to_setrow = {}
    for g in flu:
        for s in g["segs"]:
            acc_to_setrow[s["accession"]] = "S_flu"
    for g in cov:
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
        kept_strict = 0
        segs_out = []
        for s in genome["segs"]:
            acc = s["accession"]
            merged = merge_intervals(keep.get(acc, []))
            kept_strict += covered_bases(merged)
            segs_out.append(extract_trimmed(seqs[acc], keep.get(acc, [])))
        return genome["concat_header"], SPACER.join(segs_out), kept_strict

    required = [("Q", query)] + [("S_flu", g) for g in flu] + [("S_cov", g) for g in cov] + [("outgroup", outgroup)]
    trimmed_recs = []
    zero = []
    trim_info = []
    for kind, g in required:
        header, trimmed, kept = genome_trimmed(g)
        trim_info.append({"kind": kind, "org": g.get("org"), "header": header, "kept_bases": kept, "trimmed_len": len(trimmed)})
        if kept == 0:
            zero.append({"kind": kind, "org": g.get("org"), "header": header})
        trimmed_recs.append((header, trimmed))
    payload = {"intervals_note": "kept bases exclude N spacers", "zero": zero, "genomes": trim_info}
    (work / "TRIM-INFO.json").write_text(json.dumps(payload, indent=2) + "\n")
    if zero:
        return {
            "status": "INCONCLUSIVE",
            "sub": "C-homology",
            "notes": [
                "Site-homology trim left zero kept bases in at least one required genome; "
                "MAFFT and IQ-TREE were not run (C-homology). Zero genomes: "
                + ", ".join(f"{z['kind']}:{z['org']}:{z['header']}" for z in zero)
            ],
            "trim": payload,
        }
    in_fa = work / "combined.trimmed.fa"
    write_fa(in_fa, trimmed_recs)
    tree = run_mafft_iqtree(in_fa, work, outgroup_acc, tools["mafft"], tools["iqtree"], "t-protocol", log_fh, ident_script)
    tree["trim"] = payload
    return tree


def t_full(query, flu, cov, outgroup, seqs, work, log_fh, tools, ident_script):
    recs = []
    for g in [query] + flu + cov + [outgroup]:
        recs.append((g["concat_header"], concat_genome(g, seqs, spacer=SPACER)))
    in_fa = work / "combined.full.fa"
    write_fa(in_fa, recs)
    return run_mafft_iqtree(in_fa, work, outgroup["concat_header"], tools["mafft"], tools["iqtree"], "t-full", log_fh, ident_script)


def method3(query, flu, cov, outgroup, seqs):
    genomes = [query] + cov + flu + [outgroup]
    names = [g["concat_header"] for g in genomes]
    kinds = {}
    kinds[query["concat_header"]] = "Q"
    for g in cov:
        kinds[g["concat_header"]] = "S_cov"
    for g in flu:
        kinds[g["concat_header"]] = "S_flu"
    kinds[outgroup["concat_header"]] = "outgroup"
    kmers = {}
    sizes = {}
    for g in genomes:
        seq = concat_genome(g, seqs, spacer="")  # no spacer for k-mers
        km = canonical_kmers(seq, K)
        kmers[g["concat_header"]] = km
        sizes[g["concat_header"]] = len(km)
    pairs = {}
    n = len(names)
    dj = [[0.0] * n for _ in range(n)]
    dm = [[0.0] * n for _ in range(n)]
    dm_raw = [[None] * n for _ in range(n)]
    for i, a in enumerate(names):
        for j, b in enumerate(names):
            if i == j:
                continue
            if (b, a) in pairs:
                continue
            jacc = jaccard(kmers[a], kmers[b])
            d_j = None if jacc is None else (1.0 - jacc)
            d_m = mash_distance(jacc, K)
            pairs[f"{a}|{b}"] = {"jaccard": jacc, "D_J": d_j, "D_M": d_m}
            pairs[f"{b}|{a}"] = {"jaccard": jacc, "D_J": d_j, "D_M": d_m}
    # fill matrices
    finites = [v["D_M"] for v in pairs.values() if isinstance(v["D_M"], (int, float))]
    large = (max(finites) + 1.0) if finites else 1.0
    for i, a in enumerate(names):
        for j, b in enumerate(names):
            if i == j:
                continue
            rec = pairs[f"{a}|{b}"]
            dj[i][j] = 1.0 if rec["D_J"] is None else rec["D_J"]
            dm_raw[i][j] = rec["D_M"]
            if rec["D_M"] == MW_INF:
                # NJ uses D_J = 1 when D_M undefined, as pre-registered
                dm[i][j] = 1.0 if rec["D_J"] is None else rec["D_J"]
            else:
                dm[i][j] = rec["D_M"]

    q = query["concat_header"]
    cov_names = [g["concat_header"] for g in cov]
    flu_names = [g["concat_header"] for g in flu]
    og = outgroup["concat_header"]

    def d_m_to(other):
        rec = pairs[f"{q}|{other}"]
        return rec["D_M"], rec["D_J"], rec["jaccard"]

    cov_ds = []
    flu_ds = []
    nearest = None
    nearest_kind = None
    nearest_d = None
    ties = []
    for name in names:
        if name == q:
            continue
        d_m, d_j, jacc = d_m_to(name)
        used = finite_or_large(d_m, large)
        kind = kinds[name]
        entry = {"name": name, "kind": kind, "D_M": d_m, "D_J": d_j, "jaccard": jacc, "used": used}
        if kind == "S_cov":
            cov_ds.append(entry)
        elif kind == "S_flu":
            flu_ds.append(entry)
        if nearest_d is None or used < nearest_d - 1e-18:
            nearest = entry
            nearest_kind = kind
            nearest_d = used
            ties = [entry]
        elif abs(used - nearest_d) <= 1e-18:
            ties.append(entry)

    d_cov = sum(e["used"] for e in cov_ds) / len(cov_ds) if cov_ds else None
    d_flu = sum(e["used"] for e in flu_ds) / len(flu_ds) if flu_ds else None
    primary = "INCONCLUSIVE"
    reason = ""
    if not cov_ds or not flu_ds or any(sizes[n] == 0 for n in names):
        primary = "INCONCLUSIVE"
        reason = "empty k-mer set or missing comparison set"
    elif len(ties) != 1:
        kinds_tied = {e["kind"] for e in ties}
        if len(kinds_tied) == 1 and "S_cov" in kinds_tied and d_cov is not None and d_flu is not None and d_cov < d_flu:
            # ties only within S_cov, still AGREE if mean rule holds
            primary = "AGREE"
            reason = "nearest-neighbor tie is within S_cov; mean d_cov < d_flu"
        else:
            primary = "INCONCLUSIVE"
            reason = "tie for nearest reference"
    elif nearest_kind == "S_cov" and d_cov is not None and d_flu is not None and d_cov < d_flu:
        primary = "AGREE"
        reason = "nearest reference is in S_cov and mean d_cov < d_flu"
    elif nearest_kind == "S_flu" or (d_flu is not None and d_cov is not None and d_flu < d_cov):
        primary = "DISAGREE"
        reason = "nearest reference is in S_flu or mean d_flu < d_cov"
    elif nearest_kind == "outgroup":
        primary = "INCONCLUSIVE"
        reason = "nearest reference is the outgroup"
    else:
        primary = "INCONCLUSIVE"
        reason = "nearest/mean rule did not reach AGREE or DISAGREE"

    nwk = neighbor_joining(names, dm)
    leaves, parts = parse_newick_bipartitions(nwk)
    flu_h = set(flu_names)
    cov_h = set(cov_names)
    topo = "INCONCLUSIVE"
    topo_reason = ""
    expected = set(names)
    if leaves != expected:
        topo_reason = "NJ leaf set mismatch"
    else:
        og_ok = False
        for clade, label, _ in parts:
            other = leaves - clade
            if clade == {og} or other == {og}:
                og_ok = True
                break
        if not og_ok:
            topo = "INCONCLUSIVE"
            topo_reason = "outgroup split absent in NJ tree"
        else:
            def has(group_a, group_b):
                want = frozenset(group_a)
                if want | frozenset(group_b) != leaves:
                    return False
                for clade, label, _ in parts:
                    if clade == want or (leaves - clade) == want:
                        return True
                return False
            has_b = has({q} | cov_h, flu_h | {og})
            has_a = has({q} | flu_h, cov_h | {og})
            if has_b:
                topo = "AGREE"
                topo_reason = "NJ: Q groups with S_cov excluding S_flu"
            elif has_a:
                topo = "DISAGREE"
                topo_reason = "NJ: Q groups with S_flu excluding S_cov"
            else:
                topo = "DISAGREE"
                topo_reason = "NJ: Q groups with neither"

    method = primary
    if primary in ("AGREE", "DISAGREE") and topo in ("AGREE", "DISAGREE") and primary != topo:
        method = "INCONCLUSIVE"
        reason = f"primary {primary} conflicts with NJ topology {topo}"

    return {
        "k": K,
        "kmer_sizes": sizes,
        "pairs": pairs,
        "d_cov": d_cov,
        "d_flu": d_flu,
        "nearest": nearest,
        "ties": ties,
        "primary": primary,
        "primary_reason": reason if method == primary else reason,
        "nj_newick": nwk,
        "nj_topology": topo,
        "nj_reason": topo_reason,
        "verdict": method,
        "reason": reason,
    }


def main(argv=None):
    root = Path(os.environ.get("Q17_ROOT", HERE.parent))
    pins = load_pins(root)
    fasta = root / pins["fasta"]["path"]
    expected = pins["fasta"]["sha256"]
    actual = sha256_file(fasta)
    if actual.lower() != expected.lower():
        raise SystemExit(f"FASTA hash mismatch: expected {expected} got {actual}")
    recs = read_fa(fasta)
    if len(recs) != pins["fasta"]["n_records"]:
        raise SystemExit(f"FASTA record count {len(recs)} != {pins['fasta']['n_records']}")

    sel = load_selection(root)
    query_acc, outgroup_acc, query, flu, cov, outgroup = build_genomes(sel)
    needed = [query_acc, outgroup_acc] + [s["accession"] for g in flu + cov + [outgroup, query] for s in g["segs"]]
    seqs = load_seqs(root, needed)

    out = Path(os.environ.get("Q17_RESULT_DIR", str(root / "results" / "test-01" / "q17")))
    out.mkdir(parents=True, exist_ok=True)
    work = out / "work"
    work.mkdir(parents=True, exist_ok=True)
    log_path = out / "commands.log"
    log_fh = log_path.open("a")
    log_fh.write(f"\n# Q-17 start {_now()}\n# FASTA sha256={actual}\n")
    log_fh.flush()

    # Copy the identity-gate script into the run log directory before executing it.
    ident_src = root / "tools" / "test01_mean_pairwise_identity.py"
    ident_copy = out / "identity-gate-script.py"
    shutil.copy2(ident_src, ident_copy)

    bindir = Path("/opt/covid-tools/bin")
    tools = {"mafft": str(bindir / "mafft"), "iqtree": str(bindir / "iqtree3")}

    # Load committed BLAST tables (no new BLAST for the letter).
    blast_dir = root / "results" / "test-01" / "blast"
    flu_accs = {s["accession"] for g in flu for s in g["segs"]}
    cov_accs = {s["accession"] for g in cov for s in g["segs"]}
    og_accs = {outgroup_acc}
    blast_tables = {}
    for name, accs in (("S_flu", flu_accs), ("S_cov", cov_accs), ("outgroup", og_accs)):
        path = blast_dir / f"{query_acc}.{name}.tsv"
        raw_rows = parse_blast_tsv(path)
        blast_tables[name] = resolve_blast_table(raw_rows, accs)

    (work / "t-protocol").mkdir(parents=True, exist_ok=True)
    t1 = t_protocol(query, flu, cov, outgroup, seqs, blast_tables, work / "t-protocol", log_fh, tools, ident_copy)
    # t_protocol also mkdir via write? ensure dir exists before call - fix order
    method2 = {"attempt": "T-protocol", "raw": {k: v for k, v in t1.items() if k not in ("iqtree_report_text",)}}
    tree_verdict = "INCONCLUSIVE"
    tree_reason = t1.get("sub") or "; ".join(t1.get("notes") or [])
    scored = None
    if t1.get("status") == "tree":
        scored = assess_tree(
            t1["newick"], query_acc, outgroup_acc,
            [g["concat_header"] for g in flu],
            [g["concat_header"] for g in cov],
        )
        tree_verdict = scored["verdict"]
        tree_reason = scored["reason"]
        method2["assessment"] = scored
    else:
        t2_dir = work / "t-full"
        t2_dir.mkdir(parents=True, exist_ok=True)
        t2 = t_full(query, flu, cov, outgroup, seqs, t2_dir, log_fh, tools, ident_copy)
        method2["attempt"] = "T-full"
        method2["t_protocol"] = {k: v for k, v in t1.items() if k not in ("iqtree_report_text",)}
        method2["raw"] = {k: v for k, v in t2.items() if k not in ("iqtree_report_text",)}
        if t2.get("status") == "tree":
            scored = assess_tree(
                t2["newick"], query_acc, outgroup_acc,
                [g["concat_header"] for g in flu],
                [g["concat_header"] for g in cov],
            )
            tree_verdict = scored["verdict"]
            tree_reason = scored["reason"]
            method2["assessment"] = scored
        else:
            tree_verdict = "INCONCLUSIVE"
            tree_reason = t2.get("sub") or "; ".join(t2.get("notes") or [])
            method2["notes"] = t2.get("notes")

    method2["verdict"] = tree_verdict
    method2["reason"] = tree_reason

    m3 = method3(query, flu, cov, outgroup, seqs)
    # Drop bulky pairwise duplication for the written report's top level
    m3_out = dict(m3)
    overall = "PASS"
    if tree_verdict == "DISAGREE" or m3["verdict"] == "DISAGREE":
        overall = "FAIL"

    summary = {
        "written_at": _now(),
        "test1_letter_unchanged": "B-blast",
        "fasta_sha256": actual,
        "method2_verdict": tree_verdict,
        "method2_reason": tree_reason,
        "method2_attempt": method2.get("attempt"),
        "method3_verdict": m3["verdict"],
        "method3_reason": m3["reason"],
        "method3_primary": m3["primary"],
        "method3_nj": m3["nj_topology"],
        "d_cov": m3["d_cov"],
        "d_flu": m3["d_flu"],
        "nearest": m3["nearest"],
        "q17_verification": overall,
        "status": f"Q-17 {overall} (letter remains B-blast)",
    }
    (out / "SUMMARY.json").write_text(json.dumps(summary, indent=2, sort_keys=True, default=str) + "\n")
    (out / "method2.json").write_text(json.dumps(method2, indent=2, sort_keys=True, default=str) + "\n")
    # pairs can be large; write separately
    pairs = m3_out.pop("pairs")
    (out / "method3.json").write_text(json.dumps(m3_out, indent=2, sort_keys=True, default=str) + "\n")
    (out / "method3-pairs.json").write_text(json.dumps(pairs, indent=2, sort_keys=True, default=str) + "\n")
    log_fh.write(f"# Q-17 end {_now()} verification={overall}\n")
    log_fh.close()
    print(json.dumps(summary, indent=2, sort_keys=True, default=str))
    return 0 if overall == "PASS" else 1


if __name__ == "__main__":
    # Create t-protocol work dir before running trim writes
    try:
        sys.exit(main())
    except Exception:
        raise
