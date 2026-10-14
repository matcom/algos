"""Casos de prueba del ejercicio 13.

Correr con `pytest test_ejercicio_13.py` o con `python test_ejercicio_13.py`.
"""

import math
import random

from ejercicio_13 import (
    camino, buscar, splay, acceder, recorrido, potencial, tamanos, es_de_busqueda,
    es_camino_izquierdo, invariante_secuencial, descomposicion, cota_global, al_azar,
)


def test_splay_preserva_el_arbol_de_busqueda():
    rng = random.Random(1)
    for n in [1, 2, 3, 10, 57]:
        raiz = camino(n)
        for _ in range(300):
            clave = rng.randint(1, n)
            raiz, _ = acceder(raiz, clave)
            assert raiz.clave == clave and es_de_busqueda(raiz)
            assert len(tamanos(raiz)) == n


def test_invariante_de_la_pasada():
    # Teorema 2: después de acceder a k, la raíz es k y su izquierda es el camino k-1, ..., 1.
    for n in [1, 2, 3, 4, 5, 8, 31, 100, 513]:
        raiz = camino(n)
        for k in range(1, n + 1):
            raiz, _ = acceder(raiz, k)
            assert invariante_secuencial(raiz, k)
        assert es_camino_izquierdo(raiz, n)              # vuelve al camino de partida


def test_las_rondas_son_identicas():
    # Corolario: como el árbol vuelve al camino, cada ronda cuesta exactamente lo mismo.
    for n in [10, 100, 333]:
        costos, _ = recorrido(n, rondas=3)
        assert costos[:n] == costos[n:2 * n] == costos[2 * n:]


def test_lema_de_acceso_vigilado():
    # El lema de acceso nunca falla, y el potencial final es el inicial.
    for n in [16, 64, 200]:
        d = descomposicion(n)
        assert d["fallos"] == 0
        assert math.isclose(d["phi_final"], d["phi0"], rel_tol=1e-12)
        assert math.isclose(d["amortizado"], d["real"], rel_tol=1e-9)
        assert d["real"] <= d["cotas"] + d["phi0"] - d["phi_final"] + 1e-9
        assert d["real"] <= d["global_"]


def test_potencial_del_camino():
    for n in [1, 5, 100]:
        assert math.isclose(potencial(camino(n)), math.lgamma(n + 1) / math.log(2), abs_tol=1e-9)


def test_costo_lineal_y_cota_no_ajustada():
    # Medido: entre 4 y 4,5 rotaciones por acceso; el cociente cota/real crece con log n.
    cocientes = []
    for n in [100, 1000, 10000]:
        costos, _ = recorrido(n)
        assert costos[0] == n - 1
        assert 4.0 <= sum(costos) / n <= 4.5
        cocientes.append(cota_global(n) / sum(costos))
        assert cocientes[-1] >= 0.8 * math.log2(n)
    assert cocientes[0] < cocientes[1] < cocientes[2]


def test_los_primeros_accesos_se_parten_a_la_mitad():
    # El acceso k (para k chico) cuesta alrededor de n / 2^(k-1).
    n = 2**14
    costos, _ = recorrido(n)
    for k in range(1, 8):
        assert abs(costos[k - 1] - n / 2 ** (k - 1)) <= 2 * k


def test_al_azar_crece_como_log_n():
    # Con accesos al azar el costo por acceso sí crece: el lema no es flojo en general.
    por_acceso = [al_azar(n, 3 * n, semilla=n) / (3 * n) for n in [100, 1000, 10000]]
    assert por_acceso[0] < por_acceso[1] < por_acceso[2]
    assert por_acceso[2] > 13


if __name__ == "__main__":
    pruebas = [f for nombre, f in sorted(globals().items()) if nombre.startswith("test_")]
    for prueba in pruebas:
        prueba()
        print("ok", prueba.__name__)
    print(f"{len(pruebas)} pruebas pasaron")
