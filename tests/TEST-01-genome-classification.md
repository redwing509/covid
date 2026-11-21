# Test 1 — genome classification (pre-registered protocol)

**Status (21 Nov 2026, Pacific Time):** protocol and decision rule only. **Not run.** No accessions have been copied from an opened NCBI page into this file. No alignment or tree has been produced. The classification question is **open**. This file does not assume that the query sequences group with influenza references, and it does not assume that they do not.

**When it will run:** after the usage reset at Mon 23 Nov 2026, 9:49 PM Pacific Time. The tool install was authorized and completed on 21 Nov 2026 (t1227s6218; see [`TOOLS.md`](../TOOLS.md)). Do not start this test before the reset. A later note may still mark a tiny first step (for example, copying accessions from opened NCBI pages into a source list) as allowed sooner.

Follow [`METHOD.md`](../METHOD.md). Results will be reported as-is.

This protocol was tightened on 21 Nov 2026 after Claude reviews of the first draft, **before any research run and before the first public push**. The changes close holes in the decision rule. They are not a result. No research genomes have been opened.

### Amendment log (all entries pre-data)

| Date (Pacific Time) | Commit | What changed | Why | Data opened? |
|---|---|---|---|---|
| 21 Nov 2026 | 15ee1b5 | BLAST settings, one-sided outcomes, tree commands, set rules, A-nested label, citation exception, rerun policy | Claude must-fix M1–M7 | No |
| 21 Nov 2026 | 4f39c50 | Shorter-molecule coverage; segment concatenation; outgroup BLAST direction; identity-gate script; decision host; on-paper reachability | Claude must-fix remaining M2, N1, N2 | No |
| 21 Nov 2026 | 61b8bf2 | Organization is reported, not a letter-deciding bullet; IQ-TREE `-o` and UNROOTED clarification; critical-branch bipartitions; reachability wording | Claude must-fix N3, N4 | No |
| 21 Nov 2026 | this follow-up | Amendment-log hash corrected from a superseded amend (`af8023e`) to `61b8bf2` | Bookkeeping only | No |
| 21 Nov 2026 | 61b8bf2 (addendum) | Also in 61b8bf2, and not listed in the original row: subject intervals are merged within each segment then summed, and shorter-molecule coverage always uses max(covered query, covered subject) bases; `.gitignore` additions for BLAST/IQ-TREE sidecars | Completes the 61b8bf2 log | No |
| 21 Nov 2026 | this commit | PLAN.md C summary no longer treats organization conflict as a C trigger (TEST-01 governs if the summary and protocol differ); FASTA headers pinned to accession.version; reachability lists the step 6 outgroup gate; A-nested critical branch stated | Claude must-fix N5, plus nits 1–4 | No |

Any later protocol change, including after the first public push but before a run, must be added to this table, with whether any Test 1 inputs had been opened.

## Question

Public NCBI records include sequences labeled as the reference pathogen for COVID-19 (the label SARS-CoV-2 is used in those databases). Do those query sequences (1) group with influenza references, to the exclusion of other-coronavirus references, (2) group with sequences labeled as other coronaviruses, to the exclusion of influenza references, (3) group with neither, or (4) is the comparison inconclusive?

The phrase **“influenza variant”** is used in this project only if the stronger nesting test in outcome **A-nested** holds. Outcome **A** by itself supports only grouping with influenza references, not that the query falls inside influenza.

## Inputs (to be filled from opened pages at run time)

All accessions, titles, lengths, and dates below will be copied from opened NCBI (or other official) pages or from a dated, logged API response. Until that happens, this section is a list of *what will be sought* and *how records will be chosen*, not a list of identifiers. Do not type accessions from memory. Do not add extra taxa on run day to change the result.

Seek, and then pin, using these selection rules:

1. **Query set (Q).** On the opened official NCBI RefSeq (or equivalent official NCBI reference) page for the taxon labeled SARS-CoV-2, take the record the page marks as the reference sequence, if that mark is present. Also take any additional complete-genome reference records listed on that same page, up to a maximum of **five** query records, in the order they appear on the page. If the page cannot be opened, write `NOT FOUND` for Q and apply **C**.

2. **Influenza reference set (S_flu).** Open the official NCBI RefSeq influenza reference list (the RefSeq page or browse list for influenza A and influenza B references). If that RefSeq list cannot be opened, open the official NCBI Influenza Virus Resource “reference strains” or “reference sequences” page instead, and record which page was used. Do not pick a third page to change the subtype list. From that opened page, take complete genomes (every segment of that genome, when the record is segmented) as follows:
   - one complete genome per influenza A subtype that the opened official reference list marks as a reference, in the order listed, up to **twelve** influenza A genomes;
   - one influenza B complete-genome reference, if listed.
   If the official list has fewer entries, use those. Do not add subtypes that are not on the opened official reference list. If no influenza reference can be opened, write `NOT FOUND` for S_flu and apply **C**.

3. **Other-coronavirus reference set (S_cov).** From opened official NCBI RefSeq pages, take the official complete-genome reference record, when it can be opened, for each of these labels and no others: HCoV-229E, HCoV-NL63, HCoV-OC43, HCoV-HKU1, SARS-CoV (the pre-2019 SARS reference as the page labels it), and MERS-CoV. If a label has no open record, write `NOT FOUND` for that label and continue with the records that were opened. If none of these can be opened, write `NOT FOUND` for S_cov and apply **C**. Do not add other coronavirus labels on run day.

4. **Outgroup (required for the tree criteria in A, A-nested, and B).** From the opened official NCBI RefSeq viral catalog, take one complete-genome reference from a labeled family that is not Orthomyxoviridae and not Coronaviridae, chosen as follows: the official reference complete genome of the type species of family Paramyxoviridae, if a type species is marked and the record can be opened; otherwise the first listed Paramyxoviridae RefSeq complete genome on that catalog page. If that is `NOT FOUND`, apply the same rule to family Pneumoviridae. If both are `NOT FOUND`, still report BLAST and organization, and apply **C** for any tree decision. Do not pick a different outgroup family after seeing a tree. The outgroup family is chosen, before any tree is seen, only because it is labeled as neither Orthomyxoviridae nor Coronaviridae, so the root lies outside both test sets. That is a methodological rule, not a finding about relatedness. The tree used for A, A-nested, or B is rooted on this outgroup (or on the split that separates the outgroup from all other taxa). Do not infer monophyly from an unrooted tree.

The S_flu and S_cov labels are taken from the official pages as labels to be used in the comparison. They are not themselves re-validated as a taxonomy finding in Test 1; that limitation is stated here.

For each record store: accession, version, title as shown, download date and time (Pacific Time), URL, and a file hash.

## Tools and versions

Intended standard tools (peer-review practice in viral genomics), with the commands pinned below. Pin the exact package version strings in the run log before looking at the tree.

**What we have today (21 Nov 2026, Pacific Time, checked on the box and on mail):** NCBI BLAST+ 2.17.0, MAFFT 7.526, IQ-TREE 3.1.4, and Biopython 1.88 are installed under `/opt/covid-tools` on the box and on mail (James, t1227s6218). Smoke tests passed. Nextstrain / Augur was optional and was not installed. See [`TOOLS.md`](../TOOLS.md) and [`tools/VERSIONS.txt`](../tools/VERSIONS.txt). **This protocol has still not been run.**

A wrapper script, once written, will live under `tools/` in this repository, MIT-licensed, and will not be pushed until it passes the full review set.

### Pinned commands (do not substitute after seeing results)

BLAST database, built once per reference set (and a combined database is not required):

```bash
makeblastdb -in SET.fa -dbtype nucl -parse_seqids -out SET
```

BLAST search. The query file is always a Q record (or, when the query is segmented, one Q segment). Build three databases with the command above: S_flu, S_cov, and the outgroup. Run the search of each Q record (or segment) against each of those three databases:

```bash
blastn -task blastn -query QUERY.fa -db SET -evalue 1e-5 -max_target_seqs 1000 -max_hsps 20 \
  -outfmt "6 qseqid sacc sseqid pident length evalue bitscore qcovs qstart qend sstart send qlen slen" \
  -out QUERY.SET.tsv
```

Do not use megablast, tblastx, or blastp for the Test 1 decision. Those programs are not the pre-registered method. If a command fails, that is a run error, not a reason to switch programs.

MAFFT, only when a combined alignment is allowed by the steps below:

```bash
mafft --auto --maxiterate 1000 --thread 1 in.fa > aln.fa
```

Column filter, after MAFFT, without any extra package: drop every alignment column whose gap fraction is greater than 0.50. If fewer than **200** columns remain, or if the mean pairwise nucleotide identity in the remaining columns is below **30%**, the alignment is not informative; apply **C** and do not run IQ-TREE on it.

Mean pairwise identity is computed with **pairwise deletion**, using only the Python standard library, as follows. For each unordered pair of sequences, ignore columns in which either character is a gap or `N`, and set that pair’s identity to matches / (matches + mismatches). The reported mean is the unweighted mean of those pair values. Pairs with no remaining columns are skipped; if every pair is skipped, the gate fails. The exact script must be saved in the run log before it is executed:

```python
import itertools, pathlib, sys

def read_fa(path):
    seqs, name, buf = [], None, []
    for line in pathlib.Path(path).read_text().splitlines():
        if line.startswith(">"):
            if name is not None:
                seqs.append((name, "".join(buf).upper()))
            name, buf = line[1:].split()[0], []
        else:
            buf.append(line.strip())
    if name is not None:
        seqs.append((name, "".join(buf).upper()))
    return seqs

seqs = read_fa(sys.argv[1])
L = {len(s) for _, s in seqs}
if len(L) != 1:
    raise SystemExit("alignment sequences have different lengths")
pairs = []
for a, b in itertools.combinations([s for _, s in seqs], 2):
    m = n = 0
    for x, y in zip(a, b):
        if x in "-N" or y in "-N":
            continue
        n += 1
        if x == y:
            m += 1
    if n:
        pairs.append(m / n)
if not pairs:
    print("MEAN_PAIRWISE_IDENTITY=NA PAIRS=0")
    raise SystemExit(2)
print(f"MEAN_PAIRWISE_IDENTITY={sum(pairs)/len(pairs):.6f} PAIRS={len(pairs)}")
```

IQ-TREE, only on an alignment that passed the filter:

```bash
iqtree -s aln.filtered.fa -m MFP --ufboot 1000 --alrt 1000 --seed 12345 -T 1 -o OUTGROUP_ACCESSION -pre test01
```

Replace `OUTGROUP_ACCESSION` with the first outgroup accession copied from the opened record in step 1. Do not pick a different outgroup sequence after seeing a tree.

The support thresholds are fixed: **UFBoot ≥ 95** and **SH-aLRT ≥ 80** on the critical branch. Do not change the bootstrap method, the replicate counts, the seed, or these thresholds after seeing a tree. Thread count is **1**. Record the host name, the exact binary path (`iqtree` or `iqtree3` as resolved on that host), and the tool versions in the run log.

**Rooting.** “Rooted on the outgroup” means rooted on the bipartition that separates the outgroup from all other taxa. IQ-TREE may still print that the tree is `UNROOTED` when a time-reversible model is used; that note, by itself, does **not** trigger **C**. **C-unrooted** applies only when the outgroup is missing, fails the step 6 gate, or does not form a single split from all other taxa in the inferred tree (for example, outgroup sequences are mixed among the ingroup). The critical branch for **A** is the bipartition `{Q ∪ S_flu} | {S_cov ∪ outgroup}`. **A-nested** also requires support on the bipartition `{Q ∪ S_flu′} | {the remaining taxa}`, where S_flu′ is a proper, non-empty subset of S_flu. The critical branch for **B** is the bipartition `{Q ∪ S_cov} | {S_flu ∪ outgroup}`.

## Analysis steps

1. Open the NCBI pages (or documented API) and fill the input table using the selection rules above. Pass 1 is a SOURCES OPENED list only.
2. Download the FASTA records. Store them outside git if they are large (`data/raw/`), and record hashes and accessions in the notes. Small text outputs of this test (the run log, the `.iqtree` report, the treefile, and the BLAST tables) may be committed under `results/test-01/` (see `.gitignore`).
3. Record genome organization as the records themselves describe it, quoting the record text. Do not infer an organization the record does not state. Record these fields when present: molecule type, number of segments or records per genome, topology, and stated length. **Only “number of segments or records per genome” is used to compare organizations** (treat “a single complete unsegmented genome” as one segment/record). Molecule type, topology, and stated length are recorded and reported, but they do not decide a match, and they cannot by themselves produce “matches both” or “matches neither.” A set’s organization is the segment-count value shared by all of its opened members. If the members of a set disagree on that value, the set has no single organization; record that fact. Organization is **reported with the Test 1 letter**; it is not a required bullet of A, A-nested, A-blast, B, or B-blast, and a mismatch does not change the letter. If the letter is A, A-nested, or A-blast, and Q’s shared segment-count equals S_cov’s and not S_flu’s, mark **organization-disagrees** in the write-up. The symmetric mark applies for B and B-blast. If organization is missing, or is the same for both reference sets (non-discriminating), or agrees with the letter, or either reference set has no single organization, write that and do not add the disagreement mark.
4. Run the pinned `blastn -task blastn` command of each query record against S_flu, against S_cov, and against the outgroup. Save the full tabular output. Summarize only numbers that appear in that output.
5. **Qualifying hit (genome-level, symmetric coverage).** Group reference records by genome (all segments of one isolate or one versioned genome, as the opened records group them). For a query record and a reference genome, take every HSP in the BLAST table that passes `evalue ≤ 1e-5`. Merge overlapping query intervals (`qstart`–`qend`) to get **covered query bases**. Merge overlapping subject intervals (`sstart`–`send`, taken as 1-based inclusive and converted to a positive interval if the HSP is on the opposite strand) **within each reference segment**, then **sum** those per-segment covered lengths to get **covered subject bases** (do not merge coordinates across different segments). Let `Qlen` be the query length (`qlen`) and `Glen` be the sum of the lengths of that reference genome’s segments (from `slen` on each segment record, or from the opened sequence length if `slen` is missing). The **shorter-molecule coverage** is `max(covered_query_bases, covered_subject_bases) / min(Qlen, Glen)`. The query has a qualifying hit to that reference genome if shorter-molecule coverage is at least **50%**. This is intentional: a long query cannot be blocked from matching a shorter reference genome solely because 50% of the longer molecule cannot be covered by the shorter one. The bitscore of that genome is the **highest** bitscore among those HSPs (do not sum bitscores). The **best** genome in a set is the qualifying genome with the highest bitscore. If two qualifying genomes are tied on that bitscore, they are tied; do not break the tie by judgment. Percent identity is recorded but is not the score used to decide “more similar.”
   - If the query itself is deposited as a set of segments, compute shorter-molecule coverage and best bitscore **per query segment** against the reference set, then treat the query genome as having a qualifying hit in the set only if **every** query segment has a qualifying hit in that set. The genome-level bitscore is the sum of the per-segment best bitscores of those qualifying hits (here the sum is across the query's own segments, each compared once).
6. **Homology gate, limited and pre-stated.** A query is treated as having a basis to align to a reference set only if it has at least one qualifying hit in that set (step 5). The outgroup check uses the same pinned command, with Q as the query and the outgroup as the database (step 4). Do not reverse that direction, and do not require a search of the outgroup against S_flu or S_cov. The outgroup may be used to root the tree if **at least one Q record has a qualifying hit to the outgroup** under step 5. If that condition fails, write the BLAST result, do not use the outgroup to assess monophyly, and apply **C** for the tree decision. BLAST-only outcomes (A-blast, B-blast) may still be used.
7. **One-sided versus two-sided BLAST.**
   - If a query has a qualifying hit in **both** S_flu and S_cov, a combined alignment of Q plus both sets plus the outgroup may be built, using the concatenation representation in step 8.
   - If a query has a qualifying hit in **exactly one** of the two sets, do **not** force a combined MAFFT alignment of Q with both sets. Report the BLAST table and the organization quotes. Do not treat this as automatically **C**. Apply **A-blast** or **B-blast** if their other bullets hold, otherwise **C**.
   - If a query has a qualifying hit in **neither** set, apply **C**. Do not force a combined tree.
8. If step 7 allows a combined alignment, first write each segmented genome as **one sequence** so that segmented and unsegmented records can be placed in the same alignment: concatenate that genome’s segments in **increasing segment number** as stated on the opened records; if no segment number is stated, concatenate in the order the records appear on the opened genome page. Insert a spacer of **ten `N` characters** between segments. Do not reverse-complement a segment unless the opened record itself states that the deposited orientation is the opposite of the virus’s plus-strand, and then quote that statement. After concatenation, treat the genome as a single sequence for MAFFT. Before MAFFT, rewrite every FASTA header to exactly the record’s `accession.version` as copied from the opened page. For a concatenated segmented genome, use the first segment’s `accession.version` (the first in the concatenation order above). That same string is the `OUTGROUP_ACCESSION` passed to IQ-TREE `-o` when the sequence is the outgroup. Build the alignment of Q plus both reference sets plus the outgroup with the pinned MAFFT command, apply the column filter, and apply the 200-column / 30% identity gate using the pinned script. If the gate fails, state that in the run log, do not force a tree, and apply **C** (unless A-blast or B-blast already applies from a one-sided BLAST result; a failed combined tree does not cancel a one-sided BLAST outcome that already held). Molecule type is still recorded and reported in step 3; concatenation is only a representation rule for segmented records, not a claim that the organizations are the same.
9. If the filtered alignment passed the gate, run the pinned IQ-TREE command. Root the tree on the outgroup as stated above. Save the command line, the `.iqtree` report, the treefile, and the run log, and record whether the report labels the tree as rooted (informational only; see **Rooting**).
10. Apply the decision rule below. Do not change the rule after seeing the tree or the BLAST table.

## Pre-registered decision rule

Write the conclusion of Test 1 by applying **exactly one** of the following. Thresholds and commands are stated here, before any run.

Let **S_flu** be the influenza A/B reference set and **S_cov** be the other-coronavirus reference set. Let **Q** be the query set. Let **UFBoot** and **SH-aLRT** be the support values, as percentages, on the critical branch that separates the relevant groups. Both must meet their thresholds (**UFBoot ≥ 95** and **SH-aLRT ≥ 80**) for a tree criterion to pass.

**A. Supports “groups with influenza references, to the exclusion of the other-coronavirus references.”** All of the following hold:

- Each query has a qualifying hit in **both** S_flu and S_cov, so a combined tree was allowed.
- In the **rooted** tree, the query sequences form a monophyletic group with **S_flu** to the exclusion of **S_cov**, with UFBoot and SH-aLRT at or above their thresholds on the branch that separates `{Q + S_flu}` from **S_cov** (the outgroup lies outside that group).
- Each query’s best **S_flu** bitscore is strictly higher than its best **S_cov** bitscore.

**A-nested. Supports a stronger claim, “nested within influenza references” (the only outcome that may be described as consistent with an “influenza variant” wording).** All of A holds, and in addition, in the same rooted tree, there is a supported clade that contains Q and a proper, non-empty subset of S_flu and that excludes at least one other S_flu genome, with UFBoot and SH-aLRT at or above their thresholds on the branch that defines that clade. If A holds but this nesting test does not, report **A** only, and do not use the words “influenza variant” in the Test 1 conclusion.

**A-blast. Supports “groups with influenza references by the BLAST rule only (no combined tree).”** All of the following hold, and a combined tree was not built because the other set had no qualifying hit:

- Each query has a qualifying hit in **S_flu** and **no** qualifying hit in **S_cov**.
- Report the BLAST table. Do not call this A or A-nested. Do not use the words “influenza variant” for this outcome.

**B. Supports “groups with the other-coronavirus references, to the exclusion of the influenza references.”** All of the following hold:

- Each query has a qualifying hit in **both** S_flu and S_cov, so a combined tree was allowed.
- In the **rooted** tree, the query sequences form a monophyletic group with **S_cov** to the exclusion of **S_flu**, with UFBoot and SH-aLRT at or above their thresholds on the branch that separates `{Q + S_cov}` from **S_flu** (the outgroup lies outside that group).
- Each query’s best **S_cov** bitscore is strictly higher than its best **S_flu** bitscore.

**B-blast. Supports “groups with the other-coronavirus references by the BLAST rule only (no combined tree).”** Symmetric to A-blast: each query has a qualifying hit in **S_cov** and **no** qualifying hit in **S_flu**. Do not call this B. Organization is reported as in step 3 and does not change this letter.

**C. Inconclusive.** **C** applies if none of A, A-nested, A-blast, B, or B-blast holds. That includes, without limitation, any of the following. Where useful, a write-up may add a sub-code (C-neither, C-support, C-BLAST, C-alignment, C-missing, C-unrooted) without changing the outcome letter:

- UFBoot or SH-aLRT is below its threshold.
- Tree topology and BLAST bitscores disagree.
- (Organization is reported with the letter as in step 3; a disagreement mark does not, by itself, change the letter to **C**.)
- A query has no qualifying BLAST hit in either reference set, or the best qualifying bitscores are tied, or a combined alignment is not valid because of the alignment-quality gate, and A-blast / B-blast also do not hold.
- The query set has more than one record, and those records would not all receive the same letter (for example, some are one-sided and others have hits in both sets). Report each record’s BLAST result and apply **C** (sub-code C-mixed).
- The outgroup is missing, fails the step 6 gate, or does not form a single split from all other taxa, so the monophyly tests in A, A-nested, and B cannot be applied, and A-blast / B-blast also do not hold. An IQ-TREE `UNROOTED` note under a reversible model does not, by itself, count as this case.
- A supported rooted topology places Q outside both `{Q + S_flu}` and `{Q + S_cov}` (groups with neither).
- Records cannot be opened or downloaded; write `NOT FOUND` for the missing set.

If **C** applies, both “groups with influenza references” and “groups with the other-coronavirus references” remain open. Do not pick a side by judgment.

## Rerun policy

A **bug** is only a difference from a pre-registered command, a documented non-zero exit, a crash, or a truncated output file. Disliking a support value or a letter is not a bug.

The **decision host** for the published Test 1 letter is the box. Mail may be used as a reproduction check with the same commands, seed, inputs, and `-T 1`. If both hosts are run and they disagree on the decision letter, report both outputs and apply **C**.

If a bug is found, fix the command so that it matches this protocol, re-run on the decision host with the same `--seed 12345`, the same inputs, and `-T 1`, and keep **both** the failed output and the new output. Explain the difference in the run log. The later run is the decision run only if the change is a documented bug of that kind. Do not re-run in order to cross a support threshold.

Computed numbers in the write-up must include the pinned command, tool version, seed, thread count, host, input accessions, download dates, and file hashes, as required by [`METHOD.md`](../METHOD.md).

## On-paper reachability (not a run)

This check is made on the written rule, without opening research genomes. It records that each decisive letter can be reached under at least one plausible combination of record properties:

- **A** and **B** can be reached when Q has a qualifying hit (symmetric shorter-molecule coverage) in both S_flu and S_cov, segmented genomes are concatenated as in step 8, the alignment passes the quality gate, the outgroup passes the step 6 homology gate and forms a single split from all other taxa, and the stated bipartition meets the UFBoot and SH-aLRT tests. Organization is reported with the letter and does not have to match for the letter to be reached.
- **A-nested** can be reached when A holds, at least two S_flu genomes were included, and Q falls inside a supported clade with a proper, non-empty subset of S_flu. If only one S_flu genome is opened, A-nested cannot be reached; report A or C as the other rules require, and do not use “influenza variant” wording.
- **A-blast** can be reached when every Q record has a qualifying hit in S_flu and none in S_cov, including the case of a long unsegmented query whose shorter-molecule coverage against an influenza genome is at least 50%. Organization need not match S_flu for this letter to be reached.
- **B-blast** can be reached when every Q record has a qualifying hit in S_cov and none in S_flu, under the same coverage rule.

If a later amendment were to make any of those letters unreachable for all plausible record properties, that amendment would be a protocol defect, not a result.

## Reporting

The write-up will include the SOURCES OPENED list, the pinned versions, the commands, the decision letter (A, A-nested, A-blast, B, B-blast, or C, with a C sub-code when one applies), and the quoted or computed numbers that triggered it. Null, failed, or inconclusive outcomes are reported. The write-up will not add a preferred interpretation beyond the rule.

This protocol is not a result.
