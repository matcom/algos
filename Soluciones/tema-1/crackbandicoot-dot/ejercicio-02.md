**Resumen:** Invariante: todo índice a la izquierda de `lo` contiene un valor $<x$ y todo índice en `hi` o a su derecha contiene un valor $>x$. Potencial: $\Phi = hi - lo$, que como mínimo se reduce a la mitad en cada iteración, así que hay como máximo $\lfloor \log_2 n \rfloor + 1 = \lceil \log_2(n+1) \rceil$ iteraciones. Cota inferior: cualquier búsqueda basada en comparaciones tiene al menos $n+1$ “huecos” distinguibles de “no encontrado”, así que un árbol de decisión binario necesita profundidad $\ge \lceil \log_2(n+1) \rceil$. Las dos cotas coinciden, así que la búsqueda binaria es óptima.

---

## Problema

**Entrada:** un arreglo $A[0..n-1]$ ordenado en orden no decreciente y una clave $x$.

**Salida:** un índice $i$ con $A[i]=x$, o $-1$ si no existe tal índice.






**Modelo:** 
se accede a $A$ solo mediante comparaciones de tres vías de $x$ con algún $A[i]$ (resultados $<,=,>$). El costo es el número de comparaciones.

## Algoritmo

`compare(a, b)` devuelve $-1$, $0$ o $1$ cuando $a<b$, $a=b$, $a>b$. `floor_div(a, b)` devuelve $\lfloor a/b \rfloor$.

```python
def binary_search(A, n, x):
    lo = 0
    hi = n
    while lo < hi:
        mid = floor_div(lo + hi, 2)
        c = compare(A[mid], x)
        if c == 0:
            return mid
        if c < 0:
            lo = mid + 1
        else:
            hi = mid
    return -1
```

La ventana es el intervalo semiabierto $[lo, hi)$.

## Invariante del bucle

*Esquema: estado, inicialización, mantenimiento, terminación.*

$$I:\quad 0 \le lo \le hi \le n \;\wedge\; \big(\forall j<lo:\ A[j]<x\big) \;\wedge\; \big(\forall j\ge hi:\ A[j]>x\big)$$

En palabras: todo $A$ fuera de la ventana ya se sabe que difiere de $x$, así que cualquier aparición de $x$ está dentro de $[lo, hi)$.

- **Inicialización:** $lo=0$, $hi=n$, así que ambas afirmaciones universales son vacías.
- **Mantenimiento:** supón que $I$ se cumple y $lo<hi$. Entonces $lo \le mid \le hi-1$, así que los límites en $I$ siguen siendo válidos.
  - Si $A[mid]<x$, el bucle hace $lo=mid+1$. Para todo $j\le mid$, el orden no decreciente da $A[j]\le A[mid]<x$, así que la cláusula izquierda se cumple para el nuevo $lo$.
  - Si $A[mid]>x$, el bucle hace $hi=mid$. Para todo $j\ge mid$, $A[j]\ge A[mid]>x$, así que la cláusula derecha se cumple para el nuevo $hi$.
  - Si $A[mid]=x$, la función devuelve un índice correcto.
- **Terminación:** si el bucle sale con $lo\ge hi$, entonces $lo=hi$ por $I$. Las dos cláusulas cubren todos los índices, así que $A[j]\ne x$ para todo $j$ y devolver $-1$ es correcto.

## Potencial (variante) y detención

*Esquema: define $\Phi$, demuestra que es un entero no negativo que disminuye estrictamente.*

Sea $\Phi=hi-lo$. Por $I$ es un entero no negativo, y el bucle se ejecuta solo mientras $\Phi\ge1$. Con $mid=lo+\lfloor \Phi/2\rfloor$:

- Caso $lo\leftarrow mid+1$: $\Phi' = hi-mid-1 = \Phi-\lfloor\Phi/2\rfloor-1 = \lceil \Phi/2\rceil-1 \le \lfloor \Phi/2\rfloor$.
- Caso $hi\leftarrow mid$: $\Phi' = mid-lo=\lfloor\Phi/2\rfloor$.

En ambos casos $\Phi'\le\lfloor\Phi/2\rfloor<\Phi$ para $\Phi\ge1$. Un entero no negativo no puede disminuir indefinidamente, así que el algoritmo **termina**. Junto con el invariante, la salida es correcta.

## Complejidad temporal

Después de $k$ iteraciones, $\Phi_k\le\lfloor n/2^k\rfloor$. Una iteración ocurre solo mientras $\Phi\ge1$, lo que requiere $2^k\le n$. Por lo tanto, el número de iteraciones, y de comparaciones, es como máximo

$$\lfloor\log_2 n\rfloor+1=\lceil\log_2(n+1)\rceil=O(\log n).$$

## ¿Se puede hacer mejor? No.


**Afirmación:** todo algoritmo de búsqueda basado en comparaciones necesita al menos $\lceil\log_2(n+1)\rceil$ comparaciones en el peor caso. Esta es la cota de información: hay $n+1$ resultados que el algoritmo debe poder distinguir.

**Demostración.** Toma valores distintos $A[0]<\dots<A[n-1]$. La clave $x$ cae en uno de los $n+1$ **huecos** $g_0,\dots,g_n$, donde $g_i$ queda estrictamente entre $A[i-1]$ y $A[i]$, o es igual a $A[i]$ para los $n$ casos de “encontrado”.

Modela el algoritmo como un árbol de decisión. Cada nodo interno consulta algún $A[i]$ y tiene tres hijos, para los resultados $<,=,>$. El hijo $=$ es una hoja que devuelve $i$. Elimina estas hojas $=$. Lo que queda es un árbol binario cuyas hojas todas devuelven $-1$, y su profundidad es como máximo el número de comparaciones en el peor caso $d$.

**Afirmación:** ningún par de huecos $g_a<g_b$ termina en la misma hoja. Supón que sí. Algún $A[i]$ satisface $g_a<A[i]<g_b$.

1. Si el camino consultó $A[i]$, las respuestas serían distintas para $g_a$ y $g_b$ ($A[i]>x$ frente a $A[i]<x$), así que los caminos se separarían. Esto es una contradicción.
2. Si el camino nunca consultó $A[i]$, entonces la clave $x=A[i]$ da exactamente las mismas respuestas a lo largo del camino, porque toda otra consulta se comporta como lo hace para $g_a$. El algoritmo devolvería entonces $-1$ aunque $A[i]=x$, lo cual es incorrecto.

Por tanto, hay al menos $n+1$ hojas distintas en un árbol binario de profundidad a lo sumo $d$, así que

$$n+1\le 2^d\;\Longrightarrow\; d\ge\lceil\log_2(n+1)\rceil. \qquad\blacksquare$$

La búsqueda binaria usa como máximo $\lceil\log_2(n+1)\rceil$ comparaciones, lo que alcanza esta cota exactamente. Es óptima en el peor caso, no solo salvo constantes: $\Theta(\log n)$, con la constante exacta coincidiendo.