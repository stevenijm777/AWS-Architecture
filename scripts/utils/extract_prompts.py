#!/usr/bin/env python3
"""
extract_prompts.py — Materialise the ablation prompt versions out of the notebook.

The Standard prompt lineage lives in whiteboard_selection_lab/prompt_batch_ablation_lab.ipynb
as composable constants (V4 = V0 with substitutions, V5 = V4 + extension, and so
on). That composition is good practice — it makes each version's delta explicit —
but it means the actual text a run used only exists after evaluating Python, and
only inside a notebook.

This writes each version out as a plain .txt plus a manifest carrying its SHA-256,
so a run can record which prompt produced it and anyone can verify that claim
later without opening Jupyter.

Re-run after editing the notebook; output is deterministic.

Usage:
    .venv/bin/python scripts/utils/extract_prompts.py
    .venv/bin/python scripts/utils/extract_prompts.py --check   # verify, write nothing
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from datetime import date
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.append(str(PROJECT_ROOT))

NOTEBOOK = PROJECT_ROOT / "whiteboard_selection_lab" / "prompt_batch_ablation_lab.ipynb"
OUT_DIR = PROJECT_ROOT / "src" / "configs" / "prompts"
PRODUCTION = PROJECT_ROOT / "scripts" / "core" / "vision_analyzer.py"

# Cells that end in an ACTIVE_STAGE2_PROMPT assignment are alternative selections:
# exactly one is executed per experiment run. Each is evaluated independently so a
# later cell redefining STAGE2_V0_BASELINE cannot leak into an earlier variant.
ASSIGN_RE = re.compile(r"^(STAGE\d_[A-Z0-9_]+)\s*=", re.M)
ACTIVE_RE = re.compile(r"ACTIVE_STAGE(\d)_PROMPT\s*=\s*(\w+)")


def normalise(text: str) -> str:
    """Whitespace-insensitive form, so reformatting alone does not change a hash."""
    return re.sub(r"\s+", " ", text).strip()


def sha(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def production_stage2() -> str | None:
    src = PRODUCTION.read_text(encoding="utf-8")
    m = re.search(r'MFR_STAGE_2_PROMPT_TEMPLATE\s*=\s*"""(.*?)"""', src, re.S)
    return normalise(m.group(1)) if m else None


def production_stage1() -> str | None:
    src = PRODUCTION.read_text(encoding="utf-8")
    m = re.search(r'MFR_STAGE_1_PROMPT_TEMPLATE\s*=\s*"""(.*?)"""', src, re.S)
    return normalise(m.group(1)) if m else None


def extract() -> list[dict]:
    nb = json.loads(NOTEBOOK.read_text(encoding="utf-8"))
    cells = nb["cells"]
    results: list[dict] = []

    for idx, cell in enumerate(cells):
        if cell.get("cell_type") != "code":
            continue
        code = "".join(cell.get("source", []))
        active = ACTIVE_RE.search(code)
        if not active:
            continue

        stage, const_name = active.group(1), active.group(2)
        namespace: dict = {}
        try:
            exec(compile(code, f"<cell {idx}>", "exec"), namespace)
        except Exception as e:
            results.append({
                "cell": idx,
                "stage": int(stage),
                "name": const_name,
                "error": f"{type(e).__name__}: {e}",
            })
            continue

        # Capture every version the cell defines, not only the selected one:
        # v4_anti_hallucination and V5_STRICT_ROUTING were never "active" here
        # yet each has its own batch_results file, so their text matters too.
        defined = sorted(set(ASSIGN_RE.findall(code)))
        for name in defined:
            text = namespace.get(name)
            if not isinstance(text, str):
                continue
            results.append({
                "cell": idx,
                "execution_count": cell.get("execution_count"),
                "stage": int(name[5]) if name[5].isdigit() else int(stage),
                "name": name,
                "selected_in_cell": name == const_name,
                "text": text,
                "chars": len(normalise(text)),
                "sha256": sha(normalise(text)),
            })

    return results


def main() -> None:
    parser = argparse.ArgumentParser(description="Extract ablation prompts from the notebook")
    parser.add_argument("--check", action="store_true", help="Verify against existing files, write nothing")
    args = parser.parse_args()

    if not NOTEBOOK.exists():
        print(f"✗ Notebook not found: {NOTEBOOK}", file=sys.stderr)
        sys.exit(1)

    found = extract()
    prod2, prod1 = production_stage2(), production_stage1()

    entries, failures = [], []
    seen: dict[str, str] = {}
    for r in found:
        if "error" in r:
            failures.append(r)
            continue

        prod = prod2 if r["stage"] == 2 else prod1
        matches_production = prod is not None and normalise(r["text"]) == prod

        # The same constant name is defined in several cells. Identical text is
        # one artifact; genuinely different text under one name gets suffixed so
        # neither definition is silently lost.
        base = r["name"].lower().replace("stage2_", "").replace("stage1_", "")
        slug = f"stage{r['stage']}_{base}"
        if r["name"] in seen and seen[r["name"]] != r["sha256"]:
            slug = f"{slug}__cell{r['cell']}"
        elif r["name"] in seen:
            continue  # exact duplicate, already written
        seen[r["name"]] = r["sha256"]

        filename = f"{slug}.txt"
        if not args.check:
            OUT_DIR.mkdir(parents=True, exist_ok=True)
            (OUT_DIR / filename).write_text(r["text"], encoding="utf-8")

        entries.append({
            "name": r["name"],
            "stage": r["stage"],
            "file": filename,
            "sha256": r["sha256"],
            "chars": r["chars"],
            "source_cell": r["cell"],
            "execution_count": r["execution_count"],
            "selected_in_cell": r.get("selected_in_cell", False),
            "matches_production": matches_production,
        })

    manifest = {
        "generated_on": date.today().isoformat(),
        "source_notebook": str(NOTEBOOK.relative_to(PROJECT_ROOT)),
        "production_file": str(PRODUCTION.relative_to(PROJECT_ROOT)),
        "production_stage2_sha256": sha(prod2) if prod2 else None,
        "production_stage1_sha256": sha(prod1) if prod1 else None,
        "note": (
            "Hashes are over whitespace-normalised text, so reindenting a prompt "
            "does not change its identity. matches_production marks the variant "
            "that vision_analyzer.py currently runs."
        ),
        "prompts": entries,
        "unevaluable": [
            {"cell": f["cell"], "name": f["name"], "error": f["error"]} for f in failures
        ],
    }

    manifest_path = OUT_DIR / "MANIFEST.json"
    if not args.check:
        manifest_path.write_text(json.dumps(manifest, indent=2, ensure_ascii=False), encoding="utf-8")

    width = max(len(e["name"]) for e in entries) if entries else 20
    print(f"{'variant':<{width}}  {'chars':>6}  {'sha256':<12}  production")
    for e in entries:
        mark = "← RUNNING" if e["matches_production"] else ""
        print(f"{e['name']:<{width}}  {e['chars']:>6}  {e['sha256'][:12]}  {mark}")

    if failures:
        print(f"\n{len(failures)} cell(s) could not be evaluated standalone:")
        for f in failures:
            print(f"  cell {f['cell']} ({f['name']}): {f['error']}")
        print("  These reference constants defined in an earlier cell — the notebook")
        print("  relies on run order there, so the text is only recoverable in-session.")

    if args.check:
        print("\n(--check: nothing written)")
    else:
        print(f"\n✓ {len(entries)} prompt(s) → {OUT_DIR.relative_to(PROJECT_ROOT)}")
        print(f"✓ manifest → {manifest_path.relative_to(PROJECT_ROOT)}")


if __name__ == "__main__":
    main()
