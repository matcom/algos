# Outline: Capítulo 22, TSP métrico y redondeo de programas lineales

Estado: redactado (2026-11-13) dentro del flujo del libro; pendiente de revisión.
Destino: `Lectures/2026/22-tsp-lp/notas.md` en formato de libro, figuras en
`Lectures/2026/figuras_22.py`.
Extensión objetivo: 5 500–7 000 palabras con el código.
Verificaciones: `.playground/libro-daa/verif/22/` (`tsp.py`, `lp.py`, `exp1.py` a
`exp4.py`, `seis.py`, y las búsquedas `busca*.py`, `refina.py`).

## Idea del capítulo

El capítulo 21 fijó la técnica: una cota del óptimo que se puede calcular, y comparar
contra ella. Este capítulo la aplica dos veces con cotas nuevas. En el TSP métrico la
cota es el árbol generador mínimo, y la mejora de 2 a 3/2 sale de mirar qué parte del
doble árbol se paga de más. En vertex cover con pesos la cota es el óptimo de un
programa lineal, que se calcula en tiempo polinomial, y el algoritmo lee la solución
fraccionaria y la redondea. Antes de todo eso, una frontera: sin desigualdad
triangular, el TSP no tiene ninguna razón constante si P ≠ NP, con la reducción del
capítulo 19, §7 cambiando los pesos.

Error plantado: redondear con `round` de Python. `round(1/2)` es 0 (redondeo al par),
y los valores 1/2 son justo los que aparecen en los vértices del poliedro. La batería
que solo mide la razón lo aprueba en las 562 entradas; la que comprueba que la salida
sea un cubrimiento lo atrapa en 99 (en el documento: 456 y 74). La demostración señala el paso: de
$x_u + x_v \ge 1$ sale que uno de los dos vale **al menos** 1/2, con igualdad posible.

Descartado como error plantado (medido): Christofides con emparejamiento goloso.
En 300 entradas al azar no pasa de 1,349, pero las entradas que pasan de 3/2 que
encontró una búsqueda local son frágiles (redondear coordenadas las devuelve por debajo
de 1,5) y no hallé una familia limpia. Y el doble árbol con recorrido en anchura en vez
de preorden lo atrapa cualquier batería (15 de 300 pasan de razón 2).

## Estructura

1. **El viajante, otra vez.** Capítulo 11, §9 (Held-Karp, exacto, $O(2^n n^2)$),
   capítulo 19, §7 (NP-completo, también con distancias 1 y 2) y capítulo 21 (cota del
   óptimo). Las dos partes del capítulo.
2. **Sin desigualdad triangular no hay razón.** Teorema 1: para toda constante
   $\alpha \ge 1$, si P ≠ NP no hay $\alpha$-aproximación del TSP general. Pesos 1 en
   las aristas y $(\alpha - 1)n + 2$ fuera. Código: Petersen (sin ciclo hamiltoniano)
   da óptimo 21 > 20 = $2n$; el cubo da 8. Verificado en `exp4.py`.
3. **La cota del árbol mínimo.** Lema 2: $\mathrm{OPT} \ge$ peso del árbol mínimo
   (quitar una arista del recorrido deja un árbol). Prim en código.
4. **El doble árbol.** Recorrido del árbol duplicado, atajos, preorden. Teorema 3:
   razón 2. El paso que se salta: los atajos usan la desigualdad triangular.
   **Figura**: árbol, paseo doble y recorrido con atajos, sobre 9 puntos (semilla 22).
5. **Contra Held-Karp.** Batería de puntos al azar contra el oráculo. En el documento
   (150 entradas de 5 a 9 puntos, semilla 22): doble árbol peor 1,412, promedio 1,120.
6. **Lo que se paga de más.** El doble duplica todo el árbol para que los grados sean
   pares; basta arreglar los impares. Lema del apretón de manos (ejercicio 5). Euler:
   conexo con grados pares tiene circuito euleriano, demostrado en un párrafo, y
   Hierholzer en código.
7. **Christofides.** Árbol + emparejamiento perfecto mínimo de los impares + circuito
   euleriano + atajos. El emparejamiento en el código es una DP sobre subconjuntos,
   exponencial; el polinomial es Edmonds (1965), que no se estudia. **Figura**: los
   cuatro pasos sobre la misma instancia.
8. **La razón 3/2.** Lema 4: el emparejamiento mínimo de los impares cuesta a lo sumo
   OPT/2 (atajar el óptimo a los impares y partirlo en dos emparejamientos
   alternados). Teorema 5. En el documento: Christofides peor 1,185, promedio 1,038; emparejamiento/OPT hasta 0,498.
9. **3/2 es la razón del algoritmo.** Tira de triángulos con altura 0,85: el árbol es
   el zigzag, los impares son los dos extremos y el emparejamiento cruza la tira. La
   razón contra el borde (un recorrido conocido, cota superior del óptimo) sube con
   $k$: 1,279 ($k = 3$), 1,479 ($k = 100$); el límite es $(2d + 1)/2$ con
   $d = \sqrt{0{,}25 + 0{,}85^2}$, y tiende a 3/2 cuando la altura tiende a
   $\sqrt3/2$. Held-Karp confirma que el borde es óptimo hasta $k = 6$. Estado del
   arte: Karlin, Klein y Oveis Gharan (STOC 2021), aleatorizado, $3/2 - \varepsilon$
   con $\varepsilon > 10^{-36}$; NP-duro por debajo de 123/122 (Karpinski, Lampis y
   Schmied, JCSS 2015).
10. **Vertex cover con pesos.** El emparejamiento del capítulo 21 falla con pesos
    (estrella con centro barato). Programa entero, relajación, Lema 6: LP ≤ OPT.
    **Figura**: el poliedro del triángulo, con sus cinco vértices calculados por
    enumeración: cuatro enteros y $(1/2, 1/2, 1/2)$.
11. **Resolver el programa lineal.** Khachiyan: tiempo polinomial. En el código, un
    simplex exacto con fracciones que no se estudia, aplicado al cambio $z = 1 - x$ para
    que el origen sea factible. Comprobado contra la enumeración de vértices: 0
    diferencias en 92 grafos de hasta 5 vértices.
12. **Redondear.** Teorema 7 (Hochbaum, 1982): tomar $x_v \ge 1/2$ da razón 2.
    Batería contra fuerza bruta (456 grafos): peor 2,0 (el triángulo con pesos 16, 4, 20), y todos
    los valores del simplex en $\{0, 1/2, 1\}$ (Nemhauser y Trotter; ejercicio 6).
13. **El error plantado: `round`.** Lo de arriba.
14. **La regla.** La cota decide la razón; tabla con las tres cotas del capítulo.

## Ejercicios

1. [traza] Doble árbol a mano sobre los 6 puntos $(0,5), (2,0), (4,0), (4,3), (7,6),
   (8,4)$ (distancias distintas dos a dos; búsqueda en `seis.py`).
2. [demostración] Los atajos no alargan el recorrido.
3. [entrada que rompe] Familia métrica donde el doble árbol se acerca a 2.
4. [traza] Christofides sobre los mismos 6 puntos (4 impares, emparejamiento único).
5. [demostración] El número de vértices de grado impar es par.
6. [demostración ★] La relajación tiene un óptimo con valores en $\{0, 1/2, 1\}$.
7. [entrada que rompe] Relajación contra entero en $K_n$, y qué dice sobre el análisis.
8. [modelar] Set cover con pesos por redondeo, razón $f$.
9. [implementar y medir] Doble árbol y Christofides contra Held-Karp.
10. [cambio de hipótesis] TSP asimétrico.

## Citas verificadas

- Sahni y Gonzalez, "P-Complete Approximation Problems", JACM 23(3):555–565, 1976
  (Crossref).
- Christofides, "Worst-case analysis of a new heuristic for the travelling salesman
  problem", Management Science Research Report 388, Carnegie-Mellon University, 1976;
  reimpreso en Operations Research Forum 3, 2022 (Crossref y la bibliografía de van
  Bevern y Slugina).
- Serdyukov, "O nekotorykh ekstremal'nykh obkhodakh v grafakh", Upravlyaemye sistemy
  17:76–79, 1978; van Bevern y Slugina, Historia Mathematica 53:118–127, 2020.
- Edmonds, "Maximum matching and a polyhedron with 0,1-vertices", J. Res. NBS 69B,
  1965 (Crossref).
- Karlin, Klein y Oveis Gharan, STOC 2021, pp. 32–45 (arXiv 2007.01409: aleatorizado,
  $\varepsilon > 10^{-36}$).
- Karpinski, Lampis y Schmied, "New inapproximability bounds for TSP", JCSS
  81(8):1665–1677, 2015 (arXiv: 123/122).
- Khachiyan, "Polynomial algorithms in linear programming", USSR Comput. Math. and
  Math. Physics 20(1):53–72, 1980 (Crossref). No cito la nota de 1979 en Doklady
  porque no pude comprobarla.
- Hochbaum, SIAM J. Comput. 11(3):555–556, 1982 (Crossref).
- Nemhauser y Trotter, "Vertex packings: Structural properties and algorithms",
  Math. Programming 8:232–248, 1975 (Crossref).

## Decisiones que quiero confirmar

- El simplex va visible pero como caja negra (no es materia del curso). Alternativa:
  ocultarlo en un bloque `echo=false`; lo dejo visible para que el oráculo sea
  reproducible.
- No cito ninguna cota de inaproximabilidad para vertex cover, por no haberla
  comprobado en la fuente.
