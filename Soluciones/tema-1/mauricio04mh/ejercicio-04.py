"""Ejercicio 4. Contador binario en una máquina de Turing: costo amortizado."""


def incremento(cinta, cabezal):
    """Un incremento. cinta: dict posición -> '0'/'1'; el LSB está en la posición 0
    y los bits más significativos en -1, -2, ... Devuelve (cabezal, pasos)."""
    estado, pasos = "inc", 0
    while estado != "alto":
        s = cinta.get(cabezal, "_")
        pasos += 1
        if estado == "inc":
            if s == "1":
                cinta[cabezal] = "0"; cabezal -= 1
            else:                                   # '0' o blanco
                cinta[cabezal] = "1"; cabezal += 1; estado = "ret"
        else:                                       # ret
            if s == "_":
                cabezal -= 1; estado = "alto"
            else:
                cabezal += 1
    return cabezal, pasos


def valor(cinta):
    bits = [cinta.get(p, "_") for p in range(min(cinta) if cinta else 0, 1)]
    return int("".join(b for b in bits if b != "_") or "0", 2)


if __name__ == "__main__":
    cinta, cab, total = {}, 0, 0
    print(f"{'m':>3} {'valor antes':>11} {'t':>2} {'pasos':>5} {'acumulado':>9} {'4m-2*s2(m)':>10}")
    for m in range(1, 9):
        antes = valor(cinta)
        t = (antes ^ (antes + 1)).bit_length() - 1      # unos finales de 'antes'
        cab, pasos = incremento(cinta, cab)
        assert cab == 0 and pasos == 2 * t + 2
        total += pasos
        formula = 4 * m - 2 * bin(m).count("1")
        assert total == formula
        print(f"{m:>3} {antes:>11} {t:>2} {pasos:>5} {total:>9} {formula:>10}")

    # Muchas operaciones: la fórmula exacta y el costo por incremento
    cinta, cab, total, peor = {}, 0, 0, 0
    print()
    for m in range(1, 2**16 + 1):
        cab, pasos = incremento(cinta, cab)
        total += pasos
        peor = max(peor, pasos)
        assert total == 4 * m - 2 * bin(m).count("1")
        if m in (10, 1000, 2**12, 2**16):
            print(f"m = {m:>6}: total = {total:>7}, total/m = {total / m:.3f}, "
                  f"incremento más caro hasta ahora = {peor} pasos")
