# Outline: Capítulo 9, algoritmos golosos con argumentos de intercambio

Estado: redactado (2026-11-13), pendiente de revisión. El documento está en `notas.md`.
Destino: `Lectures/2026/09-golosos/notas.md`, en formato de libro.
Extensión objetivo: 5 500–7 000 palabras con el código.
Verificaciones: `.playground/libro-daa/verif/9/` (`retraso.py`, `cache.py`,
`transforma.py`, `ventana.py`, `ejercicios.py`).

## Idea del capítulo

Un algoritmo goloso decide una vez y no vuelve atrás. Escribirlo es fácil; lo difícil
es saber si acierta, porque casi siempre hay otra regla que parece igual de razonable
y se equivoca. El capítulo enseña una sola herramienta, el **argumento de
intercambio**: se toma una solución óptima cualquiera y se la transforma paso a paso
en la del goloso sin empeorarla. La transformación necesita una medida que decrezca
(las inversiones, o los pedidos en que dos planificaciones coinciden), y esa medida
es lo que hay que encontrar.

Dos problemas, en orden de dificultad:

- **Retraso máximo** con el plazo más cercano primero. El intercambio es local: dos
  tareas vecinas invertidas se cambian y el retraso no sube.
- **Caché óptima fuera de línea** con la regla de Belady. El intercambio no es local:
  cambiar un desalojo obliga a seguir modificando la planificación hasta que vuelve a
  coincidir con la original, y la planificación intermedia sale no reducida.

El error plantado es Belady con la mirada limitada a una ventana de 16 pedidos, un
"ahorro" natural del barrido hacia adelante. Las pruebas cortas no pueden verlo, y la
demostración dice dónde está: el paso que usa que $e$ se pide antes que $f$.

## Estructura

### 1. Decidir una vez
- Qué es un goloso: ordenar por una regla y tomar decisiones que no se deshacen.
- Hacia atrás: el capítulo 3, §9, con el primer rechazo, ya tenía la forma de
  "la primera decisión en que difieren". Kruskal y Dijkstra vienen de Estructuras de
  Datos sin que nadie haya dicho por qué funcionan con la misma herramienta.
- Plan del capítulo: dos problemas, la misma herramienta, la segunda vez más dura.

### 2. El retraso máximo
- $n$ tareas, duraciones $t_i$ y plazos $d_i$, una máquina desde el tiempo 0.
  Retraso $\ell_i = \max(0, f_i - d_i)$, se minimiza $L = \max_i \ell_i$
  (definición de Kleinberg y Tardos, §4.2).
- Ejemplo chico con 4 tareas, todas las órdenes calculadas por el código: cuántos
  órdenes alcanzan el óptimo.
- **Código**: `retraso(orden, t, d)` y el oráculo `optimo` por permutaciones.

### 3. Tres reglas y un experimento
- Cómo se le ocurre a uno: la más corta primero (despacha mucho rápido), la de
  menor holgura $d_i - t_i$ (la más urgente), el plazo más cercano (ignora las
  duraciones, que parece un descuido).
- Contraejemplo de dos tareas para la más corta primero, calculado.
- **Código**: las tres reglas contra el oráculo en 2 000 instancias aleatorias con
  $n \le 5$: plazo 0 fallos, corta 1 214, holgura 341 (en `retraso.py`, con $n \le 6$:
  0, 1 371 y 431).
  El experimento propone el teorema; la demostración decide.

### 4. Inversiones
- Lema (sin tiempo ocioso): existe un óptimo sin huecos. Enunciado aquí, demostración
  en el ejercicio 3 (se dice explícitamente).
- Definición de inversión: $i$ antes que $j$ con $d_i > d_j$.
- Lema: todas las órdenes sin huecos ni inversiones tienen el mismo $L$. Demostración
  completa: solo difieren en el orden de tareas con el mismo plazo, que forman un
  bloque contiguo, y el peor retraso del bloque es el de la última que termina, que
  termina en el mismo instante.

### 5. El intercambio
- Lema: un orden con inversión tiene una inversión entre vecinas (demostración de una
  línea: si ninguna vecina está invertida, los plazos crecen).
- Lema: cambiar dos vecinas invertidas $i, j$ quita exactamente una inversión y no
  sube $L$. Demostración: las demás no se mueven, $j$ termina antes, e $i$ termina
  donde terminaba $j$ con $d_i > d_j$, así que $\ell_i' \le \ell_j$. Se marca el paso
  que se salta: "vecinas" es lo que garantiza que las demás no se mueven.
- Teorema: el plazo más cercano es óptimo (inducción sobre el número de inversiones).
- **Figura** `golosos-inversion`: el orden con una inversión vecina y el mismo después
  del intercambio, con los retrasos calculados.
- **Código**: el intercambio con `assert` en 2 000 instancias.

### 6. La caché
- Memoria rápida de $k$ elementos, sucesión de pedidos conocida entera (fuera de línea),
  costo = fallos. Planificación = qué se desaloja en cada fallo.
- Por qué importa fuera de línea: es la vara contra la que se miden las reglas en línea.
- **Código**: el oráculo por programación dinámica sobre los contenidos de la caché.

### 7. Belady, LRU y FIFO
- Belady (1966): desalojar el elemento cuyo próximo pedido está más lejos. LRU y FIFO
  como reglas que miran el pasado.
- **Figura** `golosos-traza`: traza de Belady contra LRU sobre la misma sucesión, con
  los fallos marcados. La sucesión es distinta de la del ejercicio 4.
- **Código**: las tres reglas contra el oráculo en 3 000 instancias (`cache.py`:
  Belady 0 fallos; LRU y FIFO subóptimas en unas 1 300).

### 8. Planificaciones reducidas
- Definición: solo se trae un elemento cuando se pide. Costo de una planificación
  cualquiera = número de cargas.
- Lema: toda planificación se convierte en una reducida con a lo sumo tantas cargas.
  Demostración completa por asignación: cada carga de la reducida se carga a una carga
  distinta de la original en el intervalo desde que la reducida desalojó ese elemento.

### 9. La transformación (sección larga)
- Lema: si $S$ reducida coincide con Belady en los primeros $j$ pedidos, existe $S'$
  reducida que coincide en $j + 1$ y no tiene más fallos. Los tres casos, más los
  subcasos del pedido de $e$. El paso que todos se saltan: $f$ no puede pedirse antes
  que $e$, porque Belady eligió $f$ como el más lejano.
- Teorema: Belady es óptimo, por inducción sobre $j$ desde una óptima reducida.
- **Figura** `golosos-transformacion`: $S$ y $S'$ pedido a pedido, desde la diferencia
  hasta que vuelven a coincidir, sobre una instancia real que el código encuentra.
- **Código**: la transformación ejecutada, con `assert` sobre el número de cargas y la
  coincidencia. Verificado en `transforma.py` (2 000 casos, 2 359 pasos), y la
  comprobación rota a propósito (Belady cambiado por "el más cercano") falla.

### 10. El error plantado: Belady con ventana
- La variante mira solo los próximos $w$ pedidos.
- **Código**: medición con $w = 16$, $k = 4$, 6 elementos: con 12 pedidos 0 de 400 (no
  puede fallar); con 200, 1 de 400, y 0 por encima de LRU. Una entrada construida de
  26 pedidos la rompe (Belady 5 fallos, ventana 6).
- La demostración lo anunciaba: el caso del pedido de $f$ antes que $e$.

### 11. En línea y fuera de línea (sección corta)
- LRU no conoce el futuro. Sleator y Tarjan (1985), teoremas 5 y 6: con la misma
  caché $k$, LRU hace a lo sumo $k$ veces los fallos de Belady más $k$, y ninguna
  regla en línea determinista garantiza menos que ese factor en sucesiones largas.
  Ejercicio 5. El análisis competitivo no es parte del curso (el epílogo).
- Hacia adelante: el capítulo 10 dice cuándo un goloso acierta para cualquier peso;
  el capítulo 21 usa golosos que no aciertan pero se acercan.

### 12. La regla
- Un goloso se demuestra con una medida que decrece mientras se transforma un óptimo
  sin empeorarlo. Si no la encuentras, sospecha de la regla.

### Resumen y ejercicios

## Ejercicios
1. [traza] Plazo más cercano en 6 tareas.
2. [entrada que rompe] Menor holgura: dos tareas; ninguna instancia de dos tareas
   rompe a la vez las dos reglas (demostrable); dar una de tres (existe, verificado).
3. [demostración] Óptimo sin tiempo ocioso.
4. [traza] Belady y LRU con caché 3 sobre 12 pedidos (`1 2 3 4 1 2 5 1 2 3 4 5`).
5. [modelar] Familia donde el cociente LRU / Belady tiende a $k$.
6. [demostración] Selección de intervalos por el que termina primero.
7. [demostración] Regla de Smith por intercambio.
8. [entrada que rompe] Monedas {1, 3, 4}, monto 6.
9. [cambio de hipótesis] Tiempos de liberación.
10. [modelar] ★ Partición de intervalos y profundidad.
11. [implementar y medir] Belady en $O(n \log k)$.

## Audios

| Audio | Secciones | Minutos |
|---|---|---|
| 1 | 1–2 | 5 |
| 2 | 3 | 5 |
| 3 | 4 | 5 |
| 4 | 5 | 6 |
| 5 | 6–7 | 6 |
| 6 | 8 | 4 |
| 7 | 9 (lema) | 6 |
| 8 | 9 (código y teorema) | 4 |
| 9 | 10 | 5 |
| 10 | 11–12 | 4 |

## Decisiones que quiero confirmar

- Jackson (1955) se suele citar como origen del plazo más cercano, pero el informe de
  UCLA no está en línea y no se pudo comprobar: no entra.
- Mattson, Gecsei, Slutz y Traiger (1970) se cita a veces como la demostración de la
  optimalidad de Belady; el texto escaneado no se pudo leer: no entra. La demostración
  sigue el camino de Kleinberg y Tardos, §4.3.
- Se agrega un ejercicio 11 de implementar y medir: las semillas no traían ninguno y
  la guía pide uno o dos.
- El módulo de figuras es `figuras_09.py`, con dos dígitos como pide la guía
  (renombrado en la ronda 1 de revisión).
