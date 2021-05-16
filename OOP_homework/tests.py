import unittest
from rna_dna_classes import DNA, RNA


class CreateRNA(unittest.TestCase):
    """Test variants of object creation"""
    def test_string(self):
        test_set = ["AAAAAAAAAA", "UUUUUUUUU", "CCCCCCCCCC", "GGGGGGGGG",
                    "CCACaaCACa", "AgCAGcGAcG", "ACUcauCUGAUC", "caucgauc"]
        for string in test_set:
            res = RNA(string)
            self.assertIsInstance(res, RNA)
            self.assertEqual(res._seq, string.upper())

    def test_empty_string(self):
        string = ""
        self.assertRaises(RuntimeError, RNA, string)

    def test_wrong_alphabet_string(self):
        test_set = ["AAAAAAAAAo", "ABCDEFG", "ATCGU", "ATG-*()"]
        for string in test_set:
            self.assertRaises(TypeError, RNA, string)


class CreateDNA(unittest.TestCase):
    def test_string(self):
        test_set = ["AAAAAAAAAA", "TTTTTTTTTTT", "CCCCCCCCCC", "GGGGGGGGG",
                    "CCACaaCACa", "AgCAGcGAcG", "ACTcatCTGATC", "catcgatc"]
        for string in test_set:
            res = DNA(string)
            self.assertIsInstance(res, DNA)
            self.assertEqual(res._seq, string.upper())

    def test_empty_string(self):
        string = ""
        self.assertRaises(RuntimeError, DNA, string)

    def test_wrong_alphabet_string(self):
        test_set = ["AAAAAAAAAo", "ABCDEFG", "ATCGU", "ATG-*()"]
        for string in test_set:
            self.assertRaises(TypeError, DNA, string)


class BaseOperationsTest(unittest.TestCase):
    def test_DNA_equals_DNA(self):
        test_set = [("ATGC", "ATGC", True), ("AAAA", "AAAA", True), ("ATCGAC", "ATCGAC", True),
                    ("CATC", "ACTC", False), ("ATTCG", "TTA", False), ("A", "TAA", False)]
        for str1, str2, equals in test_set:
            self.assertEqual(DNA(str1) == DNA(str2), equals)

    def test_RNA_equals_RNA(self):
        test_set = [("AUGC", "AUGC", True), ("AAAA", "AAAA", True), ("AUCGAC", "AUCGAC", True),
                    ("CAUC", "ACUC", False), ("AUUCG", "UUA", False), ("A", "UAA", False)]
        for str1, str2, equals in test_set:
            self.assertEqual(RNA(str1) == RNA(str2), equals)

    def test_DNA_equals_RNA(self):
        test_set = [("ATGC", "AUGC"), ("AAAA", "AAAA"), ("ATCGAC", "ATCGAC"),
                    ("CATC", "ACUC"), ("ATTCG", "UUA"), ("A", "UAA")]
        for str1, str2 in test_set:
            self.assertRaises(TypeError, lambda x, y: DNA(x) == RNA(y), (str1, str2))

    def test_RNA_equals_DNA(self):
        test_set = [("AUGC", "ATGC"), ("AAAA", "AAAA"), ("AUCGAC", "ATCGAC"),
                    ("CAUC", "ACTC"), ("AUUCG", "TTA"), ("A", "TAA")]
        for str1, str2 in test_set:
            self.assertRaises(TypeError, lambda x, y: RNA(x) == DNA(y), (str1, str2))

    def test_RNA_plus_RNA(self):
        test_set = [("A", "U"), ("ACGA", "A"), ("GGGG", "AGCU"), ("UU", "AGCU")]
        for str1, str2 in test_set:
            self.assertEqual(RNA(str1 + str2), RNA(str1) + RNA(str2))
            self.assertEqual(RNA(str2 + str1), RNA(str2) + RNA(str1))

    def test_DNA_plus_DNA(self):
        test_set = [("A", "T"), ("ACGA", "A"), ("GGGG", "AGCT"), ("TT", "AGCT")]
        for str1, str2 in test_set:
            self.assertEqual(DNA(str1 + str2), DNA(str1) + DNA(str2))
            self.assertEqual(DNA(str2 + str1), DNA(str2) + DNA(str1))

    def test_DNA_plus_RNA(self):
        test_set = [("ATGC", "AUGC"), ("A", "GGAUGC"), ("CGAGAC", "UGC")]
        for dna_str, rna_str in test_set:
            self.assertRaises(TypeError, lambda x, y: DNA(x) + RNA(y), (dna_str, rna_str))

    def test_RNA_plus_DNA(self):
        test_set = [("AUGC", "ATGC"), ("A", "GGATGC"), ("CGAUAC", "TGC")]
        for rna_str, dna_str in test_set:
            self.assertRaises(TypeError, lambda x, y: RNA(x) + DNA(y), (rna_str, dna_str))

    def test_rna_len(self):
        test_set = [("AGUC", 4), ("A", 1), ("AGUCA", 5)]
        for string, length in test_set:
            self.assertEqual(len(RNA(string)), length)

    def test_dna_len(self):
        test_set = [("AGTC", 4), ("A", 1), ("AGTCA", 5)]
        for string, length in test_set:
            self.assertEqual(len(DNA(string)), length)

    def test_dna_getitem(self):
        test_seq = "ATCGATCGACTCGCTACGCTCGCTCGACT"
        test_set = [slice(None, None, None), slice(1, None, None), slice(None, 2, None), slice(None, None, 3),
                    slice(1, None, 2), slice(1, -1, 2), slice(None, 9, 3), slice(1, 8, None), slice(9, 1, -2)]
        for slc in test_set:
            self.assertEqual(DNA(test_seq)[slc], DNA(test_seq[slc]))

    def test_rna_getitem(self):
        test_seq = "AUCGAUCGACUCGCUACGCUCGCUCGACU"
        test_set = [slice(None, None, None), slice(1, None, None), slice(None, 2, None), slice(None, None, 3),
                    slice(1, None, 2), slice(1, -1, 2), slice(None, 9, 3), slice(1, 8, None), slice(9, 1, -2)]
        for slc in test_set:
            self.assertEqual(RNA(test_seq)[slc], RNA(test_seq[slc]))

    def test_dna_hashable(self):
        test_set = ["A", "AGCATCGATC", "GCGCGCGCGCGCTA"]
        for string in test_set:
            try:
                {DNA(string)}
                self.assertEqual(len({DNA(string), string}), 2)
            except TypeError:
                self.fail("Object is unhashable")

    def test_rna_hashable(self):
        test_set = ["A", "AGCAUCGAUC", "GCGCGCGCGCGCUA"]
        for string in test_set:
            try:
                {RNA(string)}
                self.assertEqual(len({RNA(string), string}), 2)
            except TypeError:
                self.fail("Object is unhashable")


class RNA_DNA_gc_content(unittest.TestCase):
    def test_dna_gc_content(self):
        test_set = [("GCGCGCGC", 1), ("ATATATATA", 0), ("ATGCATGCATGC", 0.5), ("ATAGATACATAGATAC", 0.25)]
        for string, gc in test_set:
            res = DNA(string).gc_content()
            self.assertEqual(res, gc)

    def test_rna_gc_content(self):
        test_set = [("GCGCGCGC", 1), ("AUAUAUAUA", 0), ("AUGCAUGCAUGC", 0.5), ("AUAGAUACAUAGAUAC", 0.25)]
        for string, gc in test_set:
            res = RNA(string).gc_content()
            self.assertEqual(res, gc)


class RNA_DNA_complement(unittest.TestCase):
    def test_dna_complement(self):
        test_set = [("A", "T"), ("T", "A"), ("G", "C"), ("C", "G"),
                    ("AT", "TA"), ("GC", "CG"), ("AG", "TC"), ("GT", "CA")]
        for string, c_string in test_set:
            res = DNA(string).complement()
            self.assertEqual(DNA(c_string), res)

    def test_rna_complement(self):
        test_set = [("A", "U"), ("U", "A"), ("G", "C"), ("C", "G"),
                    ("AU", "UA"), ("GC", "CG"), ("AG", "UC"), ("GU", "CA")]
        for string, c_string in test_set:
            res = RNA(string).complement()
            self.assertEqual(RNA(c_string), res)


class RNA_DNA_reverse_complement(unittest.TestCase):
    def test_dna_reverse_complement(self):
        test_set = [("A", "T"), ("T", "A"), ("G", "C"), ("C", "G"),
                    ("AT", "AT"), ("GC", "GC"), ("AG", "CT"), ("GT", "AC"),
                    ("ATGC", "GCAT"), ("CCCC", "GGGG")]
        for string, rc_string in test_set:
            res = DNA(string).reverse_complement()
            self.assertEqual(DNA(rc_string), res)

    def test_rna_reverse_complement(self):
        test_set = [("A", "U"), ("U", "A"), ("G", "C"), ("C", "G"),
                    ("AU", "AU"), ("GC", "GC"), ("AG", "CU"), ("GU", "AC"),
                    ("AUGC", "GCAU"), ("CCCC", "GGGG")]
        for string, rc_string in test_set:
            res = RNA(string).reverse_complement()
            self.assertEqual(RNA(rc_string), res)


class RNA_DNA_iter_test(unittest.TestCase):
    def test_dna_iter(self):
        test_set = ["CAGTCGACTGCATC", "AAAATTTCGGG", "G"]
        for string in test_set:
            res = [i for i in string]
            self.assertEqual([i for i in DNA(string)], res)

    def test_rna_iter(self):
        test_set = ["CAGUCGACUGCAUC", "AAAAUUUCGGG", "G"]
        for string in test_set:
            res = [i for i in string]
            self.assertEqual([i for i in RNA(string)], res)


class DNA_tanscribe_test(unittest.TestCase):
    def test_dna_transcribe(self):
        test_set = [("A", "U"), ("T", "A"), ("ATGCATGC", "UACGUACG")]
        for string, tr_string in test_set:
            self.assertEqual(DNA(string).transcribe(), RNA(tr_string))
