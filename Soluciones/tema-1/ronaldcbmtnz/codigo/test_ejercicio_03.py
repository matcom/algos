"""Casos de prueba del ejercicio 3.

Correr con `pytest test_ejercicio_03.py` o con `python test_ejercicio_03.py`.
"""

import random

from ejercicio_03 import (
    PilaMin, PilaMinCompacta, PilaMinCodificada, ColaMin, Oraculo, Contador,
    secuencia, ejecutar, contraejemplo_minimo,
)


VALORES = [lambda r: r.random(), lambda r: r.randrange(5), lambda r: r.randrange(100),
           lambda r: r.randrange(-3, 3)]


def test_coinciden_con_el_oraculo():
    rng = random.Random(1)
    for _ in range(2000):
        ops = secuencia(rng, rng.randint(1, 60), rng.choice(VALORES[1:]))
        esperado = ejecutar(Oraculo(), ops)
        assert ejecutar(PilaMin(), ops) == esperado
        assert ejecutar(PilaMinCompacta(), ops) == esperado
        assert ejecutar(PilaMinCodificada(), ops) == esperado


def test_invariantes_vigilados():
    # PilaMin: m_k = min del prefijo; compacta: minimos = récords débiles.
    rng = random.Random(2)
    for _ in range(800):
        ops = secuencia(rng, rng.randint(1, 50), rng.choice(VALORES))
        ejecutar(PilaMin(), ops, vigilar=True)
        ejecutar(PilaMinCompacta(), ops, vigilar=True)


def test_una_comparacion_por_operacion():
    # O(1) en el peor caso. PilaMin: a lo sumo una comparación al apilar y ninguna en el
    # resto. La compacta: a lo sumo una al apilar y exactamente una (la igualdad con
    # minimos[-1]) al desapilar. Se cuentan todas las comparaciones entre elementos.
    rng = random.Random(3)
    for clase, al_desapilar in ((PilaMin, 0), (PilaMinCompacta, 1)):
        contador = Contador()
        pila = clase(contador=contador)
        for op, x in secuencia(rng, 20000, VALORES[1]):
            antes = contador.total
            if op == "apilar":
                pila.apilar(x)
                assert contador.total - antes <= 1
            elif op == "desapilar":
                pila.desapilar()
                assert contador.total - antes == al_desapilar
            else:
                getattr(pila, op)()
                assert contador.total == antes


def test_pila_vacia():
    for clase in (PilaMin, PilaMinCompacta):
        pila = clase()
        for op in ("desapilar", "tope", "minimo"):
            try:
                getattr(pila, op)()
            except IndexError:
                pass
            else:
                raise AssertionError(f"{clase.__name__}.{op} debió fallar con la pila vacía")


def test_error_estricto_solo_con_repetidos():
    # Con valores distintos la versión con < es correcta: el error necesita un mínimo repetido.
    rng = random.Random(4)
    for _ in range(2000):
        ops = secuencia(rng, rng.randint(1, 60), VALORES[0])
        assert ejecutar(PilaMinCompacta(estricta=True), ops) == ejecutar(Oraculo(), ops)


def test_contraejemplo_minimo():
    ops = contraejemplo_minimo()
    assert len(ops) == 4
    assert ops[0] == ops[1] and ops[0][0] == "apilar"     # dos copias del mismo mínimo
    assert ejecutar(PilaMinCompacta(estricta=True), ops) != ejecutar(Oraculo(), ops)


def test_peor_caso_de_memoria():
    pila = PilaMinCompacta()
    for x in range(100, 0, -1):
        pila.apilar(x)
    assert pila.memoria() == 200


def test_cola_con_minimo():
    rng = random.Random(5)
    for _ in range(500):
        cola, lista = ColaMin(), []
        for _ in range(rng.randint(1, 80)):
            if lista and rng.random() < 0.4:
                assert cola.desencolar() == lista.pop(0)
            else:
                x = rng.randrange(20)
                cola.encolar(x)
                lista.append(x)
            if lista:
                assert cola.minimo() == min(lista)


def test_cola_mudanzas_amortizadas():
    # Cada elemento se muda a lo sumo una vez: mudanzas <= encolados.
    rng = random.Random(6)
    cola = ColaMin()
    encolados = 0
    for _ in range(50000):
        if len(cola) and rng.random() < 0.5:
            cola.desencolar()
        else:
            cola.encolar(rng.random())
            encolados += 1
    assert cola.mudanzas <= encolados


if __name__ == "__main__":
    pruebas = [f for nombre, f in sorted(globals().items()) if nombre.startswith("test_")]
    for prueba in pruebas:
        prueba()
        print("ok", prueba.__name__)
    print(f"{len(pruebas)} pruebas pasaron")
