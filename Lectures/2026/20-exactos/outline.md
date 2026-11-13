# Outline: Capítulo 20, resolver exacto un problema NP-duro

Estado: aprobado y redactado (2026-11-13), dentro del workflow del libro. El documento
está en `notas.md`.
Destino: `Lectures/2026/20-exactos/notas.md`, capítulo del libro (sin PDF por
conferencia).
Extensión objetivo: 5 500–7 000 palabras con el código.
Verificación: scripts en `.playground/libro-daa/verif/20/` (`alg.py`, `checks.py`,
`instancias.py`); la salida está en `salida.txt`.

## Idea del capítulo

Los capítulos 16 a 19 demostraron que mochila, vertex cover y conjunto independiente
son NP-completos. Eso dice que, si $P \ne NP$, ninguno tiene algoritmo polinomial en el
peor caso. No dice que haya que probar las $2^n$ soluciones. Este capítulo da tres
maneras de no probarlas todas, y cada una garantiza una cosa distinta:

- **Podar** (branch and bound, mochila): una cota superior del mejor valor de un
  subárbol permite no abrirlo. Garantiza la respuesta exacta. No garantiza nada sobre
  el tiempo: hay familias donde explora $\Theta(2^n/\sqrt{n})$ nodos (ejercicio 10).
- **Parametrizar** (vertex cover con $k$): la exponencial pasa de $n$ a $k$, y el
  algoritmo cuesta $O(2^k (n + m))$.
- **Bajar la base** (conjunto independiente): ramificar en un vértice de grado al menos
  3 da $T(n) \le T(n-1) + T(n-4) + 1$ y $O(1{,}3803^n)$ llamadas.

Y la pregunta que cierra: ¿cuánto se puede bajar la base? La ETH dice que no hasta
$2^{o(n)}$, y por la reducción del capítulo 18 eso alcanza a conjunto independiente.

El error plantado está en la cota: calcular la mochila fraccionaria en el orden de
entrada, sin ordenar por densidad. Da el valor de una solución fraccionaria factible,
que es una cota **inferior** del óptimo fraccionario, y poda ramas buenas. Tres
baterías naturales no lo atrapan, y una de ellas es la que sale de la reducción del
capítulo 19 (valores iguales a los pesos).

## Estructura

### 1. Tres maneras de no probarlo todo
- Dónde estamos: la tabla de NP-completos del capítulo 19, §12. Held-Karp del
  capítulo 11, §9 como primer exacto que mejora la fuerza bruta.
- Qué garantiza cada técnica del capítulo, en una lista. "Exacto" es la respuesta;
  el costo es lo que cambia.

### 2. Mochila: el árbol de decisiones
- Mochila 0-1 (capítulo 19, §11). El árbol binario: el nivel $i$ decide el objeto $i$.
  $2^{n+1} - 1$ nodos.
- Cómo se le ocurre a uno: si de un nodo no puede salir nada mejor que lo ya visto, no
  hace falta abrirlo. Lo que falta es una cota superior barata.
- Código `mochila_bb` con contador de nodos y registro para la figura; oráculo
  `mochila_dp` (la DP de Estructuras de Datos) en 2 000 instancias.

### 3. La cota de la mochila fraccionaria
- Mochila fraccionaria: se puede meter una fracción de cada objeto.
- Lema 1: el óptimo fraccionario es al menos el entero (relajación: toda solución
  0-1 es fraccionaria).
- Lema 2: el goloso por densidad decreciente da el óptimo fraccionario. Demostración
  por intercambio (capítulo 9): si una solución óptima pone menos de lo que pone el
  goloso en el primer objeto donde difieren, se pasa peso de un objeto posterior, de
  densidad menor o igual, y el valor no baja.
- Corolario: la poda no pierde el óptimo. El paso que todo el mundo se salta: el
  lema 2 usa el orden por densidad.

### 4. El experimento
- Tabla: nodos con cota y sin cota para $n = 8, 10, \dots, 16$ (sin cota) y hasta 30
  (con cota), máximo de 20 instancias al azar. Medido en `verif/20`: con cota, 187
  nodos en $n = 20$ contra 1 320 280 sin cota.
- **Figura 1**: el árbol de branch and bound de la instancia de 6 objetos (semilla
  3: 14 nodos, 3 podados, contra 83 sin cota), con las ramas podadas en gris.

### 5. El error plantado: la cota sin ordenar
- La variante: misma cota, en el orden de entrada. El ejemplo chico que encontró la
  búsqueda: pesos $(5, 5, 1)$, valores $(2, 1, 8)$, $W = 5$: devuelve 2 y el óptimo
  es 8.
- Baterías, 2 000 instancias cada una: al azar con $n \le 10$, 643 mal; al azar con
  $n \le 3$, 19 mal; valores = pesos (la reducción del capítulo 19), 0; ya ordenadas
  por densidad, 0; capacidad = suma de pesos, 0.
- Qué parte de la demostración lo anunciaba: el lema 2 es lo único que usa el orden,
  y sin él el número es el valor de una solución factible, que es una cota inferior.

### 6. Lo que la poda no garantiza
- La poda no cambia el peor caso: ejercicio 10 (sin dar la familia). Si $P \ne NP$
  ningún algoritmo exacto es polinomial en el peor caso; sin suponer nada, el
  ejercicio 10 lo mide para este.
- Land y Doig (1960), *Econometrica* 28(3), pp. 497–520: el método nace para
  programación entera.

### 7. Vertex cover con $k$ chico
- Dónde estamos: vertex cover es NP-completo (capítulo 16, §10 y capítulo 18). Pero
  si $k$ es chico, probar los $\binom{n}{k}$ conjuntos cuesta $O(n^k m)$: polinomial
  para cada $k$ fijo, con $k$ en el exponente.
- Cómo se le ocurre a uno: cada arista obliga a uno de sus dos extremos.

### 8. El árbol de profundidad $k$
- Algoritmo `cover_k`: toma una arista $\{u, v\}$, prueba $u$ y prueba $v$, con $k - 1$.
- Teorema 3: correcto y con a lo sumo $2^{k+1} - 1$ nodos, $O(n + m)$ cada uno, así
  que $O(2^k (n + m))$.
- Oráculo: 1 500 grafos con $n \le 8$ y $k \le 4$.
- **Figura 2**: el árbol de búsqueda en el ciclo de 7 vértices con $k = 3$ (respuesta
  no, árbol completo de 15 nodos).
- Medición en un grafo de 300 vértices con un cover plantado de tamaño $k$: el árbol
  sale completo, $2^{k+1} - 1$ nodos, porque la primera arista elige primero el
  extremo que no está en el cover.

### 9. Complejidad parametrizada
- Definición: FPT es $f(k) \cdot n^{O(1)}$. Contra $n^{O(k)}$.
- La reducción del capítulo 16 $(G, k) \mapsto (G, n - k)$ preserva la respuesta,
  pero no el parámetro: ejercicio 8.
- Kernel: reducir en tiempo polinomial a una instancia de tamaño $g(k)$. Ejercicio 3.
- Chen, Kanj y Xia (2010), *Theoretical Computer Science* 411(40–42), pp. 3736–3756:
  $O(1{,}2738^k + kn)$ con espacio polinomial (comprobado en el resumen).

### 10. Conjunto independiente: ramificar en un vértice
- Si el grado máximo es a lo sumo 2, el grafo es caminos y ciclos: $\lceil c/2 \rceil$
  en un camino de $c$ vértices, $\lfloor c/2 \rfloor$ en un ciclo.
- Si no, $v$ de grado $d \ge 3$: o no está ($G - v$) o está ($G - N[v]$, $n - 1 - d \le
  n - 4$ vértices).
- Lema 4 (las dos ramas cubren todos los casos) y lema 5 (caminos y ciclos).
- Código con máscaras de bits, oráculo de fuerza bruta en 600 grafos con $n \le 12$.

### 11. La recurrencia
- Experimento primero: llamadas medidas en grafos al azar de grado medio 4, $n = 10,
  \dots, 40$, contra $C(n) = 1 + C(n-1) + C(n-4)$ y contra $2^n$.
- Teorema 6: $C(n) < 2\alpha^n$ con $\alpha$ la raíz real mayor que 1 de
  $x^4 = x^3 + 1$, $\alpha = 1{,}38028$. Truco: $D = C + 1$ cumple
  $D(n) = D(n-1) + D(n-4)$. Inducción.
- El cociente $C(n)/\alpha^n$ medido se estabiliza en 1,095.
- Ojo con el redondeo: $\alpha > 1{,}38$, así que lo demostrado es $O(1{,}3803^n)$, no
  $O(1{,}38^n)$.
- **Figura 3**: llamadas medidas, $C(n)$ y $2^n$ en escala logarítmica. Las medidas
  quedan muy por debajo de $C(n)$: la recurrencia es una cota superior, y el capítulo
  no demuestra que algún grafo la alcance.
- Tarjan y Trojanowski (1977), *SIAM J. Computing* 6(3), pp. 537–546: $O(2^{n/3})$
  (en el resumen del reporte técnico de Stanford de 1976). Xiao y Nagamochi (2017),
  *Information and Computation* 255, pp. 126–146: $1{,}1996^n n^{O(1)}$ con espacio
  polinomial.

### 12. ETH y SETH
- $s_3 = \inf\{\delta : \text{3-SAT en } O(2^{\delta n})\}$. ETH: $s_3 > 0$.
  Impagliazzo y Paturi (2001), "On the Complexity of k-SAT", *JCSS* 62(2),
  pp. 367–375. Consecuencia: no hay algoritmo $2^{o(n)}$ para 3-SAT.
- Por qué no basta la reducción del capítulo 18: $3m$ vértices, y $m$ puede ser
  $\Theta(n^3)$. El lema de esparcimiento (Impagliazzo, Paturi y Zane, 2001, *JCSS*
  63(4), pp. 512–530), enunciado sin demostrar.
- Teorema 7: con ETH, conjunto independiente no se resuelve en $2^{o(N)}$ con $N$
  vértices. Demostración completa a partir del lema.
- SETH: $\lim s_k = 1$. Impagliazzo y Paturi lo dejan como problema abierto en la
  versión de 1999. Qué dice: para $k$-SAT con $k$ grande, nada mucho mejor que $2^n$.
- Lo que la ETH no dice: no fija la base de conjunto independiente.

### 13. La regla
- Tres garantías distintas: la respuesta (poda), la exponencial en $k$ (parámetro), la
  base (recurrencia). Y la regla: **una garantía de tiempo de un algoritmo exacto es
  una recurrencia demostrada, no una poda que funciona en las pruebas.**

### Resumen y ejercicios
1. [traza] Branch and bound a mano: pesos $(8, 8, 2, 6, 10)$, valores
   $(9, 8, 14, 15, 6)$, $W = 17$ (9 nodos, 3 podas según `instancias.py`).
2. [demostración] La cota del hijo es a lo sumo la del padre; y si la solución
   fraccionaria de un nodo es entera, el nodo no necesita ramificar.
3. [demostración] Kernel de grado alto para vertex cover: $O(k^2)$ aristas.
4. [demostración] Vector de ramificación $(a, b)$ general: $O(\alpha^n)$ con
   $x^{-a} + x^{-b} = 1$.
5. [modelar] Reglas de grado 1 y 2 para conjunto independiente, su vector y si mejoran
   la base global.
6. [modelar] Suma de subconjuntos con encuentro a mitad de camino; ★ sin el factor $n$.
7. [implementar y medir] Ramificar en orden de densidad o en el de entrada, con la
   cota bien calculada.
8. [cambio de hipótesis] Conjunto independiente parametrizado por $k$: qué se rompe.
9. [demostración] Con ETH, vertex cover no tiene $2^{o(k)} n^{O(1)}$.
10. [entrada que rompe] Familia con al menos $2^n / \mathrm{poly}(n)$ nodos.

## Audios (tentativo)

| Audio | Secciones | Minutos |
|---|---|---|
| 1 | 1 y 2 | 5 |
| 2 | 3 | 5 |
| 3 | 4 y 5 | 6 |
| 4 | 6 y 7 | 4 |
| 5 | 8 y 9 | 6 |
| 6 | 10 | 5 |
| 7 | 11 | 5 |
| 8 | 12 y 13 | 7 |

Total estimado: 43 minutos.

## Decisiones

- **Cambios a las semillas del brief.** La 2 pedía demostrar que la fraccionaria es
  cota válida, que el cuerpo demuestra (lemas 1 y 2) porque el error plantado depende
  de eso: pasa a monotonía de la cota. La 4 pedía resolver $T(n) = T(n-1) + T(n-4)$,
  que es el teorema 6: pasa al vector general $(a, b)$. La 9 tenía la dirección al
  revés: un 3-SAT en $2^{o(n)}$ no dice nada de conjunto independiente por una
  reducción 3-SAT $\le_p$ IND; la dirección útil es la contraria, y con ETH. Pasa a
  vertex cover con parámetro $k$. La 3 no nombra a Buss: no pude ver la fuente
  primaria de la atribución.
- **$O(1{,}3803^n)$ y no $O(1{,}38^n)$.** El plan dice $1{,}38$; la raíz es
  $1{,}380278$, mayor, así que el redondeo hacia abajo es una afirmación falsa.
- **Downey y Fellows fuera.** La W[1]-completitud de conjunto independiente con
  parámetro $k$ solo la vi citada en fuentes secundarias; el texto dice que no se
  conoce algoritmo FPT y no cita.
- **Schöning (4/3)ⁿ para 3-SAT fuera**: no pude leer el resumen.
