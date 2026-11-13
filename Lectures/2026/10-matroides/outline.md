# Outline: Capítulo 10, matroides

Estado: redactado (2026-11-13) en formato de libro. El documento está en `notas.md`.
Destino: `Lectures/2026/10-matroides/notas.md`, comprobado en `Lectures/2026/_check-10/`.
Extensión objetivo: 5 500–7 000 palabras con el código.
Verificaciones: `.playground/libro-daa/verif/10/` (scripts `v1` a `v8`, todos ejecutados).

## Idea del capítulo

El capítulo 9 demostró dos golosos, y cada uno necesitó su propio intercambio y su propia
medida que decrece. Este capítulo pregunta cuándo esa demostración se puede hacer una
sola vez para toda una familia de problemas. La respuesta es exacta: el goloso que
ordena por peso y agrega cada elemento si lo factible sigue siéndolo es óptimo **para
toda función de peso** si y solo si los conjuntos factibles forman un matroide (teorema
de Rado-Edmonds). El intercambio de los golosos pasa a ser un axioma.

Hay tres consecuencias. Kruskal sale como caso particular, con el union-find del
capítulo 4 como oráculo. Las tareas unitarias con plazos y penalizaciones se resuelven
con la misma línea de código, cambiando solo el oráculo. Y la frontera queda marcada: los
emparejamientos bipartitos son la intersección de dos matroides, el goloso ya no basta
(mide la mitad del óptimo en el peor caso) y con tres matroides el problema contiene el
camino hamiltoniano dirigido, que el capítulo 19 demuestra NP-completo.

El error plantado es un oráculo de tareas que comprueba la condición de conteo solo en
el plazo de la tarea nueva, y no en todos los instantes posteriores. El paso de la
demostración que lo anuncia es "al agregar $x$, sube $N_t$ para todo $t \ge d_x$".

## Estructura

### 1. Una demostración para muchos golosos
- Del capítulo 9: cada goloso tuvo su intercambio. La pregunta: ¿para qué estructuras
  basta el goloso genérico, con cualquier peso?
- El goloso genérico con un oráculo de independencia; su costo $O(n \log n + n\,T)$.

### 2. El experimento: bosques y emparejamientos del mismo grafo
- El diamante (4 vértices, 5 aristas). Todas las funciones de peso en $\{1,2,3\}^5$
  (243): el goloso sobre bosques nunca falla; sobre emparejamientos falla en 27.
  Verificado en `v1_diamante.py`.
- **Figura**: el primer peso donde falla (pesos 1, 2, 1, 2, 3): el goloso toma la
  diagonal de peso 3 y se queda en 3; el óptimo es 4.

### 3. Sistemas de independencia y matroides
- Definición: $\emptyset \in \mathcal I$, hereditario, intercambio. Bases y rango.
- Por qué los emparejamientos del diamante fallan el intercambio: $A$ = la diagonal,
  $B$ = dos aristas opuestas. Es el mismo par de la figura.
- Que todas las bases tienen el mismo tamaño queda como ejercicio 3; el capítulo no lo
  usa en ninguna demostración (la §5 lo evita a propósito).

### 4. Ejemplos: uniforme, partición, lineal, gráfico
- Uniforme y de partición, con el intercambio en una línea.
- Lineal: vectores linealmente independientes; intercambio por dimensión del espacio
  generado. Whitney (1935) definió matroide abstrayendo esto.
- Gráfico: los bosques. Demostración: un bosque con $k$ aristas en $n$ vértices tiene
  $n - k$ componentes; el que tiene más aristas tiene menos componentes, así que alguna
  de sus aristas une dos componentes del otro.
- **Figura**: grafo de 6 vértices y 9 aristas, bosque $A$ (4 aristas, 2 componentes),
  bosque $B$ (5 aristas); de las 4 aristas de $B \setminus A$ solo una une las dos
  componentes. Instancia encontrada en `v8_figura.py` (224 pares así).
- Código: comprobador de axiomas por fuerza bruta; bosques del diamante sí,
  emparejamientos no.

### 5. Rado-Edmonds, primera dirección: matroide implica goloso óptimo
- Teorema y demostración por dominancia de prefijos: $w(g_i) \ge w(o_i)$ para cada $i$,
  y $|O| \le |G|$, sin usar el lema de bases. El paso que todos se saltan: "el goloso
  la habría tomado" usa la herencia, porque el conjunto que tenía entonces era un
  subconjunto de $A$.
- Atribución (Schrijver, *Combinatorial Optimization*, Springer 2003, Teorema 40.1):
  Rado (1957) esta dirección; Gale (1968) y Edmonds (1971) la otra.

### 6. Rado-Edmonds, segunda dirección: sin intercambio hay pesos que lo rompen
- Construcción: $a + 2$ en $A$, $a + 1$ en $B \setminus A$, 0 en el resto. Cuenta exacta.
- Comprobación exhaustiva sobre los 167 sistemas de independencia de 4 elementos
  (68 matroides): ningún peso en $\{0..3\}^4$ hace fallar a un matroide, y la
  construcción hace fallar a los 99 que no lo son. La comprobación rota (mismos pesos
  en $A$ y $B$) deja de fallar en 69, así que la comprobación puede fallar
  (`v2_rado.py`).

### 7. Kruskal como caso particular
- Árbol de costo mínimo = base de peso máximo con $w = M - c$, porque todos los árboles
  generadores de un grafo conexo tienen $n - 1$ aristas.
- El oráculo es el union-find del capítulo 4. Código: el goloso genérico con union-find
  contra fuerza bruta en grafos al azar.

### 8. Tareas unitarias con plazos y penalizaciones
- Problema (Cormen et al., *Introduction to Algorithms*, 3.ª ed., §16.5).
- Lema: $A$ se puede atender a tiempo si y solo si $N_t(A) \le t$ para todo $t$.
  Demostración en las dos direcciones (orden por plazo).
- Es un matroide: la demostración del intercambio con el último $k$ donde
  $N_k(B) \le N_k(A)$.
- Instancia de 6 tareas, $d = (4,2,2,1,3,2)$, $w = (90,70,50,40,30,20)$: el goloso
  rechaza la 4 y la 6, penalización 60, igual a la fuerza bruta.
- **Figura**: el horario del goloso por plazo, con las rechazadas aparte.
- Comprobado contra fuerza bruta en 500 instancias (`v3_tareas.py`).

### 9. El error plantado: comprobar solo en su plazo
- La variante y la instancia mínima de 3 tareas: $d = (2,2,1)$, $w = (30,20,10)$.
- Baterías (`v4_error.py`): al azar falla en ~11 %; con plazos distintos o con las
  urgentes más caras, nunca. Instancia de la §8: penalización 100 en vez de 60.
- El paso que la anuncia: al agregar $x$ sube $N_t$ para todo $t \ge d_x$.

### 10. Intersección de dos matroides: el emparejamiento bipartito
- Emparejamientos bipartitos = dos matroides de partición (izquierda y derecha).
- El goloso falla; razón medida ≥ 1/2 en 3 000 instancias al azar, con un caso que
  llega a 1/2. La demostración es el ejercicio 10. Korte y Hausmann (1978): $1/k$ para
  $k$ matroides.
- Existe algoritmo polinomial para dos matroides (Lawler, 1975); el capítulo 13
  resuelve el caso bipartito con flujo.

### 11. Tres matroides: el camino hamiltoniano
- Camino hamiltoniano dirigido = común independiente de tamaño $n - 1$ en gráfico +
  entrada ≤ 1 + salida ≤ 1. Demostración. Del ciclo (capítulo 19) al camino partiendo
  un vértice. Comprobado en 400 digrafos (`v6_interseccion.py`).

### 12. La regla
- Antes de inventar un intercambio, pregunta si lo factible es un matroide.

## Ejercicios (11)

Cambios sobre las semillas del brief:
- 1: la verificación directa del matroide gráfico está en la §4; el ejercicio pide el
  otro camino, bosque ⟺ incidencias independientes sobre GF(2) (`v7`).
- 2: el cuerpo usa el diamante (5 aristas); el ejercicio pide el contraejemplo con
  menos aristas y la prueba de que no hay menor (3 aristas, `v7`).
- 8: el emparejamiento bipartito como intersección está en la §10; el ejercicio pasa a
  ramificaciones (bosque + entrada ≤ 1), que no son matroide y donde el goloso falla.
- 11 nuevo: implementar y medir, la versión $O(n \log n)$ con union-find por "último
  hueco libre" (la mezcla de la guía pide uno).

## Audios

| Audio | Secciones | Minutos |
|---|---|---|
| 1 | 1 y 2 | 5 |
| 2 | 3 y 4 | 6 |
| 3 | 5 | 5 |
| 4 | 6 y 7 | 6 |
| 5 | 8 | 6 |
| 6 | 9 | 4 |
| 7 | 10, 11 y 12 | 7 |

## Decisiones

- Rado 1957 (*Proc. London Math. Soc.* 7, 300–320) se cita según la bibliografía de
  Edmonds (1971) y el Teorema 40.1 de Schrijver; el artículo no se leyó. Gale (1968)
  se nombra solo a través de Schrijver.
- Nada sobre algoritmos de intersección más rápidos que Lawler: no verificado.
