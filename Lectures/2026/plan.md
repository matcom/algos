# Diseño y Análisis de Algoritmos: plan de conferencias 2026

Este plan sigue el programa de la asignatura en el plan de estudio de Ciencia de la
Computación (disciplina Matemática Computacional). El programa reparte 48 horas en
tres temas: 20 horas de conferencia, 24 de clase práctica y 4 de evaluación, más el
examen final escrito integrador.

| Tema | Conferencias | Clases prácticas | Evaluación |
|---|---|---|---|
| 1. Fundamentos teóricos para el diseño y análisis | 5 | 7 | |
| 2. Técnicas generales de solución de problemas | 10 | 12 | Parcial 1 |
| 3. Tratamiento de la intratabilidad con garantías formales | 5 | 5 | Parcial 2 |

Cada conferencia recorre el mismo ciclo sobre un problema concreto: enunciar el
problema, proponer un algoritmo, demostrar que es correcto, analizar su complejidad y,
cuando se pueda, dar una cota mínima para el problema. Después de cada conferencia se
orientan ejercicios para la casa, y la clase práctica siguiente se dedica a problemas
que el estudiante no ha visto.

El curso asume lo que el estudiante vio en Estructuras de Datos y Algoritmos:
ordenamientos por comparación, búsqueda binaria, BFS y DFS, Dijkstra, Bellman-Ford,
Floyd-Warshall, árboles recubridores mínimos, union-find, heaps, tablas hash y la
programación dinámica clásica (subsecuencia común más larga, mochila entera,
subsecuencia creciente más larga). Esos algoritmos aparecen aquí como herramientas o
como punto de partida, y cada conferencia trae técnicas y problemas nuevos.

Las demostraciones de correctitud, los análisis de complejidad, las cotas mínimas y
las garantías de aproximación o probabilísticas se escriben a mano, sin herramientas
de generación. Implementar, probar y depurar con ayuda de IA está permitido, siempre
que se declare.

Bibliografía básica: Cormen, Leiserson, Rivest y Stein, *Introduction to Algorithms*
(CLRS); Kleinberg y Tardos, *Algorithm Design* (KT).

## Tema 1. Fundamentos teóricos para el diseño y análisis

### Conferencia 1. El oficio algorítmico

Presenta el ciclo problema, algoritmo, correctitud, complejidad, cota mínima, que se
repite en todo el curso, recorriéndolo completo sobre el par de puntos más cercanos en
el plano. La fuerza bruta cuesta $O(n^2)$. Divide y vencerás baja a $O(n \log n)$, con
el argumento de que en la franja central basta revisar un número constante de vecinos.
La cota $\Omega(n \log n)$ en árboles de decisión algebraicos sale por reducción desde
distinción de elementos. El algoritmo aleatorio de Rabin con rejilla llega a $O(n)$
esperado, que muestra qué supuestos del modelo esconde la cota. Cierra con la
organización del curso, la evaluación y las reglas de uso de IA.

### Conferencia 2. Recurrencias difíciles

Parte del Teorema Maestro como conocimiento previo y va a las recurrencias donde no
aplica. Cambio de variable en $T(n) = 2T(\sqrt{n}) + \log n$. Recurrencias con ramas
desbalanceadas como $T(n) = T(n/5) + T(7n/10) + n$, resueltas con árbol de recurrencia
y confirmadas por sustitución. El teorema de Akra-Bazzi como generalización, con pisos,
techos y términos no polinomiales. Los errores típicos de la sustitución, como
"demostrar" $T(n) = O(n)$ para mergesort olvidando la constante.

### Conferencia 3. Demostrar que un algoritmo es correcto

Presenta las técnicas de demostración que el curso usa en cada paradigma sobre
algoritmos cuya correctitud no es obvia. El voto mayoritario de Boyer-Moore, con un
invariante de ciclo que no se adivina a primera vista. El emparejamiento estable de
Gale-Shapley: terminación por una función de potencial, estabilidad por contradicción
y optimalidad para quien propone. Incluye un algoritmo aparentemente correcto con un
error sutil, para que el estudiante vea qué atrapa la demostración.

### Conferencia 4. Análisis amortizado

Repasa los métodos agregado, de contabilidad y del potencial sobre un ejemplo corto,
la cola implementada con dos pilas. El resto de la clase aplica el potencial a dos
estructuras con demostración completa. Los splay trees, con el lema de acceso y la
cota amortizada $O(\log n)$ por operación. Union-find con unión por rango y compresión
de caminos, con la cota $O(m \log^* n)$, y el enunciado de la cota de Tarjan con la
inversa de Ackermann.

### Conferencia 5. Cotas mínimas

Cambia la pregunta de "cuánto cuesta este algoritmo" a "cuánto cuesta cualquier
algoritmo para este problema". Argumentos de adversario: mezclar dos listas ordenadas
de tamaño $n$ requiere $2n - 1$ comparaciones, y hallar el segundo mayor requiere
$n + \lceil \log_2 n \rceil - 2$, cota que el torneo alcanza. Cotas condicionales por
reducción: 3SUM-dificultad de problemas geométricos, y la hipótesis SETH con vectores
ortogonales como explicación de por qué nadie ha bajado de $O(n^{2-\varepsilon})$ la
distancia de edición.

## Tema 2. Técnicas generales de solución de problemas

### Conferencia 6. Divide y vencerás: selección y matrices

Selección determinista en tiempo lineal con la mediana de las medianas, usando la
recurrencia de la conferencia 2, y la discusión de por qué grupos de 3 no alcanzan.
Multiplicación de matrices con Strassen en $O(n^{\log_2 7})$, el exponente $\omega$
como pregunta abierta y la reducción de la inversión de matrices a la multiplicación.
Cuándo la mejora asintótica compensa la constante.

### Conferencia 7. Divide y vencerás: la transformada rápida de Fourier

Multiplicación de polinomios en $O(n \log n)$. Representación por coeficientes y por
valores, evaluación en las raíces $n$-ésimas de la unidad por divide y vencerás,
interpolación como la transformada inversa. La variante modular (NTT) para aritmética
exacta, y aplicaciones a multiplicación de enteros grandes y a conteo de sumas de
pares.

### Conferencia 8. Algoritmos golosos con argumentos de intercambio

Argumentos de intercambio en problemas donde la demostración no es inmediata.
Planificación para minimizar el retraso máximo, con la regla del plazo más cercano y
la eliminación de inversiones. Caché óptimo fuera de línea con la regla de Belady
(desalojar lo que se pide más tarde), cuya demostración de optimalidad requiere
transformar paso a paso una planificación óptima arbitraria.

### Conferencia 9. Matroides

Explica cuándo un algoritmo goloso es óptimo para cualquier función de peso. Define
matroide, con los ejemplos lineal, gráfico y de partición. Demuestra el teorema de
Rado-Edmonds: el goloso es óptimo si y solo si la estructura es un matroide. Kruskal
queda como caso particular. Aplicación a la planificación de tareas unitarias con
plazos y penalizaciones. Intersección de dos matroides como frontera: el goloso ya no
basta y aparece el emparejamiento bipartito.

### Conferencia 10. Programación dinámica sobre árboles y subconjuntos

Principio de optimalidad y elección del estado en estructuras distintas a una
secuencia. DP sobre árboles: conjunto independiente de peso máximo y la técnica de
re-enraizamiento para responder la pregunta desde todos los vértices en $O(n)$. DP
sobre subconjuntos: Held-Karp para TSP en $O(2^n n^2)$ frente a $O(n!)$, primer
ejemplo del curso de un algoritmo exacto exponencial que mejora la fuerza bruta.

### Conferencia 11. Optimizaciones de programación dinámica

Cómo bajar el costo de una DP cuya recurrencia ya es correcta. Árbol binario de
búsqueda óptimo con la optimización de Knuth, de $O(n^3)$ a $O(n^2)$, con la
demostración de monotonía de la raíz óptima. Alineamiento de secuencias con
Hirschberg en espacio lineal, combinando programación dinámica y divide y vencerás.
Mención de la optimización por divide y vencerás y del convex hull trick.

### Conferencia 12. Búsqueda exacta con garantías

Backtracking y branch and bound con cotas que se pueden demostrar. Árboles de búsqueda
acotados para vertex cover parametrizado por $k$, en $O(2^k (n + m))$, como primera
idea de complejidad parametrizada. Algoritmos de ramificación para conjunto
independiente máximo con análisis por recurrencia, $T(n) = T(n-1) + T(n-4)$, que da
$O(1.38^n)$. Branch and bound sobre mochila con la cota de la mochila fraccionaria.

### Conferencia 13. Flujo máximo: Dinic

Redes residuales, caminos de aumento y el teorema Max-Flow Min-Cut con demostración,
de forma breve. El algoritmo de Dinic: grafo de niveles, flujo bloqueante, y la
demostración de que la distancia de $s$ a $t$ crece en cada fase, que da
$O(V^2 E)$. Redes de capacidad unitaria en $O(E \sqrt{V})$ y emparejamiento bipartito
como caso particular (Hopcroft-Karp).

### Conferencia 14. Flujo máximo: push-relabel

Un enfoque distinto: en lugar de caminos de aumento, preflujos que respetan
capacidades y violan la conservación. Operaciones de empuje y reetiquetado, la
función de altura como invariante, y la demostración de correctitud y de la cota
$O(V^2 E)$ contando empujes saturantes y no saturantes. Las variantes FIFO en
$O(V^3)$ y de mayor etiqueta en $O(V^2 \sqrt{E})$, y las heurísticas de relabel global
y gap que la hacen rápida en la práctica.

### Conferencia 15. Modelar con flujos y cortes

Cómo convertir un problema nuevo en una red y demostrar que la reducción es correcta.
Selección de proyectos y segmentación de imágenes como cortes mínimos. Eliminación en
campeonatos de béisbol, donde el corte mínimo da el certificado de imposibilidad.
Asignación de costo mínimo con flujo de costo mínimo por caminos de aumento más
baratos y potenciales de Johnson.

**Parcial 1**, sobre los paradigmas del Tema 2.

## Tema 3. Tratamiento de la intratabilidad con garantías formales

### Conferencia 16. Reconocer un problema NP-completo

Repaso práctico de P, NP y NP-completitud, que el estudiante trae de Teoría de la
Computación. Recorre el catálogo clásico (SAT, 3-SAT, clique, vertex cover, ciclo
hamiltoniano, TSP, suma de subconjuntos, mochila, set cover) y el uso de reducciones
para reconocer que una variante nueva es difícil. Presenta el mapa de opciones del
resto del tema. Primer ejemplo: la DP pseudopolinomial de la mochila, convertida en
FPTAS por redondeo de valores, con las definiciones de PTAS y FPTAS.

### Conferencia 17. Aproximaciones golosas

La técnica de comparar contra una cota del óptimo que sí se puede calcular.
Balanceo de carga con la regla de Graham, razón $2 - 1/m$, y con LPT, razón $4/3$.
Centros con $k$-center, razón 2, y la demostración de que no hay razón $2 - \varepsilon$
si $P \ne NP$. Set cover goloso con razón $H_n$, demostrada por reparto de costos.

### Conferencia 18. TSP métrico y redondeo de programas lineales

TSP métrico con el doble árbol, razón 2, y Christofides, razón $3/2$, con
emparejamiento perfecto de costo mínimo sobre los vértices de grado impar. TSP
general sin aproximación con razón constante si $P \ne NP$. Vertex cover con pesos
por relajación lineal y redondeo, razón 2, como introducción al uso de programación
lineal para diseñar aproximaciones.

### Conferencia 19. Algoritmos aleatorios Las Vegas

Distingue Las Vegas (siempre correcto, tiempo aleatorio) de Monte Carlo (tiempo
acotado, puede fallar). Técnica de variables indicadoras sobre quickselect
aleatorio. Hashing universal con una familia concreta y la cota de colisiones
esperadas. Hashing perfecto de Fredman, Komlós y Szemerédi: búsqueda en $O(1)$ en el
peor caso con espacio $O(n)$ esperado.

### Conferencia 20. Algoritmos aleatorios Monte Carlo

Verificación de identidades: Freivalds para productos de matrices y el lema de
Schwartz-Zippel. Algoritmo de Karger para corte mínimo, con probabilidad de éxito
$\ge 2/(n(n-1))$ y amplificación por repetición, y la mejora de Karger-Stein a
$O(n^2 \log^3 n)$. Cierra el curso volviendo al ciclo de la conferencia 1, con la
probabilidad como parte de la garantía.

**Parcial 2**, sobre aproximación, esquemas de aproximación y algoritmos aleatorios.

**Examen final escrito integrador**, sobre los tres temas.
