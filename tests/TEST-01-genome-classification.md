# Test 1 — genome classification (pre-registered protocol)

**Status (21 Nov 2026, Pacific Time):** protocol and decision rule only. **Not run.** No accessions have been copied from an opened NCBI page into this file. No alignment or tree has been produced. The classification question is **open**. This file does not assume that the query sequences are an influenza variant, and it does not assume that they are not.

**When it will run:** after the usage reset at Mon 23 Nov 2026, 9:49 PM Pacific Time, and after James OKs install of any missing tools listed below, unless a later note marks a tiny first step (for example, copying accessions from opened NCBI pages into a source list) as allowed sooner.

Follow [`METHOD.md`](../METHOD.md). Results will be reported as-is.

## Question

Public NCBI records include sequences labeled as the reference pathogen for COVID-19 (the label SARS-CoV-2 is used in those databases). Do those query sequences group with influenza references (an influenza variant), group with sequences labeled as other coronaviruses, group with neither, or is the comparison inconclusive?

## Inputs (to be filled from opened pages at run time)

All accessions, titles, lengths, and dates below will be copied from opened NCBI (or other official) pages or from a dated, logged API response. Until that happens, this section is a list of *what will be sought*, not a list of identifiers.

Seek, and then pin:

1. **Query set:** NCBI records labeled as SARS-CoV-2 reference or complete genome sequences, including the record the database itself marks as the reference when that label is present on the opened page.
2. **Influenza reference set:** NCBI records labeled as influenza A and influenza B reference or complete genomes (all segments, when the record is segmented).
3. **Other-coronavirus reference set:** NCBI records labeled as coronavirus references other than the query set (for example, records labeled as other SARS-related or seasonal coronavirus complete genomes — only as those labels appear on the opened pages).
4. **Optional outgroup:** one or more records from a different labeled virus family, only if an opened protocol or standard reference set uses one, with the reason quoted.

For each record store: accession, version, title as shown, download date and time (Pacific Time), URL, and a file hash. Do not type accessions from memory.

## Tools and versions

Intended standard tools (peer-review practice in viral genomics):

- NCBI BLAST (or the equivalent command-line BLAST+ suite) for pairwise similarity of the query genomes against the influenza and other-coronavirus reference sets.
- MAFFT for multiple sequence alignment, or an equivalent widely used aligner if MAFFT cannot be installed and the substitute is named and pinned.
- IQ-TREE for a maximum-likelihood phylogenetic tree, with its model finder (or a pre-stated substitution model) and ultrafast bootstrap or the standard bootstrap the chosen IQ-TREE version documents.

Pin the exact package names and version strings in the run log before looking at the tree. A wrapper script, once written, will live under `tools/` in this repository, MIT-licensed, and will not be pushed until it passes the full review set.

**What we have today (21 Nov 2026, Pacific Time, checked on the box):** BLAST, MAFFT, IQ-TREE, Nextstrain/Augur, Biopython, and R were **not** found on the box. See [`TOOLS.md`](../TOOLS.md). Installing them needs James's OK.

## Analysis steps

1. Open the NCBI pages (or documented API) and fill the input table. Pass 1 is a SOURCES OPENED list only.
2. Download the FASTA records. Store them outside git if they are large (`data/raw/`), and record hashes and accessions in the notes.
3. Record genome organization as the records themselves describe it (for example, whether a record is a single complete genome or a set of segments, and the stated molecule type), quoting the record text. Do not infer an organization the record does not state.
4. Run BLAST (or BLAST+) of each query sequence against the influenza reference set and against the other-coronavirus reference set. Save the full tabular output. Summarize only numbers that appear in that output.
5. Build a multiple sequence alignment with MAFFT of the query set plus both reference sets (and the outgroup if used). If whole-genome alignment of mixed organizations is not valid (for example, segmented versus unsegmented records), state that in the run log and follow the decision rule’s conflict clause rather than forcing a single alignment.
6. Build an IQ-TREE maximum-likelihood tree from that alignment, with model selection and bootstrap or ultrafast bootstrap as documented for the pinned version. Save the command line, the `.iqtree` report, and the tree file.
7. Apply the decision rule below. Do not change the rule after seeing the tree. If a bug in a command is found, fix it, re-run, and say what changed.

## Pre-registered decision rule

Write the conclusion of Test 1 by applying **exactly one** of the following. Thresholds are stated here, before any run.

Let **S_flu** be the influenza A/B reference set and **S_cov** be the other-coronavirus reference set. Let **Q** be the query set. Let **B** be the bootstrap (or ultrafast bootstrap) support, as a percentage, on the critical branch that separates the relevant groups. The support threshold is **95** unless the pinned IQ-TREE manual for that version defines a different conventional cutoff for the chosen bootstrap method; if it does, quote that manual and use that cutoff, and record the substitution *before* inspecting the tree.

**A. Supports “influenza variant”.** All of the following hold:

- In the tree, the query sequences form a monophyletic group with **S_flu** to the exclusion of **S_cov**, with support **B** at or above the threshold on the branch that separates `{Q + S_flu}` from **S_cov**.
- BLAST (or the alignment identity the script is pre-set to report) shows each query sequence more similar to the best **S_flu** hit than to the best **S_cov** hit, using the same score (bitscore or percent identity) for both comparisons, named in the run log before the run.
- The genome organization quoted from the query records matches the organization quoted from the **S_flu** records, and does not match the organization quoted from the **S_cov** records, when those records state an organization.

**B. Supports “not an influenza variant; groups with the other-coronavirus references”.** All of the following hold:

- In the tree, the query sequences form a monophyletic group with **S_cov** to the exclusion of **S_flu**, with support **B** at or above the threshold on the branch that separates `{Q + S_cov}` from **S_flu**.
- BLAST (or the pre-set identity score) shows each query sequence more similar to the best **S_cov** hit than to the best **S_flu** hit.
- The genome organization quoted from the query records matches the organization quoted from the **S_cov** records, and does not match the organization quoted from the **S_flu** records, when those records state an organization.

**C. Inconclusive.** Any of the following holds:

- Support **B** is below the threshold.
- Tree topology and BLAST / identity scores disagree.
- Genome organization, as quoted from the records, conflicts with the tree result (for example, the tree groups Q with one set, but the records describe an organization that matches only the other set).
- Alignment of Q with both sets is not valid because of organization or length conflicts that the method cannot honestly bridge. In that case, report the BLAST results and the organization quotes, and do not force a combined tree.
- Records cannot be opened or downloaded; write `NOT FOUND` for the missing set.

If **C** applies, both “influenza variant” and “not an influenza variant” remain open. Do not pick a side by judgment.

## Reporting

The write-up will include the SOURCES OPENED list, the pinned versions, the commands, the decision letter (A, B, or C), and the quoted or computed numbers that triggered it. Null, failed, or inconclusive outcomes are reported. The write-up will not add a preferred interpretation beyond the rule.

This protocol is not a result.
