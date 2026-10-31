# Ejercicio 8: El elemento que aparece más de $n/3$ veces

> **Enunciado:** El elemento que aparece más de $n/3$ veces. Generaliza Boyer-Moore con dos candidatos, enuncia el invariante reforzado y demuéstralo. Después escribe la versión que devuelve los candidatos con contador positivo sin verificarlos, y busca un generador de pruebas que no la atrape. Cuidado: el análogo del generador binario de la conferencia 3 sí la atrapa.

Este ejercicio pide generalizar el algoritmo de Boyer-Moore (conferencia 3) al problema de encontrar todos los elementos que aparecen más de $n/3$ veces. La generalización se conoce como algoritmo de Misra-Gries para $k = 3$.


## 1. El problema

**Elemento mayoritario generalizado ($k = 3$).** Dado un arreglo $A$ de $n$ elementos comparables solo por igualdad, devolver todos los elementos que aparecen más de $n/3$ veces.

**Observación clave.** ¿Cuántos elementos pueden aparecer más de $n/3$ veces? A lo sumo dos. Si hubiera tres, entre los tres sumarían más de $n$, lo cual es imposible. Por eso el algoritmo mantiene dos candidatos con sus respectivos contadores, no uno.

**Objetivo.** Tiempo $O(n)$ y memoria extra $O(1)$: un número constante de variables, sin importar $n$.

Las soluciones ingenuas no llegan, igual que en el caso de mayoría simple:

- Contar apariciones de cada elemento: $\Theta(n^2)$ comparaciones.
- Ordenar y mirar bloques: $O(n \log n)$, y requiere un orden que no tenemos.
- Tabla hash de cuentas: $O(n)$ tiempo esperado, pero $O(n)$ memoria.

## 2. La idea: cancelación con dos candidatos

Recordemos la observación de cancelación del caso simple (conferencia 3):

> Si tacho dos elementos distintos del arreglo, la mayoría sigue siendo mayoría en lo que queda.

Para el umbral $n/3$, la idea análoga es:

> Si tacho tres elementos distintos del arreglo, cualquier elemento que aparezca más de $n/3$ veces sigue apareciendo más de $n/3$ veces en lo que queda.

**Verificación.** Sea $m$ un elemento con $k > n/3$ apariciones. En cada terna de tres elementos distintos, $m$ aparece a lo sumo una vez. Tras tachar una terna, quedan $k-1$ copias de $m$ entre $n-3$ elementos, y

$$k - 1 > \frac{n}{3} - 1 = \frac{n-3}{3}.$$

Así que $m$ sigue superando el umbral en el arreglo reducido.

**Consecuencia.** Si seguimos tachando ternas de elementos distintos hasta que no se pueda, lo que sobreviva son copias de a lo sumo dos elementos distintos. Si había algún elemento con más de $n/3$ apariciones, tiene que estar entre esos dos.

## 3. El algoritmo

```python
def candidatos_n3(A):
    """Primera pasada: devuelve los dos candidatos y sus contadores."""
    c1, n1 = None, 0
    c2, n2 = None, 0
    for x in A:
        if n1 > 0 and x == c1:
            n1 += 1
        elif n2 > 0 and x == c2:
            n2 += 1
        elif n1 == 0:
            c1, n1 = x, 1
        elif n2 == 0:
            c2, n2 = x, 1
        else:
            # x es distinto de ambos candidatos y ambos tienen contador > 0:
            # se cancela una terna (c1, c2, x)
            n1 -= 1
            n2 -= 1
    return c1, n1, c2, n2


def mayoria_n3(A):
    """Segunda pasada: verifica los candidatos."""
    c1, n1, c2, n2 = candidatos_n3(A)
    # set: el valor residual de c2 puede ser igual a c1
    return sorted({c for c in (c1, c2)
                   if c is not None and 3 * A.count(c) > len(A)})
```


## 4. El invariante reforzado

Para demostrar correctitud, hay que encontrar el invariante. La primera frase que uno escribe es la que queremos al final, aplicada a cada prefijo:

> Si el prefijo procesado tiene algún elemento con más de un tercio de apariciones, ese elemento es uno de los dos candidatos.

Esta frase es verdadera, pero no es inductiva. Intenta el paso de mantenimiento: supón que vale para el prefijo de largo $i$ y procesa el elemento $i+1$. Si el prefijo de largo $i$ no tiene ningún elemento con más de $i/3$ apariciones, la hipótesis no dice nada sobre los candidatos, y sin embargo el prefijo de largo $i+1$ podría tener uno. El invariante no se sostiene solo.

Hay que reforzarlo, afirmando algo más fuerte que sí sea inductivo. La idea de cancelación escrita como afirmación sobre el estado es:

**Invariante.** Después de procesar el prefijo $A[1..i]$, ese prefijo se puede partir en:

- $(i - n_1 - n_2)/3$ ternas de tres elementos distintos, más
- $n_1$ copias del candidato $c_1$, más
- $n_2$ copias del candidato $c_2$,

donde $c_1 \neq c_2$ siempre que ambos contadores sean positivos.

La generalización natural del invariante de Boyer-Moore (conferencia 3, §4): allí el prefijo se partía en parejas de distintos más $c$ copias del candidato; aquí se parte en ternas de distintos más $n_1$ copias de $c_1$ y $n_2$ copias de $c_2$.

**Inicialización.** Antes de la primera vuelta el prefijo es vacío, $n_1 = n_2 = 0$: cero ternas y cero copias. ✓

**Mantenimiento.** Supongamos el invariante para $A[1..i]$ y procesemos $x = A[i+1]$. Hay cinco casos, uno por rama del `if`:

1. $x = c_1$ y $n_1 > 0$. El algoritmo hace $n_1 \leftarrow n_1 + 1$. La partición nueva es la misma más una copia de $c_1 = x$. ✓

2. $x = c_2$ y $n_2 > 0$. Análogo: una copia más de $c_2$. ✓

3. $n_1 = 0$. El prefijo es solo ternas y $n_2$ copias de $c_2$. El algoritmo hace $c_1 \leftarrow x$, $n_1 \leftarrow 1$. La partición nueva es la misma más una copia de $x$. (Si $x = c_2$, no importa: la rama 2 se habría activado antes; aquí $x \neq c_2$ o $n_2 = 0$.) ✓

4. $n_2 = 0$. Análogo al caso 3. ✓

5. $x \neq c_1$, $x \neq c_2$, $n_1 > 0$, $n_2 > 0$. El algoritmo hace $n_1 \leftarrow n_1 - 1$, $n_2 \leftarrow n_2 - 1$. Emparejamos $x$ con una copia de $c_1$ y una copia de $c_2$: como $x, c_1, c_2$ son tres elementos distintos, forman una terna. Quedan $n_1 - 1$ copias de $c_1$ y $n_2 - 1$ copias de $c_2$, que es lo que el algoritmo deja en los contadores. ✓

**Conclusión.** Al terminar, $A$ entero se parte en $(n - n_1 - n_2)/3$ ternas de elementos distintos, más $n_1$ copias de $c_1$, más $n_2$ copias de $c_2$.

## 5. Correctitud: el teorema

**Teorema.** Si algún elemento $m$ aparece más de $n/3$ veces en $A$, entonces $m \in \{c_1, c_2\}$ al terminar la primera pasada.

**Demostración.** Por el invariante, $A$ se parte en ternas de elementos distintos más $n_1$ copias de $c_1$ más $n_2$ copias de $c_2$. Supongamos que $m$ aparece más de $n/3$ veces y que $m \notin \{c_1, c_2\}$. Entonces todas las apariciones de $m$ están en las ternas, y en cada terna aparece a lo sumo una vez (los tres elementos de una terna son distintos). El número de ternas es $(n - n_1 - n_2)/3 \leq n/3$. Por tanto $m$ aparece a lo sumo $n/3$ veces, contradicción. $\square$

**Forma exacta del teorema.** Es importante notar el "si": si hay un elemento con más de $n/3$ apariciones, entonces es uno de los dos candidatos. No dice que todo candidato con contador positivo sea mayoría. Guarda esa forma, porque la sección 6 depende de ella.

**Segunda pasada.** El teorema garantiza que si hay un elemento con más de $n/3$ apariciones, está entre los candidatos. La segunda pasada verifica cuáles de los candidatos realmente superan el umbral. Si ninguno lo hace, el teorema dice que no hay ninguno, y devolvemos la lista vacía.

**Complejidad.** Dos pasadas, $O(n)$ tiempo, $O(1)$ memoria extra (dos candidatos y dos contadores). Óptimo: cualquier algoritmo tiene que leer $\Omega(n)$ posiciones.


## 6. El error que la demostración anuncia: el atajo sin verificar

La segunda pasada parece un desperdicio. Mira los contadores: al final, $n_1$ y $n_2$ cuentan las copias de los candidatos que sobrevivieron. Es tentador pensar que si un candidato sobrevivió con contador positivo, es mayoría, y ahorrarse la segunda pasada:

```python
def mayoria_n3_atajo(A):
    c1, n1, c2, n2 = candidatos_n3(A)
    return [c for c, n in ((c1, n1), (c2, n2)) if c is not None and n > 0]
```

La mitad del atajo es correcta. Si hay un elemento con más de $n/3$ apariciones, el teorema garantiza que es uno de los candidatos, y su contador final no puede ser 0. (Si $n_1 = 0$, la conclusión del teorema da que cualquier $m \notin \{c_1, c_2\}$ aparece a lo sumo $n/3$ veces; y $c_1$ mismo aparece a lo sumo $n_1 = 0$ veces en las copias, más a lo sumo una vez por terna, es decir, a lo sumo $n/3$ veces.) Así que contador 0 implica que ese candidato no es mayoría.

Lo falso es la recíproca. **Contador positivo no implica que el candidato sea mayoría.**


| Pos | $x$ | $c_1$ | $n_1$ | $c_2$ | $n_2$ | Acción |
|---|---|---|---|---|---|---|
| 1 | A | A | 1 | — | 0 | $c_1 \leftarrow A$ |
| 2 | B | A | 1 | B | 1 | $c_2 \leftarrow B$ |
| 3 | C | A | 0 | B | 0 | cancelar |
| 4 | A | A | 1 | B | 0 | $c_1 \leftarrow A$ |
| 5 | B | A | 1 | B | 1 | $c_2 \leftarrow B$ |
| 6 | C | A | 0 | B | 0 | cancelar |
| 7 | D | D | 1 | B | 0 | $c_1 \leftarrow D$ |
| 8 | D | D | 2 | B | 0 | $x = c_1$: $n_1{+}{+}$ |

$c_1 = D$ con $n_1 = 2 > 0$. $D$ aparece 2 veces de 8, y $2 \leq 8/3$, así que $D$ no es mayoría. El atajo devuelve $[D]$, que es incorrecto. La respuesta correcta es la lista vacía (ningún elemento aparece más de $8/3 \approx 2.67$ veces; $A$ y $B$ aparecen 2 veces cada uno, $C$ 2 veces, $D$ 2 veces).

**Contraejemplo mínimo:** $A = [A, B, C, A, B, C, D, D]$, $n = 8$. El atajo devuelve $[D]$; la verdad es $[]$.



## 7. El generador de pruebas que no lo atrapa

Comparemos las dos versiones contra un oráculo que cuenta todo, con varios generadores de arreglos.

```python
import random
from collections import Counter

def oraculo_n3(A):
    n = len(A)
    return sorted({x for x, k in Counter(A).items() if 3 * k > n})

def atajo(A):
    c1, n1, c2, n2 = candidatos_n3(A)
    return sorted({c for c, n in ((c1, n1), (c2, n2)) if c is not None and n > 0})

def correcto(A):
    return sorted(mayoria_n3(A))

def plantada_distinta(n):
    """Dos mayorías distintas plantadas y relleno aleatorio."""
    m1, m2 = random.sample("ABCDEF", 2)          # forzadas distintas
    return ([m1] * (n // 3 + 1) + [m2] * (n // 3 + 1)
            + [random.choice("ABCDEF") for _ in range(n - 2 * (n // 3 + 1))])

def plantada_sin_forzar(n):
    """Igual, pero sorteando m1 y m2 con repetición."""
    m1, m2 = random.choice("ABCDEF"), random.choice("ABCDEF")
    return ([m1] * (n // 3 + 1) + [m2] * (n // 3 + 1)
            + [random.choice("ABCDEF") for _ in range(n - 2 * (n // 3 + 1))])

generadores = {
    "mayoría plantada (m1 != m2)": plantada_distinta,
    "mayoría plantada (sin forzar)": plantada_sin_forzar,
    "binario": lambda n: [random.choice("AB") for _ in range(n)],
    "3 símbolos": lambda n: [random.choice("ABC") for _ in range(n)],
    "5 símbolos": lambda n: [random.choice("ABCDE") for _ in range(n)],
    "8 símbolos": lambda n: [random.choice("ABCDEFGH") for _ in range(n)],
}

random.seed(7)
print(f"{'generador':>32} {'atajo':>8} {'dos pasadas':>12}")
for nombre, generar in generadores.items():
    casos = [generar(random.randint(3, 20)) for _ in range(5000)]
    f_atajo = sum(atajo(A) != oraculo_n3(A) for A in casos) / len(casos)
    f_correcto = sum(correcto(A) != oraculo_n3(A) for A in casos) / len(casos)
    print(f"{nombre:>32} {100 * f_atajo:>7.1f}% {100 * f_correcto:>11.1f}%")
```

**Salida medida** (`random.seed(7)`, 5000 casos por generador, $n \in [3, 20]$):

| Generador | Atajo | Dos pasadas |
|---|---|---|
| **Mayoría plantada ($m_1 \neq m_2$)** | **0.0%** | 0.0% |
| Mayoría plantada (sin forzar) | 8.9% | 0.0% |
| Binario | 32.8% | 0.0% |
| 3 símbolos | 41.5% | 0.0% |
| 5 símbolos | 63.5% | 0.0% |
| 8 símbolos | 67.4% | 0.0% |

**Lectura.** Un solo generador no atrapa al atajo: **mayoría plantada con los dos candidatos forzados a ser distintos**, que es la respuesta a lo que pide el enunciado. Todos los demás lo atrapan — empezando por el binario, exactamente como avisaba el «Cuidado»: es la diferencia con la conferencia 3, donde el generador binario era inofensivo.

**Por qué el binario ahora sí la atrapa.** Con dos símbolos, la rama de cancelación es imposible: exige $x \neq c_1$, $x \neq c_2$ con ambos contadores positivos y $c_1 \neq c_2$, o sea tres valores distintos en el prefijo — y con dos símbolos no existen. Entonces no se forma ninguna terna, y el invariante final dice que el arreglo son $n_1$ copias de $c_1$ más $n_2$ copias de $c_2$: los contadores finales son las cuentas exactas. El atajo devuelve ambos símbolos presentes y falla exactamente cuando el minoritario aparece $\leq n/3$ veces; por ejemplo $A^9B$ con $n = 10$: $B$ queda con contador $1$ y $1 \leq 10/3$. En la conferencia 3 esto no podía pasar: con umbral $n/2$, tener contador positivo equivalía a superar al otro símbolo, o sea a ser mayoría. Con umbral $n/3$, un símbolo puede tener cuenta positiva y seguir por debajo del tercio. Esa es la razón del «Cuidado» del enunciado.

**Por qué la plantada necesita $m_1 \neq m_2$.** Si el sorteo de los plantados se hiciera con repetición (`random.choice` dos veces), con probabilidad $1/6$ caería $m_1 = m_2$: la instancia tendría un solo candidato oficial y el segundo slot quedaría libre para que el relleno se cuele con contador positivo. Es lo que mide la fila «sin forzar» (8.9%): por ejemplo $[E, E, E, E, C]$ ($n = 5$) deja el estado final $(E, 4), (C, 1)$, el atajo devuelve $[C, E]$ y la verdad es $[E]$. Por eso el generador seguro usa `random.sample("ABCDEF", 2)`, que fuerza dos valores distintos: las dos mayorías ocupan los dos slots, sus contadores quedan positivos y el atajo acierta siempre.

**Tres símbolos.** También la atrapa. Contraejemplo mínimo: $[B, B, B, B, B, A, A, C]$ ($n = 8$). El estado final es $(B, 4), (A, 1)$: la última $C$ cancela una copia de cada candidato. El atajo devuelve $[A, B]$ porque $A$ tiene contador positivo, pero $A$ aparece 2 veces y $2 \leq 8/3$: la verdad es $[B]$. Con tres símbolos, un candidato con contador positivo puede quedar por debajo del tercio cuando sus copias se cancelaron demasiado: del invariante, $\text{count}(c_1) \leq \#\text{ternas} + n_1$, y esa cota no garantiza el umbral.

**Dos pasadas.** 0.0% de fallos con todos los generadores, como garantiza el teorema: los mayoritarios nunca quedan fuera de los candidatos, y la segunda pasada se deshace de los que no superan el umbral.

## 8. Resumen

| Pregunta (conferencia 2) | Respuesta |
|---|---|
| ¿Qué es el problema? | Devolver todos los elementos que aparecen más de $n/3$ veces. A lo sumo puede haber dos. Modelo: comparaciones solo de igualdad. |
| ¿Qué algoritmo? | Misra-Gries con $k = 3$: dos candidatos con contadores; cada elemento distinto de ambos cancela una terna. Segunda pasada que verifica los candidatos. |
| ¿Es correcto? | Invariante: el prefijo procesado se parte en ternas de elementos distintos más $n_1$ copias de $c_1$ más $n_2$ copias de $c_2$ (con $c_1 \neq c_2$ si ambos contadores son positivos). Teorema: si algún elemento aparece más de $n/3$ veces, es uno de los dos candidatos. |
| ¿Cuánto cuesta? | Dos pasadas, $O(n)$ tiempo, $O(1)$ memoria extra. Óptimo en orden: hay que leer todo, $\Omega(n)$. |
| ¿Se puede mejorar? | No en orden, y la segunda pasada no sobra: el atajo que devuelve los candidatos con contador positivo falla cuando un candidato no supera el tercio. Lo atrapan todos los generadores salvo mayoría plantada con candidatos distintos — y el binario sí la atrapa (32.8%), al revés que en la conferencia 3. |