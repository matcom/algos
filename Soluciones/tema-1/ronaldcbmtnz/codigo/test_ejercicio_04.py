"""Casos de prueba del ejercicio 4.

Correr con `pytest test_ejercicio_04.py` o con `python test_ejercicio_04.py`.
"""

from ejercicio_04 import (
    Cinta, incrementar, costo_teorico, total_teorico, potencial, correr, total_msb,
    unos_finales,
)


def test_la_maquina_suma_uno_y_vuelve_a_casa():
    # Especificación del ejercicio 7 de la C1: suma 1 y el cabezal termina en el bit menos significativo.
    cinta = Cinta()
    for k in range(1, 5000):
        incrementar(cinta)
        assert cinta.valor() == k
        assert cinta.cabezal == 0
        assert cinta.bits() == k.bit_length()


def test_costo_de_cada_incremento():
    # Lema 1: incrementar k cuesta exactamente 2 t(k) + 2 pasos.
    cinta = Cinta()
    for k in range(0, 5000):
        assert incrementar(cinta) == costo_teorico(k) == 2 * unos_finales(k) + 2


def test_costo_amortizado_exactamente_4():
    # Teorema 2: con Φ = 2·unos, cada incremento tiene costo amortizado 4.
    reales, potenciales, amortizados = correr(5000)
    assert all(a == 4 for a in amortizados)
    assert potenciales[0] == 0 and all(p >= 0 for p in potenciales)


def test_total_exacto():
    # Corolario: m incrementos cuestan 4m - 2·popcount(m) <= 4m.
    reales, potenciales, _ = correr(20000)
    s = 0
    for m, c in enumerate(reales, 1):
        s += c
        assert s == total_teorico(m) == 4 * m - potenciales[m]
        assert s <= 4 * m


def test_peor_incremento():
    # Uno solo puede costar Θ(log m): el máximo entre los m primeros es 2⌊log2 m⌋ + 2.
    reales, _, _ = correr(4096)
    for m in [1, 2, 3, 7, 8, 100, 1000, 4096]:
        assert max(reales[:m]) == 2 * (m.bit_length() - 1) + 2


def test_cabezal_en_el_bit_mas_significativo_cuesta_m_log_m():
    # La variante paga ~2 bits(k) por incremento: el total crece como m log m.
    for m in [16, 256, 2048]:
        total = total_msb(m)
        bits = sum(max(1, k.bit_length()) for k in range(m))
        assert 2 * bits <= total <= 2 * bits + 4 * m


if __name__ == "__main__":
    pruebas = [f for nombre, f in sorted(globals().items()) if nombre.startswith("test_")]
    for prueba in pruebas:
        prueba()
        print("ok", prueba.__name__)
    print(f"{len(pruebas)} pruebas pasaron")
