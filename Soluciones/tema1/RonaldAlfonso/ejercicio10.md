## 10.  Par más cercano en una dimensión (C2, C5)

**Cota mínima.** Modelo: árboles de decisión algebraicos (C2 §8). Admitimos puntos repetidos (C2 §2: si la entrada es una lista, la respuesta puede ser 0).

*Reducción desde distinción de elementos.* Dada $x_1, \dots, x_n$, la entrada de par más cercano en la recta es la misma lista $x_1, \dots, x_n$. La transformación no cuesta ninguna prueba de signo. La distancia mínima es 0 si y solo si hay dos $x_i$ iguales.

Supongamos un árbol algebraico de profundidad $T(n) = o(n\log n)$ para par más cercano en 1D. En cada hoja devuelve un par de índices $(p, q)$. Le agregamos a cada hoja un nodo que prueba el signo del polinomio de grado 1 $x_p - x_q$: "$= 0$" contesta "hay repetidos", y "$\ne 0$" contesta "todos distintos" (si el par más cercano no está a distancia 0, ningún par lo está). Resulta un árbol para distinción de elementos de profundidad $T(n) + 1 = o(n \log n)$, contra Ben-Or. Así que **par más cercano en 1D requiere $\Omega(n \log n)$ en árboles de decisión algebraicos**, y ordenar y mirar consecutivos (C2 §3) es óptimo en ese modelo.

**Qué algoritmo de C2 rompe la cota, y en qué modelo.** El incremental aleatorio con rejilla (C2 §9). No la rompe por el azar (Grigoriev et al., C2 §10), sino porque trabaja en una RAM real con **parte entera** y **direccionamiento indirecto** (tabla hash indexada por el número de celda), dos operaciones que un árbol de decisión algebraico no tiene. Costo esperado $O(n)$.

**Adaptación a una dimensión.** Las celdas son intervalos semiabiertos $[k\delta, (k+1)\delta)$, la celda de $q$ es $\lfloor q/\delta \rfloor$.

- *Invariante:* cada celda tiene a lo sumo un punto, porque dos puntos del mismo intervalo semiabierto de largo $\delta$ están a distancia $< \delta$, y $\delta$ es la distancia mínima entre los insertados.
- *Basta mirar 3 celdas:* si $|p - q| < \delta$, entonces $\lfloor p/\delta \rfloor \le p/\delta < q/\delta + 1 < \lfloor q/\delta\rfloor + 2$, así que las celdas difieren en a lo sumo 1. Se consultan las celdas $c-1$, $c$ y $c+1$.
- *Repetidos:* si $\delta$ llega a 0 se devuelve 0 de inmediato (no se puede dividir por 0, y no hay nada mejor).
- *Análisis hacia atrás*, igual que en C2: insertar $p_i$ obliga a reconstruir solo si $p_i$ pertenece a todos los pares más cercanos de $\{p_1, \dots, p_i\}$, lo que pasa con probabilidad $\le 2/i$ (con empates, todavía menos). Costo esperado $O(n) + \sum_i \frac{2}{i} O(i) = O(n)$.

```python
def par_mas_cercano_1d(X, semilla=0):
    pts = list(X)
    random.Random(semilla).shuffle(pts)
    d, par = abs(pts[0] - pts[1]), (pts[0], pts[1])
    if d == 0:
        return 0, par
    celda = lambda q: math.floor(q / d)          # lee el d actual
    rejilla = {celda(q): q for q in pts[:2]}
    for i in range(2, len(pts)):
        p, antes = pts[i], d
        c = celda(p)
        for dc in (-1, 0, 1):
            q = rejilla.get(c + dc)
            if q is not None and abs(p - q) < d:
                d, par = abs(p - q), (p, q)
        if d == 0:
            return 0, par
        if d < antes:                             # delta bajó: reconstruir
            rejilla = {celda(q): q for q in pts[:i + 1]}
        else:
            rejilla[c] = p
    return d, par
```

(Comprobado contra "ordenar y mirar consecutivos" en 3000 listas al azar, con y sin repetidos, sin fallos.)

---
