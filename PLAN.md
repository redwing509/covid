# Plan

**Status (24 Nov 2026, Pacific Time):** plan and pre-registered Test 1 decision rule, plus the authorized tool install (t1227s6218). Test 1 has been run on the decision host; the pre-registered letter is **B-blast**, written up in [`results/test-01/TEST-01-RESULT.md`](results/test-01/TEST-01-RESULT.md). A first literature check for the unit 2 isolation-and-culture sub-unit is written up in [`results/unit-02-isolation-culture/UNIT-02-ISOLATION-CULTURE.md`](results/unit-02-isolation-culture/UNIT-02-ISOLATION-CULTURE.md). The rest of the unit 2 checks, and H-A and H-B as a whole, have not been tested. No causal hypothesis has been accepted or rejected.

This file lists the testable predictions of each claim and how each will be checked. Methods and citation rules are in [`METHOD.md`](METHOD.md). Programs are in [`TOOLS.md`](TOOLS.md).

### Amendment log

| Date (Pacific Time) | Commit | What changed | Why | Data opened? |
|---|---|---|---|---|
| 21 Nov 2026, evening | 42b5a19 | Lifted the plan text that had deferred the first research run, including Test 1 compute, until after the Mon 23 Nov 2026, 9:49 PM Pacific Time usage reset. Test 1 may now be started under the already pre-registered protocol. The decision rule is unchanged. | James t1251u lifted the hold; t1252u / t1253u asked for one Covid run, which is Test 1 | No |
| 21 Nov 2026, evening | 42b5a19 | In the Test 1 “What would be inconclusive” summary, named the step 8 site-homology trim (C-homology) among the examples. [`tests/TEST-01-genome-classification.md`](tests/TEST-01-genome-classification.md) still governs if this summary and the protocol differ. The decision rule is unchanged. | Residual CodeRabbit / Claude r6 nit (PLAN wording, Claude r6 N-4) | No |
| 21 Nov 2026, late evening | 1653a1b | Logged that the 42b5a19 plan rows were committed in the same revision as the Test 1 outputs, and that their pre-data status rests on the run log. Noted the post-run runner fix (Claude M1) that does not change the letter. The decision rule is unchanged. | Claude Test 1 review S3, plus the M1 runner fix | Yes (Test 1 already run; letter B-blast unchanged) |
| 24 Nov 2026, late morning | 66f9b28 | Logged a first, citation-checked literature write-up for the unit 2 isolation-and-culture sub-unit only. The Test 1 letter, and the remaining unit 2 checks, are unchanged. No causal hypothesis is accepted or rejected. | James t1358u asked for Hermes research and a GitHub results PR; this is that sub-unit | Yes (published papers and a comment/reply, as listed in the write-up) |

The 42b5a19 rows above were written to the working tree before any Test 1 input was opened. They were committed in the same revision as the Test 1 outputs (`42b5a19`). Git cannot confirm that on-disk order; their pre-data status rests on the Test 1 run log.

## Order of work

1. **Test 1 first** — classification of the public sequences labeled as the COVID-19 reference pathogen (whether they group with influenza references, with other-coronavirus references, with neither, or the comparison is inconclusive). Open question; no starting assumption. Protocol: [`tests/TEST-01-genome-classification.md`](tests/TEST-01-genome-classification.md).
2. **Pathogen-existence and transmission checks** that H-A needs, and that H-B must also confront (isolation and culture, electron microscopy, household and other transmission studies, animal challenge studies, variant tracking).
3. **H-B immune-compromise checks** (illness rates versus 5G rollout timing, location, and speed; pre-5G pandemics; places with no 5G; seasonality; controlled RF-exposure immune-marker studies, including nulls; dose-response; SAR at deployed power; any peer-reviewed paper that claims a 5G–COVID or 5G–immune link, including retractions).

The reset hold was lifted by James t1251u (first Covid run requested t1252u / t1253u). Test 1 was run on the decision host on 21 Nov 2026, evening Pacific Time. The pre-registered letter is **B-blast**; see [`results/test-01/TEST-01-RESULT.md`](results/test-01/TEST-01-RESULT.md). A first isolation-and-culture literature check has now been written up (t1358u); the rest of unit 2 has not been run. No email is sent.

## Test 1 — do the public sequences labeled as the COVID-19 reference pathogen group with influenza references? (open)

**Question.** Public databases contain sequences labeled as the reference pathogen for COVID-19 (commonly labeled SARS-CoV-2). Do those sequences group with influenza A and/or influenza B references, group with sequences labeled as other coronaviruses, group with neither, or is the comparison inconclusive? The words “influenza variant” are used only if the protocol’s A-nested test holds.

**This question is open.** The plan does not assume either answer. James asked that the project not treat the classification as already proved (t1227u). The comparison is run at a peer-review standard, and the result is reported as-is.

**How it will be checked.** A genome comparison of public NCBI records, with versions pinned and a decision rule written before the run. Tools: BLAST and/or MAFFT alignment, plus a phylogenetic tree with IQ-TREE. Full protocol and decision rule: [`tests/TEST-01-genome-classification.md`](tests/TEST-01-genome-classification.md).

**What would support “groups with influenza references”.** Under the pre-registered rule in [`tests/TEST-01-genome-classification.md`](tests/TEST-01-genome-classification.md), the query sequences meet outcome A or A-blast (and A-nested only if the stronger nesting test also holds).

**What would support “groups with the other-coronavirus references”.** Under the same rule, the query sequences meet outcome B or B-blast.

**What would be inconclusive.** Outcome C, as defined in the protocol, including: support below the stated thresholds, missing records, a failed alignment-quality gate, a failed step 8 site-homology trim (C-homology), a missing or unusable outgroup, or a topology that matches neither set. Organization is reported alongside the letter and does not by itself make the result C. If this summary and the protocol ever differ, [`tests/TEST-01-genome-classification.md`](tests/TEST-01-genome-classification.md) governs. Both answers remain open.

Later tests may still use the database label SARS-CoV-2 as a search term. They must not treat Test 1 as settled until that write-up is citation-checked.

## H-A — pathogen-primary: testable predictions

If infectious pathogens are the primary cause of the illnesses under review, and host factors only modify risk, then the opened evidence should show some or all of the following. Each item is a check, not a finding.

| Check | Prediction if H-A is right | How it will be checked |
|---|---|---|
| Isolation and culture | The pathogen associated with COVID-19 can be isolated and cultured by independent labs, with methods and results quoted from opened papers | Literature review; grade design; include failed or disputed isolation claims and replies |
| Whole-genome sequencing and public databases | Independent deposits exist in public sequence databases (NCBI and, where a legitimate open view is available, GISAID). Counts and accessions are copied from an opened page or a dated query, never recalled | Opened database pages or API snapshots, with query and date recorded |
| Electron microscopy | Images and measurements of particles from infected samples are published and can be opened | Literature review; quote what the paper actually shows |
| Transmission | Illness clusters in households and other close-contact settings in a way the studies attribute to transmission of the pathogen, including settings where 5G exposure is absent or unchanged | Household and outbreak studies; ships, prisons, and other closed settings as the sources describe them |
| Animal challenge (Koch-style) | Inoculating a suitable animal with the isolated pathogen produces the illness, and the same pathogen can be recovered, as the opened studies report | Hamster, macaque, or other models named in opened sources; quote outcomes, including nulls |
| Phylogenetic tracking of variants | Sequences change over time in a connected tree that matches the geographic spread reported in opened sources | Published trees and, later, a Nextstrain or IQ-TREE run on public sequences (separate from Test 1) |
| Illness without a new RF rollout | Similar respiratory pandemics and seasonal flu/cold patterns exist before 5G, and in places with no 5G, if the opened records show that | Historical surveillance (the sources will be opened for 1918, 1957, 1968, and 2009, and for seasonal ILI); places and ships the sources describe as having no 5G |

H-A does **not** require that host factors are irrelevant. It requires that the pathogen is the main cause of the illness patterns.

## H-B — immune-compromise-primary: testable predictions

If 5G exposure compromises immune function, and that compromise — more than the pathogen — is the main driver of COVID, flu, cold, and other illness rates, then the opened evidence should show some or all of the following. Each item is a check, not a finding.

| Check | Prediction if H-B is right | How it will be checked |
|---|---|---|
| Timing, location, and speed of 5G rollout | Respiratory illness rates (ILI / flu surveillance, and COVID as reported) rise where and when 5G was commercially deployed, and rise more where rollout was faster, after stated confounders are taken into account | An ecological time-series and regression script with confounder controls (see [`TOOLS.md`](TOOLS.md)). Rollout dates and locations from opened official or industry records; illness rates from opened surveillance sources |
| Places with no 5G | Illness rates attributed to COVID, flu, or colds are absent, delayed, or clearly lower in places and settings the opened sources describe as having no 5G, including ships at sea when that is what the record shows | Same analysis; pre-specify how “no 5G” is defined from opened coverage maps or official statements |
| Pre-5G pandemics | If H-B is the *main* driver of this class of illness, large flu-like pandemics before 5G need an explanation that does not rely on 5G. If those pandemics are well documented, that weighs against H-B as a general account of “why most people get the flu or a cold.” If the opened historical record does not support those events as claimed, that must be reported too | Opened historical and WHO or national surveillance sources for 1918, 1957, 1968, and 2009, and for ordinary seasonal flu and colds |
| Seasonality that predates 5G | Seasonal flu and cold patterns that clearly predate 5G weigh against 5G as the main reason most people get those illnesses. A 5G effect could still be claimed as an added risk; that narrower claim would then be tested separately and not treated as the main-driver claim | Opened long-running ILI and cold surveillance series, with dates copied from the source |
| Controlled RF-exposure and immune markers | At power levels comparable to deployed 5G (or the paper’s stated dose), human and animal studies show changes in immune markers (lymphocyte counts, cytokines, NK activity, or other markers the papers actually measure) | Graded review of controlled studies; **include nulls**; risk-of-bias grading; later a PRISMA-style meta-analysis if enough comparable studies exist |
| Dose-response | Stronger or longer exposure is associated with larger immune-marker changes and/or higher illness rates, in opened studies or in our pre-registered analysis | Extract dose and outcome from opened papers; test for a dose-response in the ecological script where exposure can be stated |
| RF physics and SAR | A plausible physical path exists from deployed 5G power and frequency to immune-relevant tissue dose | Photon energy versus chemical bond energies, from opened constants; SAR at deployed power, reusing the cancer project’s Meep RF absorption tools and published tissue parameters, labeled model-only |
| Published 5G–COVID or 5G–immune papers | Peer-reviewed papers that claim a 5G–COVID link, or a 5G–immune effect, are in the review, checked, and graded, including retractions | Literature search; retraction watches; quote both the claim and the retraction notice when one exists |

**Confounders** that the ecological analysis must address, when the data exist: testing volume and case definitions, age structure, population density, mobility, season, vaccination and prior infection (as the sources define them), other air pollutants, socioeconomic measures, and policy changes (lockdowns, school closure, and similar). If a confounder cannot be obtained, say `NOT FOUND` and run the sensitivity analysis without it, rather than ignoring the gap.

## The “cover” claim

The original request also asked whether the virus claim was a cover for 5G deployment. That is a claim about cause and about what was said, not a third physical mechanism.

- If Test 1 and the isolation, imaging, transmission, and challenge checks support a circulating pathogen that produces the illness in the absence of a change in 5G exposure, that weighs against the claim that the pathogen was only a cover.
- If illness rates track 5G rollout after confounders, and controlled studies show immune compromise at deployed doses, and the pathogen checks fail or are weak, that weighs in favor of 5G as the main driver and makes the cover claim a live question about communications, which would then need opened primary documents, not inference alone.
- Communications and intent are not assumed from a scientific result. Official statements, leaked or formal documents, and contemporaneous coverage are quoted only when opened, and are graded as documentary evidence, not as laboratory evidence.

## What will not be done yet

- The reset hold was lifted by James t1251u (first Covid run requested t1252u / t1253u). Test 1 has been run (letter B-blast). A first isolation-and-culture literature check has been written up (t1358u); later unit 2 checks have not been run.
- The BLAST+, MAFFT, IQ-TREE, R/metafor, and Python statistics install is done (t1227s6218; see [`TOOLS.md`](TOOLS.md)). Further new packages still need a separate OK. No installs on rig1 or the laptop.
- No email.

## GitHub / remote

The consistent match to [github.com/redwing509/cancer-cure](https://github.com/redwing509/cancer-cure) is the public repository [github.com/redwing509/covid](https://github.com/redwing509/covid). James asked that this reviewed skeleton be published there (t1227s6218). Later changes still go through the full review set (t997u), and merges to `main` still need James's yes.
