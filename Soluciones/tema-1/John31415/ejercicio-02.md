### Cota de Información (Óptimo Teórico)

La **cota de información** (o cota inferior por árbol de decisión) determina el número mínimo de comparaciones que cualquier algoritmo basado en comparaciones debe realizar en el peor de los casos para resolver un problema.

Cuando buscamos un elemento en un arreglo de tamaño $N$, hay **$N + 1$ resultados posibles**:

* El elemento está en la posición $0, 1, 2, \dots, N-1$ ( $N$ posibilidades).
* El elemento no está en el arreglo ($1$ posibilidad).

Cada comparación binaria que hace el algoritmo (por ejemplo, "¿es $A[\text{mid}] < x$?") responde con **Sí** o **No**. Esto se puede representar como un **árbol de decisión binario**, donde cada nodo interno es una comparación y cada hoja representa uno de los resultados posibles.

```text
                     ¿A[mid] == x?
                     /           \
                 (Sí)             (No)
               Retorna        ¿A[mid] < x?
               posición       /          \
                          (Sí)            (No)
                       Buscar          Buscar
                       derecha        izquierda

```

Para poder distinguir entre todos los $N + 1$ resultados posibles, el árbol binario debe tener al menos $N + 1$ hojas. Si la altura del árbol es $h$ (que representa la cantidad de comparaciones en el peor de los casos):

$$2^h \ge N + 1 \implies h \ge \lceil \log_2(N + 1) \rceil$$

Por lo tanto, la cota de información para la búsqueda es $\Omega(\log N)$. Ningún algoritmo basado en comparaciones puede responder la búsqueda en menos de $\lceil \log_2(N + 1) \rceil$ comparaciones en el peor de los casos.

Dado que la **búsqueda binaria** descarta exactamente la mitad de las opciones en cada paso, alcanza esta cota en $O(\log N)$ comparaciones, lo que demuestra formalmente que es un **algoritmo óptimo**.

---

### Algoritmo de Búsqueda Binaria (Referencia)

Dado un arreglo ordenado $A[0 \dots N-1]$ y un valor objetivo $x$:

```python
low = 0
high = N - 1

while low <= high:
    mid = (low + high) // 2
    if A[mid] == x:
        return mid          # Éxito: encontrado
    elif A[mid] < x:
        low = mid + 1       # Descartar mitad izquierda
    else:
        high = mid - 1      # Descartar mitad derecha

return -1                   # Fracaso: no existe

```

---

### 1. Invariante del Ciclo (Correctitud Parcial)

#### Declaración del Invariante ($I$)

> **$I$:** *"Si el elemento $x$ existe en el arreglo $A$, entonces su índice debe estar dentro del rango $[\text{low}, \text{high}]$."*
> Formalmente: $x \in A[0 \dots N-1] \implies x \in A[\text{low} \dots \text{high}]$.

---

#### Demostración formal en 3 pasos

#### A. Inicialización

Antes de entrar a la primera iteración del ciclo:

* $\text{low} = 0$ y $\text{high} = N - 1$.
* El subarreglo $A[\text{low} \dots \text{high}]$ coincide exactamente con todo el arreglo $A[0 \dots N-1]$.
* Por lo tanto, si $x \in A[0 \dots N-1]$, es trivialmente cierto que $x \in A[\text{low} \dots \text{high}]$. El invariante se cumple al inicio.

#### B. Mantenimiento

Asumimos que el invariante $I$ es verdadero justo antes de una vuelta del ciclo. Durante la iteración se evalúa $A[\text{mid}]$ donde $\text{mid} = \lfloor (\text{low} + \text{high}) / 2 \rfloor$:

* **Caso 1 ($A[\text{mid}] == x$):** El algoritmo retorna $\text{mid}$ inmediatamente. El resultado es correcto.
* **Caso 2 ($A[\text{mid}] < x$):** Como el arreglo $A$ está ordenado de forma ascendente, todos los elementos desde $A[\text{low}]$ hasta $A[\text{mid}]$ son estrictamente menores que $x$. Por tanto, $x$ **no puede estar** en el rango $[\text{low}, \text{mid}]$.
Si $x$ está en el arreglo, debe estar en $[\text{mid} + 1, \text{high}]$. Al actualizar $\text{low} = \text{mid} + 1$, el nuevo rango $[\text{low}_{\text{nuevo}}, \text{high}]$ preserva la verdad de que si $x \in A$, entonces $x \in A[\text{low}_{\text{nuevo}} \dots \text{high}]$.
* **Caso 3 ($A[\text{mid}] > x$):** Análogamente, todos los elementos desde $A[\text{mid}]$ hasta $A[\text{high}]$ son estrictamente mayores que $x$. $x$ **no puede estar** en el rango $[\text{mid}, \text{high}]$.
Si $x$ está en el arreglo, debe estar en $[\text{low}, \text{mid} - 1]$. Al hacer $\text{high} = \text{mid} - 1$, el nuevo rango mantiene el invariante.

En todos los caminos donde el ciclo continúa, el invariante se sigue cumpliendo para la siguiente vuelta.

#### C. Conclusión

El ciclo termina cuando la condición de entrada deja de cumplirse, es decir, cuando $\text{low} > \text{high}$.

* Esto significa que el rango $[\text{low}, \text{high}]$ se ha convertido en un subarreglo **vacío**.
* Por el invariante (que sigue siendo verdadero): *"Si $x \in A \implies x \in \text{arreglo vacío}$"*.
* Como un arreglo vacío no contiene ningún elemento, la única posibilidad lógica es que **$x \notin A$**.

Por lo tanto, retornar $-1$ al finalizar el ciclo es una respuesta perfectamente correcta.

---

### Ejemplo Traza del Invariante

Queremos buscar $x = 7$ en el arreglo $A = [2, 4, 5, 7, 9, 12, 15]$ ($N = 7$).

| Paso | Condition | `low` | `high` | Rango Activo | `mid` | `A[mid]` | Evaluación | Estado del Invariante ($I$) |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| **Inicio** | Pre-ciclo | `0` | `6` | $[2, 4, 5, 7, 9, 12, 15]$ | - | - | Inicialización | $7 \in A[0 \dots 6]$ $\rightarrow$ **Verdadero** |
| **Iter 1** | `0 <= 6` | `0` | `6` | $[2, 4, 5, 7, 9, 12, 15]$ | `3` | `7` | $7 == 7$ | **Encontrado en index 3.** Retorna `3`. |

Si buscamos un elemento que **no existe**, por ejemplo $x = 6$:

| Paso | Condition | `low` | `high` | Rango Activo | `mid` | `A[mid]` | Evaluación | Estado del Invariante ($I$) |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| **Inicio** | Pre-ciclo | `0` | `6` | $[2, 4, 5, 7, 9, 12, 15]$ | - | - | Inicialización | $6 \in A \implies 6 \in A[0 \dots 6]$ (**Verdadero**) |
| **Iter 1** | `0 <= 6` | `0` | `6` | $[2, 4, 5, 7, 9, 12, 15]$ | `3` | `7` | $7 > 6 \implies \text{high} = 2$ | $6 \in A \implies 6 \in A[0 \dots 2]$ (**Verdadero**) |
| **Iter 2** | `0 <= 2` | `0` | `2` | $[2, 4, 5]$ | `1` | `4` | $4 < 6 \implies \text{low} = 2$ | $6 \in A \implies 6 \in A[2 \dots 2]$ (**Verdadero**) |
| **Iter 3** | `2 <= 2` | `2` | `2` | $[5]$ | `2` | `5` | $5 < 6 \implies \text{low} = 3$ | $6 \in A \implies 6 \in A[3 \dots 2]$ (**Verdadero**) |
| **Fin** | `3 <= 2` **Falso** | `3` | `2` | $\emptyset$ (Vacío) | - | - | Ciclo termina | $A[3 \dots 2]$ está vacío $\implies 6 \notin A$. Retorna `-1`. |

---

### 2. Función Potencial (Demostración de Terminación)

La **función potencial** $\Phi$ mide la cantidad de trabajo restante o el espacio de búsqueda que le queda al algoritmo.

#### Definición de $\Phi$

$$\Phi(\text{low}, \text{high}) = \max(0, \text{high} - \text{low} + 1)$$

---

#### Demostración de Terminación

1. **Es un entero no negativo ($\Phi \ge 0$):**
Por la función $\max(0, \dots)$, $\Phi$ nunca puede ser menor que 0. Además, dado que $\text{low}$ y $\text{high}$ son números enteros, $\Phi$ siempre toma valores enteros: $\Phi \in \mathbb{Z}_{\ge 0}$.
2. **Decrece estrictamente en cada iteración del ciclo:**
En cualquier vuelta donde el ciclo continúe ($\text{low} \le \text{high}$):

$$\text{mid} = \left\lfloor \frac{\text{low} + \text{high}}{2} \right\rfloor$$



De esta definición de piso entero se desprenden dos desigualdades clave: $\text{low} \le \text{mid} \le \text{high}$.
* Si se toma la rama $\text{low}_{\text{nuevo}} = \text{mid} + 1$:

$$\text{high} - \text{low}_{\text{nuevo}} + 1 = \text{high} - (\text{mid} + 1) + 1 = \text{high} - \text{mid}$$



Dado que $\text{mid} \ge \text{low}$, tenemos que $\text{high} - \text{mid} < \text{high} - \text{low} + 1$.
* Si se toma la rama $\text{high}_{\text{nuevo}} = \text{mid} - 1$:

$$\text{high}_{\text{nuevo}} - \text{low} + 1 = (\text{mid} - 1) - \text{low} + 1 = \text{mid} - \text{low}$$



Dado que $\text{mid} \le \text{high}$, tenemos que $\text{mid} - \text{low} < \text{high} - \text{low} + 1$.



En ambos casos, el tamaño del espacio de búsqueda decrece estrictamente:

$$\Phi_{\text{siguiente}} \le \left\lfloor \frac{\Phi_{\text{actual}}}{2} \right\rfloor < \Phi_{\text{actual}}$$

#### Conclusión de Terminación

Como $\Phi$ es una secuencia de números enteros no negativos que decrece estrictamente en cada vuelta del ciclo ($\Phi_0 > \Phi_1 > \Phi_2 > \dots \ge 0$), **es imposible que el ciclo se ejecute infinitamente**.

El número total de iteraciones está acotado por el valor inicial del potencial:

$$\Phi_0 = N - 0 + 1 = N$$

Dado que el valor se reduce al menos a la mitad en cada paso, el algoritmo se detiene obligatoriamente en como máximo $\lceil \log_2(N + 1) \rceil$ iteraciones.