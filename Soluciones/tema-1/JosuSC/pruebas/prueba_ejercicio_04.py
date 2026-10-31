#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Ejercicio 4 - Casos de prueba
El contador binario en una máquina de Turing y su costo amortizado.

En vez de confiar en las fórmulas, se SIMULA la máquina de la sección 2
(cinta, cabezal, estados y las 7 transiciones) y se comprueba:

  1. Que cada incremento deja el valor correcto y el cabezal de vuelta en b0.
  2. Que el costo de un incremento con t unos consecutivos es 2t+2 (y 1 si t=0).
  3. Que el costo amortizado con el potencial Phi = 2*popcount nunca pasa de 4.
  4. Que la suma total coincide con la fórmula exacta de la sección 7:
     3m + piso(m/2) - 2*popcount(m).
  5. Que el peor incremento entre los primeros m es Theta(log m).

Ejecutar:  python3 prueba_ejercicio_04.py
Solo usa la biblioteca estándar.
"""

def popcount(x):
    return bin(x).count("1")


def unos_finales(v):
    """Cantidad de unos consecutivos desde el bit menos significativo."""
    t = 0
    while (v >> t) & 1:
        t += 1
    return t


def incrementar_mt(cinta, pos):
    """Un incremento sobre la cinta (dict posicion -> bit; ausente = blanco).
    Devuelve (posicion_final, pasos). Estados: s = start, c = carry, b = back."""
    pasos = 0
    estado = "s"
    while estado != "h":
        simbolo = cinta.get(pos)        # None = blanco
        pasos += 1
        if estado == "s":
            if simbolo == 0:                       # escribir 1 y detenerse
                cinta[pos] = 1
                estado = "h"
            else:                                  # era 1: escribir 0 y llevar
                cinta[pos] = 0
                pos += 1
                estado = "c"
        elif estado == "c":
            if simbolo == 1:
                cinta[pos] = 0
                pos += 1                            # sigue el acarreo
            else:                                  # 0 o blanco: escribir 1 y volver
                cinta[pos] = 1
                pos -= 1
                estado = "b"
        else:                                      # "b": retroceder hasta b0
            if simbolo is None:
                pos += 1                            # el blanco de la izquierda: paso a b0
                estado = "h"
            else:
                pos -= 1
    return pos, pasos


def valor(cinta):
    """El valor del contador escrito en la cinta (b0 es el bit menos significativo)."""
    v, p = 0, 0
    while cinta.get(p) is not None:
        v += cinta[p] << p
        p += 1
    return v


def main():
    cinta = {0: 0}                       # el contador empieza en 0: un solo 0 en b0
    pos = 0
    suma = 0
    peor_individual = 0
    m_final = 4096

    for i in range(1, m_final + 1):
        antes = valor(cinta)
        t = unos_finales(antes)

        pos, pasos = incrementar_mt(cinta, pos)
        suma += pasos
        peor_individual = max(peor_individual, pasos)

        # 1) valor correcto y cabezal en b0
        assert pos == 0, (i, pos)
        assert valor(cinta) == i, (i, valor(cinta))

        # 2) el costo por transiciones coincide con la cuenta de la sección 3
        esperado = 1 if t == 0 else 2 * t + 2
        assert pasos == esperado, (antes, t, pasos, esperado)

        # 3) costo amortizado con Phi = 2*popcount
        phi_antes = 2 * popcount(antes)
        phi_despues = 2 * popcount(i)
        amortizado = pasos + phi_despues - phi_antes
        assert amortizado <= 4, (antes, amortizado)

        # 4) la fórmula exacta de la sección 7
        assert suma == 3 * i + i // 2 - 2 * popcount(i), (i, suma)

    # 5) el peor incremento entre los m: 2*floor(log2(m-1)) + 2 = Theta(log m)
    #    (el valor 4095 = 111111111111_2 tiene 12 unos consecutivos)
    assert peor_individual == 2 * 12 + 2

    # la cota global: suma <= 4m, y tambien suma >= m
    assert m_final <= suma <= 4 * m_final

    print("ejercicio 4: todo correcto (máquina de Turing simulada, no fórmulas)")
    print(f"  {m_final} incrementos desde 0, todos con valor y cabezal correctos")
    print("  costo por incremento = 2t+2 (o 1 si t=0) en todos los casos")
    print("  costo amortizado con Phi = 2*popcount: nunca pasa de 4")
    print(f"  suma exacta = 3m + piso(m/2) - 2*popcount(m): {suma} para m = {m_final}")
    print(f"  peor incremento individual: {peor_individual} pasos (en 4095 -> 4096), Theta(log m)")
    for m in (10, 100, 1000, 4096):
        print(f"    m = {m:5d}:  total = {3 * m + m // 2 - 2 * popcount(m):6d}  (cota 4m = {4 * m})")


if __name__ == "__main__":
    main()
