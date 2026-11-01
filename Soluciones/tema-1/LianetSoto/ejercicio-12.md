# Ejercicio 12 — Gale-Shapley con listas incompletas

> ★★★ Gale-Shapley con listas incompletas: cada proponente lista solo a algunos receptores, y prefiere quedarse solo antes que con uno que no listó. Adapta el algoritmo, su potencial y la definición de pareja bloqueante. ¿Sigue siendo estable el resultado? Demuéstralo. (C3)

---

## 1. El problema y su especificación

**Emparejamiento estable con listas incompletas.**

    Hay n proponentes A={a1​,…,an​} y m receptores B={b1​,…,bm​}.

    Cada proponente a tiene una lista de preferencias estricta sobre un subconjunto La​⊆B.

    Cada receptor b tiene una lista de preferencias estricta sobre un subconjunto Lb​⊆A.

    Clave: un proponente prefiere quedarse soltero antes que emparejarse con alguien que no está en su lista. Lo mismo para los receptores.

Supuesto de aceptabilidad mutua. Suponemos que las listas son mutuamente aceptables:
`b∈La  ⟺  a∈Lb`.

Si una instancia no cumple esto, se puede preprocesar en tiempo `O(∑a∣La∣+∑b∣Lb∣)` eliminando los pares no mutuos hasta que la equivalencia valga. El algoritmo y las demostraciones se aplican a la instancia preprocesada. Bajo este supuesto, `∑a∣La∣=∑b∣Lb∣`, y el algoritmo puede consultar el rango de `a` en la lista de `b` sin riesgo de error.

Emparejamiento. Un conjunto `M` de pares `(a,b)` con `a∈A`, `b∈B`, tal que:

    Cada proponente aparece en a lo sumo un par.

    Cada receptor aparece en a lo sumo un par.

    Si (a,b)∈M, entonces b∈La​ y a∈Lb​.

    A diferencia del caso clásico, M no tiene por qué ser perfecto. Usamos M(a)=b si (a,b)∈M, y M(a)=⊥ si a está soltero.

Preferencias con soltería. Para un proponente `a`:

    b≻a​b′ si ambos están en La​ y a prefiere estrictamente b a b′.

    b≻a​⊥ para todo b∈La​.

    ⊥≻a​b′ para todo b′∉La​.

Análogamente para los receptores.

Pareja bloqueante (redefinida). Un par (a,b) bloquea a `M` si:

    b∈La​ y a∈Lb​,

    (a,b)∉M

    b≻aM(a),

    a≻bM(b).


La condición 3 incluye el caso en que a está soltero: como b∈La​, se tiene b≻a​⊥. Un emparejamiento es estable si no tiene parejas bloqueantes.

---

## 2. Adaptación del algoritmo

El algoritmo de Gale-Shapley se adapta con un cambio mínimo: un proponente solo propone a los receptores de su lista. Si agota su lista sin conseguir pareja, se queda soltero y deja de proponer. Para que cada vuelta del ciclo haga exactamente una propuesta, solo volvemos a encolar a un proponente si aún le quedan receptores por proponer.

```python
from collections import deque

def gale_shapley_incompleto(pref_a, pref_b):
    """
    pref_a[a]: lista de receptores en orden de preferencia de a.
    pref_b[b]: lista de proponentes en orden de preferencia de b.
    Se asume que las listas son mutuamente aceptables:
    b in pref_a[a] si y solo si a in pref_b[b].
    Devuelve (M, propuestas), donde M[a] = b o None.
    """
    n = len(pref_a)
    m = len(pref_b)

    # Rango de a en la lista de b (para comparar preferencias de b)
    rango_b = [{} for _ in range(m)]
    for b, lista in enumerate(pref_b):
        for lugar, a in enumerate(lista):
            rango_b[b][a] = lugar

    siguiente = [0] * n       # próximo índice en la lista de cada proponente
    pareja_de_b = [None] * m
    libres = deque(a for a in range(n) if pref_a[a])  # solo los que tienen lista
    propuestas = 0

    while libres:
        a = libres.popleft()
        # Por construcción, si a está en libres, siguiente[a] < len(pref_a[a]).
        b = pref_a[a][siguiente[a]]
        siguiente[a] += 1
        propuestas += 1

        actual = pareja_de_b[b]
        if actual is None:
            pareja_de_b[b] = a
        elif rango_b[b][a] < rango_b[b][actual]:
            pareja_de_b[b] = a
            if siguiente[actual] < len(pref_a[actual]):
                libres.append(actual)
        else:
            if siguiente[a] < len(pref_a[a]):
                libres.append(a)

    M = [None] * n
    for b, a in enumerate(pareja_de_b):
        if a is not None:
            M[a] = b
    return M, propuestas
```
**Diferencias con el caso clásico**:

    Solo se encolan los proponentes que tienen al menos un receptor en su lista.

    Un proponente se vuelve a encolar solo si aún le quedan receptores por proponer. Así, cada vuelta del while hace exactamente una propuesta.

    Si un proponente agota su lista, se descarta y queda soltero.

    El resto del algoritmo es idéntico.

## 3. Traza sobre una instancia pequeña

Instancia de `n = 3` proponentes y `m = 3` receptores, con listas incompletas:

```text
Proponentes:
a1: [b1, b2]
a2: [b1, b3]
a3: [b2]

Receptores:
b1: [a2, a1]
b2: [a1, a3]
b3: [a2]
```

**Traza con estrategia de cola (FIFO)**:

| Paso | Proponente | Receptor | ¿Qué pasa? | Estado de parejas |
|---:|---|---|---|---|
| 1 | a1 | b1 | b1 libre → acepta | b1–a1 |
| 2 | a2 | b1 | b1 prefiere a2 sobre a1 → cambia; a1 queda libre | b1–a2 |
| 3 | a3 | b2 | b2 libre → acepta | b1–a2, b2–a3 |
| 4 | a1 | b2 | b2 prefiere a1 sobre a3 → cambia; a3 queda libre, pero ya agotó su lista y no se reencola| b1–a2, b2–a1 |


Después del paso 4 la cola de libres está vacía. Resultado: `M={a1​−b2​, a2​−b1​}`, y `a3`​ queda soltero.

**Comprobación de estabilidad.** Los pares posibles son `(a1,b1),(a1,b2),(a2,b1),(a2,b3),(a3,b2)`.

    (a1,b1): a1​ sí prefiere b1 a su pareja actual b2, pero b1 prefiere a a2 sobre a1. No bloquea.

    (a2,b3): b3 está soltero, pero a2 prefiere b1 a b3. No bloquea.

    (a3,b2): a3​ está soltero y prefiere b2​ a ⊥, pero b2 prefiere a a1 sobre a3. No bloquea.

    Los demás ya están emparejados.

Ningún par bloquea. El resultado es estable. ✔


## 4. Terminación: el potencial

El potencial es el mismo que en el caso clásico: el número de propuestas que aún no se han hecho.

Potencial `Φ`: número de pares `(a,b)` con `b∈La`​ y `a` aún no le ha propuesto a `b`. Inicialmente `Φ0​=∑a​∣La​∣`.

Propiedades:

    Φ≥0 siempre.

    Cada vuelta del ciclo hace exactamente una propuesta, porque solo encolamos a quien aún tiene propuestas pendientes. Esa propuesta no se repite porque siguiente[a] solo avanza. Por tanto, Φ baja en 1 en cada vuelta.

    El ciclo termina después de a lo sumo ∑a​∣La​∣ propuestas. ✔

Además, `siguiente[a]` nunca se sale de la lista porque solo encolamos a `a` cuando `siguiente[a] < len(pref_a[a])`.

**Conclusión:** el algoritmo termina para toda entrada válida. ✔


## 5. Correctitud: el resultado es estable

**Teorema.** El emparejamiento devuelto por Gale-Shapley con listas incompletas es estable, para cualquier orden de ejecución.

**Demostración.**

Primero, `M` es un emparejamiento válido. Invariante del algoritmo: cada receptor tiene a lo sumo un proponente en `pareja_de_b`; cada proponente aparece en a lo sumo una entrada de `pareja_de_b` (cuando `a` es aceptado estaba libre, y si desplaza a `a′`, la entrada de `a′` se sobrescribe); y todo par de `M` satisface `b∈La`​ y `a∈Lb` por el supuesto de aceptabilidad mutua. Por tanto, `M` es un emparejamiento válido.

Ahora, por contradicción. Sea `M` el resultado y supongamos que existe una pareja bloqueante `(a,b)`:

    b∈La​ y a∈Lb,

    (a,b)∉M,

    b≻aM(a) (o a está soltero),

    a≻bM(b) (o b está soltero).

Como `b∈La`​, el proponente `a` le propuso a `b` en algún momento (porque agotó su lista o se quedó con `M(a)∈La​`, y propone en orden decreciente). Como `b≻aM(a)`, le propuso a `b` antes que a `M(a)`.

En ese momento `b` lo rechazó (o lo aceptó y luego lo cambió). Es decir, en algún momento `b` prefirió a otra persona `a'` sobre `a`, por lo que `a' ≻_b a`.

Por el invariante del receptor (una vez que un receptor tiene pareja, su pareja solo mejora desde su punto de vista, porque solo cambia de pareja cuando recibe una propuesta de alguien a quien prefiere), sabemos que al final `b` tiene a `M(b)`, que es igual a `a'` o alguien a quien prefiere sobre `a'`. En cualquier caso, se cumple que `M(b) ≻_b a`'.

Como `a' ≻_b a`, por transitividad se tiene que `M(b) ≻_b a`. Pero esto contradice la hipótesis de que `a ≻_b M(b)`.

Contradicción. Por tanto, no existe pareja bloqueante. ∎

El argumento es idéntico al del caso clásico. La única diferencia es que `M(a)` puede ser `⊥`, pero `b≻a​M(a)` sigue siendo válido porque b∈La​ y `b≻a⊥`.

## 6. Optimalidad para quien propone

En el caso clásico, Gale-Shapley le da a cada proponente su mejor pareja válida. 

**Definición**. Un receptor `b` es pareja válida de un proponente `a` si existe algún emparejamiento estable en el que están juntos. Además, la soltería es una opción válida para `a` si existe un emparejamiento estable en el que `a` queda soltero. Definimos `mejor(a)` como la mejor opción entre todas las parejas válidas y la soltería (donde cualquier pareja válida es mejor que la soltería, por definición de La​).

**Teorema**. Toda ejecución de Gale-Shapley con listas incompletas empareja a cada proponente `a` con `mejor(a)`.

**Demostración**. Por el primer fallo. Como `a` propone en orden decreciente, basta ver que ningún proponente es rechazado por una pareja válida. Si eso es cierto, `a` llega hasta su mejor pareja válida y ahí se queda; si no tiene pareja válida, agota su lista y queda soltero, que es exactamente `mejor(a)=⊥`.

Supongamos que en alguna ejecución algún proponente es rechazado por una pareja válida, y tomemos el primer rechazo de ese tipo. Digamos que `b` rechaza a `a` porque tiene o recibe a `a′`, a quien prefiere. Sea `M′` un emparejamiento estable con `(a,b)∈M′`.

Si `a′` está soltero en `M′`, entonces `(a′,b)` bloquea `M′`: `a′` prefiere `b` a la soltería porque `b∈La′`​, y `b` prefiere `a′` a `a=M′(b)`. Contradicción. Luego `a′` está emparejado en `M′` con algún `b′≠b`.

Como `a′` le propuso a `b`, antes le propuso a todos los receptores que prefiere a `b`. Esos rechazos son anteriores al primero hecho por una pareja válida, así que ninguno de esos receptores es pareja válida de `a′`. Pero `b′` sí es pareja válida de `a′`, porque `(a′,b′)∈M′`. Por tanto `b′` no está entre los receptores que `a′` prefiere a `b`; como `b′≠b`, se tiene que `a′` prefiere `b` a `b′`.

Además `b` prefiere `a′` a `a`. Entonces `(a′,b)` bloquea `M′`, contradicción con que `M′` era estable.

Por tanto, ningún proponente es rechazado por una pareja válida. Como `a` propone en orden decreciente, llega hasta su mejor pareja válida y se queda con ella. Si no tiene pareja válida, agota su lista y queda soltero, que es exactamente `mejor(a)=⊥`. ∎

## 7. Complejidad

    Tiempo: O(∑a∣La∣) propuestas, y cada propuesta cuesta O(1) (comparación de rangos). Total: O(∑a​∣La​∣), lineal en el tamaño de las listas.

    Memoria: O(n+m+∑a​∣La​∣) para guardar las listas y los rangos. Bajo aceptabilidad mutua, ∑a​∣La​∣=∑b​∣Lb​∣, así que la cota también se puede escribir O(n+m+∑b​∣Lb​∣).

## 8. Verificación experimental
### 8.1. Generador de instancias
```python
import random

def instancia_incompleta(n, m, prob, rng):
    """Genera listas mutuamente aceptables: cada par (a,b) se incluye con probabilidad prob."""
    pref_a = []
    for a in range(n):
        lista = [b for b in range(m) if rng.random() < prob]
        rng.shuffle(lista)
        pref_a.append(lista)
    pref_b = []
    for b in range(m):
        # Solo incluir a 'a' en la lista de 'b' si 'b' está en la lista de 'a'
        lista = [a for a in range(n) if b in pref_a[a]]
        rng.shuffle(lista)
        pref_b.append(lista)
    return pref_a, pref_b
```

### 8.2. Verificador de estabilidad (fuerza bruta)
```python
def es_estable(M, pref_a, pref_b):
    """M[a] = b o None. Verifica que no haya parejas bloqueantes.
       Asume listas mutuamente aceptables."""
    pareja_de_b = {b: a for a, b in enumerate(M) if b is not None}
    n, m = len(pref_a), len(pref_b)
    for a in range(n):
        for b in pref_a[a]:
            if M[a] == b:
                continue
            # ¿a prefiere b a su pareja actual?
            if M[a] is None or pref_a[a].index(b) < pref_a[a].index(M[a]):
                # ¿b prefiere a a su pareja actual?
                if b not in pareja_de_b:
                    return False  # b está soltero y a lo prefiere → bloquea
                actual = pareja_de_b[b]
                if pref_b[b].index(a) < pref_b[b].index(actual):
                    return False
    return True
```

### 8.3. Prueba de estabilidad con instancias aleatorias
```python
rng = random.Random(2026)
fallos = 0
casos = 0

for _ in range(2000):
    n = rng.randint(1, 6)
    m = rng.randint(1, 6)
    prob = rng.uniform(0.3, 0.9)
    pref_a, pref_b = instancia_incompleta(n, m, prob, rng)
    M, _ = gale_shapley_incompleto(pref_a, pref_b)
    if not es_estable(M, pref_a, pref_b):
        fallos += 1
    casos += 1

print(f"{casos} instancias, fallos de estabilidad: {fallos}")
```
Salida esperada:
```text
2000 instancias, fallos de estabilidad: 0
```

### 8.4. Pruebas exhaustivas en instancias pequeñas

Para `n,m≤4`, enumeramos todos los emparejamientos válidos, calculamos todos los estables por fuerza bruta, y comprobamos que la salida de Gale-Shapley es estable y coincide con el proponente-óptimo.

```python
def todos_los_emparejamientos(pref_a, pref_b):
    n = len(pref_a)
    res = []
    def backtrack(a, usado, M):
        if a == n:
            res.append(M[:])
            return
        # opción: a queda soltero
        M.append(None)
        backtrack(a + 1, usado, M)
        M.pop()
        # opción: a emparejado con b
        for b in pref_a[a]:
            if b not in usado:
                M.append(b)
                usado.add(b)
                backtrack(a + 1, usado, M)
                usado.remove(b)
                M.pop()
    backtrack(0, set(), [])
    return res

def todos_los_estables(pref_a, pref_b):
    return [
        M for M in todos_los_emparejamientos(pref_a, pref_b)
        if es_estable(M, pref_a, pref_b)
    ]

def mejor_opcion(a, estables, pref_a):
    opciones = [M[a] for M in estables if M[a] is not None]
    if not opciones:
        return None
    return min(opciones, key=lambda b: pref_a[a].index(b))
```
Bucle de prueba:

```python
rng = random.Random(2026)
fallos_estabilidad = 0
fallos_optimalidad = 0
casos = 0

for _ in range(500):
    n = rng.randint(1, 4)
    m = rng.randint(1, 4)
    prob = rng.uniform(0.3, 0.9)
    pref_a, pref_b = instancia_incompleta(n, m, prob, rng)
    M, _ = gale_shapley_incompleto(pref_a, pref_b)
    estables = todos_los_estables(pref_a, pref_b)

    if not es_estable(M, pref_a, pref_b):
        fallos_estabilidad += 1

    for a in range(n):
        if M[a] != mejor_opcion(a, estables, pref_a):
            fallos_optimalidad += 1
            break

    casos += 1

print(f"{casos} instancias pequeñas")
print(f"fallos de estabilidad: {fallos_estabilidad}")
print(f"fallos de optimalidad: {fallos_optimalidad}")
```

Salida esperada:

```python
500 instancias pequeñas 
fallos de estabilidad: 0
fallos de optimalidad: 0
```
### 8.5. Prueba con listas asimétricas

Para ilustrar el preprocesamiento, incluimos una función que elimina los pares no mutuos iterando hasta que la equivalencia valga, y probamos con un caso asimétrico.

```python
def preprocesar(pref_a, pref_b):
    """Elimina pares no mutuos hasta que b in L_a <=> a in L_b."""
    n, m = len(pref_a), len(pref_b)
    set_a = [set(pref_a[a]) for a in range(n)]
    set_b = [set(pref_b[b]) for b in range(m)]
    # iterar hasta punto fijo
    cambiado = True
    while cambiado:
        cambiado = False
        for a in range(n):
            for b in list(set_a[a]):
                if a not in set_b[b]:
                    set_a[a].remove(b)
                    cambiado = True
        for b in range(m):
            for a in list(set_b[b]):
                if b not in set_a[a]:
                    set_b[b].remove(a)
                    cambiado = True
    pref_a = [sorted(set_a[a], key=lambda b: pref_a[a].index(b)) for a in range(n)]
    pref_b = [sorted(set_b[b], key=lambda a: pref_b[b].index(a)) for b in range(m)]
    return pref_a, pref_b
```
Caso asimétrico:

```python
pref_a = [[0], [0]]
pref_b = [[1]]  # b0 no lista a a0, aunque a0 lista a b0

pref_a2, pref_b2 = preprocesar(pref_a, pref_b)
print("pref_a2 =", pref_a2)
print("pref_b2 =", pref_b2)

assert pref_a2 == [[], [0]], f"Esperaba [[], [0]], obtuve {pref_a2}"
assert pref_b2 == [[1]], f"Esperaba [[1]], obtuve {pref_b2}"
```
Salida esperada:
```text
pref_a2 = [[], [0]]
pref_b2 = [[1]]
```
Ahora ejecutamos Gale-Shapley sobre la instancia preprocesada:
```python
M, propuestas = gale_shapley_incompleto(pref_a2, pref_b2)
print("M =", M)
print("propuestas =", propuestas)

assert M == [None, 0], f"Esperaba [None, 0], obtuve {M}"
assert propuestas == 1, f"Esperaba 1 propuesta, obtuve {propuestas}"
```
Salida esperada:
```text
M = [None, 0]
propuestas = 1
```
**Interpretación:**

    a0 se queda soltero porque, tras eliminar el par no mutuo (a0, b0), su lista queda vacía.

    a1 le propone a b0, que está libre, y se emparejan.

    Solo se hace una propuesta.

    El resultado M = [None, 0] es estable (no hay parejas bloqueantes).

Con esto se comprueba que el preprocesamiento elimina correctamente los pares no mutuos y que el algoritmo funciona sin problemas sobre la instancia resultante.

### 8.6. Casos límite

    Todos los La​ vacíos: todos solteros.

    Un solo par aceptable.

    n ≠ m.

    Un proponente con lista no vacía pero ningún par mutuo.


### 9. Ejemplo de pareja bloqueante con listas incompletas

Para ilustrar la nueva definición, construimos una instancia donde un par que no está en las listas de ambos no bloquea, pero un par que sí está y ambos prefieren al otro, sí bloquea.

```text
a1: [b2]
a2: [b1]
b1: [a2]
b2: [a1]
```
El emparejamiento `M = {a1–b2, a2–b1}` es estable. El par `(a1, b1)` no bloquea porque `b1 ∉ L_{a1}` (a1 no listó a b1) y `a1 ∉ L_{b1}`.

Si cambiamos las listas:
```text
a1: [b1, b2]
a2: [b1]
b1: [a1, a2]
b2: [a1]
```
Gale-Shapley devuelve `{a1–b1, a2 soltero}`. ¿Hay pareja bloqueante?

    (a1, b2): a1 prefiere b1 a b2 (b1 está primero). No bloquea.

    (a2, b1): b1 prefiere a1 a a2. No bloquea.

Estable. ✔