## 5.  Algoritmo de Floyd: detección de ciclos (C3)

**El problema.** Sea $x_0$ la cabeza y $x_{i+1} = \texttt{next}(x_i)$. O la sucesión llega a `None` (sin ciclo, la lista tiene $L$ nodos), o, como `next` es una función sobre un conjunto finito, es eventualmente periódica: hay una cola de largo $\mu \ge 0$ y un ciclo de largo $\lambda \ge 1$ con $x_i = x_{i+\lambda}$ para todo $i \ge \mu$, y $x_0, \dots, x_{\mu+\lambda-1}$ distintos. Total de nodos $n = \mu + \lambda$.

```python
def hay_ciclo(cabeza):
    t = l = cabeza                       # tortuga y liebre
    while l is not None and l.next is not None:
        t, l = t.next, l.next.next
        if t is l:
            return True
    return False
```

**Invariante.** Después de $k$ vueltas sin devolver: $t = x_k$, $l = x_{2k}$, y $x_j \ne x_{2j}$ para $1 \le j \le k$. La inicialización ($k = 0$) es inmediata y el mantenimiento es leer el código.

**Correctitud parcial ("si y solo si").**

- Si devuelve `True`, en la vuelta $k \ge 1$ se tiene $x_k = x_{2k}$ con $k < 2k$: un nodo se repite, y como `next` es función, desde ahí la sucesión es periódica. Hay ciclo.
- Si devuelve `False`, algún $x_{2k+1}$ o $x_{2k+2}$ es `None`: la lista se termina, no hay ciclo.
- Recíprocamente, si no hay ciclo todos los $x_i$ son distintos y nunca se cumple `t is l`; y si hay ciclo, la liebre nunca encuentra `None`. Así que cuando el algoritmo termina, su respuesta es la correcta.

**Terminación, con un potencial.**

- *Sin ciclo:* $\Phi = L - 2k$. La liebre avanza 2 por vuelta y la vuelta solo ocurre si $x_{2k+2}$ existe, o sea $2k+2 \le L-1$. $\Phi$ baja en 2 cada vuelta y está acotado por abajo: a lo sumo $\lfloor (L-1)/2 \rfloor$ vueltas.
- *Con ciclo:* mientras la tortuga no entró al ciclo ($k < \mu$), $\Phi_k = (\mu - k) + \lambda$. Una vez dentro ($k \ge \max(\mu,1)$), $\Phi_k = d_k$, la distancia que la liebre tiene que avanzar por el ciclo para alcanzar a la tortuga: $d_k \equiv (k - 2k) = -k \pmod \lambda$, con $0 \le d_k < \lambda$. En cada vuelta la tortuga avanza 1 y la liebre 2, así que la liebre gana una posición: $d_{k+1} = d_k - 1$. Al cruzar de $k = \mu - 1$ (donde $\Phi = \lambda + 1$) a $k = \mu$ (donde $\Phi \le \lambda - 1$) también baja. Es entero, no negativo y baja en cada vuelta; cuando vale 0, $t = l$ y el ciclo termina.

**Costo.** Con ciclo, se encuentran en el primer $k \ge \max(\mu, 1)$ múltiplo de $\lambda$, que es $\le \mu + \lambda = n$ (si $\mu \ge 1$, el primer múltiplo de $\lambda$ que es $\ge \mu$ es $< \mu + \lambda$; si $\mu = 0$, es $\lambda$). Sin ciclo, $\le L/2$ vueltas. Cada vuelta mueve 3 punteros. **Tiempo $O(n)$, memoria $O(1)$** (dos punteros, frente a la tabla hash de nodos visitados, que cuesta $O(n)$ memoria).

---