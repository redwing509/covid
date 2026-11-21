# Test 1 — genome classification (pre-registered protocol)

**Status (21 Nov 2026, Pacific Time):** protocol and decision rule only. **Not run.** No accessions have been copied from an opened NCBI page into this file. No alignment or tree has been produced. The classification question is **open**. This file does not assume that the query sequences are an influenza variant, and it does not assume that they are not.

**When it will run:** after the usage reset at Mon 23 Nov 2026, 9:49 PM Pacific Time. The tool install was authorized and completed on 21 Nov 2026 (t1227s6218; see [`TOOLS.md`](../TOOLS.md)). Do not start this test before the reset. A later note may still mark a tiny first step (for example, copying accessions from opened NCBI pages into a source list) as allowed sooner.

Follow [`METHOD.md`](../METHOD.md). Results will be reported as-is.

## Question

Public NCBI records include sequences labeled as the reference pathogen for COVID-19 (the label SARS-CoV-2 is used in those databases). Do those query sequences group with influenza references (an influenza variant), group with sequences labeled as other coronaviruses, group with neither, or is the comparison inconclusive?

## Inputs (to be filled from opened pages at run time)

All accessions, titles, lengths, and dates below will be copied from opened NCBI (or other official) pages or from a dated, logged API response. Until that happens, this section is a list of *what will be sought*, not a list of identifiers.

Seek, and then pin:

1. **Query set:** NCBI records labeled as SARS-CoV-2 reference or complete genome sequences, including the record the database itself marks as the reference when that label is present on the opened page.
2. **Influenza reference set:** NCBI records labeled as influenza A and influenza B reference or complete genomes (all segments, when the record is segmented).
3. **Other-coronavirus reference set:** NCBI records labeled as coronavirus references other than the query set (for example, records labeled as other SARS-related or seasonal coronavirus complete genomes — only as those labels appear on the opened pages).
4. **Outgroup (required for the tree criteria in A and B):** one or more records from a different labeled virus family than influenza and than the other-coronavirus reference set, copied from an opened official page or from a standard reference set whose use is quoted. The tree used for A or B is rooted on this outgroup (or on the split that separates the outgroup from all other taxa). If the outgroup cannot be opened or downloaded, write `NOT FOUND` for it, still report BLAST and organization, and apply **C** for the tree decision. Do not infer monophyly from an unrooted tree.

For each record store: accession, version, title as shown, download date and time (Pacific Time), URL, and a file hash. Do not type accessions from memory.

## Tools and versions

Intended standard tools (peer-review practice in viral genomics):

- NCBI BLAST (or the equivalent command-line BLAST+ suite) for pairwise similarity of the query genomes against the influenza and other-coronavirus reference sets.
- MAFFT for multiple sequence alignment, or an equivalent widely used aligner if MAFFT cannot be installed and the substitute is named and pinned.
- IQ-TREE for a maximum-likelihood phylogenetic tree, with its model finder (or a pre-stated substitution model) and ultrafast bootstrap or the standard bootstrap the chosen IQ-TREE version documents.

Pin the exact package names and version strings in the run log before looking at the tree. A wrapper script, once written, will live under `tools/` in this repository, MIT-licensed, and will not be pushed until it passes the full review set.

**What we have today (21 Nov 2026, Pacific Time, checked on the box and on mail):** NCBI BLAST+ 2.17.0, MAFFT 7.526, IQ-TREE 3.1.4, and Biopython 1.88 are installed under `/opt/covid-tools` on the box and on mail (James, t1227s6218). Smoke tests passed. Nextstrain / Augur was optional and was not installed. See [`TOOLS.md`](../TOOLS.md) and [`tools/VERSIONS.txt`](../tools/VERSIONS.txt). **This protocol has still not been run.**

## Analysis steps

1. Open the NCBI pages (or documented API) and fill the input table. Pass 1 is a SOURCES OPENED list only.
2. Download the FASTA records. Store them outside git if they are large (`data/raw/`), and record hashes and accessions in the notes.
3. Record genome organization as the records themselves describe it (for example, whether a record is a single complete genome or a set of segments, and the stated molecule type), quoting the record text. Do not infer an organization the record does not state.
4. Run BLAST+ of each query sequence against the influenza reference set and against the other-coronavirus reference set. Save the full tabular output, including at least bitscore, percent identity, alignment length, e-value, and query coverage (`qcovs` or an equivalent column whose name is recorded before the run). Summarize only numbers that appear in that output.
5. A BLAST hit is a **qualifying hit** only if its query coverage is at least **50%**. The **best** hit in a set is the qualifying hit with the highest bitscore. If two qualifying hits are tied on bitscore, they are tied; do not break the tie by judgment. Percent identity is recorded but is not the score used to decide “more similar” in A or B, because identity is measured only on the aligned region.
6. Before building a combined alignment, check homology in this limited, pre-stated sense: a query is treated as having a basis to align to a reference set only if it has at least one qualifying BLAST hit in that set. If a query has no qualifying hit in one or both sets, do not force a combined MAFFT alignment of Q with both sets. Report the BLAST table and the organization quotes, and apply **C**.
7. If the homology check in step 6 passes for both sets, build a multiple sequence alignment with MAFFT of the query set plus both reference sets plus the outgroup. If whole-genome alignment of mixed organizations is not valid (for example, segmented versus unsegmented records), state that in the run log, do not force a single alignment, and apply **C**.
8. Build an IQ-TREE maximum-likelihood tree from that alignment, with model selection and bootstrap or ultrafast bootstrap as documented for the pinned version. Root the tree on the outgroup as stated above. Save the command line, the `.iqtree` report, and the tree file, and record whether the report labels the tree as rooted.
9. Apply the decision rule below. Do not change the rule after seeing the tree. If a bug in a command is found, fix it, re-run, and say what changed.

## Pre-registered decision rule

Write the conclusion of Test 1 by applying **exactly one** of the following. Thresholds are stated here, before any run.

Let **S_flu** be the influenza A/B reference set and **S_cov** be the other-coronavirus reference set. Let **Q** be the query set. Let **B** be the bootstrap (or ultrafast bootstrap) support, as a percentage, on the critical branch that separates the relevant groups. The support threshold is **95** unless the pinned IQ-TREE manual for that version defines a different conventional cutoff for the chosen bootstrap method; if it does, quote that manual and use that cutoff, and record the substitution *before* inspecting the tree.

**A. Supports “influenza variant”.** All of the following hold:

- In the **rooted** tree, the query sequences form a monophyletic group with **S_flu** to the exclusion of **S_cov**, with support **B** at or above the threshold on the branch that separates `{Q + S_flu}` from **S_cov** (the outgroup lies outside that group).
- BLAST+ shows each query sequence has a qualifying hit in **S_flu**, and that its best **S_flu** bitscore is strictly higher than its best **S_cov** bitscore (or than the absence of a qualifying **S_cov** hit).
- The genome organization quoted from the query records matches the organization quoted from the **S_flu** records, and does not match the organization quoted from the **S_cov** records, when those records state an organization.

**B. Supports “not an influenza variant; groups with the other-coronavirus references”.** All of the following hold:

- In the **rooted** tree, the query sequences form a monophyletic group with **S_cov** to the exclusion of **S_flu**, with support **B** at or above the threshold on the branch that separates `{Q + S_cov}` from **S_flu** (the outgroup lies outside that group).
- BLAST+ shows each query sequence has a qualifying hit in **S_cov**, and that its best **S_cov** bitscore is strictly higher than its best **S_flu** bitscore (or than the absence of a qualifying **S_flu** hit).
- The genome organization quoted from the query records matches the organization quoted from the **S_cov** records, and does not match the organization quoted from the **S_flu** records, when those records state an organization.

**C. Inconclusive.** **C** applies if A does not hold and B does not hold. That includes, without limitation, any of the following:

- Support **B** is below the threshold.
- Tree topology and BLAST bitscores disagree.
- Genome organization, as quoted from the records, conflicts with the tree result (for example, the tree groups Q with one set, but the records describe an organization that matches only the other set), or the quoted organization matches both sets, or matches neither set when the records state an organization.
- A query has no qualifying BLAST hit in one or both reference sets, or the best qualifying bitscores are tied, or a combined alignment is not valid because of organization, length, or lack of a qualifying-hit basis for homology. In those cases, report the BLAST results and the organization quotes, and do not force a combined tree.
- The outgroup is missing, or the tree is unrooted, so the monophyly tests in A and B cannot be applied.
- Records cannot be opened or downloaded; write `NOT FOUND` for the missing set.

If **C** applies, both “influenza variant” and “not an influenza variant” remain open. Do not pick a side by judgment.

## Reporting

The write-up will include the SOURCES OPENED list, the pinned versions, the commands, the decision letter (A, B, or C), and the quoted or computed numbers that triggered it. Null, failed, or inconclusive outcomes are reported. The write-up will not add a preferred interpretation beyond the rule.

This protocol is not a result.
