# Greedy

## Criminal y policías

Javier es un criminal buscado, y $N$ policías están dispuestos a atraparlo. Los oficiales quieren capturar a Javier sin importar el costo, y Javier también quiere eliminar a la mayor cantidad de oficiales posible (preferentemente a todos) antes de ser atrapado (o antes de escapar después de eliminarlos a todos). Ni los oficiales ni Javier se retirarán antes de lograr sus objetivos.

Javier y los oficiales están en una cuadrícula unidimensional con coordenadas que van desde $-10^{10}$ hasta $10^{10}$. Javier está inicialmente en la coordenada $C$, y el $i$-ésimo oficial está inicialmente en la coordenada $P_i$. Los oficiales y Javier luego se turnan para moverse, siendo el equipo de oficiales el que se mueve primero.

Durante su turno, los oficiales tendrán que moverse a una celda adyacente desocupada uno por uno, en el orden que prefieran. Cada oficial tendrá que moverse. En cada momento del tiempo, ningún oficial puede estar en la misma celda que otro oficial, y tampoco puede estar en la misma celda que Javier. Si un oficial no puede moverse a una celda adyacente desocupada, será eliminado (y la celda en la que estaba se desocupa). Es importante notar que el equipo de oficiales intentará moverse de tal manera que se eliminen la menor cantidad posible de oficiales. Por ejemplo, con $P = [2, 3, 4]$ y $C = 6$, las siguientes posiciones posibles de los oficiales pueden ser $[1, 2, 3]$, $[1, 2, 5]$, $[1, 4, 5]$, o $[3, 4, 5]$. Sin embargo, con $P = [2, 3, 4]$ y $C = 5$, el único conjunto posible de las siguientes posiciones de los oficiales es $[1, 2, 3]$.

Después del turno del equipo de oficiales, Javier también se mueve a una celda adyacente desocupada o es atrapado si no puede encontrar ninguna celda adyacente desocupada. El proceso se repite hasta que Javier es atrapado o todos los oficiales son eliminados y Javier escapa.

Debes encontrar el número máximo de oficiales que pueden ser eliminados por Javier, y si Javier puede escapar o no.

Como recordatorio, dos celdas con coordenadas $X$ y $Y$ son adyacentes si y solo si $|X - Y| = 1$.

### Statement

Javier y $N$ oficiales de policía están parados en posiciones distintas en una cuadrícula unidimensional. Se mueven por turnos: primero, cada oficial se mueve un paso a la izquierda o a la derecha hacia un cuadrado desocupado, luego el Javier se mueve a la izquierda o a la derecha hacia un cuadrado desocupado. Un oficial que no puede moverse es eliminado, y si el Javier no puede moverse, es capturado. Encuentra el número máximo de oficiales que pueden ser eliminados.

### Solution

EXPLICACIÓN RÁPIDA  
Si el conjunto ordenado de posiciones es $P_1 < P_2 < \dots < P_i < C < P_{i+1} < \dots < P_N$, Javier puede eliminar el prefijo más largo de oficiales comenzando en $i+1$ y el sufijo más largo terminando en $i$, tal que $C(\text{mod}2) \neq P_j(\text{mod}2)$.

EXPLICACIÓN:  
Supongamos que Javier comienza en la posición $C$. Por ahora, concentremos nuestra atención solo en los oficiales cuyas posiciones iniciales son mayores que $C$ — el otro caso resulta ser simétrico.

Supongamos que tenemos $C < P_1 < P_2 < \dots < P_N$.  
Una observación inicial es que la paridad relativa de $C$ y $P_i$ siempre se mantiene igual, es decir, si inicialmente tienen la misma paridad, después de cualquier conjunto de movimientos seguirán teniendo la misma paridad; y si inicialmente son diferentes, cualquier conjunto de movimientos los mantendrá distintos.

Ahora, miremos primero a $P_1$. Hay dos casos:

- **$C$ y $P_1$ tienen la misma paridad**  
  En este caso, $P_1$ nunca puede ser eliminado — de hecho, ninguno de los oficiales puede ser eliminado.  
  **Prueba**
    Dado que tienen la misma paridad y deben comenzar en casillas distintas al inicio de cada turno de los oficiales, debemos tener $P_1 \geq C + 2$.  
    Esto significa que $P_1$ siempre puede simplemente dar un paso hacia Javier independientemente de los movimientos de los otros oficiales, y en particular, nunca será eliminado.  
    Además, debido a que $P_1$ siempre puede moverse hacia la izquierda hacia Javier, ese movimiento dejará al menos un espacio vacío para que $P_2$ también se mueva hacia la izquierda, lo que permite que $P_3$ se mueva hacia la izquierda, y así sucesivamente.

    Por lo tanto, cada oficial siempre tiene al menos un movimiento legal, lo que significa que ninguno de ellos puede ser eliminado.

- **$C$ y $P_1$ tienen diferente paridad**  
  En este caso, $P_1$ siempre puede ser eliminado.  
  **Prueba**
    Supongamos que $P_1 > C + 1$. Entonces, $P_1 \geq C + 3$, por lo que, sin importar qué movimiento haga $P_1$, Javier siempre puede moverse un paso hacia la derecha.  
    Así, la distancia entre Javier y $P_1$ o se mantiene igual, o disminuye en $2$ — en particular, no aumenta.

    ¿Qué pasa si $P_1 = C + 1$?  
    $P_1$ no tiene más opción que moverse hacia la derecha, lo que permite que Javier también se mueva hacia la derecha en su turno.  
    Sin embargo, nuestra cuadrícula es finita, por lo que $P_1$ no puede moverse hacia la derecha indefinidamente.  
    Por lo tanto, llegará un momento en que $P_1 = C + 1$, pero $P_1 + 1, P_1 + 2, \dots, 10^{10}$ estarán ocupados por oficiales.  
    Esto obligará a que $P_1$ sea eliminado, como se requiere.

Ahora que $P_1$ ha sido eliminado, veamos a $P_2$.  
Si $P_2$ y $C$ tienen diferentes paridades, un argumento similar al anterior nos dice que $P_2$ también puede ser eliminado — ya sea después de eliminar a $P_1$ siguiendo la misma estrategia, o $P_2$ ya fue eliminado antes que $P_1$.  
Por otro lado, si $P_2$ y $C$ tienen la misma paridad, nuestro primer argumento nos dice que $P_2$ nunca puede ser eliminado — y, por lo tanto, $P_i$ para $i \geq 2$ nunca puede ser eliminado.

Esto nos lleva al siguiente resultado:  
**Lema**: Sea $k$ el índice más pequeño tal que $\text{paridad}(C) = \text{paridad}(P_i)$. Entonces, cuando los oficiales se mueven de manera óptima, solo $P_1, P_2, \dots, P_{i-1}$ pueden ser eliminados, y ninguno más allá de eso.

La prueba sigue fácilmente de los procesos descritos anteriormente.

Por supuesto, el mismo resultado se aplica para los oficiales a la izquierda de Javier, es decir, algún sufijo de ellos con paridad diferente a la de $C$ puede ser eliminado, y ninguno más allá de eso.

Por lo tanto, tenemos nuestro algoritmo final:

1. Ordena el conjunto de oficiales.
2. Entre los oficiales a la derecha de Javier, elige el prefijo más largo tal que su paridad sea diferente a la de $C$.
3. Entre los oficiales a la izquierda de Javier, elige el sufijo más largo tal que su paridad sea diferente a la de $C$.
4. La respuesta es la suma de las dos cantidades anteriores.

Finalmente, Javier escapa si y solo si todos los oficiales son eliminados, así que imprime $1$ si todos los $N$ oficiales pueden ser eliminados y $-1$ en caso contrario.

**COMPLEJIDAD TEMPORAL:**  
$O(N \log N)$
