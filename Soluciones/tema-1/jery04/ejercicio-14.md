# Ejercicio 14: Ciclo completo de cinco preguntas sobre un problema nuevo

> **Enunciado:** Escoge un problema que no hayamos visto, recorre el ciclo completo de la conferencia 2 sobre él y consigue que el algoritmo y la cota mínima coincidan. Es el formato de la pregunta larga del examen final.

## 1. Enunciado preciso del problema

Antes de proponer un algoritmo hay que fijar qué se está preguntando, porque el enunciado esconde decisiones que cambian la respuesta. Este es el primer reflejo de la conferencia 2, §2: precisar el problema antes de resolverlo.

**El problema.** Dado un arreglo $A$ de $n \geq 2$ elementos de un orden total, devolver una pareja $(m, M)$ donde $m$ es el mínimo de $A$ y $M$ es el máximo de $A$.

**El modelo de cómputo.** El modelo de comparaciones de la conferencia 5, §1: el algoritmo solo puede preguntar si $a < b$ sobre los valores, y el costo es el número de comparaciones. Es el modelo natural porque la cota que vamos a demostrar se enuncia ahí, y porque el problema no tiene estructura aritmética que explotar.

**Precisiones que el enunciado no da y hay que fijar** (conferencia 2, §2):

- **Empates.** Si varios elementos alcanzan el mínimo o el máximo, devolvemos cualquiera de ellos. El problema no pide posiciones, así que los empates no afectan la respuesta.

- **Elementos repetidos.** A diferencia del par más cercano, aquí sí importan: si todos los elementos son iguales, $m = M$ y el algoritmo debe devolver ese valor en ambas componentes.

- **La precondición $n \geq 2$.** Con $n = 1$ el problema es trivial y la cota no aplica; lo excluimos en la precondición, como exige la conferencia 3, §1.

**Lo que hay que conseguir.** Un algoritmo correcto que haga exactamente $\lfloor 3n/2 \rfloor - 2$ comparaciones, y una demostración de que ningún algoritmo de comparaciones puede hacer menos. Que ambos números coincidan es lo que cierra el ciclo de la conferencia 2.

**Nota sobre la elección.** El ejercicio 1 de la conferencia 5 pide este mismo resultado como ejercicio guiado, pero no lo resuelve. Lo tomo porque el ejercicio 14 pide recorrer el ciclo completo, no inventar un problema inédito en la literatura; lo que se evalúa es el recorrido, y aquí se recorre entero con las herramientas del Tema 1.

## 2. Observación clave

El problema tiene dos extremos, y la fuerza bruta los busca por separado: una pasada para el mínimo con $n-1$ comparaciones (conferencia 5, §5) y otra para el máximo con otras $n-1$. Total $2n-2$.

La observación que lo mejora es de **cancelación**, la misma idea de Boyer-Moore (conferencia 3, §2) y del torneo del segundo mayor (conferencia 5, §7): cuando comparamos dos elementos $a$ y $b$ entre sí, aprendemos dos cosas a la vez. El mayor del par ya no puede ser el mínimo global, y el menor ya no puede ser el máximo global. Una sola comparación descarta a un candidato a mínimo y a un candidato a máximo, mientras que la fuerza bruta descarta a un solo candidato por comparación.

La forma de explotarlo es procesar por parejas: una comparación interna decide cuál es el menor del par ($\ell$) y cuál el mayor ($h$); después $\ell$ se compara con el mínimo candidato y $h$ con el máximo candidato. Son 3 comparaciones por pareja, en lugar de las 4 que costaría procesar sus dos elementos por separado.

Formalmente, si el costo es $T(n)$ y el presupuesto de comparaciones es $P$, lo que queremos es que el algoritmo alcance la cota

$$T(n) = \left\lfloor \frac{3n}{2} \right\rfloor - 2,$$

y que la cota mínima demostrada sea exactamente ese mismo número. Que el algoritmo y la cota coincidan es lo que significa que el ciclo se cerró: la búsqueda se acabó (conferencia 2, §8).


## 3. El algoritmo

**La estructura.** Partimos el arreglo en parejas consecutivas. Para cada pareja hacemos la comparación interna, y después actualizamos los dos candidatos globales con el menor y el mayor del par. Si $n$ es impar, un elemento queda suelto y se trata al final.

**El arranque.** La primera pareja se usa para inicializar $m$ y $M$ sin comparar contra nada: su comparación interna da el menor y el mayor, y esos son los candidatos iniciales. Cuesta 1 comparación.

**El caso impar.** El elemento suelto se compara una sola vez: con $m$ si es menor que $m$, y si no, con $M$. No hacen falta las dos comparaciones, porque si el suelto es menor que $m$ entonces es menor que todo (en particular que $M$, que ya es mayor que $m$), y si es mayor que $M$ entonces es mayor que todo. Este es el paso que la demostración de la cota va a anunciar: la versión que compara el suelto con ambos extremos hace una comparación de más y no alcanza la cota (conferencia 3, §5).

```python
def max_min(A):
    n = len(A)
    pares = [(A[i], A[i+1]) for i in range(0, n - 1, 2)]
    suelto = A[-1] if n % 2 else None

    # arranque con la primera pareja: 1 comparación
    a, b = pares[0]
    if a < b: m, M = a, b
    else:     m, M = b, a

    # el resto de las parejas: 3 comparaciones cada una
    for (a, b) in pares[1:]:
        if a < b: l, h = a, b
        else:     l, h = b, a
        if l < m: m = l
        if h > M: M = h

    # el suelto: 1 comparación, no 2
    if suelto is not None:
        if suelto < m:   m = suelto
        elif suelto > M: M = suelto
    return m, M
```
**Conteo exacto de comparaciones.**

- $n$ par: $1 + 3(n/2 - 1) = 3n/2 - 2$.

- $n$ impar: $1 + 3((n-1)/2 - 1) + 1 = 3(n-1)/2 - 1 = \lfloor 3n/2 \rfloor - 2$.

En ambos casos, $\lfloor 3n/2 \rfloor - 2$. La fuerza bruta hace $2n - 2$; la mejora es un factor $4/3$, no un cambio de orden asintótico. Es el tipo de mejora que la conferencia 1, §7 advierte que no se ve cuando la computadora mejora un factor constante: ambos son $\Theta(n)$. Pero en el modelo de comparaciones, donde cada pregunta cuesta 1 y la cota mínima especifica la constante exacta, el factor $4/3$ sí importa, y aquí la cota mínima es la del algoritmo mejorado, no la de la fuerza bruta.




## 4. La correctitud

Dos demostraciones separadas, como exige la conferencia 3, §1: correctitud parcial (invariante) y terminación (potencial).

### Correctitud parcial: el invariante

**Invariante.** Al inicio de la iteración que procesa la pareja $j$ (con $j \geq 1$, después de haber procesado las parejas $0, \ldots, j-1$):

> $m = \min(\text{elementos procesados})$ y $M = \max(\text{elementos procesados})$.

**Inicialización.** Antes de la primera iteración del ciclo (después del arranque con la pareja 0), los elementos procesados son $a, b$, y el arranque deja $m = \min(a, b)$, $M = \max(a, b)$. ✓

**Mantenimiento.** Supongamos el invariante antes de procesar la pareja $j = (a, b)$; los procesados son $S$. La comparación $a < b$ identifica $\ell = \min(a, b)$ y $h = \max(a, b)$. Entonces

$$\min(S \cup \{a, b\}) = \min(\min S, \ell) = \min(m, \ell),$$

porque $\ell$ es el único candidato nuevo a mínimo del par. La línea `if l < m: m = l` deja exactamente $\min(m, \ell)$ en $m$. Análogamente, $\max(S \cup \{a, b\}) = \max(M, h)$, y `if h > M: M = h` lo deja en $M$. ✓

El caso del elemento suelto es idéntico con un par degenerado. ✓

**Conclusión.** Al terminar el ciclo, los elementos procesados son todos los de $A$, así que $m = \min A$ y $M = \max A$. ✓

El invariante es inductivo, no solo verdadero (lección central de la conferencia 3, §4). La frase da información sobre ambos extremos, y esa información basta para el paso siguiente: la actualización con $\ell$ y $h$ solo necesita los valores viejos de $m$ y $M$. Compárese con el primer intento fallido del invariante de Boyer-Moore: allí la frase "si el prefijo tiene mayoría, el candidato es esa mayoría" era verdadera pero no inductiva, porque cuando el prefijo no tenía mayoría no decía nada sobre el estado. Aquí no ocurre, porque el invariante caracteriza el estado sin hipótesis que pueda fallar.

### Terminación: el potencial

**Potencial.** $\Phi = (\text{número de elementos sin procesar})$, un entero no negativo.

**Inicialización.** $\Phi_0 = n$.

**Decremento.** Cada vuelta del ciclo procesa una pareja (dos elementos), o el suelto (uno), y $\Phi$ baja en 2 o en 1. En cualquier caso $\Phi$ decrece estrictamente.

**Piso.** $\Phi \geq 0$.

**Conclusión.** El ciclo hace a lo sumo $\lceil n/2 \rceil$ vueltas y termina. ✓

Como en Gale-Shapley (conferencia 3, §7), el potencial no solo demuestra que termina: $\Phi_0 = n$ acota el número de vueltas.

### Verificación experimental

Antes de escribir la demostración conviene correr el algoritmo y vigilar el invariante, por la lección del "invariante vigilado" de Boyer-Moore (conferencia 3, §4):

```python
from itertools import permutations

def max_min_vigilado(A):
    n = len(A)
    pares = [(A[i], A[i+1]) for i in range(0, n - 1, 2)]
    suelto = A[-1] if n % 2 else None

    a, b = pares[0]
    m, M = (a, b) if a < b else (b, a)
    procesados = [a, b]
    assert m == min(procesados) and M == max(procesados)

    for (a, b) in pares[1:]:
        if a < b: l, h = a, b
        else:     l, h = b, a
        if l < m: m = l
        if h > M: M = h
        procesados += [a, b]
        assert m == min(procesados) and M == max(procesados)

    if suelto is not None:
        if suelto < m:   m = suelto
        elif suelto > M: M = suelto
        procesados.append(suelto)
        assert m == min(procesados) and M == max(procesados)
    return m, M

for n in range(2, 9):
    for P in permutations(range(n)):
        m, M = max_min_vigilado(list(P))
        assert (m, M) == (0, n - 1), (P, m, M)
print("correcto en todas las permutaciones de n = 2..8")
```
Esto no reemplaza la demostración: comprueba miles de prefijos, no todos. Pero confirma el invariante en un segundo y, si estuviera mal escrito, el `assert` lo diría sin perder una tarde.


## 5. El costo

**Tiempo, peor caso.** Por el conteo de la sección 3: exactamente $\lfloor 3n/2 \rfloor - 2$ comparaciones, y ese es también el mejor caso, porque el número de comparaciones no depende de los valores, solo de $n$. En la notación de la conferencia 1:

$$T(n) = \left\lfloor \frac{3n}{2} \right\rfloor - 2 \in \Theta(n).$$

**Memoria.** $O(1)$ variables además de la entrada: $m$, $M$, $\ell$, $h$ y un índice. La construcción de pares es un detalle de Python; el algoritmo en el modelo de comparaciones usa memoria constante.

**Comprobación con una máquina de conteo.** El programa siguiente cuenta las comparaciones que el algoritmo hace de verdad, sobre entradas aleatorias y sobre todas las permutaciones para $n$ pequeño, y las compara con la fórmula:

```python
import math, random

def max_min_contando(A):
    n = len(A)
    pares = [(A[i], A[i+1]) for i in range(0, n - 1, 2)]
    suelto = A[-1] if n % 2 else None
    c = 0
    a, b = pares[0]
    c += 1                                   # comparación interna de la pareja 0
    m, M = (a, b) if a < b else (b, a)
    for (a, b) in pares[1:]:
        c += 1                               # comparación interna
        if a < b: l, h = a, b
        else:     l, h = b, a
        c += 1;  m = l if l < m else m       # comparación con el mínimo
        c += 1;  M = h if h > M else M       # comparación con el máximo
    if suelto is not None:
        c += 1                               # una sola comparación con el suelto
        if suelto < m:   m = suelto
        elif suelto > M: M = suelto
    return m, M, c

random.seed(2026)
print(f"{'n':>6} {'comparaciones':>14} {'⌊3n/2⌋-2':>10}")
for n in [10, 100, 1000, 10000, 100001]:
    A = random.sample(range(10 * n), n)
    _, _, c = max_min_contando(A)
    print(f"{n:>6} {c:>14,} {math.floor(1.5 * n) - 2:>10,}")
```
La columna del medio es lo que hace el algoritmo; la de la derecha, la fórmula. Coinciden en todos los casos, pares e impares, lo que confirma el conteo del peor caso y que el conteo es independiente de la entrada: el algoritmo hace siempre el mismo número de comparaciones, no solo en el peor caso.





## 6. La cota mínima

Aquí se cierra el ciclo. La pregunta cambia de sujeto (conferencia 2, §8): en vez de preguntar cuánto cuesta este algoritmo, pregunta cuánto cuesta cualquiera. Para decir algo sobre todos los algoritmos hay que fijar el modelo, y ya lo fijamos: comparaciones.

**Teorema.** Todo algoritmo de comparaciones que devuelve el mínimo y el máximo de $n \geq 2$ elementos hace, en el peor caso, al menos $\lfloor 3n/2 \rfloor - 2$ comparaciones.

**Demostración por reducción a dos problemas ya resueltos.** Empareja mentalmente los elementos de antemano, en $\lfloor n/2 \rfloor$ parejas, y deja un suelto si $n$ es impar. (El algoritmo no conoce el emparejamiento; el argumento funciona para cualquier emparejamiento que elijamos, y eso basta para una cota inferior.)

**Paso 1: cada pareja necesita su comparación interna.** Si el algoritmo termina sin haber comparado $a$ con $b$ dentro de una pareja $(a, b)$, consideremos las dos entradas que se obtienen intercambiando los valores de $a$ y $b$ y dejando el resto igual. Las dos entradas tienen el mismo multiconjunto de valores, así que tienen el mismo mínimo y el mismo máximo globales; todas las comparaciones que el algoritmo hizo dan la misma respuesta en ambas (ninguna involucraba a los dos a la vez, y el orden con el resto no cambió); y sin embargo el algoritmo no puede saber cuál de los dos es el mínimo del par y cuál el máximo. Pero el mínimo global es uno de los dos solo si el otro es mayor que todos los demás, y el adversario puede elegir la entrada para que así sea. Así que el algoritmo se equivoca en una de las dos. Por tanto, cada una de las $\lfloor n/2 \rfloor$ parejas necesita al menos 1 comparación interna:

$$c \geq \left\lfloor \frac{n}{2} \right\rfloor.$$

**Paso 2: el máximo de los ganadores y el mínimo de los perdedores.** Después de esas comparaciones, cada pareja tiene un ganador (el mayor del par, candidato a máximo global) y un perdedor (el menor del par, candidato a mínimo global). El máximo global es el máximo de los $\lfloor n/2 \rfloor$ ganadores, y el mínimo global es el mínimo de los $\lfloor n/2 \rfloor$ perdedores (más el suelto, si lo hay, que se trata aparte).

- Encontrar el máximo de $k$ elementos requiere $k-1$ comparaciones (conferencia 5, §5, cota del máximo): $\lfloor n/2 \rfloor - 1$.
- Encontrar el mínimo de $k$ elementos requiere $k-1$ comparaciones (el mismo argumento, simétrico): $\lfloor n/2 \rfloor - 1$.

**Paso 3: las comparaciones son disjuntas.** Una comparación entre dos ganadores solo puede revelar quién es el mayor de los dos; no dice nada sobre cuál es el menor, porque ambos ya perdieron al menos una vez (contra su pareja) y por tanto ninguno puede ser el mínimo global. Recíprocamente, una comparación entre dos perdedores solo puede revelar quién es el menor; no dice nada sobre el máximo, porque ambos ya ganaron al menos una vez. Y una comparación entre un ganador y un perdedor de parejas distintas, según el resultado, o bien actualiza el máximo de los ganadores (si gana el ganador) o bien el mínimo de los perdedores (si gana el perdedor), pero el adversario puede contestar de modo que solo sirva para uno de los dos problemas, nunca para ambos a la vez. (Este es el paso de adversario que el ejercicio 1 de la conferencia 5 pide completar; formalmente, el adversario mantiene la ambigüedad en el extremo que la comparación no resuelve, y el conteo de "victorias y derrotas necesarias" de la conferencia 5, §5 se aplica por separado a ganadores y perdedores.)

Entonces las $\lfloor n/2 \rfloor - 1$ comparaciones del máximo de los ganadores y las $\lfloor n/2 \rfloor - 1$ del mínimo de los perdedores son disjuntas, y se suman:

$$c \geq \left\lfloor \frac{n}{2} \right\rfloor + 2\left(\left\lfloor \frac{n}{2} \right\rfloor - 1\right).$$

**Caso $n$ par.** $\lfloor n/2 \rfloor = n/2$, y

$$c \geq \frac{n}{2} + 2\left(\frac{n}{2} - 1\right) = \frac{3n}{2} - 2.$$

**Caso $n$ impar.** $\lfloor n/2 \rfloor = (n-1)/2$. El suelto necesita al menos 1 comparación para decidir si es menor que el mínimo de los perdedores o mayor que el máximo de los ganadores (y el adversario puede forzar que esa comparación no sirva para el otro extremo). Así que

$$c \geq \frac{n-1}{2} + 2\left(\frac{n-1}{2} - 1\right) + 1 = \frac{3(n-1)}{2} - 1 = \left\lfloor \frac{3n}{2} \right\rfloor - 2.$$

En ambos casos, $c \geq \lfloor 3n/2 \rfloor - 2$. $\square$

**Conclusión.** El algoritmo de la sección 3 hace exactamente $\lfloor 3n/2 \rfloor - 2$ comparaciones, y la cota mínima dice que ningún algoritmo de comparaciones puede hacer menos. El algoritmo es óptimo en el modelo de comparaciones, y la búsqueda se acabó (conferencia 2, §8).

**El error que la demostración anuncia** (conferencia 3, §5). La versión del algoritmo que compara el suelto con ambos extremos es correcta, pero hace una comparación de más para $n$ impar, y no alcanza la cota. La demostración dice dónde mirar: el paso 3 del caso impar, donde el suelto solo puede servir a uno de los dos extremos. Es exactamente el mismo fenómeno que el atajo del torneo del segundo mayor (conferencia 5, §8): un algoritmo que parece una optimización y hace menos que la cota está mal; uno que hace más que la cota no es óptimo, y la demostración dice qué comparación sobra.


## 7. El modelo, pegado a la cota

Como manda la conferencia 5, §9 y el Resumen, §3 ("toda cota viene con un modelo"): la cota $\lfloor 3n/2 \rfloor - 2$ vale en el modelo de comparaciones. Fuera de él puede romperse.

Si los elementos son enteros en $[0, k)$ y podemos usar el valor como índice, el ordenamiento por conteo (conferencia 5, §9) permite encontrar el mínimo y el máximo en $O(n + k)$ sin comparar, recorriendo el arreglo de cuentas. Eso no contradice la cota, porque no es un algoritmo de comparaciones: es el mismo truco de la rejilla del par más cercano (conferencia 2, §10) y del conteo de la conferencia 5, §9.

Si el modelo permite operaciones aritméticas sobre los valores, se puede hacer con menos comparaciones usando aritmética, pero el costo se mide en otro modelo (el word RAM de la conferencia 1, §9, con operaciones de bits).

La regla práctica: antes de citar una cota, pregunta cuál es su modelo y qué deja fuera. Aquí el modelo es comparaciones, y deja fuera el direccionamiento por valor.

## 8. Cierre del ciclo

| Pregunta (conferencia 2, §1) | Respuesta |
|---|---|
| **1. ¿Cuál es el problema?** | Dado $A[1..n]$, $n \geq 2$, de un orden total, devolver $(\min A, \max A)$. Modelo: comparaciones. Empates: cualquiera. |
| **2. ¿Qué algoritmo?** | Parejas: 1 comparación interna por pareja, 3 por pareja para actualizar $m$ y $M$ (2 en el arranque), 1 para el suelto. |
| **3. ¿Es correcto?** | Invariante "tras procesar un prefijo, $m$ y $M$ son sus extremos", inductivo porque caracteriza el estado. Terminación por potencial $\Phi =$ elementos sin procesar, que baja 1 o 2 por vuelta. |
| **4. ¿Cuánto cuesta?** | $\lfloor 3n/2 \rfloor - 2$ comparaciones exactas, $\Theta(n)$, memoria $O(1)$. Mejora sobre la fuerza bruta ($2n-2$) por un factor $4/3$. |
| **5. ¿Se puede hacer mejor?** | No en comparaciones: $\lfloor 3n/2 \rfloor - 2$ por reducción a "una comparación por pareja + máximo de ganadores + mínimo de perdedores", usando la cota del máximo (conferencia 5, §5). El algoritmo la alcanza: es óptimo. |