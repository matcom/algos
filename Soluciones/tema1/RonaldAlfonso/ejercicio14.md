## 14. Un problema nuevo, con el ciclo completo (C2 a C5)

**Problema elegido: el mínimo de un arreglo ordenado rotado.**

### 1. El problema

Entrada: $A[0..n-1]$, con $n \ge 1$ elementos **distintos**, que es una rotación de un arreglo creciente: existe $k \in \{0, \dots, n-1\}$ tal que $A[k], A[k+1], \dots, A[n-1], A[0], \dots, A[k-1]$ es creciente. Salida: $k$, la posición del mínimo. Modelo: comparaciones entre elementos (C5 §1).

Precisiones (C2 §2):

- $k = 0$ (sin rotar) y $n = 1$ son entradas válidas.
- **Los distintos importan.** Con repetidos el problema cambia de costo: $[1, \dots, 1, 0, 1, \dots, 1]$ es una rotación de $[0, 1, \dots, 1]$ para cualquier posición del 0, y un adversario que contesta "iguales" a todo obliga a tocar al menos $n - 1$ posiciones, porque un 0 en una posición no tocada cambiaría la respuesta. Con repetidos el costo es $\Omega(n)$.
- Con distintos, comparar dos posiciones distintas nunca da "$=$": el árbol de decisión es binario, y la trampa de los tres caminos de C5 §3 no aparece.

### 2. El algoritmo

Observación: los elementos de $A[0..k-1]$ son los más grandes del arreglo, y $A[n-1]$ es el mayor de $A[k..n-1]$. Así que comparar con $A[n-1]$ dice de qué lado del corte está una posición.

```python
def minimo_rotado(A):
    lo, hi = 0, len(A) - 1             # invariante: k está en [lo, hi]
    while lo < hi:
        m = (lo + hi) // 2             # m < hi <= n-1: nunca compara A[n-1] consigo mismo
        if A[m] > A[-1]: lo = m + 1    # m está antes del corte
        else:            hi = m        # m está en el tramo del mínimo
    return lo
```

### 3. Correctitud

*Lema.* Para todo $i$: $A[i] > A[n-1] \iff i < k$.

Demostración. Si $i \ge k$, $A[i]$ está en el tramo creciente $A[k..n-1]$, que termina en $A[n-1]$, así que $A[i] \le A[n-1]$. Si $i < k$ (lo que exige $k > 0$), $A[i]$ está en $A[0..k-1]$, que en el orden creciente va después de $A[n-1]$, así que $A[i] > A[n-1]$. $\square$

Por el lema, el predicado $P(i) = [A[i] \le A[n-1]]$ es "falso…falso verdadero…verdadero" y $k$ es el primer $i$ con $P(i)$.

*Invariante:* $k \in [lo, hi]$. Inicialización: $[0, n-1]$ contiene a $k$. Mantenimiento: si $A[m] > A[n-1]$, por el lema $m < k$ y $k \in [m+1, hi]$; si no, $m \ge k$ y $k \in [lo, m]$. Conclusión: al salir $lo = hi$, así que $lo = k$.

*Potencial:* $hi - lo$. Con $s = hi - lo + 1$ posiciones, las dos mitades tienen $\lceil s/2 \rceil$ y $\lfloor s/2 \rfloor$, así que baja estrictamente y el ciclo termina.

### 4. Costo

Una comparación por vuelta, y el tamaño pasa de $s$ a a lo sumo $\lceil s/2 \rceil$: **a lo sumo $\lceil \log n \rceil$ comparaciones**, tiempo $O(\log n)$, memoria $O(1)$. (Comprobado sobre todas las rotaciones de $[1..n]$ para $n < 40$: siempre correcto, y el peor caso es exactamente $\lceil \log n\rceil$.)

### 5. Cota mínima

Hay $n$ salidas posibles, y todas ocurren: rotar $[1, \dots, n]$ para que el 1 quede en la posición $k$ da una entrada cuya única respuesta correcta es $k$. Como la salida depende solo de la hoja (C5 §3, lema 2), esas $n$ entradas van a $n$ hojas distintas. Con elementos distintos el árbol es binario, y por el lema 1 de C5:
$$\text{peor caso} \ \ge\ \lceil \log n \rceil.$$
**El algoritmo y la cota coinciden exactamente**, sin diferencia de constantes. Aquí el argumento de información alcanza (no hace falta adversario) porque la salida es grande: $n$ respuestas posibles, a diferencia del máximo o la mezcla de C5 §4.

### 6. Qué deja fuera el modelo (C2 §10, C5 §9)

La cota vale para algoritmos de comparaciones. Si además se sabe que los valores son exactamente $1, \dots, n$, el algoritmo puede usar el valor como número: la rotación que deja el 1 en la posición $k$ tiene $A[0] = n - k + 1$ (o $A[0] = 1$ si $k = 0$), así que
$$k = (n + 1 - A[0]) \bmod n,$$
en $O(1)$. No contradice nada: usa aritmética sobre los valores, que el modelo de comparaciones no tiene, igual que el ordenamiento por conteo de C5 §9 o la rejilla de C2 §9.
