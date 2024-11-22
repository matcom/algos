# Problemas

## Criminal y policías

Ovidio es un criminal buscado, y $N$ policías están dispuestos a atraparlo. Los oficiales quieren capturar a Ovidio sin importar el costo, y Ovidio también quiere eliminar a la mayor cantidad de oficiales posible (preferentemente a todos) antes de ser atrapado (o antes de escapar después de eliminarlos a todos). Ni los oficiales ni Ovidio se retirarán antes de lograr sus objetivos.

Ovidio y los oficiales están en una cuadrícula unidimensional con coordenadas que van desde $-10^{10}$ hasta $10^{10}$. Ovidio está inicialmente en la coordenada $C$, y el $i$-ésimo oficial está inicialmente en la coordenada $P_i$. Los oficiales y Ovidio luego se turnan para moverse, siendo el equipo de oficiales el que se mueve primero.

Durante su turno, los oficiales tendrán que moverse a una celda adyacente desocupada uno por uno, en el orden que prefieran. Cada oficial tendrá que moverse. En cada momento del tiempo, ningún oficial puede estar en la misma celda que otro oficial, y tampoco puede estar en la misma celda que Ovidio. Si un oficial no puede moverse a una celda adyacente desocupada, será eliminado (y la celda en la que estaba se desocupa). Es importante notar que el equipo de oficiales intentará moverse de tal manera que se eliminen la menor cantidad posible de oficiales. Por ejemplo, con $P = [2, 3, 4]$ y $C = 6$, las siguientes posiciones posibles de los oficiales pueden ser $[1, 2, 3]$, $[1, 2, 5]$, $[1, 4, 5]$, o $[3, 4, 5]$. Sin embargo, con $P = [2, 3, 4]$ y $C = 5$, el único conjunto posible de las siguientes posiciones de los oficiales es $[1, 2, 3]$.

Después del turno del equipo de oficiales, Ovidio también se mueve a una celda adyacente desocupada o es atrapado si no puede encontrar ninguna celda adyacente desocupada. El proceso se repite hasta que Ovidio es atrapado o todos los oficiales son eliminados y Ovidio escapa.

Debes encontrar el número máximo de oficiales que pueden ser eliminados por Ovidio, y si Ovidio puede escapar o no.

Como recordatorio, dos celdas con coordenadas $X$ y $Y$ son adyacentes si y solo si $|X - Y| = 1$.

## El secreto de la Isla

En el corazón del vasto océano azul, existe una isla tropical conocida como La Isla de Coba, un lugar de exuberante vegetación y antigua sabiduría. La tribu que habita en esta isla ha vivido en armonía con la naturaleza durante siglos, guiados por un consejo de ancianos que custodian el equilibrio entre los habitantes de la isla y sus recursos.

Sin embargo, una nueva generación de líderes debe ser elegida, y para ello, los ancianos han planteado un desafío ancestral. Los aspirantes al consejo deben descubrir un grupo selecto de **guardianes**, quienes, colocados en puntos estratégicos de la isla, podrían vigilar a todos los aldeanos sin dejar a ninguno sin supervisión directa o indirecta.

La isla tiene una serie de aldeas unidas entre ellas por caminos. El reto es encontrar un grupo de guardianes tan pequeño como sea posible, de modo que cada aldea esté bajo la protección directa de un guardián, o al menos, esté conectada a una aldea donde se haya asignado un guardián.

Los jóvenes líderes deben resolver este desafío para mostrar su valía. Con cada nueva selección de guardianes, la estabilidad de la isla se estremece. El futuro de La Isla de Coba depende de que uno de los jóvenes (como tú) encuentre esta distribución óptima de guardianes y se convierta en el próximo jefe absoluto.

## Ciudades

El país de Coba ha evolucionado, ahora tiene inicialmente $N$ ciudades aisladas, donde la $i$-ésima ciudad tiene una significancia de $A_i$. El Anciano jefe de Coba quiere conectar todas las ciudades. Él puede construir una carretera bidireccional de longitud $L$ $(L > 0)$ desde la ciudad $X$ a la ciudad $Y$ si $(A_X \& A_Y \& L) = L$, donde $ \& $ representa el operador AND bit a bit.

¿Cuál es la longitud total mínima de las carreteras que tiene que construir para conectar todas las ciudades en Coba? Imprime $-1$ si es imposible.

Nota:

Se dice que la ciudad $X$ y la ciudad $Y$ están conectadas si existe una secuencia de ciudades $C_1, C_2, \dots, C_K$ $(K \geq 1)$ tal que $C_1 = X$, $C_K = Y$, y existe una carretera desde $C_i$ a $C_{i+1}$ $(1 \leq i < K)$. Todas las ciudades en Coba se dicen conectadas cuando cada par de ciudades en Coba está conectado.
