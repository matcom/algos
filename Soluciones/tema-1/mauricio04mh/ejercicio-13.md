# Ejercicio 13. Un splay tree que empieza como un camino

Dificultad: ★★ · Código: [`ejercicio-13.py`](ejercicio-13.py)

---

## Enunciado

> En un splay tree que empieza como un camino de $n$ nodos se accede a las claves $1, 2, \dots, n$ en orden. Acota el costo total con el lema de acceso y la cuenta de la sección 5 de la conferencia 4, y compáralo con lo que mide la sección 6. ¿Es ajustada la cota?

## Qué se pide

1. Acotar el costo total de los $n$ accesos con el lema de acceso (Conferencia 4, §5).
2. Compararlo con lo que mide la Conferencia 4, §6 (el contraste con «subir a la raíz»).
3. Decidir si la cota es ajustada.

**Mapa.** Se parte de un caso pequeño ($n = 4$) para ver qué ocurre de verdad. Luego se aplica la cuenta de la Conferencia 4, §5, que da una cota $O(n \log n)$ para el costo total. Después se compara con «subir a la raíz», que en este mismo ejemplo cuesta $\Theta(n^2)$, para ver qué aporta el splay. Por último se pregunta si la cota $O(n\log n)$ es ajustada, y la respuesta es que no.

## Preliminares

**Estructura.** Árbol binario de búsqueda con claves $1, \dots, n$. Acceder a una clave es hacer *splay* de su nodo: se sube a la raíz con rotaciones (zig, zig-zig, zig-zag).

**Costo** (Conferencia 4, §4). El costo de un acceso es el número de rotaciones, igual a la profundidad del nodo (cada zig-zig y zig-zag cuenta $2$, cada zig $1$), y $1$ si el nodo ya es la raíz. El código cuenta solo rotaciones, así que en ese caso suma $0$; la diferencia solo importa en el último párrafo de «¿Es ajustada la cota?».

**Camino inicial** (la función `camino(n)` de la Conferencia 4, §4): la raíz es $n$ y cada nodo tiene como único hijo, a la izquierda, al anterior:

$$n \to n-1 \to \dots \to 2 \to 1.$$

La clave $1$ está en el fondo, a profundidad $n-1$; es la orientación más cara para el primer acceso. (La otra orientación se trata en «¿Es ajustada la cota?».)

**Rango y potencial.** Para un nodo $x$, $s(x)$ es el número de nodos de su subárbol (contándolo) y $r(x) = \log_2 s(x)$. El potencial es

$$\Phi = \sum_x r(x).$$

**Lema de acceso** (Sleator y Tarjan; Conferencia 4, §5). El costo amortizado de hacer splay de $x$ en un árbol de raíz $t$ cumple

$$\hat{c} \le 3\bigl(r(t) - r(x)\bigr) + 1,$$

donde $\hat{c} = c + \Phi_{\text{después}} - \Phi_{\text{antes}}$.

**Notación.** $a(b,c)$ es «raíz $a$ con hijo izquierdo $b$ e hijo derecho $c$»; «$.$» es el árbol vacío.

---

## Qué pasa con $n = 4$

Antes de acotar nada conviene ver qué hace el splay en un caso pequeño. Este ejemplo se usa después como comprobación de cada resultado.

El camino es $4(3(2(1,.),.),.)$. Tras cada acceso se anota el costo real (rotaciones) y el potencial.

| acceso | profundidad | rotaciones | árbol después | $\Phi$ |
|---|---|---|---|---|
| (inicio) | | | $4(3(2(1,.),.),.)$ | $4{,}58$ |
| 1 | 3 | 3 | $1(.,4(2(.,3),.))$ | $4{,}58$ |
| 2 | 2 | 2 | $2(1,4(3,.))$ | $3{,}00$ |
| 3 | 2 | 2 | $3(2(1,.),4)$ | $3{,}00$ |
| 4 | 1 | 1 | $4(3(2(1,.),.),.)$ | $4{,}58$ |

Costo total real: $3 + 2 + 2 + 1 = 8$ rotaciones. Después del último acceso el árbol vuelve a ser el camino inicial.

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="figuras/ejercicio-13-arboles-oscuro.svg">
  <img src="figuras/ejercicio-13-arboles-claro.svg" alt="El árbol antes y después de cada acceso con n = 4">
</picture>

**Figura 1.** El árbol antes del primer acceso y después de cada uno, con $n = 4$. Las claves están en orden de izquierda a derecha, y el nodo recién accedido (resaltado) queda en la raíz. Las rotaciones son $3, 2, 2, 1$, y el último árbol es el camino inicial.

---

## El potencial inicial

La cuenta con el lema de acceso necesita el potencial de partida, porque el potencial inicial es lo que hay que «pagar» además de los costos amortizados de los accesos. En el ejemplo, el camino tiene $\Phi = 4{,}58$, y la tabla de arriba muestra cómo ese potencial baja y vuelve a subir.

**Lema 1.** El camino de $n$ nodos tiene potencial $\Phi_0 = \log_2 n! \le n\log_2 n$.

**Demostración.**

**Paso 1.** En el camino los subárboles tienen tamaños $n, n-1, \dots, 1$.

**Paso 2.** Entonces $\Phi_0 = \sum_{i=1}^{n}\log_2 i = \log_2 n!$.

**Paso 3.** Como $i \le n$ en cada factor, $\log_2 n! \le n\log_2 n$. $\blacksquare$

**Comprobación ($n = 4$):** $\log_2 24 \approx 4{,}58 \le 8$. El camino tiene potencial alto: es la «deuda» que el primer acceso caro va a pagar (Conferencia 4, §5).

---

## La cota con el lema de acceso

Con el potencial inicial calculado, se suma el costo amortizado de los $n$ accesos. Como el potencial se telescopia, el costo real total queda acotado por la suma de los amortizados más el potencial de partida.

**Teorema 1.** El costo total real de los $n$ accesos es a lo sumo $4n\log_2 n + n = O(n\log n)$.

**Demostración.**

**Paso 1. Costo amortizado de un acceso.** Con $c_k$ el costo real del acceso $k$ y $\Phi_k$ el potencial tras él: $\hat{c}_k = c_k + \Phi_k - \Phi_{k-1}$.

**Paso 2. Cota por acceso.** La raíz siempre tiene $n$ nodos, así que $r(t) = \log_2 n$, y $r(x) \ge 0$. Por el lema de acceso:

$$\hat{c}_k \le 3\log_2 n + 1.$$

**Paso 3. Sumar.** Los potenciales se telescopian:

$$\sum_{k=1}^{n} c_k = \sum_{k=1}^{n}\hat{c}_k + \Phi_0 - \Phi_n.$$

**Paso 4. Acotar cada término.**

$$\sum_{k=1}^{n}\hat{c}_k \le n(3\log_2 n + 1), \qquad \Phi_0 \le n\log_2 n, \qquad \Phi_n \ge 0.$$

**Paso 5. Conclusión.**

$$\sum_{k=1}^{n} c_k \le 3n\log_2 n + n + n\log_2 n = 4n\log_2 n + n. \qquad\blacksquare$$

Es la «Consecuencia» de la Conferencia 4, §5: para $m$ accesos, $O(m\log n + n\log n)$, aquí con $m = n$.

**Comprobación ($n = 4$).** La cota da $4\cdot 4\cdot 2 + 4 = 36 \ge 8$. Los costos amortizados reales:

| acceso | $c_k$ | $\Phi_k - \Phi_{k-1}$ | $\hat{c}_k$ | cota del lema $3(2 - \log_2 s) + 1$ |
|---|---|---|---|---|
| 1 | 3 | $0$ | $3$ | $7$ |
| 2 | 2 | $-1{,}58$ | $0{,}42$ | $4$ |
| 3 | 2 | $0$ | $2$ | $7$ |
| 4 | 1 | $+1{,}58$ | $2{,}58$ | $7$ |

Aquí $s$ es el tamaño del subárbol del nodo accedido justo antes del splay: $1, 2, 1, 1$. La suma de los $\hat{c}_k$ es $8$, igual al costo real, porque $\Phi_4 = \Phi_0$.

---

## Comparación con la Conferencia 4, §6 («subir a la raíz»)

Hasta aquí se sabe que el splay cuesta $O(n\log n)$ en este ejemplo. Para ver por qué el splay es especial, se calcula lo que cuesta la heurística más simple, subir a la raíz con rotaciones simples, sobre el mismo camino.

La Conferencia 4, §6 compara el splay con subir a la raíz con rotaciones simples. Las dos heurísticas difieren solo en el caso zig-zig: el splay rota primero al padre. La Conferencia mide que en el camino con accesos en orden el splay cuesta una constante por acceso y subir a la raíz $\Theta(n)$ (ejercicio 4 de esa conferencia).

**Con $n = 4$** (rotaciones simples):

| acceso | profundidad | rotaciones | árbol después |
|---|---|---|---|
| 1 | 3 | 3 | $1(.,4(3(2,.),.))$ |
| 2 | 3 | 3 | $2(1,4(3,.))$ |
| 3 | 2 | 2 | $3(2(1,.),4)$ |
| 4 | 1 | 1 | $4(3(2(1,.),.),.)$ |

Total: $3 + 3 + 2 + 1 = 9$ (el splay hizo $8$).

**Lema 2 (invariante de «subir a la raíz»).** Para $n \ge 3$ y $3 \le k \le n$, antes del acceso $k$ el árbol es:

- raíz $k-1$;
- hijo izquierdo: el camino $k-2 \to k-3 \to \dots \to 1$;
- hijo derecho: el nodo $n$, con el camino $n \to n-1 \to \dots \to k$ colgando a su izquierda.

**Demostración.**

**Base ($k = 3$).** El acceso $1$ lleva la clave $1$ a la raíz por rotaciones simples: queda $1$ con hijo derecho $n$ y el camino $n \to \dots \to 2$ a su izquierda. El acceso $2$, a profundidad $n-1$, la lleva a la raíz y deja $2(1,\ n(n{-}1(\dots 3)))$, que es el enunciado con $k = 3$.

**Paso inductivo.** Si vale para $k < n$, el nodo $k$ es el último del camino $n \to \dots \to k$, a profundidad $1 + (n-k) = n-k+1$: un paso de la raíz $k-1$ a $n$ y $n-k$ pasos hacia abajo por el camino. Las rotaciones simples lo suben así:

- Mientras su padre $p$ es un nodo del camino ($k < p \le n$), $k$ es hijo izquierdo de $p$. La rotación pone a $p$ como hijo derecho de $k$, y el que era hijo derecho de $k$ pasa a ser hijo izquierdo de $p$. Cuando $k$ ocupa el lugar de $n$, su hijo derecho es $n$, y debajo de $n$ cuelga a la izquierda el camino $n \to \dots \to k+1$.
- La última rotación es con la raíz $k-1$, de la que $k$ es ahora hijo derecho: $k-1$ pasa a ser hijo izquierdo de $k$, con su camino $k-2 \to \dots \to 1$ debajo.

Quedan la raíz $k$, el camino $k-1 \to \dots \to 1$ a su izquierda y, a su derecha, el nodo $n$ con el camino $n \to \dots \to k+1$ colgando a la izquierda de $n$. Es el enunciado con $k+1$. $\blacksquare$

**Teorema 2.** Con rotaciones simples, el costo total es exactamente

$$\frac{(n-1)(n+2)}{2} = \Theta(n^2).$$

**Demostración.**

**Paso 1.** Los accesos $1$ y $2$ cuestan $n-1$ cada uno.

**Paso 2.** Por el Lema 2, el acceso $k$ ($3 \le k \le n$) cuesta $n-k+1$.

**Paso 3.** Total:

$$2(n-1) + \sum_{k=3}^{n}(n-k+1) = 2(n-1) + \frac{(n-2)(n-1)}{2} = \frac{(n-1)(n+2)}{2}. \qquad\blacksquare$$

**Comparación** (código; rotaciones totales al acceder a $1, \dots, n$ en orden):

| $n$ | splay | splay$/n$ | subir a la raíz | $(n-1)(n+2)/2$ | cota $4n\log_2 n + n$ |
|---|---|---|---|---|---|
| 4 | 8 | 2,00 | 9 | 9 | 36 |
| 8 | 22 | 2,75 | 35 | 35 | 104 |
| 16 | 54 | 3,38 | 135 | 135 | 272 |
| 64 | 256 | 4,00 | 2079 | 2079 | 1600 |
| 256 | 1096 | 4,28 | 32 895 | 32 895 | 8448 |
| 1024 | 4478 | 4,37 | 524 799 | 524 799 | 41 984 |

La columna de «subir a la raíz» coincide con la fórmula exacta del Teorema 2 en todas las filas. Para $n = 8$ la secuencia de costos es $7, 7, 6, 5, 4, 3, 2, 1$ (total $35$).

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="figuras/ejercicio-13-costos-oscuro.svg">
  <img src="figuras/ejercicio-13-costos-claro.svg" alt="Rotaciones totales del splay, de subir a la raíz y de la cota del lema, en función de n">
</picture>

**Figura 2.** Los totales de la tabla en escala logarítmica, para $n = 4, 8, \dots, 1024$. «Subir a la raíz» crece como $n^2$, el splay como $n$ y la cota del lema como $n \log n$.

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="figuras/ejercicio-13-splay-animado-oscuro.gif">
  <img src="figuras/ejercicio-13-splay-animado-claro.gif" alt="Animación de splay y subir a la raíz sobre un camino de 8 nodos, acceso por acceso">
</picture>

**Figura 3.** Splay (izquierda) y subir a la raíz (derecha) sobre el camino de $8$ nodos, acceso por acceso. Después del primer acceso, el splay deja un árbol de profundidad $5$ y subir a la raíz uno de profundidad $7$. Al final el splay suma $22$ rotaciones y subir a la raíz $35$, como en la tabla.

**Qué dice esto.** La diferencia es el orden de las dos rotaciones del caso zig-zig. El splay rota primero el padre y casi divide a la mitad la profundidad de los nodos del camino de acceso; subir a la raíz deja un camino casi igual de largo y la siguiente clave está otra vez en el fondo (Conferencia 4, §6). La cuenta del lema no cierra para rotaciones simples: los rangos se telescopian pero los «+1» no, y solo la concavidad del logaritmo, que aparece al agrupar dos rotaciones, los paga.

---

## ¿Es ajustada la cota?

La cota $O(n\log n)$ y los números de la tabla anterior sugieren una pregunta: el costo medido del splay ($4{,}37$ por acceso para $n = 1024$) parece no crecer como $\log n$. Esta sección lo confirma.

**No lo es.** La cota $O(n\log n)$ del lema de acceso no es ajustada para esta secuencia.

**Cota inferior.** El primer acceso cuesta $n-1$ y, después de cada acceso, la clave siguiente no está en la raíz (la raíz es la clave anterior), así que cada acceso posterior cuesta al menos $1$:

$$\text{costo total} \ge (n-1) + (n-1) = 2n-2 = \Omega(n).$$

**Costo real.** Medido en la tabla anterior, el costo total del splay es $8, 22, 54, 256, 1096, 4478$ para $n = 4, 8, 16, 64, 256, 1024$, es decir, por acceso $2{,}00;\ 2{,}75;\ 3{,}38;\ 4{,}00;\ 4{,}28;\ 4{,}37$: se estabiliza alrededor de $4{,}4$ en vez de crecer como $\log n$. Es lo que predice el **teorema del acceso secuencial** (Tarjan, 1985): acceder a todas las claves en orden en un splay tree cuesta $O(n)$ en total, sea cual sea la forma inicial. Su demostración no sale del lema de acceso solo y aquí se cita, no se prueba. Es consistente con lo que mide la Conferencia 4, §6 (de $4{,}2$ a $4{,}4$ rotaciones por acceso para $n$ entre $100$ y $800$).

**Por qué el lema no alcanza.** El lema acota cada acceso por separado con $3(r(t) - r(x)) + 1$, y la suma de esas cotas con los tamaños reales $s_k$ de los subárboles accedidos sigue creciendo como $n\log n$:

| $n$ | promedio de $\log_2(n/s_k)$ |
|---|---|
| 64 | 4,09 |
| 256 | 5,28 |
| 1024 | 6,52 |
| 4096 | 7,78 |

La pérdida no está en la cota gruesa $r(x) \ge 0$, sino en que el lema trata cada acceso aislado y no ve que accesos consecutivos se ayudan entre sí.

**Con la otra orientación del camino** (raíz $1$ y cada nodo con hijo derecho), el primer acceso no necesita rotaciones (la clave $1$ ya está en la raíz; con la convención de contar $1$ si el nodo ya es la raíz, cuesta $1$) y cada uno de los siguientes cuesta exactamente $1$ rotación: el total medido en rotaciones es $n-1$ ($3$, $63$ y $1023$ para $n = 4, 64, 1024$), o $n$ con esa convención.

---

## Verificación con código

El archivo [`ejercicio-13.py`](ejercicio-13.py) implementa el árbol con `rotar`, `splay` y `subir_a_la_raiz`, calcula el potencial y verifica el lema de acceso en cada acceso. Salida parcial:

```
n = 4, splay sobre el camino 4(3(2(1))): potencial inicial = 4.58
```

| acceso | prof. | rot. | árbol | $\Phi$ | amortizado | cota del lema |
|---|---|---|---|---|---|---|
| 1 | 3 | 3 | $1(.,4(2(.,3),.))$ | 4,58 | 3,00 | 7,00 |
| 2 | 2 | 2 | $2(1,4(3,.))$ | 3,00 | 0,42 | 4,00 |
| 3 | 2 | 2 | $3(2(1,.),4)$ | 3,00 | 2,00 | 7,00 |
| 4 | 1 | 1 | $4(3(2(1,.),.),.)$ | 4,58 | 2,58 | 7,00 |

```
Invariante de 'subir a la raíz' con n = 8 (árbol antes del acceso k):
  antes del acceso 3: 2(1,8(7(6(5(4(3,.),.),.),.),.))
  antes del acceso 4: 3(2(1,.),8(7(6(5(4,.),.),.),.))
  ...
  antes del acceso 8: 7(6(5(4(3(2(1,.),.),.),.),.),8)

Otra orientación (raíz 1, hijo derecho):
  n =     4: splay total = 3 (= n - 1)
  n =    64: splay total = 63 (= n - 1)
  n =  1024: splay total = 1023 (= n - 1)
```

La traza de $n = 4$ coincide con «Qué pasa con $n = 4$», el invariante del Lema 2 coincide con los árboles impresos para $n = 8$ y las tablas de «Comparación con la Conferencia 4, §6» y «¿Es ajustada la cota?» son las de la salida completa del archivo.

## Resumen de resultados

1. **Potencial inicial del camino:** $\Phi_0 = \log_2 n! \le n\log_2 n$.
2. **Cota con el lema de acceso:** cada acceso cuesta amortizado a lo sumo $3\log_2 n + 1$; telescopiando, el total es a lo sumo $4n\log_2 n + n = O(n\log n)$.
3. **Comparación con la Conferencia 4, §6:** subir a la raíz cuesta exactamente $(n-1)(n+2)/2 = \Theta(n^2)$ en este camino (invariante: antes del acceso $k$, el nodo $k$ está a profundidad $n-k+1$); el splay no.
4. **¿Ajustada?** No: el costo real es $\Theta(n)$ (alrededor de $4{,}4$ rotaciones por acceso), por el teorema del acceso secuencial. El lema solo da $O(n\log n)$ porque acota cada acceso por separado.

## Referencias

- Conferencia 4, §5: rango, potencial, lema de acceso y su consecuencia para $m$ accesos.
- Conferencia 4, §6: splay contra subir a la raíz; ejercicio 4 de esa conferencia ($\Theta(n^2)$ con subir a la raíz).
- R. E. Tarjan, *Sequential access in splay trees takes linear time*, Combinatorica 5 (1985): teorema del acceso secuencial (citado, no demostrado).
