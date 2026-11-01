## Problema

Dado el algoritmo de detección de ciclos de Floyd (*algoritmo de la tortuga y la liebre*) sobre una lista simplemente enlazada utilizando dos punteros (`slow` que avanza de a $1$ paso y `fast` que avanza de a $2$ pasos):

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

* $\mu \ge 0$: La cantidad de nodos en el camino acíclico inicial (desde la cabeza hasta la entrada del ciclo).
* $\lambda \ge 1$: La longitud del ciclo (en número de nodos).
* $d(v)$: La distancia en aristas recorrida por un puntero $v$ desde el nodo inicial `head`.

#### Declaración del Invariante ($I$)

> *"En la $k$-ésima iteración del ciclo ($k \ge 0$), si el puntero `fast` no ha alcanzado la referencia vacía (`None`), la distancia acumulada recorrida por el puntero `slow` es $d(\text{slow}) = k$, y la distancia acumulada por el puntero `fast` es $d(\text{fast}) = 2k$."*

#### Demostración por Inducción

1. **Inicialización ($k = 0$):**
Antes de entrar al ciclo, ambos punteros coinciden en `head`. Sus distancias son $d(\text{slow}) = 0$ y $d(\text{fast}) = 2(0) = 0$. El invariante se cumple de forma trivial.
2. **Mantenimiento ($k \to k + 1$):**
Asumiendo válido el invariante en la iteración $k$:
* `slow` avanza a `slow.next`, de modo que $d(\text{slow}_{\text{nuevo}}) = k + 1$.
* `fast` avanza a `fast.next.next`, de modo que $d(\text{fast}_{\text{nuevo}}) = 2k + 2 = 2(k + 1)$.


Se preserva el invariante para la iteración $k + 1$.
3. **Conclusión (Equivalencia Lógica: Colisión $\iff$ Existe Ciclo)**
* **Suficiencia ($\Leftarrow$, Si no hay ciclo $\implies$ No hay colisión y retorna `False`):**
Si la lista es finita de longitud total $N$, no existen componentes conexas cerradas. En el paso $k = \lceil N/2 \rceil$, el puntero `fast` o su sucesor inmediato `fast.next` alcanzará `None`. El ciclo finaliza y el algoritmo retorna `False` correctamente.
* **Necesidad ($\Rightarrow$, Si hay ciclo $\implies$ Ocurre colisión y retorna `True`):**
Una vez transcurridos $k \ge \mu$ pasos, `slow` ingresa al ciclo. A partir de este instante, ambos punteros residen en el ciclo de longitud $\lambda$. La diferencia de distancia recorrida dentro del ciclo (la distancia angular relativa de `fast` respecto a `slow`) responde a la congruencia:

$$D_k = (2k - k) \pmod \lambda = k \pmod \lambda$$


Para la iteración específica $k = \mu + (\lambda - (\mu \pmod \lambda))$, la distancia relativa satisface $D_k \equiv 0 \pmod \lambda$, lo cual implica que ambos punteros se posicionan exactamente sobre la misma celda de memoria (`slow == fast`). El algoritmo detecta la coincidencia y retorna `True` correctamente.



---

### 3. Demostración de Terminación mediante Función Potencial ($\Phi$)

#### Caso A: Lista Sin Ciclo (Longitud Total $N$)

Definimos la función potencial $\Phi(k)$ como el número de saltos que le restan al puntero `fast` para agotar la lista de longitud $N$:


$$\Phi(k) = \max(0, N - 2k)$$

1. **No negatividad:** $\Phi(k) \ge 0, \forall k \ge 0$.
2. **Decrecimiento estricto:** En cada iteración donde el ciclo continúa, `fast` avanza $2$ posiciones, por lo que:

$$\Phi(k + 1) = \Phi(k) - 2 < \Phi(k)$$



Puesto que $\Phi(k) \in \mathbb{Z}_{\ge 0}$ y decrece estrictamente en una magnitud de $2$, el algoritmo garantiza su terminación en a lo sumo $\lceil N/2 \rceil$ iteraciones.

#### Caso B: Lista Con Ciclo ($\mu$ nodos de cola, $\lambda$ nodos de ciclo)

Definimos el potencial estructurado en dos fases consecutivas:

1. **Fase 1: Entrada de `slow` al ciclo ($k < \mu$):**

$$\Phi_1(k) = \mu - k$$



Representa la cantidad de pasos que restan para que `slow` alcance la entrada del ciclo. En cada iteración, $\Phi_1(k+1) = \Phi_1(k) - 1$, decreciendo estrictamente hasta $0$ en $k = \mu$.
2. **Fase 2: Persecución dentro del ciclo ($k \ge \mu$):**

$$\Phi_2(k) = (\lambda - (k \pmod \lambda)) \pmod \lambda$$



Representa el número de nodos de ventaja que `slow` tiene sobre `fast` en el sentido de avance del ciclo. En cada iteración, `slow` se aleja $1$ posición pero `fast` se aproxima $2$, reduciendo la distancia que los separa a una tasa neta de $1$ posición por paso:

$$\Phi_2(k + 1) = (\Phi_2(k) - 1) \pmod \lambda$$



Ambas funciones potenciales son no negativas, discretas y estrictamente decrecientes en cada iteración. La secuencia no puede extenderse infinitamente, garantizando la terminación en la primera colisión $\Phi_2 = 0$.

---

### 4. Análisis de Complejidad

* **Complejidad Temporal:** $\mathcal{O}(N)$ en el peor caso, donde $N = \mu + \lambda$ denota el número total de nodos de la lista.
* **Sin ciclo:** Realiza exactamente $\lfloor N/2 \rfloor$ o $\lceil N/2 \rceil$ iteraciones $\implies \mathcal{O}(N)$.
* **Con ciclo:** El puntero `slow` requiere $\mu$ iteraciones para entrar al ciclo. Una vez dentro, la persecución concluye en a lo sumo $\lambda - 1$ iteraciones adicionales. El total de iteraciones está acotado por $\mu + \lambda = N \implies \mathcal{O}(N)$.


* **Complejidad Espacial:** $\mathcal{O}(1)$ en el peor caso. El algoritmo únicamente requiere dos variables de puntero auxiliares (`slow` y `fast`), independientemente de la escala del grafo de memoria.