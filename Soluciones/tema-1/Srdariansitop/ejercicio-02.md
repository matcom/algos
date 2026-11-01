# Pregunta 2: 

Da el invariante y el potencial de la búsqueda binaria, y la cota de información que la hace óptima.

Planteamiento. Sea $A[0..n-1]$ un arreglo ordenado de forma no decreciente y $x$ el valor buscado. Usamos la versión con intervalo semiabierto $[lo, hi)$:
```lo ← 0; hi ← n
mientras lo < hi:
    m ← ⌊(lo + hi)/2⌋
    si A[m] < x:  lo ← m + 1
    sino:         hi ← m
devolver lo        // primer índice con A[lo] ≥ x (o n si no existe)

```
### 1. El invariante
Invariante $I$: en toda evaluación de la guarda del bucle se cumple
$$I:\quad 0\le lo\le hi\le n ;;\wedge;; \forall i<lo:\ A[i]<x ;;\wedge;; \forall i\ge hi:\ A[i]\ge x.$$
Es decir, todo lo que queda a la izquierda de $lo$ es estrictamente menor que $x$, y todo lo que está desde $hi$ es mayor o igual. La respuesta, el primer índice con $A[i]\ge x$, está siempre en $[lo, hi]$.
Demostración (por inducción sobre las iteraciones).
Inicialización. Con $lo=0$, $hi=n$ las condiciones sobre $i<0$ e $i\ge n$ son vacías, y $0\le 0\le n\le n$.
Conservación. Supongamos $I$ y $lo<hi$. Entonces $m=\lfloor(lo+hi)/2\rfloor$ cumple $lo\le m<hi$ (porque $lo<hi$ implica $lo\le \frac{lo+hi}{2}<hi$ y $lo,hi$ enteros, así que $lo \le m \le hi-1$). Por tanto $A[m]$ es un acceso válido. Dos casos:
- $A[m]<x$: como $A$ es ordenado, para todo $i\le m$ se tiene $A[i]\le A[m]<x$. Con $lo'=m+1$, todo $i<lo'$ cumple $A[i]<x$ (los $i<lo$ por $I$, los $lo\le i\le m$ por monotonía). $hi$ no cambia, y $lo'=m+1\le hi$. Se mantiene $I$.
- $A[m]\ge x$: para todo $i\ge m$, $A[i]\ge A[m]\ge x$. Con $hi'=m$, todo $i\ge hi'$ cumple $A[i]\ge x$, y $lo\le m=hi'$. Se mantiene $I$.
Terminación y corrección. Al salir, $lo\ge hi$; junto con $lo\le hi$ de $I$ resulta $lo=hi$. Entonces $\forall i<lo: A[i]<x$ y $\forall i\ge lo: A[i]\ge x$, de modo que $lo$ es exactamente el primer índice con $A[i]\ge x$. Si $lo<n$ y $A[lo]=x$, $x$ está en el arreglo; en otro caso no está. $\blacksquare$
Nota sobre el desbordamiento: $lo+hi$ puede desbordar en enteros de ancho fijo; se evita con $m=lo+\lfloor(hi-lo)/2\rfloor$, que da el mismo valor.
### 2. El potencial (función de terminación)
Potencial: $\Phi = hi - lo$, el tamaño del intervalo candidato.
Afirmación 1 (decrece estrictamente). En cada iteración $\Phi' \le \lfloor \Phi/2\rfloor$.
Demostración. Sea $k=hi-lo\ge 1$ y $m=lo+\lfloor k/2\rfloor$.
- Si $lo\leftarrow m+1$: $\Phi' = hi-(m+1) = k-\lfloor k/2\rfloor-1=\lceil k/2\rceil-1 \le \lfloor k/2\rfloor$.
- Si $hi\leftarrow m$: $\Phi' = m-lo=\lfloor k/2\rfloor$.
En ambos casos $\Phi'\le\lfloor k/2\rfloor<k$ (pues $k\ge1$). $\blacksquare$
Afirmación 2 (número de iteraciones). Como $\Phi_0=n$ y $\Phi_{t+1}\le\lfloor\Phi_t/2\rfloor$, por inducción $\Phi_t\le\lfloor n/2^t\rfloor$. El bucle continúa mientras $\Phi_t\ge1$, es decir, mientras $\lfloor n/2^t\rfloor\ge1\iff 2^t\le n\iff t\le\lfloor\log_2 n\rfloor$. Luego el número de iteraciones es a lo sumo
$$\boxed{\lfloor \log_2 n\rfloor + 1 = \lceil\log_2(n+1)\rceil}$$
(la igualdad entre ambas formas es un hecho aritmético estándar: $\lfloor\log_2 n\rfloor+1=\lceil\log_2(n+1)\rceil$ para $n\ge1$).
Como $\Phi\in\mathbb{N}$ decrece estrictamente y está acotado inferiormente por 0, el algoritmo termina. Junto con el invariante, queda probada la corrección total. $\blacksquare$
### 3. La cota de información (optimalidad)
Modelo. Algoritmos que acceden a los datos solo mediante comparaciones entre $x$ y elementos de $A$. Cada comparación $A[i]$ vs $x$ tiene a lo sumo 2 resultados útiles ($<$ o $\ge$). Cualquier algoritmo determinista es entonces un árbol de decisión binario: nodos internos = comparaciones, hojas = respuestas.
Teorema. Todo algoritmo de búsqueda basado en comparaciones sobre un arreglo ordenado de $n$ elementos requiere, en el peor caso, al menos $\lceil\log_2(n+1)\rceil$ comparaciones.
Demostración.
(a) Número de respuestas distintas. Para el problema "primer índice con $A[i]\ge x$" las salidas posibles son ${0,1,\dots,n}$, es decir, $n+1$ respuestas distintas. Todas son alcanzables: para cada $j$ existe una entrada $x$ que da respuesta $j$ (p. ej. con valores enteros distintos, $x=A[j]$ para $j<n$ y $x>A[n-1]$ para $j=n$). Por tanto el árbol de decisión debe tener al menos $n+1$ hojas distintas (dos entradas con respuestas distintas no pueden terminar en la misma hoja, pues el algoritmo daría la misma salida).
(b) Un árbol binario de altura $h$ tiene a lo sumo $2^h$ hojas. Por inducción en $h$: con $h=0$ hay 1 hoja ($=2^0$); un árbol de altura $h$ tiene raíz con dos subárboles de altura $\le h-1$, con a lo sumo $2\cdot2^{h-1}=2^h$ hojas en total.
(c) Combinación. Si $h$ es el número máximo de comparaciones (altura del árbol):
$$n+1\le 2^h\ \Longrightarrow\ h\ge\log_2(n+1)\ \Longrightarrow\ h\ge\lceil\log_2(n+1)\rceil.\ \blacksquare$$
Versión en términos de información. Hay $n+1$ resultados equiprobables en el peor caso, lo que requiere $\log_2(n+1)$ bits de información; cada comparación aporta como máximo 1 bit (dos resultados posibles). De ahí la cota.
Conclusión de optimalidad. La búsqueda binaria realiza a lo sumo $\lceil\log_2(n+1)\rceil$ comparaciones de tipo $A[m]<x$ (Afirmación 2), y ningún algoritmo basado en comparaciones puede hacerlo mejor en el peor caso (Teorema). Las cotas coinciden exactamente, así que la búsqueda binaria es óptima, no solo asintóticamente sino en la constante: $\Theta(\log n)$ con constante 1 en el peor caso.

### 4. Visualización experimental y simulación 

Para complementar el análisis teórico anterior y verificar de manera empírica el comportamiento del algoritmo, en la carpeta `extra02` se incluye el código fuente completo en Python que automatiza la generación de cuatro recursos gráficos clave. Este material visual permite comprobar la evolución del invariante, la reducción del potencial en tiempo real y la correspondencia exacta entre la teoría de la información y la ejecución práctica de la búsqueda binaria.

En primer lugar, el script genera la **Figura 1** (`fig1_traza_busqueda_binaria.png`) y un GIF animado como **Figura 2** (`fig2_zonas_busqueda_binaria.gif`), los cuales muestran una traza paso a paso sobre un arreglo concreto. En estas visualizaciones se desglosan las zonas delimitadas por los punteros $lo$ y $hi$, evidenciando cómo el tamaño del potencial $\Phi = hi - lo$ disminuye de manera estricta en cada iteración mientras el invariante se mantiene intacto. Esto ilustra de forma gráfica por qué la respuesta correcta siempre se encuentra atrapada dentro del intervalo activo hasta converger en un único punto donde $lo = hi = \text{RESP}$.

Por otro lado, el código construye analíticamente los árboles de decisión reales para tamaños pequeños y medianos de arreglo, generando la **Figura 3** (`fig3_arbol_decision.png`). Esta representación muestra los casos para $n=3$ y $n=10$, destacando cómo cada nodo interno corresponde a una comparación binaria y cada hoja representa una posible respuesta indexada, resaltando además el camino crítico seguido para un valor de búsqueda específico.

Finalmente, la **Figura 4** (`fig4_cota_informacion.png`) contrasta gráficamente la capacidad de los árboles de altura $h$ (con un límite de $2^h$ hojas) frente al número total de respuestas posibles $n+1$, graficando de forma empírica que la búsqueda binaria alcanza de manera estricta e impecable la cota inferior teórica de $\lceil\log_2(n+1)\rceil$ comparaciones para cualquier $1 \le n \le 64$.