# Outline: Capítulo 18, reducciones desde 3-SAT a grafos

Estado: aprobado y redactado (2026-11-13), pendiente de la revisión del libro. El documento está en `notas.md`.
Destino: `Lectures/2026/18-reducciones-grafos/notas.md`, capítulo del libro.
Extensión objetivo: 6 000–7 000 palabras con el código.
Verificación: `.playground/libro-daa/verif/18/` (`gadget.py`, `aristas.py`,
`reducciones.py`, `color4.py`, `ejercicios.py`, `intento.py`, `capitulo.py`).

## Idea del capítulo

El capítulo 16 dejó tres problemas de grafos que están en P o fuera de P juntos, y el
17 dejó 3-SAT como primer problema NP-completo cómodo. Este capítulo une las dos cosas
con dos reducciones, y lo que enseña es cómo se construyen: con **gadgets**, piezas
chicas de la instancia destino que imitan una pieza de la fórmula.

Una reducción desde 3-SAT tiene que representar tres cosas: una elección por variable
(verdadero o falso), la coherencia entre las apariciones de una misma variable, y que
cada cláusula tenga un literal verdadero. En conjunto independiente, la cláusula es un
triángulo (elige a lo sumo un literal) y la coherencia son aristas entre literales
opuestos. En 3-coloración la elección es un color, la coherencia es un triángulo con el
vértice base, y la cláusula es un gadget de seis vértices que no se puede colorear
cuando sus tres literales son falsos.

El error plantado cambia una sola arista del gadget de cláusula. La reducción rota dice
"sí" a todas las fórmulas, así que solo falla en las insatisfacibles, que entre las
fórmulas chicas al azar son raras. Una enumeración de los 8 casos del gadget la atrapa
en una línea. De ahí la regla: **un gadget se verifica solo, por enumeración, antes que
la reducción entera.**

## Estructura

### 1. Lo que falta (corta)

- El corolario 7 del capítulo 16 espera una sola reducción desde un NP-completo. El 17
  dio 3-SAT. Este capítulo da 3-SAT ≤ₚ conjunto independiente y 3-SAT ≤ₚ 3-coloración.
- Las tres cosas que una reducción desde 3-SAT tiene que representar: elección,
  coherencia, cláusula. Definición informal de gadget, con el antecedente de las
  ventanas del capítulo 17, §4.

### 2. 3-SAT ≤ₚ conjunto independiente

- Cómo se le ocurre a uno: el certificado de 3-SAT es una asignación, pero lo que se
  *comprueba* cláusula por cláusula es "este literal la hace verdadera". Un conjunto
  independiente de tamaño $m$ elige un testigo por cláusula. Primer intento: un vértice
  por literal. Falla porque un mismo literal puede ser el testigo de dos cláusulas y
  el conjunto lo contaría una vez (es el ejercicio 1 en forma de traza, y no se
  desarrolla).
- Construcción: un vértice por aparición, un triángulo por cláusula, una arista entre
  cada par de apariciones opuestas ($x$ y $\lnot x$). $k = m$.
- **Figura 1**: el grafo de una fórmula de 3 cláusulas, con el independiente que
  encontró el código resaltado.
- Teorema 1 con las dos direcciones. La vuelta usa: un triángulo aporta a lo sumo un
  vértice, así que $m$ vértices son uno por cláusula; no hay $x$ y $\lnot x$ a la vez,
  así que se puede leer una asignación; las variables sin testigo valen cualquier cosa.
- Tamaño: $3m$ vértices, $3m$ aristas de triángulos y a lo sumo $\binom{3m}{2}$ en total.

### 3. Probarla contra el oráculo

- Código: `a_independiente`, un decisor de independiente por ramificación con
  máscaras de bits, la fuerza bruta de 3-SAT. Fórmulas al azar con $n \le 5$,
  $m \le 12$. Medido en `verif/18/reducciones.py`: 400 casos, 395 sí y 5 no, ninguno
  mal. Para el capítulo se elige la batería de modo que haya instancias no (m grande
  para n chico).
- Leer la asignación desde el independiente: la traza de la figura 1.
- Karp (1972, p. 97) reduce SAT a CLIQUE con vértices $\langle \sigma, i \rangle$,
  aristas entre cláusulas distintas y literales no opuestos, y $k = p$. Ese grafo es
  exactamente el complemento del nuestro: comprobado en `reducciones.py` en 100
  fórmulas, y se comprueba en el capítulo.

### 4. Clique y vertex cover

- Corolario 2: conjunto independiente, clique y vertex cover son NP-completos (el
  corolario 7 del capítulo 16 más el teorema 1 y el lema 3 del capítulo 16).
- Qué dice esto del capítulo 11, §2 (árboles) y del capítulo 20 (bajar la base de la
  exponencial): la dificultad es del peor caso de grafos generales.

### 5. Vertex cover ≤ₚ set cover

- Set cover: universo $U$, familia de subconjuntos, $k$; ¿hay $k$ conjuntos cuya unión
  es $U$? Está en NP.
- Construcción: $U = E$, un conjunto $S_v$ por vértice con las aristas que lo tocan,
  el mismo $k$. Es la de Karp, p. 98 ("NODE COVER ∝ SET COVERING"), verificada en el
  escaneo.
- Teorema 3 con las dos direcciones. Prueba contra el oráculo.
- Nota hacia adelante: set cover vuelve en el capítulo 21 con el goloso de razón $H_n$.

### 6. 3-coloración

- Definición, en NP, 2-coloración en P (BFS que alterna, capítulo 16, §3).
- Las piezas: el **triángulo de la paleta** $T, F, B$ (verdadero, falso, base), que
  fija los nombres de los colores; el **gadget de variable**, el triángulo
  $x_i, \lnot x_i, B$, que obliga a cada literal a ser $T$ o $F$ y a los dos opuestos
  a tener colores distintos. Elección y coherencia salen juntas, en un triángulo.
- Lo difícil es la cláusula: un gadget que se pueda colorear si y solo si alguno de
  sus tres literales es $T$.

### 7. El gadget de cláusula

- Cómo se le ocurre a uno: un "O" de dos entradas con un triángulo $p, q, r$, con $p$
  unido a la entrada $a$ y $q$ unido a $b$. El experimento antes de la demostración:
  la tabla de colores posibles de $r$ según las entradas. Medido en
  `verif/18/gadget.py`: $F, F \to$ solo $F$; $T, T \to$ solo $T$; mezcla $\to$
  cualquiera. **No calcula el O**: con $a = T$ y $b = F$, $r$ puede ser $F$. Solo
  garantiza "si las dos son $F$, $r$ es $F$" y "si alguna es $T$, $r$ puede ser $T$".
- Dos "O" encadenados, $(a, b) \to r_1$ y $(r_1, c) \to r_2$, y $r_2$ unido a $F$ y a
  $B$, que lo obliga a ser $T$. 6 vértices nuevos y 12 aristas por cláusula.
- Lema 4 con las dos direcciones, por casos del "O".
- **Figura 2**: los 8 casos de $(a, b, c)$, cada uno con un coloreo que encontró la
  enumeración o con la marca de que no existe (solo $F, F, F$).
- Código: enumeración de los $3^6 = 729$ coloreos internos para cada uno de los 8
  casos, y el número de coloreos que quedan en cada caso.

### 8. 3-SAT ≤ₚ 3-coloración

- Construcción completa: $3 + 2n + 6m$ vértices, $3 + 3n + 12m$ aristas.
- Teorema 5, las dos direcciones: de una asignación a un coloreo (el lema 4 da el de
  cada gadget, y los gadgets solo se tocan a través de los literales y de $T, F, B$);
  de un coloreo a una asignación (renombrar colores para que la paleta sea $T, F, B$,
  leer $x_i$ del color de su vértice, el lema 4 da que cada cláusula tiene un literal
  $T$).
- Código: la reducción, un decisor de 3-coloración por vuelta atrás con propagación y
  partición en componentes, y la batería exhaustiva: **todas** las fórmulas de 3-SAT
  sobre las variables $x_1, x_2, x_3$ sin cláusulas repetidas, que son 255, con una
  sola insatisfacible (la de los 8 patrones de signo). Medido en `verif/18/color4.py`:
  0,5 s; más 200 fórmulas al azar con $n \le 5$, 194 sí y 6 no, peor caso 0,26 s.
- **Figura 3**: la instancia completa para $(x_1 \lor x_2 \lor x_3) \land
  (\lnot x_1 \lor \lnot x_2 \lor x_3)$, 21 vértices y 36 aristas, coloreada con el
  coloreo que devolvió el código.
- Historia: Karp (1972, p. 99) reduce 3-SAT a número cromático con $r + 1$ colores, un
  número que crece con la instancia. Que 3 colores ya bastan para la dificultad lo
  demostró Stockmeyer (1973), incluso en grafos planares ("Planar 3-colorability is
  polynomial complete", *ACM SIGACT News* 5(3), pp. 19–25; Crossref).

### 9. El error plantado

- Variante: la segunda "O" toma su entrada de $p_1$ en vez de $r_1$. Una arista
  cambiada de sitio. Medido en `gadget.py`: el gadget se colorea en los 8 casos, así
  que la reducción rota contesta "sí" a toda fórmula.
- Tres baterías: fórmulas con una asignación plantada (0 fallos, no puede fallar),
  fórmulas al azar chicas (falla exactamente en las no, que son pocas), y la
  enumeración de los 8 casos del gadget (falla en $F, F, F$ al primer intento).
- La demostración lo anunciaba: la dirección "⇐" del lema 4 usa que la entrada de la
  segunda "O" es la *salida* de la primera, la única que está obligada a $F$.

### 10. Qué hace un buen gadget

- Se comunica con el resto solo por una interfaz chica (los tres literales y la
  paleta), así que la demostración global se arma con hechos locales.
- Su especificación es una tabla finita sobre la interfaz, y se verifica por
  enumeración: 8 casos por $3^6$ coloreos internos.
- Prohíbe exactamente lo que tiene que prohibir y nada más: no calcula el O, solo
  deja sin salida el caso $F, F, F$. Pedirle más es pedir un gadget más grande.
- Tiene tamaño constante, así que la reducción es lineal en la fórmula.
- Comparación con las ventanas del capítulo 17, §4: la misma idea con otro material.

### 11. La regla, y el mapa

- La regla: un gadget se verifica solo y por enumeración, en las dos direcciones,
  antes de probar la reducción completa. Una reducción probada con instancias al azar
  solo ve el lado de la respuesta que domina.
- **Figura 4**: el mapa de reducciones demostradas hasta aquí (SAT → 3-SAT → IS →
  clique, VC → set cover; 3-SAT → 3-coloración) con los capítulos, y las del 19 en
  línea punteada.

### Resumen

### Ejercicios

1. [traza] Grafo de independiente de una fórmula de 4 cláusulas dada; un independiente
   de tamaño 4 a mano; leer la asignación. Después, el mismo grafo con un vértice por
   literal: ¿sigue habiendo uno de tamaño 4?
2. [implementar y medir] Contar los coloreos internos del gadget en cada uno de los 8
   casos, y quitar cada una de las 12 aristas por turno: ¿cuáles sobran? (Verificado:
   solo $r_2$–$B$.)
3. [demostración] 3-coloración ≤ₚ 4-coloración; $k$-coloración NP-completa para todo
   $k \ge 3$.
4. [modelar] Set cover ≤ₚ hitting set y vuelta; vertex cover como hitting set con
   conjuntos de tamaño 2.
5. [demostración] Conjunto dominante es NP-completo, desde vertex cover. (Verificado:
   la construcción con un vértice por arista funciona quitando los vértices aislados,
   y falla sin quitarlos: 251 instancias mal en `ejercicios.py`.)
6. [cambio de hipótesis] 2-coloración y conjunto independiente en bipartitos están en
   P (König enunciado, por el corte mínimo del capítulo 13). ¿Qué pieza de cada
   reducción no existe?
7. [entrada que rompe] El gadget con $r_2$ unido a $T$ y $B$ en vez de a $F$ y $B$:
   encontrar todas las asignaciones donde se equivoca, y en qué dirección.
   (Verificado: $T, T, T$ no se colorea y $F, F, F$ sí.)
8. [modelar] Horario de exámenes en 3 franjas como coloración; en qué dirección hay
   que reducir para decir que el horario es difícil.
9. [demostración] Clique en grafos de grado máximo 3 está en P; ¿por qué el
   complemento no transfiere esto a conjunto independiente?
10. ★ [demostración] Vertex cover es NP-completo en grafos de grado máximo 3, desde la
    forma del ejercicio 6 del capítulo 17. (Verificado en `ejercicios.py`: con copias
    atadas en ciclo, el grafo de la §2 tiene grado máximo 3 en 150 fórmulas.)

## Audios (tentativo)

| Audio | Secciones | Minutos |
|---|---|---|
| 1 | 1 y 2 | 6 |
| 2 | 3 y 4 | 5 |
| 3 | 5 | 4 |
| 4 | 6 y 7 | 7 |
| 5 | 8 | 6 |
| 6 | 9 | 4 |
| 7 | 10 y 11 | 5 |

Total estimado: 37 minutos.

## Decisiones

- **Cambios a las semillas del brief.** La 4 pedía vertex cover ≤ₚ set cover, que
  está en el cuerpo (§5); queda set cover ↔ hitting set. Las semillas 6 y 7 (dos
  cambios de hipótesis) van juntas en el ejercicio 6, para respetar la mezcla de la
  guía, y entra un ejercicio de modelar nuevo (8, horario de exámenes). La semilla 8
  pedía un gadget "que se colorea cuando no debería"; el del ejercicio 7 hace eso y
  además lo contrario, lo que obliga a revisar los 8 casos y no solo el que falla.
- **Sin atribución para la reducción con triángulos.** Karp reduce SAT a clique, y el
  capítulo muestra que su grafo es el complemento del nuestro. Quién escribió primero
  la versión con conjunto independiente no lo verifiqué, y no se cita.
- **Garey, Johnson y Stockmeyer (1976)** demostraron versiones restringidas (grado 3,
  planares). Verifiqué los datos en Crossref pero no el contenido (el texto está tras
  pago), así que no se cita y el ejercicio 10 se apoya solo en el capítulo 17.
- **El decisor de 3-coloración parte el grafo en componentes** después de fijar
  colores. Es un algoritmo genérico (no mira la estructura de la reducción) y es lo que
  deja correr la batería en menos de un segundo; sin la partición, una sola fórmula
  insatisfacible tardaba 7,4 s.

## Cambios al redactar (2026-11-13)

- Numeración final: teorema 1 (independiente), corolario 2, teorema 3 (set cover),
  lema 4 (el O), lema 5 (la cláusula), teorema 6 (3-coloración).
- Baterías de §3 y §8: las 255 fórmulas de $x_1, x_2, x_3$, 100 con asignación plantada
  (sí) y 100 que contienen las 8 cláusulas de tres variables (no). Las fórmulas densas al
  azar se descartaron: el decisor de independiente tardaba hasta 8,7 s en una
  insatisfacible con $m = 20$. El decisor de independiente ramifica sobre el vértice de
  menor grado y sus vecinos.
- Karp p. 99: no se cita su número de colores (el escaneo dice $k = r + 1$ con $r$
  cláusulas, y no lo pude contrastar), solo que crece con la fórmula.
- La figura 2 va después del lema 5, para no dejar media página en blanco.
