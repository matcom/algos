# Grafos

## Créditos

El colegio de Francisco comienza la próxima semana. Hay $S$ asignaturas en total, y necesita elegir $K$ de ellas para asistir cada día, para cumplir con el número requerido de créditos para pasar el semestre. Hay $N+1$ edificios. Su hostal está en el edificio número $0$. La asignatura $i$ se enseña en el edificio $A_i$. Después de cada asignatura, hay un descanso durante el cual regresa a su hostal. Hay $M$ caminos bidireccionales de longitud $1$ que conectan el edificio $u$ con el edificio $v$. Encuentra la distancia total mínima posible que Francisco necesita recorrer cada día si elige sus asignaturas sabiamente.

### Statement

El colegio de Francisco comienza la próxima semana. Hay $S$ asignaturas en total representadas mediante un arreglo $A$, y necesita elegir $K$ de ellas para asistir cada día, para cumplir con el número requerido de créditos para pasar el semestre. Hay $N+1$ edificios. Su hostal está en el edificio número $0$. La asignatura $i$ se enseña en el edificio $S[i]$. Después de cada asignatura, hay un descanso durante el cual regresa a su hostal. Hay $M$ caminos bidireccionales de tamaño $1$ que conectan el edificio $u$ con el edificio $v$. Encuentra la distancia total mínima posible que Francisco necesita recorrer cada día si elige sus asignaturas sabiamente.

### Solution

El término nivel de un nodo $x$ con respecto a un nodo fijo en un grafo se utiliza para describir el número de aristas en el camino más corto desde el nodo fijo hasta el nodo $x$.

Se ha dado que el colegio tiene un edificio de hostal y $N$ edificios restantes donde se imparten las asignaturas. También se da información sobre qué edificios están conectados por caminos de longitud $1$. Estos datos se pueden representar como un grafo con edificios como nodos y caminos como aristas. Dado que todos los caminos tienen una longitud de una unidad, el peso de cada arista se asignará como $1$. Una implicación de los caminos de una unidad de longitud es que la distancia recorrida desde el hostal hasta el edificio $B$ será igual al nivel de $B$ con respecto al hostal en el grafo.

Demostración

Consideremos que el hostal (nodo $0$) está en el nivel $0$. Todos los nodos que se pueden alcanzar desde el nodo $0$ mediante una sola arista están en el nivel 1 con respecto al nodo $0$. De manera similar, cualquier edificio alcanzable desde el hostal mediante $x$ caminos bidireccionales, cada uno conectando un par único de edificios, estará en el nivel $x$ con respecto al hostal.

Establecemos la relación entre el número de aristas $e$ (necesarias para cruzar desde el hostal hasta alcanzar cualquier otro edificio) y el nivel $L$ (de un edificio con respecto al hostal):

$$
e = L
$$

Si necesitamos viajar desde $0$ hasta $x$ en este grafo y $e$ número de aristas $E_1$ a $E_e$ constituyen el camino desde $0$ hasta $x$, entonces la distancia total $D$ de nuestro camino estará dada por:

$$
D = \sum_{i=1}^{e} d(E_i)
$$

donde $d(E_i)$ representa la longitud de la arista $E_i$. En este caso, las longitudes de los caminos individuales son $1$ cada uno, por lo que obtenemos:

$$
D = \sum_{i=1}^{e} 1
$$

$$
D = e
$$

lo cual, según la relación establecida anteriormente, se puede escribir como:

$$
D = L
$$

Donde $L$ es el nivel del nodo $x$ con respecto al nodo $0$.

Dado que el grafo no es acíclico, un solo nodo $x$ puede tener múltiples formas de llegar desde $0$ a través de diferentes conjuntos de aristas. Puede parecer que pertenece a diferentes niveles debido a esto; en este caso, consideraremos que pertenece al menor de estos niveles (el más cercano al nivel $0$), porque necesitamos encontrar la distancia mínima recorrida por Chef, lo que implica que si existe más de un camino hacia un nodo desde $0$, seguiremos el de menor peso.

Ejemplo

Si existen $2$ caminos desde el nodo $0$ hasta $x$ que consisten en $e$ y $f$ aristas respectivamente ($e < f$). Supongamos que los caminos están constituidos por las aristas $E_1$ a $E_e$ y $F_1$ a $F_f$ respectivamente. En tal caso, nuestro nivel $L$ del nodo $x$ con respecto al nodo $0$ será $e$, permitiéndonos recorrer un camino más corto desde el hostal hasta el edificio $x$ por parte de Chef.

En caso de que $e = f$, ambos caminos darán como resultado el mismo nivel de $x$, por lo que no se generará ningún conflicto.

Para implementar esta asignación de niveles a los nodos, podemos utilizar un recorrido en anchura (recorrido en orden de niveles) del grafo al que hemos convertido los datos de entrada. Más sobre este algoritmo se puede encontrar aquí y aquí.

Comenzando el recorrido en orden de niveles desde el nodo $0$ y el nivel $0$, a medida que observamos que un nivel completo ha sido eliminado de la cola y sus hijos (el siguiente nivel) han sido empujados a ella, incrementamos el nivel y continuamos el recorrido.

Una vez que todos los edificios en los que se enseñan las asignaturas de $1$ a $S$ han recibido un nivel con respecto al hostal, necesitamos seleccionar $K$ de entre estos que tengan los niveles mínimos. Los edificios pueden aparecer más de una vez, es decir, pueden existir casos en los que más de una asignatura se esté impartiendo en un solo edificio, por lo tanto, al seleccionar los $K$ edificios con niveles mínimos, necesitamos asegurarnos de que el mismo edificio pueda ser seleccionado tantas veces como asignaturas diferentes se estén impartiendo en él.

Para establecer esto, utilizamos un multiconjunto. Recorremos todos los edificios en los que se están impartiendo las asignaturas de $1$ a $S$ e insertamos sus niveles correspondientes en un multiconjunto. La suma de los primeros $K$ elementos de este multiconjunto nos dará la distancia recorrida por Chef desde el hostal hasta esos edificios en los que se están impartiendo las asignaturas que eligió, por lo tanto, multiplicamos esto por $2$ para obtener la respuesta final (ya que vuelve a su hostal después de cada asignatura, necesitando recorrer la misma distancia que tuvo al ir del hostal al edificio).

$O(\max(N, \log(S) \times S))$ es la complejidad temporal.

Esto se debe a que el recorrido en orden de niveles toma $O(N)$ de tiempo y la construcción del multiconjunto toma $O(\log(S) \times S)$, es decir, $S$ operaciones de inserción de $O(s_i)$ cada una, para todos los $s_i$ desde $0$ hasta $S-1$.

COMPLEJIDAD TEMPORAL:
$O(\max(N, \log(S) \times S))$
