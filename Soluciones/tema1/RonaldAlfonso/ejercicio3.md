## 3.  Pila con `minimo` en $O(1)$ peor caso (C3)

**Estructura.** Cada entrada de la pila guarda un par $(x, m)$: el valor y el mínimo de todo lo que está desde el fondo hasta esa entrada.

```python
class PilaMin:
    def __init__(self):
        self.P = []                       # pares (valor, mínimo hasta aquí)
    def push(self, x):
        m = x if not self.P else min(x, self.P[-1][1])
        self.P.append((x, m))
    def pop(self):
        return self.P.pop()[0]
    def tope(self):
        return self.P[-1][0]
    def minimo(self):
        return self.P[-1][1]
```

**Invariante.** Si la pila tiene entradas $P[0], \dots, P[k-1]$ (desde el fondo), entonces para todo $i$:
$$P[i].m = \min(P[0].x, \dots, P[i].x).$$

- *Inicialización:* pila vacía, vale trivialmente.
- *`push(x)`:* las entradas viejas no cambian; la nueva tiene $m = \min(x, P[k-1].m) = \min(x, \min(P[0].x,\dots,P[k-1].x))$ por el invariante.
- *`pop`:* quitar el tope no cambia los prefijos que quedan.
- *Conclusión:* `minimo` devuelve $P[k-1].m$, que por el invariante es el mínimo de toda la pila.

**Costo.** Cada operación hace un número constante de pasos: un `min`, una lectura y una escritura. Memoria: $2n$ celdas para $n$ elementos.

**Detalle de peor caso.** El `append` de una lista dinámica es $O(1)$ *amortizado*, no en el peor caso (C4 §1). Para que cada operación sea $O(1)$ en el peor caso hay que usar una lista enlazada (cada nodo con valor, mínimo y puntero al de abajo) o un arreglo de capacidad fija conocida. Es exactamente la distinción del cierre de C4.

*Variante con menos memoria:* una pila auxiliar que solo guarda los mínimos, apilando $x$ cuando $x \le$ mínimo actual. La comparación tiene que ser $\le$ y no $<$: con $<$ falla con repetidos (apilar 1, 1 y desapilar uno deja la auxiliar vacía).

---