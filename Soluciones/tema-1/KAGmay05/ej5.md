## Problema 5

Detección de ciclos en una lista enlazada con dos punteros que avanzan a velocidades 1 y 2 (algoritmo de Floyd). Demuestra que se encuentran si y solo si hay un ciclo, con un invariante, y que termina,
con un potencial. Da el costo.

### Respuesta

En el algoritmo se usan dos punteros: el lento t avanza 1 nodo por paso y el rápido h avanza 2.

```text
FLOYD(head):
    t ← head
    h ← head
    while h ≠ null y h.next ≠ null:
        t ← t.next            // 1 paso
        h ← h.next.next       // 2 pasos
        si t = h:
            devolver VERDADERO   // hay ciclo
    devolver FALSO               // el rápido llegó a null: no hay ciclo
```


$x_0 = \text{head}$ y $x_{i+1} = x_i.\text{next}$, o sea, $x_i$ es el nodo al que se llega después de $i$ saltos desde la cabeza.

- Sin ciclo: la lista tiene $n$ nodos $x_0, \dots, x_{n-1}$ todos distintos, y $x_n = \text{null}$.
- Con ciclo: existen dos números:
  - $\mu \ge 0$: longitud de la "cola", es decir, el índice del primer nodo del ciclo.
  - $\lambda \ge 1$: longitud del ciclo.

  Los nodos $x_0, \dots, x_{\mu+\lambda-1}$ son todos distintos, y para todo $i \ge \mu$ se cumple $x_{i+\lambda} = x_i$.

Si hay ciclo,

$$
x_i = x_j \iff \big(i = j\big) \ \text{ o } \ \big(i, j \ge \mu \ \text{y}\ \lambda \mid (j - i)\big). \tag{$\ast$}
$$

Esto se cumple porque antes de $\mu$ todos los nodos son distintos y dentro del ciclo la posición solo depende de $(i-\mu) \bmod \lambda$.

### Invariante del while

Sea $k$ el número de iteraciones completadas. El invariante es:

> $I(k)$: $\;t = x_k$, $\;h = x_{2k}$, y para todo $1 \le j \le k$ se cumple $x_j \neq x_{2j}$ (todavía no se han encontrado; esta última parte vale si el algoritmo no ha devuelto nada).

Inicialización ($k=0$): $t = h = \text{head} = x_0$, y la condición sobre los $j$ es vacía.

Mantenimiento: supongamos $I(k)$ y que se entra al cuerpo del bucle. Entonces $h = x_{2k} \ne \text{null}$ y $x_{2k+1} \ne \text{null}$, así que los saltos son válidos.
- $t \leftarrow t.\text{next} = x_{k+1}$.
- $h \leftarrow h.\text{next}.\text{next} = x_{2k+2} = x_{2(k+1)}$.
- Si $x_{k+1} = x_{2(k+1)}$, el algoritmo devuelve VERDADERO. Si no, sigue y se cumple $x_{k+1} \neq x_{2(k+1)}$, que completa $I(k+1)$. 

### (⇒) Si se encuentran, hay ciclo

Si el algoritmo devuelve VERDADERO en la iteración $k \ge 1$, entonces, por el invariante, $x_k = x_{2k}$ con $k \ne 2k$. Tenemos el mismo nodo con dos índices distintos. En una lista sin ciclo todos los nodos $x_0, \dots, x_{n-1}$ son distintos (y null nunca se compara porque el bucle lo evita). Por lo tanto tiene que haber ciclo. ✔

Dicho al revés: si no hay ciclo, la condición t = h nunca se cumple. Además, el rápido está siempre adelante ($2k > k$), así que no puede "alcanzar" al lento.

### (⇐) Si hay ciclo, se encuentran

Si hay ciclo, ningún $x_i$ es null, así que la guarda del bucle siempre es verdadera. El algoritmo solo puede salir por devolver VERDADERO, y hay que ver que eso ocurre en algún momento.

Por $(\ast)$, con $i = k$ y $j = 2k$:

$$
x_k = x_{2k} \iff k \ge \mu \ \text{y}\ \lambda \mid k .
$$

Así que se encuentran en el primer $k \ge 1$ que sea múltiplo de $\lambda$ y además $\ge \mu$. Ese $k$ siempre existe: entre $\max(\mu,1)$ y $\max(\mu,1) + \lambda - 1$ hay $\lambda$ enteros consecutivos, y uno de ellos es múltiplo de $\lambda$. Entonces

$$
k_{\text{encuentro}} \le \mu + \lambda .
$$

Esto prueba la existencia. La terminación la justifico más formalmente con un potencial en la sección siguiente.

### Potencial

Necesito una cantidad $\Phi \in \mathbb{N}$ que baje estrictamente en cada iteración. Como no puede bajar para siempre, el bucle termina.

### Caso sin ciclo

$$
\Phi_k = n - 2k .
$$

- El bucle solo entra si $x_{2k} \ne \text{null}$ y $x_{2k+1} \ne \text{null}$, o sea $2k+1 \le n-1$, es decir $\Phi_k \ge 2$. Por tanto $\Phi \ge 0$ mientras el bucle corre.
- Cada iteración $\Phi_{k+1} = \Phi_k - 2$, así que baja estrictamente.

Entonces hay a lo sumo $\lfloor n/2 \rfloor$ iteraciones y luego devuelve FALSO.

### Caso con ciclo

Lo hago en dos fases. La idea es: primero el lento tiene que entrar al ciclo y luego el rápido lo "persigue" dentro del ciclo.

Fase 1 ($k < \mu$): el lento todavía está en la cola.
$$
\Phi^{(1)}_k = \mu - k \quad (\text{baja en 1 por paso}).
$$

Fase 2 ($k \ge \mu$): ambos están dentro del ciclo. Defino la distancia de persecución, que es cuántos pasos hacia adelante dentro del ciclo le faltan al rápido para llegar al lento:
$$
D_k = \big((k - \mu) - (2k - \mu)\big) \bmod \lambda = (-k) \bmod \lambda \ \in \{0, \dots, \lambda - 1\}.
$$

- En cada paso el lento avanza 1 y el rápido 2, así que el rápido "gana" una posición: si $D_k > 0$, entonces $D_{k+1} = D_k - 1$.
- $D_k = 0 \iff \lambda \mid k$, y como $k \ge \mu$, por $(\ast)$ eso es exactamente $t = h$, o sea, el algoritmo termina.

Potencial combinado. Uso el par $\Phi_k = \big(\Phi^{(1)}_k,\ D_k\big)$ con orden lexicográfico (primero la fase 1 y luego la fase 2). Es un orden bien fundado y baja estrictamente en cada iteración. Por lo tanto, en total hay como máximo

$$
\underbrace{\mu}_{\text{fase 1}} + \underbrace{\lambda}_{\text{fase 2}}
$$

iteraciones. (El caso $\mu = 0$ funciona igual: empezamos en $k=1$ con $D_1 = \lambda - 1$ y se encuentran en $k = \lambda$.)

### Costo

Sea $n$ el número de nodos distintos de la lista (con ciclo, $n = \mu + \lambda$).

| Recurso | Costo |
|---|---|
| Iteraciones del bucle | sin ciclo: $\le \lfloor n/2 \rfloor$; con ciclo: $\le \mu + \lambda = n$ |
| Avances de puntero (.next) | 3 por iteración $\Rightarrow \le 3n$ |
| Tiempo | $\Theta(n)$ en el peor caso, o sea $O(\mu + \lambda)$ |
| Memoria extra | $O(1)$: solo dos punteros |

Comparado con la solución ingenua de guardar los nodos visitados en un conjunto hash, que es $O(n)$ en tiempo pero también $O(n)$ en memoria, Floyd tiene el mismo tiempo asintótico y memoria constante.


- Invariante: después de $k$ pasos, $t = x_k$ y $h = x_{2k}$, y no se han encontrado antes.
- Se encuentran ⟺ hay ciclo: $x_k = x_{2k}$ con $k \ne 2k$ obliga a un nodo repetido, y con ciclo eso pasa exactamente cuando $k \ge \mu$ y $\lambda \mid k$, lo que siempre ocurre para algún $k \le \mu + \lambda$.
- Terminación: el potencial $n - 2k$ (sin ciclo) o $(\mu - k,\ D_k)$ en orden lexicográfico (con ciclo) baja estrictamente en cada paso.
- Costo: tiempo $O(n)$, memoria $O(1)$.
