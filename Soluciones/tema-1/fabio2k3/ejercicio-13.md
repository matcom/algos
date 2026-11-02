# Solución del Ejercicio 13

El árbol empieza como un camino con n nodos. Se accede a las claves 1, 2, ...,n en orden, haciendo splay en cada una, el costo real de un acceso es el número de rotaciones con mínimo 1.

Cota con el lema de acceso:
---------------------------

Rango r(x) = log2 s(x), con s(x) el número de nodos del subárbol de x. 
Potencial Q = Σ r(x)

Lema de acceso => hacer splay de x en un árbol con raíz t cuesta amortizado a lo sumo 3*(r(t) - r(x)) + 1.

. El árbol siempre tiene n nodos, por lo que r(t) = log2n, en cada acceso. Como r(x) >= 0, cada acceso cuesta amortizado a lo sumo 3*log2(n) + 1.

. Sumando los n accesos, el potencial se reduce a: Σ amortizado + Q_0 - Q_n <= n*(3*log2(n) + 1) + Q_0 - Q_n

. La condición Q_n >= Q_0, aquí no se cumple, porque el camino inicial tiene potencial alto. Se paga aparte, una sola vez, un camino de n nodos tiene rangos log2 1, ..., log2 n, así que Q_0 = log2 (n!) <= n*log2(n). Además Q_n >= 0.

. Por lo tanto => Σ costo real <= 4*n* log2(n) + n = O(n*logn)

Ahora comparemos con lo medido en la conferencia (sección 6):
-------------------------------------------------------------

En esta se mide esta secuencia, para splay obtiene unas 4,2 rotaciones por acceso con n = 100 y 4,4 con n = 800, el costo por acceso es una constante que prácticamente no crece con n.

Por ende el total medido es Θ(n). La cota del lema da O(nlogn), y por acceso permite hasta 3*log2 n + 1, que serían unas 30 rotaciones para n = 800, es decir poco más de SIETE veces de lo que se mide.



Por lo que nos podemos preguntas, ¿es ajustada la cota?

Respuesta, Nope. Esta es correcta pero está sobrada por un factor O(logn)

- Cota inferior: cada acceso cuesta al menos 1, así que el total es Ω(n).
- Lo medido => Θ(n)
- Obtenido por el lema: O(n log n)

El lema pierde precisión porque acota cada acceso r(t) - r(x) <= log n, y no aprovecha la estructura de la secuencia. 

Por ende el lema de acceso da O(nlogn) para acceder a 1, ...,n en orden desde un camino. Lo medido en la sección 6 de nuestra conferencia es Θ(n), así que la cota es válida pero no se ajusta, ya que tiene una diferencia de O(logn).
Por lo tanto el lema es una garantía para cualquier secuencia, y por eso pierde precisión en esta secuencia concreta. 