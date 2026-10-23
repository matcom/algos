# Ejercicio 9


## El problema 

> Una mezcla "optimizada" de dos listas ordenadas de largo $n$ deja de comparar cuando a la primera lista le queda un solo elemento, y lo pone al final. Cuenta cuántas comparaciones hace en el peor caso. Sin probarla, usa la sección 6 de la conferencia 5 para decidir si es correcta, y construye con el adversario la entrada en la que falla.

---

## Conteo de comparaciones en el peor caso

En la mezcla estándar vista en la conferencia, el peor caso ocurre cuando las dos listas de largo $n$ se encuentran perfectamente intercaladas, requiriendo exactamente $2n - 1$ comparaciones.

La versión "optimizada" altera la condición de terminación del ciclo de mezcla haciendo que este se detenga tan pronto como a la primera lista ($A$) le queda un único elemento por procesar ($i = n - 1$). 

En el peor caso (una entrada con intercalación perfecta), los elementos de ambas listas se alternan estrictamente. Para el momento en que el índice de la primera lista llega a $n - 1$, el algoritmo ha realizado todas las comparaciones necesarias excepto la del último elemento de $A$ con el elemento correspondiente en $B$. Por lo tanto, el número de comparaciones en el peor caso se reduce en uno respecto a la mezcla estándar:

$$\text{Peor caso (optimizada)} = 2n - 2$$

---

## Análisis de correctitud usando El Adversario 

Sin necesidad de ejecutar el código, la teoría de la Conferencia 5 (Sección 6) nos permite determinar inmediatamente que **el algoritmo no es correcto**.

Según el análisis del adversario para la mezcla:
1. Una mezcla correcta entre dos listas de largo $n$ opera sobre $2n$ elementos totales, los cuales forman $2n - 1$ pares de vecinos en la configuración intercalada perfecta.
2. El teorema del adversario demuestra que cualquier algoritmo correcto debe comparar **todos** los $2n - 1$ pares de vecinos. Si un algoritmo termina sin haber comparado al menos uno de esos pares, existe un intercambio local de elementos que preserva el orden de ambas listas individuales pero cambia la salida correcta.
3. Como el algoritmo optimizado se detiene antes de procesar y comparar el último elemento de $A$ con los elementos restantes de $B$, deja de comparar al menos un par de vecinos necesario. En consecuencia, el algoritmo producirá una salida errónea (o no ordenada) para dicha entrada construida por el adversario.

---

## Construcción de la entrada de fallo

Para evidenciar el fallo, construyamos un ejemplo concreto utilizando $n = 3$.

Definimos las dos listas ordenadas:
* $A = [0, 2, 5]$
* $B = [1, 3, 4]$

La salida correcta que debería producir cualquier algoritmo de mezcla válido es:
$$\text{Salida correcta} = [0, 1, 2, 3, 4, 5]$$

### Ejecución de la mezcla optimizada:
1. Compara $A[0]$ ($0$) con $B[0]$ ($1$) $\rightarrow$ $0 \le 1$. Selecciona $0$ de $A$. ($i = 1, j = 0$).
2. Compara $A[1]$ ($2$) con $B[0]$ ($1$) $\rightarrow$ $2 > 1$. Selecciona $1$ de $B$. ($i = 1, j = 1$).
3. Compara $A[1]$ ($2$) con $B[1]$ ($3$) $\rightarrow$ $2 \le 3$. Selecciona $2$ de $A$. ($i = 2, j = 1$).

En este punto, el índice $i$ de la primera lista $A$ ha alcanzado $2$, lo que significa que **a la lista $A$ le queda un único elemento** ($A[2] = 5$). 

La condición de optimización se dispara: el algoritmo **detiene las comparaciones** y asume que puede colocar el elemento restante de $A$ directamente al final, junto con el resto de $B$ sin evaluar sus relaciones relativas. Específicamente, omite comparar $A[2]$ ($5$) con el elemento restante $B[2]$ ($4$).

Al concatenar o colocar el último elemento sin compararlo, el algoritmo interrumpe el orden correcto al no intercalar adecuadamente el $4$ y el $5$, violando la propiedad de orden total de la mezcla. La cota mínima y el análisis del adversario predijeron este comportamiento exacto sin necesidad de correr pruebas empíricas.