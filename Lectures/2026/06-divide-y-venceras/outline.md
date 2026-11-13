# Outline: Conferencia 6, divide y vencerás y recurrencias

Estado: redactado en formato de libro (2026-11-13), pendiente de revisión.
Las notas están en `notas.md`. En el PDF las figuras quedaron numeradas en el orden en
que aparecen: 1 árbol de Karatsuba, 2 tiempos, 3 grupos de 5, 4 cotas por tamaño de
grupo, 5 perfiles por nivel. Las notas salieron de unas 7 700 palabras con el código,
más que el objetivo: son dos algoritmos con demostración completa más el método.
Destino: `Lectures/2026/06-divide-y-venceras/notas.md` + PDF con scriptorium.
Extensión objetivo: 5 500–6 500 palabras con el código, como las conferencias 3 a 5.
Verificaciones: `../verif/karatsuba.py`, `../verif/seleccion.py`,
`../verif/recurrencias.py` y `../verif/ej5.py`. Cada número de este outline sale de
uno de ellos.

## Idea de la clase

Es la primera clase del Tema 2, y la primera organizada por técnica. Divide y vencerás
se enuncia en una línea (partir, resolver las partes, combinar), y lo difícil nunca es
la idea sino la cuenta: el costo de un algoritmo así es una **recurrencia**, y la
recurrencia hay que resolverla.

La clase recorre dos algoritmos que están en los dos extremos de esa cuenta:

- **Karatsuba**: tres subproblemas de la mitad. El trabajo por nivel **crece** con la
  profundidad, y el costo lo deciden las hojas: $n^{\log_2 3}$. Cierra la pregunta de
  la conferencia 1 (§9) sobre cuánto cuesta multiplicar.
- **Selección con la mediana de las medianas**: dos subproblemas de tamaños distintos,
  $n/5$ y $7n/10$. El trabajo por nivel **decrece**, y el costo lo decide la raíz:
  $O(n)$. El Teorema Maestro no se aplica, porque hay dos tamaños.

Entre los dos está el caso que ya vimos, mergesort y el par más cercano de la
conferencia 2: el trabajo por nivel se queda **constante** y se multiplica por la
altura.

El **árbol de recursión** es el método que resuelve los tres, y el Teorema Maestro es
lo que sale de aplicarlo a la forma $aT(n/b) + \Theta(n^d)$. La clase lo demuestra
como corolario y después muestra tres cosas que el corolario no cubre y el árbol sí:
la partición desigual de la selección, el cambio de variable (que aparece ya en
Karatsuba, por el acarreo) y el $n \log^2 n$ que la conferencia 2 (§7) afirmó sin
demostrar.

El error plantado es la mediana de medianas con grupos de 3. Devuelve la respuesta
correcta siempre, así que ninguna batería de pruebas de correctitud lo ve, y en las
entradas medidas cuesta casi lo mismo que la de grupos de 5. Lo que se rompe es la
garantía: la recurrencia deja de dar $O(n)$. Es el primer error plantado del curso
que no está en la respuesta sino en la cota de costo.

## Estructura

Cada sección tiene el tamaño de un audio de unos 5 minutos, salvo las marcadas.

### 1. La técnica y su cuenta (sección corta)

- **Dónde estamos.** La conferencia 2 (§5) usó divide y vencerás sin nombrarlo como
  técnica. La conferencia 1 (§9) dejó una tabla con el costo de multiplicar, con
  Karatsuba en $O(b^{1{,}585})$ sin demostrar. La conferencia 2 (§7) dijo que
  $2T(n/2) + O(n \log n)$ "da $O(n \log^2 n)$", también sin demostrar. Hoy se
  pagan las dos deudas.
- Las tres partes: partir, resolver, combinar. El costo es
  $T(n) = (\text{suma de los subproblemas}) + (\text{partir y combinar})$.
- El plan del curso dice que el Teorema Maestro se vio en Estructuras de Datos. Aquí
  se demuestra, y se ve qué no cubre.
- Mapa de la clase: un algoritmo donde mandan las hojas, uno donde manda la raíz y el
  método que analiza los dos.

### 2. Multiplicar: la escolar y el primer intento

- El modelo: números como listas de dígitos en base 10, y el costo es el número de
  multiplicaciones de un dígito (las sumas cuestan $O(n)$ y las contamos aparte). Es
  la convención de "costo por bit" de la conferencia 1 (§9), con dígitos decimales
  para poder hacerlo a mano.
- La escolar hace exactamente $n^2$ multiplicaciones de un dígito.
- **Cómo se le ocurre a uno: el intento que falla.** Partir cada número en dos
  mitades, $x = a \cdot 10^m + b$ y $y = c \cdot 10^m + d$, da
  $xy = ac \cdot 10^{2m} + (ad + bc) \cdot 10^m + bd$: cuatro productos de la mitad,
  $T(n) = 4T(n/2) + O(n)$. Medido: 4096 multiplicaciones para $n = 64$, las mismas
  que la escolar. Partir no ahorra nada si se resuelven todas las partes.
- La pregunta que deja: ¿hay que calcular $ad$ y $bc$, o basta su suma?

### 3. Karatsuba: tres productos en vez de cuatro

- El truco: $(a + b)(c + d) - ac - bd = ad + bc$. Un producto, dos restas.
- **Ejemplo chico a mano**: $21 \times 34$. $ac = 6$, $bd = 4$,
  $(2+1)(3+4) = 21$, $21 - 6 - 4 = 11$, resultado $600 + 110 + 4 = 714$. Tres
  multiplicaciones de un dígito en vez de cuatro.
- **Código ejecutable**: `sumar`, `restar`, `desplazar`, `escolar`, `karatsuba` sobre
  listas de dígitos, con un contador de multiplicaciones de un dígito. Oráculo: el `*`
  de Python, contra 3000 pares al azar de hasta 40 dígitos y casos borde (ceros,
  todos nueves). Verificado en `verif/karatsuba.py`.
- Crédito: Karatsuba y Ofman, *Doklady Akademii Nauk SSSR* 145(2), 293–294 (1962),
  presentado por Kolmogorov (registro de Math-Net.Ru).

### 4. El árbol de recursión de Karatsuba (sección larga, uno o dos audios)

- **El experimento antes de la demostración**: tabla de multiplicaciones medidas para
  $n = 2, 4, \dots, 1024$ contra $n^2$ y contra $3^{\log_2 n}$. El conteo se
  multiplica por 3 cada vez que $n$ se duplica (38 363 → 115 163 entre 512 y 1024), y
  la razón contra $n^{\log_2 3}$ se queda acotada (entre 1,7 y 2,5 en lo medido).
- **Figura 1**: el árbol de recursión de una corrida real con $n = 64$: cuántas
  llamadas hay en cada nivel y cuántos dígitos suman. Lo medido: 1, 3, 9, 27, 81,
  243, 729 llamadas; la suma de tamaños crece aproximadamente por 3/2 en cada nivel
  (64, 96, 147, 225, 357, 592, 1049 en la corrida al azar).
- **La demostración**: el nivel $i$ tiene $3^i$ subproblemas de tamaño $n/2^i$, el
  trabajo de partir y combinar es $c n (3/2)^i$; serie geométrica creciente, domina
  el último término; hay $3^{\log_2 n} = n^{\log_2 3}$ hojas.
- **El paso que todos se saltan (1)**: $a^{\log_b n} = n^{\log_b a}$, por logaritmos.
- **El paso que todos se saltan (2)**: $a + b$ puede tener un dígito más. La figura
  lo enseña: hay subproblemas de 33 y 17 dígitos, y el árbol tiene 8 niveles, no 6.
  La recurrencia verdadera es $T(n) \le 3T(\lceil n/2 \rceil + 1) + cn$. Se resuelve
  con un **cambio de variable**, $S(n) = T(n + 2)$, que la convierte en
  $S(n) \le 3S(\lceil n/2 \rceil) + c'n$. El caso base también cambia: con $n = 2$ la
  recursión llama otra vez a tamaño 2, pero termina, con a lo sumo 5 multiplicaciones
  (comprobado sobre los 10 000 pares de dos dígitos).
- Cierra la conferencia 1 (§9): la fila de Karatsuba de la tabla queda demostrada.

### 5. Segundos, no multiplicaciones

- **Figura 2** (la 3 del spec): tiempos medidos de la escolar, de Karatsuba puro (baja hasta un
  dígito) y de Karatsuba con umbral 16 (la escolar por debajo de 16 dígitos), de 8 a
  1024 dígitos, en ejes logarítmicos, con el punto de cruce del híbrido marcado.
- Lo medido en `verif/`: en multiplicaciones Karatsuba gana desde $n = 8$; en segundos,
  el puro **no** le gana a la escolar en ningún tamaño hasta 1024 (0,65 s contra
  0,31 s), porque cada llamada paga listas nuevas, sumas y restas. Con umbral 16 el
  híbrido gana a partir de unos 128 dígitos. El cruce exacto lo imprime el documento.
- La lección es la de la conferencia 1 (§2 y §4): contar operaciones esconde
  constantes, y la constante de una llamada recursiva es grande. El exponente gana
  siempre, pero solo a partir de cierto tamaño.
- Lo que hace Python: el `*` que usamos de oráculo es él mismo un Karatsuba con umbral.
  CPython usa la escolar mientras algún operando tenga a lo sumo 70 "dígitos"
  internos de 30 bits (`KARATSUBA_CUTOFF` en `Objects/longobject.c`; 30 bits por
  dígito en `sys.int_info`), unos 2100 bits.
- Hacia adelante: el capítulo 7 multiplica polinomios en $O(n \log n)$ operaciones
  aritméticas con la FFT. Para enteros, en el modelo por bit, la idea da
  $O(n \log n \log\log n)$ (Schönhage y Strassen, 1971) y $O(n \log n)$ solo con
  Harvey y van der Hoeven (Annals of Mathematics, 2021). El ejercicio 7 pide
  el mejor umbral.

### 6. El método general: árbol de recursión y Teorema Maestro

- El árbol de cualquier $T(n) = aT(n/b) + f(n)$: el nivel $i$ tiene $a^i$ nodos de
  tamaño $n/b^i$ y trabajo $a^i f(n/b^i)$. Sumar por niveles.
- **Teorema** (la forma con potencias): si $f(n) = \Theta(n^d)$ con $a \ge 1$,
  $b > 1$, $d \ge 0$, sea $r = a / b^d$. Si $r < 1$, $\Theta(n^d)$; si $r = 1$,
  $\Theta(n^d \log n)$; si $r > 1$, $\Theta(n^{\log_b a})$.
- **Demostración**: el trabajo del nivel $i$ es $n^d r^i$, una serie geométrica de
  razón $r$ con $\log_b n$ términos. Las tres cotas de la serie geométrica dan los tres
  casos. Paso que todos se saltan: en el caso $r > 1$, $n^d r^{\log_b n} =
  n^{\log_b a}$.
- Los tres casos con algoritmos que ya conocemos: búsqueda binaria ($a = 1, b = 2,
  d = 0$, $r = 1$, $\log n$), mergesort y par más cercano ($r = 1$, $n \log n$),
  Karatsuba ($r = 3/2$). Para $r < 1$, el ejemplo de la clase llega con la selección.
- La regla para recordarlo: **compara el trabajo de la raíz con el número de hojas**.
- Lo que el teorema pide y casi siempre se olvida: un solo tamaño de subproblema,
  $f$ una potencia de $n$, y $n/b$ exacto (el redondeo se arregla como en §4).

### 7. Lo que el Teorema Maestro no cubre: el $n \log^2 n$ (sección corta)

- La conferencia 2 (§7): $T(n) = 2T(n/2) + n \log_2 n$. Aquí $f(n) = n \log n$ no es
  $\Theta(n^d)$ para ningún $d$: es más que $n^1$ y menos que $n^{1 + \varepsilon}$.
  El teorema de §6 no dice nada.
- El árbol sí: el nivel $i$ trabaja $n \log_2(n / 2^i) = n(L - i)$ con $L = \log_2 n$,
  y la suma es $n L(L + 1)/2 = \Theta(n \log^2 n)$.
- **Código**: la recurrencia exacta con $T(1) = 0$ coincide con $n L(L+1)/2$ para
  $L \le 20$ (verificado).
- Los otros dos huecos tienen sección propia: el cambio de variable ya salió en §4, y
  el ejercicio 3 lo usa con $\sqrt n$; la partición desigual es la selección.

### 8. Selección: el problema y el pivote

- Enunciado: el $k$-ésimo menor de $n$ elementos (la mediana es $k = \lfloor (n-1)/2
  \rfloor$). Ordenar cuesta $O(n \log n)$. Cota mínima trivial: $\Omega(n)$, porque
  un elemento que el algoritmo nunca miró puede ser la respuesta (es el argumento del
  máximo de la conferencia 5, §5).
- **Cómo se le ocurre a uno.** La idea de quicksort, pero recursión en un solo lado:
  partir por un pivote $x$ y seguir solo en el lado donde está el $k$-ésimo. Con
  partición perfecta, $T(n) = T(n/2) + O(n) = O(n)$ ($r = 1/2$, manda la raíz).
- **El intento que falla**: el primer elemento como pivote. Sobre una entrada ya
  ordenada cada partición quita un elemento, y el costo es cuadrático: se mide.
- El pivote no tiene que ser la mediana: basta que deje fuera una **fracción fija**
  de los elementos en el peor caso. La conferencia 8 lo consigue eligiéndolo al azar,
  en esperanza. Hoy lo conseguimos en el peor caso.

### 9. La mediana de las medianas

- El algoritmo: grupos de 5, mediana de cada grupo ordenándolo, mediana de las
  medianas **por recursión**, partición en tres cubetas (menores, iguales, mayores),
  recursión en una.
- **Código ejecutable** con contador de comparaciones. Oráculo: `sorted(A)[k]`, sobre
  12 000 instancias con repetidos (verificado para grupos de 3, 5 y 7). Las tres
  cubetas son lo que hace que los repetidos no molesten; el ejercicio 5 rompe la
  versión con dos.
- **Figura 3** (la 2 del spec): una instancia real de 37 elementos: los grupos como columnas
  ordenadas, las columnas ordenadas por su mediana, $x$ marcado, y la región que se
  sabe $\ge x$ (las 3 de arriba de cada columna desde la de $x$ hacia la derecha).
  El pie da la cota y cuántos elementos quedaron de verdad a cada lado.
- **El conteo**: al menos la mitad de las $\lceil n/5 \rceil$ medianas son $\ge x$, y
  cada una arrastra dos más de su grupo. Descontando el grupo de $x$ y el último
  grupo incompleto, al menos $3(\lceil \frac{1}{2} \lceil n/5 \rceil \rceil - 2) \ge
  3n/10 - 6$ elementos son $\ge x$, y lo mismo $\le x$. El lado de la recursión tiene
  a lo sumo $7n/10 + 6$.
- **El paso que todos se saltan**: el $-2$ (el grupo de $x$ y el incompleto) y los
  repetidos (la región "$\ge x$" incluye iguales, por eso hacen falta tres cubetas).
- **Experimento**: en miles de llamadas, ninguna recursión pasa de $7n/10 + 6$.
  Una entrada construida (la mitad de los grupos con todo pequeño, la otra mitad con
  dos pequeños y tres grandes) llega a 702 de 1005, es decir $0{,}699\,n$: la cota es
  ajustada en un nivel.
- Crédito: Blum, Floyd, Pratt, Rivest y Tarjan, *Time bounds for selection*, JCSS
  7(4), 448–461 (1973).

### 10. La recurrencia que el Teorema Maestro no resuelve (sección larga)

- $T(n) \le T(\lceil n/5 \rceil) + T(7n/10 + 6) + an$. Dos tamaños distintos: no hay
  un $a$ ni un $b$.
- **El experimento**: comparaciones por elemento medidas para $n$ de 1000 a 32 000
  sobre entradas al azar y ordenadas: se quedan por debajo de 10.
- **El árbol**: el nivel $i$ trabaja a lo sumo $(9/10)^i a n$ (los tamaños de cada
  nivel suman a lo sumo $9/10$ de los del anterior, olvidando las constantes). Serie
  geométrica decreciente: $\le 10an$. Manda la raíz.
- **La demostración por sustitución**, que se ocupa de las constantes: suponer
  $T(m) \le cm$ para $m < n$; queda $T(n) \le 9cn/10 + 7c + an$, que es $\le cn$
  cuando $n \ge 140$ y $c \ge 20a$. El caso base cubre $n < 140$.
- **Paso que todos se saltan**: todo depende de $\frac15 + \frac{7}{10} < 1$. El $+6$
  y el techo cuestan solo una constante porque esa suma deja un margen de $1/10$.
- **Código**: la recurrencia evaluada exactamente hasta $n = 10^7$ con base $T(n) = n$
  para $n < 140$: $T(n)/n$ vale 4,20, 5,99, 7,23, 8,08, 8,67 (crece hacia su límite y
  nunca pasa de 20; verificado $T(n) \le 20n$ para todo $n < 200\,000$).

### 11. El error plantado: grupos de 3

- La variante: el mismo código con `g = 3`. Parece igual y es más barata por grupo.
- **Las pruebas no lo ven**: devuelve la respuesta correcta en todas las instancias
  (es correcta: el error no está en la respuesta). Y en tiempo, las comparaciones por
  elemento medidas al azar y en entradas ordenadas son parecidas a las de grupos de 5
  (en `verif/`: entre 7,8 y 12,3 para grupos de 3 contra 6,9 y 9,9 para grupos de 5,
  con $n$ hasta 64 000).
- **Lo que la demostración anunciaba**: el conteo de §9 con grupos de 3 da $\ge n/3 -
  4$ por lado, así que la recursión puede tener $2n/3 + 4$. La suma
  $\frac13 + \frac23 = 1$ ya no deja margen. El árbol de
  $T(n/3) + T(2n/3) + n$ trabaja $n$ en cada nivel durante $\log_{3/2} n$ niveles:
  la cota que sale es $O(n \log n)$, no $O(n)$.
- **Experimento**: la recurrencia evaluada para $g = 3, 5, 7$ hasta $10^7$: con 3,
  $T(n)/n$ crece sin parar (6,41 → 20,99); con 5 y con 7 se aplana.
  **Figura 4**: esas tres curvas, $T(n)/n$ contra $n$ en eje logarítmico.
- La construcción de §9 con grupos de 3 deja 401 de 603 en un lado ($0{,}665\,n$): el
  reparto de $2/3$ es alcanzable en un nivel.
- La moraleja: una batería de pruebas verifica respuestas. Una garantía de costo en el
  peor caso solo la da la demostración, y la demostración dice qué hipótesis hay que
  vigilar: que las fracciones sumen menos de 1.

### 12. La regla (cierre)

- **Figura 5**: el trabajo por nivel medido en tres algoritmos de verdad, normalizado
  por el del nivel 0: Karatsuba (crece), mergesort (constante, calculado de la
  recurrencia de la conferencia 2) y la selección (decrece, medido con el registro de
  tamaños).
- **La regla**: el costo de un divide y vencerás lo decide cómo cambia el trabajo de
  un nivel al siguiente. Si decrece, manda la raíz; si crece, mandan las hojas; si se
  queda igual, el trabajo de un nivel por la altura. El Teorema Maestro es esa regla
  cuando el cambio es una razón fija $a/b^d$.
- Hacia adelante con número: capítulo 7 (FFT, polinomios en $O(n \log n)$ operaciones aritméticas, la
  recurrencia $2T(n/2) + O(n)$ otra vez), conferencia 8 (quickselect en $O(n)$
  esperado frente a la selección de hoy), conferencia 12 (Hirschberg, divide y
  vencerás dentro de una programación dinámica), conferencia 20
  ($T(n) = T(n-1) + T(n-4)$: una recurrencia que resta en vez de dividir, cuya
  solución es exponencial y sale con otra herramienta).

### 13. Resumen

Viñetas, una por idea que hay que recordar.

### Ejercicios

1. **[traza]** Multiplica $1234 \times 5678$ con el Karatsuba de la sección 3 a mano.
   Escribe el árbol de llamadas con el tamaño de cada una y cuenta las
   multiplicaciones de un dígito. ¿En qué llamada aparece un subproblema más grande
   que la mitad, y por qué?
2. **[demostración]** Resuelve $T(n) = 2T(n/2) + n / \log_2 n$ con el árbol de
   recursión. ¿Qué caso de §6 se le parece, y por qué no se aplica?
3. **[demostración]** Resuelve $T(n) = 2T(\sqrt n) + \log_2 n$ con un cambio de
   variable.
4. **[demostración]** En §11 el árbol dio la cota superior $O(n \log n)$ para
   $T(n) = T(n/3) + T(2n/3) + n$. Demuestra que también es $\Omega(n \log n)$ sin el
   Teorema Maestro. Cuidado: el árbol no está completo, porque sus ramas tienen largos
   distintos.
5. **[entrada que rompe]** Una versión de la selección parte en menores y mayores que
   $x$, y si $k$ es justo el número de menores devuelve $x$. Pasa todas las pruebas
   con elementos distintos. Construye la entrada más corta en la que falla, y di qué
   paso de §9 dejó de valer.
6. **[cambio de hipótesis]** Grupos de 7: ¿sigue siendo lineal? Rehaz el conteo de §9
   y la recurrencia de §10. ¿Qué cambia, la constante del árbol o el trabajo por
   elemento de la raíz, y en qué dirección cada uno?
7. **[implementar y medir]** Escribe Karatsuba con un umbral $u$ por debajo del cual
   usa la escolar. Mide para varios $u$ y varios $n$ y encuentra el mejor umbral en tu
   máquina. ¿Coincide con el cruce de la figura 2? ¿Por qué no tendría por qué?
8. **[modelar]** Cuenta las inversiones de un arreglo (pares $i < j$ con
   $A[i] > A[j]$) en $O(n \log n)$. Escribe la recurrencia y demuestra la correctitud
   del paso de combinar.
9. **[modelar]** Dados dos arreglos ordenados de largo $n$, encuentra el $k$-ésimo
   menor de su unión en $O(\log n)$. ¿Cuál es la recurrencia?
10. **[demostración] ★** Toom-3 parte cada número en tres partes y multiplica con 5
    productos de un tercio. Escribe la recurrencia y su exponente, y compáralo con
    Karatsuba. ¿Por qué no se puede con 4 productos por esa vía? (Pista: el producto de
    dos polinomios de grado 2.)

## Audios (para el guion de grabación)

| Audio | Secciones | Minutos |
|---|---|---|
| 1 | 1 y 2 | 5 |
| 2 | 3 | 4 |
| 3 | 4, el experimento y la demostración | 5 |
| 4 | 4, el acarreo y el cambio de variable; 5 | 6 |
| 5 | 6 | 5 |
| 6 | 7 y 8 | 5 |
| 7 | 9 | 5 |
| 8 | 10 | 5 |
| 9 | 11 y 12 | 6 |

Total estimado: 46 minutos.

## Decisiones que quiero confirmar

- **El modelo de costo de la multiplicación son los dígitos decimales**, no los bits
  ni las palabras de 30 bits de Python. Se puede hacer a mano y los conteos son
  exactos. El precio es que los tiempos de la figura 2 son de Python puro y los cruces
  no se parecen a los de una biblioteca real (el de CPython está en unos 2100 bits).
- **Karatsuba puro no cruza a la escolar en el rango medido** (hasta 1024 dígitos).
  Extrapolando las razones medidas, el cruce estaría en varios miles de dígitos, pero
  no lo medí: medirlo cuesta decenas de segundos por render, y el render reejecuta la
  cadena. Por eso la figura 2 lleva también el híbrido con umbral 16 y el cruce que
  se marca es el suyo. La afirmación sobre "varios miles" no entra en las notas.
- **El acarreo de $a + b$ en el cuerpo**, con el cambio de variable. Muchos textos lo
  esconden. Aquí aparece porque la figura 1 lo muestra (subproblemas de 33 dígitos) y
  porque es el ejemplo natural de cambio de variable que el plan pide.
- **El error plantado de grupos de 3 se presenta como un error en la garantía**, no en
  el tiempo medido. No sé si el algoritmo con grupos de 3 es $\Theta(n \log n)$ en el
  peor caso o solo su análisis: no encontré ni construí una familia de entradas que
  lo fuerce en todos los niveles a la vez, y no lo verifiqué en una fuente primaria.
  Las notas dicen que la demostración ya no da $O(n)$ y que una entrada construida
  alcanza el reparto de $2/3$ en un nivel, y nada más.
- **Sin la historia del seminario de Kolmogorov de 1960.** La cuentan fuentes
  secundarias y el artículo de Karatsuba de 1995 en *Proc. Steklov Inst. Math.* 211,
  que no leí. Entra solo que el artículo de 1962 lo presentó Kolmogorov, que está en
  el registro de Math-Net.Ru.
- **El Teorema Maestro se enuncia en su forma con potencias $\Theta(n^d)$.** CLRS da
  una forma más general; no la cito con detalle para no afirmar qué casos cubre cada
  edición.
- **Semillas del spec que cambié:**
  - Ejercicio 2: el spec pedía $2T(n/2) + n \log n$, pero ese es justo el
    $n \log^2 n$ de la conferencia 2 que el plan pone en el cuerpo (§7). Lo cambié por
    $2T(n/2) + n/\log n$, que es $\Theta(n \log \log n)$ (verificado: $T(n)/n$ es
    exactamente el número armónico $H_L$), mismo tipo y mismo método.
  - Ejercicio 4: el spec pedía resolver $T(n/3) + T(2n/3) + n$, que es la
    recurrencia del error plantado y el cuerpo ya acota por arriba. Lo dejo con la
    misma instancia, pero pide la cota inferior, que el cuerpo no hace.
  - Ejercicio 5: el spec pedía grupos de 3, que es el error plantado del cuerpo. Lo
    cambié por la partición en dos cubetas que devuelve $x$: con elementos distintos
    falla 0 veces en 5000, con valores en $[0, 1000)$ falla 1513 de 5000, y la entrada
    más corta que la rompe tiene 6 elementos (verificado por enumeración). Mismo tipo.
  - Ejercicio 1: la semilla se queda, pero con la convención de las notas la cuenta
    incluye el acarreo (aparece un subproblema de 3 dígitos), y el enunciado lo pide.
- **Una errata de la conferencia 1 (§9)**: dice "La transformada de Fourier es el tema
  de la conferencia 6". Según `plan.md` es la 7. Estas notas dicen 7 y no tocan la 1.
- Revisión propia antes de redactar: los números de este outline se contrastaron con
  la salida de `verif/`; la razón de Karatsuba contra $n^{\log_2 3}$ medida va de 1,67
  a 2,50, y las comparaciones por elemento de §11 de 7,78 a 12,34 (grupos de 3) y de
  6,89 a 9,89 (grupos de 5). La figura 5 necesita que `seleccionar` registre la
  profundidad, así que el código de §9 lleva un parámetro `niveles` como el de
  Karatsuba.
