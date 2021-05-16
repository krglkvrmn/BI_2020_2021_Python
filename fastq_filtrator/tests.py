import unittest
import os
from copy import deepcopy
from fastq_filtrator import parse_arguments, fastq_filtrator


class TestArgumentParser(unittest.TestCase):
    def setUp(self):
        self.output_dict_default = {'min_length': 0, 'keep_filtered': False,
                                    'gc_bounds': [0, 100], 'file_name': '',
                                    'output_base_name': ''}
        self.base_names_test_set = ["filtered", "", "strange.base.name!"]
        self.gc_bounds_test_set = [("20", "30"), ("40",), ("0", "60"), ("50", "100")]
        self.min_length_test_set = ["0", "100", "50", "72"]

    def test_filename_only(self):
        test_args = ["fastq_filtrator.py", "example.fastq"]
        answ = deepcopy(self.output_dict_default)
        answ.update(dict(file_name="example.fastq", output_base_name="example"))

        result = parse_arguments(test_args)
        self.assertDictEqual(result, answ)

    def test_filename_and_basename(self):
        for base_name in self.base_names_test_set:
            test_args = [("fastq_filtrator.py", "--output_base_name", base_name, "example.fastq"),
                         ("fastq_filtrator.py", "example.fastq", "--output_base_name", base_name)]
            answ = deepcopy(self.output_dict_default)
            answ.update(dict(file_name="example.fastq", output_base_name=base_name))

            for arg_set in test_args:
                result = parse_arguments(arg_set)
                self.assertDictEqual(result, answ)

    def test_filename_basename_keep_filtered(self):
        test_args = [("fastq_filtrator.py", "--keep_filtered", "--output_base_name", "filtered", "example.fastq"),
                     ("fastq_filtrator.py", "example.fastq", "--keep_filtered", "--output_base_name", "filtered"),
                     ("fastq_filtrator.py", "example.fastq", "--output_base_name", "filtered", "--keep_filtered")]
        answ = deepcopy(self.output_dict_default)
        answ.update(dict(file_name="example.fastq", output_base_name="filtered", keep_filtered=True))

        for arg_set in test_args:
            result = parse_arguments(arg_set)
            self.assertDictEqual(result, answ)

    def test_filename_basename_keep_filtered_gc_bounds(self):
        for gc_bounds in self.gc_bounds_test_set:
            test_args = [("fastq_filtrator.py", "--gc_bounds", *gc_bounds, "--keep_filtered", "--output_base_name", "filtered", "example.fastq"),
                         ("fastq_filtrator.py", "example.fastq", "--gc_bounds", *gc_bounds, "--keep_filtered", "--output_base_name", "filtered"),
                         ("fastq_filtrator.py", "--output_base_name", "filtered", "example.fastq", "--gc_bounds", *gc_bounds, "--keep_filtered"),
                         ("fastq_filtrator.py", "--output_base_name", "filtered", "--keep_filtered", "--gc_bounds", *gc_bounds, "example.fastq")]
            answ = deepcopy(self.output_dict_default)
            if len(gc_bounds) == 2:
                answ.update(dict(file_name="example.fastq", output_base_name="filtered", keep_filtered=True, gc_bounds=[int(gc_bounds[0]), int(gc_bounds[1])]))
            elif len(gc_bounds) == 1:
                answ.update(dict(file_name="example.fastq", output_base_name="filtered", keep_filtered=True, gc_bounds=[int(gc_bounds[0]), 100]))

            for arg_set in test_args:
                result = parse_arguments(arg_set)
                self.assertDictEqual(result, answ)

    def test_filename_basename_keep_filtered_gc_bounds_min_length(self):
        for min_length in self.min_length_test_set:
            test_args = [("fastq_filtrator.py", "--min_length", min_length, "--gc_bounds", "20", "21", "--keep_filtered", "--output_base_name", "filtered", "example.fastq"),
                         ("fastq_filtrator.py", "example.fastq", "--min_length", min_length, "--gc_bounds", "20", "21", "--keep_filtered", "--output_base_name", "filtered"),
                         ("fastq_filtrator.py", "--output_base_name", "filtered", "--min_length", min_length, "example.fastq", "--gc_bounds", "20", "21", "--keep_filtered"),
                         ("fastq_filtrator.py", "--output_base_name", "filtered", "--keep_filtered", "--min_length", min_length, "--gc_bounds", "20", "21", "example.fastq"),
                         ("fastq_filtrator.py", "--output_base_name", "filtered", "--keep_filtered", "--gc_bounds", "20", "21", "--min_length", min_length, "example.fastq")]
            answ = deepcopy(self.output_dict_default)
            answ.update(dict(file_name="example.fastq", output_base_name="filtered", keep_filtered=True, gc_bounds=[20, 21], min_length=int(min_length)))

            for arg_set in test_args:
                result = parse_arguments(arg_set)
                self.assertDictEqual(result, answ)


class TestFastqfiltrator(unittest.TestCase):

    def get_fastq_seq_name(self, file):
        names = []
        with open(file) as fastq_file:
            while True:
                seq_name = fastq_file.readline()
                fastq_file.readline()
                fastq_file.readline()
                fastq_file.readline()

                if not seq_name:
                    break

                names.append(seq_name.strip())

        return names

    # Test support function for getting seq names in fastq
    def test_get_fastq_name(self):
        # This file has 10 sequences @[1-10]
        self.assertListEqual(self.get_fastq_seq_name("example.fastq"), ['@1', '@2', '@3', '@4', '@5', '@6', '@7', '@8', '@9', '@10'])

    def test_length_filtering(self):
        # result_passed.fastq must have onlt 5 sequences from 1st to 5th
        arguments_1 = {
            "output_base_name": "result",
            "file_name": "example.fastq",
            "keep_filtered": False,
            "min_length": 101,
            "gc_bounds": (0, 100)
        }
        fastq_filtrator(arguments_1)

        self.assertListEqual(self.get_fastq_seq_name(f"{arguments_1['output_base_name']}_passed.fastq"), ["@1", "@2", "@3", "@4", "@5"])
        os.remove("result_passed.fastq")

    def test_keep_filtered(self):
        # result_failed.fastq must have onlt 5 sequences from 6st to 10th
        arguments_1 = {
            "output_base_name": "result",
            "file_name": "example.fastq",
            "keep_filtered": True,
            "min_length": 101,
            "gc_bounds": (0, 100)
        }
        fastq_filtrator(arguments_1)

        self.assertListEqual(self.get_fastq_seq_name(f"{arguments_1['output_base_name']}_failed.fastq"), ["@6", "@7", "@8", "@9", "@10"])
        os.remove("result_passed.fastq")
        os.remove("result_failed.fastq")

    def test_gc_content_filtering(self):
        # result_passed.fastq must have only 6 sequences
        arguments_1 = {
            "output_base_name": "result",
            "file_name": "example.fastq",
            "keep_filtered": False,
            "min_length": 0,
            "gc_bounds": (1, 99)
        }
        fastq_filtrator(arguments_1)

        self.assertListEqual(self.get_fastq_seq_name(f"{arguments_1['output_base_name']}_passed.fastq"), ["@1", "@2", "@3", "@7", "@9", "@10"])
        os.remove("result_passed.fastq")

        # result_passed.fastq must have only 2 sequences
        arguments_2 = {
            "output_base_name": "result",
            "file_name": "example.fastq",
            "keep_filtered": False,
            "min_length": 0,
            "gc_bounds": (50, 50)
        }
        fastq_filtrator(arguments_2)

        self.assertListEqual(self.get_fastq_seq_name(f"{arguments_2['output_base_name']}_passed.fastq"), ["@3", "@7"])
        os.remove("result_passed.fastq")

        # result_passed.fastq must have only 2 sequences
        arguments_3 = {
            "output_base_name": "result",
            "file_name": "example.fastq",
            "keep_filtered": False,
            "min_length": 0,
            "gc_bounds": (0, 0)
        }
        fastq_filtrator(arguments_3)

        self.assertListEqual(self.get_fastq_seq_name(f"{arguments_3['output_base_name']}_passed.fastq"), ["@4", "@8"])
        os.remove("result_passed.fastq")

    def test_result_prefix(self):
        # result file must start with "result"
        arguments_1 = {
            "output_base_name": "result",
            "file_name": "example.fastq",
            "keep_filtered": False,
            "min_length": 0,
            "gc_bounds": (1, 99)
        }
        fastq_filtrator(arguments_1)

        self.assertTrue(f"{arguments_1['output_base_name']}_passed.fastq" in os.listdir())
        os.remove("result_passed.fastq")
