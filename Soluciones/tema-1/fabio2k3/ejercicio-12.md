# Solución Ejercicio 12 ( Gale Shapley)

Tenemos n proponentes y n receptores. Cada proponente a tiene una lista estricta e incompleta L(a) de receptores, de mejor a peor, y prefiere quedarse solo antes que con uno que listó

Vamos a definir nuestro emparejamiento M:
Cada proponente queda solo o con un receptor de L(a) y cada receptor tiene a lo sumo un proponente. Ya no tiene por qué ser perfecto.

Un par (a,b) con M(a) != b es bloqueante si:
1. b pertenece a L(a)
2. a prefiere b a su situación en M, es decir está solo o ranquea b por encima de M(a)
3. b prefiere a  a su situación, está solo o ranquea a por encima de M(b)

m es estable si no tienen pares bloqueantes. La 1ra condición es lo que cambia => un receptor que a no listó nunca puede bloquear con a, porque a prefiere quedarse solo.

DEfinamos nuestro algoritmo (adaptado)
---------------------------------------

Cada proponente a mantiene siguiente[a], el lugar de L(a) al que va a proponer:

Mientras haya un proponente libre a:

- Si siguiente[a] = !L(a)!, la lista se agotó y a se queda solo, es decir sale del juego.
- Si no, a le propone a b = L(a)[siguiente[a]] y avanza siguiente[a]. Si b está libre, acepta. Si ya tiene pareja y prefiere a a, lo acepta y su pareja anterior queda libre, si no rechaza a a.

Terminación:
------------

Q = Σ (|L(a)| - siguiente[a]), el número de propuestas posibles que aún no se hicieron.

Empieza en m = Σ|L(a)| <= n^2, es un entero >= 0, y cada propuesta lo baja exactamente en 1, porque siguiente[a] solo avanza no se repite ninguna.

Descartar a un proponente de lista agotada no cambia Q, pero un descartado nunca vuelve a quedar libre y eso ocurre a lo sumo n veces.

=> Hay a lo sumo m propuestas y n descartes, el ciclo termina

Invariantes:
------------
- R: un receptor una vez que recibe una propuesta, nunca vuelve a quedar libre y su pareja solo mejora en su lista.
- P: un proponente propone en orden de su lista, sin repetir, si a termina solo, agotó su lista, es decir, le propuso a todo b que pertenece a L(a).

Ahora nos podemos preguntar, ¿sigue siendo estable el resultado? Pues sí y veamos porqué:

Teorema: el emparejamiento M que devuelve el algoritmo es estable, para cualquier orden de ejecución.

Primero M es válido, cada a solo propone a receptores de L(a) así que nadie queda con un receptor que no listó.

Supongamos que (a,b) es bloqueante, veamos que a le propuso a b:

- Si a termina solo, por (P) agotó su lista, así que le propuso a todo receptor de L(a), incluido b.

- Si a termina con M(a) != b y ranquea b por encima de M(a), por (P) le propuso a b antes que a M(a).


Como a no terminó con b, b dejó de tener a a, lo que rechazó al llegar, o lo aceptó y luego lo reemplazó. En ambos casos, justo después b tenía una pareja b' que ranquea por encima de a. Por (R), b no vuelve a quedar libre y su pareja final M(b) ranquea igual o mejor b', es decir, por encima a. Entonces b no está solo y prefiere M(b) a a, lo que CONTRADICE la condición 3 vista anteriormente de que (a, b) bloquea.