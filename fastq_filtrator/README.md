# Fastq-filtrator and unit testing

The goal of this task was to implement argument parsing from scratch (without using *argparse* library). The script itself filters *fastq* files with raw sequence reads by ***gc content*** and ***minimal length***.

## Description

**Fastq-filtrator (fastq_filtrator.py)**

The script can be run from command line with following arguments:

+ `fastq-file` &mdash; *fastq* file to filter (must have a *.fastq* extension, required).

+ `--min_length` &mdash; minimal length of read (integer greater than zero, optional).
+ `--keep_filtered` &mdash; this flag tells the script to save reads that have not passed filtering to separate file (optional).
+ `--gc_bounds` &mdash; range of GC content (in percents) to filter (two or one non-negative integers <= 100, optional). Default: 0 100. If only one number is specified, it will be used as lower boundary.
+ `--output_base_name` &mdash; common prefix for resulting files (optional). By default the script uses `fastq-file` without extension.

## Usage

### Download source code

```bash
git clone https://github.com/krglkvrmn/BI_2020-2021_Python.git
cd BI_2020-2021_Python/fastq-filtrator
```

### Launch script

```python
python fastq_filtrator.py --keep-filtered --gc_bounds 50 80 --min_length 100 --output_base_name filtered example.fastq
```

### Run tests

```bash
python -m unittest
```
