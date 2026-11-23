# Q-17 pre-registered agreement rule (Test 1 second and third methods)

**Written:** Sun 22 Nov 2026, 4:46 PM PST (America/Los_Angeles, UTC-8), after
the pinned Test 1 FASTA and BLAST tables were hashed, and **before any new
MAFFT alignment, IQ-TREE run, or k-mer distance calculation for Q-17 was
started.**

This file freezes the verification rule. It must not be edited to fit later
numbers. James authorized this build on 22 Nov 2026 (widget t1270s6510).

## What this is, and what it is not

Test 1 already has a pre-registered letter **B-blast** (21 Nov 2026, ~11:27 PM
PST): each query has a qualifying BLAST hit in S_cov and no qualifying hit
in S_flu. The Test 1 protocol’s one-sided rule therefore **did not build** a
combined tree, and it forbids treating this verification as a change of that
letter.

Q-17 is a **verification** study on the same pinned inputs. It adds a second
method (MAFFT 7.526 + IQ-TREE 3.1.4 ML tree with UFBoot and SH-aLRT) and a
third method (alignment-free k-mer / Mash-class distance, and a distance
phylogeny). **Neither method may change the pre-registered Test 1 letter.
The letter remains B-blast regardless of these results.**

This work is model-only sequence comparison. It is not a statement about
patient illness, isolation, transmission, or 5G.

## Pinned inputs (must be verified at run time)

- Combined FASTA: `/workspace/covid/data/raw/test-01/fasta/all-selected.fasta`
  SHA-256 `787a51c247a3fa2195f75989a28783e6edbe3ff38c76117115a87349ababa0b3`
  (64 records, official E-utilities download recorded in
  `results/test-01/FASTA-HASHES.md`).
- Membership is the Test 1 selection already recorded in
  `results/test-01/selection.json`:
  - Q: `NC_045512.2`
  - S_cov: `NC_002645.1`, `NC_005831.2`, `NC_006213.1`, `NC_006577.2`,
    `NC_004718.3`, `NC_019843.3`
  - S_flu: the seven influenza genomes (six influenza A isolates and
    B/Lee/1940), each eight RefSeq segments as listed in `selection.json`
    (the skipped same-subtype genome is not in the combined FASTA)
  - Outgroup: `NC_140766.1`
- Committed Test 1 BLAST tables under `results/test-01/blast/` (used only
  for the protocol-trim tree attempt). The Q-17 run must not rerun BLAST
  to choose a letter.
- Tools (already installed, no new packages): MAFFT 7.526, IQ-TREE 3.1.4,
  Python standard library plus the existing `/opt/covid-tools` venv
  (Biopython 1.88, numpy). Mash / sourmash are **not** installed and will
  not be installed for this run.

If the combined FASTA hash differs, the run must stop and not score.

## Method 2 — MAFFT + IQ-TREE (verification tree)

Pinned commands, unchanged from Test 1:

```bash
mafft --auto --maxiterate 1000 --thread 1 in.fa > aln.fa
```

Column filter: drop every alignment column whose gap fraction is greater
than 0.50. Then apply the pinned mean-pairwise-identity script from
`tests/TEST-01-genome-classification.md`. If fewer than 200 columns remain,
or mean pairwise identity is below 30%, the alignment is not informative.

```bash
iqtree -s aln.filtered.fa -m MFP --ufboot 1000 --alrt 1000 --seed 12345 -T 1 -o OUTGROUP_ACCESSION -pre PREFIX
```

Segmented influenza genomes are written as one sequence by concatenating
segments in increasing segment number, with a spacer of ten `N` characters
between segments, as in Test 1 step 8. FASTA headers are `accession.version`;
for a concatenated genome the header is the first segment’s accession.version.
The IQ-TREE `-o` string for the outgroup is `NC_140766.1`.

Two tree attempts are pre-registered, in this order. The second is used only
if the first cannot produce a scored tree.

### T-protocol

Apply the Test 1 step 8 site-homology trim to Q, S_flu, S_cov, and the
outgroup, using the committed step 4 BLAST tables (evalue ≤ 1e-5 HSPs
between each genome and any Q record). If any required genome has zero kept
bases, **do not** run MAFFT or IQ-TREE on this attempt; record
INCONCLUSIVE (C-homology). Because Test 1 found no qualifying S_flu hit,
this outcome is expected and is not a reason to change B-blast.

If the trim succeeds, run the pinned MAFFT command, the column filter, and
the 200-column / 30% identity gate. If the gate fails, INCONCLUSIVE
(C-alignment). If it passes, run the pinned IQ-TREE command.

### T-full

If and only if T-protocol does not produce an IQ-TREE report, build a
second alignment of the **full** concatenated genomes in the pinned FASTA
(no site-homology trim). Same MAFFT, column filter, identity gate, and
IQ-TREE pins. If the gate fails, INCONCLUSIVE (C-alignment). This tree is
verification only. It is not an input to the Test 1 letter.

### Tree agreement rule (applied only to a produced, outgroup-rooted tree)

Let UFBoot and SH-aLRT be the support values, as percentages, on the
critical branch. Both must meet **UFBoot ≥ 95** and **SH-aLRT ≥ 80**, the
same thresholds as Test 1.

- **AGREE** with B-blast if, in the rooted tree, Q forms a monophyletic
  group with S_cov to the exclusion of S_flu, with both supports at or
  above threshold on the branch that separates `{Q + S_cov}` from S_flu,
  and the outgroup lies outside that group.
- **DISAGREE** if the supported rooted topology places Q with S_flu to the
  exclusion of S_cov, or places Q outside both `{Q + S_cov}` and
  `{Q + S_flu}`.
- **INCONCLUSIVE** if no tree could be built, the alignment gate failed,
  the outgroup does not form a single split from the other taxa so
  monophyly cannot be assessed, or the topology is as in AGREE or DISAGREE
  but support is below threshold.

If T-protocol produces a scored tree, that tree is the Method 2 result.
Otherwise Method 2 uses T-full, or INCONCLUSIVE if neither tree can be
scored.

## Method 3 — alignment-free k-mer distance (Mash-class) and NJ phylogeny

No new packages. Exact k-mer sets are used (equivalent to a complete Mash
sketch of every k-mer; Mash itself is not installed).

- Alphabet: uppercase A, C, G, T only. Other characters (including `N`
  and the ten-`N` spacers used only in Method 2) are not part of any k-mer:
  a window is skipped if it contains a non-ACGT base. Canonical k-mers:
  each window contributes `min(kmer, reverse_complement(kmer))`.
- k = 21 (the Mash default for genomes).
- For each influenza genome, concatenate its eight segments in increasing
  segment number **with no spacer** (a spacer would invent non-genomic
  junctions; those junctions cannot form a k-mer because of the non-ACGT
  skip rule anyway, but no spacer is inserted).
- Jaccard similarity J = |A ∩ B| / |A ∪ B| on the canonical 21-mer sets.
  If either set is empty, that pairwise comparison is undefined and Method
  3 is INCONCLUSIVE.
- Report both:
  - Jaccard distance D_J = 1 − J
  - Mash-like distance D_M = −(1/k) ln(2J / (1+J)) when J > 0; if J = 0,
    D_M is recorded as undefined and is treated as larger than any finite
    distance for nearest-neighbor purposes.
- The **primary** Method 3 distances are the D_M values; D_J is reported
  and is used only if D_M is undefined for a pair that still has J = 0.

### k-mer agreement rule (primary)

For the single query Q = NC_045512.2:

- Let d_cov be the mean finite D_M to the six S_cov genomes, and d_flu
  the mean finite D_M to the seven S_flu genomes. Pairs with undefined D_M
  and J = 0 are assigned a distance larger than any finite D_M for this
  mean (they count as far).
- Let the nearest reference genome be the one with the smallest finite D_M
  (or D_J if all nearest D_M are undefined). A tie for nearest, including a
  tie between an S_cov genome and an S_flu or outgroup genome, is
  INCONCLUSIVE for Method 3.

**AGREE** if and only if all of the following hold:

1. The nearest reference genome is in S_cov, not in S_flu and not the
   outgroup.
2. d_cov < d_flu (strict).

**DISAGREE** if the nearest reference is in S_flu, or d_flu < d_cov.
**INCONCLUSIVE** if the nearest is the outgroup, there is a tie, or a set
is empty.

### Distance phylogeny (secondary, reported with Method 3)

Build a neighbor-joining tree from the pairwise D_M matrix on the 15
genome-level sequences (Q, 6 S_cov, 7 S_flu, 1 outgroup). For a pair with
undefined D_M (J = 0), use D_J = 1. Root by placing the outgroup
`NC_140766.1` as the outgroup (the NJ tree is rooted by placing the split
to the outgroup). No bootstrap is computed for this distance tree; that
limitation is stated in advance.

- Topology **supports AGREE** if Q groups with S_cov to the exclusion of
  S_flu in this rooted NJ tree (the outgroup lies outside `{Q + S_cov}`).
- Topology **supports DISAGREE** if Q groups with S_flu to the exclusion
  of S_cov, or with neither.
- This topology **does not override** the primary nearest-neighbor / mean
  distance rule. It is reported. If topology and the primary rule conflict,
  Method 3 is recorded as **INCONCLUSIVE (conflict)** rather than forced to
  either side.

## Overall Q-17 verification verdict

The Test 1 letter stays **B-blast** in every case.

- Verification **PASS** if Method 2 is AGREE or INCONCLUSIVE, and Method 3
  is AGREE or INCONCLUSIVE (including Method 3 conflict).
- Verification **FAIL** if Method 2 is DISAGREE or Method 3 is DISAGREE.
  A FAIL means a second or third method supported an influenza grouping, or
  a “groups with neither” placement, at the pre-registered thresholds. It
  still does not change the Test 1 letter.

Host: box only, nice 19. No mail cancer-queue or Fan runner is used.
