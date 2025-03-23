import random
import string

def generar_codigo_barras(longitud=12):
    caracteres = string.ascii_uppercase + string.digits
    return ''.join(random.choice(caracteres) for _ in range(longitud))
