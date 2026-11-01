**Problema:** Gale-Shapley con listas incompletas: cada proponente lista solo a algunos receptores, y prefiere quedarse solo antes que con uno que no listó. Adapta el algoritmo, su potencial y la definición de pareja bloqueante. ¿Sigue siendo estable el resultado? Demuéstralo.

En el modelo clásico de Gale-Shapley, las listas de preferencia son completas y estrictas. Sin embargo, en un entorno con listas incompletas, los participantes (proponentes $m \in M$ y receptores $w \in W$) solo incluyen en sus listas a aquellos candidatos que consideran aceptables.

Esto incluye entonces, la opción de 'estar libre': un participante prefiere no estar emparejado antes que asociarse con un candidato fuera de su lista de aceptables.

## Adaptación del Algoritmo:
Sea $L(m)$ la lista ordenada de receptores aceptables para el oponente $m$, y $L(w)$ la lista ordenada de proponentes aceptables para el receptor $w$.

### 1. Inicialización: 
Todos los proponentes $m \in M$ y receptores $w \in W$ están libres. La asignación inicial es $M_{atch} = \emptyset$.
### 2. Ciclo de propuestas:
Mientras existe un proponente $m$ libre que aún tenga receptores no contactados en su lista de aceptables $L(m)$:
* $m$ elige al receptor $w \in L(m)$ de mayor preferencia al que aún no le haya propuesto.
* $w$ evalúa la propuesta recibida de $m$:
    - Caso de aceptación directa: Si $w$ está libre y $m \in L(w)$ ($m$ es aceptable para $w$), $w$ acepta temporalmente a $m$.
    - Caso de reemplazo/mejora: Si $w$ está actualmente emparejada con un $m'$, pero $m \in L(w)$ y $w$ prefiere estrictamente a $m$ sobre ese $m'$ (según $L(w)$), $w$ acepta a $m$ y libera a $m'$(quien vuelve a estar libre).
    - Caso de rechazo: En cualquier otro caso (si $m \notin L(w)$, o si $w$ prefiere a su pareja actual $m'$ sobre $m$), $w$ rechaza a $m$.
### 3. Terminación: 
El algoritmo finaliza cuando ningún proponente libre puede realizar más propuestas.

## Adaptación de la definición de pareja bloqueante
Un apareamiento de $M_{atch}$ es inestable si contiene alguna pareja bloqueante. En el modelo con listas incompletas, una pareja $(m,w)$ bloquea la asignacion $M_{atch}$ si y solo si se cumplen a la vez las siguiente condiciones:
* $m$ prefiere estrictamente a $w$ por encima de su pareja asignada $M_{atch}(m)$, o $m$ está libre en $M_{atch}$ y $w \in L(m)$ (prefiere a $w$ sobre estar libre).
* $w$ prefiere estrictamente a $m$ por encima de su pareja asignada $M_{atch}(w)$, o w está libre en $M_{atch}$ y $m \in L(w)$ (prefiere a $m$ sobre estar libre).
Si no existe ninguna pareja bloqueante y nadie está asignado a una pareja inaceptable, el apareamiento es estable.

## Terminación mediante Función de Potencial:
* Definición de la Función Potencial: Sea $\Phi$ la cantidad total de pares $(m,w)$ tales que $w \in L(m)$ y $m$ aún no ha propuesto a $w$.
* Dado que las listas de preferencia de todos los proponentes son finitas, el valor inicial del potencial es $\sum_{m \in M} \vert{}L(m)\vert{}$. Además, como representa un conteo entero, $\Phi$ está acotado inferiormente de forma estricta por cero.
* En cada iteración del ciclo $While$, exactamente un proponente libre $m$ realiza una propuesta a un receptor $w$ de su lista al que jamás le había propuesto. Esto elimina de forma irreversible a $w$ de sus candidatos pendientes por lo que en cada paso $\Phi$ decrece en 1.
* Como $\Phi$ es una secuencia de enteros no negativos estrictamente decreciente, el algoritmo garantiza su terminación en un máximo de $\sum_{m \in M} \vert{}L(m)\vert{}$ pasos.

## Demostración de estabilidad del apareamiento resultante:
Supongamos, por contradicción, que el apareamiento final $M_{atch}$ no es estable. Esto implica la existencia de al menos una pareja bloqueante $(m,w)$.

Por la definición adaptada de pareja bloqueante:
* $w \in L(m)$ y $m$ prefiere a $w$ sobre su pareja asignada $M_{atch}(m)$ (o sobre estar libre).
* $m \in L(w)$ y $w$ prefiere a $m$ sobre su pareja asignada $M_{atch}(w)$ (o sobre estar libre). 

Como los proponentes recorren su lista $L(m)$ en orden de preferencia estricta de mayor a menor, y $m$ prefiere a $w$ por encima de su resultado final $M_{atch}(m)$ (o terminó libre habiendo preferido a $w$), el proponente $m$ tuvo que haberle propuesto a $w$ obligatoriamente en alguna iteración previa del algoritmo. 
Si $m$ le propuso a $w$, se presentaron únicamente dos situaciones durante la ejecución:
* $w$ rechazó a $m$ inmediatamente en el momento de la propuesta.
* $w$ aceptó a $m$ temporalmente, pero lo abandonó más adelante al recibir una propuesta mejor de un proponente $m'$.

En la dinámica del algoritmo, el bienestar de un receptor $w$ crece de forma monótona a lo largo del tiempo pues $w$ solo cambia de pareja si el nuevo proponente es más preferido según $L(w)$. Por tanto, al finalizar el algoritmo, $w$ estará emparejada con un candidato $M_{atch}(w)$ al cual considera al menos tan preferible como cualquiera que le haya propuesto en el pasado.

Como $m$ le propuso a $w$ y fue rechazado, la monotonía de $w$ garantiza que $w$ prefiere a su pareja final $M_{atch}(w)$ por encima de $m$. Esto contradice la hipótesis de que $(m,w)$ es una pareja bloqueante. Por tanto, no pueden existir parejas bloqueantes, demostrando que el resultado del algoritmo adaptado sigue siendo estrictamente estable.