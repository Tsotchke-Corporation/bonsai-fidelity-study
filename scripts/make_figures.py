#!/usr/bin/env python3
"""Render the published paired-difference figure from results.json."""

import json
from pathlib import Path

import matplotlib.pyplot as plt


ROOT = Path(__file__).resolve().parents[1]
DATA = json.loads((ROOT / "data/results.json").read_text())


def main() -> None:
    specs = [
        ("GSM8K · reasoning off · n=1,319", "reasoning_off", "gsm8k:flexible-extract:exact_match"),
        ("IFEval · reasoning off · n=541", "reasoning_off", "ifeval:none:prompt_level_strict_acc"),
        ("GSM8K · thinking on · n=300", "thinking_on", "gsm8k:flexible-extract:exact_match"),
        ("IFEval · thinking on · n=541", "thinking_on", "ifeval:none:prompt_level_strict_acc"),
        ("HumanEval+ · thinking on · n=164", "thinking_on", "humaneval_plus"),
        ("MBPP+ · thinking on · n=378", "thinking_on", "mbpp_plus"),
    ]
    plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 10,
                         "svg.fonttype": "none"})
    fig, ax = plt.subplots(figsize=(9.5, 4.2), layout="constrained")
    for i, (label, section, name) in enumerate(specs):
        x = DATA[section][name]
        d = 100 * x["delta"]
        lo, hi = (100 * v for v in x["ci95"])
        color = "#185f8f" if section == "thinking_on" else "#a35220"
        ax.errorbar(d, i, xerr=[[d - lo], [hi - d]], fmt="o", color=color,
                    markersize=6, capsize=3, linewidth=1.8)
    ax.axvline(0, color="#404040", linewidth=1)
    ax.axvline(-2, color="#777777", linestyle="--", linewidth=1)
    ax.set_yticks(range(len(specs)), [x[0] for x in specs])
    ax.invert_yaxis()
    ax.set_xlim(-7.5, 5)
    ax.set_xlabel("Bonsai-2 minus its BF16 parent (percentage points, paired 95% CI)")
    ax.set_title("A small or unresolved task gap is not an equivalence certificate", loc="left")
    ax.grid(axis="x", alpha=0.2)
    out = ROOT / "figures/paired_differences.svg"
    out.parent.mkdir(exist_ok=True)
    fig.savefig(out, format="svg", bbox_inches="tight")
    fig.savefig(out.with_suffix(".png"), dpi=180, bbox_inches="tight")
    # Matplotlib emits trailing spaces on wrapped SVG path lines.
    out.write_text("\n".join(line.rstrip() for line in out.read_text().splitlines()) + "\n")
    plt.close(fig)


if __name__ == "__main__":
    main()
