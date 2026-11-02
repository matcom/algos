import math

# Ejercicio 4, Tema 1: contador binario en una maquina de Turing.
#
# La cinta es: '#' (marca del borde izquierdo), despues los bits del numero
# con el bit menos significativo primero, y despues blancos '_'.
#
# Maquina (dos estados):
#   sumar:  lee '1' -> escribe '0', se mueve a la derecha     (acarreo)
#           lee '0' o '_' -> escribe '1', izquierda, pasa a volver
#   volver: lee '0' o '1' -> izquierda
#           lee '#' -> derecha y termina (queda en el bit menos significativo)
#
# Potencial: phi = 2 * (cantidad de unos en la cinta)


def incrementar(cinta):
    """Suma 1 al numero de la cinta. Devuelve la cantidad de pasos de la maquina."""
    pos = 1                                   # empieza en el bit menos significativo
    estado = "sumar"
    pasos = 0
    while estado != "fin":
        pasos += 1
        if pos == len(cinta):
            cinta.append("_")                 # la cinta es infinita hacia la derecha
        s = cinta[pos]
        if estado == "sumar":
            if s == "1":
                cinta[pos] = "0"
                pos += 1
            else:                             # '0' o blanco
                cinta[pos] = "1"
                pos -= 1
                estado = "volver"
        else:                                 # volver
            if s == "#":
                pos += 1
                estado = "fin"
            else:
                pos -= 1
    assert pos == 1                           # termino en el bit menos significativo
    return pasos


def potencial(cinta):
    return 2 * cinta.count("1")


def unos_finales(i):
    """Cantidad de unos al final de i en binario (los que se cambian por ceros)."""
    k = 0
    while i & 1:
        k += 1
        i >>= 1
    return k


def valor(cinta):
    return sum(2 ** j for j, b in enumerate(cinta[1:]) if b == "1")


if __name__ == "__main__":
    # tabla con los primeros incrementos
    cinta = ["#", "0"]                        # el numero 0
    print("Primeros incrementos")
    print(f"{'i->i+1':>7} {'k':>2} {'costo real':>11} {'phi antes':>10} "
          f"{'phi despues':>12} {'amortizado':>11}")
    for i in range(8):
        antes = potencial(cinta)
        k = unos_finales(i)
        c = incrementar(cinta)
        despues = potencial(cinta)
        assert c == 2 * k + 2                 # costo real de un incremento
        print(f"{str(i) + '->' + str(i + 1):>7} {k:>2} {c:>11} {antes:>10} "
              f"{despues:>12} {c + despues - antes:>11}")
    print()

    # n incrementos desde 0
    print(f"{'n':>8} {'pasos totales':>14} {'4n - 2s(n)':>11} {'pasos/n':>8} "
          f"{'mas caro':>9} {'2*log2(n)+2':>12}")
    for n in [10, 100, 1000, 10_000, 100_000]:
        cinta = ["#", "0"]
        total = peor = 0
        for i in range(n):
            antes = potencial(cinta)
            c = incrementar(cinta)
            assert c + potencial(cinta) - antes == 4      # amortizado = 4 siempre
            total += c
            peor = max(peor, c)
        assert valor(cinta) == n
        s = bin(n).count("1")                 # unos de n en binario
        assert total == 4 * n - 2 * s
        cota = 2 * int(math.log2(n)) + 2
        assert peor == cota
        print(f"{n:>8} {total:>14} {4 * n - 2 * s:>11} {total / n:>8.2f} "
              f"{peor:>9} {cota:>12}")
