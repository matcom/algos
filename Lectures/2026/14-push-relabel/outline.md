# Outline: Capítulo 14, flujo máximo con push-relabel

Estado: aprobado y redactado (2026-11-13). El documento está en `notas.md`.
Destino: `Lectures/2026/14-push-relabel/notas.md`, capítulo del libro.
Extensión objetivo: 5 500–7 000 palabras con el código.
Verificación: `.playground/libro-daa/verif/14/` (`pr.py`, `capitulo.py`, `t1.py` a `t9.py`).

## Idea del capítulo

El capítulo 13 mantiene un **flujo** y busca caminos de aumento. Este capítulo invierte
la apuesta: mantiene algo que todavía no es un flujo, un **preflujo** que respeta las
capacidades pero deja que los vértices acumulen exceso, y lo va empujando cuesta abajo
por una función de altura. Ningún paso mira un camino entero: cada operación es local a
un vértice y sus aristas.

La correctitud cabe en un invariante de una línea, $h(u) \le h(v) + 1$ en cada arista
residual, y el costo se cuenta por separado para tres operaciones: reetiquetados,
empujes saturantes y empujes no saturantes. Los no saturantes se cuentan con el
potencial del capítulo 4. La regla de orden (FIFO o mayor etiqueta) baja la cota, y dos
heurísticas que no tocan la cota (relabel global y gap) bajan las operaciones medidas
en un factor de 20 a 60.

El error plantado: poner $h(s)$ igual a la distancia de $s$ a $t$ en la red original,
una idea que suena bien después de los niveles de Dinic. La última línea de la
demostración de correctitud dice dónde falla.

## Estructura

### 1. Otra manera de mover el flujo
- Dónde estamos: Dinic (capítulo 13) conserva el flujo en cada paso y paga por buscar
  caminos. Aquí se relaja la conservación.
- Preflujo, exceso, vértice activo. La idea es de Karzanov, según el resumen de
  Goldberg y Tarjan (1988), que dan el método de este capítulo.
- La imagen: agua que solo baja un escalón por vez; la altura dice hacia dónde.

### 2. Empujar y reetiquetar
- Inicialización: $h(s) = V$, el resto en 0, saturar todas las aristas de $s$.
- Arista admisible: residual con $h(u) = h(v) + 1$. Empujar $\min(e(u), r(u,v))$;
  saturante o no. Reetiquetar: $h(u) = 1 + \min h(v)$ sobre las residuales.
- Código: `Red` (aristas en pares, inversa `k ^ 1`), `generico` con la regla del
  primer activo y un `assert` del invariante opcional.
- Ejemplo de 5 vértices: flujo 3 en 22 operaciones (10 reetiquetados, 9 saturantes,
  3 no saturantes). Alturas finales $a = b = c = 6 > V$: el exceso que no cabía volvió
  a $s$.
- **Figura**: la red con los vértices dibujados a su altura, en tres momentos (al
  empezar, en medio del vaivén entre $a$ y $b$, al terminar).

### 3. La función de altura
- Invariante y demostración por casos (inicio, empujar, reetiquetar). El paso que se
  salta: el empuje crea la arista inversa $(v, u)$, y $h(v) = h(u) - 1$ la cumple.
- Consecuencias: reetiquetar sube estrictamente (por qué se puede reetiquetar: no hay
  admisible, así que toda residual tiene $h(v) \ge h(u)$); las alturas nunca bajan.

### 4. Correctitud
- Lema: un vértice activo tiene camino residual a $s$ (demostración por el conjunto
  alcanzable y la suma de excesos).
- Al terminar no hay activos: el preflujo es un flujo. No hay camino residual $s \to t$:
  bajaría $V$ en a lo sumo $V - 1$ aristas. Max-Flow Min-Cut (capítulo 13) cierra.
- La terminación queda para las §6 a §8.
- Código: oráculo de fuerza bruta (corte mínimo sobre los $2^{V-2}$ cortes). 2000
  redes al azar con $V \le 7$: el invariante se cumple en cada paso y el flujo coincide.

### 5. El error plantado
- $h(s) = d(s, t)$ en la red original, "como los niveles de Dinic".
- Medido (1000 redes por batería, oráculo de fuerza bruta): chicas 0,3 %, medianas
  ($V = 8..10$) 11,0 %, en capas 0,0 %. Medido aparte en verif: unitarias 0,7 %, y en
  capas con otra semilla 4 de 3000.
- La demostración lo anunciaba: la última línea necesita que $h(s)$ supere la
  longitud de **todo** camino residual simple, y los caminos residuales usan aristas
  inversas que la red original no tiene.
- Qué valor mínimo de $h(s)$ es correcto queda para el ejercicio 10 (respuesta
  verificada: $V - 2$; ver decisiones).

### 6. Las alturas no se escapan
- Experimento antes: mayor altura vista en 3000 redes, contra $2V - 1$.
- Lema: $h(u) \le 2V - 1$ (camino a $s$ con a lo sumo $V - 1$ aristas).
- Reetiquetados: a lo sumo $2V - 1$ por vértice, menos de $2V^2$ en total.

### 7. Empujes saturantes: a lo sumo $2VE$
- Entre dos empujes saturantes por $(u, v)$ tiene que haber uno de $v$ a $u$, y la
  altura de $u$ sube al menos 2. El vaivén de $a$ y $b$ en la figura es esto.

### 8. Empujes no saturantes: el potencial
- $\Phi = \sum_{v \text{ activo}} h(v)$. Empieza y termina en 0, nunca negativo
  (el paso que se olvida en el capítulo 4).
- Reetiquetar sube $\Phi$ en total a lo sumo $(2V-1)(V-2)$; un saturante, a lo sumo
  $2V - 1$; un no saturante lo baja al menos 1. Total $\le 4V^2(V + E)$, y con
  $E \ge V - 1$, $O(V^2 E)$.
- **Figura**: $\Phi$ paso a paso en el ejemplo de la §2, coloreada por tipo de operación.
- Medido: el peor cociente contra cada cota en redes al azar (V = 20, 40, 80):
  reetiquetados 0,41–0,42 de $2V^2$, saturantes 0,02–0,05 de $2VE$, no saturantes
  0,0006–0,002 de $4V^2(V+E)$. Las cotas son flojas, sobre todo la del potencial.
- Costo total: con arista actual, cada operación cuesta $O(1)$ amortizado más
  $O(\deg)$ por reetiquetado; lo demuestra la §9.

### 9. FIFO: $O(V^3)$
- Descargar un vértice con la arista actual. Lema: cuando la arista actual llega al
  final, no hay admisible (una arista inadmisible solo vuelve a ser admisible si $u$
  se reetiqueta).
- Pasadas sobre la cola (Goldberg y Tarjan, Lema 4.3): $\Phi = \max$ altura activa.
  Pasada sin reetiquetado: $\Phi$ baja. A lo sumo $4V^2$ pasadas, un no saturante por
  vértice por pasada: $4V^3$.
- Sin código en el cuerpo (recorte de extensión): la implementación es el ejercicio 8.
  En verif, FIFO coincide con el oráculo en 3000 redes y hace las mismas ~1,5 V²
  operaciones que mayor etiqueta en el embudo.

### 10. Mayor etiqueta: $O(V^2\sqrt{E})$
- Cota de Cheriyan y Maheshwari (1989); la demostración por potencial es la de
  Cheriyan y Mehlhorn (1999): fases entre cambios de la mayor altura activa, fases
  baratas ($\le K$ no saturantes) y caras, $\Phi = \sum_{\text{activo}} |\{w : h(w) \le h(v)\}|/K$,
  $K = \sqrt{E}$.
- Código con cubetas y comprobación contra el oráculo.

### 11. Las heurísticas: relabel global y gap
- Relabel global: alturas = distancia residual a $t$ (o a $s$ más $V$). Demostración de
  que no baja ninguna altura y respeta el invariante, así que las cotas siguen.
- Gap: si ningún vértice queda a altura $k < V$, los que están por encima no llegan a
  $t$. La demostración es el ejercicio 6.
- Cherkassky y Goldberg (1997) las estudian; gap ayuda a mayor etiqueta y poco a FIFO.
- Medición en la familia "embudo" ($s$ inyecta más de lo que cabe en el corte):
  Dinic, mayor etiqueta y mayor etiqueta con las dos heurísticas, $V$ de 50 a 300.
  Conteos (robustos): 1,46–1,62 V² sin heurísticas, 8,4–14,9 V con ellas. Tiempos con
  el host cargado: solo cualitativos; el código imprime cuántas veces más tarda
  push-relabel con heurísticas que Dinic en V = 300 (5,7 en el último render).
- **Figura**: tiempos log-log de los cuatro.

### 12. Cierre
- La regla: una heurística que respeta el invariante y no baja alturas hereda la
  correctitud y la cota sin demostración nueva. La demostración no dice qué hacer; dice
  qué se puede tocar.
- Hacia adelante: el capítulo 15 (Karger, corte global), el capítulo 24 (flujo en
  tiempo casi lineal).

### Resumen, Ejercicios

1. [traza] Genérico a mano, red de 5 vértices dada, regla fijada (flujo 5, 19 ops verificado).
2. [traza] Relabel global y gap sobre el estado central de la figura 1.
3. [demostración] Ninguna altura llega a $2V - 1$: la cota es $2V - 2$ (verificado:
   búsqueda al azar alcanza $2V - 2$ para $V = 4, 5, 6$; demostración en decisiones).
4. [demostración] Una altura $\ge V$ implica que no hay camino residual a $t$.
5. [demostración] Mayor etiqueta en $O(V^3)$ con el argumento de pasadas (Goldberg y
   Tarjan lo dicen en una línea).
6. [demostración] Gap no cambia la respuesta.
7. [modelar] Corte mínimo al terminar; y desde el primer momento en que ningún activo
   llega a $t$.
8. [implementar y medir] FIFO con cola y arista actual, contra Dinic y mayor etiqueta
   (la semilla 8 del brief).
9. [entrada que rompe ★] Familia y regla con el mayor crecimiento de no saturantes.
10. [cambio de hipótesis] $h(s) = k$: para qué $k$ es correcto, y cómo cambian las cotas.

## Audios (tentativo)

| Audio | Secciones | Minutos |
|---|---|---|
| 1 | 1 y 2 | 6 |
| 2 | 3 y 4 | 6 |
| 3 | 5 | 4 |
| 4 | 6 y 7 | 5 |
| 5 | 8 | 5 |
| 6 | 9 | 5 |
| 7 | 10 | 5 |
| 8 | 11 y 12 | 6 |

## Decisiones

- **Las semillas 2 a 5 del brief son demostraciones que el cuerpo hace enteras**
  (invariante, $2V - 1$, $2VE$, potencial). Como ejercicio pedirían copiar el texto.
  Se cambiaron por variantes que no están en el cuerpo: la cota $2V - 2$, alturas
  $\ge V$, mayor etiqueta en $O(V^3)$ y una traza de las heurísticas.
- **Semilla 9** pedía una familia con $\Theta(V^2 E)$ para el genérico. No encontré en
  una fuente primaria verificada que esa cota sea ajustada para el genérico, así que el
  ejercicio pide la mejor familia que se encuentre y medir contra la cota.
- **El error plantado no es $h(s) = V - 1$.** Era el primer candidato y no falla nunca:
  con $h(s) \ge V - 2$ el algoritmo es correcto. Demostración: una arista residual
  $s \to v$ al final solo existe si $v$ empujó a $s$, con $h(v) = h(s) + 1$, y las
  alturas no bajan; el resto del camino a $t$ evita $s$ y tiene a lo sumo $V - 2$
  aristas, así que $h(v) \le V - 2$. Con $h(s) = V - 3$ falla (6 % de redes chicas).
  Es el ejercicio 10.
- **La cota $2V - 2$:** un camino residual de $u$ a $s$ que pasa por $t$ da
  $h(u) \le V - 2$ (desde $t$ el invariante no deja subir); si evita $t$ tiene a lo
  sumo $V - 2$ aristas.
- **Citas verificadas en la fuente:** Goldberg y Tarjan, J. ACM 35(4):921–940, 1988
  (texto completo: lemas 3.5 a 3.10, FIFO en el lema 4.3 y el corolario 4.4, mayor
  distancia en $O(n^3)$ "con una prueba similar"); Cheriyan y Maheshwari, SIAM J.
  Comput. 18(6):1057–1086, 1989 (Crossref; la cota la atribuye el preprint de Cheriyan
  y Mehlhorn); Cheriyan y Mehlhorn, Inf. Process. Lett. 69(5):239–242, 1999 (preprint
  del autor leído entero); Cherkassky y Goldberg, Algorithmica 19(4):390–410, 1997
  (Crossref; el contenido sobre las heurísticas, por resúmenes, por eso el capítulo
  solo dice que las estudian).
- **Sin verificar, y fuera del texto:** que las cotas de FIFO y mayor etiqueta sean
  ajustadas (Cheriyan y Maheshwari lo dirían en su resumen, que no pude leer).
