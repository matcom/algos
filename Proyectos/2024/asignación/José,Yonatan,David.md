# Problemas

## PCC

Han pasado 20 años desde que José se graduó de Ciencias de la Computación  
(haciendo una muy buena tesis) y las vueltas de la vida lo llevaron a convertirse  
en el presidente del Partido Comunista de Cuba. Una de sus muchas responsabilidades  
consiste en visitar zonas remotas. En esta ocasión debe visitar una  
ciudad campestre de Pinar del Río.

También han pasado 20 años desde que David consiguió su título en MATCOM.  
Tras años de viaje por las grandes metrópolis del mundo, en algún punto  
decidió que prefería vivir una vida tranquila, aislada de la urbanización, en una  
tranquila ciudad de Pinar del Río. Las vueltas de la vida quisieron que precisamente  
David fuera el único universitario habitando la ciudad que José se  
dispone a visitar.

Los habitantes de la zona entraron en pánico ante la visita de una figura tan  
importante y decidieron reparar las calles de la ciudad por las que transitaría  
José. El problema está en que nadie sabía qué ruta tomaría el presidente y  
decidieron pedirle ayuda a David.

La ciudad tiene $n$ puntos importantes, unidos entre sí por calles cuyos  
tamaños se conoce. Se sabe que José comenzará en alguno de esos puntos  
($s$) y terminará el viaje en otro ($t$). Los ciudadanos quieren saber, para  
cada par $s$, $t$, cuántas calles participan en algún camino de distancia mínima  
entre $s$ y $t$.

## Alianza de Robots LGBT

En una futurística ciudad llena de robots, cada robot pertenece a una facción identificada por un color específico. Las piezas de los robots fueron además creadas por varios fabricantes distintos, algunos robots tienen piezas hechas por fabricantes en común.

Los robots de diferentes facciones están buscando formar una alianza estratégica multicolor. Esta alianza debe ser un grupo de robots donde todos tengan, dos a dos, alguna pieza hecha por el mismo fabricante, y lo más importante: debe haber al menos un robot de cada color en esta alianza.

Dado un grupo de robots, determine si es posible o no formar una alianza multicolor.

## Subsecuencia Buena

Supongamos que tienes un array binario $B$ de longitud $N$. Una secuencia $x_1, x_2, \dots, x_k$ se llama buena con respecto a $B$ si satisface las siguientes condiciones:

- $1 \leq x_1 < x_2 < \dots < x_k \leq N + 1$
- Para cada par $(i, j)$ tal que $1 \leq i < j \leq k$, el subarray $B[x_i : x_j - 1]$ contiene $(j - i)$ unos más que ceros. Es decir, si $B[x_i : x_j - 1]$ contiene $c_1$ unos y $c_0$ ceros, entonces se debe cumplir que $c_1 - c_0 = j - i$.

Aquí, $B[L : R]$ denota el subarray que consiste en los elementos $[B_L, B_{L + 1}, B_{L + 2}, \dots, B_R]$. Nota que, en particular, una secuencia de tamaño $1$ siempre es buena.

Por ejemplo, supongamos que $B = [0, 1, 1, 0, 1, 1]$. Entonces:

- La secuencia $[1, 4, 7]$ es una secuencia buena. Los subarrays que necesitan ser revisados son $B[1 : 3]$, $B[1 : 6]$ y $B[4 : 6]$, que todos cumplen con la condición.
- La secuencia $[1, 5]$ no es buena, porque $B[1 : 4] = [0, 1, 1, 0]$ contiene un número igual de ceros y unos (cuando debería contener un $1$ extra).

Yonatan le dio a David un array binario $A$ de tamaño $N$ y le pidió que encontrara la secuencia más larga que sea buena con respecto a $A$. Ayuda a David a encontrar una de estas secuencias.

Si existen múltiples secuencias más largas posibles, puedes devolver cualquiera de ellas.
