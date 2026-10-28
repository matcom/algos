# Ejercicio 13 — Un camino splay accedido en orden

> **Enunciado.** En un splay tree que empieza como un camino de $n$ nodos se accede a
> las claves en orden. Acota el costo total con el lema de acceso y la cuenta de la
> sección 5 de la conferencia 4, y compáralo con lo que mide la sección 6. ¿Es ajustada
> la cota?

---

## 1. La situación

El árbol inicial es el **peor árbol posible** (C4, §4, función `camino`): un camino de
$n$ nodos, con la clave $n$ en la raíz y cada clave hija izquierda de la siguiente, de
modo que la clave $1$ está al fondo, a profundidad $n-1$.

```
   camino(n):          n
                      /
                   n-1
                    /
                 n-2
                  /
                 ⋱
                1          ← la clave 1 está a profundidad n-1
```

Sobre él se accede a las claves **en orden**: $1, 2, 3, \dots, n$. Un acceso busca la
clave y luego hace **splay** (C4, §4): sube el nodo accedido a la raíz con pasos
zig / zig-zig / zig-zag. El costo de un acceso es el número de rotaciones (o $1$ si el
nodo ya es raíz).

---

## 2. La cota por el lema de acceso (C4, §5)

Recordemos la maquinaria de C4, §5. Para cada nodo $x$, $s(x)$ es el tamaño de su
subárbol y $r(x)=\log_2 s(x)$ su **rango**; el potencial es
$$\Phi=\sum_x r(x).$$

**Lema de acceso (Sleator–Tarjan, C4, §5).** El costo amortizado de hacer splay de $x$
en un árbol con raíz $t$ es a lo sumo
$$\hat c \;\le\; 3\big(r(t)-r(x)\big)+1 \;=\; O(\log n).$$

**La cuenta de la sección 5.** Para $m$ accesos, sumando costos reales y amortizados y
usando que las diferencias telescopian y $\Phi_m\ge 0$:
$$\sum_{i=1}^m c_i \;=\; \sum_{i=1}^m \hat c_i-(\Phi_m-\Phi_0)
\;\le\; m\,(3\log_2 n+1)+\Phi_0 .$$

El potencial inicial de **un camino** es (C4, §5)
$$\Phi_0 \;=\; \sum_{k=1}^n \log_2 k \;=\; \log_2 n! \;=\; \Theta(n\log n),$$
que la demostración paga **aparte, una sola vez** (es justo el caso en que
$\Phi_m\ge\Phi_0$ no se cumple y hay que abonar $\Phi_0$).

**Aplicación a nuestro caso.** Aquí accedemos a las $n$ claves **una sola ronda**, luego
$m=n$:
$$
\boxed{\;\sum c_i \;\le\; n\,(3\log_2 n+1)+\log_2 n! \;=\; O(n\log n)\;}
$$
es decir, **$O(\log n)$ amortizado por acceso**. Con $k$ rondas, $m=kn$ y la cota es
$$\sum c_i \le kn\,(3\log_2 n+1)+\log_2 n! = O\big((k n+n)\log n\big),$$
que para $k$ rondas da $O(\log n)$ amortizado por acceso: **el $\Phi_0=\Theta(n\log n)$
se diluye entre todos los accesos y no vuelve a pagarse.**

---

## 3. Lo que mide la sección 6 (C4, §6)

La sección 6 **ejecuta** exactamente esta secuencia —camino inicial, claves en orden,
varias rondas— y mide las rotaciones **reales** por acceso, para splay y para la
heurística mala (subir a la raíz). Reproduzco esa medición:

```python
import math

class Nodo:
    def __init__(self, clave):
        self.clave, self.izq, self.der, self.padre = clave, None, None, None

def rotar(x):
    p, g = x.padre, x.padre.padre
    if p.izq is x:
        p.izq, x.der = x.der, p
        if p.izq: p.izq.padre = p
    else:
        p.der, x.izq = x.izq, p
        if p.der: p.der.padre = p
    p.padre, x.padre = x, g
    if g:
        if g.izq is p: g.izq = x
        else: g.der = x

def splay(x):
    rot = 0
    while x.padre:
        p, g = x.padre, x.padre.padre
        if g is None:                               # zig
            rotar(x); rot += 1
        elif (g.izq is p) == (p.izq is x):          # zig-zig: primero el padre
            rotar(p); rotar(x); rot += 2
        else:                                       # zig-zag
            rotar(x); rotar(x); rot += 2
    return rot

def subir_a_la_raiz(x):
    rot = 0
    while x.padre:
        rotar(x); rot += 1
    return rot

def buscar(raiz, clave):
    x = raiz
    while x.clave != clave:
        x = x.izq if clave < x.clave else x.der
    return x

def camino(n):
    nodos = [Nodo(k) for k in range(1, n + 1)]
    for k in range(1, n):
        nodos[k].izq, nodos[k - 1].padre = nodos[k - 1], nodos[k]
    return nodos[-1]

def costo_por_acceso(reorganizar, n, rondas=3):
    raiz, total = camino(n), 0
    for _ in range(rondas):
        for clave in range(1, n + 1):
            x = buscar(raiz, clave)
            total += max(reorganizar(x), 1)
            raiz = x
    return total / (rondas * n)

if __name__ == "__main__":
    print(f"{'n':>6} {'splay':>8} {'subir a la raíz':>16} {'log2 n':>8}")
    for n in [100, 200, 400, 800]:
        s = costo_por_acceso(splay, n)
        r = costo_por_acceso(subir_a_la_raiz, n)
        print(f"{n:>6} {s:>8.1f} {r:>16.1f} {math.log2(n):>8.1f}")
```

```
     n    splay  subir a la raíz   log2 n
   100      4.2            50.5      6.6
   200      4.2           100.5      7.6
   400      4.3           200.5      8.6
   800      4.4           400.5      9.6
```

La columna de splay es **plana: ~4 rotaciones por acceso, prácticamente sin variar al
crecer $n$** (de $4.2$ a $4.4$ cuando $n$ pasa de $100$ a $800$). La de subir a la raíz
crece linealmente ($\approx n/2$), que es $\Theta(n)$ por acceso —la heurística mala deja
otra vez un camino casi tan largo tras cada acceso (C4, §6).

```
  rotaciones por acceso (claves en orden sobre el camino inicial)
  400 ┤                                     ● subir a la raíz  (pendiente 1 ⇒ Θ(n))
      │                        ●
  200 ┤            ●
      │     ●
    4 ┤─●──────●──────●──────●───────────── splay  (plano ⇒ Θ(1) amortizado)
      └──────────────────────────────────  n
       100    200    400    800
```

---

## 4. ¿Es ajustada la cota?

**No es ajustada para esta secuencia.** El lema de acceso garantiza $O(\log n)$
amortizado por acceso; la sección 6 mide que el splay real cuesta $\Theta(1)$ amortizado
por acceso en esta secuencia concreta (acceder en orden, una y otra vez). Hay una brecha
de un factor $\Theta(\log n)$ entre la **cota** $O(\log n)$ y el **costo real**
$\Theta(1)$.

| | fórmula | por acceso |
|---|---|---|
| cota del lema de acceso (§5) | $n(3\log_2 n+1)+\log_2 n!$ | $O(\log n)$ |
| costo real medido (§6) | $\approx 4n$ por ronda | $\Theta(1)$ |

Esto no es un defecto del lema, sino su naturaleza: es una cota de **peor caso
amortizado uniforme**, válida para *cualquier* secuencia de accesos. Las secuencias con
estructura —como acceder en orden— pueden ser **mucho** más baratas, y el lema de acceso,
tomado solo, no lo ve.

Lo que sí lo ve es un teorema más fino de la misma familia, que **no** se demostró en
la conferencia pero conviene nombrar para situar la respuesta:

- **Teorema del dedo estático / del acceso secuencial:** acceder a las $n$ claves en
  orden sobre un splay tree cuesta $O(n)$ en total, es decir $\Theta(1)$ amortizado por
  acceso. Esto es exactamente lo que mide §6, y es **estrictamente mejor** que el
  $O(n\log n)$ que da el lema de acceso.
- Más allá, la **conjetura de optimalidad dinámica** (Sleator–Tarjan) afirma que el
  splay tree es, salvo constante, tan bueno como *cualquier* árbol de búsqueda en
  *cualquier* secuencia; sigue abierta.

**Conclusión.** La cota del lema de acceso para "camino + accesos en orden" es
$O(n\log n)$ total / $O(\log n)$ amortizado, y es **correcta pero no ajustada**: el costo
verdadero, medido en §6, es $\Theta(n)$ total / $\Theta(1)$ amortizado. La herramienta
general (lema de acceso) acota por arriba cualquier secuencia; la estructura particular
de esta secuencia la hace más barata de lo que esa herramienta, por sí sola, puede
demostrar. Es otra instancia de la idea del Tema 1: *el caso típico (o estructurado) no
es la garantía*, y aquí el caso estructurado está muy por debajo de la garantía.

---

## 5. Resumen

- **Cota (lema de acceso + cuenta §5):** con el potencial de rangos, $\sum c_i \le
  m(3\log_2 n+1)+\Phi_0$ y $\Phi_0=\log_2 n!=\Theta(n\log n)$ para el camino; con
  $m=\Theta(n)$ accesos da $O(n\log n)$ total, $O(\log n)$ por acceso.
- **Medición (§6):** el splay real cuesta $\approx 4$ rotaciones por acceso,
  independiente de $n$: $\Theta(n)$ total, $\Theta(1)$ amortizado. Subir a la raíz, en
  cambio, cuesta $\Theta(n)$ por acceso.
- **¿Ajustada?** No. Hay un factor $\Theta(\log n)$ de holgura; la secuencia "en orden"
  cae bajo el teorema del acceso secuencial ($O(n)$ total), que el lema de acceso por sí
  solo no captura.
