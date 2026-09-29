---
theme: note
css: notas.css
title: "Conferencia 5: cotas mínimas"
vars:
  figure-label: "Figura"
  figure-ref-label: "figura"
execute:
  interpreters:
    python: ["uv", "run", "--quiet", "--python", "3.14", "--with", "tesserax", "python", "-"]
---

# Conferencia 5: cotas mínimas

::: meta
Diseño y Análisis de Algoritmos · Ciencia de la Computación · MatCom · 2026
:::

En la conferencia 2 cambiamos una vez la pregunta, de "cuánto cuesta este algoritmo" a
"cuánto cuesta cualquiera", y la respondimos con una reducción desde un teorema que
citamos sin demostrar. Hoy aprendemos a demostrar cotas mínimas nosotros mismos. Vamos
a trabajar en el modelo de comparaciones, que es el más simple donde todo se puede
hacer con papel y lápiz, y a ver dos herramientas, cada una con su límite. Al final la
cota mínima va a cambiar de papel: además de decir cuánto cuesta un problema, va a
servir para detectar algoritmos que están mal.

```{python echo=false output=asis}
import math
import os
import random
import sys
from itertools import permutations

sys.path.insert(0, os.path.abspath(".."))   # Lectures/2026, donde vive figuras.py
import figuras as F
```

## 1. De este algoritmo a cualquier algoritmo

Para decir algo sobre **todos** los algoritmos hay que decir primero qué es un
algoritmo. En esta clase, un algoritmo del **modelo de comparaciones** solo puede
acceder a los datos preguntando si $a_i < a_j$. Puede hacer todo el cómputo que quiera
con los índices y con las respuestas, pero sobre los valores solo sabe lo que le
dijeron las comparaciones. Su costo es el número de preguntas. Ordenamiento por
inserción, mergesort, heapsort, la búsqueda binaria y el máximo por recorrido son
todos algoritmos de este modelo.

Recuerda la conferencia 2: una cota mínima vale en su modelo, y fuera de él puede
romperse. La sección 9 vuelve sobre esto con el ordenamiento.

Hay tres maneras de demostrar una cota mínima, y las tres tienen nombre:

- **Información**: contar cuántas respuestas distintas tiene que poder dar el
  algoritmo.
- **Adversario**: imaginar un oponente que contesta las preguntas para que el
  algoritmo aprenda lo menos posible.
- **Reducción**: mostrar que un algoritmo rápido para este problema daría uno rápido
  para otro problema que ya sabemos difícil. Es lo que hicimos con Ben-Or en la
  conferencia 2, y es la herramienta del Tema 3 entero.

En Estructuras de Datos vieron enunciado que ordenar por comparaciones cuesta
$\Omega(n \log n)$. Hoy se demuestra, y vemos hasta dónde llega esa técnica.

## 2. Árboles de decisión

Fijemos $n$ y un algoritmo de comparaciones. La primera pregunta que hace no depende
de la entrada, porque todavía no sabe nada. La segunda depende solo de la respuesta a
la primera, y así sucesivamente. Todas las ejecuciones posibles del algoritmo forman
entonces un **árbol de decisión**: cada nodo interno es una comparación, con una rama
por respuesta, y cada hoja es una salida. El costo en el peor caso es la **altura**
del árbol.

**Cómo se le ocurre a uno.** El árbol no hay que dibujarlo a mano. Corre el algoritmo
sobre todas las entradas posibles, anota las preguntas de cada ejecución y pega las
ejecuciones por donde coinciden.

```{python continue}
def ordenar_por_insercion(A, menor):
    A = list(A)
    for i in range(1, len(A)):
        j = i
        while j > 0 and menor(A[j], A[j - 1]):
            A[j], A[j - 1] = A[j - 1], A[j]
            j -= 1
    return A
```

```{python continue echo=false output=asis}
def _arbol_de_decision(n):
    """Corre ordenamiento por inserción sobre las n! permutaciones y pega las
    ejecuciones en un árbol."""
    raiz = {}
    nombres = [f"a{F.sub(i + 1)}" for i in range(n)]
    for valores in permutations(range(n)):
        valor = dict(zip(nombres, valores))
        camino = []

        def menor(x, y):
            r = valor[x] < valor[y]
            camino.append((f"{x} < {y}", r))
            return r

        salida = ordenar_por_insercion(nombres, menor)
        nodo = raiz
        for pregunta, r in camino:
            assert nodo.setdefault("pregunta", pregunta) == pregunta
            nodo = nodo.setdefault(r, {})
        nodo["hoja"] = "<".join(salida)

    def a_tupla(nodo):
        if "hoja" in nodo:
            return ("hoja", nodo["hoja"])
        return (nodo["pregunta"], a_tupla(nodo[True]), a_tupla(nodo[False]))

    return a_tupla(raiz)

print(F.arbol_comparaciones(_arbol_de_decision(3), ident="arbol-insercion",
      pie="El árbol de decisión de ordenamiento por inserción para n = 3, obtenido "
          "corriendo el algoritmo sobre las seis permutaciones. Seis hojas, una por "
          "orden posible, y altura 3."))
```

La @fig-arbol-insercion es el árbol de ordenamiento por inserción para $n = 3$. Tiene
seis hojas, una por cada orden posible de tres elementos, y altura 3. Ningún
algoritmo puede ordenar tres elementos con dos comparaciones, y la sección siguiente
dice por qué.

## 3. El argumento de información

Un árbol binario de altura $h$ tiene a lo sumo $2^h$ hojas: cada nivel duplica, como
mucho, los nodos del anterior. Si un problema tiene $L$ salidas distintas que el
algoritmo tiene que poder dar, el árbol tiene al menos $L$ hojas, y entonces
$$h \ge \log_2 L.$$

**Ordenamiento.** Un algoritmo que ordena tiene que poder producir cualquiera de las
$n!$ permutaciones, así que $h \ge \log_2 n!$. Para ver cuánto es, acotamos la suma de
logaritmos por una integral, porque $\log_2$ es creciente:
$$\log_2 n! = \sum_{k=1}^{n} \log_2 k \ge \int_1^n \log_2 x \, dx
= n \log_2 n - (n - 1)\log_2 e \ge n \log_2 n - 1{,}443\, n.$$

**Teorema.** Todo algoritmo de ordenamiento por comparaciones hace, en el peor caso, al
menos $\lceil \log_2 n! \rceil \ge n \log_2 n - 1{,}443\,n$ comparaciones.

¿Está cerca de lo que hacen los algoritmos reales? Contemos el peor caso exacto de
mergesort, recorriendo **todas** las permutaciones para $n \le 8$.

```{python continue}
def mezclar(I, D, cuenta, registro=None):
    R, i, j = [], 0, 0
    while i < len(I) and j < len(D):
        cuenta[0] += 1
        if registro is not None:
            registro.append((I[i], D[j]))
        if I[i] <= D[j]:
            R.append(I[i])
            i += 1
        else:
            R.append(D[j])
            j += 1
    return R + I[i:] + D[j:]

def mergesort(A, cuenta):
    if len(A) <= 1:
        return list(A)
    m = len(A) // 2
    return mezclar(mergesort(A[:m], cuenta), mergesort(A[m:], cuenta), cuenta)

peor_mergesort, informacion = [], []
print(f"{'n':>3} {'mergesort, peor caso':>21} {'⌈log₂ n!⌉':>10}")
for n in range(2, 9):
    peor = 0
    for P in permutations(range(n)):
        cuenta = [0]
        mergesort(list(P), cuenta)
        peor = max(peor, cuenta[0])
    peor_mergesort.append(peor)
    informacion.append(math.ceil(math.log2(math.factorial(n))))
    print(f"{n:>3} {peor:>21} {informacion[-1]:>10}")
```

```{python continue echo=false output=asis}
print(F.grafica_barras([f"n = {n}" for n in range(2, 9)],
      {"mergesort": peor_mergesort, "⌈log₂ n!⌉": informacion},
      titulo_y="comparaciones", ident="mergesort-vs-informacion",
      pie="Peor caso exacto de mergesort, recorriendo todas las permutaciones, contra "
          "la cota de información. La diferencia es de una comparación a partir de "
          "n = 5."))
```

En este rango la diferencia es de una sola comparación. Para $n$ grande crece, pero
despacio: cuando $n$ es potencia de 2, el peor caso de mergesort es exactamente
$n \log_2 n - n + 1$, y la cota es $n \log_2 n - 1{,}443\,n$, así que se separan en
unas $0{,}44\,n$ comparaciones. Coinciden en el término principal, que es lo que dice
que mergesort es óptimo salvo por el término lineal. El ejercicio 8 pregunta qué
pasaría con un algoritmo que prometiera menos.

**Búsqueda en un arreglo ordenado.** Hay $n + 1$ salidas posibles: una de las $n$
posiciones, o "no está". Así que hacen falta $\lceil \log_2 (n+1) \rceil$
comparaciones de tres vías, y la búsqueda binaria las alcanza. Es óptima.

## 4. Cuándo la información no alcanza

El argumento de información cuenta salidas. Cuando la salida es pequeña pero el
trabajo para justificarla es grande, se queda corto.

- **El máximo.** Hay $n$ salidas posibles, así que la información da $\log_2 n$. Pero
  todo el mundo sabe que el máximo cuesta $n - 1$ comparaciones. El árbol no lo ve,
  porque cuenta respuestas, no el trabajo de descartar a los demás candidatos.
- **Mezclar dos listas ordenadas de largo $n$.** Hay $\binom{2n}{n}$ maneras de
  intercalarlas, y el algoritmo de mezcla usa $2n - 1$ comparaciones.
- **El segundo mayor.** Hay $n(n-1)$ salidas si contamos el par (mayor, segundo), y el
  torneo de la sección 7 usa $n + \lceil \log_2 n \rceil - 2$.

```{python continue}
print(f"{'n':>5} {'mezclar: info':>14} {'mezclar: real':>14} "
      f"{'2º mayor: info':>15} {'2º mayor: real':>15}")
for n in [4, 16, 64, 256, 1024]:
    info_mezcla = math.log2(math.comb(2 * n, n))
    info_segundo = math.log2(n * (n - 1))
    real_segundo = n + math.ceil(math.log2(n)) - 2
    print(f"{n:>5} {info_mezcla:>14.1f} {2 * n - 1:>14} "
          f"{info_segundo:>15.1f} {real_segundo:>15}")
```

Para mezclar, la información queda a una distancia de $\frac{1}{2}\log_2 n$ más una
constante: cerca, pero no llega. Para el segundo mayor queda en $2 \log_2 n$ contra
algo lineal: no sirve para nada. En los dos casos el costo está en **verificar** la
respuesta, no en **elegirla**, y para eso hace falta otra herramienta.

## 5. El adversario

La idea es cambiar de punto de vista. En lugar de fijar una entrada y mirar qué hace
el algoritmo, imaginamos que el algoritmo juega contra un **adversario** que contesta
las comparaciones. El adversario no se compromete con ninguna entrada al principio:
solo tiene que contestar de forma **consistente**, es decir, de manera que en todo
momento exista al menos una entrada que daría todas las respuestas dadas hasta ahora.

La cota sale así. Si el algoritmo termina y todavía quedan dos entradas consistentes
con todas las respuestas pero con salidas correctas distintas, el algoritmo se
equivocó en una de las dos. Entonces un algoritmo correcto tiene que seguir
preguntando hasta que eso no pase, y la cota mínima es cuántas preguntas puede forzar
el adversario.

**El máximo, $n - 1$.** Aquí el adversario ni siquiera necesita estrategia. Si al
terminar hay un elemento $x \neq m$ que nunca perdió una comparación, el adversario
puede subir el valor de $x$ por encima de todos sin contradecir ninguna respuesta, y
entonces el máximo sería $x$, no $m$. Así que los $n - 1$ elementos distintos del
máximo tienen que perder al menos una vez. Cada comparación tiene un solo perdedor, así
que hacen falta al menos $n - 1$ comparaciones.

El adversario es la herramienta de contradicción de la conferencia 3 aplicada a todas
las ejecuciones a la vez: si el algoritmo pregunta poco, existe una entrada donde se
equivoca, y el adversario es la receta para construirla.

## 6. Mezclar: $2n - 1$

**Teorema.** Mezclar dos listas ordenadas de largo $n$ requiere $2n - 1$ comparaciones
en el peor caso, y el algoritmo de mezcla las alcanza.

*Demostración.* La mezcla usa a lo sumo $2n - 1$: cada comparación saca un elemento a
la salida, y el último sale sin comparar. Para la cota mínima, el adversario contesta
como si la entrada fuera la **intercalada perfecta**
$$a_1 < b_1 < a_2 < b_2 < \dots < a_n < b_n.$$
Esa cadena tiene $2n - 1$ pares de vecinos, y cada par tiene un elemento de cada
lista. Supongamos que un algoritmo termina sin haber comparado un par de vecinos, por
ejemplo $a_i$ con $b_i$. Intercambiemos los valores de $a_i$ y $b_i$. Las dos listas
siguen ordenadas, porque $a_i$ y $b_i$ son vecinos en la cadena y nada queda entre
ellos. Todas las comparaciones que el algoritmo hizo dan la misma respuesta, porque
ninguna involucraba a los dos a la vez y el orden con el resto no cambió. Pero la
salida correcta cambió: ahora $b_i$ va antes que $a_i$. El algoritmo da la misma
salida para las dos entradas, así que se equivoca en una. Por tanto compara los
$2n - 1$ pares. $\square$

```{python continue}
for n in [4, 16, 64]:
    A, B = list(range(0, 2 * n, 2)), list(range(1, 2 * n, 2))   # intercaladas
    cuenta, registro = [0], []
    mezclar(A, B, cuenta, registro)
    print(f"n = {n:>3}: {cuenta[0]} comparaciones, 2n - 1 = {2 * n - 1}")
```

```{python continue echo=false output=asis}
_cuenta, _registro = [0], []
mezclar(list(range(0, 10, 2)), list(range(1, 10, 2)), _cuenta, _registro)
_nombre = lambda v: ("a", v // 2) if v % 2 == 0 else ("b", v // 2)
print(F.intercalado(5, [(_nombre(x), _nombre(y)) for x, y in _registro],
      ident="intercalado",
      pie="La entrada intercalada con n = 5. Las líneas son las comparaciones que la "
          "mezcla hizo de verdad al correr sobre ella: exactamente los nueve pares de "
          "vecinos de la cadena, sin sobrar ninguno."))
```

La @fig-intercalado muestra las comparaciones que la mezcla hace sobre la entrada del
adversario: son exactamente los pares de vecinos. Esta cota es también el problema
8-6 de CLRS, que la plantea como ejercicio guiado.

## 7. El segundo mayor: $n + \lceil \log_2 n \rceil - 2$

El segundo mayor por fuerza bruta es fácil: encuentra el máximo con $n - 1$
comparaciones, quítalo, y encuentra el máximo de lo que queda con $n - 2$ más. Son
$2n - 3$. ¿Se puede mejor?

**Cómo se le ocurre a uno.** El segundo mayor perdió contra el máximo en algún
momento, porque contra cualquier otro habría ganado. Así que no hace falta buscarlo
entre todos: basta buscarlo entre los que perdieron **contra el máximo**. El problema
es que el máximo por recorrido le puede ganar a $n - 1$ elementos. Hay que organizar
las comparaciones para que el máximo le gane a pocos.

**El torneo.** Los elementos juegan por parejas; los ganadores pasan a la ronda
siguiente, y así hasta que queda uno, que es el máximo. Son $n - 1$ comparaciones,
porque cada una elimina a un jugador. El máximo jugó una vez por ronda, y hay
$\lceil \log_2 n \rceil$ rondas. Su segundo es el mayor de sus rivales, que cuesta
$\lceil \log_2 n \rceil - 1$ comparaciones más. En total,
$n + \lceil \log_2 n \rceil - 2$.

```{python continue}
def torneo(A, saltar_primera=False):
    """Devuelve (segundo mayor, comparaciones). Cada jugador lleva la lista de a
    quiénes venció, en el orden de las rondas."""
    comparaciones = 0
    jugadores = [(x, []) for x in A]
    while len(jugadores) > 1:
        ronda = []
        for i in range(0, len(jugadores) - 1, 2):
            (a, va), (b, vb) = jugadores[i], jugadores[i + 1]
            comparaciones += 1
            ronda.append((a, va + [b]) if a > b else (b, vb + [a]))
        if len(jugadores) % 2:
            ronda.append(jugadores[-1])          # pasa de ronda sin jugar
        jugadores = ronda
    maximo, vencidos = jugadores[0]
    candidatos = vencidos[1:] if saltar_primera else vencidos
    segundo = candidatos[0]
    for c in candidatos[1:]:
        comparaciones += 1
        if c > segundo:
            segundo = c
    return segundo, comparaciones

random.seed(7)
print(f"{'n':>5} {'peor caso medido':>17} {'n + ⌈log₂ n⌉ - 2':>18}")
for n in [8, 64, 1024]:
    peor = 0
    for _ in range(2000):
        A = random.sample(range(10 * n), n)
        segundo, c = torneo(A)
        assert segundo == sorted(A)[-2]
        peor = max(peor, c)
    print(f"{n:>5} {peor:>17} {n + math.ceil(math.log2(n)) - 2:>18}")
```

```{python continue echo=false output=asis}
def _cuadro(A):
    jugadores = [(x, (str(x), None, None)) for x in A]
    while len(jugadores) > 1:
        ronda = []
        for i in range(0, len(jugadores) - 1, 2):
            (a, ta), (b, tb) = jugadores[i], jugadores[i + 1]
            ronda.append((max(a, b), (str(max(a, b)), ta, tb)))
        jugadores = ronda
    maximo, arbol = jugadores[0]

    def marcar(t):
        if t[1] is None:
            return ("*" + t[0], None, None)
        hijos = []
        for h in (t[1], t[2]):
            if h[0] == str(maximo):
                hijos.append(marcar(h))
            else:
                hijos.append(("+" + h[0],) + h[1:])
        return ("*" + t[0], *hijos)

    return marcar(arbol)

random.seed(3)
_A8 = random.sample(range(10, 100), 8)
print(F.cuadro_torneo(_cuadro(_A8), ident="torneo",
      pie=f"El torneo sobre {', '.join(map(str, _A8))}. En azul, los partidos del "
          f"máximo; en naranja, sus tres rivales. El segundo mayor, {sorted(_A8)[-2]}, "
          f"es uno de ellos, y solo hay que compararlos entre sí."))
```

El peor caso medido coincide con la fórmula. Ahora la pregunta de la clase: ¿se puede
con menos?

**Teorema.** Todo algoritmo de comparaciones que encuentra el segundo mayor de $n$
elementos hace, en el peor caso, al menos $n + \lceil \log_2 n \rceil - 2$
comparaciones.

*Demostración.* Va en dos pasos: primero, qué tiene que saber el algoritmo al
terminar; después, cómo el adversario lo obliga a pagar por saberlo.

*Qué tiene que saber.* Sea $m$ el máximo y $s$ el segundo, según la entrada que el
adversario termine fijando. Al terminar:

- Todo elemento distinto de $m$ perdió alguna comparación. Si dos elementos $u$ y $v$
  nunca perdieron, el adversario puede ponerlos a los dos por encima de todos, en
  cualquiera de los dos órdenes, y el segundo mayor sería $v$ o $u$ según cuál elija.
- De los elementos que perdieron **solo contra $m$**, hay exactamente uno, que es $s$.
  Si hubiera otro, $x$, los dos solo tendrían a $m$ por encima según las respuestas,
  y el adversario podría poner cualquiera de los dos inmediatamente debajo de $m$.

Sea $k$ el número de elementos que fueron comparados con $m$. Todos perdieron contra
$m$, y todos salvo $s$ perdieron además contra algún otro elemento. Contemos derrotas:
cada comparación produce exactamente una. Los $n - 1$ elementos distintos de $m$
pierden al menos una vez, y los $k - 1$ rivales de $m$ distintos de $s$ pierden al
menos dos. En total hay al menos $(n - 1) + (k - 1)$ derrotas, y otras tantas
comparaciones.

*Cómo obliga el adversario a que $k$ sea grande.* Cada elemento empieza con **peso**
1. Cuando el algoritmo compara $x$ con $y$:

- Si los dos tienen peso positivo, gana el de mayor peso (en empate, cualquiera), y el
  ganador absorbe el peso del perdedor, que queda en 0.
- Si solo uno tiene peso positivo, gana ese, y los pesos no cambian.
- Si los dos tienen peso 0, contesta de forma consistente con lo que ya dijo.

Los elementos con peso positivo son exactamente los que nunca perdieron, y la suma de
los pesos es siempre $n$. Las respuestas son consistentes: un elemento con peso
positivo nunca perdió, así que declararlo ganador no puede cerrar un ciclo. Al
terminar, solo $m$ no perdió nunca, así que su peso es $n$. El peso de $m$ solo sube
cuando le gana a un elemento de peso positivo, que tiene a lo sumo su mismo peso, así
que en cada una de esas comparaciones su peso a lo sumo se duplica. Para llegar de 1 a
$n$ necesita al menos $\lceil \log_2 n \rceil$ de ellas. Entonces
$k \ge \lceil \log_2 n \rceil$, y el total es al menos
$n + \lceil \log_2 n \rceil - 2$. $\square$

La @fig-torneo muestra por qué el torneo es óptimo: organiza las comparaciones para
que el máximo le gane exactamente a $\lceil \log_2 n \rceil$ rivales, que es lo mínimo
que el adversario permite.

## 8. La cota mínima como detector de errores

En las conferencias 2, 3 y 4 plantamos un error en un algoritmo, y la demostración de
correctitud o de costo decía dónde buscarlo. Aquí el error lo detecta la cota mínima.

Mira de nuevo el torneo. El rival de la primera ronda del máximo perdió en el primer
partido. Parece un candidato flojo, y saltárselo ahorra una comparación. Es el
parámetro `saltar_primera` del código de arriba. La versión con atajo usa
$n + \lceil \log_2 n \rceil - 3$ comparaciones: **una menos que la cota mínima**.

Sin mirar el código, sabemos que está mal: ningún algoritmo correcto puede hacer menos
que la cota. Y la demostración dice en qué entrada falla. El atajo nunca compara al
rival de la primera ronda con ningún otro rival del máximo, así que ese rival perdió
solo contra el máximo, y queda más de un elemento en esa situación. El adversario pone
a ese rival como segundo mayor. Construyamos la entrada, y midamos con qué frecuencia
lo detectan pruebas al azar.

```{python continue}
n = 16
A = [n - 1, n - 2] + random.sample(range(n - 2), n - 2)   # el 2º mayor, en la 1ª ronda
print("entrada construida:", A)
print("torneo:", torneo(A)[0], "  atajo:", torneo(A, saltar_primera=True)[0],
      "  verdad:", sorted(A)[-2])
print()

random.seed(11)
print(f"{'n':>5} {'pruebas':>8} {'fallos del atajo':>17} {'1/(n-1)':>9}")
for n, pruebas in [(8, 20_000), (64, 20_000), (1024, 4_000)]:
    fallos = 0
    for _ in range(pruebas):
        A = random.sample(range(10 * n), n)
        fallos += torneo(A, saltar_primera=True)[0] != sorted(A)[-2]
    print(f"{n:>5} {pruebas:>8} {100 * fallos / pruebas:>16.2f}% "
          f"{100 / (n - 1):>8.2f}%")
```

El atajo falla exactamente cuando el segundo mayor es el rival de la primera ronda del
máximo, que en una entrada al azar pasa con probabilidad $1/(n-1)$. Con 1024
elementos, una de cada mil pruebas. Una batería de pruebas al azar con arreglos grandes
no lo ve casi nunca. La cota mínima lo vio sin correr nada.

La lección cierra la serie de errores plantados del tema. **Una cota mínima es
también una especificación**: un algoritmo que dice hacer menos trabajo que una cota
demostrada está mal, aunque pase todas las pruebas. Y si parece estar bien, lo que hay
que revisar es en qué modelo trabaja, que es la sección siguiente.

## 9. Qué modelo

Ordenar cuesta $\Omega(n \log n)$ comparaciones. Pero si los valores son enteros en un
rango $[0, k)$ conocido, se puede ordenar sin comparar nada.

```{python continue}
def ordenar_por_conteo(A, k):
    cuenta = [0] * k
    for x in A:                      # usa el valor como índice: no compara
        cuenta[x] += 1
    salida = []
    for v in range(k):
        salida.extend([v] * cuenta[v])
    return salida

random.seed(4)
n, k = 100_000, 1000
A = [random.randrange(k) for _ in range(n)]
cuenta = [0]
assert ordenar_por_conteo(A, k) == mergesort(A, cuenta) == sorted(A)
print(f"mergesort: {cuenta[0]:,} comparaciones")
print(f"conteo:    0 comparaciones y {n + k:,} pasos (n + k)")
print(f"⌈log₂ n!⌉: {math.ceil(math.lgamma(n + 1) / math.log(2)):,}")
```

El ordenamiento por conteo cuesta $O(n + k)$, por debajo de $n \log n$ cuando
$k = O(n)$. No contradice el teorema de la sección 3, porque no es un algoritmo de
comparaciones: usa los valores como **índices** de un arreglo. Es el mismo truco que la
rejilla de la conferencia 2, que usaba la parte entera como dirección para romper la
cota de Ben-Or.

La regla es la de la conferencia 2, y ya la vimos aplicarse muchas veces: una cota
mínima viene con su modelo pegado. La cota de ordenamiento vale en comparaciones. La de
Ben-Or, en árboles de decisión algebraicos. La de Fredman y Saks de la conferencia 4,
en sondeo de celdas. Antes de citar una cota, hay que saber cuál es su modelo y qué
deja fuera.

## 10. Cierre del Tema 1

Con esta conferencia termina el Tema 1. Después de cinco conferencias tenemos las
herramientas para las cinco preguntas del ciclo: medir en un modelo (conferencia 1),
recorrer el ciclo entero (conferencia 2), demostrar correctitud (conferencia 3),
analizar el costo de secuencias de operaciones (conferencia 4) y acotar por abajo
(esta). El documento de cierre del tema junta todo en unas pocas páginas y trae
ejercicios que mezclan las cinco conferencias.

El Tema 2 cambia de eje. Las clases dejan de organizarse por pregunta y pasan a
organizarse por técnica de diseño: divide y vencerás, golosos, programación dinámica,
flujos. Las cinco preguntas siguen ahí, y siguen siendo las que se evalúan.

## 11. Resumen

- Una cota mínima es una afirmación sobre todos los algoritmos de un modelo. En el
  modelo de comparaciones, el costo es el número de preguntas $a_i < a_j$.
- Un algoritmo de comparaciones es un árbol de decisión, y su peor caso es la altura.
- **Información**: con $L$ salidas posibles, la altura es al menos $\log_2 L$.
  Ordenar cuesta al menos $\lceil \log_2 n! \rceil \ge n \log_2 n - 1{,}443\,n$, y
  mergesort está a distancia lineal de esa cota.
- La información cuenta salidas, no trabajo. Para el máximo da $\log_2 n$ en vez de
  $n - 1$.
- **Adversario**: un oponente que contesta de forma consistente y fuerza preguntas. Da
  $n - 1$ para el máximo, $2n - 1$ para mezclar y $n + \lceil \log_2 n \rceil - 2$
  para el segundo mayor, y las tres cotas se alcanzan.
- La cota del segundo mayor sale de contar derrotas y de un adversario de pesos que
  obliga al máximo a jugar $\lceil \log_2 n \rceil$ veces. El torneo lo logra.
- Un algoritmo que hace menos que una cota demostrada está mal. El torneo que se salta
  un rival falla con probabilidad $1/(n-1)$, y la cota lo detecta sin pruebas.
- El ordenamiento por conteo no contradice la cota: no compara. Toda cota viene con su
  modelo.

## Ejercicios

1. **Máximo y mínimo a la vez.** Diseña un algoritmo que los encuentre con
   $\lceil 3n/2 \rceil - 2$ comparaciones, y demuestra con un adversario que no se
   puede con menos. (Pista: clasifica cada elemento según si ya ganó, ya perdió, las
   dos cosas o ninguna.)
2. Demuestra que decidir si un arreglo está ordenado requiere $n - 1$ comparaciones.
3. Mezclar una lista de largo $m$ con otra de largo $n$: da la cota de información en
   función de $m$ y $n$, y un algoritmo que la alcance cuando $m = 1$.
4. Demuestra que la mediana de 5 elementos se puede encontrar con 6 comparaciones, y
   que con 5 no alcanza.
5. **Distinción de elementos en el modelo de comparaciones.** Demuestra
   $\Omega(n \log n)$ con un árbol de decisión. ¿Por qué no basta contar salidas, si
   solo hay dos ("sí" o "no")?
6. El tercer mayor: extiende el torneo para encontrarlo y cuenta cuántas comparaciones
   usa en el peor caso. ¿Qué dice la cota de información?
7. Radix sort ordena $n$ enteros de $b$ bits en $O(n b / \log n)$ pasos usando dígitos
   de $\log_2 n$ bits. ¿En qué modelo? ¿Contradice la sección 3?
8. Alguien afirma tener un algoritmo de ordenamiento por comparaciones que hace a lo
   sumo $n \log_2 n - 2n$ comparaciones para todo $n$ grande. ¿Puede existir? Justifica
   con la sección 3.
