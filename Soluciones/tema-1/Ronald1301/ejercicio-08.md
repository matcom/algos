# Ejercicio 8 — El elemento que aparece más de $n/3$ veces

> Generaliza Boyer-Moore con dos candidatos, enuncia el invariante reforzado y
> demuéstralo. Después escribe la versión que devuelve los candidatos con contador
> positivo **sin verificarlos**, y busca un generador de pruebas que **no** la atrape.
> Cuidado: el análogo del generador binario de la conferencia 3 sí la atrapa.

*(Borrador preparado con asistencia de IA, siguiendo el formato de Agustin y los materiales del Tema 1.)*

## 1. El problema

Dado un arreglo de $n$ elementos comparables solo por igualdad (C3, §2), devolver todos
los que aparecen **más de $n/3$ veces**. Puede haber **0, 1 o 2** de ellos (no caben
tres elementos que superen cada uno $n/3$). Queremos $O(n)$ tiempo y $O(1)$ memoria,
exactamente como Boyer-Moore pero con **dos** pares candidato-contador. Es el caso
$k=3$ del algoritmo de Misra-Gries (C3, ejercicio 2).

**Idea de cancelación generalizada** (C3, §2): si tacho **tres** elementos distintos a
la vez, cualquier elemento con más de $n/3$ copias sigue teniendo más de un tercio en
lo que queda. Con dos candidatos, "tres distintos" aparece cuando llega un elemento que
no coincide con ninguno de los dos candidatos vivos: se cancela una copia de cada uno.

## 2. El algoritmo

```python
def mas_de_n_tercios(A):
    # primera pasada: mantener 2 candidatos con cancelacion de a tres
    c1 = c2 = None
    k1 = k2 = 0
    for x in A:
        if c1 is not None and x == c1:
            k1 += 1
        elif c2 is not None and x == c2:
            k2 += 1
        elif k1 == 0:
            c1, k1 = x, 1
        elif k2 == 0:
            c2, k2 = x, 1
        else:                       # x distinto de ambos: cancelar uno de cada
            k1 -= 1
            k2 -= 1
    # segunda pasada: verificar
    res = []
    for c in {c1, c2} - {None}:
        if A.count(c) > len(A) // 3:
            res.append(c)
    return sorted(res, key=lambda v: (str(type(v)), v))
```

## 3. Invariante reforzado y su demostración (C3, §4)

Como en Boyer-Moore (C3, §4), el invariante "ingenuo" (*los candidatos son los
mayoritarios de cada prefijo*) **no es inductivo**. Lo reforzamos describiendo el estado
como una partición:

> **Invariante reforzado.** Tras procesar el prefijo $A[1..t]$, ese prefijo se puede
> descomponer en:
> - $k_1$ copias del candidato $c_1$,
> - $k_2$ copias del candidato $c_2$,
> - un conjunto de **tripletas de elementos mutuamente distintos** (cada tripleta tiene
>   tres valores distintos entre sí y distintos a lo guardado como copias),
>
> donde $k_1,k_2$ son los contadores. (Es la cancelación "de a tres" hecha explícita.)

**Inicialización.** Prefijo vacío, $k_1=k_2=0$: cero copias y cero tripletas. ✓

**Mantenimiento.** Procesamos $x=A[t+1]$ con el invariante para $A[1..t]$:
- $x=c_1$ (o $x=c_2$): sube $k_1$ (resp. $k_2$); $x$ es una copia más. La partición
  gana una copia. ✓
- $x\ne c_1,c_2$ y $k_1=0$: $c_1\leftarrow x$, $k_1=1$. Antes no había copias de $c_1$,
  ahora hay una de $x$; las tripletas no cambian. ✓ (igual con $k_2=0$).
- $x\ne c_1,c_2$ y $k_1,k_2>0$: tomamos una copia de $c_1$, una de $c_2$ y el propio
  $x$: tres valores **distintos** (porque $x\ne c_1\ne c_2$ y $c_1\ne c_2$, que se
  mantiene porque un candidato solo se fija cuando su contador está en 0). Forman una
  tripleta nueva; $k_1,k_2$ bajan en 1. ✓

**Conclusión (el teorema "si aparece > n/3, es candidato").** Al terminar, $A$ se parte
en $k_1$ copias de $c_1$, $k_2$ de $c_2$ y $T$ tripletas de distintos, con
$k_1+k_2+3T=n$. Supongamos que un valor $m$ aparece $>n/3$ veces y $m\notin\{c_1,c_2\}$.
Entonces $m$ solo puede estar en las tripletas, y como cada tripleta tiene tres valores
**distintos**, contiene a lo sumo **una** copia de $m$. Luego $m$ aparece
$\le T = (n-k_1-k_2)/3 \le n/3$ veces. Contradicción con $>n/3$. Por tanto **todo**
elemento con más de $n/3$ copias es $c_1$ o $c_2$. $\square$

La segunda pasada es imprescindible: el invariante solo dice "si aparece $>n/3$, es
candidato", **no** la recíproca — igual que en C3, §5 con la mayoría.

## 4. Figura — cancelación de a tres

Arreglo `A A B C A D A B A` ($n=9$, umbral $>3$). Columnas: contadores tras cada paso.

```
 x : A  A  B  C  A  D  A  B  A
----------------------------------------
c1 : A  A  A  A  A  A  A  A  A
k1 : 1  2  2  1  2  1  2  2  3
c2 : -  -  B  B  B  B  B  B  B
k2 : 0  0  1  1  1  0  0  1  1
            ↑  ↑        ↑
       B nuevo  C: distinto de A,B    D: distinto de A,B
       (ocupa c2) -> cancela k1,k2    -> cancela k1,k2

Al final: c1=A (k1=3), c2=B (k2=1).
Verificacion: A aparece 5 > 3 ✓ ;  B aparece 2, no > 3  ✗.
Resultado: [A].
```

El paso `C` (posición 4) y `D` (posición 6) son las cancelaciones de a tres: bajan
ambos contadores. `B` sobrevive con contador positivo pero **no** supera $n/3$ — por eso
hace falta la segunda pasada.

## 5. La versión sin verificar y un generador que no la atrapa

La versión "atajo" devuelve los candidatos con contador positivo **sin** la segunda
pasada:

```python
def atajo_sin_verificar(A):
    c1 = c2 = None
    k1 = k2 = 0
    for x in A:
        if c1 is not None and x == c1: k1 += 1
        elif c2 is not None and x == c2: k2 += 1
        elif k1 == 0: c1, k1 = x, 1
        elif k2 == 0: c2, k2 = x, 1
        else: k1 -= 1; k2 -= 1
    return sorted({c for c, k in [(c1, k1), (c2, k2)] if c is not None and k > 0},
                  key=lambda v: (str(type(v)), v))
```

Es **incorrecta** (como en C3, §5): contador positivo no implica superar $n/3$. El
contraejemplo mínimo es `A B C`: cada uno queda con contador $\le1$, el atajo devuelve
candidatos aunque **ninguno** aparezca más de $3/3=1$ veces.

**Generador que NO lo atrapa — "mayoría doble plantada".** Igual que en C3, §5 el
generador de mayoría plantada no podía atrapar el atajo binario, aquí un generador que
**siempre planta dos elementos por encima de $n/3$** no lo atrapa nunca: en esos
arreglos los dos candidatos verdaderos existen y el atajo los encuentra correctamente,
porque la mitad mala del argumento (contador positivo $\Rightarrow$ es mayoritario)
**sí** vale cuando el mayoritario de verdad existe.

```python
def generador_que_no_atrapa(n, rng):
    """Planta SIEMPRE dos elementos con > n/3 copias cada uno. El atajo nunca falla."""
    a, b = "X", "Y"
    cuota = n // 3 + 1
    arr = [a] * cuota + [b] * cuota
    arr += [rng.choice("PQRS") for _ in range(n - len(arr))]
    rng.shuffle(arr)
    return arr
```

**El análogo binario SÍ lo atrapa** (la advertencia del enunciado). Con solo dos
símbolos `A`,`B`, un arreglo sin ningún elemento $>n/3$ no existe para $n$ grande (uno
de los dos supera $n/2>n/3$), pero con **tres** símbolos equiprobables aparecen arreglos
donde ninguno supera $n/3$ y el atajo devuelve candidatos espurios. Un generador de 3+
símbolos uniformes atrapa el atajo; el de "mayoría doble plantada" no.

## 6. Comprobación — el atajo pasa un generador y falla en otro

```python
import random

def oraculo(A):
    from collections import Counter
    u = len(A) // 3
    return sorted({v for v, k in Counter(A).items() if k > u},
                  key=lambda v: (str(type(v)), v))

rng = random.Random(3)

# (a) generador que NO atrapa: dos mayoritarios plantados
fallos_plantado = 0
for _ in range(20_000):
    n = rng.randint(6, 40)
    A = generador_que_no_atrapa(n, rng)
    fallos_plantado += atajo_sin_verificar(A) != oraculo(A)

# (b) generador de 3 simbolos uniformes: SI atrapa
fallos_tres = 0
for _ in range(20_000):
    n = rng.randint(3, 40)
    A = [rng.choice("ABC") for _ in range(n)]
    fallos_tres += atajo_sin_verificar(A) != oraculo(A)

# el algoritmo correcto no falla nunca con ningun generador
ok = True
for _ in range(20_000):
    n = rng.randint(1, 40)
    A = [rng.choice("ABCDE") for _ in range(n)]
    ok &= (mas_de_n_tercios(A) == oraculo(A))

print(f"atajo, generador plantado (no atrapa): {fallos_plantado} fallos de 20000")
print(f"atajo, 3 simbolos uniformes (SI atrapa): {fallos_tres} fallos de 20000")
print(f"algoritmo correcto (2 pasadas): sin fallos = {ok}")
```

**Salida:**

```
atajo, generador plantado (no atrapa): 0 fallos de 20000
atajo, 3 simbolos uniformes (SI atrapa): 8976 fallos de 20000
algoritmo correcto (2 pasadas): sin fallos = True
```

El generador de mayoría doble plantada da **0 fallos** (no atrapa el atajo); el de tres
símbolos uniformes lo atrapa en casi la mitad de los casos. Exactamente la lección de
C3, §5: *leer la hipótesis de un teorema es leer la lista de casos que hay que probar*.

## 7. Resumen

- **Algoritmo:** Boyer-Moore con dos candidatos (Misra-Gries, $k=3$), $O(n)$ tiempo,
  $O(1)$ memoria, dos pasadas.
- **Invariante reforzado:** el prefijo se parte en $k_1$ copias de $c_1$, $k_2$ de
  $c_2$ y tripletas de distintos; prueba "si aparece $>n/3$, es candidato".
- **Atajo sin verificar:** incorrecto; un generador de "mayoría doble plantada" nunca
  lo atrapa, pero uno de tres símbolos uniformes sí — como anuncia la demostración.

