# Ejercicio 5. Detección de ciclos con dos punteros (Floyd)

Dificultad: ★★ · Código: [`ejercicio-05.py`](ejercicio-05.py)

---

## Enunciado

> Detección de ciclos en una lista enlazada con dos punteros que avanzan a velocidades 1 y 2 (algoritmo de Floyd). Demuestra que se encuentran si y solo si hay un ciclo, con un invariante, y que termina, con un potencial. Da el costo.

## Qué se pide

1. Demostrar con un **invariante** que el algoritmo devuelve `True` si y solo si la lista tiene un ciclo (correctitud parcial).
2. Demostrar con un **potencial** que el algoritmo termina en los dos casos (con y sin ciclo).
3. Dar el costo en tiempo y memoria.

## Preliminares

**El algoritmo.** Se recibe `head`, la cabeza de una lista enlazada; cada nodo tiene un campo `next` que apunta al siguiente o vale `None`.

```python
def tiene_ciclo(head):
    slow = fast = head
    while fast is not None and fast.next is not None:
        slow = slow.next            # avanza 1
        fast = fast.next.next       # avanza 2
        if slow is fast:
            return True
    return False
```

**La idea.** Dos corredores salen a la vez de la cabeza de la lista, uno al doble de velocidad que el otro (`fast` avanza 2 nodos por vuelta y `slow` avanza 1). Si la pista es recta, el rápido llega al final y la carrera se acaba. Si la pista tiene un ciclo, el rápido entra, da vueltas y termina alcanzando al lento por detrás. Detectar ese encuentro equivale a detectar el ciclo, y solo se guardan dos punteros. Las trazas completas de tres listas están en la sección «Ejemplos».

**Teorema.** El algoritmo termina para toda lista y devuelve `True` si y solo si la lista tiene un ciclo.

**Mapa de la demostración.** Primero se demuestra un invariante común: dónde están `slow` y `fast` después de $k$ vueltas. Con él se prueban tres cosas, en este orden: (1) si devuelve `True`, hay un ciclo; (2) si no hay ciclo, termina y devuelve `False`; (3) si hay ciclo, termina y devuelve `True`.

**Técnicas** (Conferencia 3, §1). Un **invariante** (inicialización, mantenimiento, conclusión) prueba la correctitud parcial; un **potencial** entero no negativo que baja en cada vuelta prueba la terminación.

**La forma de una lista.** Sea $n$ el número de nodos distintos alcanzables desde `head`, y sea la sucesión

$$x_0 = \text{head}, \qquad x_{i+1} = x_i.\text{next}.$$

- **Caso A, sin ciclo.** $x_0, \dots, x_{n-1}$ son distintos y $x_n = \text{None}$. Para $i \ge n$ se toma $x_i = \text{None}$.
- **Caso B, con ciclo.** $x_0, \dots, x_{n-1}$ son distintos y $x_n = x_\mu$ para algún $0 \le \mu \le n-1$. Se llama $\mu$ a la **longitud de la cola** y $\lambda = n - \mu \ge 1$ a la **longitud del ciclo**.

**Hecho 1 (caso A).** Si $i \ne j$ y ambos son menores que $n$, entonces $x_i \ne x_j$.

**Hecho 2 (caso B).** Para $i \ge \mu$ se cumple $x_{i+\lambda} = x_i$. Por tanto, para $i, j \ge \mu$:

$$x_i = x_j \iff i \equiv j \pmod{\lambda}.$$

Además, si $i < \mu$ el nodo $x_i$ no vuelve a aparecer.

**Ejemplo.** En la lista $1 \to 2 \to 3 \to 4 \to 5 \to 3$: $n = 5$, $\mu = 2$ (el nodo $3$ es $x_2$) y $\lambda = 3$. La sucesión es $x_0 = 1,\ x_1 = 2,\ x_2 = 3,\ x_3 = 4,\ x_4 = 5,\ x_5 = 3,\ x_6 = 4, \dots$

---

## El invariante

Todo lo que sigue se apoya en saber dónde están los dos punteros en cada vuelta. Como `slow` avanza 1 y `fast` avanza 2, después de $k$ vueltas deberían estar en los nodos de índice $k$ y $2k$.

**Invariante $I(k)$.** Después de $k$ vueltas completas del cuerpo del `while` ($k \ge 0$):

$$\text{slow} = x_k \quad\text{y}\quad \text{fast} = x_{2k}.$$

**Lema 1.** $I(k)$ vale para toda vuelta $k$ que se alcance.

**Demostración (por inducción sobre $k$).**

**Inicialización ($k = 0$).** Al empezar, `slow = fast = head`, y $x_0 = x_{2\cdot 0} = \text{head}$.

**Mantenimiento.** Se supone $I(k)$ y que se ejecuta una vuelta más, es decir, `fast` y `fast.next` no son `None`.

**Paso 1.** Por $I(k)$, `fast` $= x_{2k} \ne \text{None}$, y como `fast.next` $\ne$ `None`, existe $x_{2k+1}$.

**Paso 2.** La vuelta hace `slow = slow.next`:

$$\text{slow}_{\text{nuevo}} = x_k.\text{next} = x_{k+1}.$$

**Paso 3.** La vuelta hace `fast = fast.next.next`:

$$\text{fast}_{\text{nuevo}} = x_{2k}.\text{next}.\text{next} = x_{2k+2}.$$

**Paso 4.** Después de la vuelta $k+1$: slow $= x_{k+1}$ y fast $= x_{2(k+1)}$. Vale $I(k+1)$. $\blacksquare$

---

## Si devuelve `True`, hay un ciclo

Esta es la primera mitad del «si y solo si»: `True` solo puede aparecer cuando hay ciclo. La intuición es que, en una lista recta, cada nodo se visita una sola vez, así que dos punteros en índices distintos nunca pueden estar en el mismo nodo.

**Proposición 1.** Si el algoritmo devuelve `True`, la lista tiene un ciclo.

**Demostración.**

**Paso 1.** Se supone que devuelve `True` en la vuelta $k+1 \ge 1$; entonces `slow is fast`.

**Paso 2.** Por el Lema 1:

$$x_{k+1} = x_{2k+2}.$$

**Paso 3.** Los índices son distintos:

$$(2k+2) - (k+1) = k + 1 \ge 1.$$

**Paso 4.** Se supone que estamos en el caso A, donde $x_i$ es un nodo real si y solo si $i < n$. La vuelta se ejecutó, así que `fast.next` $= x_{2k+1}$ era real: $2k+1 < n$. Entonces $k+1 < n$ y `slow` $= x_{k+1}$ es un nodo real. Como `slow is fast`, también $x_{2k+2}$ es real, es decir, $2k+2 < n$.

**Paso 5.** Así $k+1$ y $2k+2$ son dos índices distintos (Paso 3), ambos menores que $n$, con el mismo nodo. Eso contradice el Hecho 1. Por tanto no estamos en el caso A: hay un ciclo. $\blacksquare$

---

## Si no hay ciclo, termina y devuelve `False`

Segunda parte: si la lista es recta, el rápido llega al final y el programa termina. Para demostrarlo hay que medir cuánto le falta a `fast` para llegar al final.

Se está en el caso A. Se usa el potencial

$$\Phi_k = n - 2k,$$

con $k$ el número de vueltas completadas. $\Phi_k$ cuenta los nodos que le quedan a `fast`, desde su posición $x_{2k}$ hasta el último nodo $x_{n-1}$. Cada vuelta lo avanza 2 nodos, así que $\Phi$ baja 2, y el cuerpo del `while` solo se ejecuta mientras queden al menos 2 nodos ($\Phi_k \ge 2$).

**Proposición 2.** Sin ciclo, el algoritmo hace exactamente $\lfloor n/2 \rfloor$ vueltas y devuelve `False`.

**Demostración.**

**Paso 1. Condición de entrada.** Por el Lema 1, `fast` $= x_{2k}$. El cuerpo se ejecuta si $x_{2k} \ne \text{None}$ y $x_{2k+1} \ne \text{None}$:

$$2k + 1 \le n - 1 \iff \Phi_k \ge 2.$$

**Paso 2. $\Phi$ es entero y baja.** $\Phi_k$ es un entero y

$$\Phi_{k+1} = n - 2(k+1) = \Phi_k - 2.$$

**Paso 3. Terminación.** Mientras el ciclo corre, $\Phi_k \ge 2$; como baja $2$ en cada vuelta, en algún momento $\Phi_k \le 1$ y la condición del `while` es falsa.

**Paso 4. Número de vueltas.** El cuerpo se ejecuta para $k = 0, 1, \dots$ mientras $2k+1 \le n-1$, es decir, $\lfloor n/2 \rfloor$ vueltas.

**Paso 5. Nunca devuelve `True`.** Por la Proposición 1, devolver `True` implicaría que hay ciclo.

**Paso 6.** Al terminar el `while` sin haber devuelto, ejecuta `return False`. $\blacksquare$

---

## Si hay ciclo, termina y devuelve `True`

Tercera parte: si hay ciclo, el rápido acaba alcanzando al lento. La imagen es una pista circular de $\lambda$ nodos: una vez que los dos corredores están dentro, `fast` avanza un paso más que `slow` por vuelta, así que la distancia que le falta para alcanzarlo baja de uno en uno hasta llegar a 0. Esa distancia es el potencial.

Se está en el caso B, con cola $\mu$ y ciclo $\lambda$.

**Paso 1. El `while` no termina por `None`.** Todos los $x_i$ existen, así que `fast` y `fast.next` nunca son `None`. El `while` solo se detiene por `return True`.

**Paso 2. Cuándo coinciden.** Por el Lema 1, tras $k \ge 1$ vueltas los punteros coinciden si y solo si $x_k = x_{2k}$.

**Paso 3. Antes de la cola.** Si $k < \mu$, el nodo $x_k$ no se repite (Hecho 2) y $2k \ne k$, luego $x_k \ne x_{2k}$.

**Paso 4. Dentro del ciclo.** Si $k \ge \mu$, también $2k \ge \mu$ y, por el Hecho 2:

$$x_k = x_{2k} \iff 2k \equiv k \pmod{\lambda} \iff \lambda \mid k.$$

**El potencial: el hueco dentro del ciclo.** Sea $k_0 = \max(\mu, 1)$. Para $k \ge k_0$ ambos punteros están en el ciclo. Se define

$$\Phi_k = (-k) \bmod \lambda \in \{0, 1, \dots, \lambda - 1\}.$$

Mide cuántos pasos le faltan a `fast`, avanzando por el ciclo, para llegar al nodo donde está `slow`.

**Por qué esta fórmula.** Después de $k$ vueltas, `slow` está en $x_k$ y `fast` en $x_{2k}$. Si `fast` avanza $d$ pasos más por el ciclo, llega a $x_{2k+d}$. Coincide con `slow` cuando $x_{2k+d} = x_k$, y por el Hecho 2 (todos los índices son $\ge \mu$) eso ocurre cuando

$$2k + d \equiv k \pmod{\lambda}, \quad\text{es decir,}\quad d \equiv -k \pmod{\lambda}.$$

El menor $d \ge 0$ que lo cumple es $(-k) \bmod \lambda$. El «mod $\lambda$» aparece porque en un ciclo de $\lambda$ nodos la distancia que falta va de $0$ a $\lambda - 1$.

**Proposición 3.** Con ciclo, el algoritmo devuelve `True` en la vuelta

$$k^\ast = \lambda \cdot \left\lceil \frac{\max(\mu, 1)}{\lambda} \right\rceil \le n.$$

**Demostración.**

**Paso 5.** $\Phi_k$ es un entero con $0 \le \Phi_k \le \lambda - 1$.

**Paso 6. Baja en cada vuelta.** Si $\Phi_k \ge 1$:

$$\Phi_{k+1} = (-(k+1)) \bmod \lambda = (\Phi_k - 1) \bmod \lambda = \Phi_k - 1,$$

porque $\Phi_k - 1 \ge 0$ y no hay «vuelta» del módulo.

**Paso 7. Se detiene en $\Phi_k = 0$.** Entonces $\lambda \mid k$ y, por el paso 4, los punteros coinciden. La comparación `slow is fast` se hace al final de la vuelta, con $k \ge k_0 \ge 1$.

**Paso 8. Terminación.** $\Phi$ es un entero no negativo que baja $1$ por vuelta mientras es positivo, así que llega a $0$ en a lo sumo $\lambda - 1$ vueltas desde $k_0$.

**Paso 9. Valor exacto.** La primera vuelta $k \ge 1$ con coincidencia es la menor $k \ge \max(\mu, 1)$ con $\lambda \mid k$, que es $k^\ast$.

**Paso 10. Cota $k^\ast \le n$.**

- Si $\mu \ge 1$: $k^\ast < \mu + \lambda = n$.
- Si $\mu = 0$: $k^\ast = \lambda = n$. $\blacksquare$

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="figuras/ejercicio-05-floyd-oscuro.gif">
  <img src="figuras/ejercicio-05-floyd-claro.gif" alt="Animación de slow y fast sobre una lista con cola de 3 nodos y ciclo de 5">
</picture>

**Figura 1.** Los dos punteros sobre una lista con cola $\mu = 3$ y ciclo $\lambda = 5$, vuelta por vuelta. Mientras `slow` está en la cola no se usa el potencial. Desde $k = 3$, $\Phi_k = (-k) \bmod 5$ vale $2, 1, 0$, y los punteros coinciden en $k^\ast = 5\lceil 3/5 \rceil = 5$, en el nodo $x_5$.

---

## Costo

Cada vuelta hace un número constante de operaciones (dos desplazamientos de `fast`, uno de `slow` y una comparación): $O(1)$.

| caso | vueltas | tiempo | memoria extra |
|---|---|---|---|
| sin ciclo | $\lfloor n/2 \rfloor$ | $O(n)$ | $O(1)$ |
| con ciclo | $k^\ast \le n$ | $O(n)$ | $O(1)$ |

Solo hay dos punteros, así que la memoria extra es $O(1)$. Es la ventaja frente a guardar los nodos visitados en un conjunto, que necesita $O(n)$.

## Ejemplos

Tres listas pequeñas que cubren los tres casos de la demostración: un ciclo puro, una cola con un ciclo y una lista sin ciclo.

**Ciclo de 3 nodos** $1 \to 2 \to 3 \to 1$: $n = 3$, $\mu = 0$, $\lambda = 3$, luego $k^\ast = 3\lceil 1/3 \rceil = 3$.

| vuelta $k$ | slow $= x_k$ | fast $= x_{2k}$ | ¿coinciden? |
|---|---|---|---|
| 0 | 1 | 1 | (no se comprueba) |
| 1 | 2 | 3 | no |
| 2 | 3 | 2 | no |
| 3 | 1 | 1 | **sí** |

**Cola y ciclo** $1 \to 2 \to 3 \to 4 \to 5 \to 3$: $n = 5$, $\mu = 2$, $\lambda = 3$, luego $k^\ast = 3\lceil 2/3 \rceil = 3$.

| vuelta $k$ | slow | fast | ¿coinciden? |
|---|---|---|---|
| 0 | 1 | 1 | (no se comprueba) |
| 1 | 2 | 3 | no |
| 2 | 3 | 5 | no |
| 3 | 4 | 4 | **sí** |

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="figuras/ejercicio-05-rho-oscuro.svg">
  <img src="figuras/ejercicio-05-rho-claro.svg" alt="Los punteros slow y fast sobre la lista con cola de 2 nodos y ciclo de 3, en las vueltas 0 a 3">
</picture>

**Figura 2.** La lista $1 \to 2 \to 3 \to 4 \to 5 \to 3$ ($\mu = 2$, $\lambda = 3$) en las vueltas $k = 0, \dots, 3$. `slow` está en $x_k$ y `fast` en $x_{2k}$, como dice $I(k)$. En $k = 3 = k^\ast$ coinciden en el nodo $4$.

**Sin ciclo** $1 \to 2 \to 3 \to 4 \to \text{None}$: $n = 4$, hay $\lfloor 4/2 \rfloor = 2$ vueltas.

| vuelta $k$ | slow | fast |
|---|---|---|
| 0 | 1 | 1 |
| 1 | 2 | 3 |
| 2 | 3 | None |

`fast` es `None`, el `while` termina y devuelve `False`.

---

## Verificación con código

El archivo [`ejercicio-05.py`](ejercicio-05.py) construye listas con cola $\mu$ y ciclo $\lambda$, ejecuta el algoritmo vigilando el invariante $I(k)$ en cada vuelta y compara el número de vueltas con las fórmulas:

| caso | $n$ | $\mu$ | $\lambda$ | vueltas | prevista |
|---|---|---|---|---|---|
| ciclo | 3 | 0 | 3 | 3 | 3 |
| ciclo | 5 | 2 | 3 | 3 | 3 |
| sin ciclo | 0 | 0 | 0 | 0 | 0 |
| sin ciclo | 4 | 4 | 0 | 2 | 2 |
| sin ciclo | 3 | 3 | 0 | 1 | 1 |

En 5000 listas aleatorias la respuesta, el invariante y el número de vueltas $k^\ast$ coinciden con las fórmulas, y el máximo de $\text{vueltas}/n$ es $1{,}00$.

El máximo de $\text{vueltas}/n$ se alcanza cuando $\mu = 0$ y $\lambda = n$.

Además, el programa recorre **todas** las listas de hasta $60$ nodos. Salvo los nombres de los nodos, una lista de $n$ nodos queda determinada por a dónde apunta el último: a `None` o a uno de los $n$ nodos. Hay entonces $n + 1$ formas, una por cada par $(\mu, \lambda)$ con $\mu + \lambda = n$, y $1891$ en total para $n \le 60$. En todas, la respuesta, el invariante y el número de vueltas coinciden con las Proposiciones 2 y 3. Es una comprobación exhaustiva para esos tamaños, no una demostración para todo $n$.

## Resumen de resultados

1. **Invariante:** tras $k$ vueltas, `slow` $= x_k$ y `fast` $= x_{2k}$ (inducción sobre $k$).
2. **`True` implica ciclo:** coincidir significa $x_{k+1} = x_{2k+2}$ con índices distintos, y sin ciclo todos los nodos son distintos.
3. **Sin ciclo:** $\Phi_k = n - 2k$ baja $2$ por vuelta; hay $\lfloor n/2 \rfloor$ vueltas y devuelve `False`.
4. **Con ciclo:** $\Phi_k = (-k) \bmod \lambda$ baja $1$ por vuelta hasta $0$; los punteros coinciden en $k^\ast = \lambda\lceil \max(\mu,1)/\lambda \rceil \le n$.
5. **Costo:** $O(n)$ en tiempo y $O(1)$ de memoria extra.

## Referencias

- Conferencia 3, §1: invariantes, potenciales, correctitud parcial y terminación.
