# Pregunta 9

Una mezcla "optimizada" de dos listas ordenadas de largo deja de comparar cuando a la primera lista le queda un solo elemento, y lo pone al final. Cuenta cuántas comparaciones hace en el peor caso. Sin probarla, usa la sección 6 de la conferencia 5 para decidir si es correcta, y construye con el adversario la entrada en la que falla.

---

# Contar cuántas comparaciones hace en el peor caso

## El algoritmo

Sean $A=(a_1<\dots<a_n)$ y $B=(b_1<\dots<b_n)$. La mezcla optimizada es la de la conferencia con dos cambios: el ciclo se detiene cuando a $A$ le queda un solo elemento, y ese elemento se coloca al final de la salida.

```python
def mezclar_optimizada(I, D, cuenta):
    R, i, j = [], 0, 0
    while i < len(I) - 1 and j < len(D):   # para cuando a I le queda 1
        cuenta[0] += 1
        if I[i] <= D[j]:
            R.append(I[i]); i += 1
        else:
            R.append(D[j]); j += 1
    return R + D[j:] + I[i:]               # el último de I (si queda) va al final
```

Si el ciclo termina porque se agotó $D$ (con $j=n$), $I[i:]$ tiene al menos dos elementos y se agrega como en la mezcla normal. Si termina porque $i=n-1$, $I[i:]$ es el único elemento que quedaba y va al final.

## Resultado

> **En el peor caso hace exactamente $2n-2$ comparaciones** (para $n\ge 1$), una menos que la mezcla original, que hace $2n-1$.

## Justificación

**Cota superior.** Cada comparación saca exactamente un elemento a la salida, sea de $A$ (y $i$ aumenta en 1) o de $B$ (y $j$ aumenta en 1). Por tanto, al terminar el ciclo,

$$\text{comparaciones} = i + j.$$

El ciclo continúa mientras $i<n-1$ y $j<n$. Hay dos formas de salir:

- **Sale porque $i=n-1$.** Antes de la última comparación se cumplía $i=n-2$ y $j<n$, así que $j\le n-1$ al salir. Entonces $i+j\le (n-1)+(n-1)=2n-2$.
- **Sale porque $j=n$.** Antes de la última comparación se cumplía $i<n-1$, es decir $i\le n-2$ (esa comparación aumentó $j$, no $i$). Entonces $i+j\le (n-2)+n=2n-2$.

En ambos casos $i+j\le 2n-2$.

**Cota inferior, el valor se alcanza.** Para $n\ge 2$, basta una entrada donde $B$ se agota antes de que $A$ llegue a su último elemento: los $n-2$ primeros elementos de $A$ son menores que todo $B$, y los dos últimos de $A$ son mayores que todo $B$:

$$a_1<\dots<a_{n-2}<b_1<\dots<b_n<a_{n-1}<a_n.$$

Los primeros $n-2$ pasos comparan $a_1,\dots,a_{n-2}$ con $b_1$, y $a_k$ gana cada vez, lo que da $n-2$ comparaciones. Luego $a_{n-1}$ se compara con $b_1,\dots,b_n$ y pierde cada vez, lo que da $n$ comparaciones más. En ese momento $j=n$ y el ciclo se detiene con $(n-2)+n=2n-2$ comparaciones, y la salida es correcta. Por ejemplo, con $n=2$, $A=[3,4]$ y $B=[1,2]$ hace 2 comparaciones.

Luego el peor caso es exactamente $2n-2$. $\square$

## Decisión usando la sección 6, sin probar el algoritmo

El teorema de la sección 6 dice que **todo** algoritmo de comparaciones que mezcle correctamente dos listas ordenadas de largo $n$ necesita $2n-1$ comparaciones en el peor caso. Esta mezcla hace a lo sumo $2n-2<2n-1$ comparaciones en todas las entradas. Es un algoritmo del modelo de comparaciones, porque solo accede a los valores preguntando si uno es menor que otro, y el teorema lo cubre.

**Conclusión: no puede ser correcta.** Es el caso de la sección 8: un algoritmo que promete menos trabajo que una cota demostrada está mal, aunque pase muchas pruebas. Falta construir la entrada concreta donde falla, y eso lo da el adversario.

---

# Construir con el adversario la entrada en la que falla

## La estrategia del adversario

Como en la sección 6, el adversario contesta como si la entrada fuera la **intercalada perfecta**, la cadena

$$c_1<c_2<\dots<c_{2n},\qquad a_k=c_{2k-1},\quad b_k=c_{2k}.$$

Es decir, $A=(1,3,5,\dots,2n-1)$ y $B=(2,4,6,\dots,2n)$. La cadena tiene $2n-1$ pares de vecinos $(c_t,c_{t+1})$, y cada par tiene un elemento de cada lista. Llamamos $X$ a esta entrada.

## Paso 1: qué pares compara el algoritmo sobre $X$

**Afirmación.** Sobre $X$ la mezcla optimizada hace exactamente $2n-3$ comparaciones, y la comparación número $m$ es la del par de vecinos $(c_m,c_{m+1})$, para $m=1,\dots,2n-3$.

*Demostración.* Por inducción sobre $m$, con el invariante "antes de la comparación $m$ se cumple $i+j=m-1$".

- Si $m=2k-1$ es impar, el invariante da $i=j=k-1$. Se comparan $a_k=c_{2k-1}$ y $b_k=c_{2k}$, que es el par $(c_m,c_{m+1})$. Gana $a_k$, así que $i$ pasa a $k$.
- Si $m=2k$ es par, entonces $i=k$ y $j=k-1$. Se comparan $a_{k+1}=c_{2k+1}$ y $b_k=c_{2k}$, que es el par $(c_{m},c_{m+1})$. Gana $b_k$, así que $j$ pasa a $k$.

El ciclo se detiene en cuanto $i=n-1$. Esto ocurre al terminar la comparación $m=2n-3$ (impar, con $k=n-1$), con $i=n-1$ y $j=n-2$. Antes de ese momento $i\le n-2$ y $j\le n-2<n$, así que el ciclo no se detiene antes. $\square$

**Consecuencia.** Quedan sin comparar dos pares de vecinos: $(c_{2n-2},c_{2n-1})=(b_{n-1},a_n)$ y $(c_{2n-1},c_{2n})=(a_n,b_n)$. Además, los elementos $a_n$ y $b_n$ **nunca participaron en ninguna comparación**. Las comparaciones $m\le 2n-3$ solo involucran $a_k$ con $k\le n-1$ y $b_k$ con $k\le n-1$.

## Paso 2: la entrada gemela $X'$

Intercambiamos los valores de $a_n$ y $b_n$, que son vecinos en la cadena (el par $t=2n-1$). Queda

$$X':\quad A'=(c_1,c_3,\dots,c_{2n-3},\,c_{2n}),\qquad B'=(c_2,c_4,\dots,c_{2n-2},\,c_{2n-1}).$$

**$X'$ es una entrada válida.** $A'$ sigue ordenada porque $c_{2n-3}<c_{2n}$, y $B'$ sigue ordenada porque $c_{2n-2}<c_{2n-1}$.

**Las dos entradas dan las mismas respuestas.** Las comparaciones hechas nunca involucraron a $a_n$ ni a $b_n$, y esos dos valores (los dos mayores de todos) siguen estando por encima de todos los demás en $X'$. Por tanto cada comparación recibe la misma respuesta en $X$ y en $X'$, y el algoritmo recorre el mismo camino y llega a la misma hoja. Como su salida depende solo de la hoja (lema 2), **produce la misma salida, escrita en posiciones, para $X$ y para $X'$**:

$$a_1,\,b_1,\,\dots,\,a_{n-1},\,b_{n-1},\;b_n,\;a_n.$$

(Los $2n-3$ primeros, hasta $a_{n-1}$, salen del ciclo; luego $D[j:]=(b_{n-1},b_n)$, y al final va $a_n$.)

## Paso 3: dónde falla

- En $X'$ se cumple $b_n<a_n$, así que la salida es correcta.
- En $X$ se cumple $a_n<b_n$, así que el orden correcto termina en $a_n,b_n$, y la salida termina en $b_n,a_n$. **La salida es incorrecta.**

Es lo que dice la sección 6: un algoritmo que termina sin comparar un par de vecinos de la cadena no puede distinguir la entrada de su gemela con el par intercambiado, y es incorrecto en una de las dos. Aquí la entrada que falla es la del adversario, $X$.

## La entrada que falla

$$\boxed{A=(1,3,5,\dots,2n-1),\qquad B=(2,4,6,\dots,2n)}$$

La mezcla optimizada devuelve $(1,2,\dots,2n-2,\;2n,\;2n-1)$: los dos últimos aparecen intercambiados.

**Ejemplo con $n=3$:** $A=[1,3,5]$ y $B=[2,4,6]$.

| Paso | Comparación | Sale | Estado |
|---|---|---|---|
| 1 | $1$ vs $2$ | $1$ | $i=1,\ j=0$ |
| 2 | $3$ vs $2$ | $2$ | $i=1,\ j=1$ |
| 3 | $3$ vs $4$ | $3$ | $i=2=n-1$: **se detiene** |

Son $3=2n-3$ comparaciones. La salida es $R+D[j:]+[5]=[1,2,3]+[4,6]+[5]=[1,2,3,4,6,5]$, que **no está ordenada**. El elemento $5$ debía ir antes que $6$, pero $5$ y $6$ nunca se compararon.

## Resumen

El ahorro de una comparación no es gratis: el elemento que se deja sin comparar puede ser menor que alguno de los que quedan en la otra lista, y el algoritmo nunca lo averigua. El adversario lo explota con la intercalada perfecta, donde ningún vecino puede omitirse.

---

# Código

El script `mezcla_optimizada_figuras.py` genera 7 figuras (5 PNG y 2 GIF) en la misma carpeta donde está guardado. Para ejecutarlo hace falta `pip install matplotlib pillow` y luego `python mezcla_optimizada_figuras.py`. Cada figura ilustra una parte de las dos secciones anteriores.

**`fig1_peor_caso_comparaciones.png`.** Es un gráfico de barras que compara, para $n$ de 1 a 8, la mezcla original ($2n-1$, la cota mínima de la sección 6) con el peor caso medido de la mezcla optimizada. El peor caso se mide recorriendo todas las $\binom{2n}{n}$ entradas posibles y da exactamente $2n-2$, que coincide con la fórmula (línea roja punteada). La figura muestra que la optimizada queda siempre una comparación por debajo de la cota, y eso es lo que delata que no puede ser correcta.

**`fig2_entrada_peor_caso.png`.** Dibuja, para $n=5$, la entrada $a_1<\dots<a_{n-2}<b_1<\dots<b_n<a_{n-1}<a_n$, que alcanza las $2n-2=8$ comparaciones. Cada línea verde es una comparación, numerada en orden. El ciclo termina porque $B$ se agota ($j=n$) con $i=n-2$, y la salida es correcta. Ilustra la cota superior de la primera sección: la optimizada puede llegar a $2n-2$, pero no más.

**`fig3_cadena_del_adversario.png`.** Muestra la entrada intercalada perfecta del adversario ($n=5$) como la cadena $c_1<\dots<c_{2n}$. Las líneas verdes son las $2n-3=7$ comparaciones que el algoritmo hace en realidad (los pares de vecinos), y las líneas rojas discontinuas son los 2 pares de vecinos que quedan sin comparar, $(b_{n-1},a_n)$ y $(a_n,b_n)$. Con $a_n$ y $b_n$ resaltados en naranja se ve que ninguno de los dos participó en comparación alguna.

**`fig4_entrada_gemela.png`.** Pone una sobre otra la entrada $X$ (la intercalada) y su gemela $X'$ (la misma entrada con los valores de $a_n$ y $b_n$ intercambiados). Las comparaciones y sus respuestas son idénticas en las dos, así que el algoritmo produce la misma salida en posiciones, $a_1,b_1,\dots,a_{n-1},b_{n-1},b_n,a_n$. Esa salida es correcta para $X'$ pero incorrecta para $X$, y la figura lo marca en verde y en rojo. Es la demostración del adversario (pasos 2 y 3) hecha visible.

**`fig5_fraccion_de_fallos.png`.** Muestra el porcentaje de entradas en las que la mezcla optimizada devuelve una salida incorrecta, recorriendo todas las entradas para $n$ de 1 a 8. Da exactamente 50 % para todo $n$ (por ejemplo 6435 de 12870 para $n=8$), porque el algoritmo falla justo cuando el máximo está en $B$, y por simetría eso ocurre en la mitad de las entradas. A diferencia del atajo del torneo de la sección 8, este error se encontraría enseguida con pruebas al azar, aunque la cota mínima lo detecta sin correr nada.

**`anim1_adversario_falla.gif`.** Es una animación paso a paso de la mezcla optimizada sobre la entrada del adversario con $n=4$ ($A=1,3,5,7$ y $B=2,4,6,8$). Muestra los punteros $i$ y $j$, la comparación de cada paso resaltada en amarillo y cómo se va llenando la salida. El algoritmo se detiene tras $2n-3=5$ comparaciones, agrega `D[j:] + I[i:]` y el último cuadro marca en rojo los dos elementos finales (8 y 7), que quedaron invertidos.

**`anim2_peor_caso_correcto.gif`.** Es la misma animación sobre una entrada que sí llega a $2n-2=6$ comparaciones ($A=1,2,7,8$ y $B=3,4,5,6$). Aquí el ciclo termina porque $B$ se agota y la salida sale correcta, toda en verde. Sirve de contraste con el GIF anterior: lo que decide si el algoritmo falla no es cuántas comparaciones hace, sino si el elemento que deja sin comparar es el máximo de la otra lista.