# OOP homework

In this homework I implemented *DNA* and *RNA* classes for work with biological sequences.

## Description

*RNA* and *DNA* classes are inherited from the *Sequence* class which mostly satisfies *str* interface. *Sequence* class also declares *complement*, *reverse_complement*, and *gc_content* methods, but only its descendants can use it. Also, *DNA* objects have *transcribe* method that returns the corresponding *RNA* object.

### Download source code

```bash
git clone https://github.com/krglkvrmn/BI_2020-2021_Python.git
cd BI_2020-2021_Python/OOP_homework
```

### Examples of usage

```python
>>> from rna_dna_classes import DNA, RNA

>>> RNA("AUCGCUAGCUACUAUUACG").reverse_complement()
RNA(CGUAAUAGUAGCUAGCGAU)

>>> DNA("CGATCTCACGCAC").transcribe()
RNA(GCUAGAGUGCGUG)

>>> DNA("GCGGCGGCGATC").gc_content()
0.8333333333333334

>>> (DNA("CAGCG") + DNA("CGATCGA"))[2:8]
DNA(GCGCGA)
```
