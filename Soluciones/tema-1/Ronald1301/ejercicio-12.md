# Ejercicio 12 — Gale-Shapley con listas incompletas

**Uso de IA:** Se usó IA para preparar y revisar este borrador, generar código y casos
de prueba, y apoyar la depuración. Parte de la explicación matemática también recibió
asistencia de IA; esas partes todavía no son redacción propia. Antes de entregar,
reescribiré y verificaré por mi cuenta las demostraciones, análisis de costo y cotas,
según la regla del curso.


> **Enunciado.** Gale-Shapley con listas incompletas: cada proponente lista solo a
> algunos receptores, y prefiere quedarse solo antes que con uno que no listó. Adapta el
> algoritmo, su potencial y la definición de pareja bloqueante. ¿Sigue siendo estable el
> resultado? Demuéstralo.

---

## 1. El modelo, modificado

En el emparejamiento estable clásico (C3, §6) cada lado tiene una preferencia **estricta
y completa** sobre todo el otro lado, y el resultado es un emparejamiento **perfecto**.
Ahora relajamos "completa":

- Cada proponente $a$ tiene una lista estricta $L(a)$ de un **subconjunto** de
  receptores: los que **acepta**. Prefiere **quedarse solo** ($\varnothing$) antes que
  emparejarse con un receptor fuera de $L(a)$.
- Simétricamente, cada receptor $b$ tiene una lista $L(b)$ de proponentes que acepta, y
  prefiere estar solo antes que con alguien fuera de $L(b)$.
- Un par $(a,b)$ es **mutuamente aceptable** si $b\in L(a)$ **y** $a\in L(b)$.

El resultado ya **no tiene por qué ser perfecto**: algunos quedan solos. Buscamos un
emparejamiento (parcial) **estable** en el sentido que definimos abajo.

> Este es el modelo real de la asignación de residencias médicas (C3, §6): un hospital
> no está dispuesto a aceptar a cualquiera, ni un graduado a ir a cualquier plaza.

---

## 2. Pareja bloqueante, adaptada

Con listas completas, $(a,b)$ bloquea si ambos se prefieren mutuamente a sus parejas
(C3, §6). Con listas incompletas hay que exigir **aceptabilidad mutua** y permitir que
"estar solo" sea una pareja a la que se puede mejorar. Sea $M$ un emparejamiento donde
$M(a)$ es la pareja de $a$ o $\varnothing$ si está solo.

**Definición (pareja bloqueante con listas incompletas).** $(a,b)$ bloquea a $M$ si:
1. $(a,b)$ es **mutuamente aceptable** ($b\in L(a)$ y $a\in L(b)$);
2. $a$ prefiere $b$ a $M(a)$ —y "prefiere $b$ a estar solo" cuenta, porque $b\in L(a)$;
3. $b$ prefiere $a$ a $M(b)$ —igual, "prefiere $a$ a estar solo" cuenta.

Hay que añadir dos condiciones de **individual-racionalidad**, que con listas completas
eran gratis:
- ningún $a$ está emparejado con un $b\notin L(a)$ (preferiría estar solo);
- ningún $b$ está emparejado con un $a\notin L(b)$.

$M$ es **estable** si es individualmente racional y no tiene parejas bloqueantes.

~~~
a prefiere:  ...  b  ...  M(a)  ...  solo
                      └─ mejora ─┘

b prefiere:  ...  a  ...  M(b)  ...  solo
                      └─ mejora ─┘

(a,b) bloquea si ambos lo aceptan y ambos lo prefieren a su situación actual.
~~~

---

## 3. El algoritmo, adaptado

El cambio es mínimo respecto del de C3, §7: un proponente recorre **solo su lista
$L(a)$**; si la agota sin quedar emparejado, **se queda solo** (no es un error, como sí
lo era en el caso completo). Un receptor solo acepta propuestas de proponentes que están
en **su** lista; una propuesta de alguien fuera de $L(b)$ se rechaza de inmediato.

```python
from collections import deque

def gale_shapley_incompleto(L_a, L_b):
    """
    L_a[a] = lista estricta de receptores que a acepta, de mejor a peor.
    L_b[b] = lista estricta de proponentes que b acepta, de mejor a peor.
    Devuelve (pareja_de_a, propuestas): pareja_de_a[a] = b o None.
    """
    n_a, n_b = len(L_a), len(L_b)
    # rango[b][a] = lugar de a en la lista de b; +inf si b no acepta a a.
    rango = [dict() for _ in range(n_b)]
    for b in range(n_b):
        for lugar, a in enumerate(L_b[b]):
            rango[b][a] = lugar
    siguiente = [0] * n_a            # próximo índice de L_a[a] al que a propondrá
    pareja_de_b = [None] * n_b
    libres = deque(range(n_a))       # proponentes que aún pueden proponer
    propuestas = 0

    while libres:
        a = libres.popleft()
        if siguiente[a] == len(L_a[a]):
            continue                 # a agotó su lista: se queda solo, no vuelve
        b = L_a[a][siguiente[a]]
        siguiente[a] += 1
        propuestas += 1
        if a not in rango[b]:        # b no acepta a a: rechazo inmediato
            libres.append(a)         # a sigue libre, probará el siguiente de su lista
            continue
        actual = pareja_de_b[b]
        if actual is None:
            pareja_de_b[b] = a
        elif rango[b][a] < rango[b][actual]:
            pareja_de_b[b] = a
            libres.append(actual)    # el anterior vuelve a estar libre
        else:
            libres.append(a)         # b prefiere a su pareja; a sigue libre

    pareja_de_a = [None] * n_a
    for b, a in enumerate(pareja_de_b):
        if a is not None:
            pareja_de_a[a] = b
    return pareja_de_a, propuestas
```

### Una instancia donde alguien queda solo

```python
if __name__ == "__main__":
    # 3 proponentes, 3 receptores, listas incompletas.
    # a0 solo acepta b0; a1 acepta b0>b1; a2 acepta b1.
    # b0 acepta a1>a0; b1 acepta a1>a2; b2 no acepta a nadie (y nadie lo lista).
    L_a = [[0], [0, 1], [1]]
    L_b = [[1, 0], [1, 2], []]
    M, k = gale_shapley_incompleto(L_a, L_b)
    nombre = lambda s, i: f"{s}{i}" if i is not None else "solo"
    for a in range(len(L_a)):
        print(f"a{a} -> {nombre('b', M[a])}")
    print(f"propuestas: {k}")
```

```
a0 -> solo
a1 -> b0
a2 -> b1
propuestas: 3
```

Traza: $a_0$ propone a $b_0$ (libre, acepta). $a_1$ propone a $b_0$; $b_0$ prefiere
$a_1$ a $a_0$, lo cambia, $a_0$ queda libre. $a_2$ propone a $b_1$ (acepta). $a_0$
vuelve a `libres`, pero su lista era solo $[b_0]$ y ya está agotada
(`siguiente[a0] == len(L_a[a0])`): el `continue` lo retira **sin gastar una propuesta**,
y **$a_0$ se queda solo**. Total: 3 propuestas. $b_2$ no aparece: nadie lo acepta y él
no acepta a nadie. El resultado es estable.

---

## 4. El potencial (terminación)

El potencial de C3, §7 era $\Phi=$ número de pares $(a,b)$ a los que $a$ aún no ha
propuesto, con $\Phi=n^2$ al inicio. Con listas incompletas se adapta al **total de
entradas de las listas de los proponentes**:
$$\Phi \;=\; \sum_{a}\big(|L(a)| - \mathtt{siguiente}[a]\big)
\;=\; \#\{(a,b): b\in L(a),\ a\ \text{aún no propuso a } b\}.$$

- **Al inicio:** $\Phi = \sum_a |L(a)| \le n_a\, n_b$.
- **Cada propuesta** incrementa algún `siguiente[a]` en 1 y nunca se deshace (un
  proponente nunca repite una propuesta: `siguiente[a]` solo avanza). Luego **cada
  vuelta del ciclo que hace una propuesta baja $\Phi$ en exactamente 1.**
- $\Phi \ge 0$ siempre.

Por tanto el algoritmo hace a lo sumo $\sum_a|L(a)| = O(n_a n_b)$ propuestas y
**termina**. Es el mismo argumento de monotonía de C3, §7 ("una cantidad que se mueve en
una sola dirección"), con el tope cambiado de $n^2$ al tamaño total de las listas. Las
vueltas en que $a$ ya agotó su lista (el `continue` inicial) no cuestan propuesta y solo
retiran a $a$ de `libres`, así que no afectan la cota.

Los **dos invariantes de una línea** de C3, §7 siguen valiendo y se leen igual en el
código:
- *Un receptor, una vez comprometido, no vuelve a quedar solo, y su pareja solo mejora*
  (solo cambia por alguien que prefiere más, y nunca vuelve a `None`).
- *Un proponente propone en orden decreciente de su lista*, así que sus parejas solo
  empeoran, hasta posiblemente quedarse solo al agotar $L(a)$.

---

## 5. El resultado es estable — demostración

**Teorema.** El emparejamiento $M$ que devuelve Gale-Shapley con listas incompletas es
estable (individualmente racional y sin parejas bloqueantes), para cualquier orden de
ejecución.

*Demostración.*

**(a) Individual-racionalidad.** Un proponente $a$ solo propone a receptores de $L(a)$,
así que si $M(a)=b$ entonces $b\in L(a)$. Un receptor $b$ solo acepta propuestas de
proponentes de $L(b)$ (el `continue` cuando `a not in rango[b]`), así que si $M(b)=a$
entonces $a\in L(b)$. Nadie termina con una pareja inaceptable; quien no consigue pareja
aceptable queda solo, que prefiere. $\square$(a)

**(b) Sin parejas bloqueantes.** Por contradicción, igual que en C3, §8. Supongamos que
$(a,b)$ bloquea: es mutuamente aceptable, $a$ prefiere $b$ a $M(a)$ y $b$ prefiere $a$ a
$M(b)$.

Como $a$ prefiere $b$ a $M(a)$ y $b\in L(a)$, el receptor $b$ está **antes** que $M(a)$
en la lista de $a$ (o $a$ está solo, y $b$ está en su lista en cualquier posición). En
ambos casos, como $a$ propone en orden decreciente por $L(a)$ y terminó en $M(a)$ o
solo, **$a$ le propuso a $b$ en algún momento** (antes de llegar a $M(a)$, o antes de
agotar la lista).

Cuando $a$ le propuso a $b$: como $(a,b)$ es mutuamente aceptable, $a\in L(b)$, así que
$b$ **no** rechazó a $a$ por inaceptable. Entonces $b$ o bien aceptó a $a$, o ya tenía a
alguien que prefería. En cualquier caso, **desde ese momento la pareja de $b$ solo
mejora** (primer invariante), y $b$ nunca vuelve a quedar solo. Por tanto $M(b)$ es un
proponente que $b$ prefiere a $a$ (o igual a $a$, imposible pues $(a,b)\notin M$).

Esto contradice que $b$ prefiera $a$ a $M(b)$. Luego no hay pareja bloqueante.
$\square$(b)

Por (a) y (b), $M$ es estable. $\blacksquare$

El argumento es **exactamente** el del caso completo (C3, §8: "$a$ propone en orden
decreciente, le propuso a $b$ antes que a su pareja; $b$ lo rechazó por alguien mejor; la
pareja de $b$ solo mejora"), con dos añadidos que las listas incompletas obligan:
la cláusula de aceptabilidad mutua (para que $b$ no rechazara a $a$ por inaceptable) y
tratar "estar solo" como el peor lugar de la lista, siempre mejorable.

---

## 6. Verificación empírica

Comprobamos sobre muchas instancias aleatorias con listas incompletas que la salida es
siempre individualmente racional y sin parejas bloqueantes (fuerza bruta sobre todos los
pares mutuamente aceptables).

```python
if __name__ == "__main__":
    import random

    def listas_aleatorias(n, p, semilla):
        r = random.Random(semilla)
        L_a = [[b for b in r.sample(range(n), n) if r.random() < p] for _ in range(n)]
        L_b = [[a for a in r.sample(range(n), n) if r.random() < p] for _ in range(n)]
        return L_a, L_b

    def es_estable(L_a, L_b, M):
        pareja_b = {}
        for a, b in enumerate(M):
            if b is not None:
                pareja_b[b] = a
        pos_a = [{b: i for i, b in enumerate(L_a[a])} for a in range(len(L_a))]
        pos_b = [{a: i for i, a in enumerate(L_b[b])} for b in range(len(L_b))]
        # individual-racionalidad
        for a, b in enumerate(M):
            if b is not None and (b not in pos_a[a] or a not in pos_b[b]):
                return False
        # sin bloqueantes: para todo par mutuamente aceptable
        for a in range(len(L_a)):
            for b in pos_a[a]:
                if a not in pos_b[b]:
                    continue
                a_mejora = (M[a] is None) or (pos_a[a][b] < pos_a[a][M[a]])
                bp = pareja_b.get(b)
                b_mejora = (bp is None) or (pos_b[b][a] < pos_b[b][bp])
                if a_mejora and b_mejora:
                    return False
        return True

    fallos = 0
    for s in range(3000):
        L_a, L_b = listas_aleatorias(6, 0.6, s)
        M, _ = gale_shapley_incompleto(L_a, L_b)
        if not es_estable(L_a, L_b, M):
            fallos += 1
    print(f"instancias probadas: 3000, inestables: {fallos}")
```

```
instancias probadas: 3000, inestables: 0
```

El experimento propone y la demostración decide (Tema 1, idea 3): 0 fallos en 3000
instancias es consistente con el teorema, no lo reemplaza.

---

## 7. Resumen

- **Modelo:** listas incompletas; "estar solo" es preferible a una pareja inaceptable;
  el resultado puede ser un emparejamiento parcial.
- **Pareja bloqueante:** se añade la exigencia de **aceptabilidad mutua** y se trata
  $\varnothing$ como el peor lugar de la lista; además se pide individual-racionalidad.
- **Algoritmo:** idéntico a C3 §7, salvo que cada proponente recorre solo su lista y
  puede quedarse solo, y cada receptor rechaza de plano a los inaceptables.
- **Potencial:** $\Phi=\sum_a(|L(a)|-\mathtt{siguiente}[a])\le n_a n_b$ baja en 1 por
  propuesta y es $\ge 0$ ⇒ termina en $O(n_a n_b)$ propuestas.
- **Estabilidad:** sí, por el mismo argumento de primer-fallo / monotonía de C3 §8, con
  los dos añadidos que imponen las listas incompletas.
