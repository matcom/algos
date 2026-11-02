# Solución ejercicio 5

Tenemos una lista enlazada con una cierta cantidad de nodos n, donde cada nodo tiene un nodo siguiente o None. Tenemos que decidir si algún nodo se repite al seguir los siguientes desde head.

Nuestro algoritmo sería:

def floyd(head):
    t = h = head

    while h is not None and h.next is not None:
        t = t.next
        h = h.next.next
        
        if t is h:
            return True

    return False

x_i es el nodo al que se llega tras i pasos desde head. Si hay ciclo, "p" es la longitud de la cola, es decir los nodos antes del ciclo, y λ la del ciclo, por ende: n = p + λ

Sin ciclos los nodos x_0, x_1, ..., X_[n-1] son distintos y x_n = None. 
Y si hay ciclos x_i está definido para todo i, un nodo de la cola se visita una sola vez y x_a = x_b con a < b si y solo si a >= p y λ | (b - a)

Definamos nuestra invariante I:

I => i iteraciones sin haber devuelto True, t  = x_i y h = x_[2i]

1- Con i = 0, t = h = x_0 que es head

2- La guarda del ciclo asegura que h y h.next no son None, así que t.next = x_[i+1] y h.next.next = x_[2i + 2] están definidos. Con (i + 1) iteraciones, t = x_[i+1] y h = x_[2(i+1)].

3- Si el algoritmo devuelve True tras i >= 1 iteraciones, entonces x_i = x_[2i]

Analicemos la correctitud del algoritmo: Devuelve true <=> hay ciclo:

(=>) Si devuelve True hay ciclo: Por I, x_i = x_[2i] con i >= 1, es decir que un mismo nodo se visita dos veces en dos tiempos distintos. Sin ciclo todos los x_k son distintos, así que hay ciclo.

(<=) Si hay ciclo, devuelve True: con ciclo, h nunca llega a ser None, así que el ciclo while solo termina devolviendo True

Analicemos ahora cuándo ocurre:
Sea i >= 1. Si i < p, x_i es un nodo de la cola, que solo se visita en el tiempo i, y 2i != i por ende x_[2i] != x_i. Si i >= p, por la propiedad de la notación x_i = x_[2i] si y solo si λ | i. Luego el 1er i con t = h es:

i' = λ ⌈max(p, 1) / λ⌉  que existe siempre, En la iteración i' el algoritmo devuelve True.

Potencial:
- Con ciclo: Q = i' - i es un entero que baja una unidad es decir 1 por iteración y llega a 0 en la iteración que devuelve True.
- Sin ciclo: W = número de nodos desde h hasta el final, es un entero mayor o igual a cero. El ciclo while exige que Q >= 2, y cada iteración avanza h 2 nodos, así que W baja exactamente en 2, por lo tanto hay a lo sumo ⌊n / 2⌋ iteraciones y el algoritmo devuelve False.

Costo de nuestro algoritmo
--------------------------
- Sin ciclo a lo sumo ⌊n / 2⌋ iteraciones
- Con ciclo: i' = λ*⌈max(p, 1) / λ⌉ <= p + λ = n iteraciones.

Tiempo O(n), memoria O(1). La alternativa de guardar los nodos visitados también nos da O(n), en el tiempo pero con memoria O(n).

