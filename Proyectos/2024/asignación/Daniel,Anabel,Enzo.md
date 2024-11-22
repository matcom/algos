# Problemas

## El secreto de la Isla

En el corazón del vasto océano azul, existe una isla tropical conocida como La Isla de Coba, un lugar de exuberante vegetación y antigua sabiduría. La tribu que habita en esta isla ha vivido en armonía con la naturaleza durante siglos, guiados por un consejo de ancianos que custodian el equilibrio entre los habitantes de la isla y sus recursos.

Sin embargo, una nueva generación de líderes debe ser elegida, y para ello, los ancianos han planteado un desafío ancestral. Los aspirantes al consejo deben descubrir un grupo selecto de **guardianes**, quienes, colocados en puntos estratégicos de la isla, podrían vigilar a todos los aldeanos sin dejar a ninguno sin supervisión directa o indirecta.

La isla tiene una serie de aldeas unidas entre ellas por caminos. El reto es encontrar un grupo de guardianes tan pequeño como sea posible, de modo que cada aldea esté bajo la protección directa de un guardián, o al menos, esté conectada a una aldea donde se haya asignado un guardián.

Los jóvenes líderes deben resolver este desafío para mostrar su valía. Con cada nueva selección de guardianes, la estabilidad de la isla se estremece. El futuro de La Isla de Coba depende de que uno de los jóvenes (como tú) encuentre esta distribución óptima de guardianes y se convierta en el próximo jefe absoluto.

## Distancia de árboles

Un árbol se define como un grafo no dirigido y conectado con $n$ vértices y $n-1$ aristas. La distancia entre dos vértices en un árbol es igual al número de aristas en el camino simple único entre ellos.

Se te dan dos enteros $x$ y $y$. Construye un árbol con las siguientes propiedades:

- El número de pares de vértices con una distancia par entre ellos es igual a $x$.
- El número de pares de vértices con una distancia impar entre ellos es igual a $y$.

Por par de vértices, nos referimos a un par ordenado de dos vértices (posiblemente, el mismo o diferente).

## Torneo

Tan pronto como comienza el toreno de programación competitiva, tu experimentado equipo de $3$ personas se da cuenta inmediatamente de que este presenta $a$ problemas fáciles, $b$ problemas medianos, y $c$ problemas difíciles. Resolver un problema les tomará a cualquiera de ustedes $2$, $3$ o $4$ unidades de tiempo, dependiendo de si el problema es fácil, mediano o difícil. Independientemente de la dificultad del problema, la última unidad de tiempo gastada en resolverlo debe gastarse utilizando la computadora compartida.

Tu equipo organiza sus esfuerzos de manera que cada uno de ustedes comienza (y termina) resolviendo problemas en unidades de tiempo enteras. Cualquier problema dado solo puede ser resuelto por un concursante; requiere una cantidad continua de tiempo (que depende de la dificultad del problema). Ninguno de los $3$ puede resolver más de un problema a la vez, pero pueden comenzar a resolver un nuevo problema inmediatamente después de terminar uno. De manera similar, la computadora compartida no puede ser utilizada por más de uno de ustedes al mismo tiempo, pero cualquiera de ustedes puede comenzar a usar la computadora (para completar el problema que se está resolviendo actualmente) inmediatamente después de que alguien más deje de usarla.

Dado que el concurso dura $l$ unidades de tiempo, encuentra el número máximo de problemas que tu equipo puede resolver. Además, encuentra una forma de resolver el número máximo de problemas.
