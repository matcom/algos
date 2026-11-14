# Resumen de la Parte II {.unnumbered #resumen-parte-2}

Este capítulo cierra la Parte II. No trae material nuevo. Junta en pocas páginas lo que
los capítulos 6 a 15 contaron por separado, muestra las ideas que solo se ven
mirándolos juntos, y termina con ejercicios que mezclan capítulos, en el estilo de las
preguntas del examen final. Cada vez que algo se cita, se dice de qué capítulo y
sección sale, para que puedas volver a la demostración completa.

## 1. El mapa de la parte {#resumen-parte-2-1-el-mapa-de-la-parte}

La Parte I dio las herramientas para medir, demostrar y acotar. La Parte II las usó
sobre cinco técnicas de diseño, dos capítulos por técnica, salvo el azar, que abre y
cierra la segunda mitad.

| capítulo | técnica | problema trabajado | garantía demostrada |
|---|---|---|---|
| 6 | divide y vencerás | Karatsuba, selección | $\Theta(n^{\log_2 3})$; selección $O(n)$ en el peor caso |
| 7 | divide y vencerás | producto de polinomios | $\Theta(n \log n)$ operaciones sobre coeficientes |
| 8 | azar, Las Vegas | quicksort, quickselect, hashing | $2(n+1)H_n - 4n$ comparaciones esperadas; $O(n)$ esperado; cubeta de largo esperado $\le 1 + (n-1)/m$ |
| 9 | goloso | retraso máximo, caché | óptimo por intercambio y por transformación de planificaciones |
| 10 | goloso | matroides, Kruskal, tareas con plazos | óptimo para todo peso si y solo si hay matroide |
| 11 | programación dinámica | conjunto independiente en árboles, viajante | $O(n)$; $O(2^n n^2)$ |
| 12 | programación dinámica | árbol de búsqueda óptimo, subsecuencia común | $O(n^2)$ con Knuth; memoria $O(n + m)$ con Hirschberg |
| 13 | flujo | flujo máximo, emparejamiento bipartito | $O(V^2 E)$; $O(E \sqrt V)$ en redes unitarias |
| 14 | flujo | flujo máximo con preflujos | $O(V^2 E)$, $O(V^3)$ con FIFO, $O(V^2 \sqrt E)$ con mayor etiqueta |
| 15 | azar, Monte Carlo | verificar un producto, corte mínimo global | error $\le 1/2$ por ronda; $\ge 2/(n(n-1))$ de acierto por corrida |

Cada capítulo recorrió el mismo ciclo del capítulo 2: un problema, un algoritmo, su
correctitud, su costo y, cuando se pudo, qué tan lejos está de lo mejor posible. Y cada
uno plantó un error en una variante que parecía correcta. La §4 los pone juntos.

## 2. Lo que hay que llevarse de cada capítulo {#resumen-parte-2-2-lo-que-hay-que-llevarse-de-cada-capitulo}

Cada capítulo tiene su resumen al final. Aquí va una sola idea por capítulo: la que los
demás usan.

**Capítulo 6. El costo de un divide y vencerás lo decide cómo cambia el trabajo de un
nivel al siguiente.** Si decrece geométricamente manda la raíz, si crece mandan las
hojas, y si se queda igual se multiplica por la altura. El Teorema Maestro es esa regla
cuando la razón es fija; el árbol de recursión la aplica también cuando no lo es, como
en la selección, con dos hijos de tamaños $n/5$ y $7n/10$. La selección es lineal
porque $\frac15 + \frac{7}{10} < 1$, y ese décimo que sobra paga las constantes en la
sustitución (§10).

**Capítulo 7. Si una operación es cara en una representación, busca otra donde sea
barata.** En valores, multiplicar polinomios cuesta una operación por punto; el cambio
de representación costaba $n^2$ con puntos cualesquiera y cuesta $n \log n$ en las
raíces de la unidad, porque el lema de la mitad hace que las parejas $x, -x$ se repitan
en cada nivel. El costo es en operaciones sobre coeficientes: con `float` el error de
redondeo llega a dar el entero equivocado (§10), y la NTT en $\mathbb Z_p$ calcula cada
coeficiente del producto módulo $p$ sin error, así que da el número exacto mientras los
coeficientes del **producto** sean menores que $p$: con factores de $n$ coeficientes en
$[0, B)$ basta $nB^2 \le p$ (§11).

**Capítulo 8. Una garantía esperada vale para toda entrada mientras el azar lo ponga
el algoritmo y el adversario no lo vea.** Se calcula escribiendo el costo como suma de
indicadoras y sumando probabilidades, sin pedir independencia. Quicksort aleatorio,
quickselect y el hashing universal son tres veces el mismo método con eventos
distintos: "estos dos se comparan", "esta vuelta tiene un pivote central", "estas dos
claves chocan" (§12).

**Capítulo 9. Un goloso se demuestra con una medida que decrece mientras un óptimo se
transforma en la solución del goloso sin empeorar.** En el retraso máximo la medida
son las inversiones y el paso cambia dos tareas vecinas; en la caché es el prefijo en
que el óptimo coincide con Belady, y el paso reconstruye una planificación entera.
Cada hipótesis que el paso usa es algo que la implementación no puede cambiar.

**Capítulo 10. Antes de inventar un intercambio, pregunta si hay un matroide.** El
teorema de Rado-Edmonds dice que el goloso es óptimo para toda función de peso no
negativa si y solo si el sistema de independencia cumple el intercambio (I3). Si lo
cumple, el algoritmo es ordenar y consultar un oráculo que responda la independencia
exactamente. Si no, el Teorema 2 construye los pesos que lo rompen, y la pregunta pasa
a ser cuántos matroides hacen falta: con dos está el emparejamiento bipartito.

**Capítulo 11. El estado es lo que una parte de la solución le tiene que contar al
resto, y nada más.** Si cuenta menos, la recurrencia es falsa (el camino simple más
largo con el estado "extremos"); si cuenta más, la tabla crece sin necesidad (el orden
completo del recorrido en el viajante). En un árbol cada subárbol cuenta dos números,
con y sin su raíz; en Held-Karp el estado $(S, j)$ olvida el orden en que se visitó
$S$.

**Capítulo 12. Una optimización de programación dinámica es un teorema sobre la
recurrencia, y su hipótesis es la lista de lo que el problema tiene que cumplir.**
Knuth pide que lo que se suma no dependa del corte, cumpla la desigualdad del
cuadrilátero y sea monótono por inclusión; entonces la raíz óptima es monótona y
recorrer solo la franja cuesta $O(n^2)$. Hirschberg pide que el valor de un camino sea
la suma de sus dos mitades, y con eso recupera la subsecuencia común en memoria
$O(n + m)$.

**Capítulo 13. Una cota de costo que sale de un invariante se comprueba con el
invariante, no con la salida.** Max-Flow Min-Cut da a la vez la correctitud de todo
algoritmo que aumente hasta que no haya camino y un certificado: el corte de los
alcanzables desde $s$. Dinic es rápido porque la distancia de $s$ a $t$ sube en cada
fase (Lema 3), y en redes unitarias eso da menos de $2\sqrt V + 1$ fases.

**Capítulo 14. La demostración no dice qué hacer: dice qué se puede tocar.** Push-relabel
mantiene el invariante $h(u) \le h(v) + 1$ en las aristas residuales, con
$h(s) = V$, y las cotas solo usan además que las alturas nunca bajan. Una heurística
que respeta las dos cosas, como el relabel global y el gap, hereda la correctitud y las
cuentas de operaciones; una que cambia la inicialización no hereda nada (§12).

**Capítulo 15. En un algoritmo Monte Carlo la probabilidad de error es parte de la
garantía, igual que el $O(\cdot)$.** Se demuestra para toda entrada, se baja repitiendo,
y la repetición solo funciona con monedas nuevas. Con error de un lado las corridas se
combinan sin introducir errores nuevos: "no" si alguna dice "no" en Freivalds, el menor
corte en Karger.

## 3. Cada técnica tiene su demostración

Lo que distingue a una técnica de otra no es tanto la forma del código como la forma de
la demostración que la acompaña. Esta tabla es una guía para saber qué escribir cuando
un ejercicio dice "demuestra":

| técnica | qué se demuestra | la herramienta |
|---|---|---|
| divide y vencerás | el costo | recurrencia: árbol de recursión, luego sustitución con las constantes |
| Las Vegas | el costo esperado para toda entrada | suma de indicadoras y linealidad de la esperanza |
| goloso | la optimalidad | intercambio con una medida que decrece, o un matroide |
| programación dinámica | la recurrencia | principio de optimalidad del estado elegido, cota en las dos direcciones |
| optimización de DP | que la franja contiene una raíz óptima, y el costo | desigualdad del cuadrilátero, monotonía, suma telescópica |
| flujo | correctitud y número de fases u operaciones | Max-Flow Min-Cut, invariante, potencial |
| Monte Carlo | la probabilidad de error para toda entrada | decisiones diferidas, producto de probabilidades condicionales |

Tres herramientas de la Parte I reaparecen sin cambiar de forma.

**El potencial del capítulo 4.** Push-relabel cuenta los empujes no saturantes con
$\Phi = \sum_{\text{activo}} h(v)$ (capítulo 14, §8). En una fase de Dinic, los
pasos que no llegan a $t$ se pagan con un puntero por vértice que nunca retrocede, y
los que llegan, con las aristas que cada aumento satura: $O(VE)$ por fase (capítulo 13,
§11). Y el union-find del capítulo 4 es el oráculo de Kruskal (capítulo 10, §7) y el
que recorre las aristas barajadas en Karger (capítulo 15, §9).

**El adversario del capítulo 5.** Ninguna regla de caché en línea que no use azar
garantiza menos de $k$ veces los fallos de Belady: el adversario pide siempre un
elemento que la regla no tiene (capítulo 9, §11). Si el universo tiene más de $(n-1)m$
claves, toda función de hash fija con $m$ cubetas tiene $n$ claves que caen en una
misma cubeta (capítulo 8, §10). Y el Teorema 2 del capítulo 10
fabrica, a partir de un par $A, B$ donde falla el intercambio, los pesos que hacen
fallar al goloso. En los tres casos se construye la entrada mala desde la regla.

**El invariante del capítulo 3.** El de push-relabel es una desigualdad sobre las
alturas; el de Dinic, que la distancia de $s$ a $t$ sube; el de la FFT iterativa, qué
contiene cada bloque después de cada pasada (capítulo 7, ejercicio 9). Y la correctitud
de cada programación dinámica es una inducción sobre el orden en que se llena la tabla.

## 4. Ideas que solo se ven juntando capítulos

### El mismo problema con dos técnicas

Varios problemas aparecieron dos veces, resueltos de maneras distintas, y la
comparación dice más que cada solución por separado.

- **Seleccionar.** La mediana de las medianas (capítulo 6, §9) da $O(n)$ en el peor
  caso. Quickselect (capítulo 8, §8) da $O(n)$ esperado, a lo sumo $8n$ comparaciones
  por el argumento de fases, con diez líneas de código. Lo medido no pasó de 3,29
  comparaciones por elemento. La que conviene depende de si se puede tolerar una
  corrida mala con probabilidad pequeña.
- **Multiplicar.** Karatsuba (capítulo 6) baja el exponente partiendo en mitades; la
  FFT (capítulo 7) cambia de representación. Las dos cuentan operaciones sobre
  coeficientes o dígitos chicos. Para enteros medidos en bits, el resultado es otro
  teorema: Schönhage y Strassen (1971) dan $O(b \log b \log \log b)$ y Harvey y
  van der Hoeven (*Annals of Mathematics*, 2021) dan $O(b \log b)$ (capítulo 7, §12).
  Y el capítulo 15 muestra que **comprobar** un producto de matrices cuesta $3n^2$
  multiplicaciones con Freivalds, menos que calcularlo con el algoritmo escolar.
- **Cortar.** El corte mínimo $s$-$t$ se lee de la residual final de cualquier flujo
  máximo (capítulo 13, §6). El corte mínimo global sale de $n - 1$ flujos máximos desde
  un vértice de grado mínimo, en $O(m^2)$ con Ford-Fulkerson, o de Karger, que no
  fija $s$ ni $t$ (capítulo 15, §8 a §11).
- **Emparejar.** El capítulo 10, §10, ve los emparejamientos bipartitos como la
  intersección de dos matroides de partición: el goloso pierde, y garantiza solo la
  mitad (capítulo 10, ejercicio 10). El capítulo 13, §12, los resuelve exactos como un
  flujo máximo en una red unitaria, en $O(E \sqrt V)$ (Hopcroft-Karp).
- **Flujo máximo.** Dinic y push-relabel llegan a la misma cota $O(V^2 E)$ desde
  lados opuestos. Dinic mantiene siempre un flujo válido y trabaja hasta que no queda
  camino de aumento. Push-relabel mantiene desde el principio que no hay camino de
  aumento, porque $h(s) = V$ y un camino simple baja a lo sumo $V - 1$, y trabaja hasta
  que el preflujo es un flujo.

Una coincidencia más, que no se ve en un solo capítulo: Karger con las aristas
barajadas una vez y recorridas con union-find (capítulo 15, §9) hace el mismo recorrido
que Kruskal (capítulo 10, §7) con un orden al azar, y se detiene cuando quedan dos
componentes.

### Las técnicas se anidan

Las técnicas no viven separadas. Hirschberg (capítulo 12, §9) es un divide y vencerás
dentro de una programación dinámica: parte en la fila media y resuelve las dos mitades,
y su costo se suma por niveles como en el capítulo 6. El algoritmo aleatorio del par
más cercano (capítulo 2, §9) tiene dos monedas, la permutación y la función de hash de
la rejilla, y su análisis pide que se elijan independientes (capítulo 8, §12).
Karger-Stein (capítulo 15, ejercicio 5) es una recurrencia del capítulo 6 sobre un
algoritmo Monte Carlo. Kruskal es un goloso con una estructura amortizada adentro. Una
técnica de diseño es una manera de pensar el problema, y un algoritmo real suele usar
varias.

### El error plantado rompe la respuesta o rompe la garantía

En los capítulos 1, 2, 3 y 5 el error plantado daba una respuesta equivocada, y en el 4
subir a la raíz rompía una cota de costo. En la Parte II los dos tipos se reparten:
seis variantes responden mal, y en cuatro la respuesta es buena y lo que se pierde es la
garantía, de costo o de probabilidad. La tabla junta los diez.

| capítulo | variante | qué rompe | qué vieron las pruebas | qué lo anunciaba |
|---|---|---|---|---|
| 6, §11 | grupos de 3 | la cota $O(n)$ | 3 000 instancias correctas; la recurrencia da $T(n)/n = 19{,}37$ en $n = 10^7$ y sigue subiendo | $\frac15 + \frac{7}{10} < 1$ |
| 7, §8 | rellenar hasta $N \ge d$ | la respuesta | ninguna falla con largos iguales potencia de dos desde 4; 0,20 % con largos al azar hasta 1000 | $d + 1$ puntos determinan el polinomio |
| 8, §6 | partir en dos con los iguales a un lado | el costo esperado | 500 permutaciones correctas; con $n = 2000$ claves iguales, $1\,999\,000 = n(n-1)/2$ comparaciones | "claves distintas" |
| 9, §10 | Belady con ventana | la optimalidad | 0 de 400 con 12 pedidos, 1 de 400 con 200; nunca peor que LRU | "$f$ no se pide antes que $e$" |
| 10, §9 | comprobar solo en su plazo | la respuesta | 226 de 2000 al azar; 0 con plazos distintos o con las urgentes más caras | "$N_t$ sube en 1 para todo $t \ge d_x$" |
| 11, §5 | si no tomo $v$, tomo a sus hijos | la respuesta | 0 en estrellas y en caminos sin pesos; 28 de 100 en árboles al azar con pesos | "contiene o no contiene a $c_i$" |
| 12, §7 | Knuth en la cadena de matrices | la respuesta | 0 de 1000 con matrices cuadradas o con 3 matrices; 223 de 1000 con 4 al azar | $w(i, j)$ no depende del corte |
| 13, §10 | avanzar el puntero tras un empuje parcial | la cota de fases | valor correcto en las 1000 redes; la distancia no crece en 280; 256 fases con $k = 16$ | la palabra "bloqueante" |
| 14, §5 | $h(s) = d(s, t)$ | la respuesta | 3 de 1000 redes chicas, 0 de 1000 en capas, 110 de 1000 medianas | "cualquier camino residual simple" |
| 15, §6 | la misma moneda en las $k$ rondas | la probabilidad de error | con una entrada mala pasan 10 rondas el 48 % de las veces, contra el 0,07 % con monedas nuevas; con muchas entradas malas, ninguna pasa la primera ronda | "independientes" |

Las seis variantes que dan una respuesta equivocada tienen la forma que ya conocías: pasan
las pruebas que uno escribe primero y fallan en entradas con una estructura que la
demostración nombra. Las cuatro restantes son peores, porque comparar cada
respuesta con la correcta no las atrapa. En los capítulos 6, 8 y 13 todas las respuestas
son correctas. En el 15 una respuesta equivocada no acusa a la variante, porque el
Freivalds bueno también se equivoca a veces: hay que medir con qué frecuencia. El
capítulo 6 lo dice para el peor caso: las pruebas miden las entradas que
alguien eligió, y el peor caso es la que nadie eligió. El capítulo 8 lo dice para el
costo esperado: una batería de permutaciones no tiene claves repetidas. El capítulo 13
lo convirtió en regla: una cota que sale de un invariante se comprueba vigilando el
invariante, con un `assert` sobre la sucesión de distancias. Y el capítulo 15 muestra
que la garantía de un Monte Carlo es un número, la probabilidad de error, que solo se
ve midiendo en la entrada donde la cota se alcanza: una sola entrada mala.

De ahí sale una manera de leer cualquier demostración de la parte: subraya cada
hipótesis que usa ("distintos", "independientes", "bloqueante", "no depende del corte")
y pregúntate qué entrada o qué cambio del código la viola. Esa es la lista de pruebas
que hay que escribir, y también la lista de lo que no se puede optimizar sin volver a
demostrar.

### Una garantía viene con su modelo y con su fuente de azar

La Parte I terminó con la idea de que toda cota viene con un modelo. La Parte II la
repitió, y le agregó una segunda pregunta: quién pone el azar.

- **El modelo.** La FFT multiplica polinomios en $\Theta(n \log n)$ **operaciones
  sobre coeficientes**; con `float` de 53 bits esas operaciones dejan de ser exactas
  (capítulo 7, §10), y para enteros en el modelo por bit la cota es otra. Freivalds
  cuenta multiplicaciones, no bits. Held-Karp cuesta $O(2^n n^2)$ en tiempo y $O(2^n n)$ en
  memoria (capítulo 11, §10): la tabla también es parte del costo.
- **Quién pone el azar.** El capítulo 8, §7, separó tres garantías que se parecen:
  el caso promedio (la entrada viene al azar), el costo esperado (las monedas son del
  algoritmo) y el costo amortizado (sin azar, para toda secuencia, el del capítulo 4).
  Quicksort con el primer pivote sobre una permutación uniforme hace en promedio las
  mismas $2(n+1)H_n - 4n$ comparaciones que quicksort aleatorio, y la garantía no es
  la misma: un adversario que manda la lista ordenada rompe la primera y no la segunda.
- **Si el adversario ve las monedas, no hay garantía.** La cota de LRU es para reglas
  sin azar porque el adversario tiene que saber qué pedir (capítulo 9, §11). La familia
  universal funciona porque la función se elige al azar después de recibir las claves
  (capítulo 8, §10 y §11). La repetición de Freivalds funciona solo con monedas nuevas
  (capítulo 15, §6).
- **Esperado o con error.** Las Vegas fija la respuesta y deja variar el tiempo; Monte
  Carlo fija el tiempo y deja variar la respuesta. Markov convierte lo primero en lo
  segundo cortando a tiempo $2T$ (capítulo 8, ejercicio 7). Lo segundo se convierte en
  lo primero solo si una respuesta se puede comprobar barato, y Freivalds muestra por
  qué no siempre se puede: un "no" trae un testigo y un "sí" no trae nada (capítulo 15,
  §7).

### Una cota superior no es el valor

Varias veces la parte comparó lo demostrado con lo medido, y la distancia fue grande:

- Quickselect: la cota es $8n$ y lo medido no pasó de 3,29 por elemento (capítulo 8,
  §9). El ejercicio 3 del capítulo 8 baja la cota a $4n$, y tampoco esa es el valor.
- La mediana de las medianas: el árbol da $10an$, la sustitución $20an$, y la
  recurrencia evaluada no pasó de 8,66 por elemento hasta $n = 10^7$ (capítulo 6, §10).
- Push-relabel en el embudo: sin heurísticas, mayor etiqueta hace unas $1{,}5\,V^2$
  operaciones; con relabel global y gap, entre 8 y 15 por vértice, muy lejos de
  $O(V^2 \sqrt E)$ (capítulo 14, §11).
- Hopcroft-Karp: la familia de escaleras hace $k$ fases con $V = k^2 + k + 2$, cerca de
  $\sqrt V$, así que la cota de fases se alcanza salvo un factor 2 (capítulo 13, §12).
  Aquí la cota sí es ajustada, y hubo que construir la entrada para verlo.

Una cota superior que no se alcanza en lo medido no es una cota falsa: es una garantía
para toda entrada, incluidas las que no mediste. Y una cota superior que deja de valer
no es una cota mínima: con grupos de 3, la demostración ya no da $O(n)$, pero eso no
dice que haya entradas donde la selección tarde $\Theta(n \log n)$ (capítulo 6, §11).
Para afirmar que una cota es ajustada, o que una variante pierde de verdad, hace falta
una familia de entradas: las escaleras de Hopcroft-Karp para lo primero, y la familia
de $k^2$ fases del puntero de Dinic para lo segundo (capítulo 13, §10), que con
$k = 16$ hace 256 fases en una red de 35 vértices, más que las $V - 1$ de la cota.

## 5. Ante un problema nuevo

Las reglas de los diez capítulos se pueden leer como una lista de preguntas para
escoger técnica. No es un algoritmo para diseñar algoritmos, pero ordena el trabajo.

1. ¿Se parte en pedazos del mismo tipo que se combinan barato? Escribe la recurrencia
   y mira cómo cambia el trabajo por nivel (capítulo 6). Si combinar es caro, busca
   una representación donde no lo sea (capítulo 7).
2. ¿Hay una decisión local que nunca hace falta deshacer? Busca la medida del
   intercambio (capítulo 9) o, mejor, el matroide (capítulo 10). Si los conjuntos
   factibles no cumplen (I3), el Teorema 2 dice que hay pesos que rompen al goloso.
3. ¿Hace falta deshacer decisiones? Si el resto del problema solo necesita saber poco
   de lo ya decidido, ese poco es el estado de una programación dinámica (capítulo 11).
   Si la recurrencia es correcta pero cara, mira si cumple las hipótesis de Knuth o de
   Hirschberg (capítulo 12).
4. ¿Se puede ver como mandar algo por una red con capacidades? Entonces Max-Flow
   Min-Cut da a la vez el algoritmo y el certificado (capítulos 13 y 14).
5. ¿Hay un adversario que conoce el algoritmo y escoge la peor entrada? El azar del
   algoritmo le quita esa ventaja (capítulo 8). ¿Basta con acertar con alta
   probabilidad? Un Monte Carlo con error de un lado se amplifica repitiendo
   (capítulo 15).

Y una vez escogida, la forma de la respuesta es la de la Parte I: enunciado con su modelo,
algoritmo, correctitud con la demostración propia de la técnica, costo, y una cota
mínima o una familia de entradas que muestre que el análisis es ajustado.

## Ejercicios {#resumen-parte-2-ejercicios}

Cada ejercicio dice entre paréntesis qué capítulos usa. Ninguno pide material que no
esté en el libro hasta el capítulo 15, o en Estructuras de Datos. No llevan solución:
las soluciones bien presentadas cuentan para la evaluación.

1. **[traza]** (capítulos 7 y 15) Alguien afirma que
   $$(1 + 2x + 3x^2)(4 + 5x) = 6 + 10x + 23x^2 + 15x^3.$$
   (a) Comprueba la afirmación
   como en el capítulo 15: evalúa los dos lados en $r = 4$ en $\mathbb Z_{17}$.
   (b) Encuentra todos los $r \in \mathbb Z_{17}$ para los que la comprobación dice
   "sí", y compara esa fracción con la cota $d/p$ del capítulo 7, §13. (c) Da un
   polinomio de grado 3, distinto del producto también en $\mathbb Z_{17}$, que pase
   la comprobación con la mayor probabilidad posible. ¿Alcanza la cota? ¿Qué
   afirmaciones falsas sobre los enteros no ve nunca la comprobación módulo 17? (d) ¿Cuántas rondas independientes hacen
   falta, según la cota, para que el error baje de $10^{-6}$? ¿Y si las rondas usan
   todas el mismo $r$?

2. **[entrada que rompe]** (capítulos 9 y 12) Para el árbol binario de búsqueda óptimo
   del capítulo 12, §2, se proponen dos golosos que eligen la raíz y siguen por
   recursión en cada lado: (i) la clave más buscada; (ii) la clave que deja más liviano
   el más pesado de sus dos subárboles. (a) Para cada regla, encuentra frecuencias distintas
   entre sí, y sin empates en la regla (ii), donde no da el óptimo, y calcula los dos costos con la recurrencia de la §2.
   (b) Intenta para la regla (i) un argumento de intercambio como el del capítulo 9,
   §5: intercambiar en un árbol óptimo la raíz con la clave más buscada. ¿Qué paso no
   se puede escribir?

3. **[demostración]** (capítulos 8, 13 y 15) Un algoritmo Monte Carlo $M$ corre en
   tiempo $T$ y devuelve un objeto (un corte, un producto, una asignación), que es
   correcto con probabilidad al menos $p > 0$ para toda entrada. Un verificador
   determinista decide en tiempo $T'$ si un objeto es correcto. (a) Construye con los
   dos un algoritmo Las Vegas y demuestra que su tiempo esperado es a lo sumo
   $(T + T')/p$ para toda entrada. ¿Qué tienen que cumplir las corridas de $M$?
   (b) ¿Por qué no se puede aplicar a Freivalds? (c) Aplícalo a la contracción de
   Karger con el verificador "calcula el corte mínimo global con $n - 1$ flujos
   máximos y compara" del capítulo 15, §8. ¿Cuánto cuesta, y por qué no tiene sentido?
   (d) El ejercicio 7 del capítulo 8 va en la otra dirección. Si aplicas (a) al
   algoritmo que construye ese ejercicio, ¿qué obtienes?

4. **[demostración]** (capítulos 9, 10 y 11) Hay $n$ intervalos $[s_i, f_i)$, y llamamos
   independiente a un conjunto de intervalos que no se solapan dos a dos. (a) Demuestra
   que es un sistema de independencia y que no es un matroide. (b) El ejercicio 6 del
   capítulo 9 demuestra que tomar el que termina primero da la mayor cantidad de
   intervalos. ¿Por qué eso no contradice el Teorema 2 del capítulo 10? (c) Ahora cada
   intervalo tiene un peso $w_i \ge 0$. Da una instancia donde el goloso por peso
   falla y otra donde falla el que termina primero. (d) Resuelve el caso con pesos con
   una programación dinámica: di el estado, la recurrencia, demuestra el principio de
   optimalidad para ese estado como en el capítulo 11, §4, y da el costo.

5. **[demostración]** (capítulos 10 y 13) Sea $M$ el emparejamiento que tiene Dinic
   sobre la red bipartita del capítulo 13, §12, después de algunas fases, y $M^*$ uno
   máximo. (a) Demuestra que después de la primera fase $M$ es maximal: ninguna arista
   del grafo tiene sus dos extremos libres. ¿Qué fracción de $|M^*|$ garantiza eso? Compáralo con
   lo que garantiza el goloso del capítulo 10, §10, y su ejercicio 10. (b) Sea $j$ el número de aristas de $M$ en un camino de aumento más corto.
   Demuestra que $|M| \ge \frac{j}{j+1} |M^*|$, con los Lemas 5 y 6 y la descomposición
   en caminos de la §12. (c) Usa el Lema 3 del capítulo 13 y la paridad de las
   distancias en la red bipartita para decir qué fracción de $|M^*|$ garantiza Dinic
   si se detiene después de $p$ fases.

6. **[cambio de hipótesis]** (capítulos 9 y 10) En las tareas con plazos del capítulo 10,
   §8, todas duran 1. Ahora la tarea $i$ dura $t_i \ge 1$ y tiene plazo $d_i$, y un
   conjunto es factible si sus tareas se pueden hacer una tras otra terminando cada una
   a tiempo. (a) Con el teorema del retraso máximo del capítulo 9, da un oráculo de
   costo $O(n \log n)$ que decida si un conjunto es factible. (b) Demuestra que los
   conjuntos factibles ya no forman un matroide, con una instancia de tres tareas.
   (c) Construye con el Teorema 2 del capítulo 10 los pesos que hacen fallar al goloso
   en tu instancia, y comprueba que falla. (d) Si todas las tareas duran lo mismo,
   $t_i = t$, ¿se recupera el matroide? Demuéstralo o da un contraejemplo.

7. **[entrada que rompe]** (capítulos 10 y 11) Para el conjunto independiente de peso
   máximo en un árbol se propone el goloso "toma el vértice de mayor peso, borra a sus
   vecinos y repite". (a) En un camino de tres vértices, encuentra los conjuntos $A$ y
   $B$ donde falla (I3), construye los pesos del Teorema 2 del capítulo 10, y compara
   lo que da el goloso con lo que da la recurrencia del capítulo 11, §3. (b) Construye
   una familia de árboles donde el goloso obtiene una fracción del óptimo tan chica como
   se quiera. (c) Las estrellas no atraparon el error plantado del capítulo 11, §5.
   ¿Atrapan a este goloso? ¿Por qué la respuesta es distinta?

8. **[implementar y medir]** (capítulos 13 y 14) Corre Dinic (capítulo 13, §8) y
   push-relabel FIFO con relabel global y gap (capítulo 14, §9 y §11) sobre tres
   familias: las escaleras bipartitas del capítulo 13, §12, el embudo del capítulo 14,
   §11, y redes en capas al azar. Cuenta fases y aristas examinadas en Dinic, y empujes
   y subidas de altura en push-relabel, para al menos cinco tamaños por familia. Para
   cada familia y cada algoritmo, di cuál de las cotas $O(E \sqrt V)$, $O(V^2 E)$ y
   $O(V^3)$ se aplica y qué tan cerca queda lo medido. Informa los tiempos también, y
   explica por qué los conteos son más fiables que los segundos para comparar con las
   cotas.

9. **[implementar y medir]** (capítulos 6 y 8) (a) Corre quickselect 10 000 veces sobre
   una misma entrada de $n = 10^5$ elementos distintos buscando la mediana, y dibuja la
   distribución del número de comparaciones dividido entre $n$. Compara la fracción de
   corridas que pasan de $t$ veces la media con lo que permite Markov (capítulo 8, §7),
   para varios $t$. (b) Diseña un híbrido: quickselect que, si ya gastó $4n$
   comparaciones, sigue con la mediana de las medianas del capítulo 6 sobre el pedazo
   que le queda. Demuestra que su peor caso es $O(n)$ y su costo esperado también.
   (c) Mide el híbrido y los dos algoritmos originales con entradas al azar, ordenadas
   y con todas las claves iguales. ¿Qué hipótesis del capítulo 8 hace falta revisar en
   el último caso?

10. **[modelar] ★** (capítulos 10 y 13) Hay $n$ tareas de duración 1, la tarea $i$ con
    plazo $d_i$ y penalización $w_i$, y ahora hay $m$ máquinas iguales. (a) Modela la
    factibilidad de un conjunto como un emparejamiento bipartito entre tareas y turnos
    $(\text{máquina}, \text{instante})$. (b) Generaliza el Lema 3 del capítulo 10:
    demuestra que $S$ es factible si y solo si $N_t(S) \le m\,t$ para todo $t$. Para la
    dirección difícil, usa Max-Flow Min-Cut del capítulo 13 sobre la red de (a).
    (c) Demuestra que los conjuntos factibles forman un matroide. (d) Da el algoritmo
    que minimiza la penalización total y su costo, con dos oráculos: el conteo de (b) y
    Hopcroft-Karp sobre la red de (a). Da el costo de cada uno por consulta y en
    total. ¿Cuál conviene?
