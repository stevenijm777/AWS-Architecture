# 🚧 System Constraints & Operational Boundaries

## 1. Supported Input Regime

- **Video Format**: Standard MP4 videos from YouTube (*AWS This is My Architecture* series).
- **Resolution**: No enforced minimum. ≥720p correlates with the automatic selector
  producing a high-confidence candidate more often, but this is *not* a hard floor —
  see the correction in §2.3 below. Below-720p videos are not rejected; they still
  go through the same manual-review step every video goes through.
- **Language**: Whisper transcribes in the original language and does not translate;
  Standard's Stage 2 prompt has an explicit rule to translate output fields to
  English, Parsimonious does not (verified in code, 2026-08-20). Empirically this
  causes no contamination in either mode on the current corpus — see
  `docs/estado-y-pendientes.md` / the language breakdown in the audit report.
- **Video Duration**: Technical presentations between 2 minutes and 12 minutes are
  the typical case; longer videos are not excluded by duration alone — see §2.2.

## 2. Explicit Exclusion Criteria & Manual Overrides

1. **Non-English Audio**: NOT excluded. 42 non-English videos (Italian, French,
   Korean, Spanish, German, Japanese, Arabic, Mandarin, Hebrew) are in the eligible
   study set today and score *higher* on average than English ones (90.9% vs 86.3%
   Service F1, Standard). An earlier version of this document claimed exclusion and
   cited only 2 languages — that was wrong on both counts.
2. **Compilation / Spotlight Episodes**: excluded by two independent mechanisms that
   don't always agree. `scripts/utils/audit_dataset_coverage.py` matches title
   keywords (*"spotlight"*, *"greatest hits"*, *"bloopers"*, *"reprise"*, *"special
   episode"*, *"(special)"*) against the **catalog title** in `videos.csv`.
   `main.py`'s `is_special_video()` checks the **live title fetched from YouTube**
   at download time, plus a duration threshold (`> 12:00`). These can disagree: on
   2026-08-21, `EW4X5z7m-0U` and `1VcpCVe3tLQ` were correctly caught by the live
   check (their YouTube titles carry a `(Special)` suffix the catalog's title
   doesn't have) but were invisible to the catalog-based audit. Anyone trusting the
   audit's "episodios especiales" count alone can undercount this category.
3. **Whiteboard Curation Is Always Manual — There Is No Automatic Path.**
   This document previously described manual curation as an edge case ("if a
   presenter never steps away from the whiteboard... the best frame is manually
   curated") triggered only for ~51 hard cases, implying most videos get an
   automatic pass into `data/good_whiteboard/`. **That is not what the code does.**
   Verified directly in `main.py` (2026-08-21): the pipeline only ever *reads* from
   `good_whiteboard/` (checks existence, uses it as vision input, refuses to run
   vision if absent). No code path anywhere writes to it. Every single file in
   `good_whiteboard/`, for the whole project's history, got there because a human
   looked at the pipeline's best guess (always dropped in `bad_whiteboard/` first)
   and decided it was good enough — confirmed by the git history, which is a long
   series of commits like *"move 26 manually curated whiteboards from
   bad_whiteboard to good_whiteboard"*. The "~51" figure names a *particularly
   hard* subset (severe occlusion, or videos hit by the frame-selector's own
   filtering discarding all but one candidate), not the boundary between automatic
   and manual — there is no automatic branch to draw that boundary against.

### 2.3 Correction: resolution is not the mechanism, video style might be

A prior pass through this document asserted a hard `≥720p` requirement, backed by
a stat cited in `TODO_PARA_EL_ARTICULO.md` ("the selector scores 100% at ≥720p,
26.5% at 360p"). That stat describes how often the *automatic* selector emits a
high-confidence candidate — it does not mean 360p frames are unusable, and this
document previously blurred that distinction into a hard input constraint.

Direct counter-evidence from 2026-08-21: 17 previously-unprocessed GT videos were
downloaded. All landed at 640×360 (`format_id=18`) because no local PO-Token
provider is running for yt-dlp's `mweb` client (a *different*, unrelated anti-bot
mechanism from the missing-cookies problem the 720p issue was originally attributed
to). Of these, 3 (`aN26J-7q9Hw`, `kD57QUn5myc`, `SxFag4CMWU8`) were manually
reviewed and approved as good whiteboards *at the same 360p resolution* that made
the other ~12 fail. Resolution alone does not predict outcome.

**Working hypothesis, not yet validated:** the icon/symbol detector
(`scripts/utils/symbol_detector.py`) relies on HSV saturation/value thresholds
tuned to a particular whiteboard visual style (marker colors, background,
digital-whiteboard product). Videos using a different visual style may fail
detection regardless of resolution. This needs a proper test — e.g. run the
detector on the 3 approved-vs-rejected 360p pairs and compare icon counts and
saturation histograms — before it can be stated as fact. Flagged as Future Work,
replacing the old "raise the resolution floor" framing.

## 3. Hardware & API Quotas

- **GPU Memory**: Local Whisper transcription requires CUDA GPU with $\ge 6\text{ GB}$ VRAM.
- **Gemini API Limits**: API calls must observe TPM/RPM rate limits; local keyframe pre-processing `--skip-vision` is supported to run offline stages prior to batch vision evaluation.
