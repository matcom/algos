# Ejercicio 14 ★★★ — Ciclo completo sobre un problema nuevo: mezclar $k$ listas ordenadas (C2 a C5)

> Escoge un problema que no hayamos visto, recorre el ciclo completo de la conferencia 2 sobre él y consigue que el algoritmo y la cota mínima coincidan. Es el formato de la pregunta larga del examen final.

Problema elegido: **mezclar $k$ listas ordenadas**. La C5 trató $k=2$ (cota $2n-1$); el caso general es nuevo. El resultado: algoritmo y cota coinciden en $N\log_2 k\,(1+o(1))$ comparaciones, con la misma constante principal.

## 1. ¿Cuál es el problema?

- **Entrada:** $k\ge1$ listas $L_1,\dots,L_k$, cada una ordenada crecientemente y de largo $n$. Total $N=kn$ elementos.
- **Salida:** una lista ordenada con los $N$ elementos.
- **Empates:** se permiten valores repetidos; cualquier orden entre iguales es válido.
- **Modelo:** comparaciones entre elementos (respuesta $\le$ o $>$). El costo es el número de comparaciones en el peor caso. Memoria y tiempo en la RAM de la C1.

## 2. ¿Qué algoritmo lo resuelve?

| algoritmo | idea | comparaciones (peor caso) |
|---|---|---|
| fuerza bruta | concatenar y ordenar con mergesort | $\approx N\log_2 N$ (ignora que ya vienen ordenadas) |
| secuencial | $((L_1\oplus L_2)\oplus L_3)\oplus\dots$ | $\sum_{i=2}^{k}(in-1)=\Theta(Nk)$ |
| **divide y vencerás** | mezclar la mitad izquierda, la derecha, y mezclar los dos resultados | $\le N\lceil\log_2 k\rceil-(k-1)$ |

Elegimos divide y vencerás. `mezclar(I, D, cuenta)` es la mezcla de dos listas de la C5 y acumula sus comparaciones en `cuenta`; `mezclar_k(listas, cuenta)` parte las $k$ listas en dos mitades, mezcla cada mitad recursivamente y mezcla los dos resultados.

> Código: [ejercicio-14.py](ejercicio-14.py), parte 1.

## 3. ¿Es correcto?

**Lema (mezcla de dos).** Invariante del ciclo de `mezclar`: *$R$ contiene, ordenados, los $|R|$ menores de $I\cup D$, y todo elemento de $R$ es $\le$ que todos los de $I[i:]$ y $D[j:]$.*
- *Inicialización:* $R$ vacío.
- *Mantenimiento:* si $I[i]\le D[j]$, entonces $I[i]$ es el menor de lo que queda: es $\le D[j]\le D[j:]$ y $\le I[i+1:]$ por el orden de $I$. Agregarlo al final de $R$ mantiene el orden (todo $R$ era $\le I[i]$) y la segunda parte. Simétrico en el otro caso.
- *Conclusión:* al salir, una de las dos está vacía. Lo que queda de la otra está ordenado y es $\ge$ todo $R$, así que $R$ + resto está ordenado y contiene todo.
- *Terminación:* el potencial $(|I|-i)+(|D|-j)$ baja 1 por vuelta.

**Teorema.** `mezclar_k` devuelve los $N$ elementos ordenados. *Por inducción fuerte sobre $k$:* para $k\le1$ es inmediato. Para $k\ge2$, las dos llamadas tienen menos listas ($\lceil k/2\rceil$ y $\lfloor k/2\rfloor$, ambas $<k$) y por hipótesis devuelven listas ordenadas. El lema dice que su mezcla es la lista ordenada de todo. ∎

## 4. ¿Cuánto cuesta?

**Comparaciones.** El árbol de recursión es un árbol binario con $k$ hojas (las listas) y $k-1$ nodos internos (las mezclas). Cada mezcla de dos listas de largos $p,q$ cuesta $\le p+q-1$. Contamos **por elemento** (método agregado): un elemento de la lista $L_i$ participa en una mezcla por cada nivel entre su hoja y la raíz, es decir, en $\text{prof}(i)$ mezclas. Sumando:
$$C\le\sum_{\text{mezclas}}(p+q-1)=n\sum_{i=1}^{k}\text{prof}(i)-(k-1)=n\,D(k)-(k-1),$$
donde $D(k)$ es la suma de las profundidades de las hojas. Partiendo por la mitad, las hojas quedan a profundidad $\lfloor\log_2 k\rfloor$ o $\lceil\log_2 k\rceil$, y
$$D(k)=k\lceil\log_2 k\rceil-2^{\lceil\log_2 k\rceil}+k\ \le\ k\lceil\log_2 k\rceil .$$

Resultado:
$$C\le n\,D(k)-(k-1)\le N\lceil\log_2 k\rceil-(k-1).$$
Si $k$ es potencia de 2, $C\le N\log_2 k-(k-1)$. Para $k=2$ da $2n-1$, la mezcla de la C5. En general $D(k)/k\le\log_2 k+0{,}09$, así que $C\le N(\log_2 k+0{,}09)$.

La cota se **alcanza**. Una mezcla de $I$ y $D$ cuesta $p+q-1$ cuando sus dos últimos elementos salen de lados distintos. Se construye la entrada de arriba hacia abajo: en cada nodo, el orden global pone $I[:-1] < D[:-1] < I[-1] < D[-1]$, y dentro de cada hijo se repite la construcción. Así cada mezcla del árbol usa $p+q-1$ comparaciones.

**Tiempo** $\Theta(N\log k)$ (recurrencia $T(k)=2T(k/2)+\Theta(kn)$, Teorema Maestro), **memoria** $O(N)$.

## 5. ¿Se puede hacer mejor? Cota de información

**Cuántas salidas.** Con valores distintos, la salida es un **intercalado**: la sucesión de qué lista aporta cada elemento de la salida. Hay
$$\Lambda=\binom{N}{n,\dots,n}=\frac{N!}{(n!)^k}$$
intercalados, y todos son posibles.

**Cada uno necesita su hoja.** Como en el lema 2 de la C5: la salida depende solo de la hoja (el algoritmo solo ve respuestas), y dos entradas con intercalados distintos necesitan salidas distintas (en algún punto, una pone primero un elemento de $L_i$ y la otra uno de $L_j$, y solo una de las dos tiene razón). Por el lema 1 de la C5, la altura es $\ge\log_2\Lambda$.

**Cuánto es.** Con las cotas del lema 3 de la C5 y la integral en el otro sentido:
- $\log_2 N!\ge N\log_2 N-N\log_2 e$,
- $\log_2 n!\le\int_1^{n+1}\log_2x\,dx=(n+1)\log_2(n+1)-n\log_2 e$.

Restando (los términos con $\log_2 e$ se cancelan porque $kn=N$):
$$\log_2\Lambda\ \ge\ N\log_2\frac{N}{n+1}-k\log_2(n+1)\ \ge\ N\log_2 k-k\big(\log_2(n+1)+\log_2 e\big),$$
usando $N\log_2(1+1/n)\le k\log_2 e$.

**Teorema.** Todo algoritmo de comparaciones que mezcla $k$ listas ordenadas de largo $n$ hace, en el peor caso, al menos $N\log_2 k-k(\log_2(n+1)+1{,}443)$ comparaciones.

## 6. Coinciden

| | comparaciones |
|---|---|
| cota mínima | $\ge N\log_2 k-k(\log_2(n+1)+1{,}443)$ |
| algoritmo ($k$ potencia de 2) | $\le N\log_2 k-(k-1)$ |
| algoritmo (cualquier $k$) | $\le N(\log_2 k+0{,}09)$ |

La diferencia es $O(k\log n)$, de orden menor que $N\log_2 k=kn\log_2 k$. Los dos son **$N\log_2 k\,(1+o(1))$**: coinciden en el orden y en la constante principal. Para $k=2$, el algoritmo hace $2n-1$, que es exactamente la cota del adversario de la C5 §6.

## Casos de prueba y validación

Funciones auxiliares para las pruebas: `D(k)` y `peor_caso_dyv(k, n)` calculan la fórmula del peor caso, $n\,D(k)-(k-1)$, e `info(k, n)` calcula la cota de información $\log_2\big(N!/(n!)^k\big)$. Esta parte no imprime nada.

> Código: [ejercicio-14.py](ejercicio-14.py), parte 2.

Correctitud al azar (con repetidos, listas vacías, $k=1$) contra `sorted`:

> Código: [ejercicio-14.py](ejercicio-14.py), parte 3.

```text
3000 pruebas: salida ordenada y nunca más comparaciones que n·D(k) - (k-1)
```

El peor caso se alcanza con la entrada construida en el §4, y coincide con la fórmula:

> Código: [ejercicio-14.py](ejercicio-14.py), parte 4.

```text
la entrada construida alcanza exactamente n·D(k) - (k-1)
k = 2: [1, 3, 5, 7, 9, 11, 13] = 2n - 1 (C5 §6)
max de D(k)/k - log2 k para k < 10^5: 0.0861
```

Exhaustivo para $k=3$, $n=2$: todos los intercalados posibles.

> Código: [ejercicio-14.py](ejercicio-14.py), parte 5.

```text
k=3, n=2: 90 intercalados = 6!/(2!)^3; peor caso 8; cota de información ceil(log2 90) = 7
```

Algoritmo contra cota, y contra los otros algoritmos (sobre la peor entrada para divide y vencerás):

> Código: [ejercicio-14.py](ejercicio-14.py), parte 6.

```text
   k     n  cota info      D&C  D&C/info     heap  secuencial  ordenar todo
   2  1000       1995     1999     1.002     1999        1999         12087
   4  1000       7983     7997     1.002     9996        8997         28173
  16  1000      63908    63985     1.001    77982      134979        144689
  64  1000     383606   383937     1.001   509862     2078865        706753
  10  5000     166031   169991     1.024   209990      269990        476889
 256   200     408292   409345     1.003   587812     6578223        617217
```

El cociente D&C / cota tiende a 1: coinciden en la constante principal.

## Resumen

1. **Problema:** mezclar $k$ listas ordenadas de largo $n$ ($N=kn$), en el modelo de comparaciones.
2. **Algoritmo:** divide y vencerás sobre las listas, con la mezcla de dos de la C5.
3. **Correctitud:** invariante de la mezcla e inducción fuerte sobre $k$.
4. **Costo:** $\le nD(k)-(k-1)\le N\lceil\log_2 k\rceil-(k-1)$ comparaciones (método agregado); $\Theta(N\log k)$ tiempo.
5. **Cota:** $\log_2\frac{N!}{(n!)^k}\ge N\log_2 k-O(k\log n)$ por información.
6. **Coinciden:** $N\log_2 k\,(1+o(1))$ los dos. Con $k=2$, exactamente $2n-1$.
