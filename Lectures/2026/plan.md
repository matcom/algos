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

Las demostraciones de correctitud, los análisis de complejidad, las cotas mínimas y
las garantías de aproximación o probabilísticas se escriben a mano, sin herramientas
de generación. Implementar, probar y depurar con ayuda de IA está permitido, siempre
que se declare.

Bibliografía básica: Cormen, Leiserson, Rivest y Stein, *Introduction to Algorithms*
(CLRS); Kleinberg y Tardos, *Algorithm Design* (KT).

## Tema 1. Fundamentos teóricos para el diseño y análisis

### Conferencia 1. El oficio algorítmico

Presenta el ciclo problema, algoritmo, correctitud, complejidad, cota mínima, que se
repite en todo el curso. El ejemplo conductor es un problema pequeño con varias
soluciones de costo distinto, por ejemplo el subarreglo de suma máxima, que admite
una solución cúbica, una cuadrática, una por divide y vencerás en $O(n \log n)$ y una
lineal. Repasa las notaciones $O$, $\Omega$, $\Theta$, $o$ y $\omega$ como conocimiento
previo y fija qué cuenta como operación elemental en el modelo RAM. Cierra con la
organización del curso, la evaluación y las reglas de uso de IA.

### Conferencia 2. Ecuaciones de recurrencia

Parte del costo de un algoritmo recursivo y lo escribe como recurrencia. Resuelve
recurrencias por sustitución (adivinar y demostrar por inducción) y con el árbol de
recurrencia. Enuncia el Teorema Maestro en sus tres casos, lo aplica a mergesort,
búsqueda binaria y Karatsuba, y muestra recurrencias donde no aplica, como
$T(n) = 2T(n/2) + n/\log n$.

### Conferencia 3. Demostrar que un algoritmo es correcto

Presenta las técnicas de demostración que el curso usa después en cada paradigma. El
invariante de ciclo, con sus tres obligaciones (inicialización, mantenimiento,
terminación), sobre insertion sort y la búsqueda binaria. La inducción estructural
sobre un algoritmo recursivo. El argumento por contradicción, y el argumento de
intercambio como adelanto de los algoritmos golosos. Incluye un algoritmo
aparentemente correcto con un error sutil, para que el estudiante vea qué atrapa la
demostración.

### Conferencia 4. Análisis amortizado

Explica por qué el peor caso de una operación aislada sobreestima el costo de una
secuencia de operaciones. Presenta los métodos agregado, de contabilidad y del
potencial sobre el mismo ejemplo, el array dinámico que duplica su capacidad. Aplica
el potencial a la tabla hash dinámica y presenta union-find con unión por rango y
compresión de caminos, enunciando la cota con la función inversa de Ackermann sin
demostrarla completa.

### Conferencia 5. Cotas mínimas

Cambia la pregunta de "cuánto cuesta este algoritmo" a "cuánto cuesta cualquier
algoritmo para este problema". Demuestra la cota $\Omega(n \log n)$ para ordenar por
comparaciones con árboles de decisión. Presenta cotas por reducción (por ejemplo,
envolvente convexa a partir de ordenamiento) y argumentos de adversario, con el
mínimo y el máximo simultáneos en $\lceil 3n/2 \rceil - 2$ comparaciones. Cierra
mostrando que counting sort no contradice la cota porque no compara.

## Tema 2. Técnicas generales de solución de problemas

### Conferencia 6. Divide y vencerás: ordenamiento y selección

Formaliza el esquema dividir, resolver y combinar. Mergesort con demostración de
correctitud y análisis por recurrencia. Quicksort determinista con su peor caso
cuadrático. Estadística de orden: selección en tiempo lineal esperado y el algoritmo
de la mediana de las medianas en tiempo lineal en el peor caso, con la recurrencia
$T(n) \le T(n/5) + T(7n/10) + O(n)$.

### Conferencia 7. Divide y vencerás: aritmética

Multiplicación de enteros grandes con Karatsuba, de $O(n^2)$ a $O(n^{\log_2 3})$.
Multiplicación de matrices con Strassen, de $O(n^3)$ a $O(n^{\log_2 7})$. Discute
cuándo la mejora asintótica compensa la constante y por qué las implementaciones
reales cambian al algoritmo clásico por debajo de un umbral.

### Conferencia 8. Algoritmos golosos y argumentos de intercambio

Define la decisión golosa y las dos propiedades que la justifican: elección golosa y
subestructura óptima. Selección de actividades con demostración por intercambio.
Contraejemplos donde el criterio goloso falla (otras reglas de selección, cambio de
monedas con denominaciones arbitrarias). Códigos de Huffman con demostración de
optimalidad.

### Conferencia 9. Golosos en grafos

Árboles recubridores mínimos con la propiedad del corte como argumento de
intercambio general, y Prim y Kruskal como dos formas de aplicarla. Kruskal se apoya
en el union-find de la conferencia 4. Caminos mínimos con Dijkstra, demostración por
invariante y el contraejemplo con pesos negativos.

### Conferencia 10. Programación dinámica: principios

Parte de una recursión con subproblemas repetidos, por ejemplo el corte de varillas o
la planificación de intervalos con pesos, y mide el costo exponencial de la versión
ingenua. Enuncia el principio de optimalidad. Presenta memoización y tabulación como
dos implementaciones de la misma recurrencia, y el procedimiento de reconstrucción de
la solución a partir de la tabla.

### Conferencia 11. Programación dinámica sobre secuencias

Subsecuencia común más larga y distancia de edición, con la recurrencia, el orden de
llenado de la tabla y la reducción de memoria a dos filas. Mochila entera con la
solución en $O(nW)$, y la discusión de por qué ese tiempo es pseudopolinomial y no
contradice que el problema sea NP-completo.

### Conferencia 12. Programación dinámica sobre intervalos y grafos

Multiplicación encadenada de matrices como ejemplo de DP sobre intervalos, con tabla
en $O(n^3)$. Floyd-Warshall como DP sobre el conjunto de vértices intermedios
permitidos, con demostración del principio de optimalidad y detección de ciclos
negativos.

### Conferencia 13. Búsqueda combinatoria

Backtracking como recorrido del árbol de soluciones parciales, con n-reinas y suma de
subconjuntos. Poda por factibilidad y poda por cota. Branch and bound sobre mochila,
con la cota de la mochila fraccionaria. Explica qué garantiza la búsqueda exacta
(optimalidad) y qué no garantiza (tiempo polinomial).

### Conferencia 14. Flujo máximo

Redes de flujo, flujos, residuales y caminos de aumento. Ford-Fulkerson, su
terminación con capacidades enteras y su comportamiento con capacidades irracionales.
Enuncia y demuestra el teorema Max-Flow Min-Cut. Edmonds-Karp y la cota
$O(VE^2)$.

### Conferencia 15. Aplicaciones de flujo

Emparejamiento bipartito máximo como flujo, con la integralidad del flujo como
argumento de correctitud. Relación con el teorema de Hall visto en Teoría de Grafos.
Problemas de asignación y de caminos disjuntos. El objetivo es que el estudiante
aprenda a modelar un problema nuevo como red de flujo y a justificar que la
reducción es correcta.

**Parcial 1**, sobre los cinco paradigmas del Tema 2.

## Tema 3. Tratamiento de la intratabilidad con garantías formales

### Conferencia 16. Reconocer un problema NP-completo

Repaso práctico de P, NP y NP-completitud, que el estudiante trae de Teoría de la
Computación. Recorre el catálogo clásico (SAT, 3-SAT, clique, vertex cover, conjunto
independiente, ciclo hamiltoniano, TSP, suma de subconjuntos, mochila, set cover) y
el uso de reducciones para reconocer que una variante nueva es difícil. Cierra con el
mapa de opciones del resto del tema: resolver exacto en instancias pequeñas,
aproximar con garantía o aleatorizar.

### Conferencia 17. Algoritmos de aproximación

Define la razón de aproximación $\alpha$ para minimización y maximización, y la
técnica de acotar contra una cota del óptimo que sí se puede calcular. Vertex cover
2-aproximado con emparejamiento maximal. TSP métrico 2-aproximado con árbol
recubridor mínimo y la desigualdad triangular. Resultado de inaproximabilidad del TSP
general si $P \ne NP$.

### Conferencia 18. Set cover y esquemas de aproximación

Set cover goloso con razón $H_n = O(\log n)$ y su demostración por reparto de costos.
Definición de PTAS y FPTAS. FPTAS para mochila por redondeo de valores sobre la DP de
la conferencia 11, con demostración de la razón $1 - \varepsilon$ y del tiempo
polinomial en $n$ y $1/\varepsilon$.

### Conferencia 19. Algoritmos aleatorios Las Vegas

Distingue Las Vegas (siempre correcto, tiempo aleatorio) de Monte Carlo (tiempo
acotado, puede fallar). Quicksort aleatorizado con análisis del tiempo esperado por
variables indicadoras. Hashing universal, con la definición de familia universal, una
construcción concreta y la cota del número esperado de colisiones.

### Conferencia 20. Algoritmos aleatorios Monte Carlo

Verificación aleatoria de identidades con el algoritmo de Freivalds para productos de
matrices y el lema de Schwartz-Zippel. Algoritmo de Karger para corte mínimo, con la
probabilidad de éxito $\ge 2/(n(n-1))$ y la amplificación por repetición. Cierra el
curso volviendo al ciclo de la conferencia 1, con la probabilidad como parte de la
garantía.

**Parcial 2**, sobre aproximación, esquemas de aproximación y algoritmos aleatorios.

**Examen final escrito integrador**, sobre los tres temas.
