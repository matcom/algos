# DP

## Tramposo

Leandro es profesor de programación. En sus ratos libres, le gusta divertirse con las estadísticas de sus pobres estudiantes reprobados. Los estudiantes están separados en $n$ grupos. Casualmente, este año, todos los estudiantes reprobaron alguno de los dos exámenes finales: $P$ (POO) y $R$ (Recursividad).

Esta tarde, Leandro decide entretenerse separando a los estudiantes suspensos en conjuntos de tamaño $k$ que cumplan lo siguiente: En un mismo conjunto, todos los estudiantes son del mismo grupo $i$ ($1 \leq i \leq n$) o suspendieron por el mismo examen $P$ o $R$.

Conociendo el grupo y la prueba suspendida de cada estudiante, y el tamaño de los conjuntos, ayude a Leandro a saber cuántos conjuntos de estudiantes suspensos puede formar.

### Statement

Dado que hay $n$ arbustos, cada uno con $a_i$ bayas rojas y $b_i$ bayas azules, y cada canasta puede contener $k$ bayas, pero cada canasta solo puede contener bayas del mismo arbusto o bayas del mismo color (rojo o azul):

Determina el número máximo de canastas que se puede llenar completamente.

### Solution

Solución 1:

No existe una solución ávida obvia, por lo que intentaremos la programación dinámica. Sea $dp[i][j]$ un arreglo booleano que indica si podemos tener $j$ bayas rojas extra después de considerar los primeros $i$ arbustos. Una baya es extra si no se coloca en una canasta llena (de cualquier tipo). Ten en cuenta que si sabemos que hay $j$ bayas rojas extra, también podemos calcular fácilmente cuántas bayas azules extra hay. Nota que podemos elegir nunca tener más de $k-1$ bayas rojas extra, porque de lo contrario podemos llenar alguna cantidad de canastas con ellas.

Para la transición del arbusto $i-1$ al arbusto $i$, recorremos todos los posibles valores $l$ desde $0$ hasta $\min(k-1, a_i)$ y verificamos si podemos dejar $l$ bayas rojas extra del arbusto actual $i$. Para algunos $i$ y $j$, podemos dejar $l$ bayas rojas extra y poner las bayas rojas restantes en canastas, posiblemente con bayas azules del mismo arbusto si $(a_i - l) \mod k + b_i \geq k$. El razonamiento para esto es el siguiente:

En primer lugar, estamos dejando $l$ bayas rojas (o al menos intentándolo). Mostramos que de este arbusto, habrá como máximo una canasta que contenga tanto bayas rojas como azules (todas de este arbusto). Para colocar las bayas rojas restantes en canastas llenas, cuantas más bayas azules tengamos, mejor. Es óptimo colocar las bayas rojas restantes $a_i - l$ en sus propias canastas separadas antes de fusionarlas con las bayas azules (de esta manera se requieren menos bayas azules para satisfacer la condición). Luego, si $(a_i - l) \mod k + b_i$ es al menos $k$, podemos llenar alguna canasta con las bayas rojas restantes y posiblemente algunas bayas azules. Recuerda que no nos importa cuántas bayas azules extra dejamos porque eso está determinado de manera única por la cantidad de bayas rojas extra.

También observa que siempre podemos dejar $a_i \mod k$ bayas rojas extra.

Denota el número total de bayas como $t$. La respuesta será el máximo sobre todos los $(t-j)/k$ tales que $dp[n][j]$ es verdadero, $0 \leq j \leq k-1$.

Solución 2:

Usamos programación dinámica. Sea $dp[i][j]$ verdadero si, después de considerar los primeros $i$ arbustos, $j$ es el número de bayas rojas en canastas heterogéneas módulo $k$. Las canastas heterogéneas contienen bayas del mismo arbusto, y las canastas homogéneas contienen bayas del mismo tipo.

Supongamos que conocemos el número de bayas rojas en canastas heterogéneas módulo $k$. Esto determina el número de bayas azules en canastas heterogéneas módulo $k$. Dado que el número de bayas rojas en canastas homogéneas es un múltiplo de $k$, también determina el número de bayas rojas que no están en ninguna canasta (podemos asumir de manera segura que es menos de $k$, ya que de lo contrario podemos formar otra canasta). De manera similar, podemos determinar el número de bayas azules que no están en ninguna canasta, y así deducir el número de canastas.

Para calcular los posibles números de bayas rojas en canastas heterogéneas módulo $k$, basta con observar cada arbusto por separado y determinar los posibles números de bayas rojas módulo $k$ en canastas heterogéneas para ese arbusto. Si hay más de una canasta heterogénea para un arbusto, podemos reorganizar las bayas para dejar como máximo una heterogénea. Ahora tenemos dos casos. Si no hay canastas heterogéneas, el número de bayas rojas en esas canastas es obviamente cero. Si hay una canasta heterogénea, sea $x$ el número de bayas rojas en ella y $k-x$ el número de bayas azules en ella. Claramente, $0 \leq x \leq a_i$ y $0 \leq k - x \leq b_i$. Reorganizando, obtenemos $\max(0, k - b_i) \leq x \leq \min(a_i, k)$. Estos corresponden a las transiciones para nuestra programación dinámica.

COMPLEJIDAD TEMPORAL:
$O(nk^2)$
