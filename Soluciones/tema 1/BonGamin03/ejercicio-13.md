# Ejercicio 13

## Enunciado del Problema

>Dado un *splay tree* con $n$ nodos cuya estructura inicial es un camino de longitud $n$ (donde la clave $n$ está en la raíz y cada clave $k$ es el hijo izquierdo de $k+1$), se realiza una secuencia de $n$ accesos a las claves en orden ascendente: $1, 2, \dots, n$.

Se pide acotar el costo total utilizando el **Lema de Acceso** y la cuenta de la sección 5 de la Conferencia 4, compararlo con las mediciones de la sección 6, y determinar si la cota obtenida es ajustada.

---

## Marco Teórico y Definiciones 

- **Costo Real ($c_i$):** El costo real de un acceso al nodo $x$ es proporcional al número de rotaciones realizadas en la operación `splay(x)`. Para mantener la rigurosidad, tomamos $c_i = \max(\text{rotaciones}, 1)$.
- **Tamaño del Subárbol ($s(x)$):** Número de nodos presentes en el subárbol acotado por el nodo $x$ (incluyéndose a sí mismo).
- **Rango de un Nodo ($r(x)$):** Definido como $r(x) = \log_2(s(x))$.
- **Potencial del Árbol ($\Phi$):** Suma de los rangos de todos los nodos del árbol:
   $$\Phi = \sum_{v \in T} r(v)$$
- **Costo Amortizado ($\hat{c}_i$):** Por el método del potencial:
   $$\hat{c}_i = c_i + \Phi_i - \Phi_{i-1}$$
   Sumando sobre una secuencia de $m$ operaciones:
   $$\sum_{i=1}^{m} c_i = \sum_{i=1}^{m} \hat{c}_i + \Phi_0 - \Phi_m$$
- **Lema de Acceso (Sleator y Tarjan):** El costo amortizado de hacer `splay` a un nodo $x$ en un árbol con raíz $R$ satisface:
   $$\hat{c}_i \le 3(r(R) - r(x)) + 1 = 3(\log_2 n - r(x)) + 1$$

---

## Acotación del Costo Total Teórico mediante el Lema de Acceso

Analizamos una secuencia de $m = n$ accesos a las claves $1, 2, \dots, n$.

### Paso A: Acotación de la suma de costos amortizados ($\sum \hat{c}_i$)
Por el Lema de Acceso, dado que para cualquier nodo $x$ el subárbol tiene al menos 1 nodo ($s(x) \ge 1$), su rango cumple $r(x) = \log_2 s(x) \ge 0$. Por ende:
$$\hat{c}_i \le 3\log_2 n + 1$$

Sumando sobre las $n$ operaciones de acceso:
$$\sum_{i=1}^{n} \hat{c}_i \le \sum_{i=1}^{n} (3\log_2 n + 1) = 3n \log_2 n + n$$

### Paso B: Acotación del cambio de potencial ($\Phi_0 - \Phi_n$)
* **Potencial Inicial ($\Phi_0$):** El árbol inicial es un camino degenerado de $n$ nodos. Los tamaños de subárbol son $s(k) = k$ para $k = 1, \dots, n$.
  $$\Phi_0 = \sum_{k=1}^{n} \log_2 k = \log_2(n!) \le n \log_2 n$$
* **Potencial Final ($\Phi_n$):** Como el rango de cada nodo es no negativo ($r(v) \ge 0$), el potencial final satisface:
  $$\Phi_n \ge 0$$

Por lo tanto, la diferencia de potencial cumple:
$$\Phi_0 - \Phi_n \le \Phi_0 \le n \log_2 n$$

### Paso C: Costo Total Real Teórico
Sustituyendo los resultados en la ecuación fundamental del potencial:
$$\sum_{i=1}^{n} c_i = \sum_{i=1}^{n} \hat{c}_i + \Phi_0 - \Phi_n \le (3n \log_2 n + n) + n \log_2 n = 4n \log_2 n + n$$

Dividiendo entre el número de accesos $n$, el costo amortizado por acceso derivado de la cota general del lema es:
$$\text{Costo Promedio Teórico} \le 4 \log_2 n + 1 = O(\log n)$$

---

## Comparación con las Mediciones de la Sección 6

En la **Sección 6** de la Conferencia 4, se mide el costo real por acceso al recorrer las claves en orden $1, 2, \dots, n$ sobre un árbol inicial camino:

| $n$ | `splay` (rotaciones/acceso) | $\log_2 n$ |
| :---: | :---: | :---: |
| 100 | 4.2 | 6.6 |
| 200 | 4.2 | 7.6 |
| 400 | 4.3 | 8.6 |
| 800 | 4.4 | 9.6 |

### Principales observaciones:
1. En la práctica, el costo por acceso para `splay` permanece **prácticamente constante** ($\approx 4.2 - 4.4$ rotaciones por acceso) sin importar el tamaño de $n$.
2. **Costo Total Real Practico:** Para procesar los $n$ accesos en orden, `splay` realiza un total de $O(n)$ rotaciones en total, lo que representa un costo amortizado de $O(1)$ por operación.

---

## ¿Es ajustada la cota?

**No, la cota $O(\log n)$ por acceso derivada directamente del Lema de Acceso general NO es ajustada para esta secuencia específica.**

### Análisis de la discrepancia:
1. **Generalidad del Lema de Acceso:** El Lema de Acceso provee una cota superior válida para **cualquier** secuencia arbitraria de accesos en el peor caso ($O(\log n)$ amortizado por operación).
2. **Efecto de Reestructuración por Zig-Zig:** La secuencia ordenada $1, 2, \dots, n$ explota la propiedad fundamental del paso **zig-zig**. Cada paso zig-zig en `splay` divide aproximadamente a la mitad la profundidad de todos los nodos en el camino de acceso.
3. Al acceder sucesivamente a los nodos de forma ordenada, el camino largo inicial se desmantela de forma agresiva en los primeros accesos. Los accesos posteriores encuentran los nodos restantes a profundidades muy reducidas. 
4. Sleator y Tarjan demostraron formalmente esto como el *Teorema de Acceso Secuencial* (*Sequential Access Theorem*), el cual establece que acceder a los elementos en orden en un *splay tree* toma $O(n)$ en total ($O(1)$ amortizado por operación), independientemente de la forma inicial del árbol.

---

## Conclusión

* **Cota obtenida del Lema de Acceso:** $\sum_{i=1}^n c_i \le 4n \log_2 n + n \implies O(\log n)$ por acceso.
* **Costo Real Medido (Sección 6):** $O(n)$ en total $\implies O(1)$ por acceso ($\approx 4.3$ rotaciones).
* **Evaluación de la Cota:** La cota del Lema de Acceso es una cota superior válida pero **no ajustada** para la secuencia en orden $1, \dots, n$, ya que sobreestima el costo real debido a la compresión continua que provocan las rotaciones zig-zig.
