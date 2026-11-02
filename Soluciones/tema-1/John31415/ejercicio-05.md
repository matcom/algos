## Problema

Dado el algoritmo de detección de ciclos de Floyd (algoritmo de la tortuga y la liebre) sobre una lista simplemente enlazada utilizando dos punteros (`slow` que avanza de a $1$ paso y `fast` que avanza de a $2$ pasos):

1. **Correctitud Parcial e Invariante:** Enuncie el invariante del ciclo y demuestre la condición necesaria y suficiente (si y solo si) para que ambos punteros colisionen.
2. **Terminación y Función Potencial:** Defina formalmente las funciones potencial $\Phi$ para los escenarios sin ciclo y con ciclo que garanticen la terminación del algoritmo.
3. **Análisis de Complejidad:** Determine los costos temporal y espacial en el peor caso.

---

## Solución

### 1. Algoritmo de Referencia

```python
def has_cycle(head):
    slow = head
    fast = head
    while fast is not None and fast.next is not None:
        slow = slow.next
        fast = fast.next.next
        if slow == fast:
            return True  # Se ha detectado un ciclo
    return False  # Se ha alcanzado el final de la lista finita

```

---

### 2. Invariante del Ciclo y Demostración de Correctitud

Para una lista enlazada, denotamos:

* $\mu \geq 0$: La cantidad de nodos en el camino acíclico inicial (desde la cabeza hasta la entrada del ciclo).
* $\lambda \geq 1$: La longitud del ciclo (en número de nodos).
* $d(v)$: La cantidad acumulada de movimientos realizados por el puntero $v$ desde el nodo inicial `head`. Esta cantidad representa los movimientos efectuados y no la distancia estructural hasta el nodo, pues un mismo nodo puede visitarse varias veces cuando existe un ciclo.

#### Declaración del Invariante ($I$)

En la $k$-ésima iteración del ciclo ($k \geq 0$), la cantidad acumulada de movimientos realizados por el puntero `slow` es $d(\text{slow}) = k$, mientras que la cantidad acumulada de movimientos realizados por el puntero `fast` es $d(\text{fast}) = 2k$, siempre que los punteros hayan realizado dichos movimientos.

Formalmente:


$$d(\text{slow}) = k, \qquad d(\text{fast}) = 2k$$

#### Demostración por Inducción

1. **Inicialización ($k = 0$):**
Antes de entrar al ciclo, ambos punteros coinciden en `head`. Sus distancias recorridas son $d(\text{slow}) = 0$ y $d(\text{fast}) = 2(0) = 0$. El invariante se cumple de forma trivial.
2. **Mantenimiento ($k \to k + 1$):**
Asumiendo válido el invariante en la iteración $k$:
* `slow` avanza a `slow.next`, de modo que $d(\text{slow}_{\text{nuevo}}) = k + 1$.
* `fast` avanza a `fast.next.next`, de modo que $d(\text{fast}_{\text{nuevo}}) = 2k + 2 = 2(k + 1)$.


Se preserva el invariante para la iteración $k + 1$.
3. **Conclusión (Equivalencia Lógica: Colisión $\iff$ Existe Ciclo)**
* **Necesidad ($\Rightarrow$, Si ocurre una colisión $\implies$ existe un ciclo):**
Supongamos que la lista no contiene ciclos y tiene una longitud finita $N$. En cada iteración $k \geq 1$ en la que ambos punteros apuntan a nodos válidos, `slow` se encuentra en la posición $k$ y `fast` en la posición $2k$. Como $k \neq 2k$, ambos punteros no pueden encontrarse en el mismo nodo. Además, al ser la lista finita y no contener ciclos, `fast` o `fast.next` alcanzará `None`, provocando la terminación del algoritmo sin colisión. Por contraposición, si ocurre una colisión, necesariamente existe un ciclo.
* **Suficiencia ($\Leftarrow$, Si existe un ciclo $\implies$ ocurre una colisión):**
Una vez transcurridos $k \geq \mu$ pasos, `slow` ingresa al ciclo. A partir de este instante, ambos punteros residen en el ciclo de longitud $\lambda$. La diferencia de distancia recorrida dentro del ciclo (la posición relativa de `fast` respecto a `slow`) viene determinada por la congruencia:

$$D_k = (2k - k) \pmod{\lambda} = k \pmod{\lambda}$$


Por tanto, ambos punteros coinciden si y solo si:

$$k \equiv 0 \pmod{\lambda}$$


Como el algoritmo comprueba la igualdad después de cada movimiento, la primera colisión ocurre en la menor iteración positiva múltiplo de $\lambda$ que sea mayor o igual que $\mu$:

$$k_{\min} = \lambda \left\lceil \frac{\max(1, \mu)}{\lambda} \right\rceil$$


Por tanto, necesariamente se produce una colisión en tiempo finito y el algoritmo retorna `True`.



En consecuencia, el algoritmo detecta un ciclo si y solo si este existe.

---

### 3. Demostración de Terminación mediante Función Potencial ($\Phi$)

#### Caso A: Lista Sin Ciclo (Longitud Total $N$)

Definimos la función potencial $\Phi(k)$ como una medida de las posiciones que le restan recorrer al puntero `fast` antes de alcanzar el final de la lista:


$$\Phi(k) = \max(0, N - 2k)$$

1. **No negatividad:** $\Phi(k) \geq 0, \ \forall k \geq 0$.
2. **Decrecimiento estricto:** En cada iteración donde el ciclo continúa, `fast` y `fast.next` apuntan a nodos existentes. Por tanto, $N - 2k \geq 2$ y, después de avanzar dos posiciones:

$$\Phi(k + 1) = N - 2(k + 1) = \Phi(k) - 2 < \Phi(k)$$



Puesto que $\Phi(k) \in \mathbb{Z}_{\geq 0}$ y decrece estrictamente en cada iteración, el algoritmo garantiza su terminación. En particular, realiza exactamente $\lfloor N/2 \rfloor$ iteraciones.

#### Caso B: Lista Con Ciclo ($\mu$ nodos de cola, $\lambda$ nodos de ciclo)

Definimos el potencial estructurado en dos fases consecutivas:

1. **Fase 1: Entrada de `slow` al ciclo ($k < \mu$):**

$$\Phi_1(k) = \mu - k$$



Representa la cantidad de pasos que restan para que `slow` alcance la entrada del ciclo. En cada iteración:

$$\Phi_1(k + 1) = \Phi_1(k) - 1$$



El potencial decrece estrictamente hasta alcanzar $0$ en $k = \mu$.
2. **Fase 2: Persecución dentro del ciclo ($k \geq \mu$):**
Definimos $\Phi_2(k)$ como la cantidad de iteraciones que restan hasta la siguiente colisión. Formalmente, para un estado en el que el algoritmo todavía no ha detectado la colisión:

$$\Phi_2(k) = \min \{ j \in \mathbb{Z}_{\geq 1} : (k + j) \equiv 0 \pmod{\lambda} \}$$



En el estado de colisión definimos $\Phi_2(k) = 0$.
Esta función representa el número de iteraciones necesarias para que la diferencia relativa entre los punteros, que es $D_k = k \pmod{\lambda}$, vuelva a cero.
En cada iteración en la que todavía no se produce la colisión, el potencial disminuye exactamente en una unidad:

$$\Phi_2(k + 1) = \Phi_2(k) - 1$$



Cuando $\Phi_2(k) = 1$, la siguiente iteración provoca la colisión y el potencial alcanza $0$, momento en el que el algoritmo termina.

Ambas funciones potencial son enteras y no negativas, y cada fase concluye en un número finito de iteraciones. Por tanto, el algoritmo garantiza su terminación también cuando existe un ciclo.

---

### 4. Análisis de Complejidad

* **Complejidad Temporal:** $\mathcal{O}(N)$ en el peor caso, donde $N = \mu + \lambda$ denota el número de nodos distintos alcanzables desde la cabeza de la lista.
* **Sin ciclo:** Realiza exactamente $\lfloor N/2 \rfloor$ iteraciones, puesto que `fast` avanza dos posiciones en cada una de ellas, hasta alcanzar el final de la lista. Por tanto, el costo temporal es $\mathcal{O}(N)$.
* **Con ciclo:** El puntero `slow` requiere $\mu$ iteraciones para entrar al ciclo. Una vez dentro, la persecución concluye en como máximo $\lambda$ iteraciones adicionales. El total está acotado por:

$$\mu + \lambda = N \implies \mathcal{O}(N)$$




* **Complejidad Espacial:** $\mathcal{O}(1)$ en el peor caso. El algoritmo únicamente requiere dos variables de puntero auxiliares (`slow` y `fast`), independientemente de la cantidad de nodos de la lista.