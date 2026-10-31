# Ejercicio 6 ★★ — Buscar en una matriz con filas y columnas ordenadas (C3, C5)

> Una matriz $n\times n$ tiene filas y columnas ordenadas de forma creciente. Diseña un algoritmo que decida si contiene un valor $x$ en $O(n)$ comparaciones, demuestra su correctitud con un invariante, y demuestra con un adversario que no se puede en $o(n)$.

## Modelo y especificación

- **Precondición:** $M[i][0]\le M[i][1]\le\dots$ en cada fila y $M[0][j]\le M[1][j]\le\dots$ en cada columna.
- **Postcondición:** devuelve una posición $(i,j)$ con $M[i][j]=x$, o `None` si $x$ no está.
- **Modelo:** comparaciones de $x$ con entradas de la matriz, con respuesta $<$, $=$ o $>$.

## Algoritmo (búsqueda "en escalera" desde la esquina superior derecha)

La función `buscar(M, x, comparar)` empieza en la celda $(0, n-1)$ y en cada paso compara $x$ con $M[i][j]$: si son iguales devuelve la posición; si $x$ es menor descarta la columna $j$ y se mueve a la izquierda; si es mayor descarta la fila $i$ y baja. Si se sale de la matriz, $x$ no está. Cada paso descarta una fila o una columna, así que hace a lo sumo $2n-1$ comparaciones.

> Código: [ejercicio-06.py](ejercicio-06.py), parte 1.

La esquina superior derecha es el único lugar donde una comparación siempre descarta algo: todo lo que está debajo es mayor y todo lo que está a la izquierda es menor.

## Correctitud: invariante

$$I:\quad x\ \text{no está en ninguna celda } (r,c) \text{ con } r<i \text{ o } c>j .$$

Es decir: si $x$ está, está en la submatriz $M[i..n-1][0..j]$.

- **Inicialización.** $i=0$, $j=n-1$: no hay celdas con $r<0$ ni con $c>n-1$.
- **Mantenimiento.** Sea $v=M[i][j]$.
  - $x=v$: devuelve $(i,j)$, que es correcto.
  - $x<v$: para toda fila $r\ge i$, $M[r][j]\ge M[i][j]>x$ (columna ordenada). Las filas $r<i$ ya estaban descartadas por $I$. Toda la columna $j$ queda descartada y se puede hacer $j\leftarrow j-1$.
  - $x>v$: para toda columna $c\le j$, $M[i][c]\le M[i][j]<x$ (fila ordenada). Las columnas $c>j$ ya estaban descartadas. Toda la fila $i$ queda descartada y se puede hacer $i\leftarrow i+1$.
- **Conclusión.** El ciclo termina sin devolver cuando $i=n$ o $j=-1$. En los dos casos **toda** celda cumple $r<i$ o $c>j$, así que por $I$, $x$ no está, y `None` es correcto.

## Terminación y costo: potencial

$$\Phi=(n-i)+(j+1)=\text{filas vivas}+\text{columnas vivas}.$$

Es entero, empieza en $2n$ y baja exactamente 1 por vuelta. Dentro del ciclo las dos partes son $\ge1$. Cuando el ciclo sale, una parte es 0 y la otra $\ge1$, así que $\Phi_{\text{final}}\ge1$ y el número de vueltas es a lo sumo $2n-1$.

**Costo:** a lo sumo $2n-1$ comparaciones (una por vuelta), $O(n)$ tiempo y $O(1)$ memoria. El peor caso se alcanza, por ejemplo, cuando $x$ está en la esquina inferior izquierda de una matriz con entradas distintas.

## Cota mínima: adversario, $\ge n$ comparaciones

**Por qué la información no alcanza.** Hay $n^2+1$ salidas posibles (cada celda o "no está"), así que la información solo da $\log_2(n^2+1)\approx2\log_2 n$. Hace falta un adversario.

**Construcción.** Fijamos $x=2n-2$ y la matriz
$$M[i][j]=\begin{cases}2(i+j) & \text{si } i+j\ne n-1,\\ 2n-3 & \text{si } i+j=n-1 \text{ (antidiagonal)}.\end{cases}$$

- Es ordenada: a lo largo de una fila o columna, $i+j$ sube de 1 en 1. Las celdas anteriores a la antidiagonal valen $\le 2n-4$ y las posteriores $\ge 2n$. La celda de la antidiagonal puede valer **cualquier cosa en $(2n-4,\,2n)$**, en particular $2n-3$ o $x=2n-2$, sin romper el orden.
- Las $n$ celdas de la antidiagonal están en filas y columnas distintas: cambiar una no afecta a las otras.
- $x=2n-2$ no aparece fuera de la antidiagonal (los valores fuera son pares $2(i+j)$ con $i+j\ne n-1$).

**Estrategia del adversario.** Contesta según la matriz de arriba: "$<$" o "$>$" para las celdas fuera de la antidiagonal, y "$x>M[i][j]$" para cada celda de la antidiagonal.

**Argumento.** Supongamos que un algoritmo termina sin haber comparado $x$ con alguna celda $(i,\,n-1-i)$ de la antidiagonal.
- Si responde "no está": el adversario pone $M[i][n-1-i]=x$. La matriz sigue ordenada, todas las respuestas dadas siguen siendo verdad (esa celda nunca se comparó), y ahora $x$ sí está. El algoritmo se equivocó.
- Si responde una posición: en la matriz original $x$ no está en ningún lado, así que se equivocó.

Por tanto, todo algoritmo correcto compara $x$ con las $n$ celdas de la antidiagonal: **al menos $n$ comparaciones en el peor caso**. En particular no se puede en $o(n)$, y el algoritmo de arriba ($\le2n-1$) es óptimo salvo un factor constante.

## Casos de prueba y validación

Herramientas de prueba: `Contador` (un comparador que cuenta las comparaciones), `matriz_al_azar`, que genera matrices $n\times n$ ordenadas por filas y por columnas (con repetidos), y `esta`, el oráculo que busca $x$ celda por celda. Esta parte no imprime nada.

> Código: [ejercicio-06.py](ejercicio-06.py), parte 2.

**Correctitud contra el oráculo**, y la cota $2n-1$ comprobada y alcanzada:

> Código: [ejercicio-06.py](ejercicio-06.py), parte 3.

```text
correcto en todas las pruebas; nunca más de 2n - 1 comparaciones, y la esquina inferior izquierda las usa todas
```

**El adversario en código.** Construimos la matriz, comprobamos que está ordenada con cualquier elección en la antidiagonal, y vemos qué celdas de la antidiagonal compara el algoritmo:

> Código: [ejercicio-06.py](ejercicio-06.py), parte 4.

```text
la matriz del adversario está ordenada con cualquier elección en la antidiagonal (n <= 7)
n =  4: respuesta None, 7 comparaciones, 4 de 4 celdas de la antidiagonal comparadas
n = 16: respuesta None, 31 comparaciones, 16 de 16 celdas de la antidiagonal comparadas
n = 64: respuesta None, 127 comparaciones, 64 de 64 celdas de la antidiagonal comparadas
```

**Un algoritmo que hace menos de $n$ comparaciones queda en evidencia.** Tomamos la búsqueda en escalera pero cortada con un presupuesto de $n-1$ comparaciones (después dice "no está"). El adversario construye dos matrices que reciben las mismas respuestas y tienen respuestas correctas distintas:

> Código: [ejercicio-06.py](ejercicio-06.py), parte 5.

```text
celda nunca comparada: (5, 4)
matriz original : x no está, el algoritmo dice None
matriz cambiada : x está en (5, 4), el algoritmo dice None  (mismas comparaciones: True)
```

## Resumen

- **Algoritmo:** escalera desde $(0,n-1)$. Si $x<M[i][j]$ se descarta la columna; si $x>M[i][j]$, la fila.
- **Invariante:** si $x$ está, está en $M[i..n-1][0..j]$.
- **Potencial:** filas vivas + columnas vivas; baja 1 por comparación ⇒ $\le2n-1$ comparaciones.
- **Cota mínima:** el adversario usa la antidiagonal, donde cada celda puede ser $x$ o no sin romper el orden ⇒ $\ge n$ comparaciones. $\Theta(n)$ es óptimo.
