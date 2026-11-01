# Ejercicio 9 - Una mezcla "optimizada"

> Una mezcla "optimizada" de dos listas ordenadas de largo $n$ deja de comparar cuando a
> la primera lista le queda un solo elemento, y lo pone al final. Cuenta cuántas
> comparaciones hace en el peor caso. Sin probarla, usa la sección 6 de la conferencia 5
> para decidir si es correcta, y construye con el adversario la entrada en la que falla.

## 1. La mezcla "optimizada"

La mezcla normal (C5, §6) compara el frente de cada lista y saca el menor; hace a lo
sumo $2n-1$ comparaciones. La variante "optimizada" añade una regla: **en cuanto a la
primera lista $A$ le quede un solo elemento, deja de comparar y lo pone al final**.

```python
def mezcla_optimizada(A, B):
    """A, B ordenadas de largo n. 'Optimiza' parando cuando a A le queda 1 elemento."""
    R, i, j, comp = [], 0, 0, 0
    while i < len(A) - 1 and j < len(B):     # <- para cuando a A le queda 1
        comp += 1
        if A[i] <= B[j]:
            R.append(A[i]); i += 1
        else:
            R.append(B[j]); j += 1
    # 'optimizacion': vuelca el resto de B y pone el ultimo de A al final
    R.extend(B[j:])
    R.extend(A[i:])                          # el (unico) elemento restante de A, AL FINAL
    return R, comp
```

El bug está en `R.extend(A[i:])` **después** de `B[j:]`: asume que el último elemento de
$A$ es mayor que todo lo que queda de $B$, lo cual no tiene por qué ser cierto.

## 2. Peor caso de comparaciones

El ciclo para cuando $i = n-1$ (a $A$ le queda 1) **o** cuando $j=n$ ($B$ agotada).
Cada comparación saca un elemento de $A$ o de $B$ hacia $R$. En el peor caso (la
intercalada perfecta) el ciclo saca los $n-1$ primeros de $A$ y, alternando, $n-2$
de $B$ antes de que $i$ llegue a $n-1$ y la condición `i < len(A) - 1` lo detenga:
$$\text{comparaciones en el peor caso} = (n-1) + (n-2) = 2n-3.$$
Dos menos que la mezcla correcta ($2n-1$). **Esas comparaciones ahorradas son las que
la hacen incorrecta** (C5, §8: un algoritmo que hace menos que la cota mínima está mal).

## 3. ¿Es correcta? - lo que dice C5, §6

La cota de C5, §6 dice: **mezclar dos listas de largo $n$ requiere $2n-1$ comparaciones
en el peor caso**, y el adversario usa la entrada **intercalada perfecta**
$$a_1 < b_1 < a_2 < b_2 < \dots < a_n < b_n,$$
que tiene $2n-1$ pares de vecinos, y **cada par debe compararse** o el algoritmo se
equivoca al intercambiar los valores de ese par.

La mezcla optimizada hace solo $2n-3$ comparaciones en el peor caso: **dos menos que la
cota**. Por el teorema de C5, §6, **ningún** algoritmo correcto puede hacer menos de
$2n-1$, así que la mezcla optimizada **es incorrecta**. No hace falta ejecutarla: la
cota mínima lo garantiza (C5, §8, "la cota mínima como detector de errores").

## 4. La entrada que la rompe - construida con el adversario

El adversario de C5, §6 trabaja sobre la intercalada perfecta. El par de vecinos que la
optimización **deja de comparar** es el que involucra al **último elemento de $A$**,
$a_n$, con su vecino $b_{n-1}$ en la cadena intercalada. Intercambiando los valores de
ese par de vecinos, ambas listas siguen ordenadas pero la salida correcta cambia, y la
mezcla optimizada (que no comparó ese par) produce la salida vieja: se equivoca.

**Entrada concreta ($n=3$):** tomamos $A = [1, 3, 5]$, $B = [2, 4, 6]$ (intercalada
$1<2<3<4<5<6$). La optimización para cuando a $A$ le queda $a_3=5$. Si en su lugar
ponemos $a_3$ **menor** que el resto de $B$, el "poner al final" lo coloca mal:

```python
A = [1, 3, 5]     # el ultimo elemento de A deberia ir al final solo si es el mayor
B = [2, 4, 100]   # pero si B tiene algo mayor que A[-1]=5 despues del corte...
```

El caso que rompe de forma nítida: hacer que **el último de $A$ sea menor que el último
de $B$**, de modo que `A[i:]` no deba ir al final.

## 5. Figura - por qué "poner A al final" falla

$A=[1,3,5]$, $B=[2,4,6]$. La optimización para cuando a $A$ le queda `5`:

```
paso a paso (ciclo para cuando a A le queda 1 -> i llega a 2):
  compara 1 vs 2 -> saca 1 (A)         R=[1]            i=1
  compara 3 vs 2 -> saca 2 (B)         R=[1,2]          j=1
  compara 3 vs 4 -> saca 3 (A)  i=2 -> a A le queda solo {5}: PARA
  vuelca B[j:] = [4,6]                 R=[1,2,3,4,6]
  pone A[i:] = [5] AL FINAL            R=[1,2,3,4,6,5]   ✗  5 quedo despues de 6
                                                            ^^^^ DESORDENADO

salida correcta: [1,2,3,4,5,6]
salida optimizada: [1,2,3,4,6,5]   -> MAL (el 5 quedo detras del 6)
```

El `5` de $A$ debía ir **antes** del `6` de $B$, pero la optimización lo pegó al final
sin compararlo con `6`. Ese es exactamente el par de vecinos $(a_3,b_?)$ que el
adversario de C5, §6 obliga a comparar.

## 6. Comprobación - el peor caso y el contraejemplo

```python
def mezcla_correcta(A, B):
    R, i, j, comp = [], 0, 0, 0
    while i < len(A) and j < len(B):
        comp += 1
        if A[i] <= B[j]:
            R.append(A[i]); i += 1
        else:
            R.append(B[j]); j += 1
    R.extend(A[i:]); R.extend(B[j:])
    return R, comp

# (1) contraejemplo: la optimizada se equivoca
A, B = [1, 3, 5], [2, 4, 6]
ropt, _ = mezcla_optimizada(A, B)
rok, _ = mezcla_correcta(A, B)
print("optimizada:", ropt, "  correcta:", rok, "  ¿ordenada la optimizada?",
      ropt == sorted(ropt))

# (2) peor caso de comparaciones sobre la intercalada perfecta
import random
random.seed(0)
for n in [3, 10, 100, 1000]:
    A = list(range(0, 2 * n, 2))        # 0,2,4,... (a_i)
    B = list(range(1, 2 * n, 2))        # 1,3,5,... (b_i)  -> intercalada
    _, c_opt = mezcla_optimizada(A, B)
    print(f"n={n:>5}: comparaciones optimizada = {c_opt}  (2n-3 = {2*n-3}, "
          f"cota correcta 2n-1 = {2*n-1})")
```

**Salida:**

```
optimizada: [1, 2, 3, 4, 6, 5]   correcta: [1, 2, 3, 4, 5, 6]   ¿ordenada la optimizada? False
n=    3: comparaciones optimizada = 3  (2n-3 = 3, cota correcta 2n-1 = 5)
n=   10: comparaciones optimizada = 17  (2n-3 = 17, cota correcta 2n-1 = 19)
n=  100: comparaciones optimizada = 197  (2n-3 = 197, cota correcta 2n-1 = 199)
n= 1000: comparaciones optimizada = 1997  (2n-3 = 1997, cota correcta 2n-1 = 1999)
```

La optimizada hace $2n-2$ comparaciones (una menos que la cota $2n-1$) y produce salida
**desordenada** en la intercalada: incorrecta, tal como predice C5, §6/§8.

## 7. Respuesta

- **Peor caso de comparaciones:** $2n-3$.
- **¿Correcta?** No. La cota de C5, §6 exige $2n-1$ comparaciones; hacer una menos la
  vuelve incorrecta sin necesidad de ejecutarla.
- **Entrada que falla:** la intercalada perfecta (p. ej. $A=[1,3,5]$, $B=[2,4,6]$),
  donde el par de vecinos que involucra al último de $A$ nunca se compara y "poner $A$
  al final" lo coloca después de elementos mayores de $B$.
