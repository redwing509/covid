# Q-17 erratum: influenza junction 21-mers (no rule change)

**Written:** Sun 22 Nov 2026, after official Method 3 results and the CodeRabbit review.
**Does not edit** `tests/PRE-REGISTERED-AGREEMENT-Q17.md`. Official Method 3 used the procedure as written.

## Issue

The frozen Method 3 rule concatenates influenza segments **with no spacer**, and says a spacer is unnecessary because "those junctions cannot form a k-mer because of the non-ACGT skip rule." That justification is wrong. With no spacer, consecutive ACGT bases at a segment boundary do form up to 20 canonical 21-mers that are not present in any real segment.

CodeRabbit recommended defining each influenza genome's k-mer set as the union of its eight segment-level sets, and recording that as a registration amendment.

## Disposition

The runner still follows the frozen operational text (concatenate, no spacer). This note records the factual error. Changing the k-mer construction after seeing results would be a post-hoc method change, so it is not applied here.

On this official run every query–S_flu Jaccard was already 0 (D_M undefined, placeholder used). Dropping invented junction 21-mers from the influenza sets could not have created a new shared k-mer with the query, so the official Method 3 primary AGREE, nearest SARS-CoV (`NC_004718.3`), and overall PASS would be unchanged under a union-of-segments construction.

A later pre-registered amendment and a Method 3 rerun under that amended rule would need James's OK.
