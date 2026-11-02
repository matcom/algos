

**Enunciado.** Detección de ciclos en una lista enlazada con dos punteros que avanzan a velocidades 1 y 2 (algoritmo de Floyd). Demostrar que se encuentran si y solo si hay un ciclo, con un invariante, y que termina, con un potencial. Dar el costo.

**Modelo.** La lista se da por su puntero a la cabeza (`head`). Lo único que se puede hacer con un nodo es leer su `next`, y cada lectura cuesta 1.

## Algoritmo

Un puntero lento avanza un nodo por iteración y uno rápido avanza dos. Si la lista termina, el rápido llega al final primero y no hay ciclo. Si hay un ciclo, el rápido entra antes, da vueltas, y acaba alcanzando al lento, como dos corredores en una pista circular con velocidades distintas.



```python
class Node:
    def __init__(self, value):
        self.value = value
        self.next = None


def has_cycle(head):
    slow = head
    fast = head
    while fast is not None and fast.next is not None:
        slow = slow.next
        fast = fast.next.next
        if slow is fast:
            return True
    return False
```

## Notación

Sea $x_0 = \texttt{head}$ y $x_{i+1} = x_i.\texttt{next}$, mientras $x_i$ no sea nulo. Es el recorrido de la lista. Dos casos:

- **Sin ciclo**: hay $n$ nodos y $x_0, \dots, x_{n-1}$ son todos distintos; $x_n$ es nulo.
- **Con ciclo**: el recorrido es infinito. Sea $\mu$ el número de nodos antes del ciclo y $\lambda$ la longitud del ciclo. Entonces $x_0, \dots, x_{\mu+\lambda-1}$ son distintos y, para $i \ge \mu$, $x_i$ solo depende de $(i - \mu) \bmod \lambda$. En total hay $n = \mu + \lambda$ nodos distintos.

## Correctitud parcial

**Invariante.** Al comienzo de la iteración $k$ ($k = 0, 1, \dots$):

1. `slow` $= x_k$ y `fast` $= x_{2k}$ (ambos no nulos);
2. para todo $1 \le j \le k$, $x_j \ne x_{2j}$ (si no, ya habríamos devuelto `True`).

*Inicialización.* Con $k = 0$ los dos son $x_0$ y la condición 2 es vacía.

*Mantenimiento.* Si el ciclo entra en la iteración $k$, es porque `fast` y `fast.next` no son nulos, o sea $x_{2k}$ y $x_{2k+1}$ existen. Después del cuerpo, `slow` $= x_{k+1}$ y `fast` $= x_{2k+2}$ (puede ser nulo). Si `slow is fast`, se devuelve `True` y terminamos. Si no, $x_{k+1} \ne x_{2(k+1)}$, que es la condición 2 con $j = k+1$. Como $k + 1 \le 2k + 1$, `slow` no es nulo, y la condición 1 se mantiene mientras `fast` no sea nulo; si lo es, el ciclo termina en la guarda siguiente.

*Conclusión.* Veamos las dos salidas.

- **Si devuelve `True`** en la iteración $k$: $x_k = x_{2k}$ con $k \ge 1$, o sea $k \ne 2k$. El recorrido pasa dos veces por el mismo nodo, y eso solo ocurre si hay un ciclo (sin ciclo los $x_i$ son distintos).
- **Si devuelve `False`**: `fast` o `fast.next` es nulo, o sea algún $x_i$ es nulo. El recorrido es finito, así que no hay ciclo.

Entonces, si el algoritmo devuelve, la respuesta es correcta. Falta ver que siempre devuelve (y que con ciclo devuelve `True`).

**Con ciclo, se encuentran.** Sea $k^*$ el menor múltiplo de $\lambda$ que cumple $k^* \ge \mu$ y $k^* \ge 1$. Entonces $2k^* - k^* = k^*$ es múltiplo de $\lambda$ y ambos índices son al menos $\mu$, así que
$$x_{2k^*} = x_{k^*}.$$
Por lo tanto el primer $k$ con $x_k = x_{2k}$ existe y cumple $k \le k^*$. Además
$$k^* \le \max(\lambda,\ \mu + \lambda - 1) \le n.$$
Y como el recorrido es infinito, ningún $x_i$ es nulo, así que el ciclo nunca sale por la guarda. Con ciclo, el algoritmo devuelve `True`.

**Sin ciclo, no se encuentran** (porque los $x_i$ son distintos) y el algoritmo devuelve `False`. Es la equivalencia pedida: se encuentran si y solo si hay un ciclo.

## Terminación

Un potencial que baja en cada iteración:

- **Sin ciclo.** $\Phi_k = n - 1 - 2k$, el número de nodos que quedan después de `fast`. Baja en 2 por iteración. El ciclo exige que `fast.next` exista, es decir $\Phi_k \ge 1$, así que se ejecuta a lo sumo $\lceil (n-1)/2 \rceil$ veces.
- **Con ciclo.** $\Phi_k = k^* - k$. Baja en 1 por iteración y, al llegar a 0, `slow is fast` es cierto y se devuelve `True`. Este potencial usa $k^*$, que depende de la lista y no del estado del algoritmo, y eso es legítimo en una demostración de terminación.

En ambos casos el potencial es un entero no negativo que baja estrictamente, así que el algoritmo termina.

## Complejidad temporal

Cada iteración hace 3 lecturas de `next` y una comparación: $O(1)$.

- Sin ciclo: a lo sumo $\lceil (n-1)/2 \rceil$ iteraciones.
- Con ciclo: a lo sumo $k^* \le n$ iteraciones.

**Tiempo $\Theta(n)$ en el peor caso y espacio extra $O(1)$** (dos punteros).

## ¿Se puede hacer mejor?

**En tiempo, no (en este modelo): hace falta $\Omega(n)$.** Argumento de adversario. Supón una lista simple de $n$ nodos. El algoritmo descubre los nodos de uno en uno siguiendo punteros, y el adversario no se compromete con el `next` del último nodo hasta que el algoritmo lo lea. Antes de leerlo, hay dos listas consistentes con todo lo visto: una donde el último `next` es nulo (no hay ciclo) y otra donde apunta a `head` (hay ciclo). La respuesta correcta es distinta, así que el algoritmo necesita leer ese `next`, y para llegar al último nodo hacen falta $n - 1$ lecturas antes. En total, al menos $n$ lecturas de `next`.

**En memoria,** la alternativa obvia (guardar los nodos visitados en un conjunto) usa $\Theta(n)$ de espacio. Floyd usa $O(1)$.

El algoritmo coincide con la cota mínima de tiempo, $\Theta(n)$, y usa espacio constante, así que es óptimo en ambos recursos para este modelo.
.
