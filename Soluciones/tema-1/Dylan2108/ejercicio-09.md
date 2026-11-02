# Ejercicio 9: la mezcla "optimizada"

> ★★ Una mezcla "optimizada" de dos listas ordenadas de largo $n$ deja de comparar
> cuando a la primera lista le queda un solo elemento, y lo pone al final. Cuenta
> cuántas comparaciones hace en el peor caso. Sin probarla, usa la sección 6 de la
> conferencia 5 para decidir si es correcta, y construye con el adversario la entrada
> en la que falla. (C5)

**Código:** [`ejercicio-09.py`](ejercicio-09.py). Recorre de forma exhaustiva las
$\binom{2n}{n}$ entradas para cada $n \le 8$, ejecuta el adversario de la sección 6 de la conferencia 5 y lo
compara con varios generadores de pruebas.

## La variante

```python
def mezcla_optimizada(A, B, menor):
    i = j = 0
    salida = []
    while len(A) - i >= 2 and j < len(B):     # ← la "optimización": exige 2 en A
        if menor(A[i], B[j]):
            salida.append(A[i]); i += 1
        else:
            salida.append(B[j]); j += 1
    if j == len(B):                           # B se acabó primero: como la mezcla normal
        return salida + A[i:]
    return salida + B[j:] + A[i:]             # a A le queda 1: "lo pone al final"
```

La idea que hay detrás parece razonable: "el último de $A$ es el mayor de $A$, así que
va al final". El problema es que es el mayor de $A$, no necesariamente el mayor de
todos.

## 1. Comparaciones en el peor caso: $2n - 2$

Cada comparación manda exactamente un elemento a la salida. El ciclo solo compara
mientras queden al menos 2 elementos en $A$ y al menos 1 en $B$. Cuando el ciclo
termina hay dos casos posibles:

- **A $A$ le queda 1.** Salieron $n - 1$ elementos de $A$ y, como $B$ todavía no está
  vacía, como máximo $n - 1$ de $B$. Total: $\le 2n - 2$.
- **$B$ se vació.** Salieron $n$ elementos de $B$ y, como a $A$ le quedan al menos 2,
  como máximo $n - 2$ de $A$. Total: $\le 2n - 2$.

La cota se alcanza. Por ejemplo, con $a_1 < b_1 < \dots < a_{n-1} < b_{n-1} < b_n < a_n$ salen $a_1..a_{n-1}$ y $b_1..b_{n-1}$, que son $2n-2$ comparaciones. El script lo
comprueba sobre **todas** las entradas:

```
  n  entradas  peor mezcla  peor optimizada  cota 2n-1  fallos optimizada
  1         2            1                0          1              50.0%
  2         6            3                2          3              50.0%
  ...
  8     12870           15               14         15              50.0%
```

$$
\boxed{\text{peor caso} = 2n - 2}
$$

## 2. Sin probarla: es incorrecta

La sección 6 de la conferencia 5 demuestra que **cualquier** algoritmo correcto de
comparaciones necesita $2n - 1$ comparaciones en el peor caso para mezclar dos listas
ordenadas de largo $n$. La variante hace como máximo $2n - 2 < 2n - 1$ comparaciones
en **todas** las entradas, así que no puede ser correcta. Debe existir una entrada
donde se equivoca, y eso lo sabemos sin ejecutar nada.

Este es el mismo uso de la cota que en la sección 8 de la conferencia 5 con el torneo que se
salta un rival: un algoritmo que dice hacer menos trabajo que una cota demostrada está
mal.

## 3. El adversario construye la entrada

### La entrada del adversario

El adversario de la sección 6 de la conferencia 5 responde como si la entrada fuera la **intercalada perfecta**,
en la que los elementos de $A$ y de $B$ se alternan:

$$
a_1 < b_1 < a_2 < b_2 < \dots < a_n < b_n .
$$

Con $n = 5$ usamos los valores $a_k = 2(k-1)$ y $b_k = 2(k-1) + 1$:

```
A = [0, 2, 4, 6, 8]        a1 a2 a3 a4 a5
B = [1, 3, 5, 7, 9]        b1 b2 b3 b4 b5

cadena:   a1 < b1 < a2 < b2 < a3 < b3 < a4 < b4 < a5 < b5
           0    1    2    3    4    5    6    7    8    9
```

Esta cadena tiene $2n - 1 = 9$ pares de vecinos: a1–b1, b1–a2, a2–b2, b2–a3, a3–b3,
b3–a4, a4–b4, b4–a5 y a5–b5. La demostración de la sección 6 de la conferencia 5 dice que un algoritmo correcto
tiene que compararlos **todos**.

### La variante sobre esa entrada

| paso | compara             | menor | sale | a A le quedan       |
| ---- | ------------------- | ----- | ---- | ------------------- |
| 1    | a1 con b1 (0 con 1) | a1    | 0    | 4                   |
| 2    | a2 con b1 (2 con 1) | b1    | 1    | 4                   |
| 3    | a2 con b2 (2 con 3) | a2    | 2    | 3                   |
| 4    | a3 con b2 (4 con 3) | b2    | 3    | 3                   |
| 5    | a3 con b3 (4 con 5) | a3    | 4    | 2                   |
| 6    | a4 con b3 (6 con 5) | b3    | 5    | 2                   |
| 7    | a4 con b4 (6 con 7) | a4    | 6    | 1: deja de comparar |

A $A$ le queda solo $a_5$, así que la variante pega lo que queda de $B$ ($b_4$ y $b_5$) y
después $a_5$. El script lo confirma:

```
n = 5, entrada intercalada del adversario: A = [0, 2, 4, 6, 8], B = [1, 3, 5, 7, 9]
  comparaciones: a1:b1 a2:b1 a2:b2 a3:b2 a3:b3 a4:b3 a4:b4 (7)
  pares de vecinos sin comparar: ['b4-a5', 'a5-b5']
  salida:    a1 b1 a2 b2 a3 b3 a4 b4 b5 a5
  correcta:  a1 b1 a2 b2 a3 b3 a4 b4 a5 b5
```

Hizo solo $2n - 3 = 7$ comparaciones y dejó **dos** pares de vecinos sin comparar: los
que rodean a $a_5$. 

### El intercambio

Como $a_5$ y $b_5$ son vecinos que nunca se compararon, el adversario puede
intercambiar sus valores, $a_5 = 9$ y $b_5 = 8$:

```
A' = [0, 2, 4, 6, 9]
B' = [1, 3, 5, 7, 8]
```

- **Las listas siguen ordenadas:** $6 < 9$ en $A'$ y $7 < 8$ en $B'$. Como $a_5$ y $b_5$
  son vecinos en la cadena, no hay ningún valor entre ellos que pueda quedar desordenado.
- **Las 7 comparaciones dan la misma respuesta**, porque ninguna involucraba a $a_5$ ni a
  $b_5$: los primeros siete pasos de la tabla son idénticos.

Un algoritmo de comparaciones no ve los valores,
solo las respuestas a sus comparaciones. Con las mismas respuestas toma las mismas
decisiones, y su salida es la misma **lista de posiciones**: primero $a_1$, después
$b_1$, y así hasta "$b_5$ y después $a_5$". Lo que cambia entre las dos entradas son los
valores que hay en esas posiciones:

| entrada                  | salida en posiciones          | salida en valores   | ¿ordenada? |
| ------------------------ | ----------------------------- | ------------------- | ----------- |
| A, B (la del adversario) | a1 b1 a2 b2 a3 b3 a4 b4 b5 a5 | 0 1 2 3 4 5 6 7 9 8 | no          |
| A', B' (intercambiada)   | a1 b1 a2 b2 a3 b3 a4 b4 b5 a5 | 0 1 2 3 4 5 6 7 8 9 | sí         |

Las dos entradas necesitan salidas **distintas**: en la original $a_5$ va antes que $b_5$
y en la intercambiada después. Pero la variante no las distingue, porque para eso
tendría que haber comparado $a_5$ con $b_5$, así que les da la misma. Una misma salida
no puede ser correcta para las dos, y el script lo comprueba:

**La entrada en la que falla es la propia entrada intercalada del adversario**,
$A = [0, 2, 4, 6, 8]$ y $B = [1, 3, 5, 7, 9]$.

En general la variante pone $a_n$ después de $b_n$ cuando $a_n < b_n$. Con $n = 1$ ni
siquiera compara: con $A = [0]$ y $B = [1]$ devuelve $[1, 0]$.

## 4. Cuándo falla exactamente

Si el ciclo termina porque a $A$ le queda un elemento, $a_n$ va después de todo lo que
quedaba en $B$. Eso es correcto solo si $a_n$ es mayor que todos ellos, es decir, si
$a_n > b_n$. Si el ciclo termina porque $B$ se vació, todo lo que sale es correcto. Y
el ciclo termina con $B$ vacía exactamente cuando $b_n$ sale antes que $a_{n-1}$, lo
que implica $b_n < a_n$. Juntando los dos casos:

$$
\textbf{la variante falla} \iff \max(A \cup B) \in B
$$

El script comprueba esta equivalencia en las $\sum_{n \le 8}\binom{2n}{n}$ entradas.
Por simetría entre $A$ y $B$, el máximo está en $B$ en exactamente la mitad de las
entradas, y por eso la tabla da un 50,0 % de fallos para todo $n$.

## 5. ¿La ven las pruebas?

| generador                                     | fallos        |
| --------------------------------------------- | ------------- |
| aleatorio (reparto al azar de $2n$ valores) | 50,4 %        |
| $A$ toda menor que $B$                    | 100 %         |
| intercalada, empieza $A$                    | 100 %         |
| **$B$ toda menor que $A$**          | **0 %** |
| **intercalada, empieza $B$**          | **0 %** |

A diferencia del torneo de la conferencia 5, que falla con probabilidad
$1/(n-1)$, este error es fácil de ver con pruebas aleatorias: una de cada dos
entradas lo detecta. Aun así, hay dos generadores naturales que no lo ven nunca.
Ninguno de los dos pone el máximo en $B$, que es justamente la condición del punto 4.

La cota mínima da la respuesta de antemano y no depende de la suerte con el
generador. Una mezcla que hace menos de $2n - 1$ comparaciones está mal, sea cual
sea el truco que use. La versión correcta de la "optimización" es la que ya hace la
mezcla clásica: cuando una lista **se vacía**, copiar la otra sin comparar. Eso no
cambia el peor caso de $2n - 1$, pero en entradas como "$B$ toda menor que $A$" ahorra
comparaciones sin dejar de ser correcta.
