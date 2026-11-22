# Test 1 run log (decision host)

- Host: grok-bot-vm-342803711 (the box; pre-registered decision host)
- Time zone: America/Los_Angeles (Pacific Time)
- Run log started: 2026-11-21 11:16 PM PST
- Priority: nice 19 for compute steps
- Tool versions pinned below **before** any research genome was opened and before any tree was examined.

## Pinned tool versions (copied from the binaries on this host, 21 Nov 2026, 11:16 PM Pacific Time)

- NCBI BLAST+ `blastn`: 2.17.0+ (Package: blast 2.17.0, build Jul 1 2025 08:59:18), path `/opt/covid-tools/bin/blastn`
- NCBI BLAST+ `makeblastdb`: 2.17.0+, path `/opt/covid-tools/bin/makeblastdb`
- MAFFT: v7.526 (2024/Apr/26), path `/opt/covid-tools/bin/mafft`
- IQ-TREE: version 3.1.4 for Linux x86 64-bit built Sep 10 2026, resolved binary `iqtree3` at `/opt/covid-tools/bin/iqtree3` (also linked as `/opt/covid-tools/bin/iqtree`)
- Python: 3.13.5 at `/opt/covid-tools/venv/bin/python3`
- Commands, seed, and thread count are those pinned in `tests/TEST-01-genome-classification.md`. IQ-TREE uses `--seed 12345 -T 1`.

No research genomes had been opened at the time these versions were recorded.

## Notes

Amendments for the t1251u hold lift and residual r6 nits (trim limitation, extra gitignore names, PLAN wording) were written to the working tree before this log started opening inputs.

## Pass 1 and FASTA download

- Pre-data amendments were already on the working tree before any NCBI request.
- Official NCBI pages and documented Datasets / E-utilities responses were opened starting 11:16 PM Pacific Time on 21 Nov 2026. The Pass 1 list is `results/test-01/SOURCES-OPENED.md`.
- FASTA download of the 64 selected records: 11:24:08 PM Pacific Time, 21 Nov 2026, official E-utilities efetch. Hashes: `results/test-01/FASTA-HASHES.md`. Raw sequence files remain under `data/raw/test-01/` and are not committed.

## Analysis commands

The pinned BLAST, MAFFT, identity-gate, and IQ-TREE commands from `tests/TEST-01-genome-classification.md` are used below. Compute steps run with `nice 19`. Thread count is 1. IQ-TREE seed is 12345. Host: grok-bot-vm-342803711. Binary paths are those pinned at the top of this log.

## Bug in the first decision pass (parser only)

The pinned `blastn` command ran successfully. The S_cov table has 33 HSPs, including hits to `sseqid` `ref|NC_004718.3|`. The first decision script compared `sacc` (which BLAST printed as `NC_004718`, without the version) to the pinned `accession.version` (`NC_004718.3`) and therefore counted zero HSPs. That is a documented parser bug, not a reason to change the BLAST command or the decision rule. The first `BLAST-SUMMARY.json` is archived at `results/test-01/archived/attempt-1-sacc-version-mismatch/`. The second decision pass ran the same pinned `blastn` commands again with the same `-out` paths, so it overwrote the attempt-1 tables; no hash of those first tables was kept. The commands and inputs were the same, and BLAST is deterministic, but the rerun policy’s “keep both outputs” was not met for the tables themselves. `commands.log` records both command blocks. The first decision script’s stdout is archived with the first summary, and a copy also remains at `results/test-01/run-logs/test01_run.stdout` (that file is the attempt-1 output). The parser was then fixed to resolve `sacc` / `sseqid` onto the pinned `accession.version`, and the decision step was re-run.

## Post-run runner fix (Claude Test 1 review M1)

A later review found that the first parser fix lived only inside `genome_hit`. The site-homology trim in `run_combined` still looked up BLAST `sacc` (unversioned) in a map of pinned `accession.version` keys, so any future two-sided run would have treated every reference genome as having zero kept bases and returned C-homology without running MAFFT. That path was not taken in this run (one-sided B-blast; no combined tree). The runner was changed to resolve `sacc` once after parsing and to use the resolved accession in both places. The committed BLAST tables were not regenerated. An offline re-parse of those tables still yields letter B-blast, with the same coverage numbers, and the trim would now keep the three NC_004718.3 HSPs (it would have kept none before the fix). The first attempt’s parser code is the body of `genome_hit` before `resolve_blast_table` existed; only the fixed runner is in `tools/test01_run.py`.
