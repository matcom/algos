# Envolvente convexa en el plano: el ciclo completo

## Sección 1: Problema escogido

**Envolvente convexa (convex hull) de $n$ puntos en el plano, con salida ordenada.**

No lo vimos en la conferencia. Está en $\Theta(n\log n)$ en un modelo preciso, y la cota mínima se demuestra completa, sin citar ningún teorema externo. Esto último se debe a una convención de salida que explico en la sección 2.

---

## Sección 2: Explicación y convenciones

**Enunciado.** Dada una lista $(p_1,\dots,p_n)$ de puntos de $\mathbb{R}^2$, devolver los vértices de la envolvente convexa $\mathrm{conv}(P)$ en orden antihorario.

**Convenciones (las que casi nunca se dan):**

1. **Puntos distintos.** $P$ es un conjunto. Si fuera una lista con repetidos, se eliminan tras ordenar (adyacentes iguales) con coste $O(n)$ extra.
2. **Vértice** = punto extremo de $\mathrm{conv}(P)$, es decir, $p\notin\mathrm{conv}(P\setminus\{p\})$. Los puntos colineales sobre una arista **no** son vértices.
3. **Salida.** La lista de **índices** de los vértices en orden antihorario, empezando por el menor en orden lexicográfico $(x,y)$. A diferencia del par más cercano, la respuesta es única, así que no hay empates.
4. **Casos raros.** Con $n=1$ se devuelve ese punto. Con todos colineales se devuelven los dos extremos (la envolvente es un segmento).
5. **Predicado de orientación.**
$$o(a,b,c)=(b_x-a_x)(c_y-a_y)-(b_y-a_y)(c_x-a_x).$$
Es positivo si $a\to b\to c$ gira a la izquierda, cero si son colineales y negativo si gira a la derecha. Es un polinomio de grado 2, igual que comparar distancias al cuadrado en la conferencia.
6. **Modelo de cómputo.** Árbol de decisión algebraico: cada nodo prueba el signo de un polinomio de la entrada, ramifica en $\le 3$ y el costo es la profundidad. Todo lo que hará el algoritmo (comparar coordenadas y evaluar $o$) cabe en este modelo.

**Problema parecido que no es este.** Pedir solo el *conjunto* de vértices sin orden es otro problema. La cota sigue siendo $\Omega(n\log n)$, pero su demostración necesita herramientas tipo Ben-Or. La salida ordenada por índices hace que la cota se pruebe por conteo (sección 5). Hay que fijar esto en el enunciado.

---

## Sección 3: Algoritmo y correctitud

### 3.1 Algoritmo (cadena monótona de Andrew)

```
hull(P):
  ordenar P lexicográficamente: p1 < p2 < ... < pn
  si n = 1: devolver [p1]
  L ← cadena(p1, ..., pn)        # inferior, izquierda → derecha
  U ← cadena(pn, ..., p1)        # superior, derecha → izquierda
  devolver L sin su último punto ++ U sin su último punto

cadena(q1, ..., qm):
  S ← []
  para i = 1..m:
     mientras |S| ≥ 2 y o(S[-2], S[-1], qi) ≤ 0: sacar de S
     meter qi en S
  devolver S
```

### 3.2 Reducción sin pérdida de generalidad: x distintas

Sea $T_\varepsilon(x,y)=(x+\varepsilon y,\,y)$. Su determinante es 1, así que preserva el signo de $o$, el orden antihorario y los puntos extremos. Para $\varepsilon>0$ suficientemente pequeño, el orden por la nueva abscisa coincide con el lexicográfico, y las abscisas resultan todas distintas. El algoritmo ejecuta exactamente las mismas operaciones sobre $P$ y sobre $T_\varepsilon(P)$ (mismo orden, mismos signos de $o$). Basta entonces probar la correctitud suponiendo $x_1<\dots<x_n$. La cizalla es solo un recurso de análisis y no se ejecuta.

### 3.3 Lemas

**Lema 1.** Si $x_a<x_b<x_c$, entonces $o(a,b,c)=(x_b-x_a)(x_c-x_a)\,(m_{ac}-m_{ab})$, donde $m$ es la pendiente. Por tanto $o>0\iff b$ está **estrictamente debajo** del segmento $ac$, y $o\le0\iff b$ está sobre la recta $ac$ o por encima.

*Demostración.* Se factoriza el determinante dividiendo y multiplicando por $(x_b-x_a)(x_c-x_a)>0$. $\square$

**Cadena estrictamente convexa:** una sucesión $s_1,\dots,s_m$ con $x$ creciente tal que cada $s_j$ interior queda estrictamente debajo de $s_{j-1}s_{j+1}$. Por el Lema 1 equivale a $o(s_{j-1},s_j,s_{j+1})>0$ para todo $j$. Su gráfica $g$ es la de una función convexa lineal a trozos.

**Hecho F.** Sea $Q$ un conjunto con abscisas distintas, y sea $s_1,\dots,s_m\in Q$ una cadena estrictamente convexa con $s_1$ y $s_m$ los puntos de menor y mayor $x$ de $Q$, y con $Q$ sobre o encima de $g$. Entonces $g$ es la frontera inferior de $\mathrm{conv}(Q)$, y los $s_j$ son exactamente los puntos extremos de $\mathrm{conv}(Q)$ sobre esa frontera.

*Demostración.* El epígrafo de $g$ es convexo y contiene a $Q$, luego contiene a $\mathrm{conv}(Q)$. Además $g\subset\mathrm{conv}(Q)$, porque son segmentos entre puntos de $Q$. Así la frontera inferior es $g$. Un punto en el interior de un tramo recto es punto medio de dos puntos de la envolvente, luego no es extremo. En una esquina estricta se toma una recta de apoyo con pendiente entre las dos pendientes adyacentes, y deja a todo $\mathrm{conv}(Q)$ estrictamente arriba salvo ese punto, luego es extremo. Los extremos $s_1,s_m$ quedan aislados por rectas verticales. $\square$

**Lema 2 (invariante de la cadena inferior).** Tras procesar $q_i$, la pila $S=(s_1,\dots,s_m)$ es una cadena estrictamente convexa con $s_1=q_1$, $s_m=q_i$, y $\{q_1..q_i\}$ queda sobre o encima de su gráfica. Por el Hecho F, $S$ son los vértices de la envolvente inferior de $\{q_1..q_i\}$.

*Demostración.* Por inducción sobre $i$. Para $i=1$ es trivial. Para el paso, sea $p=q_i$ y $S=(s_1..s_m)$ la pila previa, con $s_m=q_{i-1}$. El bucle saca elementos hasta quedar $(s_1..s_r)$, con $r=1$ o $o(s_{r-1},s_r,p)>0$. Se mete $p$ y la pila nueva es $S'=(s_1..s_r,p)$.

- **Estricta convexidad.** Las ternas internas de $s_1..s_r$ ya eran positivas, y $(s_{r-1},s_r,p)$ es positiva por la condición de parada.
- **Todo está encima de $g'$.** Hay tres casos.
  - Los puntos con $x\le x(s_r)$ estaban encima de $g$, y $g'=g$ ahí.
  - Los sacados $s_j$ ($j>r$) cumplen $o(s_{j-1},s_j,p)\le0$ en el instante en que se sacan. Entonces $s_j$ está sobre o encima de la recta $s_{j-1}p$. Por inducción sobre $j$ y como $s_{r+1}$ queda sobre o encima de la recta $s_rp$, también $s_{r+2}$, etc. (la recta $s_{j}p$ queda por encima de $s_rp$ a la izquierda de $p$). Así todos los $s_j$ ($j>r$) están sobre o encima de la recta $s_rp$.
  - La gráfica antigua $g$ sobre $[x(s_r),x(s_m)]$ une esos vértices, luego también está sobre o encima de $s_rp$. Los demás puntos de $\{q_1..q_{i-1}\}$ en ese rango estaban sobre o encima de $g$. No hay puntos con $x$ entre $x(s_m)$ y $x(p)$.

Esto cierra el paso. $\square$

### 3.4 Teorema de correctitud

*Cadena superior.* Una rotación de 180° preserva $o$, invierte el orden y convierte la envolvente superior en inferior. Recorrer $p_n,\dots,p_1$ equivale entonces a aplicar el Lema 2 a la nube rotada. La cadena $U$ son los extremos de la frontera superior, de derecha a izquierda.

*Conjunto de vértices.* La frontera de $\mathrm{conv}(P)$ es la unión de las fronteras inferior y superior, que comparten solo $p_1$ y $p_n$. Por el Hecho F, el conjunto de puntos extremos es $L\cup U$.

*Orden.* La inferior recorrida de izquierda a derecha y la superior de derecha a izquierda dan el sentido antihorario. La lista empieza en $p_1$, el menor lexicográfico. Quitar el último punto de cada cadena evita duplicar $p_n$ y $p_1$.

*Casos raros.* Con $n=2$ se devuelve $[p_1,p_2]$. Si todos son colineales, los intermedios se sacan porque $o=0\le0$, y quedan los dos extremos.

Luego el algoritmo devuelve exactamente la salida definida en la sección 2. $\blacksquare$

---

## Sección 4: ¿Cuánto cuesta?

**Teorema.** El algoritmo ejecuta a lo sumo $2n\lceil\log_2 n\rceil+4n$ pruebas de signo y usa memoria $O(n)$. En el modelo de árboles de decisión algebraicos tiene profundidad $O(n\log n)$.

*Demostración.*

- **Ordenar.** Con ordenamiento por mezcla bastan $\le n\lceil\log_2 n\rceil$ comparaciones. Cada comparación lexicográfica son a lo sumo 2 pruebas de signo de un polinomio de grado 1 ($x_a-x_b$ y, si da cero, $y_a-y_b$).
- **Cada cadena.** En cada iteración se mete exactamente un punto, así que hay $m=n$ inserciones. Cada extracción saca un punto previamente insertado, luego hay $\le n$ extracciones en total. En la iteración $i$ se hacen (extracciones de $i$) $+$ a lo sumo 1 pruebas de $o$: cada prueba que da $\le0$ provoca una extracción, y la última prueba, la que detiene el bucle, ocurre a lo sumo una vez por iteración. Sumando, las pruebas son $\le n+n=2n$ por cadena, es decir $\le 4n$ en las dos.
- **Total.** Sumando se obtiene la cota del enunciado. Cada prueba de $o$ son 7 operaciones aritméticas, constante.
- **Memoria.** El arreglo ordenado, las dos pilas y la salida suman $O(n)$. $\square$

**Comparación con alternativas** (para ubicar la mejora):

| Algoritmo | Costo | Observación |
|---|---|---|
| Fuerza bruta: $(i,j)$ es arista si todos los demás quedan a la izquierda | $O(n^3)$ | sirve de oráculo para probar el resto |
| Marcha de Jarvis | $O(nh)$ | con $h$ vértices en la envolvente, $\Theta(n^2)$ si $h=n$ |
| Cadena monótona | $\Theta(n\log n)$ | el de arriba |

Dos aclaraciones, igual que en la conferencia:

- Esto es el costo **del algoritmo**. Todavía no dice nada del problema.
- Con coordenadas enteras, $o$ se evalúa en aritmética exacta (con coordenadas de $b$ bits, los valores caben en $2b+3$ bits). El predicado es polinomial, así que no hay error de redondeo en las decisiones, a diferencia de $\sqrt{\cdot}$.

---

## Sección 5: ¿Se puede mejorar?

### 5.1 Cota mínima

**Teorema.** Todo árbol de decisión en el que cada nodo interno tenga a lo sumo 3 hijos (en particular, todo árbol algebraico) que resuelva la envolvente convexa de $n\ge3$ puntos tiene profundidad $\ge\log_3(n!)=\Omega(n\log n)$.

*Demostración.* Por reducción desde ordenamiento, combinada con conteo de hojas.

1. **Familia de entradas.** Para cada permutación $\sigma$ de $\{1,\dots,n\}$, sea $I_\sigma$ la entrada con $p_j=(\sigma(j),\sigma(j)^2)$. Son $n!$ entradas distintas, y la construcción cuesta $O(n)$ sin ninguna prueba de signo.
2. **Todos son vértices.** Tres puntos de una parábola nunca son colineales, y los puntos están en posición convexa. Todos los $p_j$ son vértices.
3. **La salida determina $\sigma$.** El menor lexicográfico es el de menor $\sigma$. Desde ahí, la parte inferior de la parábola se recorre de izquierda a derecha, que es el sentido antihorario, y se vuelve por la cuerda superior. La salida es entonces la lista de índices $j_1,\dots,j_n$ con $\sigma(j_1)<\dots<\sigma(j_n)$, es decir, la permutación que ordena $\sigma$. Entradas distintas dan salidas distintas.
4. **Conteo.** Cada hoja produce una única salida, así que $I_\sigma$ y $I_{\sigma'}$ ($\sigma\ne\sigma'$) no comparten hoja. El árbol tiene $\ge n!$ hojas, y uno de profundidad $h$ y ramificación $\le3$ tiene $\le3^h$. Entonces
$$h\ge\log_3 n!\ge\log_3\!\big((n/e)^n\big)=n\log_3 n-n\log_3 e=\Omega(n\log n).\qquad\blacksquare$$

El grado de los polinomios no interviene: el argumento vale para cualquier prueba con $\le3$ resultados. Esto es posible porque la salida tiene $n!$ valores posibles. En distinción de elementos solo hay 2 salidas y el conteo no sirve, por eso allí hacía falta Ben-Or.

### 5.2 Conclusión

La cota inferior $\Omega(n\log n)$ coincide con la superior $O(n\log n)$ de la sección 4, luego en árboles de decisión algebraicos el problema cuesta $\Theta(n\log n)$. El algoritmo es óptimo. La brecha de constantes es explícita, entre $\approx0{,}63\,n\log_2 n$ y $2n\log_2 n$, y no afecta al orden.

### 5.3 Qué deja fuera el modelo 

- **Modelos con direccionamiento indirecto.** La cota viene del ordenamiento, y en una word RAM se ordenan enteros polinomiales con radix sort en $O(n)$. Con coordenadas enteras de tamaño polinomial en $n$, y como la cadena monótona solo necesita ordenar y luego recorrer en tiempo lineal, el problema pasa a $O(n)$. No hay contradicción: son modelos distintos, igual que en la sección 10 de la conferencia.
- **El azar no rompe esta cota.** Un algoritmo aleatorizado es una distribución sobre árboles. Si siempre es correcto, cada árbol tiene $\ge n!$ hojas distintas, y por la desigualdad de Kraft la profundidad media sobre las hojas es $\ge\log_3 n!$, luego también su costo esperado. Si puede errar con probabilidad $\le1/3$, el principio de Yao da un árbol determinista correcto en una fracción $\ge2/3$ de las $n!$ entradas, luego $3^h\ge\frac23 n!$. Lo que rompió la cota en la conferencia fueron la parte entera y la tabla hash, no el azar.
- **Parametrizar por la salida.** La cota es de *peor caso en $n$*. En función de $n$ y del número de vértices $h$, el costo es $\Theta(n\log h)$ (Kirkpatrick–Seidel 1986 y Chan 1996, citados sin demostrar). Para $h=n$ vuelve a ser $n\log n$, consistente con nuestra familia, que tiene $h=n$.
- **Otras versiones.** Si la salida fuera solo el conjunto de vértices sin orden, la cota sigue valiendo, pero ya no se obtiene por conteo.

## Código

**`fig1_problema.png` (Sección 2).** A la izquierda está la entrada, 14 puntos del plano. A la derecha está la salida: los 6 vértices numerados en orden antihorario desde el menor lexicográfico, con la cadena inferior L en azul y la superior U en naranja. Hay un punto colineal sobre la arista inferior, marcado con una flecha, para ilustrar la convención de que los puntos sobre una arista no son vértices.

**`fig2_orientacion.png` (Sección 2, convenciones).** Muestra el predicado `o(a,b,c)` en sus tres casos con valores calculados: giro a la izquierda (`o = 2 > 0`), colineales (`o = 0`) y giro a la derecha (`o = −4 < 0`). Es la única prueba de signo que usa el algoritmo, y aquí se ve por qué `o ≤ 0` obliga a sacar el punto de la pila.

**`fig3_andrew.gif` (Sección 3, algoritmo).** Animación de 51 cuadros de la cadena monótona sobre 14 puntos aleatorios. La estrella verde es el punto que se procesa, la cruz roja es un punto que sale de la pila porque `o ≤ 0`, y el título de cada cuadro dice qué decisión se tomó. Primero se construye la cadena inferior, luego la superior, y el cuadro final rellena la envolvente.

**`fig4_invariante.png` (Sección 3, Lema 2).** Ilustra el paso clave de la demostración del invariante. A la izquierda hay una pila convexa `s1..s4` y llega `p`; a la derecha se sacan `s4` y `s3` hasta que `o(s1,s2,p) > 0`. Los puntos sacados quedan sobre o encima de la recta `s_r–p`, así que todo sigue por encima de la nueva cadena.

**`fig5_costo.png` (Sección 4, costo).** Cuenta las pruebas de signo reales de Andrew para `n` desde 2⁴ hasta 2¹⁵, divididas por `n log₂ n`. Las dibuja entre la cota superior demostrada (`2n⌈log₂n⌉ + 4n`) y la cota mínima `log₃(n!)`. El script comprueba con un `assert` que nunca se rebasa la cota superior; el cociente medido baja de ≈1,4 a ≈1,2.

**`fig6_tiempos.png` (Sección 4, comparación).** Tiempos reales en ejes logarítmicos de la fuerza bruta, Jarvis y la cadena monótona sobre puntos en posición convexa (donde `h = n`). Las pendientes medidas (≈3,03, ≈2,02 y ≈1,12) coinciden con los exponentes teóricos 3, 2 y casi 1.

**`fig7_cota_minima.png` (Sección 5, cota mínima).** A la izquierda está la reducción: la permutación `σ` se convierte en puntos de la parábola `(σ(j), σ(j)²)`. La salida de la envolvente, `[3,6,1,5,7,2,4]`, determina `σ`, y por eso entradas distintas exigen hojas distintas. A la derecha se ve el conteo `3^h ≥ n!`: la profundidad mínima `⌈log₃ n!⌉` crece como `n log₃ n − n log₃ e`.

Una advertencia sobre la figura 5: la línea punteada verde no es una cota demostrada para cada `n`, sino el límite al que tiende `log₃(n!)/(n log₂ n)`, que es `ln 2 / ln 3 ≈ 0,63`. La leyenda lo dice así, para que no se confunda en el examen.