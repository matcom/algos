# Ejercicio 2 :Da el invariante y el potencial de la búsqueda binaria, y la cota de información que la hace óptima

## Especificación Formal del Problema y Algoritmo

La Búsqueda Binaria para poder ser ejecutada tiene que cumplir con la **Precondición** que el arreglo $A[0 \dots n-1]$ está ordenado de forma estrictamente creciente (o no decreciente), es decir, $\forall i \in [0, n-2], A[i] \le A[i+1]$. Se recibe un elemento buscado $x$.Luego cumple con la **Postcondición** de forma que Si $x \in A$, devuelve un índice $m \in [0, n-1]$ tal que $A[m] = x$ y Si $x \notin A$, devuelve $-1$ (o indica de forma inequívoca el hueco donde $x$ debería insertarse).

A continuación se muestra la implementación estándar correcta en Python.

```python
def busqueda_binaria(A, x):
    lo = 0
    hi = len(A)
    while lo < hi:
        mid = (lo + hi) // 2
        if A[mid] == x:
            return mid
        elif A[mid] < x:
            lo = mid + 1 
        else:
            hi = mid   
    return -1

```

---

## Invariante de Ciclo y Correctitud Parcial

El **invariante de ciclo** es la propiedad central para demostrar la **correctitud parcial** (es decir, si el ciclo termina, la salida es correcta).

> **Invariante $I$:** En cada iteración, antes de evaluar la condición del bucle `lo < hi`:
>
> 1. $0 \le \text{lo} \le \text{hi} \le n$.
> 2. Si el elemento $x$ está en el arreglo $A$, entonces se encuentra en el rango de índices $[\text{lo}, \text{hi}-1]$, es decir, $x \in A[\text{lo} \dots \text{hi}-1]$.

### Demostración Formal

Antes de entrar al bucle por primera vez se cumple que $\text{lo} = 0$, $\text{hi} = n$. El rango $[\text{lo}, \text{hi}-1]$ es $[0, n-1]$, que abarca **todo el arreglo**. Por tanto, si $x \in A$, inequívocamente está en $A[0 \dots n-1]$. $I$ se cumple.

Supongamos que $I$ es verdadero al inicio de una iteración donde $\text{lo} < \text{hi}$.
Calculamos $\text{mid} = \lfloor(\text{lo} + \text{hi})/2\rfloor$. Como $\text{lo} < \text{hi}$, se garantiza que $\text{lo} \le \text{mid} < \text{hi}$.

- **Caso 1:** $A[\text{mid}] == x$.
    El algoritmo retorna $\text{mid}$ inmediatamente. Puesto que $A[\text{mid}] = x$, se cumple la postcondición de forma exacta.
- **Caso 2:** $A[\text{mid}] < x$.
    Dado que el arreglo está ordenado, para todo $i \le \text{mid}$ se cumple $A[i] \le A[\text{mid}] < x$. Por lo tanto, $x$ **no puede estar** en $A[0 \dots \text{mid}]$.
    Si $x \in A$, debe estar en $A[\text{mid}+1 \dots \text{hi}-1]$.
    Al hacer $\text{lo} = \text{mid} + 1$, el nuevo rango válido pasa a ser $[\text{lo}_{\text{nuevo}}, \text{hi}-1]$, preservando el invariante.
- **Caso 3:** $A[\text{mid}] > x$.
    Dado el orden, para todo $i \ge \text{mid}$ se cumple $A[i] \ge A[\text{mid}] > x$. Por tanto, $x$ **no puede estar** en $A[\text{mid} \dots n-1]$.
    Si $x \in A$, debe estar en $A[\text{lo} \dots \text{mid}-1]$.
    Al hacer $\text{hi} = \text{mid}$, el nuevo límite superior excluyente es $\text{mid}$, preservando el rango $[\text{lo}, \text{mid}-1]$. $I$ se mantiene.

Si el bucle termina, se debe a que $\text{lo} \ge \text{hi}$.
Por la parte (1) del invariante ($\text{lo} \le \text{hi}$), al terminar se cumple exactamente $\text{lo} = \text{hi}$.
El rango de búsqueda $[\text{lo}, \text{hi}-1] = [\text{lo}, \text{lo}-1]$ pasa a ser un intervalo **vacío**.
Por la parte (2) del invariante, si $x$ estuviera en $A$, debería pertenecer a un intervalo vacío, lo cual es una contradicción. Por lo tanto, $x \notin A$, y retornar $-1$ es la respuesta correcta según la postcondición. $\blacksquare$

## Demostración de Terminación mediante Función Potencial

Para demostrar que el bucle `while` termina obligatoriamente, definimos la **función potencial** $\Phi$:

$$\Phi(\text{lo}, \text{hi}) = \text{hi} - \text{lo}$$

Este potencial cumple con las Propiedades de  **Cota Inferior** por el invariante, $\text{hi} \ge \text{lo}$, de modo que $\Phi \ge 0$ es un número entero no negativo. También fundamental con el
**Decrecimiento Estricto por Paso.**
   En cada iteración donde $\text{lo} < \text{hi}$, calculamos $\text{mid} = \lfloor(\text{lo} + \text{hi})/2\rfloor$.
   Puesto que $\text{lo} < \text{hi}$, tenemos que $\text{lo} \le \text{mid} < \text{hi}$. Si tomamos la rama $\text{lo} = \text{mid} + 1$:
$\Phi_{\text{nuevo}} = \text{hi} - (\text{mid} + 1) \le \text{hi} - (\text{lo} + 1) = \Phi - 1 < \Phi$
      Si tomamos la rama $\text{hi} = \text{mid}$:
     $\Phi_{\text{nuevo}} = \text{mid} - \text{lo} \le (\text{hi} - 1) - \text{lo} = \Phi - 1 < \Phi$

En todos los caminos del bucle, $\Phi$ **decrece estrictamente en al menos 1 unidad** por cada iteración. Dado que $\Phi \in \mathbb{N}_0$ no puede decrecer indefinidamente, el ciclo debe terminar en un número finito de pasos (a lo sumo $\lceil\log_2(n+1)\rceil$ iteraciones).

## El Modelo de Comparaciones y Árboles de Decisión

En el **modelo de comparaciones**, la única forma en que un algoritmo puede obtener información sobre una entrada $A[0 \dots n-1]$ y un elemento $x$ es realizando preguntas binarias o ternarias de la forma:

$$\text{¿Es } x < A[i] \text{? \quad ó \quad ¿Es } x = A[i] \text{?}$$

Cualquier algoritmo en este modelo equivale a un **árbol de decisión**, donde cada **nodo interno** representa una comparación, cada **rama** representa el resultado de dicha comparación, cada **hoja** representa una salida o respuesta del algoritmo.
La **altura del árbol ($h$)** equivale al número de comparaciones ejecutadas en el **peor caso**.

## Argumento de Información

Dado un arreglo ordenado de $n$ elementos distinctos $A[0] < A[1] < \dots < A[n-1]$ y un valor buscado $x$, si $x \notin A$, $x$ debe situarse en uno de los **$n+1$ huecos posibles** definidos entre los elementos:

$$h_0 = (-\infty, A[0]), \quad h_1 = (A[0], A[1]), \quad \dots, \quad h_n = (A[n-1], +\infty)$$

```text
     h0        h1        h2              hn-1        hn
   <-----> A[0] <-----> A[1] <-----> ... A[n-1] <----->
```

> **Lema:** Si $x_1$ y $x_2$ pertenecen a dos huecos distintos ($h_i \neq h_j$), cualquier algoritmo correcto de comparaciones **debe llevarlos a hojas distintas** en el árbol de decisión.

### Demostración (por Contradicción)

Supongamos que $x_1 \in h_i$ y $x_2 \in h_j$ con $i < j$, y que el algoritmo los conduce a la **misma hoja** $L$.
Dado que recorren exactamente el mismo camino hasta $L$, el algoritmo habrá ejecutado exactamente las mismas comparaciones y recibido las mismas respuestas para ambos valores.
Como $i < j$, existe al menos un elemento $A[k]$ en el arreglo tal que $x_1 < A[k] < x_2$.
El algoritmo **nunca comparó** $x$ con $A[k]$. (Si lo hubiera hecho, para $x_1$ la respuesta habría sido $x_1 < A[k]$ y para $x_2$ habría sido $x_2 > A[k]$, enviándolos por ramas distintas).
Consideremos ahora el valor $x^* = A[k]$. Como no se realiza la comparación con $A[k]$, $x^*$ recibirá exactamente las mismas respuestas que $x_1$ y $x_2$, finalizando en la misma hoja $L$.
En la hoja $L$, el algoritmo responderá "No se encuentra" (pues es la respuesta para los huecos $x_1$ y $x_2$).
Sin embargo, $x^* = A[k]$ **sí pertenece al arreglo**. El algoritmo responde incorrectamente.
Contradicción. Por lo tanto, cada uno de los $n+1$ huecos debe terminar en una hoja distinta.

## Demostración  de la Cota Mínima

> **Teorema:** Todo algoritmo que busque un elemento $x$ en un arreglo ordenado de $n$ elementos mediante comparaciones requiere, en el peor caso, al menos:
> $$h \ge \lceil \log_2(n+1) \rceil \text{ comparaciones}$$

### Demostración

Por el Lema de los Huecos, el árbol de decisión debe poseer al menos $L = n+1$ hojas correspondientes a las respuestas de no presencia.
Para las consultas sobre huecos donde $x \notin A$, la respuesta a una comparación solo puede ser un resultado binario: $x < A[m]$ o $x > A[m]$. Por ende, la sección del árbol encargada de distinguir huecos es un **árbol binario**.
Por la propiedad geométrica de los árboles binarios (Conferencia 5), un árbol binario de altura $h$ posee a lo sumo $2^h$ hojas:
$$L \le 2^h \implies n + 1 \le 2^h$$
Aplicando logaritmo en base 2 a ambos lados:
   $$h \ge \log_2(n+1)$$
Como el número de comparaciones $h$ debe ser un número entero, tomamos el techo:
   $$h \ge \lceil \log_2(n+1) \rceil \quad \$$

## Demostración de Optimalidad de la Búsqueda Binaria

El algoritmo de búsqueda binaria divide en cada paso el rango de búsqueda aproximadamente a la mitad.
En el peor caso (cuando $x \notin A$), la cantidad de comparaciones ejecutadas por Búsqueda Binaria es exactamente:

$$T_{\text{BB}}(n) = \lceil \log_2(n+1) \rceil$$

Como el costo en el peor caso de la Búsqueda Binaria **coincide exactamente con la cota inferior demostrada**, concluimos que la Búsqueda Binaria es un **algoritmo estrictamente óptimo** en el modelo de comparaciones.

## Árbol de Decisión para $n=7$ ($8$ Huecos)

Para $n = 7$ elementos ($A = [a_0, a_1, a_2, a_3, a_4, a_5, a_6]$), hay $8$ huecos ($h_0 \dots h_7$).

$$\text{Cota Inferior} = \lceil \log_2(7+1) \rceil = \lceil \log_2(8) \rceil = 3 \text{ comparaciones}$$

```text
                                [ x < a3 ]
                               /          \
                       (Sí)   /            \ (No)
                             /              \
                     [ x < a1 ]            [ x < a5 ]
                     /        \            /        \
                   (Sí)      (No)        (Sí)      (No)
                   /            \        /            \
             [ x < a0 ]    [ x < a2 ]  [ x < a4 ]    [ x < a6 ]
             /     \       /     \     /     \       /     \
           (Sí)   (No)   (Sí)   (No) (Sí)   (No)   (Sí)   (No)
           /         \   /         \ /         \   /         \
          h0         h1 h2         h3 h4       h5 h6         h7
```

*Observación:* La altura del árbol es exactamente $3$, lo que satisface y alcanza la cota mínima de información.

El siguiente código evalúa el número de comparaciones de la búsqueda binaria frente a la cota teórica dada por la teoría de información para distintos tamaños $n$.

```python
import math
import pandas as pd

def contar_comparaciones_busqueda_binaria(n, hueco_objetivo):
    """
    Simula la búsqueda binaria sobre n elementos para caer en un hueco específico.
    A es conceptualmente [0, 1, ..., n-1]
    Hueco k representa buscar un valor x tal que k-1 < x < k
    """
    lo = 0
    hi = n
    comparaciones = 0
    
    # Creamos un valor float ficticio para caer en el hueco deseado
    x = hueco_objetivo - 0.5 
    
    while lo < hi:
        mid = (lo + hi) // 2
        comparaciones += 1
        if mid == x: # Imposible por ser float vs int
            return comparaciones
        elif x < mid:
            hi = mid
        else:
            lo = mid + 1
            
    return comparaciones

def generar_tabla_optimalidad():
    resultados = []
    tamanios = [1, 3, 7, 15, 31, 63, 100, 1000]
    
    for n in tamanios:
        cota_teorica = math.ceil(math.log2(n + 1))
        
        # Probar todos los huecos posibles para hallar el peor caso
        peor_caso_real = 0
        for hueco in range(n + 1):
            comps = contar_comparaciones_busqueda_binaria(n, hueco)
            peor_caso_real = max(peor_caso_real, comps)
            
        resultados.append({
            "n (Elementos)": n,
            "Huecos (n+1)": n + 1,
            "Cota Teórica ceil(log2(n+1))": cota_teorica,
            "Peor Caso Búsqueda Binaria": peor_caso_real,
            "¿Es Óptimo?": "SÍ (Alcanza Cota)" if peor_caso_real == cota_teorica else "NO"
        })
        
    df = pd.DataFrame(resultados)
    return df

print("="*80)
print("TABLA DE COMPARACIÓN: COTA TEÓRICA DE INFORMACIÓN VS BÚSQUEDA BINARIA")
print("="*80)
df_resultado = generar_tabla_optimalidad()
print(df_resultado.to_string(index=False))
```

**Salida**:
| n (Elementos) | Huecos (n+1) | Cota Teórica ceil(log2(n+1)) | Peor Caso Búsqueda Binaria | ¿Es óptimo? |
| :---: | :---: | :---: | :---: | :---: |
| 1 | 2 | 1 | 1 | Sí (Alcanza Cota) |
| 3 | 4 | 2 | 2 | Sí (Alcanza Cota) |
| 7 | 8 | 3 | 3 | Sí (Alcanza Cota) |
| 15 | 16 | 4 | 4 | Sí (Alcanza Cota) |
| 31 | 32 | 5 | 5 | Sí (Alcanza Cota) |
| 63 | 64 | 6 | 6 | Sí (Alcanza Cota) |
| 100 | 101 | 7 | 7 | Sí (Alcanza Cota) |
| 1000 | 1001 | 10 | 10 | Sí (Alcanza Cota) |
