# Outline: Capítulo 19, Reducciones a secuencias y números

Estado: aprobado y redactado (2026-11-13), dentro del workflow del libro. El documento
está en `notas.md`.
Destino: `Lectures/2026/19-reducciones-numeros/notas.md`, capítulo del libro (sin PDF
por conferencia).
Extensión objetivo: 5 500–7 000 palabras con el código.
Verificación: scripts en `.playground/libro-daa/verif/19/` (`ham.py`, `ham_lib.py`,
`rapido.py`, `suma.py`, `suma2.py`, `doble.py`, `plantado.py`, `plantado2.py`).

## Idea del capítulo

Los capítulos 16 a 18 redujeron entre problemas de grafos donde la solución es un
**conjunto** de vértices, y un gadget es un pedazo de grafo que fuerza o prohíbe
elegir ciertos vértices. Este capítulo llega a dos clases de problemas donde la
solución tiene otra forma: un **orden** (ciclo hamiltoniano, TSP) y una **suma**
(suma de subconjuntos, mochila). La pregunta de diseño es dónde se esconde una elección
binaria en cada material: en el sentido en que se recorre una fila de vértices, y en
qué número se pone en la suma. Y en los dos casos el peligro es el mismo: que las
piezas se comuniquen por donde no estaba previsto (un ciclo que salta de una fila a
otra, un acarreo que pasa de una columna a la siguiente). Los vértices de separación y
la base 10 están ahí para cortar esa comunicación.

El error plantado es una reducción a suma de subconjuntos que mezcla dos convenciones
de libro: holguras 1 y 2 con meta 3 en la columna de la cláusula (la correcta con esas
holguras es meta 4). Toda instancia construida tiene solución, así que la batería de
fórmulas con asignación plantada no ve nada (0 fallos) y la batería de fórmulas
insatisfacibles falla en todas. Lo anunciaba la línea de la demostración que dice
"las holguras suman a lo sumo 3, uno menos que la meta".

## Estructura

### 1. Dos formas nuevas de solución
- Lo demostrado hasta aquí (capítulos 16, 17, 18): SAT, 3-SAT, independiente, clique,
  vertex cover, set cover, 3-coloración. Todas las soluciones son conjuntos.
- Ciclo hamiltoniano y suma de subconjuntos (definidos como certificados en el
  capítulo 16, ejercicio 1). Por qué ahí no sirve el triángulo del capítulo 18.
- 3-SAT con exactamente tres literales sobre variables distintas (capítulo 17, §10).

### 2. Una elección binaria dentro de un ciclo
- Un ciclo pasa por todos los vértices: la elección no puede ser "pasar o no pasar".
  Tiene que ser **cómo** pasar. Una fila de vértices con aristas en los dos sentidos se
  recorre entera de izquierda a derecha o de derecha a izquierda.
- Una cláusula como un vértice que solo se puede intercalar en un sentido: arcos
  $v_p \to c \to v_{p+1}$. Ejemplo de una variable y una cláusula, a mano.
- Cada cláusula necesita su propio par en cada fila (un recorrido hace un solo desvío
  entre dos vértices consecutivos).

### 3. La construcción
- Filas de $b = 3k + 3$ vértices; la cláusula $j$ usa las posiciones $3j$ y $3j + 1$;
  las posiciones $3j - 1$ (y $3k + 2$) son de separación. $s$, $t$, arcos entre
  extremos de filas consecutivas, $t \to s$.
- Literal positivo: $v_{i,3j} \to c_j \to v_{i,3j+1}$; negativo, al revés.
- Tamaño: $n(3k + 3) + k + 2$ vértices y $6nk + 8n + 6k + 1$ arcos (filas
  $2n(b - 1)$, entre filas y con $s$, $t$: $4n + 1$, cláusulas $6k$; recontado en el
  código).
- **Código ejecutable**: `a_hamiltoniano(clausulas, n)`.
- **Figura** (`rn-filas`): las filas, los vértices de cláusula y el ciclo que encontró
  el código para una asignación que cumple la fórmula del ejemplo.

### 4. El experimento
- Contar ciclos hamiltonianos con una búsqueda en profundidad con poda por
  alcanzabilidad, y compararlos con $\sum_a \prod_j t_j(a)$, donde $t_j(a)$ es el número
  de literales verdaderos de la cláusula $j$ con la asignación $a$. Coinciden en las 100
  fórmulas de `verif/19/ham.py` (n = 3, k ≤ 3) y en las del documento.
- El número sugiere el enunciado: cada ciclo es una asignación que cumple más la
  elección de un literal verdadero por cláusula. La demostración decide.
- La fórmula insatisfacible de 8 cláusulas sobre 3 variables da 0 ciclos (91 vértices,
  147 s en `verif/19`; no va en el documento por costo).

### 5. La demostración
- Teorema 1: 3-SAT $\le_p$ CICLO-HAMILTONIANO-DIRIGIDO. Pertenencia a NP.
- ⇒: recorrer cada fila según el valor, y desviar por $c_j$ desde la fila de un
  literal verdadero.
- Lema 2 (el paso que todo el mundo se salta): si el ciclo entra a $c_j$ desde la fila
  $i$, sale a la misma fila, al vértice vecino. Usa el vértice de separación: si no,
  $v_{i,3j-1}$ (positivo) o $v_{i,3j+2}$ (negativo) queda con un solo vecino libre.
  Escrita entera, los dos casos.
- ⇐: contraer los desvíos; en lo que queda, cada vértice interior de una fila solo
  tiene vecinos en su fila, así que la fila se recorre entera en un sentido; el orden de
  filas es forzado; la asignación sale del sentido y cada $c_j$ fue visitado en el
  sentido de un literal verdadero.

### 6. Del grafo dirigido al no dirigido
- Cada vértice $v$ en tres, $v_0 - v_1 - v_2$, y cada arco $u \to v$ como arista
  $u_2 - v_0$. Es la reducción de Karp (1972, p. 98), verificado en el escaneo.
- Teorema 3, las dos direcciones; el vértice del medio tiene grado 2 y fuerza el
  sentido. Con dos copias se rompe: el ejercicio 2 (verificado: 29 de 600 digrafos al
  azar con n = 3, 4 dan una respuesta distinta con dos copias, 0 con tres).
- **Código ejecutable**: programación dinámica sobre subconjuntos (la de Held-Karp del
  capítulo 11, §9, en versión de decisión) para comparar las respuestas en digrafos
  chicos.

### 7. TSP
- TSP de decisión: distancias enteras, presupuesto $B$. En NP.
- Teorema 4: distancia 1 en las aristas, 2 en las no aristas, $B = n$. Las dos
  direcciones. Las distancias 1 y 2 cumplen la desigualdad triangular, así que la
  versión métrica también es NP-completa. Hacia adelante: el capítulo 22 usa la misma
  reducción con otros pesos.
- **Código ejecutable**: Held-Karp contra la respuesta de ciclo hamiltoniano.

### 8. Suma de subconjuntos: una columna por restricción
- Cómo se le ocurre a uno: un número es un vector de dígitos si no hay acarreos. Una
  columna por variable (meta 1: exactamente uno de $y_i$, $z_i$) y una por cláusula.
- Primer intento: meta 1 en la columna de cláusula falla con dos literales verdaderos;
  meta "al menos 1" no existe en una suma exacta. Holguras 1 y 2, meta 4.
- **Código ejecutable**: `a_suma(clausulas, n)`, con la tabla del ejemplo.
- **Figura** (`rn-tabla`): la tabla de dígitos del ejemplo, con las filas elegidas
  para la asignación que encontró el código.

### 9. La demostración
- Teorema 5: 3-SAT $\le_p$ SUMA-DE-SUBCONJUNTOS. Sin acarreos: cada columna suma a lo
  sumo 6 < 10 (paso que todo el mundo se salta). Las dos direcciones.
- Tamaño: $2n + 2k$ números de $n + k$ dígitos. Polinomial en bits; el valor es del
  orden de $10^{n+k}$ (enlace con el capítulo 16, ejercicio 10).
- **Código ejecutable**: número de subconjuntos que suman $T$ contra número de
  asignaciones que cumplen, en fórmulas al azar. Coinciden (verificado en `suma.py`
  para bases 5 a 10; la base 4 y menores dan respuestas mal). La prueba de que
  coinciden es el ejercicio 5.

### 10. El error plantado
- Meta 3 con holguras 1 y 2. Batería con asignación plantada: 0 fallos. Batería de
  fórmulas insatisfacibles (las 8 cláusulas sobre tres de las variables más cláusulas
  al azar): falla en todas. Verificado en `plantado2.py` con 20 fórmulas insatisfacibles
  sacadas al azar: la correcta 0 con solución, la rota 20.
- Qué línea de la demostración lo anunciaba.

### 11. Mochila
- MOCHILA de decisión (pesos, valores, capacidad $W$, meta $V$). En NP.
- Teorema 6: SUMA $\le_p$ MOCHILA con $w_i = v_i = a_i$, $W = V = T$. Las dos
  direcciones. La KNAPSACK de Karp (1972, p. 95, problema 18) es exactamente la suma de
  subconjuntos (verificado en el escaneo).
- La tabla $O(nW)$ no contradice nada: el capítulo 16, ejercicio 10, y el capítulo 23
  (NP-dificultad fuerte, FPTAS).

### 12. Lo que queda demostrado
- La lista de once problemas, con el capítulo de cada reducción.
- **Figura** (`rn-mapa`): el árbol de reducciones de la Parte III.
- Karp llegó a ciclo hamiltoniano desde vertex cover (NODE COVER) y a KNAPSACK desde
  EXACT COVER (figura 1, p. 96, verificado en el escaneo). Las rutas no son únicas.

### 13. La regla
- "Una reducción es correcta cuando las piezas solo se comunican por donde la
  demostración dice": vértices de separación, base sin acarreos, holguras que no llenan
  el hueco del cero. Se comprueba en las instancias no.

### Resumen y ejercicios

1. [traza] Grafo de ciclo hamiltoniano para una fórmula de 3 variables y 2 cláusulas;
   los ciclos de una asignación. (Cambiado: la semilla pedía 2 variables, pero una
   cláusula de 3-SAT tiene tres variables distintas, capítulo 17, §10.)
2. [entrada que rompe] Dos copias por vértice en lugar de tres: un digrafo sin ciclo
   hamiltoniano cuyo no dirigido sí lo tiene. (Cambiado: la semilla pedía las dos
   direcciones de la triplicación, que ahora están demostradas en la §6.)
3. [traza] La tabla de suma de subconjuntos de una fórmula dada y su objetivo.
4. [demostración] Por qué la base 10 no tiene acarreos; la base más chica sin acarreos
   (7) y la base más chica en que la reducción sigue siendo correcta (5, con meta 4;
   verificado: base 4 falla, 5 a 10 aciertan en 241 fórmulas de `suma2.py`).
5. [demostración] La reducción a suma de subconjuntos es parsimoniosa (agregado).
6. [modelar] Partición desde suma de subconjuntos, y empaquetamiento en cajas desde
   partición (dos semillas juntas para no tener tres de modelar).
7. [modelar] Camino más largo es NP-completo (desde camino hamiltoniano, capítulo 16,
   ejercicio 6).
8. [cambio de hipótesis] Reducir SAT con cláusulas de cualquier largo directo a suma de
   subconjuntos: cuántas holguras y qué base. (Cambiado: la semilla "TSP con
   distancias 1 y 2" es la reducción del cuerpo, §7.)
9. ★ [demostración] Si 3-SAT se redujera a suma de subconjuntos con $T$ acotado por un
   polinomio en el tamaño de la fórmula, $P = NP$. Relación con la tabla $O(nW)$.
   (Cambiado: la semilla "mochila NP-completa y $O(nW)$" la responde el capítulo 16,
   ejercicio 10, y la pertenencia está en la §11.)
10. [implementar y medir] Componer 3-SAT → ciclo dirigido → no dirigido → TSP y medir
    el tamaño de cada instancia; comprobar con Held-Karp en fórmulas chicas.
11. [entrada que rompe] Base 2: una fórmula insatisfacible cuya instancia tiene
    solución (verificado: existen; la de 8 cláusulas sobre 3 variables es una).

## Decisiones que quiero confirmar

- La disposición de las filas ($3k + 3$ vértices, pares en $3j$, $3j + 1$) es la de los
  libros de texto; no la atribuyo a nadie porque no comprobé su origen.
- Sin vértices de separación (filas de $2k + 2$) aparecen ciclos que saltan de una fila
  a otra por un vértice de cláusula (16 ciclos contra 12 en una cláusula), pero la
  fórmula insatisfacible de 8 cláusulas sigue sin ciclo. No sé si la variante es
  correcta en general, así que no la uso como error plantado ni como ejercicio, y la
  prosa solo dice que la demostración usa el vértice de separación.
