# Pregunta 6 :
Una matriz nxn tiene filas y columnas ordenadas de forma creciente. Diseña un algoritmo que decida si contiene un valor x en O(n) comparaciones,demuestra su correctitud con un invariante, y demuestra con un adversario que no se puede en o(n). 

**Convenciones.** $A$ es una matriz $n\times n$ con entradas comparables, e indexo $1\le i,j\le n$. Las ordenaciones son no estrictas, así que se admiten repetidos:

$$(\mathrm{F})\quad A[i][j]\le A[i][j+1]\qquad\qquad (\mathrm{C})\quad A[i][j]\le A[i+1][j]$$

La única operación sobre los datos es comparar $x$ con una entrada $A[i][j]$, con tres resultados posibles: $<$, $=$, $>$.

---

## Sección 1. Explicación del problema y propuesta del algoritmo

### El problema

**Entrada:** una matriz $A$ que cumple (F) y (C), y un valor $x$.
**Salida:** VERDADERO si existe $(p,q)$ con $A[p][q]=x$, y FALSO en caso contrario.
**Objetivo:** hacerlo con $O(n)$ comparaciones.

### Por qué los enfoques simples no bastan

| Enfoque | Comparaciones | Defecto |
|---|---|---|
| Recorrer toda la matriz | $n^2$ | ignora el orden |
| Búsqueda binaria en cada fila | $n\log n$ | ignora el orden entre filas |
| Búsqueda binaria en la diagonal y luego en dos submatrices | $O(n^{\log_2 3})$ | las dos submatrices no relacionadas por el orden siguen costando demasiado |

Se necesita una estrategia que descarte **una fila o una columna entera con una sola comparación**.

### La idea clave: la esquina superior derecha

La celda $A[1][n]$ es el **mayor elemento de su fila** y el **menor elemento de su columna**. Esto la hace informativa en ambas direcciones.

- Si $A[1][n]>x$: nada en la columna $n$ puede ser $x$, porque todos los elementos de esa columna son $\ge A[1][n]>x$. Se elimina la columna $n$.
- Si $A[1][n]<x$: nada en la fila $1$ puede ser $x$, porque todos los elementos de esa fila son $\le A[1][n]<x$. Se elimina la fila $1$.
- Si $A[1][n]=x$: se encontró.

Tras eliminar una fila o una columna queda una submatriz rectangular cuya esquina superior derecha tiene la misma propiedad, y se repite el razonamiento. Es una "escalera" que baja por filas y retrocede por columnas.

### El algoritmo

```
BUSCAR(A, n, x):
    i ← 1;  j ← n
    mientras i ≤ n  y  j ≥ 1:
        c ← comparar(x, A[i][j])
        si c es "=":  devolver VERDADERO
        si c es "<" (es decir, A[i][j] > x):  j ← j − 1     // elimina la columna j
        si c es ">" (es decir, A[i][j] < x):  i ← i + 1     // elimina la fila i
    devolver FALSO
```

### Ejemplo

$$A=\begin{pmatrix}1&4&7&11\\2&5&8&12\\3&6&9&16\\10&13&14&17\end{pmatrix}$$

**Buscar $x=6$:**

| Paso | $(i,j)$ | $A[i][j]$ | Decisión |
|---|---|---|---|
| 1 | (1,4) | 11 > 6 | $j\leftarrow 3$ |
| 2 | (1,3) | 7 > 6 | $j\leftarrow 2$ |
| 3 | (1,2) | 4 < 6 | $i\leftarrow 2$ |
| 4 | (2,2) | 5 < 6 | $i\leftarrow 3$ |
| 5 | (3,2) | 6 = 6 | VERDADERO |

**Buscar $x=15$:** se visitan (1,4)=11<15, (2,4)=12<15, (3,4)=16>15, (3,3)=9<15, (4,3)=14<15, y entonces $i=5>n$ y devuelve FALSO. Son 5 comparaciones.

---

## Sección 2. Demostración formal de correctitud

### Especificación

- **Precondición $P$:** $A$ cumple (F) y (C).
- **Postcondición $Q$:** el algoritmo devuelve VERDADERO $\iff \exists (p,q)\in[1,n]^2$ con $A[p][q]=x$.

Debemos probar tres cosas: **corrección parcial** (si termina, cumple $Q$), **terminación** y **costo**.

### Dos lemas de descarte

Primero, una consecuencia de (F) y (C) por transitividad.

**Lema 0 (monotonía global).** Si $p\le p'$ y $q\le q'$, entonces $A[p][q]\le A[p'][q']$.

*Demostración.* Por (F) aplicada repetidamente, $A[p][q]\le A[p][q']$. Por (C) aplicada repetidamente, $A[p][q']\le A[p'][q']$. Se concluye por transitividad. $\square$

**Lema 1 (descarte de columna).** Si $A[i][j]>x$, entonces para todo $p\ge i$ se tiene $A[p][j]\ne x$.

*Demostración.* Por el Lema 0 con $q=q'=j$ y $i\le p$: $A[p][j]\ge A[i][j]>x$. Luego $A[p][j]\ne x$. $\square$

**Lema 2 (descarte de fila).** Si $A[i][j]<x$, entonces para todo $q\le j$ se tiene $A[i][q]\ne x$.

*Demostración.* Por el Lema 0 con $p=p'=i$ y $q\le j$: $A[i][q]\le A[i][j]<x$. Luego $A[i][q]\ne x$. $\square$

### El invariante

Para $1\le i\le n+1$ y $0\le j\le n$ definimos la **región candidata**
$$R(i,j)=\{(p,q)\in\mathbb{Z}^2:\ i\le p\le n,\ 1\le q\le j\}.$$

(Si $i=n+1$ o $j=0$, entonces $R(i,j)=\varnothing$.)

$$\boxed{\ \mathcal I(i,j):\quad \forall (p,q)\in[1,n]^2,\ \ A[p][q]=x \ \Longrightarrow\ (p,q)\in R(i,j)\ }$$

Se cumple en cada **evaluación de la guarda** del bucle. (La Sección 3 explica este invariante en detalle.)

### Corrección parcial

**(a) Inicialización.** Antes de la primera evaluación de la guarda, $(i,j)=(1,n)$ y $R(1,n)=[1,n]^2$, así que $\mathcal I(1,n)$ se cumple trivialmente.

**(b) Conservación.** Supongamos que $\mathcal I(i,j)$ vale y que la guarda se cumple ($i\le n$, $j\ge 1$), y que la comparación no da $=$. Sea $(p,q)$ una posición con $A[p][q]=x$ (si no existe ninguna, el invariante se conserva trivialmente). Por $\mathcal I(i,j)$, $i\le p\le n$ y $1\le q\le j$.

- *Caso $A[i][j]>x$; el algoritmo hace $j\leftarrow j-1$.* Si fuera $q=j$, como $p\ge i$, el Lema 1 daría $A[p][j]\ne x$, contradicción. Luego $q\le j-1$, y por tanto $(p,q)\in R(i,j-1)$. Vale $\mathcal I(i,j-1)$.
- *Caso $A[i][j]<x$; el algoritmo hace $i\leftarrow i+1$.* Si fuera $p=i$, como $q\le j$, el Lema 2 daría $A[i][q]\ne x$, contradicción. Luego $p\ge i+1$, y por tanto $(p,q)\in R(i+1,j)$. Vale $\mathcal I(i+1,j)$.

**(c) Salida.** El bucle termina de dos formas:

1. *Por `devolver VERDADERO`.* Esto ocurre solo cuando $A[i][j]=x$ para un $(i,j)$ con $i\le n$, $j\ge1$ comprobado directamente. Luego existe una posición con valor $x$, y la respuesta VERDADERO es correcta.
2. *Por guarda falsa.* Entonces $i=n+1$ o $j=0$ (nótese que $i$ nunca supera $n+1$ ni $j$ baja de $0$, por los pasos de $\pm1$ bajo la guarda). En ambos casos $R(i,j)=\varnothing$. Por $\mathcal I(i,j)$, toda posición con valor $x$ pertenecería a $\varnothing$, así que no existe ninguna. Luego FALSO es correcto.

### Terminación

Sea $\varphi(i,j)=(n-i+1)+j$, que toma valores enteros. Sobre los estados que satisfacen la guarda, $\varphi\ge 1+1=2$.

- Cada iteración que no retorna cambia $(i,j)$ a $(i,j-1)$ o a $(i+1,j)$, y en ambos casos $\varphi$ **decrece exactamente 1**.
- Al inicio $\varphi(1,n)=2n$.

Como $\varphi$ es un entero que decrece estrictamente y está acotado inferiormente por 2 mientras se ejecuta el cuerpo del bucle, el número de iteraciones es finito.

### Costo

Las iteraciones que se ejecutan ven $\varphi=2n,2n-1,\dots,2$ (a lo sumo una vez cada valor), es decir, **a lo sumo $2n-1$ iteraciones**. Cada una hace una comparación ternaria.

**Teorema.** Con la precondición $P$, BUSCAR termina, cumple $Q$ y usa a lo sumo $2n-1$ comparaciones ternarias. En particular, es $O(n)$. $\blacksquare$

---

## Sección 3. El invariante: explicación muy detallada

### ¿Qué es un invariante y para qué sirve aquí?

Un invariante es una afirmación sobre el estado $(i,j)$ del programa que es **cierta cada vez que el bucle evalúa su guarda**. Su utilidad es que, al salir del bucle, el invariante más la negación de la guarda implican la postcondición. Todo el razonamiento sobre un bucle queda reducido a tres comprobaciones: inicio, conservación y salida.

### Lectura en palabras

$\mathcal I(i,j)$ dice:

> *"Si $x$ está en alguna parte de la matriz, entonces está dentro de la región $R(i,j)$."*

Pensemos en $R(i,j)$ como la **zona de sospechosos**. Todo lo que cae fuera de ella ya está **absuelto**: se sabe que ahí no hay $x$. El algoritmo avanza reduciendo la zona de sospechosos sin perder jamás al verdadero culpable (si existe).

Observa que el invariante es una **implicación**, no una afirmación de existencia. No dice "$x$ está en la matriz". Dice "si lo está, está aquí". Esto es lo que lo hace cierto desde el principio, sin saber nada de $x$.

### Imagen geométrica

$R(i,j)$ es el rectángulo con esquina superior derecha en $(i,j)$ y que se extiende hacia abajo hasta la fila $n$ y hacia la izquierda hasta la columna $1$.

```
          col 1   ...        j    j+1  ...  n
fila 1   [ ya        ya      ya   ya   ... ya ]   ← filas < i: descartadas
 ...     [ descartadas                         ]
fila i-1 [ ...                                 ]
fila i   [  R   R   R   R   (i,j)  ×    ×  ×  ]   × = columnas > j: descartadas
 ...     [  R   R   R   R    R     ×    ×  ×  ]
fila n   [  R   R   R   R    R     ×    ×  ×  ]
```

- Las **filas $<i$** completas están descartadas (por aplicaciones previas del Lema 2).
- Las **columnas $>j$** completas están descartadas (por aplicaciones previas del Lema 1).
- La región $R$ es lo que queda.

Con cada paso, la región se encoge por su borde superior (sube $i$) o por su borde derecho (baja $j$). La esquina $(i,j)$ recorre un camino monótono de la esquina $(1,n)$ hacia el borde inferior o izquierdo: de ahí el nombre "escalera".

### Por qué las tres comprobaciones prueban lo que queremos

**Inicio.** Cuando todavía no hemos mirado nada, no hemos descartado nada, así que la región de sospechosos es toda la matriz. Nada puede escaparse de ella, y el invariante es verdadero.

**Conservación.** Es el corazón de la demostración, y descansa en una observación geométrica: **la esquina $(i,j)$ es la celda más "extrema" de la región en ambas direcciones**. Dentro de $R(i,j)$:

- $(i,j)$ es el **máximo de su fila** (todo lo de la fila $i$ en $R$ está a su izquierda y es $\le$).
- $(i,j)$ es el **mínimo de su columna** (todo lo de la columna $j$ en $R$ está debajo y es $\ge$).

Por eso una sola comparación permite decidir cuál de las dos "tiras" (su columna o su fila) se puede retirar entera:

- *Si el valor de la esquina es demasiado grande* ($>x$), como es el mínimo de su columna, **toda su columna** es demasiado grande. Se retira la columna.
- *Si el valor de la esquina es demasiado pequeño* ($<x$), como es el máximo de su fila, **toda su fila** es demasiado pequeña. Se retira la fila.

Y lo esencial: la nueva región sigue siendo un rectángulo con esquina superior derecha, de modo que **la propiedad "la esquina es máximo de su fila y mínimo de su columna" vuelve a valer** y el razonamiento se puede repetir indefinidamente. Esto es lo que hace que el invariante sea *inductivo*.

**Salida.** Cuando $R$ queda vacía (porque $i=n+1$, no quedan filas, o $j=0$, no quedan columnas), el invariante dice "si $x$ está, está en el conjunto vacío", que es imposible. Por tanto $x$ no está. La salida es la combinación **invariante + guarda falsa $\Rightarrow$ postcondición**.

### Por qué la esquina superior derecha y no otra

Es instructivo ver qué pasa con otras esquinas:

- **Esquina superior izquierda $(1,1)$:** es el mínimo global. Si $A[1][1]<x$, no se puede descartar fila ni columna (el resto de la fila y de la columna son $\ge A[1][1]$, y pueden ser $x$). Dos opciones, ninguna decidible: el algoritmo no sabe hacia dónde ir. Peor aún, ramifica.
- **Esquina inferior derecha $(n,n)$:** es el máximo global. Simétrico: si $A[n][n]>x$ no se puede decidir.
- **Esquina superior derecha $(1,n)$ o inferior izquierda $(n,1)$:** son las dos que son "máximo en una dirección y mínimo en la otra". Solo en ellas cada resultado de la comparación elimina una tira completa. Por simetría, partir de $(n,1)$ también funciona.

### Un invariante complementario (para el análisis de costo)

Además de $\mathcal I$, el potencial $\varphi=(n-i+1)+j$ mide *cuánto falta*: es la suma del número de filas y del número de columnas que quedan en la región. Cada iteración consume exactamente una unidad de ese potencial, con exactamente una comparación. Este es el motivo preciso de que el costo sea lineal: **una comparación = una unidad de potencial**, y el potencial inicial es $2n$.

### Traza del invariante sobre el ejemplo

Con la matriz de la Sección 1 y $x=15$ (la búsqueda que falla), el 15 no está, así que el invariante vale vacuamente en todo momento. Con $x=6$, que sí está en $(3,2)$, vemos que siempre queda dentro de la región:

| Estado $(i,j)$ | Región $R(i,j)$ (filas × columnas) | ¿$(3,2)\in R$? |
|---|---|---|
| (1,4) | filas 1–4 × cols 1–4 | sí |
| (1,3) | filas 1–4 × cols 1–3 | sí |
| (1,2) | filas 1–4 × cols 1–2 | sí |
| (2,2) | filas 2–4 × cols 1–2 | sí |
| (3,2) | filas 3–4 × cols 1–2 | sí |

La región se encoge, pero nunca pierde a $(3,2)$. Es exactamente lo que el invariante asegura.

### Qué pasaría si el invariante fallara

Un algoritmo parecido pero incorrecto sería, por ejemplo, "si $A[i][j]>x$ entonces $i\leftarrow i+1$". Aquí el invariante no se conserva, porque se descarta una fila cuando lo único que se sabe es que un elemento de ella es grande, y la fila podría contener $x$ a la izquierda. El invariante es lo que separa un algoritmo correcto de uno que solo "parece razonable".

---

## Sección 4. Demostración con adversario de que no se puede en $o(n)$

### Modelo de cómputo

Un algoritmo $\mathcal A$ **determinista y adaptativo** conoce $n$ y $x$, y accede a la matriz únicamente mediante consultas $(i,j)$, cuya respuesta es el resultado de comparar $A[i][j]$ con $x$ ($<$, $=$ o $>$). La elección de la siguiente consulta puede depender de todas las respuestas anteriores. El costo es el número de consultas. $\mathcal A$ debe responder correctamente para **toda** matriz que cumpla (F) y (C).

**Afirmación a probar:** todo algoritmo correcto realiza al menos $n$ consultas en el peor caso. Por tanto el problema es $\Omega(n)$, y ningún algoritmo logra $o(n)$.

### Construcción de las entradas

Fijemos $x=2n+1$.

**Matriz base.** $B[i][j]=2(i+j)$.

**Antidiagonal.** $D=\{(k,\,n+1-k): 1\le k\le n\}$, que tiene exactamente $n$ celdas. En cada una, $i+j=n+1$, así que $B[c]=2n+2$ para todo $c\in D$.

**Matrices perturbadas.** Para cada $c\in D$, $M_c$ es igual a $B$ salvo que $M_c[c]=2n+1=x$.

### Tres propiedades

**Propiedad 1: $B$ es válida y no contiene $x$.** $B$ cumple (F) y (C), porque $B[i][j+1]=B[i][j]+2$ y $B[i+1][j]=B[i][j]+2$. Todos sus valores son pares y $x=2n+1$ es impar, así que $x\notin B$. La respuesta correcta para $B$ es **FALSO**.

**Propiedad 2: cada $M_c$ es válida y contiene $x$.** $M_c$ difiere de $B$ solo en $c$, así que (F) y (C) solo pueden fallar en pares de celdas adyacentes que incluyan a $c=(k,n+1-k)$. Sus vecinos:

- izquierdo $(k,n-k)$ y superior $(k-1,n+1-k)$ (cuando existen) tienen $i+j=n$, valor $2n\le 2n+1$. ✓
- derecho $(k,n+2-k)$ e inferior $(k+1,n+1-k)$ (cuando existen) tienen $i+j=n+2$, valor $2n+4\ge 2n+1$. ✓

Luego (F) y (C) se mantienen, y $M_c[c]=x$. La respuesta correcta para $M_c$ es **VERDADERO**.

**Propiedad 3: $B$ y $M_c$ difieren únicamente en la celda $c$.** Inmediato de la definición.

### La estrategia del adversario

El adversario **no fija la matriz de antemano**. Responde a cada consulta $(i,j)$ como si la entrada fuera $B$, es decir, contesta $\operatorname{cmp}(B[i][j],\,x)$. (En particular, a una consulta sobre $c\in D$ responde "$>$", pues $2n+2>2n+1$.)

### Teorema y demostración

**Teorema.** Todo algoritmo determinista correcto consulta **todas** las celdas de $D$ cuando la entrada es $B$. En consecuencia realiza al menos $n$ consultas.

*Demostración.* Sea $\mathcal A$ un algoritmo correcto y ejecutémoslo sobre $B$. Sea $Q$ el conjunto de celdas que consulta hasta terminar. Supongamos, por contradicción, que existe $c\in D\setminus Q$.

Consideremos las ejecuciones $E_B$ de $\mathcal A$ sobre $B$ y $E_{M_c}$ de $\mathcal A$ sobre $M_c$.

**Afirmación:** ambas ejecuciones producen la misma secuencia de consultas y respuestas.

*Por inducción sobre el paso $t$.*

- *Base ($t=0$).* Ambas ejecuciones parten del mismo estado inicial (mismos $n$, $x$, sin respuestas).
- *Paso.* Supongamos que hasta el paso $t$ las consultas y respuestas coinciden. Como $\mathcal A$ es determinista y su historial es idéntico, la consulta del paso $t+1$ es la misma en ambas ejecuciones; llamémosla $(i,j)$. En $E_B$, esa consulta pertenece a $Q$, y $c\notin Q$, luego $(i,j)\ne c$. Como $B$ y $M_c$ coinciden en toda celda distinta de $c$, la respuesta a $(i,j)$ es la misma en ambas. ∎ (afirmación)

Por tanto $\mathcal A$ termina en ambas ejecuciones con la **misma salida**. Pero la respuesta correcta es FALSO para $B$ (Propiedad 1) y VERDADERO para $M_c$ (Propiedad 2). Luego $\mathcal A$ se equivoca en al menos una de las dos entradas, contradiciendo su corrección.

Por tanto $D\subseteq Q$, y como $|D|=n$, se tiene $|Q|\ge n$. $\blacksquare$

### Conclusión

$$n\ \le\ T(n)\ \le\ 2n-1\quad\Longrightarrow\quad T(n)=\Theta(n).$$

No existe ningún algoritmo que decida la pertenencia con $o(n)$ comparaciones: el de la escalera es **asintóticamente óptimo**.

### Intuición de por qué funciona el adversario

Las $n$ celdas de la antidiagonal son **mutuamente incomparables** para las restricciones (F) y (C): ninguna está forzada por otra a ser mayor o menor, porque para dos celdas $(p,q)$ y $(p',q')$ de $D$ con $p<p'$ se tiene $q>q'$ y el Lema 0 no las relaciona. Por eso cada una puede valer $x$ de forma independiente, y la única manera de saberlo es **mirarla**. Toda la información sobre una celda de $D$ está "encerrada" en esa celda, y esto fuerza $n$ consultas.

### Observación final

La brecha entre la cota inferior $n$ y la superior $2n-1$ es un factor de 2. No afecta al resultado asintótico, que es lo que pide el enunciado. Con adversarios más finos (que además fuerzan consultas fuera de $D$) se puede acercar la cota inferior a la superior, pero no es necesario para demostrar que $o(n)$ es imposible.

# Código(Extra 06)

El script produce siete figuras, dos de ellas animadas.

**`01_s1_idea_esquina.png`** tiene tres paneles sobre la matriz de ejemplo de 4×4. El primero muestra que la esquina superior derecha es el máximo de su fila y el mínimo de su columna. El segundo, con x = 6, descarta la columna 4 porque 11 > 6. El tercero, con x = 15, descarta la fila 1 porque 11 < 15. Es la idea central del algoritmo.

**`02_s1_busqueda_x6.gif`** anima la escalera buscando x = 6. Cada cuadro marca la celda comparada, la región candidata y lo ya descartado, y muestra el camino recorrido, la decisión tomada y el contador de comparaciones. Termina en verde al encontrar el 6.

**`03_s2_flujo_e_invariante.png`** es el diagrama de flujo del bucle, con la guarda, la comparación y las ramas que descartan columna o fila. Las notas en verde indican dónde actúa cada parte de la prueba: inicio, conservación y las dos salidas. Abajo muestra el potencial φ, que baja 1 por iteración y da el límite de 2n − 1.

**`04_s3_region_candidata.png`** dibuja una matriz de 6×6 en un estado intermedio (i, j). La región candidata R(i,j) queda en azul, y las filas anteriores a i y las columnas posteriores a j en gris, ya descartadas por los Lemas 2 y 1. Ayuda a leer el invariante como "si x existe, está en lo azul".

**`05_s3_invariante_en_accion.gif`** repite la búsqueda sobre una matriz de 8×8 con x marcado con borde rojo. En cada paso comprueba el invariante y muestra "x ∈ R(i,j) ✓" mientras la región se encoge. Así se ve que x nunca sale de la zona de sospechosos.

**`06_s4_antidiagonal_incomparable.png`** muestra la matriz base B de 6×6 con la antidiagonal D resaltada, que tiene n celdas. Tomando una celda de D como referencia, el Lema 0 fuerza las celdas azules a ser menores o iguales y las naranjas claras a ser mayores o iguales. Las demás celdas de D caen en gris, sin relación forzada, por eso son incomparables.

**`07_s4_dos_mundos.gif`** muestra lado a lado B (sin x) y M_c (igual salvo en una celda c, donde vale x). El algoritmo consulta celdas distintas de c y ambos mundos responden lo mismo, con c como "?". Al revelar c se ve que el algoritmo debía responder distinto en cada mundo, y por eso se equivoca en uno de los dos.