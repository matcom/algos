from boyer_moore_n3_unverified import boyer_moore_n3_unverified

def generate_failing_test_case():
    """
    Genera un caso de prueba donde NINGÚN elemento aparece > n/3 veces,
    pero la versión sin verificación devuelve dos candidatos con contador positivo.
    """
    test_case = [1, 2, 3, 4, 1, 2, 3, 4]
    return test_case

# Validación del generador:
A = generate_failing_test_case()
unverified_result = boyer_moore_n3_unverified(A)

print(f"Arreglo de prueba: {A}")
print(f"Candidatos devueltos sin verificar: {unverified_result}")

# Conteo real:
from collections import Counter
counts = Counter(A)
n = len(A)
real_majority = [elem for elem, count in counts.items() if count > n / 3]

print(f"Frecuencias reales: {dict(counts)}")
print(f"Verdaderos elementos > n/3: {real_majority}")