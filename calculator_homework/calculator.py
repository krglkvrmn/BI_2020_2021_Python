while True:
    try:
        a = float(input())
        operator = input()
        assert operator in ('+', '-', '/', '*', '**', '//', '%')
        b = float(input())
        if operator == '+':
            res = a + b
        elif operator == '+':
            res = a - b
        elif operator == '/':
            res = a / b
        elif operator == '*':
            res = a * b
        elif operator == '**':
            res = a ** b
        elif operator == '//':
            res = a // b
        elif operator == '%':
            res = a % b
        # Return integer value if possible. For example: 5.0 -> 5
        result = int(res) if (res % 1 == 0) else res
        print(result)

    # Start again if invalid operator is entered.
    except AssertionError:
        print('Invalid operator. Try again.')
    # Start again if division by zero was performed.
    except ZeroDivisionError:
        print('Zero division! Try again.')
    # Start again if operands are not numbers.
    except ValueError:
        print('Operands must be numbers. Try again.')
