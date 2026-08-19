# The Standard pipeline

What Standard mode actually is, how it was chosen, and what is still unresolved.

Written because every comparative report so far presents *"Standard vs Parsimonious"*
as a comparison of prompts. It is not. They are different architectures, and the
difference is larger than any prompt change measured in the ablations below.

---

## 1. Architecture: two agents, not one prompt

Standard mode splits extraction into two Gemini calls with separate
responsibilities — the **Perceptor / Reasoner** split described in
`Proyecto/Chats/Ingeniería Iterativa de Prompts para Pipelines Multi-Agente.md`.

```
best whiteboard frame ─┐
                       ├─→ Stage 1 · Modeler ──→ World Model ─┐
Whisper transcript ────┘   (what is drawn)                    ├─→ Stage 2 · Planner ──→ graph JSON
                                                              │   (what it means)
                       symbol detector boxes ─────────────────┘
```

**Stage 1 — Modeler ("the eyes").** Extracts a literal inventory: entities,
visual groupings, spatial containment. Explicitly instructed *not* to solve the
final problem — no inference, no canonicalisation.

**Stage 2 — Planner ("the brain").** Takes the World Model as its primary input
and applies domain logic: normalisation against the AWS vocabulary, node fusion
and pruning, flow segmentation (`flow_id` / `seq` / `type`), and audio-driven
expansion when the board shows a generic cloud icon but the transcript names
specific services.

The rationale for splitting: a single agent asked to both perceive and reason
tends to let its architectural priors overwrite what is actually on the board.
Caching Stage 1 also isolates debugging — a bad graph can be traced to
perception or to reasoning, not to an opaque single step.

### Implementation

| Aspect | Value |
|---|---|
| Entry points | [main.py](../main.py) `--mode standard`, [batch_process_standard_missing.py](../scripts/batch_process_standard_missing.py) |
| Analyzer | [vision_analyzer.py](../scripts/core/vision_analyzer.py) |
| Prompts | `MFR_STAGE_1_PROMPT_TEMPLATE`, `MFR_STAGE_2_PROMPT_TEMPLATE` |
| Model | `gemini-3.6-flash` ([settings.py](../config/settings.py)) |
| Temperature | 0.0, both stages |
| Output contract | Pydantic `response_schema` via `types.GenerateContentConfig` |
| Retries | 5, exponential backoff, rotates across 5 API keys on 429 |
| Image input | approved frame from `data/good_whiteboard/{id}.jpg` |
| Output | `data/graphs/{id}.graphml` |

### Where Parsimonious differs

Not a prompt variant — a different pipeline:

| | Standard | Parsimonious |
|---|---|---|
| Gemini calls | **2** | **1** |
| Output contract | Pydantic schema enforced | free JSON, parsed by hand (strips ``` fences, falls back to brace-matching) |
| Transient errors | 5 retries with backoff | none; rotates key on 429 only |
| Prompt lineage | V0 → v4 → V5 → V6 → V7 | v9 → v10 |

Two calls vs one, and a schema-enforced contract vs a hand-parsed one, are
confounds sitting underneath every published Standard-vs-Parsimonious number.
Any future comparison has to either control for them or state them.

---

## 2. How prompts were chosen: the 14-video protocol

Variants were never evaluated on the full corpus. Each candidate ran against a
fixed panel of **14 videos** in [whiteboard_selection_lab/](../whiteboard_selection_lab/),
writing to `lab_workspace/` and never to `data/graphs/`, then scored with the
same `evaluate_pair` the production evaluator uses.

```
-3lnf5lzsH0  -kA0ahrhX3I  -wLEkq21cvA  07lfvavMdfU  1aYoIZvabbk
2L0m28ZLmtE  2e3vOxsHekE  6CgqEzyWpeA  6EUknQqaV1w  6YkguepAQuQ
BZ32w0SSAoY  Cgv0kfp_6xQ  wjtSHyENv0I  ww5fiygF6eg
```

None of the 14 has a zero-edge ground truth, so their Edge F1 is meaningful
throughout. Runner: `batch_prompt_test.py --experiment-label <name>`.

### Generation 1 — `gemini-3.5-flash`

From `experiment_history.json`. Strict evaluation, n=14.

| Version | Service F1 | Edge F1 | Change |
|---|---:|---:|---|
| **V0 (Baseline)** | **90.88%** | **61.11%** | World Model + graph compilation, no extra rules |
| v1_default_3.5_flash | 88.92% | 59.77% | Pydantic structured output |
| v1_monitoring | 86.87% | 55.10% | negative rule: drop background logging/metrics |
| v1_stage2_strict | 86.09% | 58.81% | strict node conservation + edge preservation |
| v2_verbal | 87.90% | 57.47% | **re-run of V0, unchanged** |

`v2_verbal` is the important row: the same prompt re-run scored 87.90% instead
of 90.88%. A 3-point swing from nothing but sampling noise, which is larger than
most of the differences being compared. That result is why temperature was
dropped to 0.0 ([b7d7b78](https://github.com/stevenijm777/AWS-Architecture/commit/b7d7b78)),
and it is the reason no single-run difference under ~3 points on this panel
should be treated as signal.

Both negative-rule variants regressed. Telling the model what *not* to emit
suppressed legitimate nodes along with the noise.

### Generation 2 — `gemini-3.6-flash`, temperature 0.0

| Version | Service F1 | Edge F1 | Change |
|---|---:|---:|---|
| baseline | 90.88% | 61.11% | carried over from V0 |
| v4_anti_hallucination | **91.62%** | 63.45% | explicit valid-vocabulary lists, anti-hallucination directives |
| v4_dynamic_few_shot (RAG) | 90.09% | 61.51% | inject 2 similar architectures as examples |
| V5_with_vision | 86.67% | 53.87% | **vision only, no transcript** |
| V5_STRICT_ROUTING | 90.99% | 65.14% | exact path routing, no intermediate shortcuts |
| **V6_corrected_v2** ← production | 89.94% | 65.28% | faithful transcriber framing, unidirectional default |
| V7_RETURN_FLOWS | 90.58% | **65.73%** | permits explicitly-evidenced return flows |
| V7_RETURN_FLOWS_V6 | 89.30% | **66.52%** | same, on the V6 base |

*(`v4_dynamic_few_shot` and `V5_with_vision` from `Proyecto/Avances/Avance Semanal 3.md`;
the rest from `batch_results_*.json`.)*

Two dead ends worth preserving:

- **Few-shot RAG regressed.** With two example architectures in context the model
  over-connected, reproducing the topology of the examples instead of the video.
- **Vision-only collapsed on edges**, 53.87% vs 61.11%. Much of the ground-truth
  connectivity is stated aloud and never drawn, so the transcript is not a
  supplement to the image — it carries edges the image does not contain. This is
  the ceiling on any purely visual approach here.

### Image-routing experiments (2026-08-08)

Which image each stage receives, same 14 videos:

| Mode | Service F1 | Edge F1 |
|---|---:|---:|
| **baseline_clean** | **91.83%** | **59.48%** |
| user_proposal | 90.90% | 55.49% |
| dual_stage1 | 89.74% | 56.59% |

The clean approved frame won. Feeding preprocessed or duplicated imagery into
Stage 1 hurt both metrics.

### What was chosen

**`V6_corrected_v2`** — not because it topped the table (it did not; it is the
*lowest* Service F1 of generation 2) but because the effort had shifted to edge
connectivity, where it was the best available at the time, and because the
faithful-transcriber framing was judged more likely to generalise beyond the
panel than rules tuned to it.

---

## 3. Production reality

Current run: [reports/runs/2026-08-16_standard_v6corrected_299v](../reports/runs/2026-08-16_standard_v6corrected_299v/).

| | Service F1 | Edge F1 |
|---|---:|---:|
| 299 videos (production) | 86.03% | 58.20% (n=286) |
| the 14 lab videos, scored inside that same run | 87.79% | 58.01% |
| the 14 lab videos, as measured in the lab | 89.94% | **65.28%** |

**The lab reports 65.28% Edge F1 on the same 14 videos that production scores
58.01% on.** Same label, same panel, same evaluator. A 7-point gap that is not
explained by sample composition. Candidate causes, unresolved:

1. **The lab's Stage 2 prompt has diverged from production.** `batch_prompt_test.py`
   carries its own copy under a comment claiming it is *"Identical to
   vision_analyzer.py"*. It is not: production runs the *"Expert Cloud
   Architecture Transcriber"* text (3984 chars), the lab still has the older
   *"expert AWS Solutions Architect … generalize your reasoning"* text (2523
   chars). Opposite instructions — transcribe faithfully vs infer the logical
   architecture. Stage 1 is still byte-identical.
2. The lab injects adaptive whiteboard detection results into the prompt; whether
   production does so identically has not been verified.

Until this is resolved, **lab numbers and production numbers are not comparable**,
and the ablation table above ranks variants only relative to each other.

### The prompts are preserved — but the version names are ambiguous

An earlier revision of this document claimed the generation-2 prompts were
unrecoverable. **That was wrong.** It was written from `batch_prompt_test.py`,
where the templates were indeed overwritten in place, without checking
[`prompt_batch_ablation_lab.ipynb`](../whiteboard_selection_lab/prompt_batch_ablation_lab.ipynb),
which holds all of them.

The notebook defines each version compositionally, which makes every delta
explicit and is better practice than duplicating whole prompts:

```python
V4 = V0.replace(TOXIC_INTRO, NEW_INTRO_TRANSCRIBER).replace(...) + ANTI_HALLUCINATION_RULES
V5 = V4 + STRICT_ROUTING_RULES
V6 = V4 + CONTAINMENT_ROUTING_RULE
V7 = V6 + RETURN_PATH_RULES
```

The real problem is different, and narrower: **the notebook has five alternative
selection cells, and each redefines the base constants.** The same name therefore
denotes different text depending on which cell ran:

| Constant | cell 7 | cell 8 | cell 9 | cell 10 |
|---|---:|---:|---:|---:|
| `STAGE2_V0_BASELINE` | 2513 | 2375 | — | — |
| `STAGE2_V4_ANTI_HALLUCINATION` | 3422 | 2904 | — | — |
| `STAGE2_V5_STRICT_ROUTING` | 3737 | 3256 | — | — |
| `STAGE2_V6_CORRECTED` | 3887 | — | **3974** | 3835 |

*(whitespace-normalised character counts)*

So `batch_results_V6_corrected_v2.json` names a prompt that has three candidate
texts, and the filename alone does not say which one produced it. That is the
gap to close — not lost prompts, but unresolvable references.

**Which one production runs is now settled.** The cell-9 `STAGE2_V6_CORRECTED`
is byte-identical to `MFR_STAGE_2_PROMPT_TEMPLATE` in `vision_analyzer.py`
(sha256 `ed1d85054d73…`), and cell-6 `STAGE1_V0_BASELINE` matches Stage 1
(`497d30164f48…`). All 299 production graphs run that pair. This was previously
listed here as an open question; it is answered.

Every variant is now materialised outside the notebook by
[`extract_prompts.py`](../scripts/utils/extract_prompts.py) into
`src/configs/prompts/`, one `.txt` per version plus a `MANIFEST.json` carrying
each SHA-256. Texts that share a name but differ get a `__cellN` suffix rather
than overwriting each other. Hashes are over whitespace-normalised text, so
reindenting a prompt does not change its identity.

One variant resists extraction: cell 11's `STAGE2_V7_RETURN_FLOWS` builds on
constants defined in an earlier cell, so it only resolves in a live session with
the right run order. Cell 7 defines a `STAGE2_V7_RETURN_FLOWS` that does extract
cleanly, but there is no guarantee the two are the same text.

Parsimonious solved this differently and arguably better:
`parsimonious_prompt_history.md` archives the full text of all 79 records inline,
so no reconstruction is needed at all.

---

## 4. Open items

**V7 was never promoted.** Both V7 variants beat V6 on Edge F1 (65.73% and
66.52% vs 65.28%), and `V7_RETURN_FLOWS` also beats it on Service F1 (90.58% vs
89.94%). Return flows are exactly the known weakness — roughly a third of
ground-truth flows are bidirectional against about 11% in V6. All 299 production
graphs are V6. Whether to promote V7 should wait until item 1 above is settled,
since the gap it would be judged on is smaller than the lab/production
discrepancy.

**Provenance of 28 graphs is unproven.** The Stage 2 prompt last changed in
[a7b218f](https://github.com/stevenijm777/AWS-Architecture/commit/a7b218f),
committed 2026-08-03 12:34. 28 of the 316 graphs were written that morning
starting 11:41 — before the commit, though working-tree edits normally precede
commits, so they were probably produced with the current prompt. Not provable
from timestamps. Re-running those 28 would remove the doubt.

**Disambiguate the redefined constants.** Three different texts answer to
`STAGE2_V6_CORRECTED`, and two each to `V0_BASELINE`, `V4_ANTI_HALLUCINATION`
and `V5_STRICT_ROUTING`. Every `batch_results_*.json` records a version *name*,
not a hash, so the generation-2 rows in the ablation table cannot currently be
tied to a specific text. Resolving it means either checking which cell was last
run before each result file, or accepting the rows as approximate.

**Prompt archival in runs.** `src/configs/prompts/MANIFEST.json` now gives every
variant a stable SHA-256. The remaining step is for `evaluate_standard.py` to
record the hash of the prompt that produced the graphs into each `run.json`, so
a result can never again name a prompt it cannot prove.

---

## 5. Reproducing an evaluation

```bash
.venv/bin/python scripts/utils/evaluate_standard.py --label v6corrected
.venv/bin/python scripts/utils/render_standard_report.py reports/runs/<run-dir>
.venv/bin/python scripts/utils/build_manifest.py
```

Edge averages exclude ground-truth graphs with zero edges, where F1 is 0 by
construction; the all-inclusive average is kept in `run.json` as
`edge_f1_legacy_including_zero_edge_gt` for comparison with older reports.
`scripts/utils/snapshot_state.py` gives a read-only view of coverage and
integrity without producing a run.
