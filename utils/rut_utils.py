import re
from itertools import cycle

def validar_rut(rut):
    rut = rut.replace(".", "").replace("-", "").upper()

    if not rut[:-1].isdigit():
        return False

    cuerpo, verificador = rut[:-1], rut[-1]
    reversed_digits = map(int, reversed(cuerpo))
    factors = cycle(range(2, 8))
    s = sum(d * f for d, f in zip(reversed_digits, factors))
    check_digit = (-s) % 11
    check_digit = "K" if check_digit == 10 else str(check_digit)

    return check_digit == verificador
