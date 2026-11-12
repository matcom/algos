## 8.  Elementos que aparecen más de $n/3$ veces (C3)

Hay a lo sumo dos (tres de ellos sumarían más de $n$ apariciones).

**Algoritmo** (Boyer-Moore con dos candidatos; es el caso $k = 3$ de Misra-Gries, ejercicio 2 de C3):

```python
def frecuentes(A, verificar=True):
    c1 = c2 = None
    k1 = k2 = 0
    for x in A:
        if x == c1:   k1 += 1
        elif x == c2: k2 += 1
        elif k1 == 0: c1, k1 = x, 1
        elif k2 == 0: c2, k2 = x, 1
        else:         k1 -= 1; k2 -= 1        # tachar el trío {c1, c2, x}
    cand = {c for c, k in ((c1, k1), (c2, k2)) if k > 0}
    if not verificar:
        return cand                           # la versión con atajo
    return {c for c in cand if 3 * A.count(c) > len(A)}
```

Nota: un candidato con contador 0 puede volver a sumar (`x == c1` con `k1 == 0`); eso equivale a reasignarlo al mismo valor, así que no molesta.

**El invariante que uno escribe primero** ("si algo aparece más de $i/3$ veces en el prefijo, es candidato") es verdadero pero no inductivo, por la misma razón que en C3 §4: cuando el prefijo no tiene frecuentes, la hipótesis no dice nada.

**Invariante reforzado.** Después de procesar $A[1..i]$:

> $c_1 \ne c_2$, y el prefijo se puede partir en **tríos de tres elementos distintos entre sí**, más $k_1$ copias de $c_1$, más $k_2$ copias de $c_2$.

- *Inicialización.* Prefijo vacío, $k_1 = k_2 = 0$, y `None` $\ne$ `None` no hace falta porque los contadores son 0 (o se toma la convención de que dos candidatos vacíos no cuentan).
- *Mantenimiento*, una rama por caso:
  - $x = c_1$: una copia más de $c_1$. Igual con $c_2$.
  - $x \ne c_1, c_2$ y $k_1 = 0$: el candidato 1 pasa a ser $x$ con una copia. Sigue $c_1 \ne c_2$ porque $x \ne c_2$. Igual con $k_2 = 0$, usando $x \ne c_1$.
  - $x \ne c_1, c_2$ y $k_1, k_2 \ge 1$: se forma el trío $\{c_1, c_2, x\}$ con una copia de cada candidato. Es un trío de distintos porque $c_1 \ne c_2$ y $x$ es distinto de los dos. Los contadores bajan en 1.

  Los candidatos solo se reasignan a un $x$ distinto del otro candidato, así que $c_1 \ne c_2$ se mantiene.
- *Conclusión.* Sea $v$ con más de $n/3$ apariciones. Si $v$ no fuera un candidato con contador positivo, todas sus copias estarían en tríos, a lo sumo una por trío, y hay $(n - k_1 - k_2)/3 \le n/3$ tríos. Contradicción. **Teorema: si $v$ aparece más de $n/3$ veces, $v$ es candidato con contador positivo.** $\square$

La segunda pasada cuenta los (a lo sumo dos) candidatos y se queda con los que superan $n/3$; por el teorema no se pierde ninguno. Tiempo $O(n)$, memoria $O(1)$.

**La versión sin verificar** devuelve los candidatos con contador positivo. Leyendo la hipótesis del teorema (C3 §5): dice que los frecuentes *están* entre los candidatos, pero no dice nada sobre candidatos que no sean frecuentes. Ese es el error: falsos positivos. El contraejemplo mínimo es `A A B` ($n = 3$): termina con $c_1 = $ A, $k_1 = 2$, $c_2 = $ B, $k_2 = 1$, y devuelve {A, B}, pero B aparece una vez, que no es más de 1.

**Por qué el generador binario sí la atrapa.** Con dos símbolos, en cuanto los dos ocupan los dos lugares, la tercera rama no se ejecuta nunca: los contadores no bajan y son **exactamente las frecuencias**. La versión sin verificar devuelve todos los símbolos presentes, y falla cada vez que uno de ellos aparece $\le n/3$ veces. Es lo contrario de lo que pasaba en C3, donde con dos símbolos el atajo era correcto. Tampoco sirve el análogo de "mayoría plantada" con un solo frecuente: `A A B` es justo una de esas entradas.

**Un generador que no la atrapa: plantar dos frecuentes.** Si dos valores aparecen cada uno más de $n/3$ veces, el teorema dice que los dos son candidatos con contador positivo, y como hay solo dos lugares, *son* los dos candidatos. La salida sin verificar coincide con el oráculo siempre. El generador tiene que plantar tantos frecuentes como lugares tiene el algoritmo.

```python
def dos_plantados(n):
    a, b = random.sample("ABCDE", 2)
    q = n // 3 + 1
    A = [a] * q + [b] * q + [random.choice("ABCDE") for _ in range(n - 2 * q)]
    random.shuffle(A)
    return A
```

Medido sobre 4000 arreglos de largo 3 a 15 por generador (fallos de la versión sin verificar; la versión con verificación falla 0 % en todos):

| generador | fallos sin verificar |
|---|---|
| un frecuente plantado | ≈ 55 % |
| **dos frecuentes plantados** | **0 %** |
| binario | ≈ 41 % |
| 3 símbolos | ≈ 42 % |
| 5 símbolos | ≈ 58 % |

---
