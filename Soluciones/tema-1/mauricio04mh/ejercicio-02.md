# Ejercicio 2. Búsqueda binaria: invariante, potencial y cota de información

Dificultad: ★ · Código: [`ejercicio-02.py`](ejercicio-02.py)

---

## Enunciado

> Da el invariante y el potencial de la búsqueda binaria, y la cota de información que la hace óptima.

## Qué se pide

1. Enunciar y demostrar un **invariante** de la búsqueda binaria (correctitud parcial).
2. Definir y demostrar un **potencial** que garantice la terminación y acote el número de vueltas.
3. Demostrar la **cota de información**: ningún algoritmo de comparaciones busca con menos comparaciones, de modo que la búsqueda binaria es óptima.

## Preliminares

**Correctitud** (Conferencia 3, §1). Un algoritmo es correcto respecto a una especificación (precondición y postcondición). La correctitud total es la correctitud parcial (si termina, la salida es correcta) más la terminación. La primera se demuestra con un invariante (inicialización, mantenimiento, conclusión) y la segunda con un potencial entero no negativo que baja en cada vuelta.

**Modelo de comparaciones** (Conferencia 5, §1). El algoritmo solo accede a los datos comparando; el costo es el número de comparaciones. Todo algoritmo de este modelo es un árbol de decisión cuya altura es el costo en el peor caso (§2). **Lema 1 de la Conferencia 5:** un árbol binario de altura $h$ tiene a lo sumo $2^h$ hojas.

**El algoritmo.** Se busca $x$ en un arreglo $A$ de $n$ elementos distintos y ordenados de forma creciente. El rango $A[lo:hi]$ incluye la posición `lo` y excluye la posición `hi`.

```python
lo, hi = 0, n
while lo < hi:
    m = (lo + hi) // 2
    if x == A[m]: return "está", m
    if x < A[m]:  hi = m
    else:         lo = m + 1
return "no está"
```

Cada comparación de $x$ con $A[m]$ tiene tres respuestas: $x < A[m]$, $x = A[m]$ o $x > A[m]$. En el código se escribe con dos operadores (`==` y después `<`), pero en el modelo de la Conferencia 5 cuenta como una sola comparación de tres respuestas. Si se contara cada operador por separado, el número de comparaciones a lo sumo se duplicaría.

**Ejemplo.** Con $A = [1, 3, 5, 7, 9, 11, 13]$ y $x = 11$:

| vuelta | lo | hi | m | $A[m]$ | comparación | efecto |
|---|---|---|---|---|---|---|
| 1 | 0 | 7 | 3 | 7 | $11 > 7$ | `lo = 4` |
| 2 | 4 | 7 | 5 | 11 | $11 = 11$ | devuelve «está» |

---

## El invariante (correctitud parcial)

**Invariante.** Al comenzar cada vuelta del `while`:

$$\text{si } x \text{ está en } A, \text{ entonces } x \text{ está en } A[lo:hi].$$

**Inicialización.** Antes de la primera vuelta, $lo = 0$ y $hi = n$. El rango $A[0:n]$ es todo el arreglo, así que si $x$ está en $A$, está en él.

**Mantenimiento.** Se supone que el invariante vale al empezar una vuelta en la que se ejecuta el cuerpo, de modo que $lo \le m < hi$.

- **Caso $x = A[m]$.** El algoritmo devuelve «está» y no hay otra vuelta que mantener.
- **Caso $x < A[m]$.**

  **Paso 1.** Como $A$ está ordenado con elementos distintos, $A[j] \ge A[m]$ para todo $j \ge m$.

  **Paso 2.** Entonces $A[j] \ge A[m] > x$ para todo $j \ge m$, es decir, $x$ no está en $A[m:hi]$.

  **Paso 3.** Por el invariante, si $x$ está en $A$ está en $A[lo:hi]$, y como no está en $A[m:hi]$, está en $A[lo:m]$.

  **Paso 4.** El algoritmo hace $hi = m$. El nuevo rango es $A[lo:m]$ y el invariante se mantiene.
- **Caso $x > A[m]$.** Es análogo al caso anterior, con las desigualdades invertidas. El algoritmo hace $lo = m + 1$ y el invariante se mantiene en el nuevo rango $A[m+1:hi]$.

**Conclusión.** El ciclo termina cuando $lo \ge hi$, es decir, con el rango vacío. Por el invariante, si $x$ estuviera en $A$ estaría en un rango vacío, lo cual es imposible. Entonces $x$ no está en $A$ y devolver «no está» es correcto. Si el algoritmo devolvió «está» en la posición $m$, es porque $x = A[m]$, lo que también es correcto. $\blacksquare$

Esto prueba la **correctitud parcial**. Falta probar que el algoritmo termina.

---

## El potencial (terminación y costo)

El invariante solo garantiza que, si el algoritmo termina, responde bien. Falta probar que termina, y cuántas vueltas da.

**Potencial.**

$$\Phi = hi - lo,$$

el tamaño del rango que queda por mirar.

**Lema 1.** (a) $\Phi$ es un entero. (b) $\Phi \ge 1$ al empezar cada vuelta. (c) En cada vuelta, $\Phi_{\text{nuevo}} \le \lfloor \Phi/2 \rfloor$.

**Demostración.**

(a) $lo$ y $hi$ son enteros.

(b) El cuerpo solo se ejecuta si $lo < hi$.

(c) Sea $k = hi - lo \ge 1$. Entonces $m = lo + \lfloor k/2 \rfloor$.

- Si $hi = m$: $\Phi_{\text{nuevo}} = m - lo = \lfloor k/2 \rfloor$.
- Si $lo = m + 1$: $\Phi_{\text{nuevo}} = hi - m - 1 = k - \lfloor k/2 \rfloor - 1 = \lceil k/2 \rceil - 1 \le \lfloor k/2 \rfloor$.

En ambos casos $\Phi_{\text{nuevo}} \le \lfloor k/2 \rfloor < k$. $\blacksquare$

**Teorema 1 (terminación y costo).** La búsqueda binaria termina y hace a lo sumo $\lceil \log_2 (n+1) \rceil$ comparaciones.

**Demostración.**

**Paso 1.** Por el Lema 1(c), después de $j$ vueltas $\Phi_j \le \lfloor n / 2^j \rfloor$.

**Paso 2.** El ciclo termina cuando $\Phi = 0$. Esto ocurre seguro si $2^j > n$, porque entonces $\lfloor n/2^j \rfloor = 0$. El menor $j$ con $2^j > n$ es $\lfloor \log_2 n \rfloor + 1 = \lceil \log_2(n+1) \rceil$.

**Paso 3.** Cada vuelta hace una sola comparación (de tres respuestas). Por tanto el número de comparaciones es a lo sumo $\lceil \log_2 (n+1) \rceil$. $\blacksquare$

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="figuras/ejercicio-02-rango-oscuro.svg">
  <img src="figuras/ejercicio-02-rango-claro.svg" alt="El rango de la búsqueda binaria vuelta por vuelta, con x = 11 y con x = 8">
</picture>

**Figura 1.** El rango $A[lo:hi]$ (sombreado) y la posición $m$ que se compara (recuadrada) en cada vuelta, con $A = [1,3,5,7,9,11,13]$. Con $x = 11$ lo encuentra en la vuelta $2$. Con $x = 8$ el potencial $hi - lo$ pasa por $7, 3, 1, 0$: son $3 = \lceil \log_2 8 \rceil$ comparaciones, como dice el Teorema 1.

Junto con el invariante de la sección anterior, el algoritmo es **totalmente correcto**.

**Por qué `lo = m + 1` y no `lo = m`.** Con `lo = m` el potencial no baja siempre. Con $A = [5]$ y $x = 7$: `lo = 0`, `hi = 1`, `m = 0`, $7 > A[0]$ y `lo = m` deja `lo = 0`. El potencial sigue en $1$ y el ciclo no termina (Conferencia 3, ejercicio 7).

---

## La cota de información

La búsqueda binaria hace $\lceil \log_2 (n+1) \rceil$ comparaciones. Falta ver que ningún otro algoritmo de comparaciones hace menos.

**Teorema 2.** Todo algoritmo de comparaciones que busque $x$ en un arreglo ordenado de $n$ elementos distintos hace al menos $\lceil \log_2 (n+1) \rceil$ comparaciones en el peor caso.

**El árbol de decisión.** Cada nodo interno compara $x$ con un $A[m]$ y tiene una rama por respuesta; cada hoja es una salida. El costo en el peor caso es la altura.

**Los huecos.** Si $x$ no está en $A$, cae en uno de los $n+1$ **huecos**:

$$h_0:\ x < A[1], \qquad h_i:\ A[i] < x < A[i+1], \qquad h_n:\ A[n] < x.$$

Con $n = 7$ hay 8 huecos.

**Lema 2 (Conferencia 5, Lema 4).** Si $x_1$ y $x_2$ caen en huecos distintos, un algoritmo correcto los lleva a hojas distintas.

**Demostración (por contradicción).**

**Paso 1.** Se supone que $x_1$ y $x_2$ llegan a la misma hoja, y que el hueco de $x_1$ está a la izquierda del de $x_2$.

**Paso 2.** Entre los dos huecos hay al menos un elemento $A[k]$ con $x_1 < A[k] < x_2$.

**Paso 3.** El algoritmo no comparó con ningún elemento situado entre los dos huecos: si lo hubiera hecho con uno de ellos, $x_1$ habría recibido «$<$» y $x_2$ «$>$», y habrían seguido ramas distintas.

**Paso 4.** Entonces todo $A[j]$ comparado está a la izquierda de ambos huecos o a la derecha de ambos, y para esos $A[j]$ el valor $A[k]$ recibe la misma respuesta que $x_1$ y $x_2$ (y es distinto de $A[j]$).

**Paso 5.** Con $x = A[k]$ el algoritmo recorre el mismo camino y llega a la misma hoja, donde dice «no está» porque esa es la salida de $x_1$.

**Paso 6.** Pero $A[k]$ sí está en $A$. El algoritmo se equivoca, lo que contradice su correctitud. $\blacksquare$

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="figuras/ejercicio-02-contradiccion-oscuro.gif">
  <img src="figuras/ejercicio-02-contradiccion-claro.gif" alt="Animación: un algoritmo que nunca compara con 11 lleva 10, 12 y 11 a la misma hoja">
</picture>

**Figura 2.** El Lema 2 con un algoritmo concreto que nunca compara con $A[5] = 11$ (`busqueda_sin` en [`ejercicio-02.py`](ejercicio-02.py)). Su árbol tiene una sola hoja para los huecos $h_5$ y $h_6$. A ella llegan $x_1 = 10$ y $x_2 = 12$, y también $x = 11$, que recibe las mismas respuestas: el algoritmo dice «no está» y se equivoca, como en los Pasos 5 y 6.

**Demostración del Teorema 2.**

**Paso 1.** Por el Lema 2, los $n+1$ huecos necesitan $n+1$ hojas distintas.

**Paso 2.** Para un $x$ que no está en $A$, la respuesta «$x = A[m]$» nunca ocurre, así que la parte del árbol que se recorre solo usa las ramas «$<$» y «$>$»: es un árbol binario.

**Paso 3.** Por el Lema 1 de la Conferencia 5, un árbol binario de altura $h$ tiene a lo sumo $2^h$ hojas. Entonces $2^h \ge n+1$.

**Paso 4.** Tomando $\log_2$ y usando que la altura es entera: $h \ge \lceil \log_2(n+1) \rceil$. $\blacksquare$

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="figuras/ejercicio-02-hojas-oscuro.gif">
  <img src="figuras/ejercicio-02-hojas-claro.gif" alt="Animación: en el árbol de decisión de la búsqueda binaria con n = 7, cada hueco llega a su propia hoja">
</picture>

**Figura 3.** El árbol de decisión de la búsqueda binaria con $A = [1,3,5,7,9,11,13]$, construido corriendo el algoritmo. Cada nodo compara $x$ con el valor que muestra, y la rama «$=$» lleva a la hoja «está». Un $x$ de cada hueco recorre su camino: los $8$ huecos llegan a $8$ hojas distintas, todas a profundidad $3 = \lceil \log_2 8 \rceil$.

**Nota (por qué no basta la cota con tres ramas).** Con tres respuestas por nodo el Lema 1 solo daría $3^h$ hojas y, por tanto, una cota $\log_3$. Por eso el argumento se restringe a las entradas con $x \notin A$, donde solo hay dos ramas (Conferencia 5, §3).

---

## Verificación con código

El archivo [`ejercicio-02.py`](ejercicio-02.py) implementa el algoritmo vigilando en cada vuelta el invariante y la cota del potencial ($\Phi_{\text{nuevo}} \le \lfloor \Phi/2 \rfloor$), y mide el peor caso consultando todos los elementos y todos los huecos, para $1 \le n \le 129$:

```
   n  peor caso medido  ceil(log2(n+1))  huecos n+1
   1                 1                1           2
   3                 2                2           4
   7                 3                3           8
  15                 4                4          16
  31                 5                5          32
  63                 6                6          64
 127                 7                7         128
peor caso = ceil(log2(n+1)) para todo 1 <= n <= 129

Variante con lo = m, A = [5], x = 7: no termina
Búsqueda binaria correcta, A = [5], x = 7: ('no está', None)
```

El peor caso medido coincide con la cota $\lceil \log_2 (n+1) \rceil$ para todos los $n$ probados, y la variante con `lo = m` no termina, como se predijo.

## Resumen de resultados

| | Comparaciones en el peor caso |
|---|---|
| Cota mínima (cualquier algoritmo de comparaciones) | $\lceil \log_2 (n+1) \rceil$ |
| Búsqueda binaria | $\lceil \log_2 (n+1) \rceil$ |

1. **Invariante:** si $x$ está en $A$, está en $A[lo:hi]$.
2. **Potencial:** $\Phi = hi - lo$, entero, positivo mientras el ciclo corre, y con $\Phi_{\text{nuevo}} \le \lfloor \Phi/2 \rfloor$.
3. **Cota de información:** $n+1$ huecos exigen $n+1$ hojas en un árbol binario, así que $h \ge \lceil \log_2(n+1) \rceil$. Las dos cantidades coinciden y la búsqueda binaria es óptima. Con $n = 7$: $8$ huecos y $3$ comparaciones.

## Referencias

- Conferencia 3, §1: correctitud parcial, terminación, invariante y potencial.
- Conferencia 5, §2: árboles de decisión.
- Conferencia 5, §3: Lema 1 (hojas de un árbol binario) y Lema 4 (huecos).
