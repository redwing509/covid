# Method

This is the working method for the Covid evidence review. The [disclaimer in the README](README.md) applies to every page: this is not medical advice, and no page is a conclusion until the cited evidence has been opened and checked.

Follow the same citation-honesty rules used on the cancer-cure project and the other research projects on this account (James, 15 Nov 2026, t1084u).

## Open questions stay open

Until a test in [`PLAN.md`](PLAN.md) has been run (or its published sources opened), the citation check is done, and the result is written from the opened record, do not state that result in our own voice as fact. In particular, **Test 1** — whether the public sequences labeled as the COVID-19 reference pathogen group with influenza references, with other-coronavirus references, with neither, or are inconclusive — is open. Do not assume either answer in notes, code comments, or figure captions. The words “influenza variant” are used only if the protocol’s A-nested test holds.

Database labels (for example a record titled SARS-CoV-2) are labels to be checked, not a classification finding.

## Evidence scale

Each study or analysis gets **one** evidence level from the table in [`README.md`](README.md), taken from the design in the opened source, not from how impressive the result sounds. If the design is unclear, say so and use the lower of the plausible levels.

Use the **highest design the opened source actually is**, not the highest design it cites. A systematic review is labeled systematic review; the individual trials it includes, if entered separately, keep their own levels. Animal work inside a paper that also has a human arm should be split or clearly labeled. A calculation or model run is labeled physics / calculation or genomic / sequence, and is not a human clinical result.

## Citation honesty

1. **Quote plus locator.** Every factual claim that comes from a published or database source includes a direct quote of the supporting sentence and that source’s URL or DOI. Drop any such claim that lacks both. Numbers we compute ourselves are an exception: they must come from a stated command and pinned tool version, run on pinned inputs (accessions, dates of download, and file hashes when a file is saved), and must be reported with that command, version, seed, thread count, and host, not as if they were quoted from a paper. See “Work we run ourselves” below.
2. **`NOT FOUND`, never a guess.** When a search finds nothing, write `NOT FOUND` and say what was searched. Never fill gaps from memory.
3. **Copy, don’t recall.** Do not write numbers, sequence accessions, institution names, author names, dates, or product or formula names unless they are copied from a source opened for that check. Numbers we compute ourselves are the same exception as in rule 1: they must come from a stated command and pinned tool version, run on pinned inputs, and must be reported with that command, version, seed, thread count, and host, not as if they were copied from a paper.
4. **Two passes on a fresh search.** Pass 1 is only a **SOURCES OPENED** list (URL or DOI, title, one quote, and `full text` / `abstract only` / `not opened`). Pass 2 writes findings only from that list.
5. **Say how the source was opened.** Never describe, quote, or give numbers from content that was not opened. If only the abstract was opened, quote the abstract and mark the rest unseen.
6. **Paywalls.** Look for a legitimate alternate copy (author preprint, thesis, university repository, conference slides, or a later open paper that quotes the numbers). Do **not** use Sci-Hub, Library Genesis, or similar sites. If only a paywalled record exists, cite the bibliographic data, label it `not opened` or `abstract only`, and mark unseen numbers as “paywalled; no legitimate open copy found”.
7. **No raw paywalled PDFs** in this repository. The notes are summaries, short quotes, numbers, and links only.
8. **Nulls, harms, and retractions** are recorded, not omitted. A retraction is quoted from the retraction notice when that notice can be opened. The original paper is not treated as standing evidence after a retraction, except as the object of the retraction record.

## What a findings entry must contain

When a later pull request adds findings, each entry should include:

1. **Claim or test** — which hypothesis or test the entry bears on (Test 1, H-A, H-B, or a named sub-claim)
2. **What was measured** — as the opened source or the pre-registered protocol names it
3. **Population, system, or dataset** — who or what was studied, copied from the source or from the pinned accessions
4. **Measured result (quoted or computed)** — a quote from an opened source, or a number produced by a stated script from pinned inputs, with the command and version recorded
5. **Link, DOI, or accession** — a locator a reader can open without a piracy site
6. **Evidence level** — one value from the scale
7. **Negative / null results** — what did not support the claim, was not significant, was harmful, or was retracted; write `not reported in the opened source` if the source is silent
8. **Confounders and limits** — as the source states them, plus any that the protocol said would be checked

## Work we run ourselves

For tools listed in [`TOOLS.md`](TOOLS.md):

- Write the protocol and the decision rule **before** the run (see [`tests/TEST-01-genome-classification.md`](tests/TEST-01-genome-classification.md) for Test 1).
- Pin tool names, versions, inputs (accessions, dates of download, hashes when a file is saved), and, for any computed result, the command, seed, thread count, and host.
- Label output as our analysis, not as a published paper, until it is written up and reviewed.
- Installing a third-party program, downloading a new package, or accepting a license needs a separate OK from James, unless he has already given one for that install.
- Code that will be pushed must pass the full review set (Claude, the controller, PR-Agent, CodeRabbit CLI, gitleaks, trufflehog, a board note, rb.py, a push-hold bundle, MANIFEST) before it is pushed. Merges need James's yes (t997u).

## What this method is not

It is not a clinical protocol, a treatment guide, or a public-health order. It is not permission to send email about this project. It is not a conclusion.
