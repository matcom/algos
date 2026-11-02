"""Ejercicio 4: el contador binario en una máquina de Turing de una cinta.

Corre: python ejercicio-04.py  (simula m incrementos, vigila el potencial en cada uno,
compara con la versión con el cabezal en el bit más significativo y genera la figura)
"""
B = " "   # el blanco

# Incremento con el cabezal en el bit menos significativo (LSB), número escrito como
# siempre: el bit más significativo a la izquierda. (estado, símbolo) -> (escribe, mueve, estado)
INCREMENTAR = {
    ("acarreo", "1"): ("0", -1, "acarreo"),   # 1 + acarreo = 0, y el acarreo sigue a la izquierda
    ("acarreo", "0"): ("1", +1, "volver"),    # 0 + acarreo = 1, se terminó el acarreo
    ("acarreo", B):   ("1", +1, "volver"),    # el número crece un bit
    ("volver", "0"):  ("0", +1, "volver"),
    ("volver", "1"):  ("1", +1, "volver"),
    ("volver", B):    (B, -1, "fin"),         # pasó el LSB: un paso atrás y queda sobre él
}

# La misma suma, pero con el cabezal empezando y terminando en el bit más significativo (MSB).
INCREMENTAR_DESDE_MSB = {
    ("ir", "0"): ("0", +1, "ir"), ("ir", "1"): ("1", +1, "ir"),
    ("ir", B):   (B, -1, "acarreo"),          # llegó al LSB
    ("acarreo", "1"): ("0", -1, "acarreo"),
    ("acarreo", "0"): ("1", -1, "volver"),
    ("acarreo", B):   ("1", -1, "volver"),    # el número creció: el 1 nuevo es el MSB
    ("volver", "0"): ("0", -1, "volver"), ("volver", "1"): ("1", -1, "volver"),
    ("volver", B):   (B, +1, "fin"),
}


def correr(maquina, cinta, cabezal, estado):
    """Ejecuta hasta el estado 'fin'. La cinta es un dict posición -> símbolo. Devuelve (cabezal, pasos)."""
    pasos = 0
    while estado != "fin":
        escribe, mueve, estado = maquina[(estado, cinta.get(cabezal, B))]
        cinta[cabezal] = escribe
        cabezal += mueve
        pasos += 1
    return cabezal, pasos


def leer(cinta):
    """El número escrito en la cinta, ignorando los blancos."""
    s = "".join(cinta[p] for p in sorted(cinta)).strip()
    return int(s, 2)


def unos(cinta):
    return sum(1 for v in cinta.values() if v == "1")


def unos_finales(v):
    """Cantidad de unos al final de bin(v): los bits que el acarreo pone en 0."""
    t = 0
    while v & 1:
        v >>= 1; t += 1
    return t


def contar(maquina, m, estado_inicial, vigilar=False, en_msb=False):
    """m incrementos desde 0. El 0 se escribe como "0" con el cabezal encima. Devuelve los costos."""
    cinta, cabezal, costos = {0: "0"}, 0, []
    for k in range(m):
        if en_msb:
            assert cinta.get(cabezal) != B and cinta.get(cabezal - 1, B) == B   # el cabezal está en el MSB
        phi_antes = 2 * unos(cinta)
        lsb_antes = max(p for p, v in cinta.items() if v != B)
        cabezal, c = correr(maquina, cinta, cabezal, estado_inicial)
        costos.append(c)
        assert leer(cinta) == k + 1                           # suma bien
        if vigilar:
            assert cabezal == lsb_antes                       # el cabezal volvió al LSB (que no se mueve)
            assert c == 2 * unos_finales(k) + 2               # costo real = 2(t + 1)
            assert c + 2 * unos(cinta) - phi_antes == 4       # costo amortizado con Φ = 2·(unos) = 4
    return costos


if __name__ == "__main__":
    # 1. Correctitud y potencial vigilados en cada incremento
    M = 5000
    costos = contar(INCREMENTAR, M, "acarreo", vigilar=True)
    print(f"{M} incrementos: suma bien, el cabezal vuelve al LSB y el amortizado es 4 en todos")

    # 2. Total exacto: 4m - 2·(unos de m), y el peor incremento
    print(f"\n{'m':>7} {'total':>8} {'4m - 2·unos(m)':>15} {'total/m':>8} {'peor incremento':>16} {'2·⌊log2 m⌋ + 2':>14}")
    for m in [1, 2, 7, 8, 100, 1000, 1024, 5000]:
        total = sum(costos[:m])
        exacto = 4 * m - 2 * bin(m).count("1")
        peor = max(costos[:m])
        assert total == exacto and total <= 4 * m
        assert peor == 2 * (m.bit_length() - 1) + 2            # el peor es el de 2^j - 1 a 2^j
        print(f"{m:>7} {total:>8} {exacto:>15} {total / m:>8.3f} {peor:>16} {2 * (m.bit_length() - 1) + 2:>14}")

    # 3. El cabezal en el MSB: la misma suma cuesta Θ(log m) cada vez
    print(f"\n{'m':>7} {'total LSB':>10} {'total MSB':>10} {'MSB / m':>8} {'log2 m':>7}")
    for m in [8, 64, 512, 4096]:
        lsb = sum(contar(INCREMENTAR, m, "acarreo"))
        msb = contar(INCREMENTAR_DESDE_MSB, m, "ir", en_msb=True)
        assert all(c >= 2 * max(k.bit_length(), 1) for k, c in enumerate(msb))   # recorre el número dos veces
        print(f"{m:>7} {lsb:>10} {sum(msb):>10} {sum(msb) / m:>8.2f} {m.bit_length() - 1:>7}")

    # 4. Figura
    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
    except ImportError:
        print("\n(sin matplotlib: no se genera la figura)")
    else:
        m = 64
        c, acum = costos[:m], []
        for x in c:
            acum.append((acum[-1] if acum else 0) + x)
        fig, axs = plt.subplots(1, 2, figsize=(10, 3.8))
        axs[0].bar(range(1, m + 1), c, color="#93c5fd", label="costo real")
        axs[0].axhline(4, c="#dc2626", lw=1.5, label="amortizado = 4")
        axs[0].set_xlabel("incremento k"); axs[0].set_ylabel("pasos")
        axs[0].set_title("Pasos de cada incremento")
        axs[0].legend()
        axs[1].plot(range(1, m + 1), acum, c="#2563eb", label="total real")
        axs[1].plot(range(1, m + 1), [4 * k for k in range(1, m + 1)], "--", c="#dc2626", label="4m")
        axs[1].set_xlabel("m"); axs[1].set_ylabel("pasos acumulados")
        axs[1].set_title("Total de m incrementos")
        axs[1].legend()
        fig.tight_layout()
        fig.savefig("ejercicio-04-contador.png", dpi=150)
        print("\nfigura: ejercicio-04-contador.png")
