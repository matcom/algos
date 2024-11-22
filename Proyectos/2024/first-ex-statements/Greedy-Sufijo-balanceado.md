# Greedy

## Sufijo Balanceado

Te dan una cadena $S$ de longitud $N$ y un número entero $K$.

Sea $C$ el conjunto de todos los caracteres en $S$. La cadena $S$ se llama buena si, para cada sufijo de $S$:

La diferencia entre las frecuencias de cualquier par de caracteres en $C$ no excede $K$.
En particular, si el conjunto $C$ tiene un solo elemento, la cadena $S$ es buena.

Encuentra si existe una reordenación de $S$ que sea buena.
Si existen múltiples reordenaciones de este tipo, imprime la reordenación lexicográficamente más pequeña.
Si no existe tal reordenación, imprime $-1$ en su lugar.

Nota que un sufijo de una cadena se obtiene eliminando algunos (posiblemente cero) caracteres desde el principio de la cadena. Por ejemplo, los sufijos de $S = abca$ son $\\{a, ca, bca, abca\\}$.

### Statement

Una cadena $S$ se llama buena si, para cada sufijo $T$ de $S$ y los caracteres $c_1, c_2$ que ocurren en $S$, las frecuencias de $c_1$ en $T$ y $c_2$ en $T$ difieren en como máximo $K$.

Dada $S$, encuentra su reordenación buena lexicográficamente más pequeña.

### Solution

Primero, averigüemos cuándo exactamente una cadena $S$ tiene una reordenación buena.
Llamaremos a un sufijo que satisfaga la condición dada, balanceado.

Sea $c_1$ y $c_2$ algunos dos caracteres que ocurren en $S$, y sean $f_{c_1}$ y $f_{c_2}$ sus respectivas frecuencias.
Si $S$ va a ser buena, claramente debe cumplirse $\lvert f_{c_1} - f_{c_2} \rvert \leq K$; de lo contrario, la cadena en sí no está balanceada, sin importar cómo la reorganicemos.

De hecho, esta condición también es suficiente para que $S$ tenga una reordenación buena, es decir, $\lvert f_{c_1} - f_{c_2} \rvert \leq K$ para cada par de caracteres $c_1, c_2$ en $S$.

Prueba
Podemos construir una reordenación buena de manera codiciosa.

Supongamos que tenemos $N$ caracteres, de modo que $\lvert f_{c_1} - f_{c_2} \rvert \leq K$ para cada par de ellos.
Construya una cadena de la siguiente manera:

Sea $c$ un carácter con la frecuencia máxima. Coloca una ocurrencia de $c$, y disminuye $f_c$ en $1$.
Es fácil ver que esto preserva la condición $\lvert f_{c_1} - f_{c_2} \rvert \leq K$, y así podemos colocar todos los $N$ caracteres.
Además, la cadena que construimos es buena, ya que en cada paso el sufijo que creamos está balanceado.

Observe que, en lugar de verificar cada diferencia, es suficiente verificar si la diferencia máxima satisface la condición.
Es decir, una cadena tiene una reordenación buena si y solo si la diferencia entre los caracteres de frecuencia máxima y mínima es $\leq K$.

Ahora que sabemos cómo verificar si $S$ tiene una reordenación buena, necesitamos averiguar cómo construir la reordenación lexicográficamente más pequeña.
Construir objetos lexicográficamente más pequeños generalmente implica hacerlo de manera codiciosa, y esta tarea no es diferente.

Para cada $i$ de $1$ a $N$, intentemos colocar los caracteres `'a', 'b', 'c', \dots, 'z'` en orden. Tan pronto como se pueda colocar uno de ellos, hazlo y pasa al siguiente índice.
Para verificar si colocar un cierto caracter es posible, necesitamos verificar si el sufijo de la cadena comenzando desde $i+1$ tiene una reordenación buena o no.

Sin embargo, tenemos una condición bastante simple para esto: la diferencia entre las frecuencias máximas y mínimas de los caracteres restantes debe ser $\leq K$.
Sabemos qué caracteres hemos colocado hasta ahora, por lo que también conocemos las frecuencias de los caracteres restantes.
Entonces, podemos verificar esta condición en $O(\Sigma)$ simplemente calculando directamente la frecuencia máxima y mínima, donde $\Sigma$ es el tamaño del alfabeto (aquí, $\Sigma = 26$).

Para cada posición, probamos (como máximo) $26$ posibilidades, y procesamos cada una en $O(26)$.
Por lo tanto, nuestra solución se ejecuta en $O(26^2 \cdot N)$, lo cual es lo suficientemente rápido.
Es posible pero innecesario hacerlo correr en $O(26 \cdot N)$ con algunas optimizaciones menores.

COMPLEJIDAD TEMPORAL
$O(26 \cdot N)$
