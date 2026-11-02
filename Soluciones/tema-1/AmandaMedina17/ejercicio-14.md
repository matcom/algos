## Definición formal del problema
Dado un conjunto $I={ I1, I2, ..., In}$ de $n$ intervalos cerrados en la recta real $\mathbb{R}$, donde cada intervalo $I_i=[l_i,r_i]$ con $l_i<=r_i$ tiene asociado un peso real positivo $w_i > 0$.
* Función de peso acumulado: Se define $W: \mathbb{R} \to \mathbb{R}_{\ge 0}$ como:

$$
W(x) = \sum_{i : x \in I_i} w_i = \sum_{i : l_i \le x \le r_i} w_i
$$

* Objetivo: Encontrar un punto óptimo $x^*$ que pertenece a $\mathbb{R}$ que maximice la función de peso acumulado:

$$
W(x^*) = \max_{x \in \mathbb{R}} W(x)
$$

## Modelo de computación
* Modelo de árboles de decisión algebraicos: Los extremos de los intervalos $l_i$, $r_i$ y sus pesos $w_i$ son números reales. Las decisiones del algoritmo se basan en comparaciones binarias algebraicas de orden  $(ej. x_i < x_j)$.
* Modelo Word RAM: Si los puntos provienen de un dominio discreto acotado, las operaciones aritméticas y accesos a memoria toman $O(1)$ por palabra de memoria de tamaño $w>= logn$ bits.

## Diseño de algoritmo
La función $W(x)$ es una función constante a trozos. Sus únicos puntos de discontinuidad ocurren estrictamente en las coordenadas de los extremos de los intervalo: $E={l_1, r_1, l_2, r_2, ..., l_n, r_n}$.
Definamos dos tipos de eventos:
1. Evento de inicio (start): Ocurre en $x=l_i$, suma un peso de $+w_i$.
2. Evento de Fin (end): Ocurre en x = ri, resta un peso de $-w_i$.

Entonces, en lugar de evaluar infinitos puntos en la recta real, reducimos el problema al conjunto discreto de $2n$ eventos de cambio de estado, ordenándolos sobre la recta real y simulando el movimiento de una "linea horizontal de barrido" de izquierda a derecha:
* Al cruzar el inicio de un intervalo $(l_i)$, sumamos un peso $+w_i$ al acumulado actual.
* Al cruzar el fin de un intervalo $(r_i)$ restamos su peso $-w_i$ al acumulado actual.
* Mantenemos un registro en todo momento del valor máximo observado y la coordenada donde ocurre.

### Estructura de datos de los eventos
Cada evento en el sistema se representa como una tupla con la siguiente estructura: Evento = $(x, tipo, peso)$
* $x$ pertenece a $\mathbb{R}$: La coordenada  en la recta real donde ocurre el evento ($l_i$ o $r_i$).
* tipo pertenece a { $start$ , $end$ }: Identifica si el intervalo se abre o se cierra.
* peso pertenece a $\text{peso} \in \mathbb{R}^+$: EL peso positivo $w_i$ asociado al intervalo $i$.

### Criterio de ordenamiento de eventos
Para ordenar los $2n$ eventos se define una relación de orden total:
1. Primer criterio (coordenada $x$): Los eventos se procesan estrictamente de menor a mayor coordenada $x$.
2. Segundo criterio (desempate en la misma $x$): Si un evento de inicio y un evento de fin coinciden exactamente en la misma coordenada $x$ (por ejemplo $l_i$ = $r_j$), el evento de inicio debe procesarse primero. como los intervalos son cerrados, en el punto de coincidencia $x$, ambos intervalos cubren el punto, por lo que el peso de ambos debe sumarse antes de cerrar el intervalo anterior.

**Implementación en el archivo: max_weighted_interval_overlap.py**


## Demostración de correctitud por invariante de ciclo
Definición del invariante $I(k)$:
Al finalizar la iteración $k$ del bucle for, se cumplen las tres condiciones siguientes:
1. Consistencia local: `W_current` es exactamente igual al peso acumulado $`W(e_k*x_{val})`$ de todos los intervalo que cubren el punto $`e_k*x_{val}`$.
2. optimalidad parcial: `W_max` contiene el valor máximo de $W(x)$ evaluado en el subconjunto de eventos procesados hasta el momento.
3. Punto óptimo: `x_opt` almacena la coordenada del punto donde se registró por primera vez dicho valor máximo `W_max`.

**Prueba de correctitud por inducción**
* Caso base: El peso actual es 0, el peso máximo encontrado es 0, no hay aún punto óptimo. El invariante se cumple trivialmente.
* Paso inductivo: Asumimos que $I(k-1)$ es cierto, demostremos $I(k)$:
Sea $e_k = (x_k, tipo_k, peso_k)$ el $k$-ésimo evento procesado.
    - Si $tipo_k == start$, acaba de entrar al intervalo $I_i$. Por definición de $W(x)$, la cobertura total aumenta en $+w_i$. Al peso actual se le suma $w_i$, manteniendo la condición 1.
    - Si $tipo_k == end$, acaba de salir del intervalo $I_i$. La cobertura disminuye en $-w_i$. Al peso actual se le resta $w_i$, manteniendo la condición 1.
    - Si el peso actual es mayor que el peso máximo registrado hasta el momento, se actualiza el peso máximo y el punto óptimo igual a $x_k$. Por hipótesis de inducción, el peso máximo nuevo va a ser el máximo entre el peso máximo anterior y el peso actual, lo que satisface la condición 2 y 3.
* Terminación ($k=2n$): El algoritmo ha procesado todos los puntos de discontinuidad de $W(x)$. Como $W(x)$ es constante en los intervalos abiertos entre eventos consecutivos, el máximo global de $W(x)$ sobre $\mathbb{R}$ ocurre necesariamente en al menos uno de los puntos del conjunto de eventos $E$. Por $I(2n)$, el peso máximo registrado contiene el máximo global absoluto y el punto óptimo es su ubicación. 

## Análisis de costes
Analicemos la complejidad del algoritmo descomponiendo sus fases:
1. Fase de generación de eventos: Se insertan $2n$ eventos en la lista $E$. Costo temporal: $\Theta(n)$.
2. Fase de ordenamiento: Se ordena una lista de tamaño $2n$. Costo temporal: $O(nlogn)$.
3. Fase de barrido lineal: Un bucle que itera $2n$ veces, donde en cada iteración se ejecutan operaciones en tiempo $O(1)$. Coste temporal: $\Theta(n)$.

## Método del potencial
Definición de la función de potencial: Sea $\Phi_t$, el peso acumulado del conjunto de intervalos activos $A_t$ en la iteración t:

$$
\Phi_t = \sum_{I_i \in A_t} w_i
$$

* Estado inicial: Antes de iniciar el barrido $(t=0)$, $A_0 = \emptyset \implies \Phi_0 = 0$.
* Como todos los pesos son mayor que 0, la función de potencial es no negativa para todo $t$.
* Costo amortizado por evento ($c_t^{\text{amortized}}$):
El costo real $c_t$ de procesar un evento en el bucle es $O(1)$. La variación del potencial al procesar el evento $t$ es:
($c_t^{\text{amortized}}$)
Suma Telescópica del Costo Total del Barrido:

$$
\sum_{t=1}^{2n} c_t = \sum_{t=1}^{2n} \left( c_t^{\text{amortized}} - \Phi_t + \Phi_{t-1} \right) = \sum_{t=1}^{2n} c_t^{\text{amortized}} + \Phi_0 - \Phi_{2n}
$$

Como al finalizar el barrido todos los intervalos han cerrado ($A_{2n} = \emptyset$), tenemos $\Phi_{2n} = 0$. Por lo tanto:

$$
\text{Costo real total del barrido} = \sum_{t=1}^{2n} c_t = \sum_{t=1}^{2n} c_t^{\text{amortized}} = \Theta(n)
$$

## Cota inferior del algoritmo
Para determinar el límite teórico fundamental en el modelo basado en comparaciones, demostraremos que este problema requiere al menos  $\Omega(n \log n)$ comparaciones mediante una reducción desde el problema de ordenamiento.

* Teorema de reducción: El problema de ordenamiento de $n$ números reales se reduce en tiempo lineal $O(n)$ al problema de la intersección máxima de intervalos con peso.

* Construcción de la reducción: Para cada elemento $x_i$ que pertenece a $X$, creamos  un intervalo $I_i= [e_i, M]$, donde $M > max(X)$. Asignamos a cada intervalo peso $w_i =1$.

* Análisis del comportamiento de $W(x)$:
A medida que un punto de prueba $x$ avanza de izquierda a derecha en la recta real:
    - Al cruzar a la derecha de un punto $x_i$, el intervalo $[x_i,M]$ comienza a cubrir a $x$, por lo que la función $W(x)$ se incrementa en 1.
    - El valor de $W(x)$ en cualquier punto $x$ es exactamente igual al número de elementos $x_i <= x$.

* Los puntos críticos donde $W(x)$ cambia de valor corresponden exactamente a los elementos del conjunto $X$ en orden ascendente. Un algoritmo que resuelve la estructura completa de la función $W(x)$ debe identificar la secuencia ordenada de todos los eventos de cambio de peso.

### Aplicación de árboles de decisión y Ben-Or
* El espacio de permutaciones de los $n$ números en $n!$.
* Cualquier árbol de decisión binario que resuelva la función $W(x)$ debe ser capaz de distinguir entre las $n!$ hojas posibles correspondientes a cada permutación del orden de los extremos $l_i$.
* La altura $h$ del árbol de decisión cumple:
$$2^h \ge n! \implies h \ge \log_2(n!) = \sum_{i=1}^{n} \log_2 i = \Theta(n \log n)$$
**Cota inferior estricta demostrada:** $$\mathcal{C}_{\text{lower}} = \Omega(n \log n)$$

## Coincidencia de cotas
Cota superior obtenida: $\mathcal{O}(n \log n)$
Cota inferior del árbol de decisión:  $\Omega(n \log n)$
Por tanto, el algoritmo en 

$$
\mathcal{C}_{\text{upper}} = \mathcal{C}_{\text{lower}} = \Theta(n \log n)
$$

El algoritmo es óptimo en el modelo de árboles de decisión algebraicos basados en comparaciones.

## Rompimiento del modelo
La cota $\Omega(n \log n)$ solo es irrompible si el algoritmo se restringe al modelo de compraraciones algebraicas. Podemos romper esta cota cambiando al Modelo Word Ram con claves discretas.
* Supongamos que las coordenadas de los extremos $l_i$, $r_i$ son números enteros dentro de un rango acotado $U = {1, 2,..., K}$, o pueden ser representados mediante enteros de $w$ bits $(w>=logn)$.
* En el algoritmo, en lugar de utilizar un ordenamiento basado en comparaciones $`(O(n \log n))`$, ordenamos la lista $E$ de $2n$ eventos utilizando Counting Sort.
* Nuevo costo computacional:
    - Generación de eventos: $\Theta(n)$.
    - Ordenamiento con Counting Sort: $O(n+K)$.
    - Barrido lineal: $\Theta(n)$.
    - Costo total en Word RAM: $O(n)$.
