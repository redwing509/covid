# Rotation note

James asked that Covid be added to the research rotation (t1227s6218), then that it take a regular turn with a unit list taken from the conversation that set the project's direction (t1251u). The official cadence file is kept in the private research-rotation notes (not in this public repository). This note is the project-side description of that fit.

## Cadence

- The hold that had skipped Covid turns, and deferred Test 1, until after the usage reset at Mon 23 Nov 2026, 9:49 PM Pacific Time, was lifted by James t1251u (first Covid run requested t1252u / t1253u, 21 Nov 2026, evening Pacific Time).
- The shared research rotation runs every 12 hours, at about 10 AM and 10 PM Pacific Time (James t1247u). The cycle is digester → cancer-cure → Covid → Anti-Gravity → digester. Each Covid turn covers **one unit** from the list below, in order, starting with unit 1.
- **Unit 1 is Test 1** (genome classification; protocol already pre-registered in [`tests/TEST-01-genome-classification.md`](tests/TEST-01-genome-classification.md)). That is a project test, not a country survey.
- After Test 1 is written up, later Covid units proceed on later Covid turns, one unit at a time.
- Each Covid result goes into a pull request that is not merged without James's yes, and a one-line note in chat. **No email** on this track, same as cancer-cure.
- **Compute** (Test 1, later Meep SAR reuse, later phylogeny) should use spare capacity under the existing cancer-compute caps and pause rules, and must not starve Sentinel or outside-PR checks. Label outputs model-only until citation-checked. Run Test 1 at low priority (`nice 19`).

## Unit list (t1251u)

Units are taken from the conversation that set the direction of this project. One unit per Covid turn, in this order. Test 1 is unit 1 and runs first.

1. **Test 1 — genome classification.** Do the public sequences labeled as the COVID-19 reference pathogen group with influenza references, with other-coronavirus references, with neither, or is the comparison inconclusive? Protocol: [`tests/TEST-01-genome-classification.md`](tests/TEST-01-genome-classification.md). The words “influenza variant” are used only if the protocol’s A-nested test holds.
2. **Pathogen-existence and transmission checks.** Isolation and culture, electron microscopy, household and other transmission studies, animal challenge studies, and variant tracking (the H-A checks in [`PLAN.md`](PLAN.md), which H-B must also confront).
3. **Illness rates versus 5G rollout.** Compare illness rates with when, where, and how fast 5G rolled out, region by region, with the confounders listed in [`PLAN.md`](PLAN.md) controlled when the data exist.
4. **Pandemics before 5G, and places with no 5G.** The 1918, 1957, 1968, and 2009 pandemics, ordinary seasonal patterns that predate 5G, and places or settings the opened sources describe as having no 5G.
5. **Controlled RF-exposure immune studies.** Human and animal studies at power levels comparable to deployed 5G (or the paper’s stated dose), including the studies that found nothing, plus dose-response, with nulls and retractions recorded.
6. **SAR and photon-energy physics.** Absorbed-energy (SAR) and photon-energy calculations at the power levels 5G actually uses, from opened constants and stated formulas, labeled model-only.
7. **Published 5G–COVID or 5G–immune papers.** Every peer-reviewed paper that claims a 5G–COVID link, or a 5G–immune effect, together with retractions and rebuttals, checked and graded.
8. **The “cover” claim.** Judged only on primary documents that can actually be opened (official statements, leaked or formal documents, and contemporaneous coverage), not inferred from a scientific result alone. See [`PLAN.md`](PLAN.md).

This is a long list of units, not a conclusion. Later claimants or sub-questions may be added as further units after unit 8, without changing the order of units 1–8.

## Unit 1 run (t1252u / t1253u)

Test 1 was run on the decision host on 21 Nov 2026, evening Pacific Time, as a manual Covid unit run requested by James t1252u / t1253u after the t1251u hold lift. The pre-registered letter is **B-blast**. Write-up: [`results/test-01/TEST-01-RESULT.md`](results/test-01/TEST-01-RESULT.md). No email was sent. The pull request that carries this run is not merged without James's yes.


## Unit 2, first sub-unit (t1358u)

Pathogen-existence checks, isolation and culture only, were run as bite-size Hermes jobs on 24 Nov 2026, Pacific Time, on NVIDIA NIM Nemotron 3.5 Super VL, then citation-checked by fetching the cited pages. Write-up: [`results/unit-02-isolation-culture/UNIT-02-ISOLATION-CULTURE.md`](results/unit-02-isolation-culture/UNIT-02-ISOLATION-CULTURE.md). This does not finish the rest of unit 2 (electron microscopy, transmission, animal challenge, variant tracking), and it is not a conclusion about H-A or H-B. No email was sent. The pull request that carries this write-up is not merged without James's yes.
