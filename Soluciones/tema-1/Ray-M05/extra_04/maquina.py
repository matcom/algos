import sys

BLANCO = "_"


TRANSICIONES = {
    ("acarreo", "1"): ("0", -1, "acarreo"),
    ("acarreo", "0"): ("1", +1, "regreso"),
    ("acarreo", BLANCO): ("1", +1, "regreso"),
    ("regreso", "0"): ("0", +1, "regreso"),
    ("regreso", "1"): ("1", +1, "regreso"),
    ("regreso", BLANCO): (BLANCO, -1, "fin"),
}


def incrementar(cinta, traza=None):
    cabezal, estado, pasos = 0, "acarreo", 0
    while estado != "fin":
        escribe, mueve, estado = TRANSICIONES[(estado, cinta.get(cabezal, BLANCO))]
        cinta[cabezal] = escribe
        cabezal += mueve
        pasos += 1
        if traza is not None:
            traza.append((dict(cinta), cabezal, estado))
    assert cabezal == 0
    return pasos


def valor(cinta):
    bits = [cinta[p] for p in sorted(cinta) if cinta[p] != BLANCO]
    return int("".join(bits), 2)


def unos(cinta):
    return sum(s == "1" for s in cinta.values())


def unos_finales(v):
    t = 0
    while v & 1:
        v >>= 1
        t += 1
    return t


def contar(m):
    cinta = {0: "0"}
    costos, total = [], 0
    for i in range(1, m + 1):
        t = unos_finales(i - 1)
        c = incrementar(cinta)
        total += c
        assert valor(cinta) == i
        assert c == 2 * t + 2
        assert unos(cinta) == bin(i).count("1")
        assert total == 4 * i - 2 * bin(i).count("1")
        costos.append(c)
    return costos


def _verificacion():
    m = 1 << 16
    contar(m)
    print(f"El simulador corre los {m:,} primeros incrementos desde 0 y, en cada uno, "
          f"comprueba que la cinta vale lo que debe, que el incremento costó $2t + 2$ pasos y "
          f"que el total acumulado es exactamente $4m - 2\\,s(m)$. Ningún `assert` falla.")


SECCIONES = {
    "verificacion": _verificacion,
}

if __name__ == "__main__":
    SECCIONES[sys.argv[1]]()
