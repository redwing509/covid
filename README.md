# Covid — an evidence review of cause and classification

> **This is not medical advice.**
> Nothing in this repository diagnoses, treats, or replaces care from a qualified clinician.
> Do not start, stop, or replace any treatment on the basis of these notes.
> Results, when they exist, are reported as graded evidence, not as a recommendation.

**Status (21 Nov 2026, Pacific Time):** project skeleton only. No research run has started. No genome comparison has been run. No conclusion has been reached on any hypothesis. The first research run waits until after the usage reset at **Mon 23 Nov 2026, 9:49 PM Pacific Time**, unless a later note marks a step as tiny enough to do sooner.

This project was started at James's request (t1225u, confirmed t1225s6200; hypotheses clarified t1226u and t1227u). It is an evidence review. Evidence decides. Results are reported whichever way they land. There is **no email** on this project. Nothing is pushed to a remote or merged without the full review set and James's yes.

## Goal

Prove or disprove, at a standard that would pass peer review in the relevant field, two things:

1. **Test 1 (runs first):** what kind of virus, if any, is associated with the illness called COVID-19 — specifically, whether sequences labeled as the COVID-19 reference pathogen in public databases group with influenza references (an influenza variant) or with something else. This question is **open**. The project does **not** start from the assumption that it is influenza, and it does **not** start from the assumption that it is not. The comparison is run, and the result is written up as-is.
2. **Main causal hypotheses:** whether 5G wireless exposure, by compromising immune function, is the main driver of COVID, flu, cold, and other illness rates, or whether the pathogens themselves are the primary cause, with host factors modifying risk.

A related claim from the original request is also in scope: that the virus claim was a cover for 5G deployment. That claim is tested by the same evidence, not by a separate starting assumption.

## Test 1 — open classification question (no starting assumption)

James asked that the project not treat the classification of the COVID-19 pathogen as already proved (t1227u). Until Test 1 is run against opened public sequences, with a pre-registered decision rule, and the citations are checked, this repository will not state in its own voice that the pathogen is an influenza variant, and it will not state in its own voice that it is not.

- The illness name **COVID-19**, and database labels such as **SARS-CoV-2**, are used as *labels found in sources and databases*, not as a settled taxonomy.
- Test 1 compares public NCBI sequences labeled as SARS-CoV-2 references against public influenza A, influenza B, and other coronavirus reference sequences, using standard tools (BLAST and/or MAFFT alignment, plus an IQ-TREE phylogenetic tree), pinned versions, and a decision rule written down **before** the run. See [`PLAN.md`](PLAN.md) and [`tests/TEST-01-genome-classification.md`](tests/TEST-01-genome-classification.md).
- Whatever the comparison shows is what the report will say.

## Hypotheses (stated neutrally)

**H-A (pathogen-primary).** One or more infectious pathogens are the primary cause of COVID-19, influenza, colds, and the other illnesses under review. Host factors (age, prior immunity, other exposures, nutrition, and so on) can modify who gets sick and how badly, but they are not the main driver of the outbreak patterns.

**H-B (immune-compromise-primary; the claim under test).** 5G wireless exposure compromises immune function, which raises susceptibility, so that this immune compromise — more than the pathogen — is the main driver of COVID, flu, cold, and other illness rates. Under this claim, once a respiratory virus is circulating it can keep spreading, but the reason most people get sick is the immune effect of the rollout (timing, location, and speed), not the pathogen acting as the main cause.

Both are treated as testable claims. The write-up does not prefer either one in advance.

## Methods in brief

The full method is in [`METHOD.md`](METHOD.md). The tests and their predictions are in [`PLAN.md`](PLAN.md). Programs needed to run those tests, whether we have them, and the peer-review standard for each, are in [`TOOLS.md`](TOOLS.md) (James, t1223u).

In short:

- Every factual claim needs a direct quote plus a URL or DOI from a source that was opened (full text or abstract). If that cannot be done, the claim is dropped or marked `NOT FOUND`.
- Numbers, accessions, author names, dates, and product names are copied from an opened source, not recalled from memory.
- Negative, null, harmful, and retracted findings are recorded, not omitted.
- Two passes: a **SOURCES OPENED** list first, then findings only from that list.
- No Sci-Hub, Library Genesis, or similar sites. No raw paywalled PDFs in the notes.
- Model and software output is labeled as such and is not a medical conclusion.
- Code and notes that go to a remote need the full review set used on this account, and James's yes to merge.

## Evidence scale

Each study or analysis is given **one** evidence level, taken from the design in the opened source (or from the pre-registered method, for work we run ourselves), not from how impressive the result sounds. If the design is unclear, say so and use the lower of the plausible levels.

| Level | What it means | Typical source |
|---|---|---|
| **Physics / calculation** | Energy, dosimetry, or similar, from opened constants and stated formulas | Calculation or FDTD / SAR model |
| **In vitro** | Cells or other systems outside a living animal or human | Laboratory paper |
| **Genomic / sequence** | Public or deposited sequence comparison, alignment, or tree | Database records plus stated method |
| **Animal** | Living non-human animals | Preclinical in vivo study, including challenge studies |
| **Case report** | One person or a very small uncontrolled series | Case report or case series |
| **Observational / ecological** | Cohort, case-control, or population rates versus exposure or time | Observational or surveillance study |
| **Controlled human exposure** | Interventional RF or other exposure in humans, not necessarily a disease trial | Controlled exposure study |
| **Early trial** | First-in-human, Phase I, Phase II, or other early interventional trial | Registered or published early trial |
| **RCT** | Randomized controlled trial in humans | Phase III or other randomized trial |
| **Systematic review / meta-analysis** | Systematic review or meta-analysis of primary studies | Cochrane or other systematic review; PRISMA-style review we run |

Use the **highest design the opened source actually is**, not the highest design it cites.

## Honesty rules

These are the same rules used on the cancer-cure project (James, t1084u, and the cancer-cure method):

1. **Quote plus locator.** Every factual claim includes a direct quote of the supporting sentence and that source’s URL or DOI.
2. **`NOT FOUND`, never a guess.** When a search finds nothing, write `NOT FOUND` and say what was searched.
3. **Copy, don’t recall.** Do not write numbers, accessions, institution names, author names, dates, or product names unless they are copied from a source opened for that check.
4. **Two passes on a fresh search.** Pass 1 is only a SOURCES OPENED list. Pass 2 writes findings only from that list.
5. **Say how the source was opened.** `full text`, `abstract only`, or `not opened`.
6. **Paywalls.** Look for a legitimate alternate copy. Do not use Sci-Hub, Library Genesis, or similar sites.
7. **Nulls and retractions are in scope.** Include them, and grade the unretracted record that remains.
8. **No email** on this project.

## Repository layout

- [`METHOD.md`](METHOD.md) — citation rules, evidence scale, how entries are written
- [`PLAN.md`](PLAN.md) — testable predictions of each claim, and how each will be checked
- [`tests/TEST-01-genome-classification.md`](tests/TEST-01-genome-classification.md) — pre-registered protocol and decision rule for Test 1 (no results yet)
- [`TOOLS.md`](TOOLS.md) — programs needed, whether we have them, and the peer-review standard for each
- [`ROTATION.md`](ROTATION.md) — a suggestion for how this project could fit the daily research rotation; it does **not** change the existing rotation
- [`CONTRIBUTING.md`](CONTRIBUTING.md) — how changes are reviewed
- [`LICENSE`](LICENSE) — MIT for software; CC BY 4.0 for original notes

This copy is **local** on the box (`/workspace/covid`). It is not on GitHub yet. See the note at the end of [`PLAN.md`](PLAN.md).

## License

The software and repository tooling, if any, are under the MIT License — see [`LICENSE`](LICENSE).

Original research summaries and documentation in this repository are also licensed under [Creative Commons Attribution 4.0 International (CC BY 4.0)](https://creativecommons.org/licenses/by/4.0/). Short quotations from papers and databases remain the copyright of their authors and publishers.
