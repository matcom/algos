"""Ejercicio 4 (C1, C4): contador binario en una maquina de Turing de una cinta.
"""

BLANCO = "_"
IZQ, DER = -1, +1

TABLA = {
    ("inc", "1"): ("0", IZQ, "inc"),
    ("inc", "0"): ("1", DER, "volver"),
    ("inc", BLANCO): ("1", DER, "volver"),
    ("volver", "0"): ("0", DER, "volver"),
    ("volver", "1"): ("1", DER, "volver"),
    ("volver", BLANCO): (BLANCO, IZQ, "alto"),
}


class SinTransicion(Exception):
    """La maquina quedo en una configuracion sin transicion (y no esta en 'alto')."""


def cinta_de(bits):
    """Cinta con la cadena `bits` (ej. '1011'), su ultimo caracter en la celda 0."""
    return {-i: ch for i, ch in enumerate(reversed(bits))}


def leer(cinta, pos):
    return cinta.get(pos, BLANCO)


def texto(cinta):
    """El contenido de la cinta como cadena (de la primera a la ultima celda no blanca)."""
    celdas = [p for p, s in cinta.items() if s != BLANCO]
    if not celdas:
        return ""
    return "".join(leer(cinta, p) for p in range(min(celdas), max(celdas) + 1))


def valor(cinta):
    t = texto(cinta)
    assert BLANCO not in t, f"hay un blanco dentro del numero: {t!r}"
    return int(t, 2) if t else 0


def unos(cinta):
    return sum(1 for s in cinta.values() if s == "1")


def ceros(cinta):
    return sum(1 for s in cinta.values() if s == "0")


def terminan_en_unos(bits):
    """k = cantidad de unos al final de la cadena (el oraculo del costo)."""
    return len(bits) - len(bits.rstrip("1"))


def ejecutar(cinta, tabla=TABLA, estado="inc", pos=0, tope=10 ** 7, paso=None):
    """Corre la maquina hasta 'alto'. Devuelve (pasos, pos, estado).

    `paso(pasos, estado, pos)` (opcional) se llama despues de cada paso.
    Lanza SinTransicion si falta una transicion; devuelve estado 'no termina' si pasa `tope` pasos.
    """
    pasos = 0
    get = cinta.get
    while estado != "alto":
        if pasos >= tope:
            return pasos, pos, "no termina"
        try:
            escribe, mueve, nuevo = tabla[(estado, get(pos, BLANCO))]
        except KeyError:
            raise SinTransicion(f"estado {estado!r} leyendo {get(pos, BLANCO)!r} en la celda {pos}") from None
        cinta[pos] = escribe
        pos += mueve
        estado = nuevo
        pasos += 1
        if paso is not None:
            paso(pasos, estado, pos)
    return pasos, pos, estado


def incrementar(cinta, tabla=TABLA, **kw):
    """Un incremento: cabezal en la celda 0, estado inicial 'inc'."""
    return ejecutar(cinta, tabla, **kw)


def costo_esperado(k):
    return 2 * k + 2


def suma_bits(n):
    """s2(n): cantidad de unos en la representacion binaria de n."""
    return bin(n).count("1")


def total_exacto(n):
    """Pasos totales de n incrementos seguidos desde 0: T(n) = 4n - 2 s2(n) (se demuestra en el informe)."""
    return 4 * n - 2 * suma_bits(n)
