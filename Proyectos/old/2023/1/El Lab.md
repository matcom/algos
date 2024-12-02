
El Bar

En un bar se controla la entrada de personas diaria durante una cantidad determinada de días. En lo adelante, la administración del bar se refiere a la cantidad de personas que entran, en relación a la media durante ese período, por ej si un día entran 5 personas más que la media calculada se registra como '5', si entran 10 personas menos que la media ya calculada se registra '-10' (esta media no se actualiza). 

La administración del bar tiene un registro de la asistencia durante n días consecutivos, que ha sido registrada de la forma antes mencionada, y se ha visto que la asistencia al bar en la segunda mitad analizada fue la misma cada día.

El dueño del bar va a hacerle una auditoría a la administración para saber si todo marcha bien, de la siguiente forma: El administrador le dirá un número k, y el dueño elegirá k días aleatorios de la lista de n días, si el total de personas que ha ido en total en todos esos días es positivo con respecto a la media anterior concluirá que el bar marcha bien, de lo contrario, mal.

El administrador lo contrata a usted para que lo ayude como científico que se considera..., que k debe elegir el administrador, para que, siempre que sea posible, el dueño del bar le dé el visto bueno?



MineCraft

En el juego de MineCraft una de las principales distracciones es la construccion, los mejores jugadores logran hacer monumentos imponentes que sorprenden a todos. Actualmente se esta llevando a cabo un torneo de construcción en el juego, donde la tarea es hacer un muro. Un muro es, como sabemos, una ilera de columnas de bloques de piedra, todos de la misma altura. En MineCraft, para llevar a cabo esta tarea hay 3 movimientos válidos: 

- sacar un bloque de piedra del inventario y aumentar la altura de la columna en cuestion en 1 de altura
- destruir un bloque de piedra de una columna y disminuir la altura de la columna en cuestion en 1 de altura
- mover un bloque de piedra de una columna a otra, aumentando la altura de la 2da columna y disminuyendo la de la 1ra en 1 de altura cada una.

Se sabe que hacer cada movimiento consume c, d y m de energia respectivamente, y que en los inventarios de los jugadores hay suficienues bloques de piedra siempre. Los jugadores comienzan a jugar con un muro a medio hacer aleatorio, osea, se les da una cantidad n de columnas de bloques de piedra en ilera, de disímiles tamaños y el ganador del torneo será el que construya un muro de largo n utilizando la menor cantidad de energia, no se permite crear columnas nuevas ni dejar huecos de antiguas columnas en el muro porsupuesto.

Elabore una estrategia que asegure que para cualquier muro inicial a medio hacer con que comience, usted logrará hacer el muro pedido utilizando la menor cantidad de energia posible.


El Zoologico

En un zoológico un poco especial, a los animales se les separa en dos habitats diferentes de manera general. El habitat para la reproducción, que solo acepta animales de la misma especie, y el habitat para la maduración, que admite animales de distintas especies, pero no de géneros distintos. El zoológico está pasando por una remodelación ya que va a recibir n especies distintas de animales, cada una con un número 'a' de hembras y 'b' de machos, que puede ser distinto entre cada especie. En la remodelación se está pensando en construir salas de exhibición de los animales, cada una se construirá para ser un habitat de reproducción o de maduración, y cada sala podrá soportar un máximo de k animales, igual para todas las salas.
Como el zoológico necesita ser rentable y cada sala se cobra por separado, se quiere construir el máximo número posible de salas que cumplan con los requerimientos planteados y que, además, estén llenas de animales, para el disfrute de los visitantes. Cuantas salas deberá construir el zoológico?


El Lab

En un laboratorio de la BIOFAM quieren modificar genéticamente una gallina para que sea más resistente a las enfermedades. Para esto deben de cambiar la secuencia de aminoácidos presentes en su genoma. La secuencia que quieren reproducir es la de los cocodrilos, que se sabe que son animales que han existido por millones de años. Entonces, dado que una secuencia de aminoácidos se puede codificar como una secuencia de caracteres se tiene: 
T - la secuencia de aminoácidos de los cocodrilos, de tamaño m
S - la secuencia de aminoácidos de la gallina original, de tamaño n
A - la secuencia de aminoácidos de la galllina a crear (inicialmente vacía)

Para lograr que la gallina modificada adquiera la resistencia de un cocodrilo se sabe que su secuencia de aminoácidos A, debe contener como prefijo a T. Como en la BIOFAM hubo recortes de presupuesto solo cuentan con una máquina que puede hacer dos modificaciones genéticas:
1 - Extrae y elimina el primer aminoácido de S y lo coloca al principio de A
2 - Extrae y elimina el primer aminoácido de S y lo coloca al final de A

Encuentre la cantidad de secuencias de operaciones posibles tales que la gallina geneticamente modificada sea resistente a las enfermedades.

La Pelota

Para un campeonato de Pelota el Manager debe elegir a su equipo de p jugadores y, en este caso, podrá elegir a k espectadores especiales para que suban la moral del equipo. El manager conoce, de cada jugador i de los n a elegir, el valor que aporta a la moral del equipo a_i, y el valor que aporta jugando en la posición j, s_i,j. Determine una alineación entre jugadores en el campo y espectadores de forma que el equipo tenga la mayor cantidad de valor acumulado posible.

Los Espías

Durante la segunda guerra mundial una parte importante de la información era transmitida en cartas encriptadas en buzones públicos que eran depositadas en estos por espias. Funcionaba de la siguiente manera:
- En la ciudad solo había un buzón usado para temas militares que era compartido para todas estas operaciones.
- En un período dos generales hacían cada uno una lista de órdenes: s y t, de tamaños cualesquiera.
- La lista de órdenes de un general era una secuencia de comandos, cada uno podía ser de enviar información o de ir al buzon a recogerla, ej L1: r,r,e,r ; L2: e,e,r (para r: recoger y e: enviar)
- Si cuando un espía iba al buzón a recoger información se encontraba varias cartas, solo recogía una. 
- Si cuando un espía iba al buzón a recoger información, no encontraba nada, le reportaba al general como un posible caso de información filtrada y se daba la orden de fusilar a todos los implicados.
- Si al finalizar el período quedan cartas en el buzón, un cartero común las lee, y se da un caso de información filtrada y se fusila a todos los implicados también.

Usted es un mediador de paz, por tanto su tarea es construir una lista de ordenes que contenga las listas de los dos generales, agregando la menor cantidad de ordenes posibles (al principio en el medio o al final), ya sea de enviar o recoger información, de manera que no fusilen a nadie.


