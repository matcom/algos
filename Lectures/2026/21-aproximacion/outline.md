# Outline: Capítulo 21, algoritmos de aproximación

Estado: redactado (2026-11-13) dentro del flujo del libro. El documento está en `notas.md`.
Destino: `Lectures/2026/21-aproximacion/notas.md`, formato de libro.
Extensión objetivo: 5 500–7 000 palabras con el código.
Verificación: `.playground/libro-daa/verif/21/` (`vc.py`, `vc_rompe.py`, `carga.py`,
`kcentro.py`, `cubrir.py`).

## Idea del capítulo

Los capítulos 16 a 19 demostraron que vertex cover, set cover, 3-SAT y compañía son
NP-completos, y el capítulo 20 los resolvió exactos en tiempo exponencial. Este capítulo
pide otra cosa: tiempo polinomial y una solución que, en **toda** entrada, cueste a lo
sumo $\alpha$ veces el óptimo. La dificultad es que no conocemos el óptimo. La técnica
de todo el capítulo es una sola: encontrar una **cota del óptimo que sí se puede
calcular** (un emparejamiento, el promedio de la carga, $k + 1$ puntos lejanos, los
precios de los elementos, la esperanza) y comparar contra ella. La cota decide la razón.

El error plantado es una variante de vertex cover que toma un solo extremo de cada
arista, el de más grado. Gana a la versión correcta en casi todos los grafos al azar y
no tiene razón 2. La demostración dice dónde: la cota del óptimo pedía aristas
disjuntas.

## Estructura

### 1. Rendirse con garantía
- Definición de razón $\alpha$ para minimización ($c(A(I)) \le \alpha\,\mathrm{OPT}(I)$,
  $\alpha \ge 1$) y maximización ($v(A(I)) \ge \alpha\,\mathrm{OPT}(I)$, $\alpha \le 1$),
  para toda entrada $I$. Polinomial en el tamaño de la entrada.
- El problema: OPT es lo que no sabemos calcular. La técnica: una cota $B(I)$ con
  $B(I) \le \mathrm{OPT}(I)$ (minimización) que sí se calcula, y $c(A(I)) \le \alpha B(I)$.
- Conexión: capítulo 16 (decisión frente a optimización), capítulo 20 (exacto).

### 2. Vertex cover: una cota del óptimo
- Ejemplo chico. Lema: si $M$ es un emparejamiento, todo vertex cover tiene al menos
  $|M|$ vértices (cada arista de $M$ necesita un extremo y no comparten extremos).

### 3. Emparejamiento maximal: razón 2
- Algoritmo: recorrer aristas, si está descubierta, tomar los dos extremos.
- Teorema: es un vertex cover, las aristas tomadas forman un emparejamiento maximal,
  cuesta $2|M| \le 2\,\mathrm{OPT}$.
- Código contra fuerza bruta. **Medido**: 2 698 grafos al azar de hasta 10 vértices,
  peor razón 2,0 (se alcanza).
- **Figura** `aprox-emparejamiento`: grafo, aristas del emparejamiento, los dos extremos.

### 4. El error plantado: un extremo por arista
- Variante: tomar solo el extremo de más grado entre lo que falta cubrir. Es un vertex
  cover. **Medido**: en los mismos 2 698 grafos nunca pasa de 2 (peor 1,5).
- La demostración anuncia el error: las aristas tomadas ya no son disjuntas, la cota
  $\mathrm{OPT} \ge |M|$ no vale.
- Instancia construida (bipartita, $k$ a la izquierda, por cada $i$ grupos de $\lfloor
  k/i \rfloor$ vértices de grado $i$): **medido** $k = 24$: 60 vértices contra un cover
  de 24, razón al menos 2,5; $k = 96$: 363 contra 96.

### 5. Balanceo de carga: la regla de Graham
- $n$ tareas, $m$ máquinas idénticas, makespan. Cotas: $\mathrm{OPT} \ge \max_j t_j$ y
  $\mathrm{OPT} \ge \frac{1}{m}\sum_j t_j$.
- Teorema (Graham, 1966): la regla de la máquina menos cargada da $\le (2 - 1/m)\,
  \mathrm{OPT}$. Demostración con la última tarea de la máquina más cargada.
- **Figura** `aprox-graham`: diagrama de cargas, la última tarea y las dos cotas.

### 6. Graham medido
- Código contra un óptimo por ramificación. **Medido** (4 000 instancias, $m \le 4$,
  $n \le 9$): peor 22/15 con $m=2$, 11/7 con $m=3$, 30/19 con $m=4$.

### 7. LPT: 4/3
- Ordenar de mayor a menor. Intento fácil: $3/2$. Teorema (Graham, 1969):
  $\le (4/3 - 1/(3m))\,\mathrm{OPT}$. Lema: si $t_k > \mathrm{OPT}/3$, tras asignar
  $k$ esa máquina carga $\le \mathrm{OPT}$ (conteo de las tareas grandes).
  **Comprobado** en 16 133 pasos; sin la hipótesis falla 559 veces en 1 500 instancias.
- **Medido**: peor LPT 43/38, 17/15, 36/31.

### 8. k-center y el más lejano
- Problema métrico; algoritmo del más lejano; teorema razón 2 por casillero y
  desigualdad triangular. Gonzalez (1985).
- Código contra fuerza bruta: 1 500 instancias, peor 1,995.
- **Figura** `aprox-kcentro`: puntos, centros, radios.

### 9. No hay razón $2 - \varepsilon$
- Desde conjunto dominante (ejercicio del capítulo 18): distancias 1 y 2.

### 10. Set cover goloso
- Precio por elemento nuevo. Ejemplo. Código contra fuerza bruta: 942 instancias, peor 1,8.

### 11. $H_n$ por reparto de costos
- Precios, la suma de precios es el costo, cada conjunto del óptimo paga a lo sumo
  $c_S H_{|S|}$. Chvátal (1979). Comprobado sobre las mismas instancias.
- Dinur y Steurer (2014): $(1 - \varepsilon)\ln n$ es NP-duro.

### 12. MAX-3SAT: 7/8 por linealidad de la esperanza
- Indicadoras, capítulo 8. Existencia. Las Vegas: $p \ge 1/(8k)$, a lo sumo $8k$
  intentos esperados (comprobado: el mínimo de $8kp$ medido es 1). Håstad (2001).

### 13. La regla
- Tabla: problema, cota del óptimo, razón, qué no se puede mejorar.
- Hacia adelante: capítulo 22 (programación lineal como cota), capítulo 23 (PTAS).

## Ejercicios

1. [traza] LPT sobre 5,5,4,4,3,3,3 con $m = 3$; óptimo y razón contra $4/3 - 1/(3m)$.
2. [entrada que rompe] Instancias ajustadas: emparejamiento maximal 2 en cualquier orden;
   Graham $2 - 1/m$.
3. [entrada que rompe] Set cover: el goloso paga $\Theta(\log n)$ veces el óptimo.
4. [demostración] Empaquetamiento en cajas: no hay razón $< 3/2$ si P ≠ NP, desde partición.
5. [demostración] Set cover con frecuencia $f$: razón $f$.
6. [demostración] ★ MAX-CUT por búsqueda local: razón 1/2, a lo sumo $m$ mejoras.
7. [implementar y medir] Desaleatorizar MAX-3SAT por esperanzas condicionales.
8. [implementar y medir] Graham y LPT contra el óptimo.
9. [cambio de hipótesis] k-center sin desigualdad triangular.
10. [modelar] Bases de ambulancias: set cover y k-center.

## Cambios a las semillas del brief

- Semillas 4 y 5 (inaproximabilidad de k-center y la razón $H_n$) son demostraciones que
  el plan pone en el cuerpo (§9 y §11); se reemplazan por empaquetamiento en cajas y
  set cover con frecuencia $f$.
- Semilla 9 (vertex cover goloso por grado) es el error plantado de §4; sale de los
  ejercicios.
- Semillas 1 y 2 se juntan en el ejercicio 2 para no pasar de dos "entrada que rompe".
- Semilla 8 (MAX-CUT) pasa a demostración; el "modelar" es el ejercicio 10.

## Citas verificadas

- Graham 1966, BSTJ 45(9):1563–1581; Graham 1969, SIAM J. Appl. Math. 17(2):416–429
  (metadatos en Crossref; el contenido, por fuentes secundarias).
- Gonzalez 1985, TCS 38:293–306 (resumen: $O(kn)$, razón 2, óptimo si P ≠ NP).
- Hsu y Nemhauser 1979, Discrete Appl. Math. 1(3):209–215.
- Chvátal 1979, Math. Oper. Res. 4(3):233–235.
- Håstad 2001, J. ACM 48(4):798–859. Dinur y Steurer, STOC 2014, 624–633.
