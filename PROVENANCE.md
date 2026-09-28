# Provenance and release boundary

## What is included

- [`data/results.json`](data/results.json): pinned model/runtime identifiers, artifact SHA-256 values, aggregate measurements and SHA-256 values of the internal source receipts used to assemble them. Receipt identifiers contain no machine-local paths or credentials.
- [`data/paired_outcomes.csv`](data/paired_outcomes.csv): **5,403 response-free rows** of paired correctness bits. It covers reasoning-off GSM8K strict/flexible and IFEval strict, plus thinking-enabled GSM8K strict/flexible, IFEval strict/loose, HumanEval+ and MBPP+. Item identifiers are SHA-256 digests of source document hashes or task IDs; prompt text, generated text, code and reasoning traces are omitted. `analysis_order` preserves the ordering needed to reproduce the study's seeded bootstrap exactly. Run [`scripts/recompute_ci.py`](scripts/recompute_ci.py) to calculate the nine paired intervals from this file with Python's standard library.
- [`data/sae_layers.csv`](data/sae_layers.csv): the 63 deciding-layer rare-feature survival values and standard errors for Bonsai-2 and the same-run Q8_0 control. This allows independent recomputation of the reported minima against GeoRefine's 0.975 threshold. It is a parent-coordinate readout, not a universal behavior verdict.

The compact public data were derived from the 25 September frozen samples and receipts. The original source summary digests are listed in `source_receipt_sha256` inside `data/results.json`; the two public CSV digests appear there as well. The raw analysis was not rerun on GPUs for this publication package.

## Primary source bindings

| Result family | Internal source receipt ID | Public extraction |
|---|---|---|
| Bonsai-2 artifact sizes and hashes | `assets_manifest` | `results.json → artifacts` |
| Controlled RTX PRO decode and prefill | `speed_parent`, `speed_bonsai2` | `results.json → efficiency` |
| Reasoning-off paired GSM8K/IFEval | `reasoning_off_ci` and the same run's per-item samples | `results.json → reasoning_off`; `paired_outcomes.csv` |
| Thinking-enabled paired tasks, validity | `thinking_on_analysis` and the same run's per-item samples | `results.json → thinking_on`; `paired_outcomes.csv` |
| MMLU and MMMU pilot | `mmlu_pair`, `mmmu_pair` | `results.json → mmlu`, `mmmu_pilot` |
| BF16 proxy versus Prism runtime | `proxy_parity` | `results.json → proxy_parity` |
| Output-distribution census | `census` | `results.json → parent_relative_census` |
| Rare-feature readout and Q8 control | `sae_ladder` | `results.json → sae`; `sae_layers.csv` |
| Small teacher-relative gates | `behavior_gates` | `results.json → behavior_gates` |
| Separate 1.7B repair bed | `bed_before`, `bed_after_scale_training`, `bed_positive_control`, `bed_after_behavior` | `results.json → bed_1p7b_repair` |

The study's source reports were in the internal Selene workspace. Their frozen SHA-256 values are:

| Source document | SHA-256 |
|---|---|
| `BONSAI_ANALYSIS_REPORT_20260925.md` | `86d5db0941a4a1d17d14897a622af35784ebb0330848f368e52198bd97788fe0` |
| `BONSAI_REPAIR_RESEARCH_20260923.md` | `19c6e08f33dfbbfe068d3caeb3d1ffbf9bee681a0381e36942bc1ce4cec88139` |
| `BONSAI_ANALYSE_REPAIR_20260922.md` | `00fa81c05925c419eae8c04030e10f87b6a81676093b46c10fd10a7a39bd5075` |
| `bonsai_report_20260925/nothink2_ci.json` | `d77835cc6699497727743e242ca489ae0f6b4843a605c8a541301163ed8287ac` |
| `bonsai_report_20260925/thinkon/thinkon_analysis.json` | `5c86435b800fcc9d91f5dbe52620654f0eac07e99443a454fb3a27c299522c06` |

The report here is a publication rewrite: it is **not** a verbatim release of operational logs, private storage addresses or generated traces.

## What a complete independent rerun still requires

The public CSV reproduces the headline paired point estimates and intervals; it does not by itself verify that each correctness bit was scored from the claimed model output. A full rerun requires the pinned public weights, a compatible Prism runtime, exact benchmark dataset versions and prompts, scoring scripts, the full request settings, and preferably independently downloadable redacted sample receipts. The raw internal records include full reasoning and code generations and operational paths; they need a separate review before redistribution. The report states this limitation wherever it discusses reproducibility. No unpublished or third-party model weights are included here.

## Prepublication checklist

1. Recompute the nine paired intervals from `paired_outcomes.csv` and compare them with `results.json`.
2. Verify all 63 SAE rows and the two deciding minima against the recorded ladder receipt.
3. Confirm the pinned public model revisions and Prism runtime availability; mark any newer release outside the dated study.
4. Independently review the public package for machine paths, hostnames, credentials, private prompts, generated traces and unlicensed third-party assets.
5. Keep a public, versioned correction route for any reader; do not imply Prism ML's endorsement.
6. Freeze a public release tag with the source document, outcome-table and figure hashes after the final editorial pass.
