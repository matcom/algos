# Problemas

## Corrupción

Han pasado 20 años desde que Lidier se graduó de Ciencias de la Computación  
(haciendo una muy buena tesis) y las vueltas de la vida lo llevaron a convertirse  
en el presidente del Partido Comunista de Cuba. Una de sus muchas responsabilidades  
consiste en visitar zonas remotas. En esta ocasión debe visitar una  
ciudad campestre de Pinar del Río.

También han pasado 20 años desde que Marié consiguió su título en MATCOM.  
Tras años de viaje por las grandes metrópolis del mundo, en algún punto  
decidió que prefería vivir una vida tranquila, aislada de la urbanización, en una  
tranquila ciudad de Pinar del Río. Las vueltas de la vida quisieron que precisamente  
Marié fuera la única universitaria habitando la ciudad que Lidier se  
dispone a visitar.

Los habitantes de la zona entraron en pánico ante la visita de una figura tan  
importante y decidieron reparar las calles de la ciudad por las que transitaría  
Lidier. El problema está en que nadie sabía qué ruta tomaría el presidente y  
decidieron pedirle ayuda a Marié.

La ciudad tiene $n$ puntos importantes, unidos entre sí por calles cuyos  
tamaños se conoce. Se sabe que Lidier comenzará en alguno de esos puntos  
($s$) y terminará el viaje en otro ($t$). Los ciudadanos quieren saber, para  
cada par $s$, $t$, cuántas calles participan en algún camino de distancia mínima  
entre $s$ y $t$.

## Banco

Eduardo es el gerente principal de un gran banco. Tiene acceso ilimitado al sistema de bases de datos del banco y, con unos pocos clics, puede mover cualquier cantidad de dinero de las reservas del banco a su propia cuenta privada. Sin embargo, el banco utiliza un sofisticado sistema de detección de fraude impulsado por IA, lo que hace que robar sea más difícil.

Eduardo sabe que el sistema antifraude detecta cualquier operación que supere un límite fijo de M euros, y estas operaciones son verificadas manualmente por un número de empleados. Por lo tanto, cualquier operación fraudulenta que exceda este límite es detectada, mientras que cualquier operación menor pasa desapercibida.

Eduardo no conoce el límite M y quiere descubrirlo. En una operación, puede elegir un número entero X y tratar de mover X euros de las reservas del banco a su propia cuenta. Luego, ocurre lo siguiente.

Si X≤M, la operación pasa desapercibida y el saldo de la cuenta de Eduardo aumenta en X euros.  
De lo contrario, si X>M, se detecta el fraude y se cancela la operación. Además, Eduardo debe pagar X euros de su propia cuenta como multa. Si tiene menos de X euros en la cuenta, es despedido y llevado a la policía.  
Inicialmente, Eduardo tiene 1 euro en su cuenta. Ayúdalo a encontrar el valor exacto de M en no más de 105 operaciones sin que sea despedido.

Entrada:
Cada prueba contiene múltiples casos de prueba. La primera línea contiene el número de casos de prueba t (1≤t≤1000).

Para cada caso de prueba, no hay entrada previa a la primera consulta, pero puedes estar seguro de que M es un número entero y 0≤M≤1014.

Salida:
Para cada caso de prueba, cuando sepas el valor exacto de M, imprime una única línea con el formato "! M". Después de eso, tu programa debe proceder al siguiente caso de prueba o terminar, si es el último.

## Rompiendo amistades

Por algún motivo, a José no le gustaba la paz y le irritaba que sus compañeros de aula se llevaran tan bien. Él quería ver
el mundo arder. Un día un demonio se le acercó y le propuso un trato: "A cambio de un cachito de tu alma, te voy a dar el poder para
romper relaciones de amistad de tus compañeros, con la única condición de que no puedes romperlas todas". Sin pensarlo mucho (Qué más
da un pequeño trocito de alma), José aceptó y se puso a trabajar. Él conocía, dados sus k compañeros de aula, quiénes eran mutuamente
amigos.

Como no podía eliminar todas las relaciones de amistad, pensó en qué era lo siguiente que podía hacer más daño. Si una persona quedaba con
uno o dos amigos, podría hacer proyectos en parejas o tríos (casi todos los de la carrera son así), pero si tenía exactamente tres amigos,
cuando llegara un proyecto de tres personas, uno de sus amigos debería quedar afuera y se formaría el caos.

Ayude a José a saber si puede sembrar la discordia en su aula eliminando relaciones de amistad entre sus compañeros de forma que todos queden, o bien sin amigos, o con exactamente tres amigos.
