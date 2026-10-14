"""Casos de prueba del ejercicio 7.

Correr con `pytest test_ejercicio_07.py` o con `python test_ejercicio_07.py`.
"""

import math
import random

from ejercicio_07 import (
    Contador, oraculo, mediana_clasica, mediana_escalera, predicado_en_la_escalera,
    par_de_la_escalera, intercalados, peor_caso, cota_informacion, salidas_posibles,
)


def test_correctas_con_repetidos():
    rng = random.Random(1)
    for _ in range(5000):
        n = rng.randint(1, 30)
        r = rng.choice([3, 20, 10**6])
        A = sorted(rng.randrange(r) for _ in range(n))
        B = sorted(rng.randrange(r) for _ in range(n))
        assert mediana_clasica(A, B) == mediana_escalera(A, B) == oraculo(A, B)


def test_escalera_cubre_los_pares():
    # (0,n-1), (0,n-2), (1,n-2), ..., (n-1,0): 2n - 1 pares, i y j dentro del rango.
    for n in range(1, 30):
        pares = [par_de_la_escalera(k, n) for k in range(2 * n - 1)]
        assert pares[0] == (0, n - 1) and pares[-1] == (n - 1, 0)
        assert all(0 <= i < n and 0 <= j < n for i, j in pares)
        assert len(set(pares)) == 2 * n - 1


def test_predicado_monotono():
    # Lema 2': q es verdadero y después falso a lo largo de la escalera (con repetidos también).
    rng = random.Random(2)
    for _ in range(5000):
        n = rng.randint(1, 25)
        r = rng.choice([3, 50, 10**6])
        A = sorted(rng.randrange(r) for _ in range(n))
        B = sorted(rng.randrange(r) for _ in range(n))
        q = predicado_en_la_escalera(A, B)
        assert q == sorted(q, reverse=True)


def test_peor_caso_exacto_igual_a_la_cota():
    # Teorema 3 + cota de información: la escalera usa exactamente ⌈log2 2n⌉ en el peor caso.
    for n in range(1, 9):
        assert peor_caso(mediana_escalera, n) == cota_informacion(n)


def test_clasico_una_de_mas_en_potencias_de_dos():
    for n in range(1, 9):
        extra = peor_caso(mediana_clasica, n) - cota_informacion(n)
        assert extra == (1 if n >= 2 and n & (n - 1) == 0 else 0)


def test_hay_2n_salidas_posibles():
    # La base de la cota de información: cada uno de los 2n elementos es la mediana de alguna entrada.
    for n in range(1, 8):
        assert len(salidas_posibles(n)) == 2 * n


def test_arbol_binario_con_2n_hojas():
    # Teorema 4 sobre el árbol real de la escalera: con valores distintos ninguna comparación
    # entre A y B empata, así que las ejecuciones son caminos de un árbol binario. Cada camino
    # (hoja) da una sola posición de salida, y hay exactamente 2n hojas, una por respuesta.
    class Registro(Contador):
        def __init__(self):
            super().__init__()
            self.camino = []

        def menor(self, a, b, par=None):
            assert a != b                                   # nunca un "=" entre A y B
            respuesta = super().menor(a, b, par)
            self.camino.append(respuesta)
            return respuesta

    for n in range(1, 8):
        hojas = {}
        for A, B in intercalados(n):
            registro = Registro()
            m = mediana_escalera(A, B, registro)
            posicion = ("A", A.index(m)) if m in A else ("B", B.index(m))
            hojas.setdefault(tuple(registro.camino), set()).add(posicion)
        assert all(len(salidas) == 1 for salidas in hojas.values())
        assert len(hojas) == 2 * n


def test_comparaciones_en_arreglos_grandes():
    rng = random.Random(3)
    for n in [1000, 2**12, 10**5]:
        valores = rng.sample(range(10 * n), 2 * n)
        A, B = sorted(valores[:n]), sorted(valores[n:])
        cont = Contador()
        assert mediana_escalera(A, B, cont) == oraculo(A, B)
        assert cont.total <= math.ceil(math.log2(2 * n))


if __name__ == "__main__":
    pruebas = [f for nombre, f in sorted(globals().items()) if nombre.startswith("test_")]
    for prueba in pruebas:
        prueba()
        print("ok", prueba.__name__)
    print(f"{len(pruebas)} pruebas pasaron")
