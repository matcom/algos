# Ejercicio 2: invariante, potencial y cota de la búsqueda binaria

> Da el invariante y el potencial de la búsqueda binaria, y la cota de información que la hace óptima. (C3, C5)

## El algoritmo

```python
def busqueda_binaria(A, x):     # precondición: A está ordenado
    lo, hi = 0, len(A)
    while lo < hi:
        m = (lo + hi) // 2
        if A[m] == x:
            return m             # lo encontré
        if x < A[m]:
            hi = m               # x solo puede estar a la izquierda de m
        else:
            lo = m + 1           # x solo puede estar a la derecha de m
    return -1                    # no está
```

El rango donde busca es A[lo], …, A[hi − 1]: `hi` no se incluye. Ese rango tiene hi − lo elementos.

## Invariante

> Si x está en A, entonces está entre A[lo] y A[hi − 1].


**Inicialización.** Al principio lo = 0 y hi = len(A): el rango es el arreglo entero. Si x está en A, está entre el inicio y el final de A.

**Mantenimiento.** Supongo el invariante al empezar una vuelta. Si A[m] = x, el algoritmo devuelve m y termina. Si no, hay dos casos:

- **x < A[m]**, y el algoritmo hace hi = m. Como A está ordenado, los elementos a partir de A[m] son mayores o iguales que A[m], y como x < A[m], x es menor que A[m], A[m + 1], A[m + 2], etc. Ninguno puede ser x. Entonces, si x está en A, por el invariante estaba en A[lo..hi − 1], y como no está en A[m..hi − 1], está en A[lo..m − 1], que es el rango nuevo.
- **x > A[m]**, y el algoritmo hace lo = m + 1. Lo mismo, al revés: los elementos anteriores son menores o iguales que A[m] < x, así que ninguno es x. Si x está en A, está en A[m + 1..hi − 1].

**Conclusión.** El algoritmo termina de dos formas. Si devuelve m es porque A[m] = x: correcto. Si sale del `while` es porque lo ≥ hi, y el rango A[lo..hi − 1] tiene hi − lo ≤ 0 elementos: está vacío. Por el invariante, si x estuviera en A estaría en ese rango, así que x no está en A



## Potencial

> Φ = hi − lo, el tamaño del rango.

Es entero, empieza en n = len(A) y dentro del ciclo es positivo (lo < hi). Baja en cada vuelta:

- Primero, **lo ≤ m < hi**. m está entre lo y hi, y nunca es igual a hi: como lo < hi, lo ≤ hi − 1, y entonces m = ⌊(lo + hi)/2⌋ ≤ ⌊(2hi − 1)/2⌋ <= hi − 1/2 < hi.
- Si hi = m: el nuevo potencial es m − lo, y como m < hi, m − lo < hi − lo.
- Si lo = m + 1: m es al menos lo, entonces m + 1 es siempre mayor que lo, y el nuevo potencial hi − (m + 1) < hi − lo.

Un entero no negativo que baja al menos 1 en cada vuelta no puede bajar para siempre, así que el ciclo termina, en a lo sumo n vueltas.

## Cota de información: por qué es óptima

Modelo: el algoritmo solo puede comparar x con elementos de A, y cada comparación cuesta 1.


**Los huecos.** Si x no está en A, cae en uno de los espacios entre elementos consecutivos, antes del primero o después del último. Con n elementos hay **n + 1 huecos**. Con A = [10, 20, 30]:

```
  (antes del 10)  10  (entre 10 y 20)  20  (entre 20 y 30)  30  (después del 30)
```

Cuando x cae en un hueco, ninguna comparación puede responder "igual", así que cada comparación tiene solo dos respuestas, menor o mayor

Para responder "no está" con seguridad, el algoritmo tiene que saber en qué hueco cae x. Si solo sabe, por ejemplo, "x está entre 10 y 30", no puede responder: x podría ser 15 (no está) o 20 (sí está). En cambio, si sabe "x es mayor que 20 y menor que 30", puede responder que x no está, porque entre 20 y 30 no hay elementos de A.

Más precisamente: el algoritmo no ve x, solo ve las respuestas a sus comparaciones, así que con las mismas respuestas hace lo mismo y responde lo mismo. Si con k comparaciones hay más huecos que listas de respuestas posibles (2ᵏ < n + 1), dos huecos distintos reciben la misma lista. Ejemplo con [10, 20, 30] y un algoritmo que solo compara con el 30: x = 5, x = 15 y x = 25 reciben todos "menor", y el algoritmo dice "no está" en los tres. Entre esos huecos están el 10 y el 20, con los que nunca comparó.

**Conclusión.** Todo algoritmo correcto cumple 2ᵏ ≥ n + 1, o sea, hace al menos **⌈log₂(n + 1)⌉** comparaciones en el peor caso. La búsqueda binaria hace exactamente esa cantidad, así que es **óptima** en el modelo de comparaciones.

## Experimentos

`ej02_busqueda_binaria.py` corre la búsqueda con el invariante, el potencial y la conclusión comprobados con `assert` en cada vuelta, en 5000 búsquedas al azar, sin fallos. Después mide el peor caso probando un x en cada hueco y cada elemento:

```
     n  peor caso medido   ⌈log2(n+1)⌉
     1                 1             1
     2                 2             2
     3                 2             2
     7                 3             3
     8                 4             4
    15                 4             4
   100                 7             7
  1000                10            10
  1023                10            10
  1024                11            11
```

El peor caso coincide exactamente con la cota en todos los tamaños.

---
*Declaración de uso de IA: usé un asistente de IA (Claude) para escribir el código de experimentación, y como tutor (explicaciones, pistas y corrección de mi redacción). Las demostraciones son mías.*
