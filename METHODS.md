# Methods and statistical reading guide

This supplement describes the **25 September 2026 snapshot**. It separates artifact identity, task scoring, internal probes and repair studies. The source run plan and amendments were written before the final reported scores; [Provenance](PROVENANCE.md) binds them to receipts. A public raw-data release remains to be completed.

## 1. Artifacts and runtime

The July study used the Qwen3.6-27B parent (`6a9e13bd6fc8f0983b9b99948120bc37f49c13e9`), Prism's July 1-bit MLX pack (`ef22f239c670`) and July ternary MLX pack (`70f75f3ad081`). The September study used Qwen3.8-27B (`1d4bf0f2ff6012fd82039f2fa52739d0dd7c60c0`) and Prism's Bonsai-2 GGUF (`6ed5e12b` for its main repo). We verified the downloaded Bonsai-2 assets against their recorded SHA-256 values. The language GGUF and separate vision projector must be counted separately.

The September controlled task and speed runs used Prism's `llama.cpp` fork commit `0324c66521960d67aa7da8687fb1453a79a6565c`. Both parent and Bonsai-2 ran in that build for the primary GSM8K, IFEval and `llama-bench` comparisons. Stock llama.cpp must not be substituted for Bonsai-2 without its required activation transform. The reasoning-off EvalPlus coding parent/reference runs used stock commit `f46bc30c`, so their cross-model deltas have a runtime confound. The internal census and SAE readout used a BF16 materialization of Prism's MLX pack, with a separate runtime parity check (25,550 positions, KL 0.000351, top-1 98.87%). This is close numerical agreement, not exact identity.

## 2. Task protocols

### Reasoning off

All arms used `/v1/chat/completions`, the model's chat template and a preflight probe that rejected any nonempty `reasoning_content`. GSM8K scored all 1,319 questions under strict `#### N` extraction and a flexible final-number extractor. IFEval scored all 541 prompts at prompt level, strict and loose. The scorer checked per-arm empty responses (zero in the valid run), document identity and paired prompt hashes. The main table reports strict GSM8K and strict IFEval; both GSM8K extraction results are available because answer formatting is a material issue.

MMLU used `lm_eval` 0.4.13 through the HF backend with 100 questions per subject (5,700 total). EvalPlus used version 0.3.1, HumanEval+ 164 and MBPP+ 378 problems, greedy generation with thinking disabled and a 768-token cap. The MMMU vision result is a first-128 validation pilot with `lmms-eval` at commit `14b9c079`, temperature zero and 256 new tokens. It is not a full vision suite.

### Thinking enabled

The primary thinking-enabled run used the September parent and Bonsai-2 PQ2_0 on separate RTX PRO 6000 Blackwell GPUs under the same Prism runtime. Requests explicitly set `enable_thinking=true` and `reasoning_effort=xhigh`. Sampling used temperature 1.0, top-p 0.95, top-k 20 and min-p 0.05, seed `20260925`, with a 32,768-token shared thinking-plus-answer budget. A logging proxy recorded the effective settings, finish reason, token counts and reasoning/final separation. Only the final answer was scored. GSM8K's harness stop string was applied to the final answer, not to the reasoning trace.

The primary subset was seeded GSM8K **300**; IFEval used **541**, HumanEval+ **164**, MBPP+ **378**. The pre-registered validity rule rejected an arm/task if more than **2%** of answers were empty or hit the generation limit. Every reported arm/task passed (maximum 1.3%). The initial run plan allowed larger GSM8K and thinking-mode MMLU extensions. Before accuracy was read, the team dropped those extensions under its stated time rule. Accordingly, there is **no** thinking-mode MMLU result in this report.

One important scorer distinction: with thinking enabled, the strict GSM8K `#### N` format made Bonsai-2 appear +7.3 points ahead. Inspection found that the parent more often gave the correct number without that exact marker. Flexible final-number extraction, closer to the intended math question, gave −0.3 points [−2.0, +1.3] and is the headline thinking-mode GSM8K result. The strict-format result remains a format-adherence observation, not a reasoning-capability result.

## 3. Pairing, uncertainty and decision rules

Per-item differences were paired by document/prompt, with 10,000 percentile-bootstrap resamples. The reasoning-off GSM8K/IFEval analysis used seed `20260923`; the thinking-mode analysis and coding used their recorded seeds. Differences are in **percentage points** (candidate minus parent). A CI containing zero means the sign is unresolved at this sampling resolution. It does **not** prove equivalence.

GeoRefine's registered non-inferiority criterion for a candidate requires the lower paired 95% CI bound to be strictly greater than −2.0 points on **both** GSM8K strict and IFEval prompt-strict, alongside separate feature and long-context gates for a full internal certificate. This paper applies that decision rule descriptively. It is a GeoRefine threshold, not an industry standard or Prism's own release criterion. Exact equality to the boundary does not pass. The thinking-on comparison is not a full certificate: the GSM8K lower bound is −2.0, MBPP+ is −5.3, and thinking-on MMLU/vision were not run.

The July MMLU interval was computed unpaired; the September MMLU interval is paired per item. Directly comparing their interval widths or treating them as a controlled generation improvement would be misleading. The MMMU interval reaches zero and has only 128 questions. The 12/12 needle probes reached about 97k tokens and test single-fact retrieval, not broad long-context reasoning.

## 4. Internal-fidelity probes

The next-token census evaluated 64 held-out sequences of 2,048 tokens: 32 from WikiText-2 `test`, 32 from UltraChat `test_sft`, using the relevant parent's tokenizer. It reports KL(parent‖candidate), top-1 agreement, top-5 overlap and residual-stream similarity. Confidence intervals bootstrap over the 64 sequences. Those text splits are disjoint from the calibration splits reported for these runs; no blanket training-data decontamination claim is made for Prism's original model.

The SAE readout uses dictionaries and a probe corpus fixed for the parent, and scores rare-feature survival across layers 1–63. The registered criterion is ≥0.975 at **every** layer; layer 64 is telemetry. Its same-run identity anchor is 1.0 and stock Q8_0 is a control. The descriptive `bonsai_study.py` census's “fraction of rare features lost” uses a different rule from the registered minimum survival. Neither number is a task accuracy score. In a trained or Hadamard-rotated model, parent-coordinate feature loss can reflect representational re-encoding. We read it together with output-distribution and task evidence.

The small teacher-relative behavior battery checks 15 chat-start probes (July used 13), eight parent-continuation probes and eight comprehensibility probes. The chat budget is per-probe KL ≤1.0 nat, L1 ≤1.0 and the parent's top token in the candidate's top five. The continuation score must reach 0.85. Comprehensibility must average ≥0.72 with no more than 25% failing. The so-called “coherence” gate is only the logical conjunction of these three checks. The continuation score is *not* a factual-knowledge benchmark, and failing the conjunction must not be recast as general incoherence.

## 5. Invalid configurations and repairs to the harness

1. **Raw completion mode:** Bonsai-2 returned empty text on all 1,319 GSM8K items. Its valid interface was chat completions with its template.
2. **Thinking on with a 4,096-token cap:** 18–29% of answers were empty or truncated, creating a false ranking driven by trace length. Those scores were quarantined.
3. **Ignored reasoning-off flag:** a server flag did not suppress reasoning. The corrected run set the chat-template keyword and checked the observed `reasoning_content` before scoring.
4. **Thinking-run port collision:** one early parent stream reached the candidate server. It did not complete, was quarantined, and the parent arm was restarted on its intended proxy. Scored records were verified by prompt identity.
5. **Harness item labels:** `lm_eval --samples` permuted `doc_id` labels. The evaluated set was correct; pairing used document text/hash rather than the displayed label.

The final published scores exclude the invalid attempts. The existence of those attempts is important: a benchmark number without chat-template, answer-channel and truncation checks can reverse a model ranking.

## 6. Scope of reproducibility

[Results](data/results.json) gives the aggregate observations and source receipt digests. The [response-free paired table](data/paired_outcomes.csv) and [`recompute_ci.py`](scripts/recompute_ci.py) reproduce the nine main paired intervals; [all 63 deciding SAE layers](data/sae_layers.csv) are also available. The complete internal receipts include full generation traces and machine-local paths; they are not copied here. A complete independent rerun would additionally require exact prompts or dataset-version bindings, scoring scripts, source-object hashes and preferably reviewed, downloadable sample receipts. [Provenance](PROVENANCE.md) marks that gap explicitly. Readers can independently download the pinned public model weights and repeat the stated methods, but should not treat this aggregate-and-outcome package alone as a full rerun.
