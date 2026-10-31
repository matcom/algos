# Ejercicio 2: Invariante y potencial de la búsqueda binaria, y su cota de información

> **Enunciado:** Da el invariante y el potencial de la búsqueda binaria, y la cota de información que la hace óptima.

## 1. Especificación del problema

Antes de escribir invariante o potencial hay que fijar el contrato, como pide la conferencia 3.

**Entrada.** Un arreglo $A[0..n-1]$ ordenado de forma no decreciente ($A[0] \leq A[1] \leq \ldots \leq A[n-1]$) y un valor $x$.

**Salida.**

- Si $x$ está en $A$, una posición $p$ con $A[p] = x$.
- Si $x$ no está, el hueco donde debería insertarse: el único $h \in \{0, 1, \ldots, n\}$ tal que $A[h-1] < x < A[h]$, con las convenciones $A[-1] = -\infty$ y $A[n] = +\infty$.

**Precondición.** $A$ está ordenado. Sobre un arreglo desordenado la búsqueda binaria no es incorrecta: el contrato simplemente no dice nada.

**Modelo.** Comparaciones entre $x$ y elementos de $A$. Cada comparación devuelve $<$, $=$ o $>$. El costo es el número de comparaciones en el peor caso.

**Formulación con el invariante del rango candidato**, que es la versión que se va a analizar:

```python
def busqueda_binaria(A, x):
    lo, hi = 0, len(A)          # el rango candidato es A[lo:hi]
    while lo < hi:
        m = (lo + hi) // 2
        if A[m] == x:
            return ("está", m)
        elif A[m] < x:
            lo = m + 1
        else:
            hi = m
    return ("hueco", lo)
```

## 2. Invariante (correctitud parcial)

## 2.1. El invariante

> En cada iteración del ciclo `while`, si $x$ está en $A$, entonces está en $A[lo:hi]$.

Equivalentemente, y es la forma que se usa en el paso de mantenimiento:

> Todo elemento fuera de $A[lo:hi]$ ya fue descartado: o es menor que $x$, o es mayor que $x$.

## 2.2. Demostración en tres pasos

**Inicialización.** Antes de la primera vuelta, $lo = 0$ y $hi = n$, así que $A[lo:hi] = A[0:n] = A$. Si $x$ está en $A$, trivialmente está en $A[lo:hi]$. ✔

**Mantenimiento.** Supongamos el invariante antes de una vuelta, con $lo < hi$ (condición del ciclo). Sea $m = \lfloor (lo+hi)/2 \rfloor$. Por la definición del rango, $lo \leq m < hi$, así que $A[m]$ está dentro del rango y la comparación es válida. Hay tres casos:

- $A[m] == x$: el algoritmo devuelve `("está", m)`, que es correcto. No hay más vueltas que analizar.

- $A[m] < x$: como $A$ está ordenado, todo $A[i]$ con $i \leq m$ cumple $A[i] \leq A[m] < x$. Ninguno de ellos puede ser $x$. Se puede descartar $A[lo..m]$ entero, y el nuevo rango $A[m+1:hi]$ sigue conteniendo a $x$ si estaba en el rango viejo. El algoritmo hace exactamente $lo = m + 1$. ✔

- $A[m] > x$: simétricamente, todo $A[i]$ con $i \geq m$ cumple $A[i] \geq A[m] > x$, así que se descarta $A[m..hi-1]$. El nuevo rango $A[lo:m]$ sigue conteniendo a $x$ si estaba. El algoritmo hace $hi = m$. ✔

En los dos casos de descarte, el invariante se restablece. ✔

**Conclusión.** Al salir del ciclo, $lo == hi$, así que el rango $A[lo:hi]$ es vacío. Por el invariante, si $x$ estuviera en $A$ estaría en el rango vacío, lo cual es imposible. Por lo tanto $x$ no está en $A$.

Falta ver que $lo$ es el hueco correcto, es decir, que $A[lo-1] < x < A[lo]$ (con las convenciones de los extremos). Esto no lo da el invariante solo: hace falta reforzarlo.

## Invariante reforzado

> **Invariante reforzado.** $A[lo:hi]$ contiene a $x$ si $x \in A$, y además:
> - si $lo > 0$, entonces $A[lo-1] < x$;
> - si $hi < n$, entonces $A[hi] > x$.

**Inicialización.** $lo = 0$ y $hi = n$, así que no hay elementos a la izquierda de $lo$ ni a la derecha de $hi$: las dos cláusulas son vacuamente verdaderas. ✔

**Mantenimiento.** En el caso $A[m] < x$, el nuevo $lo$ es $m+1$. La cláusula izquierda se satisface porque $A[lo-1] = A[m] < x$. La cláusula derecha se hereda del invariante viejo, ya que $hi$ no cambió. En el caso $A[m] > x$, el nuevo $hi$ es $m$, y la cláusula derecha se satisface porque $A[hi] = A[m] > x$; la izquierda se hereda. ✔

**Conclusión.** Al salir, $lo == hi$ y las dos cláusulas dan $A[lo-1] < x < A[lo]$: $lo$ es exactamente el hueco. ✔

Esta es la lección de la conferencia 3: el invariante que uno escribe primero suele ser verdadero pero no inductivo. El invariante "si $x$ está, está en $A[lo:hi]$" no permite concluir que $lo$ es el hueco; hay que reforzarlo con las dos cláusulas sobre los bordes. Sin refuerzo, la demostración no cierra.

## 3. Potencial (terminación)

## 3.1. El potencial

**Potencial.** $\Phi(lo, hi) = hi - lo$, el tamaño del rango candidato.

Es entero, no negativo ($lo \leq hi$ siempre, porque $m < hi$ implica $m+1 \leq hi$, y $m \geq lo$ implica que $hi = m$ deja $hi \geq lo$). Está acotado por arriba por $n$.

## 3.2. Demostración

**Cota inferior.** $\Phi = hi - lo \geq 0$ siempre, porque el rango $[lo, hi)$ es válido. ✔

**Decrecimiento estricto.** En cada vuelta del ciclo se ejecuta una de las dos ramas de descarte (la rama de igualdad no vuelve a iterar). Veamos que en ambas $\Phi$ baja al menos en 1:

- **Rama $lo = m + 1$:** el potencial nuevo es $hi - (m+1)$. La diferencia es

$$\Phi_{\text{viejo}} - \Phi_{\text{nuevo}} = (hi - lo) - (hi - m - 1) = m + 1 - lo.$$

Como $m = \lfloor (lo+hi)/2 \rfloor$ y $lo < hi$, se tiene $m \geq lo$, luego $m + 1 - lo \geq 1$. ✔

- **Rama $hi = m$:** el potencial nuevo es $m - lo$. La diferencia es

$$\Phi_{\text{viejo}} - \Phi_{\text{nuevo}} = (hi - lo) - (m - lo) = hi - m.$$

Como $m = \lfloor (lo+hi)/2 \rfloor < hi$ cuando $lo < hi$, se tiene $hi - m \geq 1$. ✔

**Terminación.** $\Phi$ es un entero no negativo que baja al menos en 1 en cada vuelta. No puede bajar indefinidamente, así que el ciclo ejecuta a lo sumo $\Phi_0 = n$ vueltas y termina. Más aún, el número de vueltas está acotado por el valor inicial del potencial, que es $n$.


## 3.3. La cota exacta por el potencial

El potencial no solo demuestra terminación: da una cota del número de vueltas. Pero la cota $n$ es floja. Para apretarla, se usa un potencial logarítmico:

$$\Psi(lo, hi) = \log_2(hi - lo).$$

En cada vuelta, el rango se parte por la mitad: el nuevo tamaño es a lo sumo $\lceil (hi-lo)/2 \rceil$. Por lo tanto

$$\Psi_{\text{nuevo}} \leq \log_2\!\left(\left\lceil \frac{hi-lo}{2} \right\rceil\right) \leq \log_2(hi-lo) - 1 + \frac{1}{hi-lo} \leq \Psi_{\text{viejo}} - 1 + \frac{1}{hi-lo}.$$

El término $1/(hi-lo)$ molesta, pero es a lo sumo $1/2$ en cuanto el rango tiene tamaño $\geq 2$, y el caso de tamaño $1$ se agota en una vuelta. Contando con cuidado (o simplemente notando que el tamaño se reduce a la mitad en cada vuelta), el número de vueltas es a lo sumo $\lceil \log_2(n+1) \rceil$.


## 4. Cota de información

## 4.1. El árbol de decisión y los huecos

La búsqueda binaria es un algoritmo de comparaciones, así que su ejecución sobre todas las entradas posibles forma un árbol de decisión (conferencia 5, §2). Cada nodo interno es una comparación con tres respuestas ($<$, $=$, $>$), y cada hoja es una salida.

La trampa que menciona la conferencia 5, §3: con tres ramas por nodo, el argumento de información ingenuo daría $\log_3$, que es más débil. La forma correcta de obtener $\log_2$ es mirar solo los casos en que $x$ no está en el arreglo.

**Los huecos.** Si $x \notin A$, entonces $x$ cae en exactamente uno de los $n+1$ huecos:

$$h_0 = (-\infty, A[0]), \quad h_1 = (A[0], A[1]), \quad \ldots, \quad h_n = (A[n-1], +\infty).$$

En esos casos ninguna comparación puede responder $=$, así que el algoritmo solo usa las ramas $<$ y $>$. La parte del árbol que corresponde a $x \notin A$ es un árbol binario.

## 4.2. Lema: huecos distintos exigen hojas distintas

**Lema.** Si $x_1$ y $x_2$ caen en huecos distintos, un algoritmo correcto los lleva a hojas distintas.

**Demostración** (la de la conferencia 5, §3, adaptada). Supongamos que $x_1$ cae en un hueco a la izquierda del de $x_2$, y que ambos terminan en la misma hoja.

- Entre sus huecos hay al menos un elemento $a$ del arreglo, con $x_1 < a < x_2$.
- El algoritmo no comparó con ese $a$. Si lo hubiera hecho, $x_1$ habría recibido $<$ y $x_2$ habría recibido $>$, y habrían seguido caminos distintos.
- Consideremos ahora $x = a$. En cada comparación que el algoritmo hace, con un elemento a la izquierda de ambos huecos o a la derecha, $a$ recibe la misma respuesta que $x_1$ y $x_2$. Así que $x = a$ recorre el mismo camino y llega a la misma hoja.
- En esa hoja el algoritmo dice "no está", porque es la hoja de $x_1$. Pero $a$ sí está. El algoritmo se equivoca.

Contradicción. ∎

## 4.3. El teorema

**Teorema.** Todo algoritmo de comparaciones que busca en un arreglo ordenado de $n$ elementos hace, en el peor caso, al menos

$$\left\lceil \log_2(n+1) \right\rceil \;=\; \left\lfloor \log_2 n \right\rfloor + 1$$

comparaciones.

**Demostración.** Por el lema, los $n+1$ huecos necesitan $n+1$ hojas distintas en la parte binaria del árbol. Por el lema 1 de la conferencia 5 (un árbol binario de altura $h$ tiene a lo sumo $2^h$ hojas), hace falta

$$2^h \geq n+1 \implies h \geq \log_2(n+1).$$

Como $h$ es entero, se concluye $h \geq \lceil \log_2(n+1) \rceil$. La igualdad con $\lfloor \log_2 n \rfloor + 1$ se comprueba así: si $2^k \leq n < 2^{k+1}$, entonces $\lfloor \log_2 n \rfloor = k$, y $2^k < n+1 \leq 2^{k+1}$ da $\lceil \log_2(n+1) \rceil = k+1$. ∎

## 4.4. La búsqueda binaria alcanza la cota

Cada comparación parte el rango candidato por la mitad. Si el rango tiene tamaño $s = hi - lo$, el índice medio es $m = lo + \lfloor s/2 \rfloor$: la rama $A[m] < x$ deja un rango de tamaño $\lceil s/2 \rceil - 1$ y la rama $A[m] > x$ deja uno de tamaño $\lfloor s/2 \rfloor$, así que la peor de las dos deja exactamente $\lfloor s/2 \rfloor$. Sea $f(s)$ el peor número de comparaciones que faltan cuando el rango candidato tiene tamaño $s$ y $x$ todavía no apareció:

$$f(0) = 0, \qquad f(s) = 1 + f(\lfloor s/2 \rfloor) \;\; (s \geq 1).$$

Por inducción, $f(s) = \lfloor \log_2 s \rfloor + 1$: para $s = 1$ da $f(1) = 1$, y al pasar de $s \geq 2$ a $\lfloor s/2 \rfloor$ el piso del logaritmo baja exactamente en 1. Por la identidad del teorema, $\lfloor \log_2 s \rfloor + 1 = \lceil \log_2(s+1) \rceil$. Con $s = n$:

$$\text{peor caso} \;=\; f(n) \;=\; \left\lceil \log_2(n+1) \right\rceil \;=\; \left\lfloor \log_2 n \right\rfloor + 1 \;\; \text{comparaciones.}$$

**Ejemplo con $n = 7$.** Hay 8 huecos, y la búsqueda binaria los separa con 3 comparaciones, que es exactamente $\lceil \log_2 8 \rceil = 3$. El árbol de decisión de la conferencia 5, figura 7, tiene 8 hojas y altura 3: es óptimo.

**Donde el techo se nota ($n = 8$).** Hay 9 huecos y el peor caso es $\lceil \log_2 9 \rceil = 4$: con $x$ en el hueco entre $A[0]$ y $A[1]$, el camino es $A[4], A[2], A[1], A[0]$, cuatro comparaciones. Ni una menos: un árbol binario de altura 3 tiene a lo sumo 8 hojas, y aquí hacen falta 9.

**Conclusión.** La búsqueda binaria es óptima en el modelo de comparaciones: su costo en el peor caso, $\lceil \log_2(n+1) \rceil$, coincide exactamente con la cota inferior. No hay factor de holgura: es óptima con la constante exacta.