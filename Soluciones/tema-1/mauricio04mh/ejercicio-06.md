# Ejercicio 6. Búsqueda en una matriz con filas y columnas ordenadas

Dificultad: ★★ · Código: [`ejercicio-06.py`](ejercicio-06.py)

---

## Enunciado

> Una matriz $n \times n$ tiene filas y columnas ordenadas de forma creciente. Diseña un algoritmo que decida si contiene un valor $x$ en $O(n)$ comparaciones, demuestra su correctitud con un invariante, y demuestra con un adversario que no se puede en $o(n)$.

## Qué se pide

1. Diseñar un algoritmo que decida si $x \in M$ con $O(n)$ comparaciones.
2. Demostrar su correctitud parcial con un invariante y su terminación y costo con un potencial.
3. Demostrar con un adversario que todo algoritmo de comparaciones necesita $\Omega(n)$ comparaciones.

**Mapa.** El ejercicio tiene dos mitades. Primero se construye un algoritmo que recorre la matriz como una escalera y se prueba que es correcto (invariante) y que hace a lo sumo $2n-1$ comparaciones (potencial). Después se prueba que ningún algoritmo puede hacerlo con menos de $n$ comparaciones. Esa segunda mitad no se resuelve con la cota de información, y las Preliminares explican por qué.

## Preliminares

**La matriz.** $M$ tiene filas y columnas numeradas de $0$ a $n-1$ y cumple

$$M[i][j] < M[i][j+1] \quad\text{(filas crecientes)}, \qquad M[i][j] < M[i+1][j] \quad\text{(columnas crecientes)}.$$

**Modelo de comparaciones** (Conferencia 5, §1). El algoritmo solo accede a los datos comparando $x$ con una celda; cada comparación tiene tres respuestas ($<$, $=$, $>$). El costo es el número de comparaciones. En el código de la escalera cada comparación se escribe con `==` y `<`, y cuenta como una sola; si se contara cada operador por separado, el número a lo sumo se duplicaría.

**Por qué la cota de información no basta.** La cota de información (Conferencia 5, §3) cuenta respuestas: si el problema tiene $R$ respuestas posibles, el árbol de decisión necesita al menos $R$ hojas, y como cada comparación tiene tres respuestas, un árbol de altura $h$ tiene a lo sumo $3^h$ hojas. Entonces $h \ge \log_3 R$.

- Ordenar $n$ elementos tiene $n!$ respuestas (los órdenes posibles), y la cota resulta $\Theta(n \log n)$.
- Aquí el algoritmo solo responde «está» o «no está»: $R = 2$, y la cota resulta $h \ge \log_3 2$, es decir, una sola comparación.

La información cuenta cuántas respuestas distintas hay, no cuánto hay que mirar para decidir entre ellas. Con solo dos respuestas posibles, el árbol puede ser muy bajo según este argumento, aunque en realidad el algoritmo tenga que mirar muchas celdas. Hay que usar un **adversario** (Conferencia 5, §4: cuándo la información no alcanza; §5: el adversario).

**Ejemplo** ($n = 4$). Es la matriz que se usa en el resto del ejercicio para ejecutar el algoritmo (con $x = 9$ y con $x = 15$). Cada fila crece de izquierda a derecha y cada columna de arriba hacia abajo, pero las filas no están ordenadas entre sí: la primera fila termina en $11$ y la última empieza en $10$. Por eso no se puede aplicar una búsqueda binaria a la matriz leída fila por fila.

```
  1   4   7  11
  2   5   8  12
  3   6   9  16
 10  13  14  17
```

---

## El algoritmo (la escalera)

La pregunta de esta sección es cómo recorrer la matriz sin mirarla entera. La clave es elegir una celda cuya comparación con $x$ siempre elimine toda una fila o toda una columna.

**Idea.** La esquina superior derecha $M[0][n-1]$ es la mayor de su fila y la menor de su columna. Compararla con $x$ siempre permite descartar una fila entera o una columna entera.

```python
i, j = 0, n - 1              # esquina de arriba a la derecha
while i < n and j >= 0:
    if x == M[i][j]: return "está", (i, j)
    if x < M[i][j]:  j = j - 1     # descarta la columna j
    else:            i = i + 1     # descarta la fila i
return "no está"
```

**Ejemplo con $x = 9$.**

| vuelta | $(i, j)$ | $M[i][j]$ | comparación | efecto |
|---|---|---|---|---|
| 1 | $(0,3)$ | 11 | $9 < 11$ | $j = 2$ |
| 2 | $(0,2)$ | 7 | $9 > 7$ | $i = 1$ |
| 3 | $(1,2)$ | 8 | $9 > 8$ | $i = 2$ |
| 4 | $(2,2)$ | 9 | $9 = 9$ | devuelve «está» |

**Ejemplo con $x = 15$ (no está).**

| vuelta | $(i, j)$ | $M[i][j]$ | comparación | efecto |
|---|---|---|---|---|
| 1 | $(0,3)$ | 11 | $15 > 11$ | $i = 1$ |
| 2 | $(1,3)$ | 12 | $15 > 12$ | $i = 2$ |
| 3 | $(2,3)$ | 16 | $15 < 16$ | $j = 2$ |
| 4 | $(2,2)$ | 9 | $15 > 9$ | $i = 3$ |
| 5 | $(3,2)$ | 14 | $15 > 14$ | $i = 4$ |

Con $i = 4 = n$ no quedan filas y devuelve «no está».

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="figuras/ejercicio-06-escalera-oscuro.svg">
  <img src="figuras/ejercicio-06-escalera-claro.svg" alt="La escalera sobre la matriz del ejemplo, con x = 9 y con x = 15">
</picture>

**Figura 1.** Las celdas que compara la escalera (recuadradas) y el orden en que las mira, sobre la matriz del ejemplo. Con $x = 9$ hace $4$ comparaciones y lo encuentra en $(2,2)$. Con $x = 15$ hace $5$ y sale por abajo con $i = n$.

---

## El invariante (correctitud parcial)

Los ejemplos muestran que el algoritmo va achicando la zona donde $x$ puede estar. El invariante dice exactamente cuál es esa zona: el rectángulo que queda hacia abajo y hacia la izquierda de la celda actual.

**Invariante.** Al comenzar cada vuelta del `while`:

$$\text{si } x \text{ está en } M, \text{ entonces está en el rectángulo } R = \{(a,b) : a \ge i,\ b \le j\}.$$

**Teorema 1.** El invariante vale al comenzar cada vuelta, y si el algoritmo devuelve una respuesta, esta es correcta.

**Demostración.**

**Inicialización.** Antes de la primera vuelta, $i = 0$ y $j = n-1$, y $R$ es toda la matriz.

**Mantenimiento.** Se supone el invariante al empezar una vuelta; sea $v = M[i][j]$.

- **Caso $x = v$.** Devuelve «está»; no hay otra vuelta.
- **Caso $x < v$.**
  - **Paso 1.** Sea $M[k][j]$ una celda de la columna $j$ dentro de $R$, con $k \ge i$.
  - **Paso 2.** Las columnas crecen hacia abajo: $M[k][j] \ge M[i][j] = v$.
  - **Paso 3.** Entonces $M[k][j] \ge v > x$: ninguna celda de la columna $j$ en $R$ vale $x$.
  - **Paso 4.** Por el invariante, si $x$ está en $M$ está en las columnas $\le j-1$.
  - **Paso 5.** El algoritmo hace $j = j-1$; el nuevo rectángulo es $\{a \ge i,\ b \le j-1\}$ y el invariante se mantiene.
- **Caso $x > v$.**
  - **Paso 1.** Sea $M[i][k]$ una celda de la fila $i$ dentro de $R$, con $k \le j$.
  - **Paso 2.** Las filas crecen hacia la derecha: $M[i][k] \le M[i][j] = v$.
  - **Paso 3.** Entonces $M[i][k] \le v < x$: ninguna celda de la fila $i$ en $R$ vale $x$.
  - **Paso 4.** Por el invariante, si $x$ está en $M$ está en las filas $\ge i+1$.
  - **Paso 5.** El algoritmo hace $i = i+1$; el nuevo rectángulo es $\{a \ge i+1,\ b \le j\}$ y el invariante se mantiene.

El caso $x < v$ usa que **las columnas crecen**; el caso $x > v$, que **las filas crecen**.

**Conclusión.**

**Paso 1.** El ciclo termina cuando $i = n$ o $j < 0$; en ambos casos $R$ está vacío.

**Paso 2.** Por el invariante, si $x$ estuviera en $M$ estaría en un rectángulo vacío: imposible. Luego $x \notin M$ y «no está» es correcto.

**Paso 3.** Si devolvió «está» en $(i,j)$, es porque $x = M[i][j]$: correcto. $\blacksquare$

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="figuras/ejercicio-06-escalera-animada-oscuro.gif">
  <img src="figuras/ejercicio-06-escalera-animada-claro.gif" alt="Animación de la escalera buscando x = 15, con la zona R del invariante sombreada">
</picture>

**Figura 2.** La búsqueda de $x = 15$ en la matriz del ejemplo, vuelta por vuelta. La zona sombreada es el rectángulo $R$ del invariante. Cada comparación descarta una fila o una columna de $R$ y baja $\Phi$ en $1$, de $8$ a $3$, hasta que $R$ queda vacío.

---

## El potencial (terminación y costo)

Falta probar que el ciclo termina y cuánto cuesta. Cada vuelta descarta una fila o una columna, así que basta contar cuántas filas y columnas quedan.

**Potencial.**

$$\Phi = (n - i) + (j + 1),$$

el número de filas más el número de columnas que quedan vivas.

**Teorema 2.** El algoritmo termina y hace a lo sumo $2n - 1$ comparaciones.

**Demostración.**

**Paso 1.** $i$ y $j$ son enteros, así que $\Phi$ es un entero.

**Paso 2.** El cuerpo solo se ejecuta si $i < n$ y $j \ge 0$; entonces $n - i \ge 1$ y $j + 1 \ge 1$, luego $\Phi \ge 2$ al empezar cada vuelta.

**Paso 3.** Si $j = j-1$, baja $j+1$ en $1$; si $i = i+1$, baja $n-i$ en $1$. En ambos casos $\Phi$ baja exactamente $1$.

**Paso 4.** Al empezar, $\Phi = 2n$. Cuando el ciclo se detiene, una de las dos partes vale $0$ y la otra al menos $1$, así que $\Phi \ge 1$.

**Paso 5.** Cada vuelta hace una comparación. Hay dos formas de terminar:

- **Devuelve «no está».** Cada vuelta bajó $\Phi$ en $1$, de $2n$ a un valor $\ge 1$: hubo a lo sumo $2n - 1$ vueltas.
- **Devuelve «está».** La última vuelta no baja $\Phi$, pero al empezarla $\Phi \ge 2$ (Paso 2). Las anteriores lo bajaron de $2n$ a un valor $\ge 2$, así que fueron a lo sumo $2n - 2$, y con la última son a lo sumo $2n - 1$. $\blacksquare$

Junto con el Teorema 1, el algoritmo es **totalmente correcto** y hace $O(n)$ comparaciones. Con $n = 4$ son a lo sumo $7$; los dos ejemplos usaron $4$ y $5$.

---

## Ningún algoritmo lo hace en $o(n)$ (adversario)

Ya se probó que $2n-1$ comparaciones bastan. Falta ver que no se puede bajar de orden lineal: ningún algoritmo, por ingenioso que sea, puede hacerlo con $o(n)$ comparaciones.

**Teorema 3.** Todo algoritmo correcto de comparaciones hace al menos $n$ comparaciones en el peor caso.

**La idea del adversario.** Se construyen dos matrices válidas casi idénticas: una donde $x$ no está ($M_1$) y otra donde sí está ($M_2^{c}$), que difieren en una sola celda $c$. Si el algoritmo no compara esa celda, no puede distinguirlas y se equivoca en una. Para que esto funcione hace falta que haya $n$ celdas candidatas a ser $c$ y que ninguna se pueda deducir a partir de las otras. Esas son las celdas de la antidiagonal.

**La antidiagonal.** Las celdas $(i, n-1-i)$, $i = 0, \dots, n-1$, son $n$ celdas con $s = i + j = n-1$. Dos celdas distintas de la antidiagonal están una más arriba y la otra más a la izquierda, así que el orden de la matriz **no impone** ninguna relación entre ellas.

**Un caso pequeño primero** ($n = 4$, $x = 10$). Esta es la matriz $M_1$ que se define después en general. Las celdas de la antidiagonal (las que valen $10.2$, $10.4$, $10.6$ y $10.8$) quedan entre $x$ y $x+1$, las de arriba a la izquierda valen menos que $x$ y las de abajo a la derecha valen más:

```
   6    7    8   10.2
   7    8   10.4  11
   8   10.6  11   12
  10.8  11   12   13
```

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="figuras/ejercicio-06-adversario-oscuro.svg">
  <img src="figuras/ejercicio-06-adversario-claro.svg" alt="La matriz M1 con n = 4 y x = 10, con la antidiagonal sombreada y el recorrido de la escalera">
</picture>

**Figura 3.** La matriz $M_1$ con $n = 4$ y $x = 10$. La antidiagonal (sombreada) separa los valores menores que $x$ de los mayores que $x + 1$. La escalera hace $7 = 2n - 1$ comparaciones y pasa por las $4$ celdas de la antidiagonal, como exige el Teorema 3.

**La matriz $M_1$ en general** (fijado $x$):

- Si $s \le n-2$: $M_1[i][j] = x - (n - s)$.
- Si $s \ge n$: $M_1[i][j] = x + 1 + (s - n)$.
- Si $s = n-1$ (antidiagonal), en la fila $i$: $M_1[i][n-1-i] = x + \dfrac{i+1}{n+1}$.

**$M_1$ es válida.** Al pasar a la celda siguiente de una fila o columna, $s$ sube en $1$ y el valor sube:

- entre dos celdas con $s \le n-2$: sube en $1$;
- de $s = n-2$ (valor $x-2$) a $s = n-1$ (valor entre $x$ y $x+1$): sube;
- de $s = n-1$ (valor menor que $x+1$) a $s = n$ (valor $x+1$): sube;
- entre dos celdas con $s \ge n$: sube en $1$.

**$x \notin M_1$.** Las celdas con $s \le n-2$ valen a lo sumo $x-2$; las de la antidiagonal están estrictamente entre $x$ y $x+1$; las de $s \ge n$ valen al menos $x+1$.

**La matriz $M_2^{c}$.** Para una celda $c$ de la antidiagonal, es igual a $M_1$ salvo en $c$, donde se escribe $x$. Sigue siendo válida: los vecinos de $c$ hacia arriba o la izquierda tienen $s \le n-2$ y valen a lo sumo $x-2 < x$; los de abajo o la derecha tienen $s \ge n$ y valen al menos $x+1 > x$. En $M_2^{c}$ el valor $x$ **sí está**.

**Demostración del Teorema 3.**

**Paso 1.** Se supone que un algoritmo correcto hace menos de $n$ comparaciones sobre $M_1$.

**Paso 2.** Cada comparación mira una sola celda, así que hay una celda $c$ de la antidiagonal que nunca fue comparada.

**Paso 3.** $M_1$ y $M_2^{c}$ solo difieren en $c$. Mientras el algoritmo no la compare, recibe las mismas respuestas en ambas.

**Paso 4.** Entonces recorre el mismo camino y da la misma respuesta. Pero en $M_1$ la correcta es «no está» y en $M_2^{c}$ es «está».

**Paso 5.** Se equivoca en una de las dos: contradicción. $\blacksquare$

---

## Verificación con código

El archivo [`ejercicio-06.py`](ejercicio-06.py) implementa la escalera, cuenta sus comparaciones sobre matrices aleatorias y construye las matrices $M_1$ y $M_2^{c}$ del adversario verificando que son válidas:

```
x = 9: ((2, 2), 4)
x = 15: (None, 5)

  n  pruebas  máx. comparaciones  2n-1
  2      300                   3     3
  3      300                   5     5
  4      300                   7     7
  5      300                   9     9
  8      300                  15    15
 12      300                  23    23

Adversario (antidiagonal): M1 no contiene x; M2c lo contiene en la celda c.
n = 2: M1 válida sin x, y las 2 matrices M2c válidas con x
n = 3: M1 válida sin x, y las 3 matrices M2c válidas con x
n = 4: M1 válida sin x, y las 4 matrices M2c válidas con x
n = 6: M1 válida sin x, y las 6 matrices M2c válidas con x
n = 8: M1 válida sin x, y las 8 matrices M2c válidas con x
```

El máximo de comparaciones alcanza exactamente $2n - 1$, de modo que la cota del potencial es ajustada para este algoritmo. En todos los $n$ probados, $M_1$ es válida sin $x$ y cada $M_2^{c}$ es válida con $x$.

## Resumen de resultados

| | Comparaciones en el peor caso |
|---|---|
| Cota mínima (adversario, cualquier algoritmo) | $\ge n$ |
| Escalera | $\le 2n - 1$ |

Las dos cotas son lineales: el problema es $\Theta(n)$ en el modelo de comparaciones, frente a las $n^2$ celdas de la búsqueda exhaustiva.

1. **Algoritmo:** empezar en la esquina superior derecha; si $x < M[i][j]$ descartar la columna, si $x > M[i][j]$ descartar la fila.
2. **Invariante:** si $x \in M$, está en $\{a \ge i,\ b \le j\}$.
3. **Potencial:** $\Phi = (n-i) + (j+1)$ baja $1$ por vuelta; a lo sumo $2n-1$ comparaciones.
4. **Adversario:** las $n$ celdas de la antidiagonal son independientes; sin compararlas todas no se distingue $M_1$ de una $M_2^{c}$.

## Referencias

- Conferencia 3, §1: invariante y potencial.
- Conferencia 5, §1: modelo de comparaciones.
- Conferencia 5, §4: la cota de información se queda corta cuando la salida es pequeña.
- Conferencia 5, §5: argumento del adversario.
