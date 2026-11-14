# Ejercicio 9. Una mezcla «optimizada» de dos listas

Dificultad: ★★ · Código: [`ejercicio-09.py`](ejercicio-09.py)

---

## Enunciado

> Una mezcla «optimizada» de dos listas ordenadas de largo $n$ deja de comparar cuando a la primera lista le queda un solo elemento, y lo pone al final. Cuenta cuántas comparaciones hace en el peor caso. Sin probarla, usa la sección 6 de la conferencia 5 para decidir si es correcta, y construye con el adversario la entrada en la que falla.

## Qué se pide

1. Contar las comparaciones de la mezcla «optimizada» en el peor caso.
2. Usar la cota mínima de la mezcla (Conferencia 5, §6) para decidir, **sin ejecutarla**, si es correcta.
3. Construir con el adversario la entrada en la que falla.

## Preliminares

**Datos.** $A$ y $B$ son listas crecientes de $n$ elementos, todos distintos entre sí. El algoritmo solo accede a los datos comparando un elemento de $A$ con uno de $B$; el costo es el número de comparaciones (Conferencia 5, §1).

**Mezclar** es obtener, a partir de dos listas ordenadas, una sola lista ordenada con todos sus elementos.

**Ejemplo.** Con $A = [1,3,5]$ y $B = [2,4,6]$, la mezcla correcta es $[1,2,3,4,5,6]$.

---

## La mezcla normal

```python
i = j = 0
salida = []
while i < n and j < n:
    if A[i] <= B[j]:                  # una comparación
        salida.append(A[i]); i += 1
    else:
        salida.append(B[j]); j += 1
salida += A[i:]                       # una lista ya se acabó: se copia el resto
salida += B[j:]                       # de la otra, sin comparar
```

**Proposición 1.** La mezcla normal es correcta y hace a lo sumo $2n - 1$ comparaciones; esa cota se alcanza.

**Demostración del costo.**

**Paso 1.** Cada comparación saca un elemento a la salida.

**Paso 2.** El ciclo se detiene cuando una lista se acaba; en ese momento a la otra le queda al menos un elemento, que sale sin comparar.

**Paso 3.** De los $2n$ elementos, al menos uno sale sin comparar: comparaciones $\le 2n - 1$.

**Paso 4.** Se llega a $2n - 1$ cuando las listas se alternan. Con $A = [1,3,5]$ y $B = [2,4,6]$ son $5$ comparaciones. $\blacksquare$

**Demostración de la correctitud.** Invariante: al comenzar cada vuelta, `salida` tiene, en orden creciente, los elementos de $A[0:i]$ y $B[0:j]$, y cada uno de ellos es menor que todos los de $A[i:]$ y $B[j:]$.

- **Inicialización.** Con $i = j = 0$, `salida` está vacía.
- **Mantenimiento.** Si $A[i] < B[j]$, entonces $A[i]$ es menor que todo $A[i+1:]$ (porque $A$ está ordenada) y que todo $B[j:]$ (porque $B[j]$ es el menor de $B[j:]$): es el menor de lo que queda, y ponerlo al final de `salida` conserva las dos partes del invariante. El otro caso es simétrico.
- **Conclusión.** Al salir del ciclo una lista está agotada. Lo que queda de la otra está ordenado y es mayor que todo lo que ya salió, así que copiarlo al final da la mezcla ordenada de $A$ y $B$. $\blacksquare$

---

## La versión «optimizada» y su costo

**La idea.** La mezcla normal hace $2n - 1$ comparaciones porque al final saca un elemento sin comparar. La «optimizada» intenta ahorrar una comparación más: cuando a $A$ le queda **un solo elemento**, detiene el ciclo, copia lo que queda de $B$ y pone ese último elemento de $A$ **al final**, sin compararlo con nada. Parece razonable porque el último de $A$ es el mayor de $A$, y se supone que va al final.

```python
def mezcla_optimizada(A, B):
    n = len(A)
    i = j = 0
    salida = []
    while n - i > 1 and j < n:        # A tiene al menos 2 elementos y B no se acabó
        if A[i] <= B[j]:              # una comparación
            salida.append(A[i]); i += 1
        else:
            salida.append(B[j]); j += 1
    salida += B[j:]                   # lo que quede de B
    salida += A[i:]                   # lo que quede de A (a lo sumo 1 elemento) va al final
    return salida
```

La única diferencia con la mezcla normal es la condición del `while`: corta una vuelta antes cuando es $A$ la que se agota.

**Ejemplo** con $A = [2,4,6]$ y $B = [1,3,5]$:

| vuelta | `i` | `j` | comparación | sale |
|---|---|---|---|---|
| 1 | 0 | 0 | 2 contra 1 | 1 |
| 2 | 0 | 1 | 2 contra 3 | 2 |
| 3 | 1 | 1 | 4 contra 3 | 3 |
| 4 | 1 | 2 | 4 contra 5 | 4 |

Tras la vuelta 4, `i = 2`: a $A$ le queda un solo elemento (el $6$). Se copia el $5$ de $B$ y se pone el $6$ al final: $[1,2,3,4,5,6]$. En esta entrada la salida es correcta y se hicieron $4$ comparaciones.

**Proposición 2.** La mezcla «optimizada» hace a lo sumo $2n - 2$ comparaciones, y esa cota se alcanza.

**Demostración.**

**Paso 1.** Cada vuelta hace una comparación y avanza `i` o `j` en $1$. Al terminar, el número de comparaciones es $i + j$.

**Paso 2.** El ciclo termina por una de dos razones.

- **Porque a $A$ le queda un elemento ($i = n-1$).** La última vuelta avanzó `i` desde $n-2$, y en ella $j \le n-1$ (si $j = n$ el ciclo ya habría terminado). Entonces $i + j \le (n-1) + (n-1) = 2n - 2$.
- **Porque $B$ se acabó ($j = n$).** La última vuelta avanzó `j` desde $n-1$, con $i \le n-2$. Entonces $i + j \le (n-2) + n = 2n - 2$.

**Paso 3.** La cota se alcanza: con $n = 3$ el ejemplo anterior hace $4 = 2n - 2$ comparaciones. $\blacksquare$

Es una comparación menos que la mezcla normal.

---

## Dónde falla la versión optimizada

La suposición «el último de $A$ es el mayor» es falsa cuando $B$ todavía tiene elementos más grandes. Primero se ve una entrada concreta en la que falla, y después cuándo sí acierta.

### La entrada en la que falla

Se toma la cadena intercalada:

$$A = [1,3,5,\dots,2n-1], \qquad B = [2,4,6,\dots,2n].$$

**Paso 1. Qué hace.** Las listas se alternan: salen $a_1, b_1, a_2, b_2, \dots$ Cuando sale $a_{n-1}$ (el elemento $2n-3$), a $A$ le queda un elemento y el ciclo se detiene, tras $2n-3$ comparaciones.

**Paso 2. Qué queda sin comparar.** Los pares $(b_{n-1}, a_n)$ y $(a_n, b_n)$: el algoritmo nunca comparó $a_n$.

**Paso 3. Qué devuelve.** Lo que ya salió, luego lo que queda de $B$ ($b_{n-1}, b_n$) y al final $a_n$:

$$[1,2,\dots,2n-3,\ 2n-2,\ 2n,\ 2n-1].$$

Los dos últimos están al revés: **la salida es incorrecta.**

**Ejemplo con $n = 3$,** $A = [1,3,5]$, $B = [2,4,6]$:

| vuelta | `i` | `j` | comparación | sale |
|---|---|---|---|---|
| 1 | 0 | 0 | 1 contra 2 | 1 |
| 2 | 1 | 0 | 3 contra 2 | 2 |
| 3 | 1 | 1 | 3 contra 4 | 3 |

Tras la vuelta 3, `i = 2` y a $A$ le queda el $5$. Se copia lo que queda de $B$ ($4$ y $6$) y se pone el $5$ al final: $[1,2,3,4,6,5]$, en vez de $[1,2,3,4,5,6]$. Hizo $3$ comparaciones, menos de las $5$ necesarias. El error es que **nunca comparó el $5$ con el $6$**.

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="figuras/ejercicio-09-intercalado-oscuro.svg">
  <img src="figuras/ejercicio-09-intercalado-claro.svg" alt="Pares de vecinos que comparan la mezcla normal y la optimizada sobre la cadena intercalada con n = 3">
</picture>

**Figura 1.** Los pares de vecinos de la cadena $1 < 2 < \dots < 6$ que compara cada mezcla, con $A = [1,3,5]$ y $B = [2,4,6]$. La normal compara los $5$. La optimizada compara $3$ y deja sin comparar $(b_2, a_3)$ y $(a_3, b_3)$ (en rojo punteado), y por eso pone el $5$ después del $6$.

### ¿Cuándo acierta?

En el primer ejemplo de la versión optimizada, con $A = [2,4,6]$ y $B = [1,3,5]$, la salida sí fue correcta. No es casualidad:

**Proposición 3.** La mezcla «optimizada» devuelve la salida correcta si y solo si el máximo de los $2n$ elementos está en $A$. En particular, falla en exactamente la mitad de las entradas.

**Demostración.**

**Paso 1 ($\Leftarrow$).** Si el máximo es $A[n-1]$, el único elemento que el algoritmo puede dejar sin comparar en $A$ es $A[n-1]$, y ponerlo al final es correcto. Si el ciclo terminó porque $B$ se acabó, el resto de $A$ se copia en orden, también correcto.

**Paso 2 ($\Rightarrow$).** Si el máximo es $B[n-1]$, entonces $A[n-1] < B[n-1]$. El ciclo se detiene con $i = n-1$ antes de consumir $A[n-1]$; como $B[n-1] > A[n-1]$ no puede haberse consumido antes, así que $j < n$ y $B[n-1]$ sigue sin salir. Se copia lo que queda de $B$ (que incluye $B[n-1]$) y luego $A[n-1]$ va después de un elemento mayor: salida incorrecta.

**Paso 3.** El máximo está en $A$ en la mitad de las $\binom{2n}{n}$ entradas (por simetría), es decir, en $\binom{2n-1}{n}$ de ellas. $\blacksquare$

---

## Por qué no puede ser correcta (cota mínima, Conferencia 5, §6)

La versión optimizada acierta en la mitad de las entradas, así que las pruebas al azar no bastan para descartarla. Lo que la descarta es una cota mínima: ningún algoritmo de comparaciones puede mezclar con menos de $2n - 1$ comparaciones.

**Argumento del adversario** (Conferencia 5, §5). Para probar una cota inferior se hace que el adversario conteste como una entrada concreta y se muestra que, si el algoritmo omite una comparación, existen dos entradas que no distingue y cuyas respuestas correctas difieren.

**Teorema 1.** Todo algoritmo que mezcle dos listas ordenadas de largo $n$ por comparaciones necesita $2n - 1$ comparaciones en el peor caso.

**La entrada del adversario.** El adversario contesta como si la entrada fuera la cadena intercalada

$$a_1 < b_1 < a_2 < b_2 < \dots < a_n < b_n,$$

donde las $a_i$ forman $A$ y las $b_i$ forman $B$. Para $n = 3$: $A = [1,3,5]$, $B = [2,4,6]$.

**Los pares de vecinos.** La cadena tiene $2n$ elementos y $2n - 1$ pares de vecinos consecutivos:

$$(a_1,b_1),\ (b_1,a_2),\ (a_2,b_2),\ \dots,\ (b_{n-1},a_n),\ (a_n,b_n),$$

y cada par tiene un elemento de $A$ y uno de $B$.

**Demostración (por contradicción).** Se prueba que un algoritmo correcto debe comparar **todos** los pares de vecinos.

**Paso 1.** Se supone que el algoritmo termina sin haber comparado el par de vecinos $(u,v)$, con $u < v$ consecutivos en la cadena.

**Paso 2.** Se construye una segunda entrada **intercambiando los valores** de $u$ y $v$.

**Paso 3.** Las dos listas siguen ordenadas. Si $c_1 < c_2 < \dots < c_{2n}$ son los valores de la cadena y el par es $(a_i, b_i) = (c_{2i-1}, c_{2i})$, tras el intercambio $a_i = c_{2i}$ y $b_i = c_{2i-1}$:

- en $A$: $a_{i-1} = c_{2i-3} < c_{2i}$ y $a_{i+1} = c_{2i+1} > c_{2i}$;
- en $B$: $b_{i-1} = c_{2i-2} < c_{2i-1}$ y $b_{i+1} = c_{2i+2} > c_{2i-1}$.

El par $(b_i, a_{i+1})$ es simétrico. La razón es que $u$ y $v$ son vecinos: no hay ningún valor entre ellos.

**Paso 4.** Toda comparación que hizo el algoritmo compara un elemento de $A$ con uno de $B$ y no es la de $(u,v)$. Su respuesta no cambia con el intercambio, porque $u$ y $v$ solo se intercambiaron entre sí y no hay nada entre ellos.

**Paso 5.** El algoritmo sigue el mismo camino y da la **misma salida** en ambas entradas.

**Paso 6.** Pero la mezcla correcta es distinta: en una $u$ va antes que $v$ y en la otra, después.

**Paso 7.** Se equivoca en una de las dos: contradicción. Hacen falta al menos $2n-1$ comparaciones. $\blacksquare$

La mezcla normal alcanza esa cota (Proposición 1), así que es óptima.

### La decisión, sin ejecutarla

**Paso 1.** Por la Proposición 2, la mezcla optimizada hace a lo sumo $2n - 2$ comparaciones.

**Paso 2.** Por el Teorema 1, cualquier algoritmo correcto necesita $2n - 1$ en el peor caso.

**Paso 3.** Como $2n - 2 < 2n - 1$, **no puede ser correcta**.

**Paso 4.** Más concretamente: en la entrada de la cadena deja sin comparar algún par de vecinos; el adversario intercambia sus valores y el algoritmo se equivoca en una de las dos entradas.

### La entrada gemela

Se intercambian los valores del par $(a_n, b_n)$, que el algoritmo nunca comparó:

$$A' = [1,3,\dots,2n-3,\ 2n], \qquad B' = [2,4,\dots,2n-2,\ 2n-1].$$

Con $n = 3$: $A' = [1,3,6]$ y $B' = [2,4,5]$. Las comparaciones y respuestas son idénticas (tabla de «La entrada en la que falla»); se copia lo que queda de $B'$ ($4$, $5$) y se pone el $6$ al final: $[1,2,3,4,5,6]$, **correcta**. El algoritmo hace lo mismo en las dos entradas y las mezclas correctas son distintas: acierta en una y falla en la otra, exactamente lo que predice el adversario.

---

## Verificación con código

El archivo [`ejercicio-09.py`](ejercicio-09.py) enumera **todas** las intercalaciones posibles de $A$ y $B$ para $n = 2, \dots, 7$, mide el máximo de comparaciones de ambas mezclas y cuenta las entradas en que la optimizada falla. También registra qué pares compara cada versión sobre la cadena intercalada.

Ejemplo $A=[2,4,6]$, $B=[1,3,5]$: la mezcla optimizada da $[1,2,3,4,5,6]$ con $4$ comparaciones, igual que la correcta.

| $n$ | normal máx. | $2n-1$ | optimizada máx. | $2n-2$ | entradas incorrectas | de |
|---|---|---|---|---|---|---|
| 2 | 3 | 3 | 2 | 2 | 3 | 6 |
| 3 | 5 | 5 | 4 | 4 | 10 | 20 |
| 4 | 7 | 7 | 6 | 6 | 35 | 70 |
| 5 | 9 | 9 | 8 | 8 | 126 | 252 |
| 6 | 11 | 11 | 10 | 10 | 462 | 924 |
| 7 | 13 | 13 | 12 | 12 | 1716 | 3432 |

Entrada del adversario (cadena intercalada) para $n = 3$:

| versión | resultado | comparaciones | pares comparados |
|---|---|---|---|
| mezcla normal | $[1,2,3,4,5,6]$ | 5 | $(1,2),(2,3),(3,4),(4,5),(5,6)$ |
| mezcla optimizada | $[1,2,3,4,6,5]$ | 3 | $(1,2),(2,3),(3,4)$ |

Entrada gemela $A'=[1,3,6]$, $B'=[2,4,5]$: la optimizada da $[1,2,3,4,5,6]$ con $3$ comparaciones.

Los máximos medidos coinciden con $2n-1$ y $2n-2$. Las entradas incorrectas son exactamente $\binom{2n-1}{n}$ (por ejemplo $10$ de $20$ para $n=3$ y $1716$ de $3432$ para $n=7$), la mitad, como dice la Proposición 3. La mezcla normal compara los cinco pares de vecinos de la cadena; la optimizada solo tres.

## Resumen de resultados

1. **Mezcla normal:** a lo sumo $2n - 1$ comparaciones (óptima).
2. **Mezcla optimizada:** a lo sumo $2n - 2$ comparaciones.
3. **Cota mínima (Conferencia 5, §6):** toda mezcla necesita $2n - 1$, una por cada par de vecinos de la cadena $a_1 < b_1 < \dots < a_n < b_n$.
4. **Decisión:** $2n - 2 < 2n - 1$, luego la optimizada es incorrecta.
5. **Entrada que falla:** la cadena intercalada; para $n = 3$ da $[1,2,3,4,6,5]$. Es correcta solo cuando el máximo está en $A$ (la mitad de las entradas).

## Referencias

- Conferencia 5, §1: modelo de comparaciones.
- Conferencia 5, §5–§6: argumento del adversario y cota $2n-1$ para la mezcla.
- Conferencia 5, §8: una cota mínima demostrada sirve también para detectar algoritmos incorrectos.
