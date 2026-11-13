# Outline: Capítulo 12, optimizaciones de programación dinámica

Estado: redactado (2026-11-13) por el workflow del libro, pendiente de revisión.
Destino: `Lectures/2026/12-dp-optimizaciones/notas.md`, en formato de libro.
Extensión objetivo: 5 500–7 000 palabras con el código.
Verificación: `.playground/libro-daa/verif/12/` (`v1_knuth.py`, `v2_cadena.py`,
`v3_baterias.py`, `v4_hirschberg.py`).

## Idea del capítulo

En los capítulos anteriores la pregunta de una DP era cuál es la recurrencia. Aquí la
recurrencia ya es correcta, y la pregunta es cuánto cuesta evaluarla. El costo de una
DP es estados × transiciones en tiempo, y lo que se guarda en memoria. Se baja de dos
maneras:

- **Menos transiciones**, porque se demuestra que el óptimo vive en una franja
  (Knuth en el árbol binario de búsqueda óptimo: de $O(n^3)$ a $O(n^2)$).
- **Menos memoria**, porque se recalcula en vez de guardar (Hirschberg: la
  subsecuencia común más larga en espacio lineal, con divide y vencerás, al precio de
  hacer a lo sumo algo más del doble de trabajo).

La lección es que cada optimización es un teorema sobre la recurrencia, no un truco
de código. El error plantado lo muestra: Knuth sobre la cadena de matrices, que tiene
la misma forma de recurrencia y no cumple la hipótesis.

## Estructura

### 1. Cuando la recurrencia ya está bien
- Costo de una DP = estados × trabajo por estado; memoria = lo que se guarda.
- Conexión: la DP clásica de Estructuras de Datos (LCS, mochila), el capítulo 11
  (elegir el estado), el capítulo 6 (recurrencias y sustitución, §10).

### 2. El árbol binario de búsqueda óptimo
- Claves $1..n$ con frecuencias $f_i$; costo $= \sum f_i\,(\text{profundidad}_i+1)$.
- Recurrencia $c(i,j) = w(i,j) + \min_{i<k\le j} c(i,k-1)+c(k,j)$, $c(i,i)=0$,
  $w(i,j) = f_{i+1}+\dots+f_j$. Por qué: cada clave baja un nivel al colgar de la raíz.
- Código $O(n^3)$, probado contra la enumeración de todos los árboles ($n \le 7$,
  verificado en `v1_knuth.py`).

### 3. La tabla de raíces (el experimento)
- Imprimir la tabla de raíces $K(i,j)$ (la mayor raíz óptima) de una instancia.
- Lo que se ve: crece hacia la derecha y hacia abajo. Enunciado propuesto:
  $K(i,j-1) \le K(i,j) \le K(i+1,j)$.
- Comprobado en 3 000 instancias al azar con empates, con la mayor y con la menor
  raíz óptima: 0 violaciones (`v1_knuth.py`).
- **Figura**: la tabla de raíces con una celda y su franja.

### 4. Knuth: recorrer solo la franja
- El algoritmo y su costo por suma telescópica: por diagonal $d$, a lo sumo
  $2n-d$ evaluaciones; en total $\sum_{d=2}^{n}(2n-d) = O(n^2)$.
- Medido: $n=160$: 695 360 evaluaciones contra 25 907 (cota 38 001).
- **Figura**: evaluaciones contra $n$, log-log.

### 5. La desigualdad del cuadrilátero
- Definición; $w$ de sumas la cumple con igualdad y es monótona por inclusión.
- Lema 1 (Yao): si $w$ cumple las dos, $c$ cumple la desigualdad. Demostración
  completa por inducción en $d-a$: casos $a=b$ o $c=d$ triviales, caso $b=c$
  (usa la monotonía de $w$), caso $b<c$ con $z=K(a,d)$, $y=K(b,c)$ y dos subcasos.

### 6. La monotonía de la raíz
- Lema 2 con la mayor raíz óptima; las dos desigualdades por separado. El paso
  clave: el término $w(i,j)$ no depende de $k$ y se cancela.
- Teorema: Knuth devuelve el costo óptimo. Citas: Knuth (Acta Informatica 1, 1971,
  14–25), Yao (STOC 1980, 429–435).

### 7. El error plantado: Knuth en la cadena de matrices
- Misma forma de recurrencia, pero el costo $d_i d_k d_j$ depende del corte.
- Medido (`v3_baterias.py`): matrices cuadradas 0/1 000, cadenas de 3 matrices
  0/1 000, dimensiones crecientes 0/1 000, decrecientes 12/1 000, 4 matrices al azar
  215/1 000, 8 al azar 943/1 000. Menor contraejemplo: dimensiones $(1,1,2,2,1)$,
  óptimo 7, Knuth 8.

### 8. Memoria: la tabla de la LCS
- Para la longitud bastan dos filas; para la subsecuencia, la tabla entera.

### 9. Hirschberg: el punto medio
- Lema: $\mathrm{LCS}(X,Y) = \max_k \mathrm{LCS}(X_{<m}, Y_{<k}) +
  \mathrm{LCS}(X_{\ge m}, Y_{\ge k})$, con demostración de las dos desigualdades.
- **Figura**: la tabla partida por la fila media, los valores $F_k+B_k$ y los dos
  rectángulos que quedan.

### 10. Hirschberg: el algoritmo y su costo
- Código con índices (sin copiar cadenas en cada nivel); probado contra la tabla.
- Celdas: $C(n,m) \le G(n)\,m$ con $G(n) = n + G(\lceil n/2 \rceil)$, $G(1)=1$, y
  $G(n) \le 2n + \lceil\log_2 n\rceil - 1$. "Constante 2" no es exacto: $n=9$ sin
  letras comunes da $20m > 2nm$ (`v4_hirschberg.py`, peor razón observada 2,222).
- Memoria $O(n+m)$; medida con `tracemalloc`. **Figura**: memoria contra $n$.

### 11. Otras dos franjas
- Optimización por divide y vencerás (corte óptimo monótono en $i$), y convex hull
  trick (pendientes ordenadas, pila con costo amortizado del capítulo 4). Mención sin
  demostración; los ejercicios 7 y 8 las trabajan.

### 12. La regla
- Una optimización de DP es un teorema sobre la recurrencia; su hipótesis es la lista
  de lo que el problema tiene que cumplir.

## Ejercicios (cambios respecto de las semillas)

- 4: la semilla (Knuth en la cadena de matrices) es el error plantado del cuerpo; pasa
  a la mezcla de montones vecinos, donde la monotonía sí vale (0 violaciones en 2 000
  instancias, `v3_baterias.py`).
- 6: "constante 2" es falso tal cual; el ejercicio pide demostrar
  $C(n,m) \le 2nm$ cuando $n$ es potencia de 2, construir entradas que lo superen con
  $n = 5$ y $n = 9$, y demostrar que con $n = 3$ o $7$ no hay ninguna ($G(2^t-1) = 2n$).
- 9: se pide una $w$ que cumpla la desigualdad del cuadrilátero y no la monotonía por
  inclusión, con raíz no monótona; existe con $n=3$ (`v3_baterias.py`).

## Audios (tentativo)

| Audio | Secciones | Minutos |
|---|---|---|
| 1 | 1 y 2 | 6 |
| 2 | 3 y 4 | 6 |
| 3 | 5 | 6 |
| 4 | 6 | 5 |
| 5 | 7 | 4 |
| 6 | 8 y 9 | 6 |
| 7 | 10 | 5 |
| 8 | 11 y 12 | 4 |

## Decisiones que quiero confirmar

- Las frecuencias son solo de búsquedas exitosas (sin las $q_i$ de Knuth y CLRS); la
  demostración es la misma.
- Sin cita para la optimización por divide y vencerás ni para el convex hull trick:
  no encontré una fuente primaria clara de ninguna de las dos.
- Las citas de Knuth y Yao se comprobaron en Crossref (autor, título, lugar, páginas);
  el texto de los artículos no se pudo descargar.
