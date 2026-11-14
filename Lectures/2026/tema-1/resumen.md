# Resumen de la Parte I {.unnumbered #resumen-parte-1}

```{python echo=false output=asis}
import os
import random
import sys

sys.path.insert(0, os.path.abspath(".."))   # Lectures/2026
```

La Parte I termina aquí. Este resumen no trae material nuevo. Junta en pocas páginas lo
que los cinco capítulos contaron por separado, muestra las ideas que solo se ven
mirándolos juntos, y termina con ejercicios que mezclan capítulos, en el estilo de las
preguntas del examen final. Cada vez que algo se cita, se dice de qué capítulo y
sección sale, para que puedas volver a la demostración completa.

## 1. El mapa de la parte {#resumen-parte-1-1-el-mapa-de-la-parte}

El capítulo 2 organizó el trabajo en cinco preguntas: qué es el problema, qué
algoritmo lo resuelve, si es correcto, cuánto cuesta y si se puede hacer mejor. Cada
capítulo de la parte dio la herramienta para una de ellas.

| pregunta | capítulo | herramienta | ejemplo trabajado | error que atrapa |
|---|---|---|---|---|
| ¿cómo se mide? | 1 | modelo RAM, notación asintótica, tamaño en bits | primalidad por división | llamar polinomial a algo exponencial en bits |
| ¿qué algoritmo? | 2 | el ciclo completo | par más cercano | saltarse etapas del ciclo |
| ¿es correcto? | 3 | invariante, potencial, primer fallo | Boyer-Moore, Gale-Shapley | el atajo del contador |
| ¿cuánto cuesta? | 4 | análisis amortizado | cola, splay, union-find | subir a la raíz |
| ¿se puede mejor? | 5 | información, adversario, reducción | ordenar, mezclar, segundo mayor | el torneo que se salta un rival |

## 2. Lo que hay que llevarse de cada capítulo {#resumen-parte-1-2-lo-que-hay-que-llevarse-de-cada-capitulo}

Cada capítulo tiene su resumen al final. Aquí va una sola idea por capítulo: la que
los demás usan.

**Capítulo 1. Se mide en un modelo, y la entrada se mide en bits.** Un algoritmo no
cuesta segundos: cuesta operaciones en un modelo de cómputo. El modelo por defecto del
libro es la word RAM, con palabras de $w \ge \log_2 n$ bits y operaciones de costo 1
sobre ellas. El tamaño de la entrada es la cantidad de bits que ocupa, y por eso
probar divisores hasta $\sqrt{n}$ es exponencial aunque parezca un solo ciclo. Cuando
los números de un algoritmo crecen, se cuentan operaciones de bits.

**Capítulo 2. El ciclo de cinco preguntas, y la primera cota mínima.** El par más
cercano en el plano recorrió el ciclo entero: fuerza bruta en $\Theta(n^2)$, divide y
vencerás en $\Theta(n \log n)$ con el lema de la franja, cota $\Omega(n \log n)$ en
árboles de decisión algebraicos por reducción desde distinción de elementos, y un
algoritmo aleatorio de costo esperado lineal que la rompe. La conclusión fue que una
cota mínima es una afirmación sobre un modelo.

**Capítulo 3. Correcto quiere decir correctitud parcial más terminación.** La
parcial se demuestra con un invariante, que tiene que ser inductivo y no solo
verdadero (Boyer-Moore). La terminación, con un potencial que baja (Gale-Shapley). Las
propiedades globales del resultado, con el primer fallo: si algo sale mal, hay un
primer momento en que salió mal, y ese momento es imposible (optimalidad de
Gale-Shapley para quien propone).

**Capítulo 4. El costo amortizado es una garantía de peor caso sobre secuencias.**
No es un promedio y no tiene probabilidad. Se demuestra con un potencial que mide una
deuda: los elementos sin mudar en la cola, los caminos largos en el splay tree, el
crédito por grupos de rango en union-find. La suma funciona solo si el potencial
termina al menos donde empezó, o si se paga la diferencia aparte.

**Capítulo 5. La información cuenta salidas y el adversario cuenta trabajo.** La
información da $\lceil \log_2 n! \rceil$ para ordenar, pero solo $\log_2 n$ para el
máximo. El adversario da las cotas exactas del máximo ($n - 1$), de mezclar
($2n - 1$) y del segundo mayor ($n + \lceil \log_2 n \rceil - 2$). Y una cota mínima
demostrada sirve también para detectar algoritmos que están mal.

## 3. Cuatro ideas que atraviesan la parte

### Toda cota viene con un modelo

La misma lección aparece en los cinco capítulos, cada vez con un modelo distinto:

- **Máquina de Turing contra RAM** (capítulo 1, §3). La máquina de Turing define qué
  es computable, pero cambia los exponentes: para leer la celda $i$ el cabezal camina
  hasta ella, y reconocer un palíndromo, lineal en la RAM, cuesta $\Theta(n^2)$ en una
  cinta.
- **Multiplicación de costo 1** (capítulo 1, §9). Una RAM con celdas sin límite que
  multiplica en un paso, y que además tiene operaciones bit a bit, resuelve en tiempo
  polinomial los problemas que una máquina de Turing resuelve en espacio polinomial
  (Hartmanis y Simon), una clase que se cree mucho más grande. Por eso las celdas son
  palabras.
- **Árboles algebraicos contra la rejilla** (capítulo 2, §8 a §10). El par más
  cercano requiere $\Omega(n \log n)$ en árboles de decisión algebraicos, y el
  algoritmo aleatorio lo hace en tiempo esperado lineal usando la parte entera como
  dirección en una tabla hash, que ese modelo no tiene.
- **Sondeo de celdas** (capítulo 4, §9). La cota de Fredman y Saks para union-find
  vale en un modelo que regala todo el cómputo y solo cobra los accesos a memoria.
- **Comparaciones contra conteo** (capítulo 5, §9). Ordenar requiere
  $\Omega(n \log n)$ comparaciones, y el ordenamiento por conteo ordena enteros en
  $[0, k)$ en $O(n + k)$ usando los valores como índices. Las cotas polinomiales de la
  misma sección (palíndromos, propiedades de grafos, matrices booleanas, 3SUM) siguen
  la misma regla.

Antes de citar una cota, pregunta cuál es su modelo y qué deja fuera.

### Las pruebas no bastan, y la demostración dice dónde buscar

En cada capítulo plantamos un error en una variante que parecía correcta, y medimos
cuánto lo ven las pruebas.

| dónde | error plantado | qué vieron las pruebas | qué lo anunciaba |
|---|---|---|---|
| capítulo 1, §3 | rechazar al leer un blanco en la máquina de los palíndromos | ningún fallo con longitudes pares, 126 con impares | la cuenta de pasos, que solo termina en 2 con $n$ par |
| capítulo 2, §7 | 1 vecino en lugar de 7 en la franja | 19 fallos en 2000 instancias de $n = 12$, ninguno en 40 de $n = 400$ | el lema de la franja |
| capítulo 3, §5 | devolver el candidato si el contador es positivo | 0 % de fallos con mayoría plantada o alfabeto binario, 34 % con tres símbolos | la hipótesis "si hay mayoría" |
| capítulo 4, §5 y §6 | subir a la raíz en vez de splay | la cota del lema falla en 4 de 1500 accesos mezclados; en orden, cerca de $n/2$ rotaciones por acceso | el caso zig-zig del lema de acceso |
| capítulo 5, §8 | el torneo que se salta un rival | falla con probabilidad $1/(n-1)$: 0,12 % medido con $n = 1024$ | la cota del adversario |

Los cinco casos tienen la misma forma. La variante pasa las pruebas que uno escribe
primero, y falla en entradas con una estructura particular. La demostración nombra esa
estructura: palabras de longitud impar, puntos amontonados contra la recta de corte, arreglos sin mayoría, claves
recorridas en orden, el segundo mayor eliminado en la primera ronda. Probar verifica
que implementaste lo que pensaste. La demostración verifica que pensaste bien, y
además te dice qué probar.

### Experimentar antes de demostrar

La otra cara de la idea anterior. Correr el algoritmo y mirar sirve para proponer el
enunciado que después se demuestra:

- El experimento de 7 contra 1 vecino en la franja (capítulo 2, §7), leído al revés,
  sugiere que basta una constante pequeña, que es lo que el lema demuestra.
- El invariante vigilado de Boyer-Moore (capítulo 3, §4) comprueba en miles de
  prefijos que la partición en parejas se mantiene, antes de intentar demostrarlo.
El experimento también sirve después de demostrar, en la dirección contraria. El lema
de acceso ejecutado (capítulo 4, §5) no propone nada: comprueba la cota que se acaba
de demostrar, calculando el potencial en cada acceso, y la muestra cumpliéndose para
splay y fallando para subir a la raíz.

El experimento propone y la demostración decide. Ninguno reemplaza al otro.

### El caso típico no es la garantía

- En una nube de puntos uniforme, el par que mejora a $\delta$ en la franja resulta
  casi siempre consecutivo en el orden por $y$, aunque la franja tenga muchos puntos
  (capítulo 2, §6). El 7 del lema es una garantía, no una descripción.
- Gale-Shapley hace del orden de $n \ln n$ propuestas con listas al azar (243,7 en
  promedio para $n = 60$), no las $n^2$ de la cota (capítulo 3, §8).
- Una operación suelta de una estructura amortizada puede costar $\Theta(n)$: un
  `desencolar` que muda toda la pila, un acceso al fondo de un splay tree
  (capítulo 4, §10).

La garantía es la del peor caso, y el análisis tiene que cubrirlo aunque casi nunca
ocurra.

## 4. Cómo se ve una respuesta completa {#resumen-parte-1-4-como-se-ve-una-respuesta-completa}

Un ejercicio del libro pide casi siempre lo mismo: el algoritmo, su correctitud, su
costo y, cuando se puede, una cota mínima. El ejemplo que sigue es deliberadamente
fácil, para que lo que se vea sea la forma de la respuesta.

**Problema.** Dado un arreglo $A$ de $n \ge 1$ elementos de un orden total, devolver
el máximo. Modelo: comparaciones.

**Algoritmo.** Recorrer el arreglo guardando el mayor visto hasta ahora.

```{python continue}
def maximo(A):
    m = A[0]
    for x in A[1:]:
        if x > m:
            m = x
    return m
```

**Correctitud.** Invariante: después de procesar $A[1..i]$, $m$ es el máximo de
$A[1..i]$. *Inicialización*: con $i = 1$, $m = A[1]$. *Mantenimiento*: si $m$ es el
máximo de $A[1..i]$, después de comparar con $A[i+1]$ la variable tiene el mayor de
los dos, que es el máximo de $A[1..i+1]$. *Conclusión*: con $i = n$, $m$ es el máximo
de $A$. Termina porque el ciclo recorre una lista finita: el potencial es la cantidad
de elementos que faltan por visitar.

**Costo.** Exactamente $n - 1$ comparaciones, en todos los casos. Memoria $O(1)$.

**Comprobación.** Contamos las comparaciones con un envoltorio que las cuenta, y
comparamos el resultado con el `max` de Python, que hace de oráculo.

```{python continue}
class Contado:
    comparaciones = 0

    def __init__(self, v):
        self.v = v

    def __gt__(self, otro):
        Contado.comparaciones += 1
        return self.v > otro.v

random.seed(1)
for n in [1, 2, 10, 1000]:
    bien = 0
    for _ in range(200):
        A = [Contado(random.random()) for _ in range(n)]
        Contado.comparaciones = 0
        m = maximo(A)
        assert Contado.comparaciones == n - 1
        bien += m is max(A, key=lambda c: c.v)
    print(f"n = {n:>4}: correcto en {bien} de 200, {n - 1} comparaciones en cada una")
```

La comprobación no demuestra nada, pero confirma que el código es el algoritmo que
analizamos: 200 de 200 correctos para cada $n$, y siempre $n - 1$ comparaciones.

**Cota mínima.** Todo algoritmo de comparaciones necesita $n - 1$. Si al terminar un
elemento distinto del máximo declarado nunca perdió una comparación, se le puede subir
el valor por encima de todos sin contradecir ninguna respuesta, y el algoritmo habría
devuelto un máximo equivocado. Así que los $n - 1$ elementos restantes pierden al menos
una vez, y cada comparación tiene un solo perdedor (capítulo 5, §5). La cota de
información, $\lceil \log_2 n \rceil$, es mucho más baja y aquí no sirve (capítulo 5,
§4).

**Conclusión.** El algoritmo es óptimo en el modelo de comparaciones.

Esa es la forma: enunciado con su modelo, algoritmo, invariante con sus tres pasos,
terminación, costo exacto o asintótico, y cota mínima con su modelo. Una respuesta de
examen no tiene que ser más larga que esto para un problema de este tamaño.

## Resumen {#resumen-parte-1-resumen}

- Toda pregunta sobre un algoritmo se responde en un modelo: la word RAM por defecto,
  operaciones de bits cuando los números crecen, comparaciones para las cotas mínimas
  de ordenar y buscar.
- Un algoritmo está terminado cuando las cinco preguntas del capítulo 2 tienen
  respuesta: problema, algoritmo, correctitud, costo y cota mínima.
- La correctitud se demuestra con tres herramientas: invariante (parcial), potencial
  (terminación) y primer fallo (propiedades globales).
- El costo amortizado es peor caso sobre secuencias, y el potencial que lo demuestra
  mide una deuda.
- La información cuenta salidas, el adversario cuenta trabajo, y las dos cotas valen
  solo en su modelo.
- Las pruebas atrapan lo que uno piensa probar. La demostración dice qué entradas
  hay que probar, y una cota mínima demostrada detecta algoritmos que hacen menos de lo
  que se puede.

## Ejercicios {#resumen-parte-1-ejercicios}

Cada ejercicio dice entre paréntesis qué capítulos usa. Ninguno trae la solución:
como dice el capítulo 1, una solución bien presentada es parte de la respuesta.

1. **La cola, paso a paso** (capítulos 3 y 4). Traza la cola con dos pilas del
   capítulo 4, §2, sobre esta secuencia: encolar 1, 2, 3; desencolar; encolar 4, 5;
   desencolar tres veces; encolar 6; desencolar. Después de cada operación escribe el
   contenido de las dos pilas, el costo real y el potencial. Enuncia el invariante que
   relaciona el contenido de las dos pilas con el orden de la cola, y demuéstralo con
   los tres pasos del capítulo 3, §1.
2. **El torneo, paso a paso** (capítulos 3 y 5). Traza el torneo del capítulo 5, §7,
   sobre 31, 8, 57, 22, 40, 13, 65, 9. Escribe cada ronda, cuenta las comparaciones de
   las dos fases y compáralas con $n + \lceil \log_2 n \rceil - 2$. Enuncia el
   invariante que vale al final de cada ronda de la primera fase y explica por qué
   garantiza que el segundo mayor está entre los rivales directos del máximo.
3. **Pila con mínimo, y lo que no se puede** (capítulos 3, 4 y 5). Diseña una pila con
   `apilar`, `desapilar` y `minimo`, las tres en $O(1)$ en el peor caso, y demuestra
   su correctitud con un invariante. Después demuestra que ninguna estructura del
   modelo de comparaciones puede tener `insertar` y `extraer_minimo` con costo
   amortizado $O(1)$ las dos. ¿Por qué no contradice esto la primera parte?
4. **El contador en la cinta** (capítulos 1 y 4). Vuelve a la máquina de Turing del
   ejercicio 7 del capítulo 1, que suma 1 a un número binario con el cabezal en el bit
   menos significativo. Demuestra con un potencial que $m$ incrementos desde 0 cuestan
   $O(m)$ pasos en total, aunque uno solo pueda costar $\Theta(\log m)$. Di qué deuda
   mide tu potencial, y comprueba que el potencial termina al menos donde empezó.
5. **Buscar en una matriz ordenada** (capítulos 3 y 5). Una matriz $n \times n$ tiene
   filas y columnas ordenadas de forma creciente. Diseña un algoritmo que decida si
   contiene un valor $x$ (sin devolver su posición) con $O(n)$ comparaciones, y demuestra su correctitud con un
   invariante y su terminación con un potencial. Calcula la cota de información y
   demuestra con un adversario que hacen falta $\Omega(n)$ comparaciones. ¿Por qué la
   información no alcanza aquí, en el sentido del capítulo 5, §4?
6. ★ **La mediana de dos arreglos** (capítulos 2, 3 y 5). Dados dos arreglos
   ordenados de largo $n$, se busca el $n$-ésimo menor de los $2n$ elementos. Diseña un
   algoritmo de $O(\log n)$ comparaciones, demuestra su correctitud con un invariante
   y su terminación con un potencial, y da la cota de información. ¿Coinciden el
   algoritmo y la cota, salvo constantes?
7. **Dos candidatos y un atajo** (capítulo 3). El ejercicio 2 del capítulo 3
   generaliza Boyer-Moore con $k - 1$ candidatos. Toma $k = 3$: dos candidatos con su
   contador, para los elementos que aparecen más de $n/3$ veces. Escribe la versión
   correcta, con la segunda pasada, y la versión atajo que devuelve los candidatos con
   contador positivo sin verificarlos. Compáralas contra un oráculo que cuenta, con
   varios generadores de pruebas: alfabetos de 2, 3 y 5 símbolos, un elemento plantado
   más de $n/3$ veces y dos elementos plantados. Mide el porcentaje de fallos de cada
   versión con cada generador. ¿Qué generador no atrapa al atajo, y qué parte de la
   demostración lo explica? ¿Atrapa aquí el alfabeto binario al atajo? Mide con
   arreglos chicos ($n$ al azar entre 1 y 15) y con $n = 1000$. ¿Depende la respuesta
   de $n$? Explícalo con la demostración, y compara con lo que pasaba con el binario
   en el capítulo 3, §5.
8. **Splay sobre las claves en orden** (capítulos 1 y 4). Empezando desde el camino
   del capítulo 4, §6, se accede una vez a las claves $1, \dots, n$ en orden con
   splay. Calcula la cota que da el lema de acceso para el total, con el $\Phi_0$ del
   camino incluido, como en el capítulo 4, §5. Implementa el experimento para
   $n = 100, 200, 400, 800$, mide el total de rotaciones y el potencial al principio y
   al final, y compara con la cota en una gráfica log-log. ¿Es ajustada la cota para
   esta secuencia? ¿Cuánto del total paga el primer acceso? ¿Qué parte de la cuenta
   del lema es la que sobra?
9. **Una mezcla que ahorra una comparación** (capítulos 3 y 5). Una mezcla
   "optimizada" de dos listas ordenadas $A$ y $B$ de largo $n$ deja de comparar en
   cuanto a $A$ le queda un solo elemento: pone el resto de $B$ en la salida y después
   ese último elemento de $A$. Si $B$ se acaba antes, vuelca lo que queda de $A$.
   Cuenta cuántas comparaciones hace en el peor caso. Sin correrla, usa el capítulo 5,
   §6, para decidir si es correcta. Después caracteriza exactamente las entradas sobre
   las que falla, di qué fracción de las entradas son, y compara con el torneo del
   capítulo 5, §8: ¿cuál de los dos errores atrapan las pruebas aleatorias, y por qué?
10. **Ordenar con pocos valores** (capítulos 1 y 5). Cambia la hipótesis del
    teorema de ordenamiento: la entrada tiene $n$ elementos que toman solo $k$ valores
    distintos, cada uno exactamente $n/k$ veces, y los valores no se conocen de
    antemano. Demuestra que todo algoritmo que solo hace preguntas $a_i < a_j$, de dos
    respuestas, necesita al menos
    $n \log_2 k - 1{,}443\, n$ comparaciones en el peor caso, usando la cota de
    $\log_2 n!$ del capítulo 5, §3. Da un algoritmo de comparaciones que ordene en
    $O(n \log k)$. ¿Contradice esto el teorema del capítulo 5, §3? Compara la
    hipótesis que cambiaste aquí con la que usa el ordenamiento por conteo del
    capítulo 5, §9.
11. **Tutores de tesis** (capítulos 2 y 3). Los estudiantes de un año eligen tutor.
    Cada estudiante lista, en orden de preferencia, solo a los tutores que le
    interesan, y prefiere quedarse sin tutor antes que tener uno que no listó. Cada
    tutor ordena a los estudiantes que lo listaron y acepta a lo sumo uno. Modela el
    problema: define qué es una asignación y qué es una pareja bloqueante en este
    caso. Adapta Gale-Shapley con los estudiantes como proponentes, da su potencial y
    su costo en función del total de entradas de las listas, y demuestra que el
    resultado es estable con un argumento de primer fallo o por contradicción.
12. **El ciclo completo** (capítulos 2 a 5). Este es el formato de la pregunta larga
    del examen final. Un sensor guarda $n$ lecturas $A[1..n]$, y se busca un pico: una
    posición $i$ con $A[i] \ge A[i-1]$ y $A[i] \ge A[i+1]$, tomando $A[0] = A[n+1] =
    -\infty$. Recorre las cinco preguntas del capítulo 2: demuestra que siempre existe
    un pico, da un algoritmo de $O(\log n)$ consultas al arreglo, demuestra su
    correctitud con un invariante y su terminación con un potencial, y demuestra una
    cota mínima de $\Omega(\log n)$ consultas con un adversario. ¿Coinciden el
    algoritmo y la cota? (Pista para el adversario: las consultas devuelven valores,
    no respuestas sí o no, así que el árbol del capítulo 5 no se aplica tal cual.
    Mantén un intervalo tal que las respuestas dadas fuera de él crezcan hacia él,
    para que ningún pico pueda estar fuera, y contesta cada consulta de modo que
    sobreviva el pedazo más largo.)
