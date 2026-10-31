# Ejercicio 7 ★★★ — Mediana de dos arreglos ordenados (C2, C3, C5)

> Mediana de dos arreglos ordenados de largo $n$: el $n$-ésimo menor de los $2n$ elementos. Diseña un algoritmo $O(\log n)$, demuestra su correctitud y da la cota de información.

## 1. El problema

- **Entrada:** $A[0..n-1]$ y $B[0..n-1]$ ordenados crecientemente (se permiten repetidos), $n\ge1$.
- **Salida:** el $n$-ésimo menor de los $2n$ elementos, es decir `sorted(A + B)[n-1]` (la mediana inferior).
- **Modelo:** comparaciones entre elementos.
- **Fuerza bruta (oráculo):** mezclar hasta sacar $n$ elementos, con $\le n$ comparaciones y $O(n)$. Queremos $O(\log n)$.

## 2. La idea: elegir cuántos elementos aporta $A$

El $n$-ésimo menor separa los $2n$ elementos en "los $n$ menores" y "el resto". Los $n$ menores son un prefijo de $A$ más un prefijo de $B$: $A[0..i-1]$ y $B[0..j-1]$ con $i+j=n$. Basta encontrar el $i$ correcto, y eso se hace por búsqueda binaria sobre $i\in\{0,\dots,n\}$.

Definimos, para $1\le m\le n$, el predicado
$$P(m):\quad A[m-1]\le B[n-m] ,$$
y $P(0)=$ verdadero. Intuitivamente, "tomar $m$ elementos de $A$ no es demasiado".

**$P$ es monótono:** si $P(m)$ y $m'<m$, entonces $A[m'-1]\le A[m-1]\le B[n-m]\le B[n-m']$, así que $P(m')$. Por tanto $P$ es verdadero en $0..i^*$ y falso después, para un único $i^*$.

## 3. Algoritmo

La función `n_esimo(A, B, comparar)` hace una búsqueda binaria sobre $m$, la cantidad de elementos que $A$ aporta a los $n$ menores, usando la prueba $P(m)$: $A[m-1]\le B[n-m]$. Al terminar, `lo` es $i^*$, y la respuesta es el mayor entre $A[i^*-1]$ y $B[n-i^*-1]$ (o el único de los dos que exista, si una de las listas aporta 0 elementos).

> Código: [ejercicio-07.py](ejercicio-07.py), parte 1.

## 4. Correctitud

### 4.1 La búsqueda binaria encuentra $i^*$ (invariante y potencial)

**Invariante:** $0\le lo<hi\le n+1$, $P(lo)$ es verdadero, y ($hi=n+1$ o $P(hi)$ es falso).

- *Inicialización:* $lo=0$ (y $P(0)$ es verdadero por definición), $hi=n+1$.
- *Mantenimiento:* $m=\lfloor(lo+hi)/2\rfloor$ cumple $lo<m<hi$ porque $hi-lo\ge2$, así que $1\le m\le n$ y los índices $m-1$ y $n-m$ son válidos. Si $P(m)$, se hace $lo=m$; si no, $hi=m$. Las dos partes se mantienen.
- *Conclusión:* al salir, $hi=lo+1$. $P(lo)$ es verdadero y $P(lo+1)$ es falso (o $lo=n$). Por monotonía, $lo=i^*$.

**Potencial:** $\Phi=hi-lo$, que empieza en $n+1$ y en cada vuelta pasa a $\lfloor\Phi/2\rfloor$ o $\lceil\Phi/2\rceil$. El ciclo hace a lo sumo $\lceil\log_2(n+1)\rceil$ vueltas.

### 4.2 Con $i=i^*$, $j=n-i$, la respuesta es $\max(A[i-1],B[j-1])$

Por la definición de $i^*$ (con las convenciones $A[-1]=B[-1]=-\infty$ y $A[n]=B[n]=+\infty$):

- (a) $A[i-1]\le B[j]$, porque $P(i)$ (si $i=0$ es trivial);
- (b) $A[i]>B[j-1]$, porque $P(i+1)$ es falso: $A[i]>B[n-i-1]=B[j-1]$ (si $i=n$ es trivial).

Sean $L=A[0..i-1]\cup B[0..j-1]$ ($n$ elementos) y $R$ el resto. **Todo elemento de $L$ es $\le$ todo elemento de $R$:**
- $A[0..i-1]\le A[i..]$ y $B[0..j-1]\le B[j..]$ por el orden;
- $A[0..i-1]\le A[i-1]\le B[j]\le B[j..]$ por (a);
- $B[0..j-1]\le B[j-1]<A[i]\le A[i..]$ por (b).

Sea $v=\max L$. Hay al menos $n$ elementos $\le v$ (todo $L$), y todo elemento $<v$ está en $L\setminus\{v\}$, porque los de $R$ son $\ge v$. Así que $v$ es el $n$-ésimo menor. Y $\max L=\max(A[i-1],B[j-1])$ porque cada parte está ordenada. ∎

## 5. Costo

- Comparaciones: $\le\lceil\log_2(n+1)\rceil$ en la búsqueda, más 1 al final, o sea $\le\lceil\log_2(n+1)\rceil+1$.
- Tiempo $O(\log n)$ y memoria $O(1)$.
- Visto como divide y vencerás: cada comparación descarta la mitad de los candidatos, $T(n)=T(n/2)+O(1)=O(\log n)$.

## 6. Cota de información

**Hay $2n$ salidas posibles.** Con valores distintos, la respuesta puede ser cualquiera de los $2n$ elementos. Para que sea $A[i]$ basta que haya exactamente $i$ elementos de $A$ y $n-1-i$ de $B$ por debajo de él, y eso se logra eligiendo bien los valores. Lo mismo para $B[j]$.

**Cada salida necesita su propia hoja.** Un algoritmo de comparaciones no ve los valores, solo las respuestas. Su salida es "el elemento de tal posición", y depende solo de la hoja a la que llega (lema 2 de la C5 §3). Dos entradas cuyas respuestas correctas están en posiciones distintas no pueden terminar en la misma hoja. Además, con valores distintos ninguna comparación da empate y el árbol es binario.

**Conclusión:** el árbol tiene $\ge2n$ hojas, así que su altura es $\ge\lceil\log_2(2n)\rceil=1+\lceil\log_2 n\rceil$ comparaciones.

| | comparaciones |
|---|---|
| cota de información | $\lceil\log_2 2n\rceil=1+\lceil\log_2 n\rceil$ |
| nuestro algoritmo | $\le\lceil\log_2(n+1)\rceil+1$ |

Son iguales salvo cuando $n$ es potencia de 2, y entonces difieren en 1. El algoritmo es óptimo: $\Theta(\log n)$, con la misma constante.

## 7. Casos de prueba y validación

Herramientas de prueba: `Contador`, un comparador que cuenta las comparaciones, y `oraculo`, que calcula el $n$-ésimo menor ordenando $A+B$ completo. Esta parte no imprime nada.

> Código: [ejercicio-07.py](ejercicio-07.py), parte 2.

Casos a mano:

> Código: [ejercicio-07.py](ejercicio-07.py), parte 3.

```text
A=[1], B=[2] -> 1  (oráculo 1)
A=[1, 2, 3], B=[4, 5, 6] -> 3  (oráculo 3)
A=[4, 5, 6], B=[1, 2, 3] -> 3  (oráculo 3)
A=[1, 3, 5], B=[2, 4, 6] -> 3  (oráculo 3)
A=[2, 2, 2], B=[2, 2, 2] -> 2  (oráculo 2)
A=[1, 1, 9, 9], B=[1, 9, 9, 9] -> 9  (oráculo 9)
```

**Exhaustiva:** para cada $n\le9$, todas las formas de repartir los valores $0..2n-1$ entre $A$ y $B$ (todas las entradas posibles con valores distintos, salvo renombrar). Comprobamos el resultado y el número de comparaciones:

> Código: [ejercicio-07.py](ejercicio-07.py), parte 4.

```text
n = 1:      2 entradas, peor caso 1 comparaciones, cota de información 1
n = 2:      6 entradas, peor caso 3 comparaciones, cota de información 2
n = 3:     20 entradas, peor caso 3 comparaciones, cota de información 3
n = 4:     70 entradas, peor caso 4 comparaciones, cota de información 3
n = 5:    252 entradas, peor caso 4 comparaciones, cota de información 4
n = 6:    924 entradas, peor caso 4 comparaciones, cota de información 4
n = 7:   3432 entradas, peor caso 4 comparaciones, cota de información 4
n = 8:  12870 entradas, peor caso 5 comparaciones, cota de información 4
n = 9:  48620 entradas, peor caso 5 comparaciones, cota de información 5
```

Al azar con muchos repetidos y $n$ grande:

> Código: [ejercicio-07.py](ejercicio-07.py), parte 5.

```text
n =    1,000: 10 comparaciones (log2(n+1)+1 = 11)
n =  100,000: 18 comparaciones (log2(n+1)+1 = 18)
n = 1,000,000: 21 comparaciones (log2(n+1)+1 = 21)
```

**La cota de información en código:** construimos, para cada una de las $2n$ posiciones, una entrada en la que la respuesta está ahí. Así se ve que hay $2n$ salidas distintas.

> Código: [ejercicio-07.py](ejercicio-07.py), parte 6.

```text
n =  1: 2 salidas distintas -> al menos ceil(log2 2) = 1 comparaciones
n =  2: 4 salidas distintas -> al menos ceil(log2 4) = 2 comparaciones
n =  5: 10 salidas distintas -> al menos ceil(log2 10) = 4 comparaciones
n =  8: 16 salidas distintas -> al menos ceil(log2 16) = 4 comparaciones
n = 13: 26 salidas distintas -> al menos ceil(log2 26) = 5 comparaciones
```

## 8. Resumen

- **Algoritmo:** búsqueda binaria del número $i$ de elementos que aporta $A$, con el predicado monótono $A[i-1]\le B[n-i]$. Respuesta: $\max(A[i-1],B[n-i-1])$.
- **Correctitud:** invariante de búsqueda binaria + la partición $L\le R$.
- **Costo:** $\le\lceil\log_2(n+1)\rceil+1$ comparaciones.
- **Cota:** $2n$ salidas posibles ⇒ $\ge\lceil\log_2 2n\rceil$. Óptimo.
