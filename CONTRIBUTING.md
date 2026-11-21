# Contributing

This repository is **not medical advice**. Do not submit treatment recommendations.

Contributions that help are: additional published sources, corrections to quotes or numbers, better open links, missing negative or null results, retraction notices, tool implementations that match [`TOOLS.md`](TOOLS.md), and improvements to the method or to a pre-registered protocol. Do not change a decision rule after the corresponding test has been run unless the change is a documented bug-fix and the test is re-run.

## How to submit

Open an issue or a pull request targeting `main` on [redwing509/covid](https://github.com/redwing509/covid). Include a clear description and the opened source (URL, DOI, or accession) for every factual claim. Quote the supporting sentence.

Do not submit:

- secrets or personal information
- copyrighted PDFs or other full-text publisher files
- material from Sci-Hub, Library Genesis, or similar sites
- unsourced anecdotes presented as evidence
- invented or reconstructed citations, DOIs, accessions, or numbers
- a request to install software as if a tools row were already permission to install

## Review

Every change starts as **unvalidated**. Merges to `main` need James's yes. Code and notes that are pushed must first pass the full review set used on this account (t997u): Claude, the controller, PR-Agent, CodeRabbit CLI, gitleaks, trufflehog, a board note, rb.py, a push-hold bundle, and MANIFEST.

There is **no email** on this project.

Follow [`METHOD.md`](METHOD.md) and [`PLAN.md`](PLAN.md). Keep the README disclaimer intact. On contested claims, submit supporting and opposing sources; do not omit inconvenient results. Do not state Test 1’s classification as settled in either direction until that test has been run and citation-checked.
