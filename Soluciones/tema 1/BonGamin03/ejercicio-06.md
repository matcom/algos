# Ejercicio 6

## 1. Diseño del Algoritmo $O(n)$

Iniciamos la búsqueda en la esquina superior derecha $(i = 0, j = n - 1)$. En cada paso, comparamos el elemento actual $M[i][j]$ con $x$ para descartar una fila o una columna completa.

```python
def buscar_matriz(M, n, x):
    i = 0
    j = n - 1
    
    while i < n and j >= 0:
        if M[i][j] == x:
            return True
        elif M[i][j] > x:
            j -= 1  # x no está en la columna j; la descartamos.
        else:
            i += 1  # x no está en la fila i; la descartamos.
            
    return False
```

---

## Demostración de Correctitud 

### **Invariante:**
Al inicio de cada iteración del bucle `while`, si el elemento $x$ se encuentra en la matriz $M$, entonces $x$ debe pertenecer al subbloque delimitado por las filas $i \dots n-1$ y las columnas $0 \dots j$:
$$x \in M \implies x \in \{ M[r][c] \mid i \le r \le n-1, \, 0 \le c \le j \}$$

### **Demostración por Inducción:**

* **Inicialización:** $i = 0$ y $j = n - 1$. El subbloque cubre toda la matriz $M$. El invariante se cumple de forma trivial.
* **Mantenimiento:** Asumiendo que el invariante se cumple al inicio de una iteración:
  * Si $M[i][j] == x$, se retorna `True` (éxito).
  * Si $M[i][j] > x$, como la columna $j$ está ordenada de forma creciente ($M[r][j] \ge M[i][j] > x$ para $r \ge i$), $x$ no puede estar en la columna $j$. Al hacer $j \leftarrow j - 1$, descartamos la columna manteniendo el invariante.
  * Si $M[i][j] < x$, como la fila $i$ está ordenada de forma creciente ($M[i][c] \le M[i][j] < x$ para $c \le j$), $x$ no puede estar en la fila $i$. Al hacer $i \leftarrow i + 1$, descartamos la fila manteniendo el invariante.
* **Terminación:** El bucle termina si $i = n$ o $j = -1$. En este punto, el subbloque candidato queda vacío. Por el invariante, si $x$ estuviera en la matriz debería estar en este subbloque; como está vacío, concluimos que $x \notin M$ y retorna `False`.

### **Complejidad:**
En cada iteración, la variable $S = (n - 1 - j) + i$ (que representa la suma de desplazamientos a la izquierda y hacia abajo) se incrementa exactamente en $1$. Dado que $0 \le i \le n$ y $-1 \le j < n$, el valor máximo que alcanza $S$ antes de salir del bucle es $2n - 1$. Por lo tanto, el número total de comparaciones está acotado por $2n - 1 \in O(n)$.

---

## Demostración de Cota Inferior $\Omega(n)$ mediante Adversario

Queremos demostrar que ningún algoritmo determinista basado en comparaciones puede decidir la presencia de $x$ en $o(n)$ comparaciones en el peor caso.

### **Estrategia del Adversario:**
Sea la diagonal secundaria dada por $i + j = n - 1$. 

El adversario construye una matriz $M$ de la siguiente manera:
1. En la diagonal secundaria coloca números pares estrictamente crecientes:
   $$M[i][n - 1 - i] = 2i \quad \text{para } i = 0, 1, \dots, n - 1$$
2. En las posiciones por encima de la diagonal ($i + j < n - 1$), asigna $-\infty$.
3. En las posiciones por debajo de la diagonal ($i + j > n - 1$), asigna $+\infty$.

El algoritmo busca un valor impar $x = 2k + 1$ (donde $0 \le k < n - 1$).

### **Respuesta a las Consultas:**
* Si el algoritmo consulta celdas fuera de la diagonal secundaria, el adversario responde $-\infty$ o $+\infty$. Esto no aporta información relevante sobre las posiciones de la diagonal secundaria.
* Si el algoritmo consulta una celda $(i, n - 1 - i)$ de la diagonal secundaria, el adversario revela su valor par $2i$.

### **Conclusión:**
Los $n$ elementos de la diagonal secundaria son mutuamente independientes según las reglas de ordenamiento de la matriz (reemplazar un elemento par $2i$ por $2i+1$ mantiene ordenadas todas las filas y columnas). 

Si el algoritmo realiza menos de $n$ comparaciones, dejará al menos una celda de la diagonal secundaria sin consultar. El adversario puede decidir que $x$ estaba en esa celda no consultada (si el algoritmo devuelve `False`) o que no estaba (si el algoritmo devuelve `True`), haciendo fallar al algoritmo. 

Por tanto, se requieren al menos $n$ comparaciones en el peor caso, lo que demuestra que la complejidad es $\Omega(n)$ y es imposible resolverlo en $o(n)$.