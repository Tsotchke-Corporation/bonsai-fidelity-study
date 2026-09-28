#!/usr/bin/env python3
"""Render the published paired-difference figure from results.json."""

import csv
from html import escape
import json
from pathlib import Path

import matplotlib.pyplot as plt


ROOT = Path(__file__).resolve().parents[1]
DATA = json.loads((ROOT / "data/results.json").read_text())


def _finish_svg(path: Path, title: str) -> None:
    svg = path.read_text()
    end = svg.find(">", svg.find("<svg")) + 1
    if end == 0:
        raise ValueError("missing SVG root")
    svg = svg[:end] + "\n<title>" + escape(title) + "</title>" + svg[end:]
    path.write_text("\n".join(line.rstrip() for line in svg.splitlines()) + "\n")


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
                         "svg.fonttype": "none", "svg.hashsalt": "bonsai-study-v1"})
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
    ax.set_title("Bonsai-2 27B vs Qwen3.8-27B BF16: paired task accuracy",
                 loc="left", fontsize=14, pad=15)
    ax.grid(axis="x", alpha=0.2)
    out = ROOT / "figures/paired_differences.svg"
    out.parent.mkdir(exist_ok=True)
    fig.savefig(out, format="svg", bbox_inches="tight")
    fig.savefig(out.with_suffix(".png"), dpi=180, bbox_inches="tight")
    _finish_svg(out, "Bonsai-2 27B vs Qwen3.8-27B BF16: paired task accuracy")
    plt.close(fig)

    with (ROOT / "data/sae_layers.csv").open(newline="") as fh:
        rows = list(csv.DictReader(fh))
    layer = [int(r["layer"]) for r in rows]
    b2 = [float(r["bonsai2_survival"]) for r in rows]
    q8 = [float(r["q8_survival"]) for r in rows]
    fig, ax = plt.subplots(figsize=(9.5, 4.1), layout="constrained")
    ax.plot(layer, b2, color="#a35220", linewidth=2.2, label="Bonsai-2 PQ2_0")
    ax.plot(layer, q8, color="#185f8f", linewidth=2.0, label="Stock Q8_0 control")
    ax.axhline(0.975, color="#404040", linestyle="--", linewidth=1.2,
               label="GeoRefine parent-preservation criterion: 0.975")
    ax.plot([46], [b2[45]], marker="o", markersize=5, color="#a35220")
    ax.annotate("L46: 0.802", (46, b2[45]), xytext=(49, 0.77),
                arrowprops={"arrowstyle": "-", "color": "#a35220"}, fontsize=9)
    ax.set(xlim=(1, 63), ylim=(0.73, 1.01), xlabel="Residual-stream layer",
           ylabel="Parent rare-feature survival",
           title="Bonsai-2 misses the parent-coordinate criterion at every deciding layer")
    ax.grid(alpha=0.18)
    ax.legend(loc="lower left", fontsize=9, frameon=False)
    out = ROOT / "figures/sae_survival.svg"
    fig.savefig(out, format="svg", bbox_inches="tight")
    fig.savefig(out.with_suffix(".png"), dpi=180, bbox_inches="tight")
    _finish_svg(out, "Bonsai-2 and Q8_0 parent rare-feature survival by layer")
    plt.close(fig)


if __name__ == "__main__":
    main()
