# Units converter

Here I made script for unit conversion. It supports primitive syntax. 

## Description

Converter supports ***length*** and ***weight*** units which are listed in **units.json** file. You can interact with script via CLI with simple syntax.

### Syntax rules

**Command structure:**

` command unit_type 1st_unit_value operator 2nd_unit_value` 

**Available commands:**

+ ***calc*** - calculate (subtract of add) two units. Available operators are "**+**" and "**-**".
+ ***cvt*** - convert one unit to another. Only conversions inside one unit_type allowed. The only available operator is "**->**".

**Available unit types:**

+ ***length***
+ ***weight***

### Examples

```bash
>>> cvt length 2.5m -> ft
2.5m = 8.202099737532809ft
```

```bash
>>> calc length 5km + 345.5yd
5.0km + 345.5yd = 5.3159252km
```

```bash
>>> cvt weight 5g -> lb
5.0g = 0.011023113109243879lb
```

```bash
>>> calc weight 4lb + 10oz
4.0lb + 10.0oz = 4.625lb
```

## Usage

### Download source code

```bash
git clone https://github.com/krglkvrmn/BI_2020-2021_Python.git
cd BI_2020-2021_Python/units_converter
```

### Launch script

```
python units_converter.py
```