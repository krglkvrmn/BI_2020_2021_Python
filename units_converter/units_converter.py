import re
import json

# Read units and their ratios
with open('units.json') as file:
    UNITS = json.load(file)

HELP_MESSAGE = """
                  To convert units type 'cvt' command.
                  Type 'calc' to add or substract different units.
                  Then specify unit type, for example length, weight, etc.
                  Write expression using '->' operator for convertion and
                  '+' and '-' operators for calculation.
                  Examples:
                      cvt length 2.5m -> ft
                      calc length 5km + 345.5yd
                      cvt weight 5g -> lb
                      calc weight 4lb + 10oz
                  Type 'help' to display this message again.
                  Type 'available' to list available units.
                  Press 'Ctrl+C' to exit.
                  Feel free to extend functionality by
                  adding new units to units.json"""


def print_available_units(units: dict):
    for unit_type in units:
        print(f'{unit_type}: {" ".join(units[unit_type])}')


class Value:
    """
    Represents value of particular measurement unit.
    """
    def __init__(self, number: float, unit: str):
        self.number = number
        self.unit = unit

    def __add__(self, other):
        return type(self)(self.number + other.number, self.unit)

    def __sub__(self, other):
        return type(self)(self.number - other.number, self.unit)

    def __repr__(self):
        return '{}{}'.format(self.number, self.unit)


class Converter:
    """
    Provides convertion and calculation of units.
    """
    UNITS = UNITS

    def __init__(self, unit_type: str):
        self.unit_type = unit_type
        self.unit_ref = self.UNITS[self.unit_type]

    def convert(self, value: Value, target_unit: str) -> Value:
        basic_unit_value = value.number * self.unit_ref[value.unit]
        target_unit_value = basic_unit_value / self.unit_ref[target_unit]
        return Value(target_unit_value, target_unit)

    def calculate(self, value1: Value, value2: Value, operator: str):
        # Convert value2 to unit of value1 so you can add them.
        converted_val2 = self.convert(value2, value1.unit)
        if operator == '+':
            return value1 + converted_val2
        elif operator == '-':
            return value1 - converted_val2


print(HELP_MESSAGE)
# Endless loop for convenient interaction.
while True:
    # UI block
    user_command = input('>')
    if user_command == 'help':
        print(HELP_MESSAGE)
        continue
    elif user_command == 'available':
        print_available_units(Converter.UNITS)
        continue
    # Check if all arguments are presented.
    try:
        arguments = re.findall(r'(\w*) (\w*) (\d*\.?\d*)(\w*) ' +
                               r'((?:\-\>)|(?:\+|\-)) (\d*\.?\d*)(\w*)',
                               user_command)[0]
    except IndexError:
        print('Invalid syntax!')
        continue

    operation, unit_type, num1, unit, operator, num2, target_unit = arguments
    # Check if unit type is presented
    try:
        converter = Converter(unit_type)
    except KeyError:
        print(f"Invalid unit type: {unit_type}")
        continue

    # Check if unit is presented
    if not (unit in converter.UNITS[unit_type] and
            target_unit in converter.UNITS[unit_type]):
        print("Unit does not exists!")
        continue

    # Calculation block
    value1 = Value(float(num1), unit)
    if operation == 'cvt':
        if operator != '->':
            print(f'Invalid operator {operator} for cvt!')
            continue
        # Prettify output
        converted_val = converter.convert(value1, target_unit)
        print(f'{value1} = {converted_val}')
    elif operation == 'calc':
        if operator not in ('+', '-'):
            print(f'Invalid operator {operator} for calc!')
            continue
        value2 = Value(float(num2), target_unit)
        result = converter.calculate(value1, value2, operator)
        # Prettify output
        print('{} {} {} = {}'.format(value1, operator, value2, result))
    else:
        print(f"Operation {operation} does not exists!")
