# DP

## Plígono

En un reino lejano, existía un mago llamado Héctor que protegía un gran tesoro escondido dentro de un castillo mágico. Este castillo tenía la forma de un polígono perfecto y estrictamente convexo con $n$ torres, cada una conectada por paredes fuertes e inquebrantables.

La reina María que creía firmemente en las ideas de la Revolución (¿Cuál? no sé, la revolución mágica del reino lejano) decidió que era hora de compartir parte del tesoro con el pueblo, pero debía hacerlo con cuidado para no despertar la ira de Héctor. La reina María llamó a los mejores arquitectos del reino y les pidió que hicieran $k$ cortes en las paredes del castillo, utilizando portales mágicos que conectaran dos torres distintas que no estuvieran directamente adyacentes. Sin embargo, había una advertencia: los portales no podían cruzarse en medio de las paredes, solo en las torres del castillo.

El objetivo de la reina María era repartir las riquezas de tal manera que cada porción de territorio dentro del castillo fuera lo más equitativa posible. Así, pidió a los arquitectos que maximizaran el área de la porción más pequeña que se formara dentro del castillo después de colocar los $k$ portales mágicos.

Tu tarea es ayudar a la reina María a encontrar la mejor manera de cortar el castillo para que la distribución del tesoro sea justa para todos.

(PD: Cuando Héctor regresó a su castillo y lo vio todo cuarteado, en un ataque de ira convocó a la bestia mágica Yesapin, pero eso es historia para otro momento)

### Statement

Se te da un polígono estrictamente convexo con $n$ vértices.

Realizarás $k$ cortes que cumplan con las siguientes condiciones:

- cada corte es un segmento que conecta dos vértices diferentes no adyacentes;
- dos cortes solo pueden intersectarse en los vértices del polígono.

Tu tarea es maximizar el área de la región más pequeña que se formará por el polígono y esos $k$ cortes.

### Solution

Vamos a buscar la respuesta usando búsqueda binaria.

Supongamos que queremos verificar si podemos obtener $k+1$ regiones con un área de al menos $w$. A partir de ahora, un corte correcto significa un corte que separará una región con un área de al menos $w$.

Consideremos un intervalo de vértices $(i,j)$. Vamos a separarlo virtualmente usando un corte desde $i$ hasta $j$. Nos gustaría saber cuántas regiones correctas podemos obtener realizando cortes solo en este intervalo. El área junto al corte virtual se considera un sobrante. Dado un conjunto de cortes correctos en este intervalo, siempre es óptimo elegir el conjunto con más cortes, y si tienen la misma cantidad de cortes, el que tenga el sobrante más grande.

Esta observación nos lleva a una solución de programación dinámica. Sea $dp_{i,j}$ un par $(r_{i,j}, l_{i,j})$ donde $r_{i,j}$ representa la mayor cantidad de regiones y $l_{i,j}$ el mayor sobrante que podemos obtener al realizar cortes en el intervalo $(i,j)$.

Para calcular este $dp$, iteraremos sobre todos los vértices $k$ tal que $i < k < j$ y consideraremos el vértice $k$ como uno de los vértices incluidos en la región sobrante. Esta es una transición simple desde los estados $dp_{i,k}$ y $dp_{k,j}$. Después de calcular nuestro estado $dp$, podemos cortar este intervalo de manera segura si $l_{i,j} \geq w$.

Si y solo si $r_{1,n} \geq k+1$, la respuesta es al menos $w$.

COMPLEJIDAD TEMPORAL:
$O(n^3 \log(10^{16}))$.
