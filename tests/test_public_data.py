"""Verify that the released item-level data reproduce the published claims."""

import hashlib
import importlib.util
import json
import csv
import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DATA = json.loads((ROOT / "data/results.json").read_text())


def _bootstrap_module():
    path = ROOT / "scripts/recompute_ci.py"
    spec = importlib.util.spec_from_file_location("recompute_ci", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class PublicDataTests(unittest.TestCase):
    def test_paired_outcomes_reproduce_all_nine_intervals(self):
        csv_path = ROOT / "data/paired_outcomes.csv"
        self.assertEqual(hashlib.sha256(csv_path.read_bytes()).hexdigest(),
                         DATA["paired_outcomes_sha256"])
        actual = _bootstrap_module().compute(csv_path)
        mapping = {
            "off/gsm8k/strict": ("reasoning_off", "gsm8k:strict-match:exact_match"),
            "off/gsm8k/flexible": ("reasoning_off", "gsm8k:flexible-extract:exact_match"),
            "off/ifeval/prompt_strict": ("reasoning_off", "ifeval:none:prompt_level_strict_acc"),
            "on/gsm8k/strict": ("thinking_on", "gsm8k:strict-match:exact_match"),
            "on/gsm8k/flexible": ("thinking_on", "gsm8k:flexible-extract:exact_match"),
            "on/ifeval/prompt_strict": ("thinking_on", "ifeval:none:prompt_level_strict_acc"),
            "on/ifeval/prompt_loose": ("thinking_on", "ifeval:none:prompt_level_loose_acc"),
            "on/humaneval/plus": ("thinking_on", "humaneval_plus"),
            "on/mbpp/plus": ("thinking_on", "mbpp_plus"),
        }
        self.assertEqual(set(actual), set(mapping))
        for key, (section, name) in mapping.items():
            expected = DATA[section][name]
            self.assertEqual(actual[key]["n"], expected["n"])
            self.assertAlmostEqual(actual[key]["delta"], expected["delta"], places=12)
            for a, b in zip(actual[key]["ci95"], expected["ci95"]):
                self.assertAlmostEqual(a, b, places=12)

    def test_sae_layer_export_reproduces_minima(self):
        csv_path = ROOT / "data/sae_layers.csv"
        self.assertEqual(hashlib.sha256(csv_path.read_bytes()).hexdigest(),
                         DATA["sae_layers_sha256"])
        with csv_path.open(newline="") as fh:
            rows = list(csv.DictReader(fh))
        self.assertEqual([int(r["layer"]) for r in rows], list(range(1, 64)))
        self.assertAlmostEqual(min(float(r["bonsai2_survival"]) for r in rows),
                               DATA["sae"]["bonsai2_min_survival"], places=12)
        self.assertAlmostEqual(min(float(r["q8_survival"]) for r in rows),
                               DATA["sae"]["q8_min_survival"], places=12)
        self.assertEqual(sum(float(r["bonsai2_survival"]) < 0.975 for r in rows), 63)
        self.assertEqual(sum(float(r["q8_survival"]) < 0.975 for r in rows), 0)

    def test_quality_gate_ledger_distinguishes_failure_and_unmeasured(self):
        gates = DATA["quality_gates"]
        self.assertGreater(gates["chat"]["max_kl"], gates["chat"]["kl_max_allowed"])
        self.assertGreater(gates["chat"]["parent_top_rank"],
                           gates["chat"]["parent_top_rank_max_allowed"])
        self.assertLess(gates["parent_continuation"]["score"],
                        gates["parent_continuation"]["threshold"])
        self.assertGreater(gates["comprehensibility"]["score"],
                           gates["comprehensibility"]["threshold"])
        self.assertEqual(gates["attribution"]["status"], "unmeasured")

    def test_public_package_links_and_local_data(self):
        for path in ROOT.glob("*.md"):
            for target in re.findall(r"(?<!!)\[[^]]+\]\(([^)]+)\)", path.read_text()):
                if target.startswith(("https://", "http://", "#")):
                    continue
                self.assertTrue((path.parent / target.split("#", 1)[0]).exists(),
                                f"{path.name}: missing {target}")
        forbidden = ("/Users/", "/opt/bonsai", "gs://", "hf_", "pypi-")
        for path in list(ROOT.glob("*.md")) + list((ROOT / "data").glob("*")):
            content = path.read_text()
            self.assertFalse(any(marker in content for marker in forbidden), path.name)


if __name__ == "__main__":
    unittest.main()
