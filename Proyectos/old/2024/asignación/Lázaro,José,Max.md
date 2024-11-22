# Problemas

## Alianza de Robots LGBT

En una futurística ciudad llena de robots, cada robot pertenece a una facción identificada por un color específico. Las piezas de los robots fueron además creadas por varios fabricantes distintos, algunos robots tienen piezas hechas por fabricantes en común.

Los robots de diferentes facciones están buscando formar una alianza estratégica multicolor. Esta alianza debe ser un grupo de robots donde todos tengan, dos a dos, alguna pieza hecha por el mismo fabricante, y lo más importante: debe haber al menos un robot de cada color en esta alianza.

Dado un grupo de robots, determine si es posible o no formar una alianza multicolor.

## PCC

Han pasado 20 años desde que José se graduó de Ciencias de la Computación  
(haciendo una muy buena tesis) y las vueltas de la vida lo llevaron a convertirse  
en el presidente del Partido Comunista de Cuba. Una de sus muchas responsabilidades  
consiste en visitar zonas remotas. En esta ocasión debe visitar una  
ciudad campestre de Pinar del Río.

También han pasado 20 años desde que Max consiguió su título en MATCOM.  
Tras años de viaje por las grandes metrópolis del mundo, en algún punto  
decidió que prefería vivir una vida tranquila, aislada de la urbanización, en una  
tranquila ciudad de Pinar del Río. Las vueltas de la vida quisieron que precisamente  
Max fuera el único universitario habitando la ciudad que José se  
dispone a visitar.

Los habitantes de la zona entraron en pánico ante la visita de una figura tan  
importante y decidieron reparar las calles de la ciudad por las que transitaría  
José. El problema está en que nadie sabía qué ruta tomaría el presidente y  
decidieron pedirle ayuda a Max.

La ciudad tiene $n$ puntos importantes, unidos entre sí por calles cuyos  
tamaños se conoce. Se sabe que José comenzará en alguno de esos puntos  
($s$) y terminará el viaje en otro ($t$). Los ciudadanos quieren saber, para  
cada par $s$, $t$, cuántas calles participan en algún camino de distancia mínima  
entre $s$ y $t$.

## Sufijo Balanceado

Te dan una cadena $S$ de longitud $N$ y un número entero $K$.

Sea $C$ el conjunto de todos los caracteres en $S$. La cadena $S$ se llama buena si, para cada sufijo de $S$:

La diferencia entre las frecuencias de cualquier par de caracteres en $C$ no excede $K$.
En particular, si el conjunto $C$ tiene un solo elemento, la cadena $S$ es buena.

Encuentra si existe una reordenación de $S$ que sea buena.
Si existen múltiples reordenaciones de este tipo, imprime la reordenación lexicográficamente más pequeña.
Si no existe tal reordenación, imprime $-1$ en su lugar.

Nota que un sufijo de una cadena se obtiene eliminando algunos (posiblemente cero) caracteres desde el principio de la cadena. Por ejemplo, los sufijos de $S = abca$ son $\\{a, ca, bca, abca\\}$.
