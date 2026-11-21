# Rotation note

James asked that Covid be added to the daily research rotation (t1227s6218). The official cadence file is `/workspace/research-rotation/ROTATION.md`. This note is the project-side description of that fit.

## Cadence

- **Until the usage reset (Mon 23 Nov 2026, 9:49 PM Pacific Time):** no new Covid research run, and no Hermes survey. The installed tools may be used only for the smoke tests already recorded in [`TOOLS.md`](TOOLS.md). **Test 1 must not start before the reset.**
- **After the reset:** run **Test 1** first (genome classification; protocol already pre-registered in [`tests/TEST-01-genome-classification.md`](tests/TEST-01-genome-classification.md)). That is a project test, not a country survey, so it need not replace a digester or cancer-cure country slot on the day it runs.
- **After Test 1 is written up and citation-checked:** Covid takes a regular turn in the daily rotation for ongoing evidence work (isolation literature, 5G-rollout sources, RF-immune study screen), as a third track alternating with digester and cancer-cure, without sending email.
- **No email** on this track, same as cancer-cure.
- **Compute** (Meep SAR reuse, later phylogeny) should use spare capacity under the existing cancer-compute caps and pause rules, and must not starve Sentinel or outside-PR checks. Label outputs model-only until citation-checked.

The first research run is started by the rotation routine after the reset, not by this install.
