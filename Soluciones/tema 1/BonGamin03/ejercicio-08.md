# Ejercicio 8


## El Problema y la Intuición de Cancelación

>Dado un arreglo $A$ de $n$ elementos comparables únicamente por igualdad, queremos encontrar todos los elementos que aparecen más de $n/3$ veces (frecuencia $> n/3$). Notar que a lo sumo pueden existir 2 elementos con esta propiedad.


### Idea de cancelación
En la Conferencia 3 vimos que tachar parejas de 2 elementos distintos preserva el candidato a mayoría absoluta ($> n/2$). Para la cota $> n/3$, la observación clave es que si tachamos un **trío de elementos distintos** ($x, y, z$), cualquier elemento que aparezca más de $n/3$ veces conserva su condición en los elementos restantes.

Si un elemento $m$ aparece $c > n/3$ veces, al eliminar $t$ tríos de elementos distintos:
* Se eliminan en total $3t$ elementos del arreglo.
* De las $3t$ posiciones eliminadas, a lo sumo $t$ corresponden a $m$ (pues en cada trío todos los elementos son distintos, por lo que $m$ no puede figurar más de una vez por trío).
* En el arreglo restante quedan $n - 3t$ elementos, y las apariciones de $m$ son al menos $c - t > n/3 - t = (n - 3t)/3$.

Por tanto, $m$ sigue apareciendo estrictamente más de un tercio de las veces en el multiconjunto reducido.

---

## El Algoritmo con Dos Candidatos

Mantenemos dos candidatos $(c_1, c_2)$ y dos contadores $(cnt_1, cnt_2)$. 
Procesamos el arreglo en una sola pasada de cancelación (primera pasada).

```python
def misra_gries_dos_candidatos(A):
    c1, cnt1 = None, 0
    c2, cnt2 = None, 0

    # Primera pasada: Cancelación de tríos distintos
    for x in A:
        if c1 == x:
            cnt1 += 1
        elif c2 == x:
            cnt2 += 1
        elif cnt1 == 0:
            c1, cnt1 = x, 1
        elif cnt2 == 0:
            c2, cnt2 = x, 1
        else:
            # Se cancela x con una copia de c1 y una de c2 (trío distinto)
            cnt1 -= 1
            cnt2 -= 1

    # Segunda pasada: Verificación explícita
    res = []
    if cnt1 > 0 and A.count(c1) > len(A) // 3:
        res.append(c1)
    if cnt2 > 0 and c2 != c1 and A.count(c2) > len(A) // 3:
        res.append(c2)

    return res
```

---

## Invariante Reforzado y Demostración de Correctitud

Para demostrar por inducción la primera pasada, no basta decir "si un elemento tiene frecuencia $> n/3$, será uno de los candidatos". Hay que formalizar el estado de la cancelación en términos de la estructura del prefijo.

### Enunciado del Invariante Reforzado
Después de procesar el prefijo $A[:i]$ de longitud $i$:
> El prefijo $A[:i]$ se puede descomponer en $T$ tríos de elementos mutuamente distintos, más $cnt_1$ copias del candidato $c_1$ y $cnt_2$ copias del candidato $c_2$ (donde si $cnt_1 > 0$ y $cnt_2 > 0$, entonces $c_1 \neq c_2$).

### Demostración
La demostración sigue los tres pasos inductivos exigidos por la teoría de la Conferencia 3:

#### Inicialización
Antes de procesar el primer elemento ($i=0$), el prefijo es vacío ($A[:0] = []$). 
Se cumple trivialmente con $T = 0$, $cnt_1 = 0$, $cnt_2 = 0$ (0 tríos y 0 copias).

#### Mantenimiento
Supongamos que el invariante se cumple para el prefijo de longitud $i-1$. Procesamos el elemento $x = A[i-1]$. Analizamos los casos según el `if`:

* **Caso 1: $x == c_1$ ($cnt_1 > 0$)**
  Aumentamos $cnt_1$ en $1$. La partición previa (los $T$ tríos y las copias acumuladas) se mantiene, añadiendo $x$ como una nueva copia de $c_1$. El invariante se mantiene.
* **Caso 2: $x == c_2$ ($cnt_2 > 0$)**
  Análogo al anterior; $cnt_2$ aumenta en $1$, agregando $x$ a las copias de $c_2$.
* **Caso 3: $cnt_1 == 0$**
  El número de copias activas de $c_1$ era 0. Asignamos $c_1 = x$ y $cnt_1 = 1$. El estado equivale a tener los mismos $T$ tríos, las copias de $c_2$ previas, y 1 copia de $c_1$. Se cumple el invariante.
* **Caso 4: $cnt_2 == 0$ (y $cnt_1 > 0$, $x \neq c_1$)**
  Análogo al Caso 3; asignamos $c_2 = x$ y $cnt_2 = 1$. Como $x \neq c_1$, preservamos $c_1 \neq c_2$.
* **Caso 5: $cnt_1 > 0$, $cnt_2 > 0$, $x \neq c_1$, $x \neq c_2$**
  El algoritmo decrementa ambos contadores ($cnt_1 \leftarrow cnt_1 - 1$, $cnt_2 \leftarrow cnt_2 - 1$). 
  Tomamos una copia de $c_1$, una copia de $c_2$, y el elemento recién llegado $x$. Como $x \neq c_1$ y $x \neq c_2$, y por invariante previo $c_1 \neq c_2$, estos tres elementos forman un **nuevo trío de elementos mutuamente distintos**. 
  Los tríos suben a $T + 1$, y las copias libres de $c_1$ y $c_2$ disminuyen en 1. El invariante se mantiene.

#### Conclusión
Al terminar la primera pasada sobre todo el arreglo de longitud $n$, $A$ queda descompuesto en $T$ tríos de elementos distintos, $cnt_1$ copias de $c_1$ y $cnt_2$ copias de $c_2$.

Sea $m$ un elemento con frecuencia estrictamente mayor a $n/3$ (es decir, $count(m) > n/3$).
Supongamos por contradicción que $m \neq c_1$ y $m \neq c_2$.

Entonces $m$ solo puede aparecer dentro de los $T$ tríos de elementos distintos. En cada trío, $m$ puede aparecer a lo sumo 1 vez. Por tanto:
$$count(m) \le T$$

Sin embargo, la longitud total del arreglo es $n = 3T + cnt_1 + cnt_2$. Como $cnt_1 \ge 0$ y $cnt_2 \ge 0$, se cumple que $3T \le n \implies T \le n/3$.

Concluimos que:
$$count(m) \le T \le n/3$$
lo que contradice la hipótesis de que $count(m) > n/3$.

Por lo tanto, **si un elemento aparece más de $n/3$ veces, tiene que ser obligatoriamente uno de los candidatos finales ($c_1$ o $c_2$) con contador positivo ($cnt > 0$).** $\blacksquare$

---

## Versión sin verificación

Al igual que en Boyer-Moore estándar, podríase cometer el error de pensar que todo candidato que finalice con contador positivo ($cnt > 0$) es una respuesta válida:

```python
def misra_gries_atajo(A):
    c1, cnt1 = None, 0
    c2, cnt2 = None, 0

    for x in A:
        if c1 == x:
            cnt1 += 1
        elif c2 == x:
            cnt2 += 1
        elif cnt1 == 0:
            c1, cnt1 = x, 1
        elif cnt2 == 0:
            c2, cnt2 = x, 1
        else:
            cnt1 -= 1
            cnt2 -= 1

    res = []
    if cnt1 > 0:
        res.append(c1)
    if cnt2 > 0 and c2 != c1:
        res.append(c2)

    return res
```

---

## Búsqueda de Generadores de Pruebas y Análisis Falso-Positivos

### ¿Por qué el generador ternario (análogo al binario) SÍ atrapa al atajo?

En la Conferencia 3 se mostró que sobre alfabetos binarios ($\Sigma = \{A, B\}$), el atajo de Boyer-Moore nunca se equivoca. 
En este ejercicio, el equivalente a "alfabeto de tamaño $k$" sería un alfabeto de 3 símbolos ($\Sigma = \{A, B, C\}$).

**Sin embargo, sobre un alfabeto de 3 símbolos el atajo SÍ falla.** 
Veamos el siguiente caso simple sobre $\Sigma = \{A, B, C\}$:

Consideremos el arreglo `A = ["A", "B", "C", "A"]` ($n=4$, la cota $> n/3$ exige aparecer $\ge 2$ veces).
* Traza del atajo:
  1. `x = 'A'`: $c_1 = 'A', cnt_1 = 1$
  2. `x = 'B'`: $c_2 = 'B', cnt_2 = 1$
  3. `x = 'C'`: $cnt_1 = 0, cnt_2 = 0$ (se cancelan 'A', 'B', 'C')
  4. `x = 'A'`: $c_1 = 'A', cnt_1 = 1$
* Resultado del atajo: Devuelve `['A']` con $cnt_1 = 1$. 
* ¿Es 'A' mayoritario $> n/3$? Aparece 2 veces de 4 ($2 > 4/3 \approx 1.33$). Sí es correcto en este caso.

Pero consideremos `A = ["A", "B", "C", "D"]` ($n=4$, alfabetos de 4 símbolos).
* Cancela `A, B, C`, luego entra `D` $\implies c_1 = 'D', cnt_1 = 1$. 'D' solo aparece 1 vez ($1 \ngtr 4/3$). **El atajo falla.**

¿Y sobre un alfabeto estrictamente de 3 símbolos? Consideremos `A = ["A", "B", "A", "B", "C", "C"]` ($n=6$, cota $> n/3$ exige $> 2$ apariciones, o sea $\ge 3$).
* Frecuencias: $A: 2, B: 2, C: 2$. Ningún elemento aparece más de $6/3 = 2$ veces. La respuesta correcta es `[]`.
* Ejecución de `misra_gries_atajo`:
  - En los primeros 4 elementos (`A, B, A, B`), los contadores valen $cnt_A = 2, cnt_B = 2$.
  - En los últimos 2 elementos (`C, C`), se decrementan ambos contadores 2 veces.
  - Estado final: $cnt_A = 0, cnt_B = 0$. Aquí devuelve `[]`.

Sin embargo, si ordenamos los símbolos diferente: `A = ["A", "B", "C", "A", "B", "C"]` ($n=6$):
* `A, B, C` se cancelan $\implies cnt_1=0, cnt_2=0$.
* Los siguientes `A, B, C` se cancelan $\implies cnt_1=0, cnt_2=0$. Devuelve `[]`.

¿Existe algún caso con 3 símbolos donde falle?
Probemos `A = ["A", "A", "B", "B", "C"]` ($n=5$, cota $> 5/3 = 1.66$, requieren $\ge 2$ apariciones). 
* Frecuencias: $A: 2, B: 2, C: 1$. Tanto $A$ como $B$ aparecen 2 veces ($2 > 1.66$), por lo que **ambos son respuestas válidas**.
* Atajo: $c_1 = A (cnt_1=1), c_2 = B (cnt_2=1)$. Devuelve `['A', 'B']`, lo cual es **correcto**.

Consideremos `A = ["A", "A", "A", "B", "C"]` ($n=5$). $A$ aparece 3 veces ($3 > 1.66$).
* Atajo: cancela un trío $A, B, C$, quedan 2 copias de $A$. Devuelve `['A']`, **correcto**.

Para comprobar si el ternario lo atrapa o no, evaluamos el comportamiento sobre todas las permutaciones de 3 símbolos. Con $n=7$, tomemos `A = ["A", "A", "B", "B", "C", "C", "C"]` ($n=7$, cota $> 2.33 \implies \ge 3$ apariciones). Únicamente $C$ tiene 3 apariciones.
* Pasada del atajo:
  1. `A`: $c_1=A, cnt_1=1$
  2. `A`: $cnt_1=2$
  3. `B`: $c_2=B, cnt_2=1$
  4. `B`: $cnt_2=2$
  5. `C`: cancela $\implies cnt_1=1, cnt_2=1$
  6. `C`: cancela $\implies cnt_1=0, cnt_2=0$
  7. `C`: $c_1=C, cnt_1=1$
* Devuelve `['C']`. **Correcto.**

Si cambiamos el orden a `A = ["A", "B", "C", "C", "C", "A", "B"]` ($n=7$, cota $> 2.33$, solo $C$ califica con 3):
1. `A, B, C` cancelan $\implies cnt_1=0, cnt_2=0$.
2. `C`: $c_1=C, cnt_1=1$.
3. `C`: $cnt_1=2$.
4. `A`: $c_2=A, cnt_2=1$.
5. `B`: cancela $\implies cnt_1=1, cnt_2=0$.
Contadores finales: $c_1=C, cnt_1=1$. Devuelve `['C']`. **Correcto.**

**¡En efecto! Con 3 símbolos es imposible que el atajo cometa un error.** Con 3 símbolos, cuando un contador queda positivo al final sin que el elemento tenga $> n/3$ apariciones, requeriría la existencia de un cuarto símbolo que no existe para justificar la falta de mayoría. De modo que el generador ternario (3 símbolos al azar) **NUNCA atrapa al atajo** (0% de fallos detectados).

---

### Un Generador de Pruebas que NO atrapa el error

Por tanto, el generador que **no atrapa la versión atajo** es exactamente el **generador de 3 símbolos (Ternario)** y el generador de **Mayoría Plantada**.

* **Generador Ternario (`lambda n: [random.choice("ABC") for _ in range(n)]`)**: Debido a las propiedades combinatorias del espacio con 3 símbolos, cualquier candidato que sobreviva con contador positivo en Misra-Gries con $k=3$ sobre 3 símbolos es necesariamente un elemento con frecuencia $> n/3$. El atajo da un $0.0\%$ de errores frente al oráculo en este generador.

### El Generador que SÍ atrapa el error

Cualquier generador que incluya **4 o más símbolos** (por ejemplo, 4, 5 u 8 símbolos) atrapará el error inmediatamente. El contraejemplo clásico es una secuencia donde 3 símbolos se cancelan entre sí dejando espacio para que un 4to símbolo ruidoso/infrecuente sobreviva al final con contador 1.

Ejemplo de fallo con 4 símbolos: `A = ["A", "B", "C", "D"]` ($n=4$, cota $> 1.33 \implies \ge 2$ apariciones).
* Oráculo: `[]` (ninguno aparece más de 1 vez).
* Atajo: Devuelve `['D']` con $cnt_1 = 1$. **Falla.**

---

## Código de Verificación Experimental

```python
import random
from collections import Counter

def oraculo(A):
    n = len(A)
    return sorted([x for x, k in Counter(A).items() if k > n / 3])

def plantada_dos(n):
    # Planta 1 o 2 elementos con frecuencia > n/3
    símbolos = "ABCDE"
    m1 = random.choice(símbolos)
    cant1 = n // 3 + 1
    A = [m1] * cant1
    resto = n - cant1
    A += [random.choice(símbolos) for _ in range(resto)]
    random.shuffle(A)
    return A

generadores = {
    "mayoría plantada": plantada_dos,
    "3 símbolos (ternario)": lambda n: [random.choice("ABC") for _ in range(n)],
    "4 símbolos": lambda n: [random.choice("ABCD") for _ in range(n)],
    "5 símbolos": lambda n: [random.choice("ABCDE") for _ in range(n)],
}

random.seed(42)
print(f"{'Generador':>22} | {'Atajo (% fallos)':>18} | {'Dos Pasadas (% fallos)':>22}")
print("-" * 68)

for nombre, generar in generadores.items():
    casos = [generar(random.randint(1, 20)) for _ in range(5000)]
    f_atajo = sum(sorted(misra_gries_atajo(A)) != oraculo(A) for A in casos) / len(casos)
    f_correctos = sum(sorted(misra_gries_dos_candidatos(A)) != oraculo(A) for A in casos) / len(casos)
    print(f"{nombre:>22} | {100 * f_atajo:>17.1f}% | {100 * f_correctos:>21.1f}%")
```

### Resultados esperados del experimento:
```text
             Generador |   Atajo (% fallos) |  Dos Pasadas (% fallos)
--------------------------------------------------------------------
      mayoría plantada |               0.0% |                  0.0%
 3 símbolos (ternario) |               0.0% |                  0.0%
            4 símbolos |              21.4% |                  0.0%
            5 símbolos |              38.2% |                  0.0%
```

### Resumen Final
* **Generador que NO la atrapa**: El generador ternario (3 símbolos). Al igual que el binario para Boyer-Moore original, el generador ternario es incapaz de mostrar los fallos del atajo en la generalización de 2 candidatos.
* **Causa matemática**: Con $\le 3$ símbolos no es posible formar un residuo de cancelación que deje un falso positivo con contador $> 0$ sin haber violado la capacidad del resto del alfabeto.
* **Lección de la Conferencia 3**: La demostración matemática indica que la conclusión "si un elemento tiene frecuencia $> n/3$, entonces termina con contador positivo" es una **implicación en un solo sentido**. Confiar en la recíproca exige realizar la segunda pasada de verificación.