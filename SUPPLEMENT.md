# Technical tables and result boundaries

This supplement preserves the principal measurement tables from the four source documents in a public-facing form. Values are rounded for display; [machine-readable results](data/results.json) and [paired outcomes](data/paired_outcomes.csv) retain greater precision. **July and September have different parents.** All differences are candidate minus its own parent.

## A. July 27B generation

The July models were measured against Qwen3.6-27B. Their MLX file sizes were 5,129,115,752 bytes (1-bit) and 8,490,785,104 bytes (ternary). The parent was BF16. The behavior battery used 13 chat probes, eight parent-continuation probes and eight comprehensibility probes.

| Teacher-relative gate | Parent vs itself | July ternary | July 1-bit |
|---|---:|---:|---:|
| Chat, worst KL (≤1.0 nat) | 0.00, pass | 2.48, fail on 5/13 | 5.94, fail on 3/13 |
| Parent-continuation fidelity (≥0.85) | 0.919, pass | 0.833, fail | 0.818, fail |
| Comprehensibility (≥0.72; at most 25% failed) | 0.941, pass | 0.808, pass | 0.832, pass |

The composite “coherence” label in the original instrument is a logical conjunction of these **small tests**, not an ordinary-language judgment of conversation quality. Its failure should not be paraphrased as “the model cannot reason or chat.” The parent-vs-parent continuation score is below 1.0 because the two-card run was not perfectly deterministic.

| July held-out census, 64×2,048 tokens | Ternary | 1-bit |
|---|---:|---:|
| Next-token KL(parent‖candidate), nats [95% CI] | 0.480 [0.435, 0.527] | 0.735 [0.686, 0.790] |
| Parent top-1 agreement [95% CI] | 74.0% [72.6, 75.5] | 67.5% [66.1, 68.9] |
| Live-feature recall, mean over 63 layers | 0.522 | 0.459 |
| Rare-feature recall, mean over 63 layers | 0.471 | 0.413 |
| Rare parent features below descriptive recall threshold | 49.7% | 56.8% |

The descriptive feature table uses the Qwen3.6 parent's feature basis. It is **not** the later Qwen3.8 rare-survival certificate. On 5,700 MMLU questions, the Qwen3.6 parent scored 85.2%, July ternary 77.7% (unpaired difference −7.5 points [−8.9, −6.1]) and July 1-bit 68.1% (−17.1 [−18.6, −15.6]). A separate same-runtime, reasoning-off July head-to-head measured ternary GSM8K strict −2.8 [−3.9, −1.7] and IFEval strict −8.1 [−11.6, −4.6] points; 1-bit −3.9 [−5.2, −2.7] and −10.9 [−14.4, −7.4]. This edition did not complete a July vision battery or the later full SAE/attribution certificate.

## B. Bonsai-2 storage and speed

The September release derives from Qwen3.8-27B. Language GGUF variants contain the same 851 logical tensors, and the vision projector is a separate 931,145,856-byte file. The MLX pack includes vision. Whole-file rates therefore do not have a common numerator across GGUF and MLX.

| Language GGUF | Bytes | Ratio versus Prism F16 GGUF | File-wide bits per logical parameter |
|---|---:|---:|---:|
| Prism F16 GGUF | 53,808,408,928 | 1.00× | 16.005 |
| Bonsai-2 PQ2_0 | 7,206,168,928 | 7.47× smaller | 2.143 |
| Bonsai-2 PTQ1_0 | 5,946,648,928 | 9.05× smaller | 1.769 |

The same-build `llama-bench` measurements used one RTX PRO 6000 Blackwell, CUDA, BF16 K/V cache, batch size 1 and the same parent/candidate settings. Parent speed below used a 54,657,734,080-byte BF16 GGUF of Qwen3.8-27B, distinct from Prism's F16 file in the storage table.

| Probe | Parent BF16 | Bonsai-2 PQ2_0 | Bonsai-2 PTQ1_0 |
|---|---:|---:|---:|
| Decode, tg128 | 27.74 tok/s | 126.54 tok/s | 121.8 tok/s |
| Prefill, pp512 | 3,854 tok/s | 4,014 tok/s | 3,981 tok/s |
| Prefill, pp4096 | 3,841 tok/s | 4,055 tok/s | 3,988 tok/s |
| VRAM at 32k context | 51,900 MiB | 9,578 MiB | not measured |
| VRAM at 131k context | 58,140 MiB | 15,818 MiB | not measured |

The `tg128` numbers are short benchmark repetitions, **not** production fleet averages. Prefill did not scale with the file-size ratio. PTQ1_0 and PQ2_0 produced the same tested outputs; their speed differs because their packing differs. The only justified speedup in the main report is 126.54/27.74 ≈4.56× under this setup.

## C. Bonsai-2 capability by task and mode

All task differences below use the candidate's Qwen3.8 parent. The reasoning-off GSM8K/IFEval run used the same Prism runtime for every arm; all main-task answers were nonempty. Its two-point non-inferiority criterion was specified before scoring.

| Reasoning off | Parent | Bonsai-2 | Difference, pp [95% CI] |
|---|---:|---:|---:|
| GSM8K strict, n=1,319 | 97.3% | 95.3% | −2.0 [−3.0, −1.1] |
| GSM8K flexible, n=1,319 | 97.3% | 95.2% | −2.1 [−3.0, −1.2] |
| IFEval strict, n=541 | 82.3% | 78.9% | −3.3 [−6.7, 0.0] |
| MMLU, n=5,700 | 84.5% | 79.1% | −5.33 [−6.18, −4.49] |
| HumanEval+, n=164 | 90.2% | 86.0% | −4.3 [−9.2, +0.6] |
| MBPP+, n=378 | 77.0% | 74.1% | −2.9 [−5.6, −0.3] |
| MMMU validation pilot, n=128 | 55.5% | 46.9% | −8.6 [−17.2, 0.0] |

The MMLU result uses a BF16 materialization of Bonsai-2; its parity check with PQ2_0 is reported in section D. HumanEval+/MBPP+ cross-arm coding comparisons have a different parent/reference runtime, and MMMU is a pilot whose CI reaches zero. None of those qualifications should be dropped in a public excerpt.

| Thinking enabled at tested Prism settings | Parent | Bonsai-2 | Difference, pp [95% CI] | Empty/truncated counts, parent / candidate |
|---|---:|---:|---:|---:|
| GSM8K flexible, n=300 | 96.0% | 95.7% | −0.3 [−2.0, +1.3] | 0 / 0 |
| IFEval strict, n=541 | 93.7% | 93.7% | 0.0 [−1.8, +1.8] | 2 / 3 |
| HumanEval+, n=164 | 92.7% | 94.5% | +1.8 [0.0, +4.3] | 1 / 2 |
| MBPP+, n=378 | 81.2% | 79.1% | −2.1 [−5.3, +1.1] | 5 / 4 |

The thinking-enabled run's pre-registered empty/truncated ceiling was 2% per arm/task; every cell passed. Final-answer scoring excluded reasoning traces. The mean total completion tokens per item were parent/Bonsai-2: GSM8K **398/439**, IFEval **2,045/2,173**, HumanEval+ **2,130/2,566**, MBPP+ **2,271/2,568**. Thus a speed/cost comparison needs actual generated tokens, not only output accuracy or model-file size. No task difference in this table has a CI excluding zero; the CIs also do **not** establish equivalence. Thinking-on MMLU and vision were unmeasured.

## D. Internal probes and their interpretation

| Probe | Bonsai-2 | Control / threshold | Scope |
|---|---:|---:|---|
| BF16 proxy vs PQ2_0 runtime, 25,550 positions | KL 0.000351; 98.87% top-1 | parent HF vs parent GGUF KL 0.00165 | Supports proxy use on tested text, not bitwise whole-model parity |
| Candidate vs parent next-token census, 131,072 positions | KL 0.354 [0.336, 0.373]; 74.5% top-1 | parent self-comparison KL 0 | Held-out text, parent vocabulary |
| Rare SAE feature survival, worst of L1–63 | 0.8022 at L46 | Q8_0 0.9820; GeoRefine criterion ≥0.975 | Parent-coordinate readout; [all 63 values](data/sae_layers.csv) |
| Descriptive rare-feature loss | 33.9% | July ternary 49.7% with different parent | Separate descriptive threshold, not the certificate statistic |
| Chat-start probe | one of 15 outside budget; max KL 1.16 | budget KL ≤1.0 | Small prompt set; one structured-text failure |
| Parent-continuation fidelity | 0.785 | criterion ≥0.85 | Not a factual quiz |
| Comprehensibility probe | 0.830, pass | criterion ≥0.72 | Eight prompts, one scored zero |

The parent-coordinate SAE readout reports 63/63 Bonsai-2 layers below the 0.975 criterion, while Q8_0 has 0/63 below it in the same run. A Hadamard-rotated or otherwise re-encoded representation can lose alignment to the parent's dictionary without losing every encoded function. That is why the output-distribution and task results are reported alongside the feature probe.

## E. 1.7B repair bed, not a 27B result

The later real scale-only run on Bonsai-1.7B moved held-out KL **0.6081→0.4648** and top-1 **0.7137→0.7527**, while its recoverable-damage positive control passed. The chat and parent-continuation gates still failed. A separate sign-training arm improved average KL but failed its packed export. Neither is a deployable repaired model. Earlier simulation receipts from a toy 256-token vocabulary are deliberately excluded. The training hypothesis and next controls are in [Repair research](REPAIR_RESEARCH.md).
