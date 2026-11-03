# Ejercicio 8 — Elemento mayoritario con umbral n/3

**Diseño y Análisis de Algoritmos · Tema 1 · Curso 2026**

> El elemento que aparece más de n/3 veces. Generaliza Boyer-Moore con dos candidatos, enuncia el invariante reforzado y demuéstralo. Después escribe la versión que devuelve los candidatos con contador positivo sin verificarlos, y busca un generador de pruebas que no la atrape. Cuidado: el análogo del generador binario de la conferencia 3 sí la atrapa. (C3)

---

## 1. Descripción del algoritmo

El algoritmo clásico de Boyer-Moore para encontrar un elemento que aparece más de $n/2$ veces cancela parejas de elementos distintos. Para encontrar elementos que aparecen más de $n/3$ veces, no podemos cancelar parejas (podríamos cancelar dos mayoritarios mutuamente). En su lugar, **cancelamos tripletas de elementos mutuamente distintos**.

Mantenemos dos candidatos (`cand1`, `cand2`) y dos contadores (`count1`, `count2`), inicializados en 0. Para cada elemento `x` del arreglo:
1. Si `x == cand1`, incrementamos `count1`.
2. Si `x == cand2`, incrementamos `count2`.
3. Si `count1 == 0`, asignamos `cand1 = x` y `count1 = 1`.
4. Si `count2 == 0`, asignamos `cand2 = x` y `count2 = 1`.
5. Si `x` es distinto a ambos y ambos contadores son $>0$, decrementamos **ambos** contadores (esto equivale a tachar una tripleta de 3 elementos distintos).

## 2. Correctitud total

La correctitud total se compone de correctitud parcial (demostrada con el invariante) más terminación.

### 2.1 Correctitud parcial (Invariante reforzado)

**Invariante:** *Después de procesar un prefijo de tamaño $m$, si eliminamos los `count1` elementos iguales a `cand1` y los `count2` elementos iguales a `cand2`, los elementos restantes pueden agruparse en exactamente $\lfloor (m - count1 - count2) / 3 \rfloor$ tripletas de elementos mutuamente distintos.*

- **Inicialización:** Antes de procesar, $m=0$, $count1=count2=0$. Hay 0 tripletas. Se cumple.
- **Mantenimiento:** Supongamos que se cumple para el prefijo de tamaño $m$.
  - Si se incrementa un contador (casos 1 y 2): $m$ aumenta en 1 y el contador también, por lo que el término $(m - count1 - count2)$ no cambia. La cantidad de tripletas se mantiene.
  - Si se asigna un candidato (casos 3 y 4): $m$ aumenta en 1 y el contador también. Igual que antes, la cantidad de tripletas no cambia.
  - Si se decrementan ambos contadores (caso 5): $m$ aumenta en 1, pero $count1$ y $count2$ disminuyen en 1. El término $(m - count1 - count2)$ aumenta en $1 - (-2) = 3$. Es decir, se forma exactamente una nueva tripleta (el nuevo `x` y los dos elementos que representaban los contadores decrementados). El invariante se preserva.
- **Conclusión (parcial):** Al final del arreglo (tamaño $n$), la cantidad de tripletas formadas es a lo sumo $n/3$. Si un elemento $y$ **no** es `cand1` ni `cand2`, todas sus apariciones fueron tachadas en tripletas. Como en cada tripleta hay a lo sumo un $y$, su frecuencia total es $\le n/3$. Por lo tanto, cualquier elemento con frecuencia $> n/3$ **debe** ser `cand1` o `cand2`.

### 2.2 Terminación

El algoritmo recorre el arreglo una sola vez, mediante un ciclo `for` que se ejecuta exactamente $n$ veces. En cada iteración realiza un número constante de operaciones elementales (comparaciones, asignaciones e incrementos/decrementos). Por lo tanto, el algoritmo siempre termina.

### 2.3 Correctitud total

De 2.1 (correctitud parcial) y 2.2 (terminación) se sigue la correctitud total: el algoritmo siempre termina y, al terminar, devuelve los únicos candidatos posibles a aparecer más de $n/3$ veces.

## 3. La versión sin verificar y el generador de pruebas

Si al final del algoritmo devolvemos los candidatos cuyo contador quedó positivo **sin verificar** su frecuencia real, el algoritmo puede dar falsos positivos. 

### ¿Por qué el generador binario de la conferencia 3 sí atrapa el error?
Si usamos un generador que solo emplea 2 símbolos (ej. `A` y `B`), como el arreglo tiene $n$ elementos, uno de los dos debe aparecer al menos $n/2$ veces (que es $> n/3$). Si ambos aparecen exactamente $n/2$ veces, los contadores de ambos quedarán positivos. La versión sin verificar devolverá `[A, B]`, pero la respuesta real debería ser `[]` (porque ninguno es estrictamente $> n/3$). El test detecta el error.

### Un generador de pruebas que NO atrapa el error
Para que el test no atrape el error, debemos generar casos donde los contadores de los candidatos falsos terminen en 0, de modo que la versión sin verificar devuelva exactamente lo mismo que la versión correcta.

**La estrategia:** Generar arreglos usando **exactamente 3 símbolos** en bloques perfectos, por ejemplo: `[A, B, C, A, B, C, ...]`.
- En estos casos, el algoritmo tachará perfectamente todas las tripletas (cada `A`, `B` y `C` se cancela mutuamente).
- Al final, `count1 = 0` y `count2 = 0`.
- La versión sin verificar devolverá `[]`. La versión correcta también devolverá `[]`.
- El test pasará con éxito, y el bug (la falta de verificación) pasará desapercibido.

## 4. Extra: Generalización para cualquier umbral n/k

La lógica del algoritmo se puede generalizar para encontrar todos los elementos que aparecen estrictamente más de $n/k$ veces, para cualquier $k \ge 2$.

**Observación matemática:** Como máximo puede haber $k-1$ elementos distintos que superen el umbral $n/k$ (pues si hubiera $k$ elementos, la suma de sus frecuencias superaría $n$). Por lo tanto, el algoritmo mantiene **$k-1$ candidatos** y **$k-1$ contadores**.

**Mecánica:** Para cada elemento $x$, si $x$ es un candidato, incrementamos su contador. Si hay un contador en 0, reemplazamos ese candidato por $x$. Si $x$ es distinto a todos y todos los contadores son positivos, decrementamos **todos** los contadores en 1 (tachando $k$ elementos mutuamente distintos).

**Invariante generalizado:** *Después de procesar un prefijo, si eliminamos los elementos representados por los contadores, el resto de los elementos puede agruparse en $\lfloor (m - \sum \text{count}_i) / k \rfloor$ grupos de $k$ elementos mutuamente distintos.*

**Correctitud y Terminación:** La terminación sigue siendo $O(n)$ iteraciones. La correctitud parcial se mantiene porque cualquier elemento que no sea candidato solo pudo aparecer en los grupos tachados, limitando su frecuencia a $\lfloor n/k \rfloor$. Por lo tanto, cualquier elemento con frecuencia $> n/k$ debe estar entre los $k-1$ candidatos.

**Costo computacional:** Tiempo $O(n \cdot k)$ en el peor caso (o $O(n)$ con tabla hash) y espacio $O(k)$.