# Problema

## 1. Planteamiento del problema

### 1.1 Problema original

> Dos equipos participantes en el NWERC han planeado una broma sutil para desconcertar a los organizadores. Durante el registro, cuando los organizadores se agachan a buscar una camisa, cada equipo aprovechará para mover una sola pieza de mobiliario en la sala. 
> 
> Como los equipos llegan en momentos distintos y no pueden comunicarse, deben acordar de antemano una estrategia común que aplicarán siempre que se encuentren con una misma distribución de la sala. El objetivo es que el equipo que llega más tarde deshaga exactamente lo que hizo el equipo que llegó primero, de modo que al final todo quede como estaba. 
> 
> Para lograrlo, la estrategia debe ser una función determinista e involutiva que transforme cualquier disposición válida de los muebles en otra, moviendo exactamente una pieza de una celda ocupada (`#`) a una celda vacía (`.`), de manera que aplicar la estrategia dos veces consecutivas recupere la configuración original. 
> 
> Dado que para algunas combinaciones de tamaño de la sala y cantidad de muebles esto resulta imposible, intentarlo en esos casos sería demasiado arriesgado.
> 
> ### Entrada y Salida
> 
> * **Entrada:** Se recibe el número de casos de prueba. Para cada caso, se especifican las dimensiones de la sala ($h$ y $w$), la cantidad de piezas de mobiliario ($k$) y una cuadrícula con el estado actual del lugar (`.` para espacios vacíos y `#` para los muebles). Es un problema interactivo de múltiples pasadas.
> * **Salida:** Imprime `risky` si no existe una estrategia válida que funcione para cualquier distribución posible. En caso contrario, especifica el movimiento indicando primero las coordenadas de origen (fila y columna) de la pieza que se mueve y luego las coordenadas de su destino.

### 1.2. Reducción del problema

Sea $n=h\cdot w$ la cantidad total de celdas de la cuadrícula y $k$ la cantidad de objetos. Podemos representar cada configuración mediante una cadena binaria de longitud $n$, donde cada posición indica si la celda correspondiente está ocupada o vacía.

Por tanto, el conjunto de configuraciones posibles está formado por todas las cadenas binarias de longitud $n$ que contienen exactamente $k$ bits iguales a uno. Denotaremos este conjunto por $S_{n,k}$.

Su cardinalidad es:

$$\vert{}S_{n,k}\vert{}=\binom nk$$

El objetivo consiste en construir una función determinista

$$f:S_{n,k}\longrightarrow S_{n,k}$$

que cumpla las siguientes propiedades:

1. Para toda configuración $x$, las configuraciones $x$ y $f(x)$ deben diferir exactamente en dos posiciones: una ocupada en $x$ y vacía en $f(x)$, y otra vacía en $x$ y ocupada en $f(x)$.
2. La función debe ser involutiva, es decir:

$$f(f(x))=x$$

De esta manera, aplicar la estrategia dos veces consecutivas garantiza que se recupera la configuración inicial.

# Solución

## 2. Diseño del algoritmo

### 2.1. Construcción de un orden de las configuraciones

La idea consiste en construir un orden de todas las cadenas binarias de longitud $n$ que contienen exactamente $k$ unos, de manera que dos cadenas consecutivas difieran exactamente en dos posiciones.

Para ello, definimos recursivamente una secuencia $H(n,k)$.

Los casos base son:

$$H(n,0)=[0^n]$$

$$H(n,n)=[1^n]$$

Para los demás casos, dividimos las cadenas según su primer bit:

* Las que comienzan con cero tienen exactamente $k$ unos en las $n-1$ posiciones restantes.
* Las que comienzan con uno tienen exactamente $k-1$ unos en las posiciones restantes.

Definimos entonces:

$$\boxed{H(n,k) = 0H(n-1,k) + 1\operatorname{rev}(H(n-1,k-1))}$$

donde:

* $0H(n-1,k)$ representa la secuencia obtenida anteponiendo un cero a cada elemento de $H(n-1,k)$.
* $1\operatorname{rev}(H(n-1,k-1))$ representa la secuencia obtenida anteponiendo un uno a cada elemento de la secuencia $H(n-1,k-1)$, recorriéndola en orden inverso.
* El signo $+$ representa la concatenación de ambas secuencias.

La inversión del segundo bloque es fundamental para garantizar la propiedad que necesitamos.

### 2.2. Propiedades de la construcción

La secuencia $H(n,k)$ contiene exactamente una vez cada cadena binaria de longitud $n$ con $k$ unos.

Esto se demuestra directamente por inducción, ya que las cadenas se dividen en dos grupos disjuntos según su primer bit, y cada grupo se construye recursivamente.

Además, dos elementos consecutivos de $H(n,k)$ difieren exactamente en dos posiciones.

Dentro de cada bloque, esta propiedad se mantiene por hipótesis de inducción, puesto que todos sus elementos comparten el mismo primer bit.

Solo queda demostrar que también se cumple entre el último elemento del primer bloque y el primero del segundo.

Para ello, observemos que el primer elemento de la secuencia es:

$$F(n,k)=0^{n-k}1^k$$

Por otra parte, su último elemento es:

$$L(n,k)=10^{n-k}1^{k-1}, \qquad k\geq 1$$

Estos resultados se obtienen directamente de la definición recursiva.

El último elemento del primer bloque y el primero del segundo son, respectivamente:

$$u=0L(n-1,k)$$

$$v=1L(n-1,k-1)$$

Si $k=1$, estos elementos son:

$$u=010^{n-2},\qquad v=10^{n-1}$$

que difieren únicamente en sus dos primeras posiciones.

Para $k\geq 2$, tenemos:

$$u=010^{n-k-1}1^{k-1}$$

$$v=110^{n-k}1^{k-2}$$

Ambas cadenas difieren en su primera posición y en exactamente una posición adicional, correspondiente al desplazamiento de la frontera entre los bloques de ceros y unos. Por tanto, su distancia de Hamming es exactamente dos.

Así, por inducción, cualquier par de elementos consecutivos de $H(n,k)$ difiere exactamente en dos posiciones.

### 2.3. Construcción de la estrategia

Una vez obtenido este orden, podemos emparejar sus elementos consecutivos:

$$(H_0,H_1),\ (H_2,H_3),\ldots$$

donde $H_i$ representa el elemento situado en la posición $i$, utilizando índices desde cero.

Cada pareja está formada por dos configuraciones que difieren exactamente en dos posiciones. Por tanto, pasar de una a otra equivale a trasladar un objeto desde una celda ocupada hasta una celda vacía.

La estrategia consiste en que, dada una configuración $x=H_i$, se devuelva la configuración correspondiente a:

$$\boxed{H_{i\oplus 1}}$$

donde $\oplus$ representa el XOR binario.

Esta operación intercambia los índices consecutivos de cada pareja: si $i$ es par, selecciona $i+1$; si es impar, selecciona $i-1$.

Por consiguiente, aplicar la estrategia dos veces devuelve siempre la configuración original.

### 2.4. Determinación de cuándo existe una estrategia

Para poder emparejar todos los elementos de la secuencia, su cardinalidad debe ser par.

Si $\binom nk$ es impar, resulta imposible construir una función involutiva sin puntos fijos sobre $S_{n,k}$, pues una función de estas características divide necesariamente el conjunto en parejas disjuntas.

Por tanto:

$$\boxed{\text{Existe una estrategia}\iff \binom nk \equiv 0\pmod 2}$$

Esto resuelve la condición de existencia del problema.

Además, mediante el teorema de Lucas, podemos determinar la paridad del coeficiente binomial utilizando:

$$\binom nk \text{ es impar} \iff (k\ \&\ (n-k))=0$$

donde $\&$ representa el AND a nivel de bits.

En consecuencia, si esta condición se cumple, la respuesta es `risky`.

## 3. Demostración de correctitud

Demostraremos que el algoritmo proporciona una estrategia válida siempre que exista.

**Lema 1.** La secuencia $H(n,k)$ contiene exactamente una vez cada cadena binaria de longitud $n$ con exactamente $k$ unos.

*Demostración.*

Para $k=0$ y $k=n$, la propiedad se cumple trivialmente.

En los demás casos, dividimos las cadenas según su primer bit. Si este es cero, el sufijo contiene $k$ unos; si es uno, contiene $k-1$ unos.

Ambos grupos son disjuntos y, por hipótesis de inducción, sus respectivas secuencias contienen exactamente una vez todas las posibilidades correspondientes. Por tanto, su concatenación contiene exactamente una vez cada cadena válida. $\square$

**Lema 2.** Dos elementos consecutivos de $H(n,k)$ difieren exactamente en dos posiciones.

*Demostración.*

Para los casos base la propiedad es trivial, pues las secuencias contienen un único elemento.

Supongamos que se cumple para las secuencias de longitud $n-1$. Dentro de cada bloque, la propiedad se conserva por hipótesis de inducción, ya que todos los elementos tienen el mismo primer bit.

En la frontera entre ambos bloques, los elementos involucrados son $0L(n-1,k)$ y $1L(n-1,k-1)$. Como se demostró anteriormente, estas cadenas difieren exactamente en dos posiciones.

Por tanto, la propiedad se cumple para toda la secuencia $H(n,k)$. $\square$

**Teorema.** Si $\binom nk$ es par, la estrategia construida garantiza que aplicar dos movimientos consecutivos devuelve la configuración inicial.

*Demostración.*

Por el lema 1, toda configuración válida aparece exactamente una vez en $H(n,k)$. Como su cardinalidad es par, podemos dividir la secuencia en parejas de elementos consecutivos.

Por el lema 2, los elementos de cada pareja difieren exactamente en dos posiciones. Como ambos tienen la misma cantidad de unos, una de esas posiciones cambia de uno a cero y la otra de cero a uno. Esto representa exactamente el traslado de un objeto a una celda vacía.

La estrategia asigna a cada elemento de una pareja el otro elemento de esa misma pareja. Por tanto, al aplicar nuevamente la estrategia, se recupera el elemento original.

Así, para cualquier configuración válida $x$:

$$f(f(x))=x$$

La estrategia es, por tanto, válida para todas las configuraciones posibles. $\square$

Por otra parte, si $\binom nk$ es impar, no existe una estrategia válida, ya que el conjunto de configuraciones no puede dividirse en parejas disjuntas. Esto demuestra también la necesidad de la condición de existencia.

## 4. Pseudocódigo y complejidad computacional

Aunque la construcción anterior define la estrategia mediante una posición dentro de una secuencia, no es necesario generar toda la secuencia ni calcular explícitamente el índice completo de cada configuración.

Podemos calcular únicamente la paridad del índice mediante una recurrencia y obtener el elemento anterior o siguiente de la secuencia utilizando su propia definición recursiva.

Esto permite implementar la estrategia en tiempo lineal.

### 4.1. Cálculo de la paridad del índice

Sea $R(x,n,k)$ la posición de una configuración $x$ dentro de $H(n,k)$, empezando desde cero.

Por la definición de la secuencia:

$$R(x,n,k)= \begin{cases} R(s,n-1,k), & x_1=0,\\ \binom nk-1-R(s,n-1,k-1), & x_1=1, \end{cases}$$

donde $s$ es el sufijo de $x$ después de eliminar su primer bit.

Solo necesitamos conocer $R(x,n,k)\bmod 2$. Definimos $P(x,n,k)$ como esa paridad:

$$P(x,n,k)= \begin{cases} 0, & k=0\text{ o }k=n,\\ P(s,n-1,k), & x_1=0,\\ P(s,n-1,k-1)\oplus E(n,k), & x_1=1, \end{cases}$$

donde:

$$E(n,k)= \begin{cases} 1, & \binom nk \text{ es par},\\ 0, & \binom nk \text{ es impar}. \end{cases}$$

Como la paridad del coeficiente binomial se calcula mediante una operación AND, cada nivel de la recurrencia requiere tiempo constante. Por tanto, calcular $P$ cuesta $O(n)$.

### 4.2. Obtención del elemento anterior o siguiente

Definiremos dos procedimientos recursivos:

* `NEXT`: encuentra el elemento siguiente de una configuración dentro de $H(n,k)$.
* `PREV`: encuentra el elemento anterior.

Para implementarlos eficientemente, necesitamos reconocer los extremos de las secuencias recursivas.

Recordemos que:

$$F(n,k)=0^{n-k}1^k$$

es el primer elemento, mientras que:

$$L(n,k)= \begin{cases} 0^n, & k=0,\\ 10^{n-k}1^{k-1}, & k>0 \end{cases}$$

es el último elemento.

Una cadena de bits que contiene exactamente $k$ unos es el primer elemento de su secuencia si y solo si no contiene la subsecuencia `10`.

Análogamente, es el último elemento si $k=0$, o si comienza con `1` y el resto no contiene la subsecuencia `10`.

Podemos precalcular un arreglo `BAD`, donde `BAD[i]` indica si existe una aparición de `10` en el sufijo que comienza en la posición `i`.

Su cálculo es lineal:

```text
BAD[n] = false

for i = n-1 downto 0:
    BAD[i] = BAD[i+1]

    if i+1 < n and x[i] == 1 and x[i+1] == 0:
        BAD[i] = true

```

De esta manera:

```text
IS_FIRST(i):
    return not BAD[i]


IS_LAST(i, k):
    if k == 0:
        return true

    return x[i] == 1 and not BAD[i+1]

```

Ambas consultas se realizan en tiempo constante.

Para construir el último elemento de una secuencia, utilizamos:

```text
WRITE_LAST(y, i, m, k):
    if k == 0:
        escribir m ceros en y desde i
        return

    y[i] = 1

    escribir m-k ceros en y desde i+1
    escribir k-1 unos en las posiciones restantes

```

Los procedimientos para encontrar el siguiente y el anterior quedan definidos por la estructura recursiva:

```text
NEXT(i, m, k):

    if k == 0 or k == m:
        return false

    if x[i] == 0:

        if IS_LAST(i+1, k):
            y[i] = 1
            WRITE_LAST(y, i+1, m-1, k-1)
            return true

        y[i] = 0
        return NEXT(i+1, m-1, k)

    else:

        if IS_FIRST(i+1):
            return false

        y[i] = 1
        return PREV(i+1, m-1, k-1)

```

```text
PREV(i, m, k):

    if k == 0 or k == m:
        return false

    if x[i] == 0:

        if IS_FIRST(i+1):
            return false

        y[i] = 0
        return PREV(i+1, m-1, k)

    else:

        if IS_LAST(i+1, k-1):
            y[i] = 0
            WRITE_LAST(y, i+1, m-1, k)
            return true

        y[i] = 1
        return NEXT(i+1, m-1, k-1)

```

Estos procedimientos siguen directamente la definición de $H$.

Cuando el primer bit es cero, se trabaja dentro del primer bloque, cuya secuencia conserva el orden original. Cuando es uno, se trabaja dentro del segundo bloque, cuya secuencia está invertida; por eso `NEXT` utiliza `PREV` y viceversa.

Si se alcanza un extremo de un bloque, se pasa al extremo correspondiente del bloque contiguo. Así se obtiene exactamente el elemento anterior o siguiente de la secuencia, sin necesidad de generar los demás.

### 4.3. Algoritmo principal

Una vez definidos los procedimientos anteriores, el algoritmo completo es:

```text
SOLVE(x, n, k):

    if ODD_BINOMIAL(n, k):
        output "risky"
        return

    precalcular BAD

    p = RANK_PARITY(x, 0, n, k)

    if p == 0:
        NEXT(0, n, k)
    else:
        PREV(0, n, k)

    buscar las dos posiciones donde x e y difieren:

        origen     = posición con x[i] = 1 e y[i] = 0
        destino    = posición con x[i] = 0 e y[i] = 1

    convertir ambas posiciones lineales a coordenadas
    output origen y destino

```

Aquí `ODD_BINOMIAL(n,k)` devuelve verdadero exactamente cuando:

$$(k\ \&\ (n-k))=0$$

La función `RANK_PARITY` es la recurrencia definida anteriormente para calcular la paridad del índice.

El procedimiento `NEXT` o `PREV` siempre encontrará el elemento solicitado: si la cardinalidad total es par, el último índice es impar y el primero es par. Por tanto, un elemento de índice par siempre tiene sucesor y uno de índice impar siempre tiene predecesor.

### 4.4. Análisis de complejidad

Sea $n$ la cantidad total de celdas.

El cálculo de `BAD` requiere recorrer una vez la cadena, por lo que cuesta:

$$O(n)$$

El cálculo de la paridad del índice realiza una llamada recursiva por cada posición:

$$O(n)$$

La búsqueda del elemento anterior o siguiente también realiza, como máximo, una llamada por nivel recursivo. Además, la escritura del último sufijo se realiza como máximo una vez y requiere tiempo lineal. Por tanto:

$$O(n)$$

Finalmente, localizar las dos posiciones donde difieren ambas configuraciones requiere otro recorrido lineal:

$$O(n)$$

Sumando todos los costes:

$$T(n)=O(n)+O(n)+O(n)+O(n)=O(n)$$

El espacio auxiliar es $O(n)$, debido al arreglo `BAD`, la configuración resultante y la profundidad de la recursión.

Por tanto:

$$\boxed{T(n)=O(n),\qquad S(n)=O(n)}$$

Este análisis utiliza el modelo Word-RAM, donde las operaciones sobre enteros de tamaño $O(\log n)$ y las operaciones básicas sobre palabras de máquina cuestan $O(1)$. No se calculan coeficientes binomiales completos ni índices de $O(n)$ bits, sino únicamente su paridad.

## 5. Demostración de la cota mínima

Para demostrar que la complejidad obtenida es asintóticamente óptima, debemos establecer que cualquier algoritmo que resuelva el problema necesita al menos $\Omega(n)$ tiempo en el peor caso.

Consideremos instancias en las que existe exactamente un objeto, es decir, $k=1$, y donde $n$ es par.

Estas instancias admiten una estrategia válida, puesto que:

$$\binom n1=n$$

es par.

Sin embargo, para producir una respuesta correcta, el algoritmo debe identificar la posición del único objeto, ya que esa posición debe aparecer como origen del movimiento.

Supongamos que existe un algoritmo que, en el peor caso, inspecciona estrictamente menos de $n-1$ posiciones de la cuadrícula.

Un adversario puede responder que todas las posiciones inspeccionadas están vacías. Como el algoritmo ha inspeccionado menos de $n-1$ posiciones, quedan al menos dos posiciones sin inspeccionar.

El adversario puede situar el único objeto en cualquiera de esas dos posiciones. En particular, puede elegir una posición distinta de la que el algoritmo pretende utilizar como origen.

De esta manera, el algoritmo no puede garantizar que su respuesta identifique correctamente la posición del objeto.

Por tanto, necesariamente debe inspeccionar al menos $n-1$ posiciones en el peor caso:

$$T(n)=\Omega(n)$$

Como anteriormente construimos un algoritmo con complejidad $O(n)$, ambas cotas coinciden:

$$\boxed{T(n)=\Theta(n)}$$

En consecuencia, la solución tiene complejidad temporal asintóticamente óptima.
