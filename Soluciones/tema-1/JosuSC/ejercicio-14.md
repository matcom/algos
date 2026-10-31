# Ejercicio 14: La moneda falsa. Ciclo completo de cinco preguntas sobre un problema nuevo

> **Enunciado:** Escoge un problema que no hayamos visto, recorre el ciclo completo de la conferencia 2 sobre él y consigue que el algoritmo y la cota mínima coincidan. Es el formato de la pregunta larga del examen final.

## 1. Enunciado preciso del problema

Antes de proponer un algoritmo hay que fijar qué se está preguntando, porque los problemas de pesadas esconden varias decisiones que cambian la respuesta. Es el primer reflejo de la conferencia 2, §2: precisar el problema antes de resolverlo.

**El problema.** Hay $n \geq 1$ monedas que se ven idénticas. Exactamente una es falsa y pesa menos que las demás, que pesan todas lo mismo. Disponemos de una balanza de dos platillos. En cada pesada se ponen dos grupos disjuntos de monedas, con la misma cantidad en cada platillo, y la balanza responde una de tres cosas: el platillo izquierdo pesa menos, el derecho pesa menos, o equilibrio. Hay que identificar la moneda falsa con el menor número de pesadas en el peor caso.

**El modelo de cómputo.** Cada pesada es una pregunta con tres respuestas posibles, así que un algoritmo es un árbol de decisión ternario (conferencia 5, §2): cada nodo interno es una pesada y tiene tres hijos, cada hoja nombra una moneda, y el costo es la profundidad del árbol, o sea el número de pesadas en el peor caso. Es el modelo natural porque en este problema no hay nada que calcular, solo preguntarle a la balanza. El costo de decidir qué poner en cada platillo lo medimos aparte, en el modelo de la conferencia 1 (sección 5).

**Precisiones que el enunciado no da y hay que fijar** (conferencia 2, §2):

- **Cuántas falsas y de qué tipo.** Exactamente una, y sabemos que es más liviana. Si no supiéramos si pesa más o menos, sería otro problema, y más caro (conferencia 2, §2 pide separar un problema de uno "parecido y más caro"). Ese es el de la sección 7.

- **Qué se puede poner en los platillos.** Dos grupos disjuntos con igual cantidad de monedas y ninguna moneda genuina de referencia al principio. Esto importa: con una moneda genuina de sobra se pueden comparar grupos de tamaños distintos, y ya no sería el mismo problema.

- **Qué hay que devolver.** Solo la moneda falsa. Para $n = 1$ la respuesta es la única moneda y no hace falta pesar: cero pesadas.

**Lo que hay que conseguir.** Un algoritmo que encuentre la falsa con $\lceil \log_3 n \rceil$ pesadas, y una demostración de que ninguna estrategia puede hacerlo con menos. Que los dos números coincidan es lo que cierra el ciclo (conferencia 2, §8).

## 2. Observación clave

La fuerza bruta se justifica sola y sirve de oráculo (conferencia 2, §4): pesar las monedas de dos en dos. Si la balanza se inclina, la falsa es la del platillo que pesa menos; si equilibra, las dos son genuinas y se pasa a la pareja siguiente; si al final queda una moneda sola, esa es la falsa. Es correcto porque examina todas las monedas, y hace $\lfloor n/2 \rfloor$ pesadas en el peor caso. Es lineal.

Una idea mejor es partir las candidatas en dos mitades y pesarlas una contra otra. Si hay una moneda sobrante se aparta. La mitad que pesa menos contiene a la falsa y se repite con ella. Es la búsqueda binaria de siempre, y necesita del orden de $\log_2 n$ pesadas.

Esa idea desperdicia una de las tres respuestas de la balanza. **El equilibrio también informa:** si la balanza equilibra, la falsa no está en ninguno de los dos platillos, está entre las monedas que quedaron fuera. Entonces una pesada reparte a las candidatas en tres grupos: las del platillo izquierdo, las del derecho y las apartadas, y cada una de las tres respuestas deja como candidatas a las de uno solo de los tres. Si los grupos son casi iguales, cada pesada divide por tres en lugar de por dos.

Formalmente, lo que queremos es que el número de pesadas sea

$$T(n) = \lceil \log_3 n \rceil,$$

y que la cota mínima demostrada sea exactamente ese mismo número.

## 3. El algoritmo

**La estructura.** Las monedas se numeran $0, \ldots, n-1$ y el algoritmo mantiene un intervalo $[lo, hi)$ de candidatas. Mientras haya más de una, sea $m = hi - lo$ y $a = \lceil m/3 \rceil$. Se ponen las $a$ primeras candidatas en el platillo izquierdo, las $a$ siguientes en el derecho, y las $m - 2a$ restantes se apartan.

Las cuentas dan: como $a \geq m/3$, lo que se aparta cumple $m - 2a \leq m/3 \leq a$, así que los tres grupos tienen a lo sumo $a$ monedas. Y para $m \geq 2$ se tiene $2a \leq m$, de modo que los platillos se pueden llenar. Según la balanza:

- el izquierdo pesa menos: la falsa está en las $a$ del platillo izquierdo;
- el derecho pesa menos: está en las $a$ del derecho;
- equilibrio: está entre las $m - 2a$ apartadas.

En los tres casos quedan a lo sumo $\lceil m/3 \rceil$ candidatas.

```python
def techo_log3(n):
    """Menor k con 3^k >= n."""
    k, p = 0, 1
    while p < n:
        k += 1
        p *= 3
    return k

def buscar_falsa(n, falsa, vigilar=False):
    """Las monedas son 0..n-1 y la falsa (la más liviana) es `falsa`.
    La balanza es la pregunta `falsa in izq` / `falsa in der`.
    Devuelve (moneda encontrada, número de pesadas)."""
    lo, hi, pesadas = 0, n, 0                    # la falsa está en [lo, hi)
    while hi - lo > 1:
        m = hi - lo
        a = -(-m // 3)                           # ceil(m / 3)
        izq, der = range(lo, lo + a), range(lo + a, lo + 2 * a)
        if vigilar:
            assert len(izq) == len(der) and 0 <= m - 2 * a <= a
            assert lo <= falsa < hi
        pesadas += 1
        if falsa in izq:                         # la izquierda pesa menos
            hi = lo + a
        elif falsa in der:                       # la derecha pesa menos
            lo, hi = lo + a, lo + 2 * a
        else:                                    # equilibrio: está fuera de los platillos
            lo = lo + 2 * a
        if vigilar:
            assert lo <= falsa < hi and hi - lo <= a
    return lo, pesadas
```

**Conteo de pesadas.** Después de $t$ pesadas quedan a lo sumo $\lceil n / 3^t \rceil$ candidatas, porque $\lceil \lceil x/3 \rceil / 3 \rceil = \lceil x/9 \rceil$ y así sucesivamente. Ese número llega a 1 exactamente cuando $3^t \geq n$. Por tanto el algoritmo hace a lo sumo

$$\lceil \log_3 n \rceil \text{ pesadas.}$$

## 4. La correctitud

Dos demostraciones separadas, como pide la conferencia 3: correctitud parcial (invariante) y terminación (potencial).

### Correctitud parcial: el invariante

**Invariante.** Cada vez que se evalúa la guarda del ciclo:

> la moneda falsa está en $[lo, hi)$.

**Inicialización.** Antes de la primera vuelta, $[lo, hi) = [0, n)$, que contiene a todas las monedas. ✓

**Mantenimiento.** Supongamos el invariante y $hi - lo \geq 2$. Los tres grupos (izquierdo, derecho y apartadas) son una partición de $[lo, hi)$, así que la falsa está en exactamente uno de ellos. Como el resto de las monedas pesa lo mismo y la falsa pesa menos:

- si está en el platillo izquierdo, la balanza lo marca más liviano, y el algoritmo pasa a $[lo, lo + a)$, que es el grupo izquierdo;
- si está en el derecho, el algoritmo pasa a $[lo + a, lo + 2a)$;
- si está entre las apartadas, la balanza equilibra, y el algoritmo pasa a $[lo + 2a, hi)$.

En cada caso el nuevo intervalo contiene a la falsa. ✓

**Conclusión.** Al salir del ciclo, $hi - lo = 1$ y el invariante dice que la falsa está en ese intervalo de una sola moneda: es $lo$, que es lo que devuelve el algoritmo. ✓

El invariante es inductivo y suficiente: la frase alcanza para el paso siguiente (los tres grupos cubren el intervalo, así que cada respuesta de la balanza localiza a la falsa), y en la salida, con un solo elemento, da exactamente la respuesta.

### Terminación: el potencial

**Potencial.** $\Phi = hi - lo$, el número de candidatas. Es un entero y $\Phi \geq 1$ durante todo el programa.

**Decremento.** Mientras $\Phi \geq 2$, el ciclo la reduce a lo sumo a $\lceil \Phi/3 \rceil$, que es estrictamente menor que $\Phi$ (porque $\lceil m/3 \rceil < m$ si $m \geq 2$). Por tanto el ciclo termina.

Como en el invariante, el potencial dice más que "termina": con $\Psi = \lceil \log_3 \Phi \rceil$ se tiene $\Psi' \leq \Psi - 1$ en cada vuelta, y $\Psi_0 = \lceil \log_3 n \rceil$ acota el número de pesadas, que es el costo de la sección 5.

### Verificación experimental

Antes de confiar en el argumento conviene vigilar el invariante en ejecución, como en el "invariante vigilado" de Boyer-Moore (conferencia 3, §4). La balanza se simula con la pregunta `falsa in izq`, y se prueban **todas** las posiciones de la falsa para cada $n \leq 400$.

```python
for n in range(1, 401):
    peor = 0
    for f in range(n):
        enc, p = buscar_falsa(n, f, vigilar=True)
        assert enc == f and p <= techo_log3(n)
        peor = max(peor, p)
    assert peor == techo_log3(n), (n, peor)
print("correcto para n = 1..400 y todas las posiciones; peor caso = ceil(log3 n)")
```

Esto no reemplaza la demostración: comprueba un número finito de casos. Pero confirma el invariante y el conteo sin esperar a descubrir un error de índices en la demostración.

## 5. El costo

**Pesadas.** Exactamente $\lceil \log_3 n \rceil$ en el peor caso: ya vimos que no hace más, y la sección 6 demuestra que ninguna estrategia hace menos, así que el peor caso del algoritmo no puede ser más pequeño. El programa de arriba lo confirma: el máximo sobre todas las posiciones es igual a la fórmula para todo $n \leq 400$.

**Tiempo y memoria en el modelo de la conferencia 1.** Decidir cada pesada es aritmética sobre dos enteros: calcular $a$ y los extremos de los intervalos cuesta $O(1)$ operaciones de la word RAM, y hay $O(\log n)$ pesadas, así que el costo de cómputo es $O(\log n)$. La memoria es $O(1)$: $lo$, $hi$ y $a$. El costo en pesadas y el costo de cómputo son dos medidas distintas, y las dos son logarítmicas.

**Comparación con las ideas anteriores.**

```python
print(f"{'n':>9} {'n // 2':>9} {'ceil(log2 n)':>13} {'ceil(log3 n)':>13}")
for n in [3, 9, 12, 27, 28, 100, 10**6]:
    print(f"{n:>9,} {n // 2:>9,} {(n - 1).bit_length():>13} {techo_log3(n):>13}")
```

La tabla muestra lo que calcula el programa: el costo lineal de la fuerza bruta, $\lceil \log_2 n \rceil$ como referencia de lo que cuesta partir en dos, y el de tres grupos. Para un millón de monedas, tres grupos dan 13 pesadas, y partir en dos daría del orden de 20. Es la diferencia entre $\log_3$ y $\log_2$: no es un cambio de orden asintótico, pero en un problema donde cada pregunta cuesta 1 y la cota mínima fija la constante exacta, la diferencia es lo que separa un algoritmo óptimo de uno que no lo es.

| $n$ | $\lfloor n/2 \rfloor$ | $\lceil \log_2 n \rceil$ | $\lceil \log_3 n \rceil$ |
|---|---|---|---|
| 3 | 1 | 2 | 1 |
| 9 | 4 | 4 | 2 |
| 12 | 6 | 4 | 3 |
| 27 | 13 | 5 | 3 |
| 28 | 14 | 5 | 4 |
| 100 | 50 | 7 | 5 |
| 1 000 000 | 500 000 | 20 | 13 |

## 6. La cota mínima

Aquí se cierra el ciclo. La pregunta cambia de sujeto (conferencia 2, §8): en vez de preguntar cuánto cuesta este algoritmo, pregunta cuánto cuesta cualquiera. Para decir algo sobre todos los algoritmos hay que fijar el modelo, y ya lo fijamos: árboles de decisión ternarios.

**Teorema.** Toda estrategia que identifica a la moneda falsa entre $n$ monedas, con una balanza de tres resultados, hace en el peor caso al menos $\lceil \log_3 n \rceil$ pesadas.

**Demostración (por conteo de hojas).** Para cada $i \in \{0, \ldots, n-1\}$ hay una entrada posible: la que tiene a la moneda $i$ como falsa. Son $n$ entradas, con $n$ respuestas distintas.

- Una estrategia es un árbol ternario. Cada entrada recorre un camino hasta una hoja, y la hoja nombra una moneda.
- Dos entradas con falsas distintas no pueden terminar en la misma hoja: la hoja da una sola respuesta, y sería incorrecta para una de las dos. Por tanto el árbol tiene al menos $n$ hojas.
- Un árbol ternario de altura $h$ tiene a lo sumo $3^h$ hojas (cada nivel multiplica por 3).

Entonces $3^h \geq n$, y como $h$ es entero, $h \geq \lceil \log_3 n \rceil$. $\square$

**La misma cota con un adversario** (conferencia 5). El adversario no fija la falsa de antemano. Mantiene el conjunto $S$ de candidatas que siguen siendo posibles. En cada pesada, las candidatas de $S$ quedan repartidas en tres grupos: las del platillo izquierdo, las del derecho y las apartadas. El adversario responde con la respuesta que corresponde al **grupo más grande**, que tiene al menos $\lceil |S|/3 \rceil$ candidatas. Esa respuesta es coherente con todas las anteriores, porque cualquiera de esas candidatas, si fuera la falsa, produciría exactamente esas respuestas. Tras $t$ pesadas quedan al menos $\lceil n/3^t \rceil$ candidatas, y el algoritmo no puede parar mientras haya dos o más. Por eso necesita $3^t \geq n$.

**La trampa de contar con base 3.** En la búsqueda binaria (conferencia 5, §3) los nodos también tenían tres ramas, pero la rama del medio, la igualdad, solo la recorría la entrada que estaba en el arreglo; contar las hojas con base 3 daba una cota floja y había que contar solo los huecos. Aquí es al revés: las tres respuestas de la balanza las recorre cada una un tercio de las entradas, y contar con base 3 es **exacto**. No hay que corregir nada: la cota por información es la verdadera.

**Conclusión.** El algoritmo de la sección 3 hace $\lceil \log_3 n \rceil$ pesadas, y la cota dice que ninguna estrategia puede hacer menos. El algoritmo es óptimo en este modelo, y la búsqueda se acabó (conferencia 2, §8).

### Una comprobación independiente de la cota

Para no fiarse solo de la demostración, se puede buscar el **óptimo exacto** probando todas las estrategias adaptativas posibles. Como las monedas candidatas son intercambiables, el estado de la búsqueda es solo cuántas candidatas quedan y cuántas monedas genuinas se conocen. El programa prueba todas las pesadas posibles en cada estado (cuántas candidatas poner a cada lado, completando con genuinas si hace falta) y se queda con la mejor:

```python
import math
from functools import lru_cache

@lru_cache(maxsize=None)
def optimo(m, g, N):
    """Mínimo de pesadas, en el peor caso, para localizar la falsa entre m candidatas
    (se conocen g monedas genuinas; hay N en total). Prueba TODAS las pesadas posibles:
    x candidatas a la izquierda, y a la derecha, y se completa con genuinas si x != y."""
    if m <= 1:
        return 0
    mejor = math.inf
    for x in range(1, m):                        # x == m no avanza: se descarta
        for y in range(0, min(x, m - x) + 1):    # y <= x por simetría
            if x - y > g:
                continue                         # no alcanzan las genuinas para equilibrar
            resto = m - x - y
            val = 1 + max(optimo(x, N - x, N),                           # la izquierda pesa menos
                          optimo(y, N - y, N) if y > 0 else 0,           # la derecha pesa menos
                          optimo(resto, N - resto, N) if resto > 0 else 0)  # equilibrio
            mejor = min(mejor, val)
    return mejor

coincide = True
print("   n  óptimo exacto  ceil(log3 n)")
for n in range(1, 82):
    o, c = optimo(n, 0, n), techo_log3(n)         # sin moneda de referencia: g = 0
    coincide &= (o == c)
    if n in (1, 2, 3, 4, 8, 9, 10, 13, 27, 28, 81):
        print(f"{n:>4} {o:>14} {c:>13}")
print("coincide en todos los n <= 81:", coincide)
```

El óptimo exacto coincide con $\lceil \log_3 n \rceil$ para todo $n \leq 81$.

### El error que la demostración anuncia

Hay una variante del algoritmo que parece igual de razonable y tiene un error de redondeo: usar $a = \lfloor m/3 \rfloor$ en lugar de $\lceil m/3 \rceil$. Sigue siendo **correcta**: siempre encuentra la falsa. Lo que no hace es alcanzar la cota.

```python
def buscar_falsa_piso(n, falsa):
    """Igual que buscar_falsa, pero con a = floor(m / 3) en lugar de ceil(m / 3)."""
    lo, hi, pesadas = 0, n, 0
    while hi - lo > 1:
        m = hi - lo
        a = max(1, m // 3)
        izq, der = range(lo, lo + a), range(lo + a, lo + 2 * a)
        pesadas += 1
        if falsa in izq:
            hi = lo + a
        elif falsa in der:
            lo, hi = lo + a, lo + 2 * a
        else:
            lo = lo + 2 * a
    return lo, pesadas

malas = []
for n in range(1, 401):
    peor = 0
    for f in range(n):
        enc, p = buscar_falsa_piso(n, f)
        assert enc == f                          # siempre encuentra la falsa
        peor = max(peor, p)
    if peor > techo_log3(n):
        malas.append((n, peor, techo_log3(n)))
print("n con más pesadas que la cota, entre 400:", len(malas))
print("los primeros (n, pesadas, cota):", malas[:5])
print("afectados con n <= 100:", [n for n, _, _ in malas if n <= 100])
```

Con $n = 8$, por ejemplo, el piso da $a = 2$: se pesan 2 contra 2 y se apartan 4. Si equilibra, quedan 4 candidatas y hacen falta 2 pesadas más (total 3), mientras que $\lceil \log_3 8 \rceil = 2$. La demostración dice dónde estaba el fallo: el invariante necesita que los tres grupos tengan a lo sumo $3^{k-1}$ candidatas cuando quedan $k$ pesadas, y con el piso el grupo apartado puede pasarse. Es el mismo mecanismo de la conferencia 2, §7: las pruebas de correctitud ("¿encuentra la moneda?") pasan siempre, y lo que delata a la variante es la cota mínima, que dice que con $n = 8$ se puede hacer con dos. Una cota demostrada sirve también para detectar algoritmos que no son óptimos.

## 7. El modelo, pegado a la cota

Como dice la conferencia 2, §10, una cota mínima siempre viene con un modelo pegado, y la primera pregunta ante una es cuál es ese modelo y qué deja fuera. La cota $\lceil \log_3 n \rceil$ vale para **una falsa conocida como más liviana, una balanza de platillos, y grupos de igual tamaño sin moneda de referencia**. Cambiar una de esas hipótesis cambia la respuesta.

**Si no se sabe si la falsa pesa más o menos** (y hay que decir cuál es y de qué tipo), cada moneda son dos hipótesis, y el problema se vuelve más caro. La cota ingenua por información dice que $2n \leq 3^k$ con $k$ pesadas, es decir, $n \leq \lfloor 3^k/2 \rfloor$: 13 monedas con 3 pesadas. Pero sin moneda de referencia el máximo es **uno menos**, y en general:

$$n_{\max}(k) = \frac{3^k - 3}{2} \ \text{ sin moneda de referencia}, \qquad n_{\max}(k) = \frac{3^k - 1}{2} \ \text{ si se dispone de una moneda genuina.}$$

Es el famoso problema de las 12 monedas con 3 pesadas, y la cota por información sola no basta para explicar el 12: hay que usar la estructura de la primera pesada.

*Por qué no se puede pasar de esos valores.* Sea $G(j)$ el máximo de monedas desconocidas que se resuelven en $j$ pesadas disponiendo de genuinas de sobra. Con $j = 0$ no se resuelve ni una moneda (tiene dos hipótesis), así que $G(0) = 0$. En la primera pesada se ponen $x$ monedas a la izquierda y $y$ a la derecha.

- Si la balanza se inclina quedan $x + y$ hipótesis, cada una con su tipo ya decidido (las de un lado más pesadas, las del otro más livianas). Con $j - 1$ pesadas hay a lo sumo $3^{j-1}$ hojas, así que $x + y \leq 3^{j-1}$.
- Si equilibra, quedan $n - x - y$ monedas todavía sin información, que se resuelven en $j - 1$ pesadas: $n - x - y \leq G(j-1)$.

Luego $G(j) \leq 3^{j-1} + G(j-1)$, y por inducción $G(j) \leq (3^j - 1)/2$. Sin moneda de referencia, la primera pesada tiene que tener $x = y$. Si se inclina, quedan $2x$ hipótesis, así que $2x \leq 3^{k-1}$ y $x \leq (3^{k-1} - 1)/2$. Si equilibra, $n - 2x \leq G(k-1) \leq (3^{k-1} - 1)/2$. Sumando, $n \leq 3 \cdot (3^{k-1} - 1)/2 = (3^k - 3)/2$.

*La otra mitad* (que esas cantidades sí se alcanzan) es el resultado clásico de Dyson (1946); no se desarrolla aquí, pero se comprueba por búsqueda exhaustiva de estrategias para $k = 2$ y $k = 3$:

```python
from functools import lru_cache

@lru_cache(maxsize=None)
def factible(u, h, l, g, k):
    """¿Se pueden identificar la falsa y su tipo en k pesadas?
    u: monedas sin información (2 hipótesis cada una: más pesada o más liviana);
    h: monedas que solo pueden ser la falsa si pesa más; l: solo si pesa menos;
    g: monedas genuinas conocidas."""
    hip = 2 * u + h + l                          # hipótesis vivas
    if hip <= 1:
        return True
    if k == 0 or hip > 3 ** k:                   # cada hoja resuelve una hipótesis
        return False
    N = u + h + l + g
    for u1 in range(u + 1):
        for u2 in range(u1 + 1):                 # simetría izquierda/derecha
            if u1 + u2 > u:
                continue
            for h1 in range(h + 1):
                for h2 in range(h - h1 + 1):
                    for l1 in range(l + 1):
                        for l2 in range(l - l1 + 1):
                            izq, der = u1 + h1 + l1, u2 + h2 + l2
                            if abs(izq - der) > g or izq + der == 0:
                                continue         # no se puede equilibrar / no se pesa nada
                            ub, hb, lb = u - u1 - u2, h - h1 - h2, l - l1 - l2
                            if not factible(ub, hb, lb, N - ub - hb - lb, k - 1):       # equilibrio
                                continue
                            hp, lp = u1 + h1, u2 + l2                                   # izquierda más pesada
                            if not factible(0, hp, lp, N - hp - lp, k - 1):
                                continue
                            hp, lp = u2 + h2, u1 + l1                                   # derecha más pesada
                            if not factible(0, hp, lp, N - hp - lp, k - 1):
                                continue
                            return True
    return False

print("k  sin referencia  con 1 genuina  (3^k-3)/2  (3^k-1)/2  cota ingenua 3^k/2")
for k in (2, 3):
    a = max(n for n in range(1, 30) if factible(n, 0, 0, 0, k))
    b = max(n for n in range(1, 30) if factible(n, 0, 0, 1, k))
    assert a == (3**k - 3) // 2 and b == (3**k - 1) // 2
    print(f"{k}  {a:>14}  {b:>13}  {(3**k - 3) // 2:>9}  {(3**k - 1) // 2:>9}  {3**k // 2:>16}")
print("12 monedas en 3 pesadas:", factible(12, 0, 0, 0, 3), "| 13 sin referencia:", factible(13, 0, 0, 0, 3),
      "| 14 con una genuina:", factible(14, 0, 0, 1, 3))
```

| $k$ | Sin referencia (máximo medido) | Con una genuina (máximo medido) | $(3^k - 3)/2$ | $(3^k - 1)/2$ | Cota ingenua $\lfloor 3^k/2 \rfloor$ |
|---|---|---|---|---|---|
| 2 | 3 | 4 | 3 | 4 | 4 |
| 3 | 12 | 13 | 12 | 13 | 13 |

Con 3 pesadas, 12 monedas se resuelven, 13 sin referencia no se pueden, y 14 no se pueden ni con una moneda genuina de ayuda.

**Si el instrumento fuera otro**, la respuesta también cambia. Con una báscula que da el peso (y se sabe cuánto menos pesa la falsa), pesar un subconjunto de monedas solo dice si la falsa está en él o no: dos resultados por pesada, y la cota pasa a ser $\lceil \log_2 n \rceil$. La balanza de platillos, con sus tres resultados, es un instrumento más fuerte para este problema: es el mismo problema con otro modelo y otra respuesta, como el par más cercano con árboles de decisión y con tabla hash (conferencia 2, §10).

La regla práctica de siempre: antes de citar una cota, preguntar cuál es su modelo y qué deja fuera. Aquí el modelo es *una balanza de tres resultados con grupos iguales, una falsa más liviana*.

## 8. Cierre del ciclo

| Pregunta (conferencia 2, §1) | Respuesta |
|---|---|
| **1. ¿Cuál es el problema?** | $n$ monedas, una falsa más liviana, balanza de dos platillos con grupos de igual tamaño; hallar la falsa con el menor número de pesadas en el peor caso. Modelo: árbol de decisión ternario. |
| **2. ¿Qué algoritmo?** | Partir las candidatas en tres grupos de tamaño $\lceil m/3 \rceil$ (dos en los platillos, el resto aparte) y quedarse con el grupo que indica la balanza. |
| **3. ¿Es correcto?** | Invariante "la falsa está en $[lo, hi)$", inductivo y suficiente: los tres grupos cubren el intervalo. Terminación por el potencial $hi - lo$, que baja a $\lceil \cdot/3 \rceil$ en cada vuelta. |
| **4. ¿Cuánto cuesta?** | Exactamente $\lceil \log_3 n \rceil$ pesadas en el peor caso; $O(\log n)$ de cómputo y $O(1)$ de memoria. |
| **5. ¿Se puede hacer mejor?** | No: cualquier estrategia necesita $\geq n$ hojas en un árbol ternario, es decir, $\lceil \log_3 n \rceil$ pesadas. Coincide con el algoritmo; la cota por información es exacta, a diferencia de la búsqueda binaria. Con peso desconocido la respuesta cambia a $(3^k - 3)/2$ monedas en $k$ pesadas. |
