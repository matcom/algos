# Ejercicio 5: detección de ciclos de Floyd

> Detección de ciclos en una lista enlazada con dos punteros que avanzan a velocidades 1 y 2 (algoritmo de Floyd). Demuestra que se encuentran si y solo si hay un ciclo, con un invariante, y que termina, con un potencial. Da el costo. (C3)

## El problema y el algoritmo

En una lista enlazada cada nodo apunta al siguiente. Puede terminar en `None`, o tener un ciclo: el último nodo apunta a uno anterior y la lista no termina nunca.

```
A → B → C → D → E
        ↑       ↓
        H ← G ← F
```

Queremos decidir si hay ciclo sin saber cuántos nodos hay y sin guardar los nodos visitados.

```python
def tiene_ciclo(inicio):
    tortuga = liebre = inicio
    while liebre is not None and liebre.siguiente is not None:
        tortuga = tortuga.siguiente              # avanza 1
        liebre = liebre.siguiente.siguiente      # avanza 2
        if tortuga is liebre:
            return True      # se encontraron: hay ciclo
    return False             # la liebre llegó al final: no hay ciclo
```

Numero los nodos según el camino desde el inicio: el nodo 0 es el inicio, el nodo k es al que se llega con k pasos. Si hay ciclo, μ es la cantidad de nodos antes de entrar al ciclo y λ la cantidad de nodos del ciclo (en el dibujo, μ = 2 y λ = 6). La lista tiene n = μ + λ nodos.

## Invariante

> Después de t vueltas, la tortuga está en el nodo t y la liebre en el nodo 2t.

**Inicialización.** Con t = 0, los dos están en el nodo 0.

**Mantenimiento.** En cada vuelta la tortuga avanza 1 (del nodo t al t + 1) y la liebre avanza 2 (del nodo 2t al 2t + 2 = 2(t + 1)).

## Si no hay ciclo, no se encuentran

Sin ciclo, todos los nodos del camino son distintos: el nodo número t y el nodo número 2t son el mismo solo si t = 2t, o sea, t = 0. Por el invariante, después de t ≥ 1 vueltas la tortuga está en el nodo t y la liebre en el 2t, que es más adelante: nunca coinciden. La liebre avanza 2 por vuelta en una lista finita, así que llega a `None` (o al último nodo) en a lo sumo n/2 vueltas, y el algoritmo dice False. Correcto.

## Si hay ciclo, se encuentran

Con ciclo, la liebre nunca llega a `None`, así que el algoritmo solo puede terminar cuando se encuentran, y hay que demostrar que eso pasa.

Cuando la tortuga llega al ciclo (en la vuelta t = μ), la liebre ya está dentro, porque va por delante. Desde ahí los dos dan vueltas en la pista circular.

**Potencial.** d = cuántos nodos le faltan a la liebre para alcanzar a la tortuga, contando hacia adelante por el ciclo. Es un entero entre 0 y λ − 1.

En cada vuelta la tortuga se aleja 1 y la liebre se acerca 2, así que **d baja exactamente 1**. Cuando d llega a 0, la liebre alcanzó a la tortuga: están en el mismo nodo y el algoritmo dice True. Correcto.

Que baje exactamente 1 importa: si bajara de 2 en 2, la liebre y la tortuga podrían no encontrarse. Por ejemplo, con d = 3 sería 3 → 1 → −1: la liebre se saltaría el 0 y pasaría por encima de la tortuga sin caer en el mismo nodo. Bajando de 1 en 1, pasa sí o sí por 0.

## Terminación y costo

- Sin ciclo: a lo sumo n/2 vueltas.
- Con ciclo: μ vueltas para que la tortuga llegue al ciclo, y desde ahí d ≤ λ − 1 baja 1 por vuelta. El algoritmo solo compara después de mover, así que el caso μ = 0 (los dos empiezan juntos dentro del ciclo, d = 0 sin comparar) cuesta una vuelta completa: λ vueltas. En todos los casos, a lo sumo μ + λ = n vueltas.

**Tiempo O(n)**, con un número constante de operaciones por vuelta. **Memoria O(1)**: la lista es la entrada y no cuenta; el algoritmo solo crea dos punteros. Esa es la gracia de Floyd: la forma obvia de detectar un ciclo es guardar los nodos visitados en un conjunto, con memoria O(n).

## Experimentos

`ej05_floyd.py` construye listas con μ nodos antes del ciclo y un ciclo de λ nodos (λ = 0 sin ciclo). En 3000 listas al azar comprueba la respuesta, el invariante en cada vuelta (tortuga = nodo t, liebre = nodo 2t), que el potencial d baja exactamente 1 por vuelta una vez que la tortuga está en el ciclo, y que las vueltas no pasan de la cota. Sin fallos. Algunos casos:

```
    mu  lambda      n  pasos
     0       1      1      1
     0      10     10     10
    10       0     10      5
    10       1     11     10
     2       6      8      6
   100     100    200    100
   500       3    503    501
     3     500    503    500
  1000       0   1000    500
```

Sin ciclo son n/2 vueltas, y con ciclo nunca más de μ + λ = n. El caso μ = 0, λ = 10 hace exactamente λ vueltas, por lo que se explica arriba.

---
*Declaración de uso de IA: usé un asistente de IA (Claude) para escribir el código de experimentación, y como tutor (explicaciones, pistas y corrección de mi redacción). Las demostraciones son mías.*
