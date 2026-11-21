# Tools (t1223u inventory)

James’s rule (t1223u): if we do not have the program needed to validate or disprove a claim, the rule is to build it, and to make sure it would pass peer-review standards in its industry.

**Nothing in this file is an install permit.** Installing a third-party program, downloading a new package, or accepting a license needs a separate OK from James.

Checked on the box on **21 Nov 2026, Pacific Time**. Mail and vps3 were not re-probed in this pass; Meep locations below are taken from the existing cancer-compute operations README, which records Meep 1.35.1 at `/opt/cancer-tools/envs/rf` on mail and vps3.

## Summary

We do **not** yet have all the programs this project needs. Several are planned and not written. Test 1’s standard virology tools are not installed on the box. The cancer project’s RF absorption tools can be reused for SAR work, but Meep is not installed on the box itself.

No tool has been run for this project yet. Builds and first runs wait until after the usage reset at Mon 23 Nov 2026, 9:49 PM Pacific Time, except a later-marked tiny step, and except installs James has OK’d.

## Inventory

### 1. Test 1 genome comparison (BLAST and/or MAFFT + IQ-TREE)

- **Claim it serves:** Test 1 — whether public sequences labeled as the COVID-19 reference pathogen are an influenza variant.
- **Standard:** Public, accession-pinned NCBI records; BLAST+ and/or MAFFT alignment; IQ-TREE with model selection and bootstrap or ultrafast bootstrap; a decision rule written before the run; pinned versions and saved commands. This is ordinary practice in viral genome papers.
- **Have it?** **No**, not on the box (21 Nov 2026, Pacific Time). `blastn` / BLAST+, `mafft`, `iqtree` / `iqtree2`, Nextstrain / Augur, and Biopython were not found. Python 3.13.5 is present.
- **Plan:** After James OKs the install (or an equivalent pinned method), add a small MIT-licensed wrapper under `tools/` that downloads only the pinned accessions, runs the protocol in [`tests/TEST-01-genome-classification.md`](tests/TEST-01-genome-classification.md), and writes a machine-readable summary. No run before the protocol and versions are recorded.

### 2. Public sequence snapshot (NCBI; GISAID if a legitimate open view exists)

- **Claim it serves:** Test 1 inputs; later H-A checks of database deposits and counts.
- **Standard:** Dated query, accessions and versions copied from the opened page or API, file hashes, and a repeatable command. Counts are never recalled from memory. GISAID use only if access is legitimate and the terms allow the snapshot we need; otherwise write `NOT FOUND` for GISAID and use NCBI.
- **Have it?** **No** project script yet. A browser or `curl` can open public NCBI pages when the run starts.
- **Plan:** A small snapshot script, or a documented manual download, checked into `tools/` after review. Do not invent accessions in the meantime.

### 3. Variant phylogenetics (Nextstrain or IQ-TREE on public sequences)

- **Claim it serves:** H-A prediction that variants track in a connected tree that matches reported spread. This is separate from Test 1.
- **Standard:** Public accessions, stated alignment and tree method, pinned Nextstrain / Augur or IQ-TREE versions, and a comparison to opened published trees.
- **Have it?** **No.** Nextstrain / Augur and IQ-TREE were not found on the box.
- **Plan:** After Test 1, and after an install OK, reuse the same IQ-TREE toolchain if that is enough, or Nextstrain if James OKs that install.

### 4. Isolation, culture, electron microscopy, transmission, and animal-challenge review

- **Claim it serves:** H-A pathogen-existence and causation checks; also a hurdle H-B must confront.
- **Standard:** Opened papers, quoted methods and results, evidence grading, Rivers / Koch-style criteria as the opened sources apply them, independent replication, nulls and disputed claims included. No special simulator is required for the literature review itself.
- **Have it?** **Yes**, as a method: the citation workflow in [`METHOD.md`](METHOD.md). **No** separate program is required for the review. No papers have been opened for this project yet.
- **Plan:** A findings file in a later pull request, after the usage reset, not a Hermes survey yet.

### 5. Ecological time-series and regression (illness rates versus 5G rollout)

- **Claim it serves:** H-B predictions on timing, location, and speed of rollout; places with no 5G; pre-5G pandemics; seasonality; dose-response at the population level.
- **Standard:** A protocol written before the fit; opened sources for both illness rates and rollout dates; confounder controls (testing, age, density, mobility, season, policy, and others listed in [`PLAN.md`](PLAN.md)); interrupted time series, difference-in-differences, or another stated design that epidemiology reviewers would expect; pre-stated sensitivity analyses; no specification search after seeing the p-values. Missing confounders are marked `NOT FOUND`.
- **Have it?** **No.** The script has not been written. On the box: Python 3.13.5, pandas 3.0.6, and numpy 2.5.5 were present. `statsmodels` and `scipy` were not. R was not found.
- **Plan:** Build a Python script with a stated design and tests, using pandas / numpy and, if James OKs the install, statsmodels or an equivalent. Do not install packages until that OK. Historical series (1918, 1957, 1968, 2009, and seasonal ILI) are inputs from opened sources, not from memory.

### 6. Meta-analysis of RF-exposure immune-marker studies

- **Claim it serves:** H-B prediction that controlled human and animal RF exposure, at deployed power levels, changes immune markers (lymphocyte counts, cytokines, NK activity, or other markers the papers measure). Includes nulls and dose-response.
- **Standard:** A protocol first; PRISMA reporting; risk-of-bias grading (for example Cochrane RoB 2 for human randomized or controlled studies, SYRCLE for animal studies, or another stated tool); inclusion of null and retracted records (retractions quoted, then excluded from the pooled estimate as the protocol states); a random-effects or other pre-stated model. R `metafor` is a common peer-review standard; a Python equivalent is acceptable if the method is stated and validated against a known example.
- **Have it?** **No.** R and `metafor` were not found on the box. Python `statsmodels` and `scipy` were not found either. No project meta-analysis script exists.
- **Plan:** After the usage reset, either request an install of R and `metafor`, or build a Python tool and check it against a published worked example. The literature screen can start with a SOURCES OPENED list before any pooling.

### 7. RF photon energy versus chemical bond energies

- **Claim it serves:** Physical plausibility of a direct ionization-like path from 5G photons to molecular damage, as one piece of the mechanism discussion. This calculation cannot, by itself, prove or disprove immune effects at non-ionizing doses.
- **Standard:** Constants and formulas copied from opened sources (for example a CODATA or textbook page for Planck’s constant and a chemistry source for bond energies; 5G band frequencies from opened allocation or operator records). Show the arithmetic. Do not recall the numbers.
- **Have it?** **No** project script yet. The box has Python 3, which is enough once the constants are copied from opened pages. The cancer-cure frequency-absorption notes may already cite some band records; any number reused here must still be copied from an opened source for this project.
- **Plan:** A short stdlib script after the sources are opened. Tiny enough that it could be a first post-reset coding step, still not run until the constants are in a SOURCES OPENED list.

### 8. SAR at deployed 5G power (reuse cancer Meep tools)

- **Claim it serves:** Tissue dose at stated deployed power and frequency, as a check on whether controlled-study doses and real deployments are in the same range.
- **Standard:** Published tissue dielectric parameters; mesh or resolution convergence; validation against a known analytic case (the cancer project already reports Meep checks against exact formulas on spheres and layers — those figures may be reused only if the opened cancer-project note is cited); results labeled **model-only**, not a medical conclusion. Peer reviewers in bioelectromagnetics expect the validation and the tissue-parameter source.
- **Have it?** **Partly.** The cancer-cure in-repo analytic tool lives at `/workspace/cancer-cure/tools/frequency_absorption` (Python, stdlib). Cancer-compute documents Meep 1.35.1 at `/opt/cancer-tools/envs/rf` on mail and vps3. Meep was **not** importable on the box in this check. Reusing those tools for this project is a plan, not a run. New job grids or tissue sites need the usual review before any shared-queue change, and must not interfere with Sentinel or with the cancer queues’ caps.
- **Plan:** First reuse the analytic script with 5G bands and tissue sites copied from opened sources. A Meep run on mail or vps3 only after a written job spec, and not before the usage reset unless James asks.

### 9. Citation and grading workflow

- **Claim it serves:** Every literature check in this project.
- **Standard:** Quote plus link, `NOT FOUND` rather than a guess, no recalled numbers, nulls and retractions included, second-person citation check, as in [`METHOD.md`](METHOD.md) and the cancer-cure method.
- **Have it?** **Yes** (the method). No findings files have been filled yet.

## Build order (after the reset, and after any needed install OK)

1. Test 1 toolchain and wrapper (highest priority; Test 1 runs first).
2. Ecological time-series script (core H-B test).
3. Photon-energy calculator (small).
4. Analytic SAR reuse, then Meep only if needed.
5. Meta-analysis tool, once the RF-immune paper list exists.
6. Variant-phylogeny reuse of the Test 1 toolchain.

## Programs not found and likely to need an install OK

- BLAST+
- MAFFT
- IQ-TREE
- Optional: Nextstrain / Augur, Biopython
- Optional: R and the `metafor` package, or Python `statsmodels` / `scipy` as an equivalent
