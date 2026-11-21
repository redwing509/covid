# Tools (t1223u inventory, updated t1227s6218)

James’s rule (t1223u): if we do not have the program needed to validate or disprove a claim, the rule is to build it, and to make sure it would pass peer-review standards in its industry.

James authorized the Test 1 and statistics install on 21 Nov 2026 (t1227s6218): BLAST+, MAFFT, IQ-TREE, Biopython, scipy, statsmodels, and R with metafor, on the box and on mail. Nextstrain / Augur was optional and was **not** installed. New packages beyond this list still need a separate OK. Installing on rig1 or the laptop is not allowed.

Pinned names, versions, URLs, and checksums are in [`tools/VERSIONS.txt`](tools/VERSIONS.txt), copied from `/opt/covid-tools/VERSIONS` on the install hosts. Host install logs live only on those machines, at `/opt/covid-tools/INSTALL-LOG.txt`.

Checked on the box and on mail on **21 Nov 2026, Pacific Time**.

## Summary

The standard Test 1 genome-comparison tools, and the statistics tools for later meta-analysis and regression, are now installed under `/opt/covid-tools` on the box and on mail. Smoke tests passed on both hosts. **Test 1 itself has not been run.** No research genomes were downloaded. The first research run still waits until after the usage reset at Mon 23 Nov 2026, 9:49 PM Pacific Time.

Other project needs remain: a Test 1 wrapper script, a sequence-snapshot script, the ecological time-series script, the photon-energy calculator, and SAR work that reuses the cancer project's tools. Meep is still not installed on the box.

## How to use the installed tools

```bash
source /opt/covid-tools/env.sh
# or prepend /opt/covid-tools/bin and /opt/covid-tools/venv/bin to PATH
```

A login-shell snippet was also added at `/etc/profile.d/covid-tools.sh` on both hosts.

## Inventory

### 1. Test 1 genome comparison (BLAST+ / MAFFT / IQ-TREE)

- **Claim it serves:** Test 1 — whether public sequences labeled as the COVID-19 reference pathogen are an influenza variant.
- **Standard:** Public, accession-pinned NCBI records; BLAST+ and/or MAFFT alignment; IQ-TREE with model selection and bootstrap or ultrafast bootstrap; a decision rule written before the run; pinned versions and saved commands. This is ordinary practice in viral genome papers.
- **Have it?** **Yes**, on the box and on mail (21 Nov 2026, Pacific Time). Official binaries, checksum-verified (see [`tools/VERSIONS.txt`](tools/VERSIONS.txt)):
  - NCBI BLAST+ **2.17.0** (official Linux x64 tarball; official MD5 checked)
  - MAFFT **7.526** (official portable Linux tarball; SHA-256 recorded; the official site did not offer a checksum file)
  - IQ-TREE **3.1.4** (official Linux intel release; GitHub asset SHA-256 checked)
  - Biopython **1.88** in `/opt/covid-tools/venv` (official PyPI SHA-256 checked)
- **Smoke tests (not Test 1):**
  - BLAST+: constructed 60-nt query against a two-sequence local database; exact self-hit, 100% identity, length 60. PASS on box and mail.
  - MAFFT: four constructed nucleotide sequences; one alignment of length 60. PASS on box and mail.
  - IQ-TREE: official bundled `example.phy` (17 sequences, 1998 nucleotide sites) with `-m HKY`; report and treefile written; best score **-23117.030**. PASS on box and mail. Both hosts printed a non-fatal `libarcher.so: cannot open shared object file` message; the run still finished.
- **Plan:** Add a small MIT-licensed wrapper under `tools/` that downloads only pinned accessions, runs the protocol in [`tests/TEST-01-genome-classification.md`](tests/TEST-01-genome-classification.md), and writes a machine-readable summary. **Do not run Test 1 until after the usage reset.**

### 2. Public sequence snapshot (NCBI; GISAID if a legitimate open view exists)

- **Claim it serves:** Test 1 inputs; later H-A checks of database deposits and counts.
- **Standard:** Dated query, accessions and versions copied from the opened page or API, file hashes, and a repeatable command. Counts are never recalled from memory. GISAID use only if access is legitimate and the terms allow the snapshot we need; otherwise write `NOT FOUND` for GISAID and use NCBI.
- **Have it?** **No** project script yet. A browser or `curl` can open public NCBI pages when the run starts.
- **Plan:** A small snapshot script, or a documented manual download, checked into `tools/` after review. Do not invent accessions in the meantime.

### 3. Variant phylogenetics (Nextstrain or IQ-TREE on public sequences)

- **Claim it serves:** H-A prediction that variants track in a connected tree that matches reported spread. This is separate from Test 1.
- **Standard:** Public accessions, stated alignment and tree method, pinned Nextstrain / Augur or IQ-TREE versions, and a comparison to opened published trees.
- **Have it?** **Partly.** IQ-TREE 3.1.4 is installed (see item 1). Nextstrain / Augur was optional and was **not** installed.
- **Plan:** After Test 1, reuse the IQ-TREE toolchain if that is enough. Nextstrain only if James later OKs that install.

### 4. Isolation, culture, electron microscopy, transmission, and animal-challenge review

- **Claim it serves:** H-A pathogen-existence and causation checks; also a hurdle H-B must confront.
- **Standard:** Opened papers, quoted methods and results, evidence grading, Rivers / Koch-style criteria as the opened sources apply them, independent replication, nulls and disputed claims included. No special simulator is required for the literature review itself.
- **Have it?** **Yes**, as a method: the citation workflow in [`METHOD.md`](METHOD.md). **No** separate program is required for the review. No papers have been opened for this project yet.
- **Plan:** A findings file in a later pull request, after the usage reset, not a Hermes survey yet.

### 5. Ecological time-series and regression (illness rates versus 5G rollout)

- **Claim it serves:** H-B predictions on timing, location, and speed of rollout; places with no 5G; pre-5G pandemics; seasonality; dose-response at the population level.
- **Standard:** A protocol written before the fit; opened sources for both illness rates and rollout dates; confounder controls (testing, age, density, mobility, season, policy, and others listed in [`PLAN.md`](PLAN.md)); interrupted time series, difference-in-differences, or another stated design that epidemiology reviewers would expect; pre-stated sensitivity analyses; no specification search after seeing the p-values. Missing confounders are marked `NOT FOUND`.
- **Have it?** **Partly.** The project script has not been written. On both hosts, `/opt/covid-tools/venv` has Python (3.13.5 on the box, 3.12.3 on mail), pandas **3.1.1**, numpy **2.5.5**, scipy **1.18.1**, and statsmodels **0.15.0** (official PyPI SHA-256 checked for the primary wheels).
- **Plan:** Build a Python script with a stated design and tests, using those packages. Historical series (1918, 1957, 1968, 2009, and seasonal ILI) are inputs from opened sources, not from memory.

### 6. Meta-analysis of RF-exposure immune-marker studies

- **Claim it serves:** H-B prediction that controlled human and animal RF exposure, at deployed power levels, changes immune markers (lymphocyte counts, cytokines, NK activity, or other markers the papers measure). Includes nulls and dose-response.
- **Standard:** A protocol first; PRISMA reporting; risk-of-bias grading (for example Cochrane RoB 2 for human randomized or controlled studies, SYRCLE for animal studies, or another stated tool); inclusion of null and retracted records (retractions quoted, then excluded from the pooled estimate as the protocol states); a random-effects or other pre-stated model. R `metafor` is a common peer-review standard; a Python equivalent is acceptable if the method is stated and validated against a known example.
- **Have it?** **Yes**, for the software (not yet a project script). Distro packages, `--no-install-recommends`:
  - Box (Debian 13): R **4.5.0** (`r-base-core` 4.5.0-3), `metafor` **4.8.0** (`r-cran-metafor` 4.8-0-1)
  - Mail (Ubuntu 24.04): R **4.3.3** (`r-base-core` 4.3.3-2build2), `metafor` **4.4.0** (`r-cran-metafor` 4.4-0-1)
- **Smoke test:** random-effects REML meta-analysis of the `dat.bcg` data set (Colditz et al. 1994 BCG vaccine studies, as shipped in the `metadat` package). The printed results were:
  - estimate **-0.7145**, se **0.1798**, tau^2 **0.3132**, Q(df = 12) **= 152.2330**, k = 13
  - These match the printed numbers in the opened local vignette `/usr/lib/R/site-library/metafor/doc/metafor.pdf` (Viechtbauer 2010, *Journal of Statistical Software* 36(3), https://doi.org/10.18637/jss.v036.i03), which states that the estimated average log relative risk is µ̂ = −0.7145 (95% CI: −1.0669 to −0.3622). PASS on box and mail (the two `metafor` versions agreed to the printed four decimals).
  - A Python DerSimonian–Laird calculation on the same `yi`/`vi` matched `metafor` `method="DL"` exactly (estimate −0.7141172221). That is a cross-check of the Python path; the published vignette numbers above are the REML results.
- **Plan:** After the usage reset, the literature screen can start with a SOURCES OPENED list before any pooling. The project meta-analysis script is not written yet.

### 7. RF photon energy versus chemical bond energies

- **Claim it serves:** Physical plausibility of a direct ionization-like path from 5G photons to molecular damage, as one piece of the mechanism discussion. This calculation cannot, by itself, prove or disprove immune effects at non-ionizing doses.
- **Standard:** Constants and formulas copied from opened sources (for example a CODATA or textbook page for Planck’s constant and a chemistry source for bond energies; 5G band frequencies from opened allocation or operator records). Show the arithmetic. Do not recall the numbers.
- **Have it?** **No** project script yet. The box has Python 3, which is enough once the constants are copied from opened pages.
- **Plan:** A short stdlib script after the sources are opened. Still not run until the constants are in a SOURCES OPENED list.

### 8. SAR at deployed 5G power (reuse cancer Meep tools)

- **Claim it serves:** Tissue dose at stated deployed power and frequency, as a check on whether controlled-study doses and real deployments are in the same range.
- **Standard:** Published tissue dielectric parameters; mesh or resolution convergence; validation against a known analytic case (the cancer project already reports Meep checks against exact formulas on spheres and layers — those figures may be reused only if the opened cancer-project note is cited); results labeled **model-only**, not a medical conclusion. Peer reviewers in bioelectromagnetics expect the validation and the tissue-parameter source.
- **Have it?** **Partly.** The cancer-cure in-repo analytic tool lives at `/workspace/cancer-cure/tools/frequency_absorption` (Python, stdlib). Cancer-compute documents Meep 1.35.1 at `/opt/cancer-tools/envs/rf` on mail and vps3. Meep was **not** importable on the box in the earlier check. Reusing those tools for this project is a plan, not a run.
- **Plan:** First reuse the analytic script with 5G bands and tissue sites copied from opened sources. A Meep run on mail or vps3 only after a written job spec, and not before the usage reset unless James asks.

### 9. Citation and grading workflow

- **Claim it serves:** Every literature check in this project.
- **Standard:** Quote plus link, `NOT FOUND` rather than a guess, no recalled numbers, nulls and retractions included, second-person citation check, as in [`METHOD.md`](METHOD.md) and the cancer-cure method.
- **Have it?** **Yes** (the method). No findings files have been filled yet.

## Build order

1. Test 1 wrapper (highest priority; Test 1 runs first, after the usage reset).
2. Ecological time-series script (core H-B test).
3. Photon-energy calculator (small).
4. Analytic SAR reuse, then Meep only if needed.
5. Meta-analysis project script, once the RF-immune paper list exists.
6. Variant-phylogeny reuse of the Test 1 toolchain.

## Programs still not installed

- Nextstrain / Augur (optional; not requested as required)
- Meep on the box (available on mail and vps3 for cancer work)
