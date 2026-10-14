def incrementar_contador(contador):
    """Incrementa el contador binario (lista de bits, LSB al final).
    Devuelve el número de bits que cambiaron."""
    cambios = 0
    i = len(contador) - 1
    while i >= 0 and contador[i] == 1:
        contador[i] = 0
        cambios += 1
        i -= 1
    if i >= 0:
        contador[i] = 1
        cambios += 1
    else:
        contador.insert(0, 1)
        cambios += 1
    return cambios

def main():
    print(f"{'m':>8} {'bits cambiados':>16} {'m':>10} {'m log2 m':>12}")
    for m in [10, 100, 1000, 10000, 100000]:
        bits = (m.bit_length() + 1)
        contador = [0] * bits
        total = 0
        for _ in range(m):
            total += incrementar_contador(contador)
        print(f"{m:>8} {total:>16} {m:>10} {m * (m.bit_length()):>12}")

if __name__ == "__main__":
    main()
