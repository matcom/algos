# Ejercicio 13 — Un camino splay accedido en orden

**Uso de IA:** Se usó IA para preparar y revisar este borrador, generar código y casos
de prueba, y apoyar la depuración. Parte de la explicación matemática también recibió
asistencia de IA; esas partes todavía no son redacción propia. Antes de entregar,
reescribiré y verificaré por mi cuenta las demostraciones, análisis de costo y cotas,
según la regla del curso.


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

La sección 6 mide las rotaciones reales de cada acceso. La primera búsqueda de cada
ronda parte de la clave 1, que está a profundidad $n-1$ en el camino que deja el acceso
anterior a la clave $n$. Separamos ese costo del resto de la ronda:

~~~python
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
        if g is None:
            rotar(x); rot += 1
        elif (g.izq is p) == (p.izq is x):
            rotar(p); rotar(x); rot += 2
        else:
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
def costos_por_ronda(reorganizar, n, rondas=3):
    raiz = camino(n)
    resultado = []
    for _ in range(rondas):
        costos = []
        for clave in range(1, n + 1):
            x = buscar(raiz, clave)
            costos.append(max(reorganizar(x), 1))
            raiz = x
        resultado.append(costos)
    return resultado

def costo_por_acceso(reorganizar, n, rondas=3):
    todos = costos_por_ronda(reorganizar, n, rondas)
    return sum(map(sum, todos)) / (rondas * n)

print(f"{'n':>6} {'primero':>9} {'resto/ronda':>13} "
      f"{'subir a raíz':>13}")
for n in [100, 200, 400, 800]:
    rondas = costos_por_ronda(splay, n)
    assert all(r[0] == n - 1 for r in rondas)
    primero = rondas[0][0]
    resto = sum(sum(r[1:]) for r in rondas) / (len(rondas) * (n - 1))
    malo = costo_por_acceso(subir_a_la_raiz, n)
    print(f"{n:>6} {primero:>9.1f} {resto:>13.2f} {malo:>13.1f}")
~~~

~~~
     n   primero   resto/ronda  subir a raíz
   100      99.0          3.20          50.5
   200     199.0          3.22         100.5
   400     399.0          3.34         200.5
   800     799.0          3.37         400.5
~~~

El primer acceso cuesta exactamente $n-1$ rotaciones. Los accesos restantes promedian
entre $3.2$ y $3.4$ rotaciones en estas mediciones. La heurística de subir cada nodo a
la raíz promedia aproximadamente $n/2$ rotaciones por acceso.
## 4. ¿Es ajustada la cota?

**No es ajustada para esta secuencia.** El lema de acceso garantiza $O(\log n)$
amortizado por acceso; la sección 6 mide que el splay real cuesta $\Theta(1)$ amortizado
por acceso en esta secuencia concreta (acceder en orden, una y otra vez). Hay una brecha
de un factor $\Theta(\log n)$ entre la **cota** $O(\log n)$ y el **costo real**
$\Theta(1)$.

| | fórmula | por acceso |
|---|---|---|
| cota del lema de acceso (§5) | $n(3\log_2 n+1)+\log_2 n!$ | $O(\log n)$ |
| costo real medido (§6) | $n-1$ en el primer acceso; luego $\approx3.3$ por acceso | $\Theta(1)$ en los restantes |

Esto no es un defecto del lema, sino su naturaleza: es una cota de **peor caso
amortizado uniforme**, válida para *cualquier* secuencia de accesos. Las secuencias con
estructura —como acceder en orden— pueden ser **mucho** más baratas, y el lema de acceso,
tomado solo, no lo ve.

Lo que sí lo ve es un teorema más fino de la misma familia, que **no** se demostró en
la conferencia pero conviene nombrar para situar la respuesta:

- **Teorema del acceso secuencial de Tarjan:** acceder a las $n$ claves en
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
- **Medición (§6):** cada ronda empieza con $n-1$ rotaciones y los accesos restantes
  promedian $\approx3.3$: $\Theta(n)$ por ronda. Subir a la raíz, en
  cambio, cuesta $\Theta(n)$ por acceso.
- **¿Ajustada?** No. Hay un factor $\Theta(\log n)$ de holgura; la secuencia "en orden"
  cae bajo el teorema del acceso secuencial de Tarjan ($O(n)$ total), que el lema de acceso por sí
  solo no captura.
