# Diseño y Análisis de Algoritmos: plan de conferencias 2026

Este plan sigue el programa de la asignatura en el plan de estudio de Ciencia de la
Computación (disciplina Matemática Computacional). El programa reparte 48 horas en
tres temas: 20 horas de conferencia, 24 de clase práctica y 4 de evaluación, más el
examen final escrito integrador. El programa distribuye las conferencias 5, 10 y 5
entre los temas. Este plan las distribuye 5, 10 y 8, y suma una conferencia final
sobre las fronteras del área: 24 en total. El Tema 2 crece porque divide y vencerás
necesita una conferencia de recurrencias antes de la FFT, y porque los algoritmos
aleatorios pasan a ser una técnica de diseño más, en dos conferencias. El Tema 3 queda
solo para la intratabilidad, y la NP-completitud se da desde cero en cuatro
conferencias propias.

| Tema | Conferencias | Evaluación |
|---|---|---|
| 1. Fundamentos teóricos para el diseño y análisis | 5 | |
| 2. Técnicas generales de solución de problemas | 10 | Parcial 1 |
| 3. Tratamiento de la intratabilidad con garantías formales | 8 | Parcial 2 |
| Cierre: fronteras del área | 1 | |

Cada conferencia recorre el mismo ciclo sobre un problema concreto: enunciar el
problema, proponer un algoritmo, demostrar que es correcto, analizar su complejidad y,
cuando se pueda, dar una cota mínima para el problema. Después de cada conferencia se
orientan ejercicios para la casa, y la clase práctica siguiente se dedica a problemas
que el estudiante no ha visto.

El curso asume la búsqueda binaria, que el estudiante vio en Programación en primer
año, y lo que vio en Estructuras de Datos y Algoritmos: ordenamientos por
comparación, BFS y DFS, Dijkstra, Bellman-Ford,
Floyd-Warshall, árboles recubridores mínimos, union-find, heaps, tablas hash, el
Teorema Maestro (que la conferencia 6 formaliza) y la programación dinámica clásica (subsecuencia común más larga,
mochila entera, subsecuencia creciente más larga). Esos algoritmos aparecen aquí como
herramientas o como punto de partida, y cada conferencia trae técnicas y problemas
nuevos. El curso no asume nada sobre P, NP ni reducciones, ni la demostración de la
cota $\Omega(n \log n)$ para ordenar por comparaciones, que la conferencia 5 hace entera.

Las demostraciones de correctitud, los análisis de complejidad, las cotas mínimas, las
reducciones y las garantías de aproximación o probabilísticas se escriben a mano, sin
herramientas de generación. Implementar, probar y depurar con ayuda de IA está
permitido, siempre que se declare.

Bibliografía básica: Cormen, Leiserson, Rivest y Stein, *Introduction to Algorithms*
(CLRS); Kleinberg y Tardos, *Algorithm Design* (KT).

## Tema 1. Fundamentos teóricos para el diseño y análisis

### Conferencia 1. Qué significa que un algoritmo es eficiente

Conferencia introductoria. Parte de la máquina de Turing como definición de lo
computable y explica por qué no sirve para medir costos realistas: acceder a la
posición $i$ de la cinta cuesta $i$ pasos. Presenta el modelo RAM como el modelo en el
que el curso cuenta operaciones, y qué se gana y qué se esconde al contar operaciones
en lugar de segundos. Repasa las notaciones $O$, $\Omega$, $\Theta$, $o$ y $\omega$.
Explica por qué se mide tiempo y memoria, y por qué la diferencia entre $O(n)$ y
$O(n^2)$ crece cuando mejora la computadora: con una máquina diez veces más rápida,
el tamaño de problema que se resuelve en una hora se multiplica por 10 en el primer
caso y por $\sqrt{10} \approx 3.2$ en el segundo. Con la prueba de primalidad por
división hasta $\sqrt{n}$ muestra que el tamaño de la entrada es la cantidad de bits,
$\log_2 n$, y que ese algoritmo es exponencial en ese tamaño. De ahí la convención del
modelo RAM de contar la aritmética como $O(1)$, cuándo es razonable (palabras de
$O(\log n)$ bits) y por qué en los algoritmos numéricos se cuenta el costo por bit.
Cierra con el programa de la asignatura, la organización del curso, la evaluación y
las reglas de uso de IA.

### Conferencia 2. El oficio algorítmico

Presenta el ciclo problema, algoritmo, correctitud, complejidad, cota mínima, que se
repite en todo el curso, recorriéndolo completo sobre el par de puntos más cercanos en
el plano. La fuerza bruta cuesta $O(n^2)$. Divide y vencerás baja a $O(n \log n)$, con
el argumento de que en la franja central basta revisar un número constante de vecinos.
La cota $\Omega(n \log n)$ en árboles de decisión algebraicos sale por reducción desde
distinción de elementos. El algoritmo aleatorio de Rabin con rejilla llega a $O(n)$
esperado, que muestra qué supuestos del modelo esconde la cota.

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
algoritmo para este problema". Árboles de decisión y argumentos de información.
Argumentos de adversario: mezclar dos listas ordenadas de tamaño $n$ requiere $2n - 1$
comparaciones, y hallar el segundo mayor requiere $n + \lceil \log_2 n \rceil - 2$,
cota que el torneo alcanza. Las recurrencias que el Teorema Maestro no resuelve se
tratan en las conferencias donde aparecen.

## Tema 2. Técnicas generales de solución de problemas

### Conferencia 6. Divide y vencerás y recurrencias

La técnica y su herramienta de análisis. Karatsuba multiplica enteros de $n$ dígitos
con la recurrencia $T(n) = 3T(n/2) + O(n)$, que da $O(n^{\log_2 3}) \approx
O(n^{1.585})$, y cierra la pregunta de la conferencia 1 sobre el costo de
multiplicar. Selección en tiempo lineal con la mediana de las medianas, cuya
recurrencia $T(n) \le T(n/5) + T(7n/10) + O(n)$ el Teorema Maestro no resuelve. El
árbol de recursión como método general, y el Teorema Maestro como el corolario que
casi siempre alcanza, con lo que no cubre: particiones desiguales, cambio de variable y
el $n \log^2 n$ de la conferencia 2.

### Conferencia 7. Divide y vencerás: la transformada rápida de Fourier

Multiplicación de polinomios en $O(n \log n)$. Representación por coeficientes y por
valores, evaluación en las raíces $n$-ésimas de la unidad por divide y vencerás,
interpolación como la transformada inversa. La variante modular (NTT) para aritmética
exacta, y aplicaciones a multiplicación de enteros grandes y a conteo de sumas de
pares.

### Conferencia 8. Algoritmos aleatorios I: Las Vegas y costo esperado

Algoritmos que usan azar y siempre dan la respuesta correcta, con un tiempo que es una
variable aleatoria. Quicksort aleatorio con $2n \ln n$ comparaciones esperadas,
demostrado con variables indicadoras: los elementos $i$ y $j$ se comparan con
probabilidad $2/(j - i + 1)$. Quickselect en $O(n)$ esperado, frente a la selección
determinista de la conferencia 6. Hashing universal con una familia concreta y la cota
de colisiones esperadas. Cierra dos hilos: el algoritmo incremental de la conferencia 2
es Las Vegas, y la garantía esperada se distingue del costo amortizado de la
conferencia 4, que no tiene probabilidad.

### Conferencia 9. Algoritmos golosos con argumentos de intercambio

Argumentos de intercambio en problemas donde la demostración no es inmediata.
Planificación para minimizar el retraso máximo, con la regla del plazo más cercano y
la eliminación de inversiones. Caché óptimo fuera de línea con la regla de Belady
(desalojar lo que se pide más tarde), cuya demostración de optimalidad requiere
transformar paso a paso una planificación óptima arbitraria.

### Conferencia 10. Matroides

Explica cuándo un algoritmo goloso es óptimo para cualquier función de peso. Define
matroide, con los ejemplos lineal, gráfico y de partición. Demuestra el teorema de
Rado-Edmonds: el goloso es óptimo si y solo si la estructura es un matroide. Kruskal
queda como caso particular. Aplicación a la planificación de tareas unitarias con
plazos y penalizaciones. Intersección de dos matroides como frontera: el goloso ya no
basta y aparece el emparejamiento bipartito.

### Conferencia 11. Programación dinámica sobre árboles y subconjuntos

Principio de optimalidad y elección del estado en estructuras distintas a una
secuencia. DP sobre árboles: conjunto independiente de peso máximo y la técnica de
re-enraizamiento para responder la pregunta desde todos los vértices en $O(n)$. DP
sobre subconjuntos: Held-Karp para TSP en $O(2^n n^2)$ frente a $O(n!)$, primer
ejemplo del curso de un algoritmo exacto exponencial que mejora la fuerza bruta.

### Conferencia 12. Optimizaciones de programación dinámica

Cómo bajar el costo de una DP cuya recurrencia ya es correcta. Árbol binario de
búsqueda óptimo con la optimización de Knuth, de $O(n^3)$ a $O(n^2)$, con la
demostración de monotonía de la raíz óptima. Alineamiento de secuencias con
Hirschberg en espacio lineal, combinando programación dinámica y divide y vencerás.
Mención de la optimización por divide y vencerás y del convex hull trick.

### Conferencia 13. Flujo máximo: Dinic

Redes residuales, caminos de aumento y el teorema Max-Flow Min-Cut con demostración.
El algoritmo de Dinic: grafo de niveles, flujo bloqueante, y la demostración de que la
distancia de $s$ a $t$ crece en cada fase, que da $O(V^2 E)$. Redes de capacidad
unitaria en $O(E \sqrt{V})$ y emparejamiento bipartito como caso particular
(Hopcroft-Karp).

### Conferencia 14. Flujo máximo: push-relabel

Un enfoque distinto: en lugar de caminos de aumento, preflujos que respetan
capacidades y violan la conservación. Operaciones de empuje y reetiquetado, la
función de altura como invariante, y la demostración de correctitud y de la cota
$O(V^2 E)$ contando empujes saturantes y no saturantes. Las variantes FIFO en
$O(V^3)$ y de mayor etiqueta en $O(V^2 \sqrt{E})$, y las heurísticas de relabel global
y gap que la hacen rápida en la práctica. El modelado de problemas con flujos y cortes
(selección de proyectos, eliminación en campeonatos, asignación de costo mínimo) se
trabaja en las clases prácticas.

### Conferencia 15. Algoritmos aleatorios II: Monte Carlo

Algoritmos de tiempo acotado que pueden equivocarse con probabilidad controlada, y la
amplificación por repetición. Verificación de productos de matrices con Freivalds, con
error a lo sumo $1/2$ por ronda. Algoritmo de Karger para el corte mínimo global, con
probabilidad de éxito $\ge 2/(n(n-1))$ y la repetición que la lleva a alta
probabilidad, en contraste con el corte $s$-$t$ que da Max-Flow Min-Cut en la
conferencia 13. Cierra el tema con la probabilidad como parte de la garantía.

**Parcial 1**, sobre las técnicas del Tema 2, incluidos los algoritmos aleatorios.

## Tema 3. Tratamiento de la intratabilidad con garantías formales

### Conferencia 16. P, NP y reducciones

Problemas de decisión frente a problemas de optimización, y por qué basta estudiar la
versión de decisión. La clase P. La clase NP definida por certificados verificables en
tiempo polinomial. Reducción polinomial, su transitividad, y las definiciones de
NP-duro y NP-completo. La receta de una demostración de NP-completitud: pertenencia a
NP, construcción polinomial, y las dos direcciones de la equivalencia. Primeras
reducciones entre conjunto independiente, clique y vertex cover, cortas para que la
atención esté en la estructura de la demostración. La pregunta P vs NP y qué
significaría cada respuesta.

### Conferencia 17. Cook-Levin: SAT y 3-SAT

El primer problema NP-completo, que no puede salir de una reducción desde otro.
Demostración del teorema de Cook-Levin: dada una máquina de Turing no determinista
que decide un problema en tiempo polinomial, se construye una fórmula que es
satisfacible si y solo si la máquina acepta, a partir de la tabla de configuraciones.
Paso a forma normal conjuntiva. Reducción de SAT a 3-SAT partiendo cláusulas largas
con variables nuevas. 3-SAT queda como punto de partida del resto de las reducciones. La máquina de Turing de la conferencia 1 vuelve aquí por primera vez: es la base de la demostración.

### Conferencia 18. Reducciones desde 3-SAT a grafos

Reducción de 3-SAT a conjunto independiente con un triángulo por cláusula y aristas
entre literales contradictorios, y por la conferencia 16, clique y vertex cover como
corolarios. Vertex cover a set cover. Reducción de 3-SAT a 3-coloración con gadgets:
el triángulo de verdad, falso y base, y el gadget de cláusula que no admite colorear
con los tres literales falsos. Qué hace un buen gadget y cómo se verifica.

### Conferencia 19. Reducciones a secuencias y números

Reducción de 3-SAT a ciclo hamiltoniano dirigido, con una fila de vértices por
variable recorrida en uno de dos sentidos y un vértice por cláusula. Paso a ciclo
hamiltoniano no dirigido, y de ahí a la versión de decisión de TSP. Reducción de 3-SAT
a suma de subconjuntos con números escritos en base 10, uno por literal y por
cláusula, y de suma de subconjuntos a mochila. Con esto quedan demostrados SAT, 3-SAT,
conjunto independiente, clique, vertex cover, set cover, 3-coloración, ciclo
hamiltoniano, TSP, suma de subconjuntos y mochila.

### Conferencia 20. Resolver exacto un problema NP-duro

Qué se puede garantizar cuando se quiere la respuesta óptima. Branch and bound sobre
mochila con la cota de la mochila fraccionaria. Árboles de búsqueda acotados para
vertex cover parametrizado por $k$, en $O(2^k (n + m))$, como primera idea de
complejidad parametrizada. Algoritmos de ramificación para conjunto independiente
máximo con análisis por recurrencia, $T(n) = T(n-1) + T(n-4)$, que da $O(1.38^n)$.
Las hipótesis ETH y SETH como límite de cuánto se puede bajar la base de la
exponencial.

### Conferencia 21. Algoritmos de aproximación

Definición de razón de aproximación $\alpha$ para minimización y maximización, y la
técnica de comparar contra una cota del óptimo que sí se puede calcular. Vertex cover
con razón 2 por emparejamiento maximal. Balanceo de carga con la regla de Graham,
razón $2 - 1/m$, y con LPT, razón $4/3$. Centros con $k$-center, razón 2, y la
demostración de que no hay razón $2 - \varepsilon$ si $P \ne NP$. Set cover goloso con
razón $H_n$, demostrada por reparto de costos. Como ejemplo aleatorio, una asignación al azar satisface en esperanza 7/8 de las cláusulas de MAX-3SAT, por linealidad de la esperanza (conferencia 8).

### Conferencia 22. TSP métrico y redondeo de programas lineales

TSP general sin aproximación con razón constante si $P \ne NP$, usando la reducción
desde ciclo hamiltoniano de la conferencia 19. TSP métrico con el doble árbol, razón
2, y Christofides, razón $3/2$, con emparejamiento perfecto de costo mínimo sobre los
vértices de grado impar. Vertex cover con pesos por relajación lineal y redondeo,
razón 2, como introducción al uso de programación lineal para diseñar
aproximaciones.

### Conferencia 23. Esquemas de aproximación

Definiciones de PTAS y FPTAS. FPTAS para mochila por redondeo de valores sobre la DP
pseudopolinomial, con demostración de la razón $1 - \varepsilon$ y del tiempo
polinomial en $n$ y $1/\varepsilon$. NP-dificultad fuerte, y por qué excluye un FPTAS
para problemas como 3-partición. PTAS para balanceo de carga con un número fijo de
máquinas, cerrando lo visto en la conferencia 21.

**Parcial 2**, sobre NP-completitud, algoritmos exactos y aproximación.

## Cierre

### Conferencia 24. Fronteras del diseño y análisis de algoritmos

El estado del arte al momento de dictarla, como colofón de lo que los estudiantes van
a encontrar al salir. Todas las afirmaciones se verifican contra fuentes primarias al
redactarla, y la conferencia lleva la fecha.

- **P vs NP.** Dónde está la pregunta y por qué es difícil: las tres barreras que
  descartan familias enteras de demostraciones (relativización, pruebas naturales y
  algebrización). La complejidad de grano fino como lo que la investigación hace
  mientras tanto: SETH, 3SUM y caminos mínimos entre todos los pares como hipótesis
  que explican por qué ciertos algoritmos polinomiales no mejoran.
- **Problemas clásicos que se movieron hace poco.** Flujo máximo y de costo mínimo en
  tiempo casi lineal (Chen, Kyng, Liu, Peng, Probst Gutenberg y Sachdeva, 2022), que
  vuelve sobre las conferencias 13 y 14. Caminos mínimos desde un origen en grafos
  dirigidos por debajo de la barrera del ordenamiento, $O(m \log^{2/3} n)$ (Duan y
  otros, mejor artículo de STOC 2025), que vuelve sobre la cota de la conferencia 5.
  Dijkstra universalmente óptimo (Haeupler y otros, mejor artículo de FOCS 2024), un
  resultado más fuerte que el peor caso. Tiempo $t$ simulado en espacio
  $O(\sqrt{t \log t})$ (Williams, 2025), que vuelve sobre la máquina de Turing de la
  conferencia 1.
- **Algoritmos descubiertos con ayuda de IA.** Multiplicación de matrices complejas de
  $4 \times 4$ con 48 productos (AlphaEvolve, 2025) y la cota $\omega < 2.371177$ para
  el exponente de la multiplicación de matrices (Google DeepMind con colaboradores
  académicos, agosto de 2026). Qué significa que una búsqueda automática mejore una
  cota, y los algoritmos galácticos, que son asintóticamente mejores e inútiles en la
  práctica.
- **Lo que el curso no trató.** Algoritmos en línea y análisis competitivo, streaming y
  algoritmos sublineales, algoritmos con predicciones, análisis suavizado (por qué el
  símplex funciona), algoritmos paralelos y distribuidos, algoritmos cuánticos (Shor y
  Grover) y complejidad en el caso promedio.
- **Cierre del curso.** El ciclo de la conferencia 2 como método de investigación: los
  resultados de esta conferencia son vueltas completas del mismo ciclo, hechas por
  gente que aprendió lo que el curso enseñó.

**Examen final escrito integrador**, sobre los tres temas.
