# Repairing extreme low-bit models: measured starting point and research plan

**Status: research program, not a repaired Bonsai-27B release.** This note distills the 22 September pre-registration, 23 September literature review and the subsequently measured 1.7B run. Dates matter: the design memo initially said nothing had been launched; the later main report includes a real bed experiment. Earlier apparent “trained-arm failures” were from a 256-token-vocabulary CPU simulation, not a shipped Bonsai model, and are excluded from the conclusions here.

## What has actually been measured

The real 1.7B Bonsai-1.7B bed uses Qwen3-1.7B as teacher. A scale-only end-to-end distillation run with 32× more **unique** calibration data changed held-out KL(parent‖student) from **0.608 to 0.465** (paired gain 0.143 [0.133, 0.154]) and next-token top-1 agreement from **71.4% to 75.3%**. A same-scale recoverable-damage positive control passed. These are meaningful recovery signals, consistent with data supply having constrained the earlier short run. They do not prove it was the only constraint.

The behavior gates did **not** recover. Chat's worst KL increased from 2.86 to 3.94, and the count of failing chat probes rose from four to five. Parent-continuation fidelity rose from 0.675 to 0.697, short of its 0.841 bed threshold. A separate sign-level arm improved held-out KL to 0.514 but did not recover a gate; its packed-format export failed. Neither arm is a deployable repair. No 27B Bonsai repair result follows from the bed.

## Why local weight correction is insufficient as a general recipe

Bonsai's trained representation is not simple rounding of the BF16 parent. Our weight and activation observations include changed unquantized parameters, altered scales and residual directions. A low-rank fit to `W_parent − W_bonsai` in the parent's raw coordinate system can therefore spend capacity undoing a learned gauge rather than correcting output errors. The observed 1.7B KL improvement without chat recovery shows why optimizing an average next-token loss alone is not a graduation rule. These are **interpretations** motivating controlled tests, not a settled causal account of Prism's training.

## Two tracks to test

**Track A: parent-preserving repair at a fixed packed format.** First train group scales and normalization parameters end to end with teacher logits on a larger, held-out-separated corpus; then test sign/level updates in the same packing. Include candidate-specific chat and code prompts in validation, while keeping benchmark test items sealed. Compare with ordinary knowledge distillation, shuffled site selection and matched-compute nulls. A full-depth trained run is needed before saying the compressed 27B representation cannot be repaired.

**Track B: deeper low-bit reconstruction.** At two bits and below, allow the student representation to move substantially, with continued QAT/distillation and model-level objectives. [ParetoQ](https://arxiv.org/abs/2502.02631) reports a change in learning behavior between two and three bits on its tested scales. [EfficientQAT](https://arxiv.org/abs/2407.11062) separates blockwise parameter training from end-to-end quantization-parameter training. [LLM-QAT](https://arxiv.org/abs/2305.17888) and [on-policy distillation](https://arxiv.org/abs/2306.13649) supply concrete data/objective alternatives. These papers motivate experiments; their token budgets and quality results are **not** measured compute requirements or guarantees for Bonsai-27B. If a low-bit student substantially re-encodes or changes behavior, it needs its own capability claim rather than an inherited parent-preservation certificate.

## Pre-registered controls for the next run

1. **Frozen inputs and identity:** pin teacher/student hashes, tokenizer, packed format and held-out dataset IDs; prohibit evaluation examples in training. Keep parent and candidate on the same scoring path.
2. **Recoverable-damage positive control:** inject damage at the same model scale that the proposed trainable parameters can actually undo. Confirm the optimizer and export path recover it. This proves machinery, not Bonsai repair.
3. **Matched-compute nulls:** ordinary KD without geometry, a shuffled feature/site allocation, and a random equal-bit precision restoration where bits are added. Use the same data, steps, optimizers and model budget.
4. **Mechanistic readouts:** paired next-token KL and top-1, per-layer SAE survival in the parent's coordinates, and a basis-insensitive output comparison. Do not treat the SAE readout alone as capability.
5. **Capability gates:** score chat, parent-continuation, GSM8K, IFEval, coding and available vision tasks before/after on identical items. Report paired uncertainty, empty/truncated rates, reasoning mode and costs.
6. **Packed export:** reload the selected snapshot from the actual deployment format and repeat logits, gates, memory and decode tests. A training-state result without working packed export is not a releasable model.

Promote from a 1.7B pilot to a 27B experiment only if a held-out gain exceeds the matched controls, deep-layer error moves rather than merely local training loss, the positive control works, and the exported candidate does not lose a previously passing endpoint. For a parent-preserving certificate, apply GeoRefine's stated all-layer feature and paired capability rules unchanged. A failed arm remains an informative result with its original thresholds.

## Open questions

- Does a sufficiently long **full-depth** run repair deep-layer drift that the short scale-only experiment could not?
- How much of Bonsai-2's lower parent-coordinate SAE survival is re-encoding versus a loss visible in outputs or task behavior?
- Which target-data mixture improves the chat and knowledge-continuation probes without sacrificing the strong efficiency point?
- Can an improved student retain the same 1-bit/ternary packing and real kernel speed after export?

The primary study's [report](REPORT.md) provides the measured starting point. This research agenda should not be read as a critique of an experiment Prism ML did not claim to run.
