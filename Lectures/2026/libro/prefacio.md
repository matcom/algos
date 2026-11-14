# Prefacio {.unnumbered #prefacio}

Este libro reúne las conferencias de Diseño y Análisis de Algoritmos en la Facultad de
Matemática y Computación de la Universidad de La Habana, para la carrera de Ciencia de
la Computación. Cada capítulo es una conferencia, y se lee en el mismo orden en que se
imparte.

Supone lo que el estudiante vio en Programación y en Estructuras de Datos y Algoritmos:
la búsqueda binaria, los ordenamientos por comparación, BFS y DFS, Dijkstra,
Bellman-Ford, Floyd-Warshall, los árboles recubridores mínimos, union-find, los heaps,
las tablas hash y la programación dinámica clásica (subsecuencia común más larga,
mochila entera, subsecuencia creciente más larga). Esos algoritmos aparecen aquí como
herramientas o como punto de partida. No supone nada sobre P, NP ni reducciones, ni la
demostración de la cota mínima para ordenar por comparaciones, que el capítulo 5 hace
entera. El lenguaje del código es Python.

Cada capítulo recorre el mismo ciclo sobre un problema concreto: enunciar el problema,
proponer un algoritmo, demostrar que es correcto, analizar su complejidad y, cuando se
puede, dar una cota mínima que diga que no se puede hacer mejor. Muchos capítulos
plantan además un error a propósito, en un algoritmo o en una demostración, para que
se vea cómo falla y qué lo detecta.

Todo el código del libro se ejecutó para construirlo. Lo que aparece debajo de cada
bloque es lo que imprimió ese bloque, y las figuras que ilustran un
algoritmo se dibujan con el estado que ese algoritmo calculó. Los tiempos que se miden
dependen de la máquina en que se construyó el libro: en la tuya serán otros, pero las
razones entre ellos, que es lo que el texto discute, deberían parecerse.

El libro tiene tres partes, que son los tres temas del programa de la asignatura. La
primera, Fundamentos, fija qué es un algoritmo eficiente y correcto y cómo se demuestra
una cota mínima. La segunda, Estrategias, estudia las técnicas generales de diseño:
divide y vencerás, algoritmos golosos, programación dinámica, flujo máximo y
algoritmos aleatorios. La tercera, Intratabilidad, define P y NP y trata los problemas
NP-duros con garantías formales. Cada parte cierra con un resumen de sus ideas y
ejercicios que integran sus capítulos, y un epílogo recoge problemas que siguen
abiertos.

Cada capítulo termina con un resumen y al menos diez ejercicios. Las demostraciones de
correctitud, los análisis de complejidad, las cotas mínimas, las reducciones y las
garantías de aproximación o probabilísticas se escriben a mano, sin herramientas de
generación. Implementar, probar y depurar con ayuda de IA está permitido, siempre que
se declare.

La bibliografía básica del curso es *Introduction to Algorithms*, de Cormen, Leiserson,
Rivest y Stein, y *Algorithm Design*, de Kleinberg y Tardos.

El libro se lee en línea en <https://matcom.github.io/algos/> y se descarga completo en
PDF desde <https://matcom.github.io/algos/daa.pdf>. Las dos versiones salen del mismo
texto y se actualizan juntas.
