# Ejercicio 14 — El ciclo completo sobre un problema nuevo

> **Enunciado.** Escoge un problema que no hayamos visto, recorre el ciclo completo de
> la conferencia 2 sobre él y consigue que el algoritmo y la cota mínima coincidan. Es
> el formato de la pregunta larga del examen final.

El ciclo de la conferencia 2 (C2, §1) son cinco preguntas: **qué es el problema**, **qué
algoritmo lo resuelve**, **si es correcto**, **cuánto cuesta** y **si se puede hacer
mejor**. Las recorro de principio a fin sobre un problema que no salió en el curso, y
cierro con algoritmo y cota mínima coincidiendo en $\Theta(n)$.

**Problema escogido: la máxima suma de un subarreglo contiguo** (problema de Kadane /
*maximum subarray*). No apareció en ninguna de las cinco conferencias.

---

## 1. ¿Qué es el problema? (con su modelo)

**Máxima suma de subarreglo.** Dado un arreglo $A[0..n-1]$ de $n$ números reales
(posiblemente negativos), devolver
$$\mathrm{OPT}(A) \;=\; \max_{0 \le i \le j \le n}\ \sum_{k=i}^{j-1} A[k],$$
la mayor suma sobre todos los subarreglos **contiguos**. Admitimos el subarreglo vacío
(suma $0$), de modo que $\mathrm{OPT}(A)\ge 0$; la variante sin vacío es idéntica salvo
el caso de todos negativos.

**Modelo de cómputo.** Para el algoritmo, la word-RAM (C1, §4): sumar y comparar reales
cuesta $O(1)$. Para la cota mínima usaremos el modelo de **árboles de decisión
algebraicos** (C2, §8; C5), donde el costo es el número de pruebas de signo de
polinomios sobre la entrada —el mismo modelo en que se prueba la cota del par más
cercano.

```
  A = [ -2,  1, -3,  4, -1,  2,  1, -5,  4 ]
                      └──────────────┘
                      subarreglo [4,-1,2,1] = 6  = OPT
```

---

## 2. ¿Qué algoritmo? (el ciclo completo, C2 §4–§7)

Recorro el mismo arco que el par más cercano en C2: fuerza bruta, una mejora, y el
algoritmo final.

- **Fuerza bruta (C2, §4).** Probar los $\binom{n+1}{2}$ subarreglos y sumar cada uno:
  $O(n^3)$, o $O(n^2)$ con sumas acumuladas. Correcto pero caro.
- **Divide y vencerás (como C2, §5).** Partir por la mitad; el óptimo está entero a la
  izquierda, entero a la derecha, o **cruza el centro**. El que cruza se calcula en
  $O(n)$ extendiendo desde el centro hacia ambos lados. Recurrencia
  $T(n)=2T(n/2)+O(n)=O(n\log n)$. Es el análogo exacto del "par que cruza la franja".
- **Kadane, el algoritmo final (incremental, $O(n)$).** Recorrer el arreglo una vez
  manteniendo la mejor suma de un subarreglo **que termina en la posición actual**.

```python
def kadane(A):
    mejor = 0          # mejor suma global vista (subarreglo vacío permitido)
    aqui = 0           # mejor suma de un subarreglo que termina en el índice actual
    for x in A:
        aqui = max(0, aqui + x)   # o empiezo de nuevo (vacío) o extiendo
        mejor = max(mejor, aqui)
    return mejor

if __name__ == "__main__":
    print(kadane([-2, 1, -3, 4, -1, 2, 1, -5, 4]))   # [4,-1,2,1] = 6
    print(kadane([-3, -1, -2]))                       # todos negativos -> vacío = 0
    print(kadane([1, 2, 3, 4]))                        # todo el arreglo = 10
```

```
6
0
10
```

---

## 3. ¿Es correcto? (invariante, C3 §4)

Kadane es un ciclo, así que lo correcto se demuestra con un **invariante inductivo**
(C3, §1: correctitud parcial + terminación).

**Invariante.** Justo después de procesar $A[0..t-1]$:
- `aqui` $=\displaystyle\max\Big(0,\ \max_{0\le i\le t}\sum_{k=i}^{t-1}A[k]\Big)$ = mejor
  suma de un subarreglo que **termina en $t$** (o vacío);
- `mejor` $=\displaystyle\max_{0\le i\le j\le t}\sum_{k=i}^{j-1}A[k]$ = óptimo del
  prefijo $A[0..t-1]$.

*Inicialización ($t=0$):* `aqui = mejor = 0`, correcto (solo el subarreglo vacío).

*Mantenimiento:* supongamos el invariante tras $t$, procesamos $A[t]$. Un subarreglo que
termina en $t+1$ es vacío, o es (un subarreglo que termina en $t$) seguido de $A[t]$.
Su mejor suma es $\max(0,\ \texttt{aqui}+A[t])$, que es justo la nueva `aqui`. Y el
óptimo del prefijo $A[0..t]$ es, o bien el óptimo de $A[0..t-1]$ (la vieja `mejor`), o
bien un subarreglo que termina en $t+1$ (la nueva `aqui`); `mejor = max(mejor, aqui)`
toma el mayor. El invariante se mantiene.

*Conclusión:* tras $t=n$, `mejor` $=\mathrm{OPT}(A)$. $\square$

*Terminación:* el ciclo recorre una lista finita de $n$ elementos.

La clave es que el invariante es **inductivo**, no solo verdadero al final (C3, §4,
Boyer-Moore): `aqui` carga exactamente la información que hace falta para que el paso
$t\to t+1$ se sostenga sin volver a mirar el pasado.

---

## 4. ¿Cuánto cuesta? (C1, C4)

Un solo recorrido, trabajo $O(1)$ por elemento (una suma, dos `max`): **$\Theta(n)$
tiempo**, **$O(1)$ memoria** adicional. No hay nada amortizado aquí: el costo es $O(1)$
peor caso por iteración, exacto. Lo medimos contando operaciones (sumas + comparaciones),
que es exactamente $3n$ y no depende del contenido del arreglo:

```python
def kadane_con_cuenta(A):
    mejor = 0
    aqui = 0
    ops = 0
    for x in A:
        aqui = max(0, aqui + x)    # 1 suma + 1 comparación
        mejor = max(mejor, aqui)   # 1 comparación
        ops += 3
    return mejor, ops

if __name__ == "__main__":
    print(f"{'n':>7} {'operaciones':>12} {'ops/n':>7}")
    for n in [1000, 2000, 4000, 8000]:
        _, ops = kadane_con_cuenta(list(range(-n // 2, n // 2)))
        print(f"{n:>7} {ops:>12} {ops // n:>7}")
```

```
      n  operaciones   ops/n
   1000         3000       3
   2000         6000       3
   4000        12000       3
   8000        24000       3
```

Exactamente $3n$ operaciones en todos los casos: trabajo constante por elemento, total
$\Theta(n)$, sin dependencia de la entrada (peor caso = caso promedio aquí).

---

## 5. ¿Se puede hacer mejor? La cota mínima (C5, C2 §8)

**Teorema.** Todo algoritmo que resuelve la máxima suma de subarreglo debe **leer las
$n$ entradas**, luego requiere $\Omega(n)$. En particular, en el modelo de árboles de
decisión algebraicos (y en cualquier modelo donde una celda no leída no influye en la
salida), el costo es $\Omega(n)$.

*Demostración, por adversario (C5, §1 "el adversario cuenta trabajo").* El adversario
mantiene las respuestas a las pruebas del algoritmo consistentes con **más de una**
respuesta final, hasta que el algoritmo haya tocado las $n$ celdas.

Supongamos que un algoritmo correcto se detiene habiendo **ignorado** la celda $A[p]$.
Construyo dos entradas que coinciden en todo salvo en $A[p]$ y que el algoritmo no puede
distinguir (nunca miró $A[p]$), pero que tienen **distinto** $\mathrm{OPT}$:

- $A[k]=0$ para todo $k\ne p$. Entonces $\mathrm{OPT}$ depende solo de $A[p]$:
  - si $A[p]=+1$: el mejor subarreglo es $[p,p{+}1)$, $\mathrm{OPT}=1$;
  - si $A[p]=-1$: ningún subarreglo no vacío mejora el vacío, $\mathrm{OPT}=0$.

El algoritmo, no habiendo leído $A[p]$, toma el mismo camino en el árbol de decisión y
da la misma salida para ambas entradas. Pero una exige $1$ y la otra $0$: en al menos
una se equivoca. Contradicción con que sea correcto. Luego todo algoritmo correcto lee
las $n$ celdas, y $\Omega(n)$. $\square$

```
  dos entradas que el adversario deja indistinguibles si no se lee A[p]:
     A⁺ = [0, 0, …,  +1 , …, 0]   OPT = 1   (el subarreglo {p})
     A⁻ = [0, 0, …,  -1 , …, 0]   OPT = 0   (solo el vacío)
                      ↑ p
  un algoritmo que no mira A[p] responde igual a ambas ⇒ se equivoca en una.
```

```python
if __name__ == "__main__":
    # El adversario, hecho código: si un "algoritmo" ignora una celda, falla.
    def kadane_tramposo_ignora(A, p):      # ignora A[p] (p. ej. lo trata como 0)
        B = list(A); B[p] = 0
        return kadane(B)

    n, p = 7, 3
    masA = [0] * n; masA[p] = 1            # OPT = 1
    menosA = [0] * n; menosA[p] = -1       # OPT = 0
    print("correcto  A+:", kadane(masA),   " A-:", kadane(menosA))
    print("tramposo  A+:", kadane_tramposo_ignora(masA, p),
          " A-:", kadane_tramposo_ignora(menosA, p),
          " <- da lo mismo en ambas: por eso falla en A+")
```

```
correcto  A+: 1  A-: 0
tramposo  A+: 0  A-: 0  <- da lo mismo en ambas: por eso falla en A+
```

---

## 6. Algoritmo y cota coinciden

| pregunta (C2 §1) | respuesta |
|---|---|
| ¿qué es? | máxima suma de subarreglo contiguo, $A\in\mathbb R^n$ |
| ¿qué algoritmo? | Kadane, incremental en un recorrido |
| ¿es correcto? | invariante inductivo sobre `aqui`/`mejor` (C3 §4) |
| ¿cuánto cuesta? | $\Theta(n)$ tiempo, $O(1)$ memoria |
| ¿se puede mejor? | no: $\Omega(n)$ por adversario (hay que leer toda la entrada) |

**Cierre.** Cota inferior $\Omega(n)$ y algoritmo $O(n)$ coinciden: Kadane es
**óptimo**, y no por casualidad —el límite inferior es el trivial "hay que mirar la
entrada", y Kadane la mira exactamente una vez. Es la forma de respuesta completa que
describe C2 §10 / el resumen del Tema 1: enunciado con su modelo, algoritmo, invariante
con sus pasos, terminación, costo exacto, y cota mínima con su modelo y su adversario.

> **Por qué este problema cierra limpio.** A diferencia del par más cercano —donde el
> algoritmo algebraico ($n\log n$) coincide con la cota algebraica, pero un modelo más
> rico (parte entera + hash) la rompe (C2, §9; y el ejercicio 10)— aquí la cota es la
> trivial $\Omega(n)$ de "leer la entrada", que **ningún modelo puede esquivar**: una
> celda no leída se puede cambiar sin que el algoritmo lo note. Por eso algoritmo y cota
> coinciden de forma estable, sin el matiz de "depende del modelo".

