## Problema

Considere el algoritmo de Gale-Shapley adaptado al escenario de **listas incompletas**, donde cada proponente lista únicamente a un subconjunto de receptores aceptables, prefiriendo explícitamente quedarse solo antes que emparejarse con alguien omitido de su lista (y viceversa).

1. **Adaptación:** Describa la modificación del algoritmo y de la definición de pareja bloqueante.
2. **Terminación:** Defina la función potencial que demuestra la terminación finita del algoritmo.
3. **Estabilidad:** Enuncie y demuestre formalmente si el resultado sigue siendo estable bajo este esquema.

---

## Solución

### 1. Adaptación del Algoritmo y Definición de Pareja Bloqueante

#### Adaptación del Algoritmo de Gale-Shapley

* **Listas de Preferencia:** Cada proponente $p$ posee una lista ordenada exclusivamente de receptores aceptables. Cualquier receptor ausente de dicha lista se considera inaceptable para $p$ (y de forma recíproca para los receptores respecto a los proponentes).
* **Fase de Propuestas:**
1. Un proponente libre $p$ que aún conserve receptores aceptables en su lista propone al primer receptor de la misma al que no le haya propuesto previamente.
2. Si un proponente agota la totalidad de su lista de aceptables y es rechazado, se retira definitivamente y permanece soltero.


* **Respuesta del Receptor $a$:** Al recibir una propuesta de $p$:
* Si $p$ no figura en la lista de aceptabilidad de $a$, la propuesta es rechazada de inmediato.
* Si $a$ se encuentra libre y encuentra a $p$ aceptable, acepta la propuesta de forma provisional.
* Si $a$ ya está emparejado provisionalmente con $p'$, $a$ acepta a $p$ y rechaza a $p'$ si y solo si $a$ prefiere estrictamente a $p$ por encima de $p'$. De lo contrario, rechaza a $p$.



#### Adaptación de la Definición de Pareja Bloqueante

Una pareja $(p, a)$ constituye un bloque para un emparejamiento final $M$ si y solo si se satisfacen simultáneamente las siguientes condiciones de racionalidad individual y preferencia estricta:

1. $p$ y $a$ no están emparejados entre sí en $M$.
2. **Aceptabilidad mutua:** $a$ figura en la lista de aceptables de $p$, y $p$ figura en la lista de aceptables de $a$.
3. **Preferencia de $p$:** $p$ prefiere estrictamente a $a$ por encima de su pareja actual en $M$ (o bien $p$ se encuentra soltero en $M$).
4. **Preferencia de $a$:** $a$ prefiere estrictamente a $p$ por encima de su pareja actual en $M$ (o bien $a$ se encuentra soltero en $M$).

---

### 2. Función Potencial (Demostración de Terminación)

Para garantizar formalmente que el proceso iterativo concluye en un número finito de pasos, definimos una función potencial $\Phi$ basada en las opciones de propuesta no exploradas:

* **Definición de $\Phi$:** Sea $\Phi$ el número total de pares ordenados $(p, a)$ tales que el proponente $p$ considera aceptable al receptor $a$, pero **aún no le ha propuesto**.
* **Propiedades de $\Phi$:**
1. **Entera y no negativa:** $\Phi \ge 0$, puesto que la cantidad de pares no probados nunca puede ser inferior a cero.
2. **Decrecimiento estricto:** En cada paso del algoritmo, un proponente $p$ realiza una propuesta a un receptor $a$ de su lista al cual no le había propuesto antes. Dicho par transita de la categoría de "no intentado" a "intentado", reduciendo el valor de la función potencial exactamente en una unidad ($\Phi_{\text{nuevo}} = \Phi_{\text{actual}} - 1$).



Dado que $\Phi$ es una secuencia de enteros no negativos acotada superiormente por la suma de las longitudes de las listas de todos los proponentes, y decrece estrictamente en cada iteración, el algoritmo garantiza su terminación en tiempo finito.

---

### 3. ¿Sigue siendo estable el resultado? Demostración Formal

**Sí, el resultado producido por el algoritmo adaptado sigue siendo perfectamente estable.**

#### Demostración por Reducción al Absurdo

Supongamos por contradicción que el emparejamiento final $M$ producido por el algoritmo no es estable.

1. Por definición de inestabilidad, debe existir al menos una pareja bloqueante $(p, a)$ respecto a $M$. Esto implica que:
* $p$ prefiere a $a$ sobre su pareja actual $m(p)$ en $M$ (o $p$ está soltero).
* $a$ prefiere a $p$ sobre su pareja actual $m(a)$ en $M$ (o $a$ está soltero).
* Ambas partes se consideran mutuamente aceptables.


2. Puesto que los proponentes realizan sus ofertas en orden estrictamente decreciente de preferencia (comenzando por su primera opción), y el enunciado establece que $p$ prefiere a $a$ por encima de su pareja final $m(p)$, es un hecho lógico que **$p$ le propuso a $a$ en algún momento anterior** de la ejecución antes de ser rechazado definitivamente o antes de casarse con $m(p)$ (si $p$ terminó soltero).
3. Dado que $p$ le propuso a $a$, debió ocurrir un rechazo: en algún instante temporal, $a$ rechazó a $p$ (o lo abandonó tras haberlo aceptado de manera provisional para sustituirlo por un pretendiente de mayor preferencia). Por la propiedad monótona fundamental de los receptores en los procesos de asignación estable, un receptor jamás empeora su situación: únicamente rechaza candidatos para retener a otros que valora más (o permanece libre si la alternativa vigente es inferior). En consecuencia, al finalizar el algoritmo, la pareja asignada a $a$, $m(a)$, es preferida por $a$ (o es la única disponible) frente a cualquier pretendiente que haya tenido en el pasado, incluido $p$.
4. Esto entra en contradicción directa con la premisa de la pareja bloqueante, la cual afirmaba que $a$ prefería estrictamente a $p$ por encima de su pareja actual $m(a)$.

#### Conclusión

La suposición de la existencia de una pareja bloqueante conduce a una contradicción insalvable. Por lo tanto, se demuestra formalmente que **el resultado del algoritmo de Gale-Shapley con listas incompletas conserva la propiedad de estabilidad**.