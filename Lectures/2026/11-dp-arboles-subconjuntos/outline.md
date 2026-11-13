# Outline: Capítulo 11, programación dinámica sobre árboles y subconjuntos

Estado: aprobado por el redactor y redactado (2026-11-13), pendiente de la revisión del libro. El documento está en `notas.md`.
Destino: `Lectures/2026/11-dp-arboles-subconjuntos/notas.md`, capítulo del libro.
Extensión objetivo: 6 000–7 000 palabras con el código.
Verificaciones: `.playground/libro-daa/verif/11/verif.py` (salida en `salida.txt`).

## Idea del capítulo

En Estructuras de Datos la programación dinámica fue siempre sobre una secuencia: un
prefijo, un par de prefijos, una capacidad. El estado venía dado por la forma de la
entrada. Este capítulo trabaja dos estructuras donde el estado hay que elegirlo, un
árbol y un conjunto, y la tesis es una sola: **el estado es lo que una parte de la
solución le tiene que contar al resto**. Si cuenta menos, la recurrencia es falsa. Si
cuenta más, la tabla es más grande de lo necesario.

- En un árbol, el subárbol de $v$ solo le cuenta al resto si $v$ está tomado o no. Eso
  da dos valores por vértice y un algoritmo en $O(n)$.
- En TSP, un camino parcial solo le cuenta al resto qué ciudades visitó y dónde
  terminó. Eso da $2^{n-1}$ conjuntos por $n-1$ finales en lugar de $(n-1)!$ órdenes.

El principio de optimalidad (Bellman) se presenta como una propiedad del estado
elegido, no del problema: el camino simple más largo es el contraejemplo que lo
muestra.

Error plantado: en el conjunto independiente, "si $v$ no está, tomo a todos sus hijos"
($\text{no}(v) = \sum \text{tom}(c)$). Pasa todas las pruebas sobre estrellas y sobre
caminos sin pesos, y falla en árboles al azar. La línea de la demostración que lo
anuncia es la que dice que, sin $v$, cada hijo queda libre.

## Estructura

### 1. El estado es la frontera

- Lo que se asume de Estructuras de Datos: subsecuencia común más larga, mochila
  entera, subsecuencia creciente más larga. Las tres sobre secuencias.
- El principio de optimalidad, enunciado como propiedad de un estado: la mejor
  solución desde un estado se arma con la mejor solución de los estados que alcanza.
- Contraejemplo (CLRS, el grafo de cuatro vértices $q, r, s, t$ en ciclo): el camino
  simple más largo de $q$ a $t$ es $q, r, t$, pero el de $q$ a $r$ es $q, s, t, r$ y el
  de $r$ a $t$ es $r, q, s, t$. Pegarlos repite vértices. Verificado por enumeración
  (verif §4). Las dos mitades compiten por los mismos vértices: el estado "extremos del
  camino" no dice cuáles se usaron.
- Lo que viene: árbol (dos valores por vértice) y subconjuntos (conjunto y final).

### 2. Conjunto independiente de peso máximo en un árbol

- Problema: árbol con pesos positivos en los vértices, conjunto sin dos vecinos, peso
  máximo. En un grafo general es NP-duro (capítulos 16 y 18). Lo que el árbol aporta:
  quitar un vértice lo parte en piezas que no se tocan.
- Ejemplo: el árbol de 10 vértices de la semilla 24 (padre de $i$ al azar entre los
  cuatro anteriores, pesos de 1 a 9). Óptimo 35, que no toma la raíz.
- Primer intento, un valor por vértice: $f(v) = \max(w(v), \sum_c f(c))$. Medido contra
  fuerza bruta: acierta en todas las estrellas y falla en el ejemplo (28 en vez de 35).
  Falla porque, si toma $v$, tira todo el subárbol: no sabe qué parte del mejor
  conjunto de cada hijo es compatible con $v$.

### 3. Dos valores por vértice

- $\text{tom}(v) = w(v) + \sum_c \text{no}(c)$ y
  $\text{no}(v) = \sum_c \max(\text{tom}(c), \text{no}(c))$. Respuesta
  $\max(\text{tom}(r), \text{no}(r))$.
- Código iterativo: los padres tienen índice menor, se recorre al revés. Oráculo por
  fuerza bruta sobre $2^n$ subconjuntos, $n \le 12$, en cuatro formas de árbol.
- **Figura**: el árbol con los dos valores por vértice y el conjunto óptimo marcado,
  recibiendo `tom`, `no` y el conjunto reconstruido.
- Variante equivalente con nietos, $f(v) = \max(w(v) + \sum_{g \text{ nieto}} f(g),
  \sum_c f(c))$: correcta (verif §1), un solo valor pero con dos niveles. Se menciona
  como la otra forma de contar lo mismo.

### 4. La demostración

- Lema de la frontera: si $S$ es independiente en $T_v$ y $v \notin S$, entonces
  $S \cap T_c$ es independiente en $T_c$ para cada hijo $c$, y la unión de conjuntos
  independientes de los $T_c$ es independiente en $T_v$ (no hay aristas entre
  subárboles distintos). Si $v \in S$, además ningún hijo está en $S$.
- Inducción sobre la altura, las dos desigualdades de cada fórmula (cota superior por
  restricción, alcanzabilidad por unión).
- El paso que todos se saltan: en $\text{no}(v)$ cada hijo queda **libre**, puede
  estar o no estar.
- Complejidad: cada vértice aparece una vez como hijo, $O(n)$. La versión recursiva se
  rompe en Python con un camino de más de 1 000 vértices (límite de recursión); por eso
  el código es iterativo.

### 5. El error plantado

- $\text{no}(v) = \sum_c \text{tom}(c)$.
- Baterías (400 árboles cada una, $n \le 12$, verif §1): estrellas con y sin pesos y
  caminos sin pesos: pasa todas. Árboles al azar: falla. El documento lo mide con su
  propio código.
- Por qué pasan esas baterías: en una estrella la raíz o todas las hojas; en un camino
  sin pesos alternar es óptimo. En ningún caso hace falta saltarse dos niveles.
- La demostración lo anunciaba: la desigualdad "$\le$" de $\text{no}(v)$ se prueba
  restringiendo un óptimo a cada $T_c$, y la restricción puede no contener a $c$.

### 6. Re-enraizamiento: la pregunta desde todos los vértices

- Pregunta nueva: para cada vértice $v$, el peso del mejor conjunto independiente de
  todo el árbol que contiene a $v$ (y el mejor que no lo contiene).
- Ingenuo: enraizar en cada vértice, $n$ veces $O(n)$, $O(n^2)$.
- Idea: al enraizar en $v$ en lugar de en la raíz, el único subárbol nuevo es "todo
  menos $T_v$", colgado de $p(v)$. Sus dos valores son los que **bajan** por la arista
  $p(v) \to v$; los de $T_v$ son los que **suben**.
- **Figura**: el árbol con una arista resaltada, los dos valores que suben y los dos
  que bajan, con los números calculados.

### 7. Re-enraizamiento: fórmulas, demostración y costo

- $\text{arr}_\text{tom}(c) = w(v) + \sum_{c' \ne c} \text{no}(c') + \text{arr}_\text{no}(v)$
  y $\text{arr}_\text{no}(c) = \sum_{c' \ne c} \max(\cdot) + \max(\text{arr}_\text{tom}(v),
  \text{arr}_\text{no}(v))$, donde $v = p(c)$.
- Demostración: es la recurrencia de §3 aplicada al árbol enraizado en $c$, donde el
  vecino $v$ tiene como hijos a los otros hijos de $v$ y a su propio padre.
- Costo: la suma sobre $c' \ne c$ sale de la suma total menos un término, $O(1)$ por
  arista, $O(n)$ en total. Funciona porque la suma se puede deshacer; con un máximo no
  (ejercicio 6).
- Código contra el ingenuo en 500 árboles (verif §3: 0 discrepancias) y tiempos
  medidos del ingenuo contra el re-enraizado.

### 8. Subconjuntos: el viajante

- TSP con matriz de distancias (no necesariamente simétrica). Fuerza bruta: fijar la
  ciudad 0 y probar los $(n-1)!$ órdenes.
- El estado que uno escribe primero: $g(S)$ = el camino más corto que visita $S$. No
  basta: la continuación depende de dónde termina. Dos caminos que visitan lo mismo
  y terminan en ciudades distintas no se pueden comparar.
- El estado $(S, j)$: lo que el resto necesita saber. El orden interno no importa:
  esa es la compresión de $(n-1)!$ a $2^{n-1}$.
- Bellman (J. ACM 9(1):61–63, 1962) y Held y Karp (J. SIAM 10(1):196–210, 1962),
  independientes. Verificados en Crossref (DOI 10.1145/321105.321111 y 10.1137/0110015).

### 9. Held-Karp

- $g(\{j\}, j) = d(0, j)$; $g(S, j) = \min_{i \in S \setminus \{j\}} g(S \setminus \{j\}, i)
  + d(i, j)$; respuesta $\min_j g(\{1..n-1\}, j) + d(j, 0)$.
- Código con máscaras de bits; orden de cálculo por máscara creciente (un subconjunto
  tiene máscara menor). Contra fuerza bruta en matrices asimétricas, $n \le 8$.
- Demostración por inducción sobre $|S|$, con el intercambio de sufijo: si el mejor
  camino que termina en $j$ pasa por $i$ antes, su prefijo es el mejor de
  $(S \setminus \{j\}, i)$, porque cambiarlo por otro mejor da un camino válido (los
  vértices de $S \setminus \{j\}$ no se repiten con $j$).

### 10. Cuánto cuesta y hasta dónde llega

- Experimento: contar estados y transiciones en el código, comparar con
  $2^{n-1}(n-1)^2$; la razón tiende a $1/4$ (el ejercicio 8 da la fórmula exacta).
- Cota: $O(2^n n^2)$ tiempo, $O(2^n n)$ memoria.
- **Figura**: tiempos de Held-Karp ($n = 6..14$) y fuerza bruta ($n = 6..10$; a
  $n = 11$ ya cuesta decenas de segundos por render), en escala log. Se imprime la
  extrapolación de la fuerza bruta a $n = 14$ con $13!/9!$.
- No es polinomial: es el primer algoritmo exacto exponencial del curso que mejora la
  fuerza bruta. El capítulo 19 demuestra que TSP es NP-duro, el 20 trata cuánto puede
  bajar la base, el 22 aproxima el caso métrico.

### 11. La regla

- Tabla: estado con menos información (un valor por vértice, $g(S)$): recurrencia
  falsa. Estado justo: correcta y barata. Estado con más (el orden del camino): correcta
  y $(n-1)!$.
- Hacia adelante: el capítulo 12 baja el costo de una DP con recurrencia ya correcta.

## Ejercicios

1. [traza] MWIS en un árbol de 9 vértices dado (semilla 1; óptimo único).
2. [entrada que rompe] El goloso de hojas con pesos.
3. [demostración] Sin pesos, el goloso de hojas es óptimo (intercambio, capítulo 9).
   Verificado: 0 fallos en 2 000 árboles (verif §2); con pesos, 772 fallos.
4. [modelar] Cobertura de vértices de peso mínimo en un árbol.
5. [modelar] Suma de distancias desde cada vértice, por re-enraizamiento.
6. [cambio de hipótesis] Diámetro con pesos en las aristas, y después la excentricidad
   de cada vértice: la agregación es un máximo y no se puede restar.
7. [traza] Held-Karp sobre 4 ciudades, tabla completa (matriz asimétrica dada).
8. [demostración] Número exacto de estados y transiciones; memoria por capas.
9. ★ [demostración] Suma sobre subconjuntos en $O(2^n n)$ frente a $O(3^n)$.
10. [implementar y medir] Hasta qué $n$ llega Held-Karp en un minuto en Python, cuánta
    memoria usa ahí, y qué se acaba primero con una implementación compilada.

## Audios (para el guion de grabación)

| Audio | Secciones |
|---|---|
| 1 | §1 |
| 2 | §2 |
| 3 | §3 |
| 4 | §4 |
| 5 | §5 |
| 6 | §6 |
| 7 | §7 |
| 8 | §8 |
| 9 | §9 |
| 10 | §10–§11 |

## Decisiones que quiero confirmar

- La semilla 10 del brief ("por qué se acaba antes la memoria") es falsa en Python:
  medido a ~800 ns por transición con la máquina cargada, un minuto llega a $n \approx 20$,
  donde la tabla ocupa cientos de MiB. La memoria se acaba primero solo en una versión
  compilada. El ejercicio pide medir y decidir.
- La semilla 8 (camino hamiltoniano con bits) queda fuera para dejar sitio a la mezcla
  de tipos de la guía; la semilla 5 (diámetro) se funde con el ejercicio 6.
- No se afirma nada sobre si $O(2^n n^2)$ es lo mejor posible para TSP: queda para el
  capítulo 20 y el epílogo.
