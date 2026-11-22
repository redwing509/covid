# Test 1 result — genome classification

**This is not medical advice.** This write-up is the output of the pre-registered protocol in [`tests/TEST-01-genome-classification.md`](../../tests/TEST-01-genome-classification.md), applied to official NCBI records opened for this run. It is our analysis, not a published paper, and it is not a clinical conclusion. Test 1 is a sequence-classification comparison of those public records only. It does not, by itself, establish which virus is associated with patients’ illness, or whether no virus is.

**Decision letter: B-blast.** Under the pre-registered rule, this supports “groups with the other-coronavirus references by the BLAST rule only (no combined tree).” It is not outcome B, and it is not A, A-nested, or A-blast. The words “influenza variant” are not used. A combined tree was not built.

- Decision host: grok-bot-vm-342803711 (the box), America/Los_Angeles (Pacific Time)
- Run date: 21 Nov 2026, evening (sources opened from 11:16 PM; FASTA downloaded 11:24:08 PM; BLAST and the decision step 11:26–11:27 PM, after a parser fix described below)
- Priority: `nice 19`. BLAST thread count is the tool default for the pinned command (the pinned IQ-TREE command was not run).
- Pass 1 list: [`SOURCES-OPENED.md`](SOURCES-OPENED.md)
- FASTA hashes: [`FASTA-HASHES.md`](FASTA-HASHES.md)
- Pinned BLAST tables: [`blast/`](blast/)
- Machine-readable summary: [`BLAST-SUMMARY.json`](BLAST-SUMMARY.json)

## Pinned tools (copied from the binaries on the decision host before the tree would have been examined; no tree was run)

- NCBI BLAST+ `blastn` and `makeblastdb`: 2.17.0+ (Package: blast 2.17.0, build Jul 1 2025 08:59:18), `/opt/covid-tools/bin/blastn`, `/opt/covid-tools/bin/makeblastdb`
- MAFFT 7.526 and IQ-TREE 3.1.4 (`/opt/covid-tools/bin/iqtree3`) were installed and pinned, and were **not run**, because the pre-registered one-sided BLAST rule applied.
- Python 3.13.5 at `/opt/covid-tools/venv/bin/python3`, used only for the coverage arithmetic and the (unused in this letter) identity-gate script already saved at `results/test-01/run-logs/identity-gate-script.py`.

## Inputs used

Accessions, titles, lengths, and hashes are copied from the opened official NCBI responses and from the dated FASTA download. See [`SOURCES-OPENED.md`](SOURCES-OPENED.md) and [`FASTA-HASHES.md`](FASTA-HASHES.md). In brief:

- **Q (one record):** NC_045512.2, title “Severe acute respiratory syndrome coronavirus 2 isolate Wuhan-Hu-1, complete genome”, 29903 bp, official GenBank comment “REVIEWED REFSEQ: This record has been curated by NCBI staff. The reference sequence is identical to MN908947.”
- **S_flu:** six influenza A complete genomes, one per subtype in the official RefSeq list order (H1N1 A/California/07/2009, H7N9 A/Shanghai/02/2013, H2N2 A/Korea/426/1968, H3N2 A/New York/392/2004, H5N1 A/goose/Guangdong/1/1996, H9N2 A/Hong Kong/1073/99), plus one influenza B complete genome (B/Lee/1940), each with all eight official segments. A later H1N1 genome (A/Puerto Rico/8/1934) was listed and not taken.
- **S_cov:** NC_002645.1 (HCoV-229E), NC_005831.2 (HCoV-NL63), NC_006213.1 (HCoV-OC43), NC_006577.2 (HCoV-HKU1), NC_004718.3 (SARS-CoV, official organism name “SARS coronavirus Tor2”, report release_date 2003-04-14), NC_019843.3 (MERS-CoV).
- **Outgroup:** NC_140766.1, title “Bat paramyxovirus, complete genome”, 18095 bp, first listed Paramyxoviridae RefSeq complete genome on the official catalog whose own record title states “complete genome” (type species was `NOT FOUND` on the official family taxonomy record; the catalog’s first row, NC_140767.1, is titled “partial genome” and was not used).

### Pass-1 interpretations

These are the Pass-1 readings used to apply the written selection rules. They are also recorded in [`SOURCES-OPENED.md`](SOURCES-OPENED.md).

- The official Influenza Virus Resource HTML page redirected to an NCBI Virus JavaScript shell and did not yield a usable accession list. The official NCBI Datasets v2 virus `dataset_report` with `filter.refseq_only=true` was used as the official RefSeq influenza reference list, and “listed order” is that report’s return order. The protocol’s fallback order is RefSeq list, then the Influenza Virus Resource; the Datasets RefSeq-only report is a documented official API for that RefSeq list.
- For the Paramyxoviridae outgroup, the catalog’s first row was marked COMPLETE on the report but titled “partial genome” and was not used. The first listed record whose own title states “complete genome” (NC_140766.1) was taken, after type species was `NOT FOUND`.

The selection actually used is also committed at [`selection.json`](selection.json) (accessions, labels, and lengths only; no sequence residues).

## Organization (reported with the letter; does not change it)

Copied from the opened records, using only the pre-registered segment-count comparison:

- Q: one complete unsegmented genome (segment-count **1**).
- S_flu: eight official segments in every taken genome (shared segment-count **8**).
- S_cov: one complete unsegmented genome in every taken record (shared segment-count **1**).
- Outgroup: one complete unsegmented genome (segment-count **1**).

Q’s shared segment-count equals S_cov’s and not S_flu’s, which agrees with letter B-blast. The organization-disagrees mark is **not** applied.

Molecule type, topology, and stated length are recorded in the Pass 1 tables and were not used to decide the letter.

## Pinned BLAST commands

Databases were built once per reference set:

```bash
makeblastdb -in SET.fa -dbtype nucl -parse_seqids -out SET
```

for SET in S_flu, S_cov, and outgroup. Each Q record (here, the single record NC_045512.2) was then searched against each database:

```bash
blastn -task blastn -query QUERY.fa -db SET -evalue 1e-5 -max_target_seqs 1000 -max_hsps 20 \
  -outfmt "6 qseqid sacc sseqid pident length evalue bitscore qcovs qstart qend sstart send qlen slen" \
  -out QUERY.SET.tsv
```

The command log, including binary paths, working directories, and exit codes, is `results/test-01/run-logs/commands.log`. The tables are:

- [`blast/NC_045512.2.S_flu.tsv`](blast/NC_045512.2.S_flu.tsv) — 0 rows
- [`blast/NC_045512.2.S_cov.tsv`](blast/NC_045512.2.S_cov.tsv) — 33 rows
- [`blast/NC_045512.2.outgroup.tsv`](blast/NC_045512.2.outgroup.tsv) — 0 rows

## Qualifying-hit numbers (step 5)

A qualifying hit requires shorter-molecule coverage of at least 50%, with the numerator equal to the covered bases on the shorter molecule (covered subject bases when the reference genome is shorter; covered query bases when the query is shorter). Bitscore used to pick the best genome in a set is the highest bitscore among HSPs with `evalue ≤ 1e-5`, not a sum. Percent identity is recorded and is not the score used to decide “more similar.”

### S_flu

The S_flu table is empty: no HSP with `evalue ≤ 1e-5` was reported against any selected influenza A or influenza B segment. Every S_flu genome therefore has no qualifying hit. Qlen is not printed in that table because no row was returned.

### S_cov

| official label | subject accession.version | n HSPs (evalue ≤ 1e-5) | Qlen | Glen | L_short | covered query bases | covered subject bases | covered bases on shorter / L_short | shorter-molecule coverage | max bitscore | pident of that max-bitscore HSP | qualifying (≥ 50%) |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| HCoV-229E | NC_002645.1 | 6 | 29903 | 27317 | 27317 | 5172 | 5148 | 5148/27317 | 18.8454% | 461.0 | 66.667 | no |
| HCoV-NL63 | NC_005831.2 | 6 | 29903 | 27553 | 27553 | 6219 | 6217 | 6217/27553 | 22.5638% | 685.0 | 64.769 | no |
| HCoV-OC43 | NC_006213.1 | 5 | 29903 | 30741 | 29903 | 7891 | 7860 | 7891/29903 | 26.3887% | 1309.0 | 65.264 | no |
| HCoV-HKU1 | NC_006577.2 | 5 | 29903 | 29926 | 29903 | 8110 | 8077 | 8110/29903 | 27.1210% | 1354.0 | 66.746 | no |
| SARS-CoV | NC_004718.3 | 3 | 29903 | 29751 | 29751 | 29435 | 29399 | 29399/29751 | 98.8168% | 22291.0 | 80.264 | yes |
| MERS-CoV | NC_019843.3 | 8 | 29903 | 30119 | 29903 | 8783 | 8771 | 8783/29903 | 29.3716% | 1865.0 | 67.061 | no |

The only qualifying S_cov genome is SARS-CoV, NC_004718.3. Its shorter-molecule coverage is 29399/29751 = 98.8168%. The highest bitscore among its three HSPs is 22291, on the HSP with `pident` 80.264, `length` 24666, `evalue` 0.0, query interval 3347–27910, subject interval 3280–27798, copied from the first row of [`blast/NC_045512.2.S_cov.tsv`](blast/NC_045512.2.S_cov.tsv):

```
NC_045512.2	NC_004718	ref|NC_004718.3|	80.264	24666	0.0	22291	98	3347	27910	3280	27798	29903	29751
```

There is no qualifying-bitscore tie in S_cov: no other S_cov genome meets the 50% coverage rule, so NC_004718.3 is the unique best qualifying genome. The other five S_cov records have HSPs but shorter-molecule coverage between 18.8454% and 29.3716%, which is below 50%.

### Outgroup

The outgroup table is empty: no HSP with `evalue ≤ 1e-5` was reported against NC_140766.1. The step 6 outgroup homology gate therefore fails. That gate is required only for the monophyly tests in A, A-nested, and B. It is not required for B-blast.

## Application of the pre-registered rule

- The single query record has a qualifying hit in **S_cov** (NC_004718.3, shorter-molecule coverage 98.8168%, max bitscore 22291).
- The same query record has **no** qualifying hit in **S_flu** (no HSP at the pre-registered evalue cutoff).
- Therefore a combined MAFFT alignment and IQ-TREE were **not** built, as required by step 7 for a one-sided BLAST result.
- Outcome **B-blast** holds. Outcome B is not used. Outcomes A, A-nested, and A-blast do not hold.

## Parser bug on the first decision pass

The first pass over the same BLAST tables compared `sacc` values such as `NC_004718` to pinned `accession.version` strings such as `NC_004718.3` and therefore counted zero S_cov HSPs. That first summary is archived at [`archived/attempt-1-sacc-version-mismatch/BLAST-SUMMARY.json`](archived/attempt-1-sacc-version-mismatch/BLAST-SUMMARY.json). The pinned BLAST commands and tables were not wrong. The parser was changed to resolve `sacc` / `sseqid` onto the pinned `accession.version`, and the decision was re-computed. The later run is the decision run because the change is a documented bug of that kind. The letter was not chosen in order to cross a threshold.

## What this letter is not

This letter is not a statement about patient illness, isolation, transmission, or 5G. It is not outcome B (which would have required a combined tree). It does not use the words “influenza variant.” If this letter is later citation-checked and accepted, later tests may still use the database label SARS-CoV-2 as a search term, as already stated in [`PLAN.md`](../../PLAN.md).

Both “groups with influenza references” by a tree criterion, and a stronger nesting claim, remain untested by a combined tree in this run, because the pre-registered one-sided BLAST rule stopped at B-blast.

## Post-run runner fix

After this letter was written, a review found a latent bug in the combined-tree path of `tools/test01_run.py` (unversioned BLAST `sacc` in the site-homology trim). This run did not take that path. The runner was fixed afterwards; an offline re-parse of the committed BLAST tables still yields **B-blast** with the same coverage numbers. The decision rule was not changed.
