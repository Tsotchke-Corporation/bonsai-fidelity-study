#!/usr/bin/env python3
"""Recompute the report's paired CIs from response-free outcome rows.

The input contains only hashed item identifiers and correctness bits. Bootstrap
order, sample count, percentile convention and per-task seeds match the study.
"""

import argparse
import csv
import json
import random
from collections import defaultdict
from pathlib import Path


def compute(path: Path, draws: int = 10_000) -> dict:
    groups = defaultdict(list)
    with path.open(newline="") as fh:
        for row in csv.DictReader(fh):
            key = (row["mode"], row["task"], row["metric"])
            groups[key].append((int(row["analysis_order"]), int(row["parent_correct"]),
                                int(row["bonsai2_correct"])))
    out = {}
    for (mode, task, metric), records in sorted(groups.items()):
        records.sort()
        if [r[0] for r in records] != list(range(len(records))):
            raise ValueError(f"duplicate or missing analysis order: {mode}/{task}/{metric}")
        if any(p not in (0, 1) or b not in (0, 1) for _, p, b in records):
            raise ValueError(f"non-binary correctness: {mode}/{task}/{metric}")
        diff = [b - p for _, p, b in records]
        n = len(diff)
        seed = 20260925 if task in ("humaneval", "mbpp") else 20260923
        rng = random.Random(seed)
        boots = sorted(sum(diff[rng.randrange(n)] for _ in range(n)) / n
                       for _ in range(draws))
        out[f"{mode}/{task}/{metric}"] = {
            "n": n,
            "parent": sum(p for _, p, _ in records) / n,
            "bonsai2": sum(b for _, _, b in records) / n,
            "delta": sum(diff) / n,
            "ci95": [boots[int(0.025 * draws)], boots[int(0.975 * draws) - 1]],
            "parent_only": sum(d < 0 for d in diff),
            "bonsai2_only": sum(d > 0 for d in diff),
        }
    return out


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("outcomes", type=Path, nargs="?",
                        default=Path(__file__).resolve().parents[1] / "data/paired_outcomes.csv")
    args = parser.parse_args()
    print(json.dumps(compute(args.outcomes), indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
