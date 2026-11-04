## 9.  La mezcla "optimizada" (C5)

```python
def mezcla_optimizada(I, D):
    R, i, j = [], 0, 0
    while i < len(I) and j < len(D):
        if len(I) - i == 1:               # le queda uno: dejar de comparar
            return R + D[j:] + [I[i]]
        if I[i] <= D[j]: R.append(I[i]); i += 1
        else:            R.append(D[j]); j += 1
    return R + I[i:] + D[j:]
```

**Peor caso: $2n - 2$ comparaciones.** Cada comparación saca un elemento. Al terminar el ciclo quedan al menos dos elementos sin sacar por comparación: si paró porque a $I$ le queda uno, a $D$ le queda al menos uno; si paró porque $D$ se vació, la última comparación sacó un elemento de $D$ cuando a $I$ le quedaban al menos dos. Así que hay a lo sumo $2n - 2$ comparaciones, y se alcanzan, por ejemplo, con $I = [n, n+1, \dots, 2n-2, 2n]$ y $D = [1, \dots, n-1, 2n-1]$: $n-1$ comparaciones sacan $1, \dots, n-1$, otras $n-1$ sacan $n, \dots, 2n-2$, y a $I$ le queda el $2n$.

**Decisión sin probarla (C5 §6 y §8).** Mezclar dos listas ordenadas de largo $n$ requiere $2n - 1$ comparaciones en el peor caso, en el modelo de comparaciones. Este algoritmo es de ese modelo y nunca hace más de $2n - 2$. **Es incorrecto.**

**La entrada en la que falla, construida con el adversario de C5 §6.** El adversario contesta como si la entrada fuera la intercalada perfecta
$$a_1 < b_1 < a_2 < b_2 < \cdots < a_n < b_n, \qquad I = (a_k),\ D = (b_k).$$
El algoritmo compara $(a_1,b_1), (b_1, a_2), \dots, (a_{n-1}, b_{n-1})$, que son $2n - 3$ comparaciones, saca $a_{n-1}$, ve que a $I$ le queda solo $a_n$ y para. **Nunca comparó los pares vecinos $(b_{n-1}, a_n)$ ni $(a_n, b_n)$.** Su salida es
$$a_1, b_1, \dots, a_{n-1}, b_{n-1}, \mathbf{b_n, a_n},$$
que está mal porque $a_n < b_n$. El argumento de C5 lo confirma: si intercambiamos los valores de $a_n$ y $b_n$ (las listas siguen ordenadas y ninguna comparación hecha cambia de respuesta), el algoritmo da la misma salida por posiciones, y ahora la correcta es otra. Las dos entradas reciben la misma salida y solo una la merece. Para $n = 2$: $I = [1, 3]$, $D = [2, 4]$ devuelve $[1, 2, 4, 3]$.

En general falla exactamente cuando el máximo de todo está en $D$: en la mitad de las intercalaciones (enumerando todas para $n \le 7$, falla en 1716 de 3432 con $n = 7$). Aquí las pruebas lo encontrarían enseguida; lo que muestra el ejercicio es que la cota mínima lo encontró sin correr nada y además dijo qué entrada construir.

---
