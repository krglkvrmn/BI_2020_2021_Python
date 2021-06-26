# SQL homework

The goal of this homework was to create SQLite database using python.

## Description

The work was divided into two parts: **data downloading**  and **database creation**.

### Data downloading (get_data.py)

The data about Japanese animation films was taken from https://myanimelist.net/. Main information from every page was processed and saved to **data/raw_data.csv**. 

```
usage: get_data.py [-h] -o OUTPUT [-c] [-s SEP] [--start START] [--end END]

optional arguments:
  -h, --help            show this help message and exit
  -o OUTPUT, --output OUTPUT
                        Output CSV file to save data
  -c, --continue        Allows continuation of script from the moment where it
                        failed/stopped
  -s SEP, --sep SEP     Field separator
  --start START         ID to start parsing from (ignored if --continue specified)
  --end END             The last ID to parse
```

### Database creation (Database_creation.ipynb)

This notebook contains consecutive instructions that are used for SQLite database creation. This includes usage of pandas and sqlalchemy. Also there is a small EDA, which is designed to proof database correctness.

## Usage

### Download source code and install dependencies

```
git clone https://github.com/krglkvrmn/BI_2020-2021_Python.git
cd BI_2020-2021_Python/SQL_homework
pip install -r requirements.txt
```

### Launch script

```bash
python get_data.py -o data/parsed_data.csv [options]
```

### Launch notebook

```
jupyter notebook Database_creation.ipynb
# or
jupyter lab Database_creation.ipynb
```

