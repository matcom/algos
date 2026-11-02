
# Problema 13 ★★ 

**Enunciado.** En un splay tree que empieza como un camino de $n$ nodos se accede a las claves $1, \ldots, n$ en orden. Acota el costo total con el lema de acceso y la cuenta de la sección 5 de la conferencia 4, y compáralo con lo que mide la sección 6. ¿Es ajustada la cota? 

## Solución formal

**El escenario.** El árbol inicial es un camino de $n$ nodos: la raíz es $n$, su hijo izquierdo es $n-1$, el hijo izquierdo de este es $n-2$, y así hasta $1$ en la hoja más profunda. Accedemos a las claves $1, 2, \ldots, n$ en ese orden, haciendo splay de cada una después de buscarla.

**Potencial inicial.** El potencial es $\Phi = \sum_x r(x)$, con $r(x) = \log_2 s(x)$ y $s(x)$ el tamaño del subárbol de $x$. En el camino inicial, los tamaños de subárbol son $1, 2, \ldots, n$, así que:
$$
\Phi_0 = \sum_{k=1}^n \log_2 k = \log_2(n!) = \Theta(n \log n).
$$

**Cota con el lema de acceso.** El lema de acceso dice que el costo amortizado de hacer splay de un nodo $x$ con raíz $t$ es a lo sumo:
$$
\hat{c} \le 3(r(t) - r(x)) + 1.
$$
Como $r(t) = \log_2 n$ y $r(x) \ge 0$, cada acceso tiene costo amortizado $O(\log n)$. Para $m = n$ accesos, la cuenta de la sección 5 da:
$$
\sum_{i=1}^n c_i \le \sum_{i=1}^n \hat{c}_i + \Phi_0 - \Phi_n \le n(3\log_2 n + 1) + \Phi_0 = O(n \log n).
$$
Aquí usamos que $\Phi_n \ge 0$ y $\Phi_0 = O(n \log n)$.

**Lo que mide la sección 6.** La sección 6 corre exactamente esta secuencia (un camino, accesos $1, \ldots, n$ en orden, tres rondas) y mide el costo por acceso para splay:

| $n$ | splay | subir a la raíz | $\log_2 n$ |
|-----|-------|-----------------|------------|
| 100 | 4.2   | 50.5            | 6.6        |
| 200 | 4.2   | 100.5           | 7.6        |
| 400 | 4.3   | 200.5           | 8.6        |
| 800 | 4.4   | 400.5           | 9.6        |

El costo por acceso con splay es aproximadamente constante (~4.3), no $O(\log n)$. Para $n$ accesos, el costo total medido es $\approx 4.3n = O(n)$.

**¿Es ajustada la cota?** La cota del lema de acceso da $O(n \log n)$, pero el costo real medido es $O(n)$. La cota **no es ajustada**: es holgada por un factor de $\log n$.

**¿Por qué es holgada?** El lema de acceso da una cota por acceso de $3(r(t) - r(x)) + 1$. Al aplicarla uniformemente se usa $r(t) \le \log n$ y $r(x) \ge 0$, lo que da $O(\log n)$ por acceso. Pero en esta secuencia, para $i \ge 2$, el nodo accedido $x_i$ está cerca de la raíz después del splay anterior. El acceso a $1$ cuesta $n-1$ rotaciones y deja el árbol casi balanceado hacia la derecha; los accesos a $2, 3, \ldots, n$ cuestan $O(1)$ rotaciones cada uno. La suma telescópica real es mucho menor que la cota, pero el lema general no lo aprovecha porque acota cada paso usando el peor caso $r(t) - r(x) \approx \log n$.
