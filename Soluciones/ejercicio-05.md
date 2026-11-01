# Ejercicio 5: Detección de ciclos (Algoritmo de Floyd)

**Enunciado:** Detección de ciclos en una lista enlazada con dos punteros que avanzan a velocidades 1 y 2 (algoritmo de Floyd). Demuestra que se encuentran si y solo si hay un ciclo, con un invariante, y que termina, con un potencial. Da el costo. (C3)

**Modelo:** Modelo RAM. Una lista enlazada simple. Las operaciones básicas (leer `.next`) cuestan \(O(1)\).

---

## 1. El algoritmo (punteros lento y rápido)

El algoritmo utiliza dos punteros que recorren la lista simultáneamente:

- El puntero `lento` avanza un nodo por iteración.
- El puntero `rapido` avanza dos nodos por iteración.

```python
def tiene_ciclo(head):
    lento = head
    rapido = head

    while rapido is not None and rapido.next is not None:
        lento = lento.next
        rapido = rapido.next.next

        if lento is rapido:
            return True  # Hay un ciclo

    return False  # No hay ciclo
```

La comparación `is` permite comprobar que ambos punteros hacen referencia al mismo nodo.

---

## 2. Invariante (Correctitud parcial)

Para demostrar la correctitud del algoritmo, debemos probar las dos implicaciones:

1. Si existe un ciclo, los punteros terminan encontrándose.
2. Si los punteros se encuentran, necesariamente existe un ciclo.

**Invariante:** Después de \(i\) iteraciones completas, siempre que los punteros estén definidos, se cumple que:

- El puntero `lento` ha avanzado \(i\) enlaces desde la cabeza.
- El puntero `rapido` ha avanzado \(2i\) enlaces desde la cabeza.

Podemos expresarlo utilizando la función \(f(v)=v.next\):

\[
lento=f^i(head)
\]

\[
rapido=f^{2i}(head)
\]

Esta propiedad se cumple inicialmente porque ambos punteros comienzan en `head`, y se conserva porque en cada iteración uno avanza un enlace y el otro avanza dos.

### Demostración: Si los punteros se encuentran, existe un ciclo

Supongamos que después de \(i\) iteraciones los punteros coinciden:

\[
lento=rapido
\]

Por el invariante:

\[
f^i(head)=f^{2i}(head)
\]

Como el algoritmo realiza al menos una iteración antes de comparar los punteros, \(i>0\).

Esto significa que, siguiendo los enlaces desde la cabeza, llegamos al mismo nodo después de recorrer \(i\) enlaces y después de recorrer \(2i\) enlaces.

Por tanto, existe un recorrido que vuelve a un nodo previamente visitado. Esto solo puede suceder si la lista contiene un ciclo.

En consecuencia:

\[
\boxed{lento=rapido\implies\text{existe un ciclo}}
\]

### Demostración: Si existe un ciclo, los punteros se encuentran

Supongamos que la lista contiene un ciclo.

Definimos:

- \(\mu\): cantidad de nodos que hay desde la cabeza hasta la entrada del ciclo.
- \(\lambda\): longitud del ciclo.

Una vez que ambos punteros han entrado en el ciclo, podemos analizar su distancia relativa.

Como `lento` avanza una posición y `rapido` avanza dos, la distancia relativa entre ellos cambia en una posición por iteración.

Sea \(d_i\) la distancia desde `rapido` hasta `lento`, siguiendo los enlaces del ciclo, medida módulo \(\lambda\).

Entonces:

\[
d_{i+1}=(d_i-1)\pmod{\lambda}
\]

Como existen únicamente \(\lambda\) posiciones posibles dentro del ciclo, después de, como máximo, \(\lambda\) iteraciones adicionales, la distancia será cero:

\[
d_i=0
\]

Esto significa que ambos punteros apuntan al mismo nodo:

\[
lento=rapido
\]

Por tanto:

\[
\boxed{\text{Existe un ciclo}\implies lento=rapido}
\]

**Conclusión del invariante:**

Hemos demostrado ambas direcciones:

\[
\boxed{lento=rapido\iff\text{existe un ciclo}}
\]

Por tanto, el algoritmo devuelve `True` exactamente cuando existe un ciclo.

---

## 3. Potencial (Terminación)

Para demostrar que el algoritmo termina, analizamos por separado los dos posibles tipos de lista: sin ciclo y con ciclo.

### Caso 1: Lista sin ciclo

Sea \(n\) la cantidad de nodos de la lista.

Definimos el potencial como:

\[
\boxed{\Phi=\text{cantidad de nodos restantes desde rapido hasta el final}}
\]

Si `rapido` es `None`, definimos \(\Phi=0\).

Inicialmente:

\[
\Phi_0=n
\]

En cada iteración, el puntero `rapido` avanza dos enlaces. Por tanto, el número de nodos que quedan por recorrer disminuye en dos, o llega a cero si alcanza el final.

Así:

\[
\Phi_{\text{nuevo}}=\max(\Phi-2,0)
\]

Por tanto, el potencial disminuye estrictamente en cada iteración.

Como es un entero no negativo, el algoritmo necesariamente termina cuando el puntero `rapido` alcanza el final de la lista y deja de cumplirse la condición del ciclo `while`.

### Caso 2: Lista con ciclo

En este caso, el potencial debe considerar dos fases:

1. El desplazamiento inicial hasta que ambos punteros entren en el ciclo.
2. El encuentro de ambos punteros dentro del ciclo.

Sean:

- \(\mu\): longitud de la parte lineal anterior al ciclo.
- \(\lambda\): longitud del ciclo.
- \(i\): número de iteraciones completas realizadas.

**Primera fase: antes de que el puntero lento entre en el ciclo.**

Mientras \(i<\mu\), definimos:

\[
\boxed{\Phi_i=\lambda+\mu-i}
\]

En cada iteración, el puntero lento avanza un nodo hacia el ciclo, por lo que el potencial disminuye en una unidad.

Cuando \(i=\mu\), ambos punteros ya están dentro del ciclo.

**Segunda fase: ambos punteros están dentro del ciclo.**

A partir de este momento, definimos el potencial como:

\[
\boxed{\Phi_i=d_i}
\]

donde \(d_i\) es la distancia desde `rapido` hasta `lento`, siguiendo los enlaces del ciclo, y tomando su valor entre \(0\) y \(\lambda-1\).

Si los punteros todavía no se han encontrado:

\[
d_i>0
\]

Como el puntero rápido avanza una posición más que el lento en cada iteración, la distancia disminuye en una unidad:

\[
\Phi_{i+1}=\Phi_i-1
\]

Cuando:

\[
\Phi_i=0
\]

los punteros coinciden y el algoritmo devuelve `True`.

**Nota sobre la inicialización:** Si la cabeza ya pertenece al ciclo (\(\mu=0\)), ambos punteros comienzan en el mismo nodo, pero el algoritmo todavía no ha realizado la primera comparación. Por eso, en ese estado inicial tomamos \(\Phi_0=\lambda\). Después del primer movimiento, si todavía no se han encontrado, la distancia desde `rapido` hasta `lento` es \(\lambda-1\). A partir de ahí, el potencial disminuye hasta cero.

**Conclusión del potencial:**

En una lista sin ciclo, el puntero rápido termina alcanzando el final. En una lista con ciclo, el potencial disminuye hasta que los punteros coinciden.

En ambos casos, el algoritmo termina después de un número finito de iteraciones.

---

## 4. Costo

Analizamos el costo en función de la cantidad de nodos.

Sea:

- \(n\): cantidad de nodos distintos de la lista.
- \(\mu\): cantidad de nodos antes de entrar al ciclo.
- \(\lambda\): longitud del ciclo.

Cuando existe un ciclo:

\[
n=\mu+\lambda
\]

### Tiempo

**Si no existe un ciclo:**

El puntero rápido avanza dos posiciones por iteración y alcanza el final de la lista después de, como máximo, \(O(n)\) iteraciones.

**Si existe un ciclo:**

- El puntero lento necesita como máximo \(\mu\) iteraciones para entrar en el ciclo.
- Una vez que ambos punteros están dentro del ciclo, necesitan como máximo \(\lambda\) iteraciones adicionales para encontrarse.

Por tanto, el número total de iteraciones está acotado por:

\[
\mu+\lambda=n
\]

En cada iteración se realiza una cantidad constante de operaciones: asignaciones, accesos a `.next` y comparaciones.

Por tanto:

\[
\boxed{T(n)=O(n)}
\]

En el peor caso, también se tiene una cota inferior lineal, por lo que:

\[
\boxed{T(n)=\Theta(n)}
\]

### Espacio

El algoritmo utiliza únicamente dos punteros adicionales:

- `lento`.
- `rapido`.

No necesita almacenar nodos adicionales ni utilizar estructuras auxiliares cuyo tamaño dependa de la lista.

Por tanto:

\[
\boxed{S(n)=O(1)}
\]

---

## 5. Conclusión

El algoritmo de Floyd permite detectar ciclos en una lista enlazada utilizando dos punteros que avanzan a velocidades diferentes.

El invariante demuestra que, si los punteros coinciden después de avanzar, necesariamente existe un ciclo. Además, la diferencia de velocidad garantiza que, cuando existe un ciclo, los punteros terminan encontrándose.

El potencial demuestra la terminación: si no existe un ciclo, el puntero rápido alcanza el final; si existe, la distancia relativa entre ambos punteros disminuye hasta cero una vez que entran en el ciclo.

Finalmente, el análisis de complejidad establece que:

\[
\boxed{T(n)=\Theta(n)}
\]

\[
\boxed{S(n)=O(1)}
\]

Por tanto, el algoritmo de Floyd detecta ciclos en tiempo lineal y utilizando espacio auxiliar constante, sin necesidad de almacenar los nodos visitados.