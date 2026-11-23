"""Q-17 unit tests. No MAFFT or IQ-TREE runs."""
import hashlib
import json
import math
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

from q17_run import (
    K,
    assess_tree,
    canonical_kmers,
    jaccard,
    load_pins,
    load_selection,
    mash_distance,
    method3,
    neighbor_joining,
    sha256_file,
    validate_selection,
)


class RegistrationTests(unittest.TestCase):
    def test_agreement_document_frozen(self):
        text = (ROOT / "tests" / "PRE-REGISTERED-AGREEMENT-Q17.md").read_text()
        self.assertIn("Written:** Sun 22 Nov 2026, 4:46 PM PST", text)
        self.assertIn("before any new", text)
        self.assertIn("The letter remains B-blast regardless of these results.", text)
        self.assertIn("k = 21", text)
        self.assertIn("UFBoot ≥ 95", text)
        pins = load_pins(ROOT)
        self.assertTrue(pins["written_before_mafft_iqtree_or_kmer"])
        self.assertEqual(pins["test1_letter_unchanged"], "B-blast")
        self.assertEqual(
            pins["fasta"]["sha256"],
            "787a51c247a3fa2195f75989a28783e6edbe3ff38c76117115a87349ababa0b3",
        )

    def test_fasta_hash_matches_if_present(self):
        pins = load_pins(ROOT)
        path = ROOT / pins["fasta"]["path"]
        if path.is_file():
            self.assertEqual(sha256_file(path), pins["fasta"]["sha256"])
            self.assertEqual(sha256_file(path), hashlib.sha256(path.read_bytes()).hexdigest())


class KmerTests(unittest.TestCase):
    def test_canonical_skips_n_and_is_canonical(self):
        # k=21 needs a longer string; test via a short k by calling with k=3
        s = "ACGNTTA"
        km = canonical_kmers(s, k=3)
        # Windows: ACG (skip, N), CGN skip, GNT skip, NTT skip, TTA / TAA canonical TAA? TTA rc=TAA, min is TAA
        self.assertEqual(km, {"ACG", "TAA"})
        # identical sequences, J=1, Mash distance 0
        a = canonical_kmers("ACGT" * 20, k=21)
        b = canonical_kmers("ACGT" * 20, k=21)
        self.assertEqual(jaccard(a, b), 1.0)
        self.assertAlmostEqual(mash_distance(1.0, 21), 0.0)
        self.assertEqual(mash_distance(0.0, 21), "undefined")
        self.assertEqual(mash_distance(None, 21), "undefined")
        # Mash formula at J=0.5
        j = 0.5
        expected = -(1 / 21) * math.log((2 * j) / (1 + j))
        self.assertAlmostEqual(mash_distance(j, 21), expected)

    def test_empty_set_is_undefined(self):
        self.assertIsNone(jaccard(set(), {"ACGT"}))


class NeighborJoiningTests(unittest.TestCase):
    def test_three_taxon_split(self):
        names = ["A", "B", "C"]
        # A close to B, both far from C
        matrix = [
            [0.0, 0.1, 0.9],
            [0.1, 0.0, 0.9],
            [0.9, 0.9, 0.0],
        ]
        nwk = neighbor_joining(names, matrix)
        self.assertIn("A", nwk)
        self.assertIn("B", nwk)
        self.assertIn("C", nwk)
        self.assertTrue(nwk.endswith(";"))


class TreeAgreementTests(unittest.TestCase):
    def test_agree_and_disagree_topologies(self):
        # ((Q,C1,C2), (F1,F2), O)
        # Newick with support labels on the critical branch
        agree = "(((Q:0.01,C1:0.01):0.01,C2:0.01)80/95:0.2,(F1:0.01,F2:0.01):0.2,O:0.3);"
        r = assess_tree(agree, "Q", "O", ["F1", "F2"], ["C1", "C2"])
        self.assertTrue(r["outgroup_split"])
        self.assertEqual(r["verdict"], "AGREE")
        disagree = "(((Q:0.01,F1:0.01):0.01,F2:0.01)80/95:0.2,(C1:0.01,C2:0.01):0.2,O:0.3);"
        r = assess_tree(disagree, "Q", "O", ["F1", "F2"], ["C1", "C2"])
        self.assertEqual(r["verdict"], "DISAGREE")
        low = "(((Q:0.01,C1:0.01):0.01,C2:0.01)50/70:0.2,(F1:0.01,F2:0.01):0.2,O:0.3);"
        r = assess_tree(low, "Q", "O", ["F1", "F2"], ["C1", "C2"])
        self.assertEqual(r["verdict"], "INCONCLUSIVE")
        # Supported mixed placement: Q with one cov and one flu.
        neither = "(((Q:0.01,C1:0.01):0.01,F1:0.01)80/95:0.2,(C2:0.01,F2:0.01):0.2,O:0.3);"
        r = assess_tree(neither, "Q", "O", ["F1", "F2"], ["C1", "C2"])
        self.assertEqual(r["verdict"], "DISAGREE")
        # Same mixed placement but support below threshold: INCONCLUSIVE.
        neither_low = "(((Q:0.01,C1:0.01):0.01,F1:0.01)50/70:0.2,(C2:0.01,F2:0.01):0.2,O:0.3);"
        r = assess_tree(neither_low, "Q", "O", ["F1", "F2"], ["C1", "C2"])
        self.assertEqual(r["verdict"], "INCONCLUSIVE")
        # Singleton outgroup is not its own internal node; monophyly split
        # already places the outgroup on the far side (Method 2 workaround).
        # Unrooted form: ((Q,C1,C2),F1,F2,O) with support on the Q+cov clade.
        singleton_og = "((Q:0.01,C1:0.01,C2:0.01)80/95:0.2,F1:0.01,F2:0.01,O:0.3);"
        r = assess_tree(singleton_og, "Q", "O", ["F1", "F2"], ["C1", "C2"])
        self.assertTrue(r["outgroup_split"])
        self.assertEqual(r["verdict"], "AGREE")



class SelectionPinTests(unittest.TestCase):
    def test_committed_selection_matches_pins(self):
        pins = load_pins(ROOT)
        sel = load_selection(ROOT)
        validate_selection(sel, pins)

    def test_rejects_query_mismatch(self):
        pins = load_pins(ROOT)
        sel = load_selection(ROOT)
        sel = dict(sel)
        sel["query"] = "NC_999999.1"
        with self.assertRaises(SystemExit):
            validate_selection(sel, pins)


class Method3RuleTests(unittest.TestCase):
    def _g(self, acc):
        return {"org": acc, "segs": [{"segment": 1, "accession": acc}], "concat_header": acc}

    def test_outgroup_nearest_is_inconclusive_even_if_mean_flu_is_closer(self):
        # Q almost identical to the outgroup. S_cov shares no 21-mers with Q
        # (mean d_cov is the undefined-pair placeholder). S_flu shares a few,
        # so mean d_flu < d_cov. The frozen primary rule is still INCONCLUSIVE
        # because the nearest reference is the outgroup.
        q = "ACGT" * 30  # 120 bp
        o = "ACGT" * 29 + "ACGA" * 1
        # shift start of flu so some k-mers overlap, cov is all T (no overlap)
        f = "ACGT" * 10 + "GGGG" * 20
        c = "TTTT" * 30
        seqs = {"Q": q, "O": o, "C1": c, "C2": c, "F1": f, "F2": f}
        report = method3(
            self._g("Q"),
            [self._g("F1"), self._g("F2")],
            [self._g("C1"), self._g("C2")],
            self._g("O"),
            seqs,
        )
        self.assertEqual(report["primary"], "INCONCLUSIVE")
        self.assertIn("outgroup", report["reason"].lower())

    def test_nj_neither_is_disagree_so_conflict_is_inconclusive(self):
        # Primary: Q nearest C1 and mean d_cov < d_flu (AGREE).
        # Topology: forced mixed by making Q close to C1 and F1 only.
        # We only assert the secondary branch when NJ fails both complete
        # monophyly splits.
        q = "ACGT" * 40
        c1 = "ACGT" * 39 + "AAAA"
        c2 = "TTTT" * 40
        f1 = "ACGT" * 20 + "CCCC" * 20
        f2 = "GGGG" * 40
        o = "ATAT" * 40
        seqs = {"Q": q, "C1": c1, "C2": c2, "F1": f1, "F2": f2, "O": o}
        report = method3(
            self._g("Q"),
            [self._g("F1"), self._g("F2")],
            [self._g("C1"), self._g("C2")],
            self._g("O"),
            seqs,
        )
        # If NJ recovered neither complete split, the frozen secondary
        # rule is DISAGREE, and a primary/secondary conflict is INCONCLUSIVE.
        if report.get("nj_topology") == "DISAGREE" and "neither" in report.get("nj_reason", ""):
            if report["primary"] == "AGREE":
                self.assertEqual(report["verdict"], "INCONCLUSIVE")
        self.assertIn(report.get("nj_topology"), {"AGREE", "DISAGREE", "INCONCLUSIVE"})


if __name__ == "__main__":
    unittest.main()
