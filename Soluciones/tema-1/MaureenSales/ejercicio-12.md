# Ejercicio 12 — Gale-Shapley con listas incompletas

**Tema 1 · Diseño y Análisis de Algoritmos · MatCom 2026**
Conferencias que usa: **C3** (el error que la demostración anuncia, el problema y la pareja bloqueante, el algoritmo, sus dos invariantes y el potencial, estabilidad, optimalidad por el primer fallo, costo) · Dificultad: ★★★

---

## Enunciado

> Gale-Shapley con listas incompletas: cada proponente lista solo a algunos receptores, y prefiere quedarse solo antes que con uno que no listó. Adapta el algoritmo, su potencial y la definición de pareja bloqueante. ¿Sigue siendo estable el resultado? Demuéstralo.

---

## 1. Modelo

- Proponentes $P$ y receptores $R$ (no hace falta que $|P| = |R|$).
- Cada $p \in P$ tiene una lista ordenada $L_p \subseteq R$: los receptores que acepta, del preferido al menos preferido. Prefiere cualquiera de su lista antes que quedarse solo, y quedarse solo antes que cualquiera que no esté en su lista. **Esta es la única lista incompleta.**
- Cada $r \in R$ tiene, como en C3, una lista estricta y **completa** de todos los proponentes. En particular, un receptor acepta a cualquier proponente antes que quedarse solo.

Un **emparejamiento** $M$ es un conjunto de pares $(p, r)$ con $r \in L_p$, disjuntos (cada agente en a lo sumo un par). Los agentes que no están en ningún par están **solos**. Escribo $M(a)$ para la pareja de $a$, o $\varnothing$ si está solo.

Exigir $r \in L_p$ en cada par es la "racionalidad individual" del lado de los proponentes: nadie queda con alguien que no listó, porque preferiría romper el par y quedarse solo. Del lado de los receptores no hace falta exigir nada, porque aceptan a todos.

## 2. Pareja bloqueante, adaptada

> **Definición.** $(p, r)$ **bloquea** a $M$ si:
> 1. $r \in L_p$,
> 2. $(p, r) \notin M$,
> 3. $p$ está solo, o prefiere $r$ a $M(p)$, y
> 4. $r$ está solo, o prefiere $p$ a $M(r)$.
>
> $M$ es **estable** si ningún par lo bloquea.

Comparación con la de C3 ("$M$ es inestable si hay un proponente $a$ y un receptor $b$, no emparejados entre sí, tales que $a$ prefiere $b$ a su pareja en $M$, y $b$ prefiere $a$ a su pareja en $M$"):

| | listas completas (C3) | listas incompletas |
|---|---|---|
| quién puede bloquear | cualquier par | solo $(p, r)$ con $r \in L_p$ (cond. 1) |
| "está solo" | no pasa: el emparejamiento es perfecto | pasa, por los dos lados (cond. 3 y 4) |
| emparejamiento válido | perfecto | cada par respeta la lista del proponente |

La condición 1 es la traducción de "prefiere quedarse solo antes que con uno que no listó": si $r \notin L_p$, a $p$ no le conviene irse con $r$, esté como esté, así que $(p, r)$ no puede bloquear. Las condiciones 3 y 4 son las de C3 con un caso más, el de estar solo. Para un receptor, estar solo es peor que cualquier proponente (su lista es completa); para un proponente, es peor que cualquiera de su lista.

## 3. Algoritmo adaptado

```python
from collections import deque

def gale_shapley_incompleto(Lp, Lr):
    """Lp[p] = receptores que p acepta, del preferido al menos preferido (lista incompleta).
    Lr[r] = todos los proponentes, en el orden de preferencia de r (lista completa).
    Devuelve (pareja de cada proponente o None, número de propuestas)."""
    rango = {r: {p: k for k, p in enumerate(Lr[r])} for r in Lr}   # menor = mejor
    siguiente = {p: 0 for p in Lp}          # próximo índice de su lista a proponer
    pareja_r = {r: None for r in Lr}
    libres = deque(Lp)
    propuestas = 0
    while libres:
        p = libres.popleft()
        if siguiente[p] == len(Lp[p]):       # se le acabó la lista: se rinde y queda solo
            continue
        r = Lp[p][siguiente[p]]
        siguiente[p] += 1
        propuestas += 1
        if pareja_r[r] is None:              # r estaba sola: acepta
            pareja_r[r] = p
        elif rango[r][p] < rango[r][pareja_r[r]]:   # r prefiere a p: cambia
            libres.append(pareja_r[r])
            pareja_r[r] = p
        else:                                # r prefiere a su pareja actual
            libres.append(p)
    pareja_p = {p: None for p in Lp}
    for r, p in pareja_r.items():
        if p is not None:
            pareja_p[p] = r
    return pareja_p, propuestas
```

Es la aceptación diferida de C3 ("mientras haya un proponente libre, ese proponente le propone al mejor receptor de su lista al que todavía no le ha propuesto"), con la tabla `rango` de C3 para comparar pretendientes en $O(1)$. El **único cambio** respecto al de C3 es la línea comentada con "se le acabó la lista". Los receptores no cambian nada: como su lista es completa, toda propuesta que reciben es de alguien que tienen ordenado. Como el de C3, es **no determinista** en la elección del proponente libre (aquí, la cola), y todo lo que se demuestre abajo vale para cualquier elección.


![Ilustración](svgviewer-emparejamiento.png)
```
  ¿(C, Z) bloquea?  No: Z no está en la lista de C (cond. 1).
  ¿(C, Y) bloquea?  C está solo y quiere a Y, pero Y prefiere A a C.  No.
  ¿(A, X) bloquea?  A prefiere X a Y, pero X prefiere B a A.  No.
```

Fíjate en C: no se rinde al principio, sino **después** de que lo desplazan. Tuvo pareja, la perdió, y ya no le queda nadie en la lista. Y Z queda sola aunque ordena a todos: nadie la listó, así que nadie le propuso.

## 4. Terminación: el potencial

En C3 el potencial es "el número de pares $(a, b)$ tales que $a$ todavía no le ha propuesto a $b$", que empieza en $n^2$ y baja 1 por propuesta. Con listas incompletas solo cuentan los pares de las listas de los proponentes:

> **Potencial.** $\Phi = \sum_{p \in P} \big(|L_p| - \text{siguiente}[p]\big)$ = cantidad total de propuestas que todavía se pueden hacer.

- Empieza en $\Phi_0 = \sum_p |L_p| \le |P|\cdot|R|$, y siempre $\Phi \ge 0$.
- Cada vuelta del `while` hace una de dos cosas:
  - una propuesta, que nunca se repite porque `siguiente[p]` solo avanza, y $\Phi$ baja exactamente 1;
  - una **rendición**: saca de `libres` a un proponente con la lista agotada. Ese proponente no vuelve nunca a `libres`, porque a `libres` solo entra alguien rechazado o reemplazado, y quien se rinde no tiene pareja que perder ni vuelve a proponer.

Así que hay a lo sumo $\Phi_0$ propuestas y a lo sumo $|P|$ rendiciones: el algoritmo termina después de a lo sumo $\sum_p |L_p| + |P|$ vueltas. En el ejemplo, $\Phi_0 = 4$: 4 propuestas y 1 rendición. Con listas completas y $|P| = |R| = n$ nadie se rinde (ver abajo) y queda el $n^2$ de C3.

Si se quiere una sola cantidad que baje en **cada** vuelta, como el potencial de C3, sirve $\Psi = \Phi + |\text{libres}|$. Una propuesta baja $\Phi$ en 1 y no hace crecer `libres` (el que propone sale, y vuelve a entrar a lo sumo uno: él mismo o la pareja que reemplazaron). Una rendición deja $\Phi$ igual y baja `libres` en 1. $\Psi$ es un entero que nunca es negativo y empieza en $\sum_p |L_p| + |P|$, así que esa es la cantidad máxima de vueltas.

**Lo que se rompe de C3.** Allí, después del potencial, había que demostrar que `siguiente[a]` nunca se sale de la lista ("termina con un emparejamiento perfecto"), contando que $n$ receptores comprometidos necesitan $n$ proponentes. Aquí ese lema es **falso**: en el ejemplo, C agota su lista. Por eso hace falta la línea nueva; sin ella, el algoritmo de C3 lee `Lp["C"][1]`, que no existe, y se cae (lo comprueba la sección 7). La rendición reemplaza al lema, y su lugar en la demostración de estabilidad lo ocupa el invariante (I4) de abajo.

**El arreglo que no termina.** Otro arreglo que parece razonable es "si se le acaba la lista, que vuelva a empezar". Es peor: `siguiente[p]` deja de avanzar en un solo sentido, el potencial deja de bajar y el algoritmo no termina. Quien agotó la lista fue rechazado por todos los de su lista, que desde entonces solo mejoran (I1), así que lo rechazan otra vez, y otra, para siempre. Es la lección de la reparación local de C3: sin algo que avance en un solo sentido, no hay garantía de terminar.

## 5. Correctitud: el resultado es estable

**Especificación (C3).**

- **Precondición.** Cada $L_p$ es una lista sin repetidos de receptores, y cada $L_r$ es un orden estricto de **todos** los proponentes.
- **Postcondición.** El resultado es un emparejamiento válido (cada par $(p, r)$ cumple $r \in L_p$, y nadie está en dos pares) y estable en el sentido de la sección 2.

**Invariantes.** Valen antes de cada vuelta del `while`. (I1) e (I2) son los dos "invariantes de una línea" de C3, cuya "demostración es leer el código"; (I3) es nuevo.

- **(I1) Los receptores solo mejoran.** Una vez que $r$ tiene pareja, nunca vuelve a estar sola, y cada cambio de pareja es a alguien que prefiere.
- **(I2) Los proponentes bajan por su lista.** $p$ le propone a los de $L_p$ en orden, a cada uno a lo sumo una vez; sus parejas solo empeoran.
- **(I3) Lo que hay es un emparejamiento válido, y `libres` tiene exactamente a los proponentes sin pareja que no se rindieron.**

Los tres pasos:

- *Inicialización.* Nadie tiene pareja, todos los proponentes están en `libres` y `siguiente[p] = 0`. (I1) e (I2) todavía no dicen nada, y (I3) vale con el emparejamiento vacío.
- *Mantenimiento.* Sale de `libres` un proponente $p$, y hay cuatro ramas. Si se le acabó la lista, se rinde: no tiene pareja y no vuelve a `libres`, y nada más cambia. Si no, le propone a `Lp[p][siguiente[p]]`, el siguiente de su lista, y `siguiente[p]` avanza (I2); como ese receptor $r$ está en $L_p$, el par que se pueda formar respeta la lista (I3). Si $r$ estaba sola, acepta, y $p$ queda con pareja. Si $r$ prefiere a $p$, cambia a alguien mejor (I1), y su pareja anterior vuelve a `libres` sin pareja. Si $r$ prefiere a su pareja actual, nada cambia y $p$ vuelve a `libres`. En ningún caso un receptor queda solo después de tener pareja, ni un agente queda en dos pares.
- *Conclusión.* Al terminar, `libres` está vacía. Por (I3), el resultado es un emparejamiento válido, y además vale **(I4): todo proponente está emparejado o agotó su lista**, porque los que no tienen pareja y no están en `libres` son los que se rindieron.

Falta ver que es estable, que es el teorema que sigue y usa (I1), (I2) y (I4).

> **Teorema.** El emparejamiento $M$ que devuelve el algoritmo es estable, para cualquier orden de ejecución.

*Demostración.* Por contradicción, con la estructura de la de C3 ("como $a$ propone en orden decreciente y terminó con $M(a)$, le propuso a $b$ antes [...]; en algún momento $b$ rechazó a $a$ [...]; por el primer invariante, la pareja de $b$ solo mejora"). Supongamos que $(p, r)$ bloquea a $M$. Por la condición 1, $r \in L_p$.

**Paso 1: $p$ le propuso a $r$.** Por la condición 3 hay dos casos.
- $p$ está emparejado con $M(p)$ y prefiere $r$: como $p$ baja por su lista (I2) y llegó hasta $M(p)$, que está debajo de $r$ en $L_p$, antes le propuso a $r$.
- $p$ está solo: por (I4) agotó su lista, así que le propuso a todos los de $L_p$, y $r$ está en $L_p$.

**Paso 2: $r$ terminó con alguien que prefiere a $p$.** Cuando $p$ le propuso a $r$, o $r$ lo rechazó porque tenía a alguien que prefería, o lo aceptó y más tarde lo cambió por alguien que prefería. (No hay otra posibilidad: $p$ terminó sin $r$.) En los dos casos, en algún momento $r$ estuvo con alguien que prefiere a $p$, y por (I1) termina con alguien al menos igual de bueno. Así que $r$ no está sola y prefiere $M(r)$ a $p$.

Esto contradice la condición 4. ∎

**¿Dónde se usó cada adaptación?**
- **La condición 1** se usa en los dos casos del Paso 1: tanto "llegó hasta $M(p)$, que está debajo de $r$" como "le propuso a todos los de $L_p$" necesitan que $r$ esté en la lista. Sin la condición 1, un $p$ solo "bloquearía" con cualquier $r$ que no listó y que lo prefiriera a su pareja actual. Ese par no es un problema, porque $p$ prefiere quedarse solo, pero haría falsa la estabilidad. Por ejemplo, $(C, Z)$ en el ejemplo: Z está sola, así que la cond. 4 se cumple.
- **La rendición** se usa en el segundo caso del Paso 1, vía (I4). Sin (I4), un proponente podría estar solo "por error", sin haberle propuesto a todos los de su lista.
- **Las listas completas de los receptores** se usan en el Paso 2: cuando $p$ propone, $r$ lo tiene ordenado y la respuesta es una comparación de preferencias. No hay rechazos "porque no te listé".

**Corolario (como el de C3).** Toda instancia con listas incompletas de los proponentes tiene un emparejamiento estable: el algoritmo es la demostración de existencia, constructiva.

## 6. Bonus: sigue siendo óptimo para los proponentes (primer fallo)

En C3 la optimalidad de Gale-Shapley se demostró con la técnica del **primer fallo**: "tomar el primer contraejemplo en el tiempo y usar que es el primero, porque todo lo que pasó antes todavía está bien". Funciona igual aquí. Con la definición de C3, $r$ es una **pareja válida** de $p$ si existe algún emparejamiento estable que contiene $(p, r)$, y $\text{mejor}(p)$ es la pareja válida que $p$ prefiere entre todas.

> **Teorema.** Toda ejecución empareja a cada proponente $p$ con $\text{mejor}(p)$, o lo deja solo si no tiene ninguna pareja válida.

*Demostración.* Basta ver que **ningún proponente es rechazado (ni dejado) nunca por una pareja válida**. Si eso vale, hay dos casos. Si $p$ termina con $r$, esa pareja es válida (el resultado es estable), y cualquier pareja válida que $p$ prefiera a $r$ lo tuvo que rechazar antes, cosa que no pasa; así que $r = \text{mejor}(p)$. Si $p$ termina solo, agotó su lista, es decir, todos los de su lista lo rechazaron, así que ninguno es pareja válida, y los que no están en su lista tampoco pueden serlo (ningún emparejamiento los junta).

Supongamos que sí pasa, y miro **el primer momento** en que pasa: $r$ rechaza (o deja) a $p$ por $p'$, que $r$ prefiere, y existe un estable $M'$ con $(p, r) \in M'$.

- En $M'$, $r$ está con $p$, así que $p'$ está con otro $r' = M'(p')$ o está solo.
- **$r \in L_{p'}$**, porque $p'$ le propuso a $r$.
- **$p'$ prefiere $r$ a su situación en $M'$.** $p'$ está ahora con $r$, así que todos los que $p'$ prefiere a $r$ ya lo rechazaron antes. Si $p'$ prefiriera $r'$ a $r$, entonces $r'$ lo habría rechazado antes, y $r'$ es pareja válida de $p'$ (están juntos en $M'$): eso sería un rechazo por pareja válida **anterior** al primero. Imposible. Y si $p'$ está solo en $M'$, prefiere a $r$, que está en su lista, antes que estar solo.
- **$r$ prefiere $p'$ a $p = M'(r)$**, por cómo elegimos el momento.

Entonces $(p', r)$ cumple las cuatro condiciones y bloquea a $M'$, que era estable. Contradicción. ∎

Es el dibujo de la figura 5 de C3 con un caso más: en $M'$, $p'$ puede estar **solo** en lugar de con un $b'$. Ese caso se cierra con la condición 3 adaptada (estar solo es peor que cualquiera de la lista). Como en C3, el resultado no depende del orden de ejecución, porque $\text{mejor}(p)$ no depende de él. El reverso de C3 ej. 5 (cada receptor recibe su **peor** pareja válida) también vale aquí, pero no lo demuestro.

**Observación (quiénes quedan solos).** Un hecho conocido de este modelo es que **en todos los emparejamientos estables quedan solos exactamente los mismos agentes** (McVitie y Wilson, 1970; Roth lo extendió en 1986 a receptores con varias plazas, con el nombre de teorema de los "hospitales rurales"). No lo demuestro aquí, pero lo compruebo abajo por fuerza bruta en instancias chicas. En el ejemplo, el único estable es el que devuelve el algoritmo: no hay forma de "arreglar" que C quede solo eligiendo otro emparejamiento estable.

---

## 7. Casos de prueba

Para instancias chicas genero listas incompletas al azar para los proponentes y listas completas al azar para los receptores, enumero **todos** los emparejamientos válidos por fuerza bruta, me quedo con los estables, y compruebo:
1. que el resultado del algoritmo es un emparejamiento válido y estable;
2. que cada proponente recibe su pareja válida preferida (y por lo tanto que el resultado no depende del orden en que se procesan los libres);
3. que el número de propuestas es $\le \sum_p |L_p|$;
4. que el conjunto de solos es el mismo en todos los estables;
5. y dos errores plantados, los de la sección 4: el algoritmo de C3 sin adaptar (sin rendición) y el arreglo que vuelve a empezar la lista.

```python
import random, itertools

def es_valido(M, Lp, Lr):
    usados_r = [r for r in M.values() if r is not None]
    return len(usados_r) == len(set(usados_r)) and \
           all(r is None or r in Lp[p] for p, r in M.items())

def bloqueantes(M, Lp, Lr):
    pareja_r = {r: None for r in Lr}
    for p, r in M.items():
        if r is not None: pareja_r[r] = p
    res = []
    for p in Lp:
        for r in Lp[p]:                                           # cond. 1: r en la lista de p
            if M[p] == r:
                continue                                          # cond. 2
            p_quiere = M[p] is None or Lp[p].index(r) < Lp[p].index(M[p])               # cond. 3
            r_quiere = pareja_r[r] is None or Lr[r].index(p) < Lr[r].index(pareja_r[r])  # cond. 4
            if p_quiere and r_quiere:
                res.append((p, r))
    return res

def todos_los_estables(Lp, Lr):
    P = list(Lp)
    opciones = [[None] + Lp[p] for p in P]
    for eleccion in itertools.product(*opciones):
        M = dict(zip(P, eleccion))
        if es_valido(M, Lp, Lr) and not bloqueantes(M, Lp, Lr):
            yield M

def instancia_aleatoria(np_, nr, prob):
    """Listas incompletas para los proponentes (cada receptor entra con probabilidad prob),
    listas completas para los receptores."""
    P = [f"p{i}" for i in range(np_)]; R = [f"r{j}" for j in range(nr)]
    Lp = {}
    for p in P:
        L = [r for r in R if random.random() < prob]; random.shuffle(L); Lp[p] = L
    Lr = {r: random.sample(P, len(P)) for r in R}
    return Lp, Lr

# Ejemplo de la sección 3
Lp = {"A": ["X", "Y"], "B": ["X"], "C": ["Y"]}
Lr = {"X": ["B", "A", "C"], "Y": ["A", "C", "B"], "Z": ["A", "B", "C"]}
M, prop = gale_shapley_incompleto(Lp, Lr)
print("ejemplo:", M, f"({prop} propuestas)")
print("estables del ejemplo:", list(todos_los_estables(Lp, Lr)))
assert M == {"A": "Y", "B": "X", "C": None} and not bloqueantes(M, Lp, Lr)

random.seed(12)
total, con_solos = 0, 0
for _ in range(1500):
    Lp, Lr = instancia_aleatoria(random.randint(1, 5), random.randint(1, 5), random.choice([0.3, 0.5, 0.8, 1.0]))
    M, prop = gale_shapley_incompleto(Lp, Lr)
    estables = list(todos_los_estables(Lp, Lr))
    # 1) válido y estable
    assert es_valido(M, Lp, Lr) and not bloqueantes(M, Lp, Lr)
    # 2) óptimo para proponentes
    for p in Lp:
        validas = {E[p] for E in estables if E[p] is not None}
        mejor = min(validas, key=Lp[p].index) if validas else None
        assert M[p] == mejor
    # 3) potencial
    assert prop <= sum(len(L) for L in Lp.values())
    # 4) quiénes quedan solos: los mismos en todos los estables
    solos = {frozenset(p for p in E if E[p] is None) for E in estables}
    assert len(solos) == 1
    total += 1
    con_solos += any(r is None for r in M.values())
print(f"{total} instancias aleatorias: estable, óptimo para proponentes, propuestas <= sum |L_p|,")
print(f"  mismos solos en todos los estables. ({con_solos} de ellas dejaban a algún proponente solo)")
```

Los dos errores plantados de la sección 4 comparten el código de C3 y difieren solo en qué hacen cuando a $p$ se le acaba la lista. Los pruebo como en C3, con generadores distintos: el de listas completas $n \times n$ es el que sale de copiar las pruebas de C3.

```python
def gs_sin_rendicion(Lp, Lr, reiniciar, tope=10_000):
    """Gale-Shapley de C3 sin la línea nueva. reiniciar=False: lee fuera de la lista.
    reiniciar=True: quien agota su lista vuelve a empezarla. Devuelve qué pasó."""
    rango = {r: {p: k for k, p in enumerate(Lr[r])} for r in Lr}
    siguiente = {p: 0 for p in Lp}
    pareja_r = {r: None for r in Lr}
    libres = deque(Lp)
    for _ in range(tope):
        if not libres:
            return "termina"
        p = libres.popleft()
        if reiniciar and siguiente[p] == len(Lp[p]):
            siguiente[p] = 0
        if siguiente[p] >= len(Lp[p]):
            return "se cae"                  # Lp[p][siguiente[p]] daría IndexError
        r = Lp[p][siguiente[p]]
        siguiente[p] += 1
        if pareja_r[r] is None:
            pareja_r[r] = p
        elif rango[r][p] < rango[r][pareja_r[r]]:
            libres.append(pareja_r[r])
            pareja_r[r] = p
        else:
            libres.append(p)
    return "no termina"

Lp = {"A": ["X", "Y"], "B": ["X"], "C": ["Y"]}
Lr = {"X": ["B", "A", "C"], "Y": ["A", "C", "B"], "Z": ["A", "B", "C"]}
print("\nejemplo, sin adaptar:", gs_sin_rendicion(Lp, Lr, reiniciar=False))
print("ejemplo, reiniciando la lista:", gs_sin_rendicion(Lp, Lr, reiniciar=True))

generadores = {
    "completas n×n": lambda: instancia_aleatoria(*[random.randint(1, 5)] * 2, 1.0),
    "incompletas 0.8": lambda: instancia_aleatoria(random.randint(1, 5), random.randint(1, 5), 0.8),
    "incompletas 0.5": lambda: instancia_aleatoria(random.randint(1, 5), random.randint(1, 5), 0.5),
}
print(f"\n{'generador':>16} {'sin adaptar':>12} {'reiniciando':>12} {'adaptado':>9}")
for nombre, generar in generadores.items():
    casos = [generar() for _ in range(2000)]
    fallas = {"sin adaptar": 0, "reiniciando": 0, "adaptado": 0}
    for Lp, Lr in casos:
        M = gale_shapley_incompleto(Lp, Lr)[0]
        fallas["adaptado"] += not es_valido(M, Lp, Lr) or bool(bloqueantes(M, Lp, Lr))
        alguien_solo = None in M.values()
        for clave, reiniciar in [("sin adaptar", False), ("reiniciando", True)]:
            falla = gs_sin_rendicion(Lp, Lr, reiniciar) != "termina"
            assert falla == alguien_solo       # fallan justo cuando alguien debe quedar solo
            fallas[clave] += falla
    print(f"{nombre:>16} {100 * fallas['sin adaptar'] / len(casos):>11.1f}% "
          f"{100 * fallas['reiniciando'] / len(casos):>11.1f}% "
          f"{100 * fallas['adaptado'] / len(casos):>8.1f}%")

# Costo: lineal en el tamaño de la entrada
print(f"\n{'|P|=|R|':>8} {'prob':>5} {'sum |L_p|':>10} {'propuestas':>11}")
for n in [100, 1000]:
    for prob in [0.05, 0.5]:
        Lp, Lr = instancia_aleatoria(n, n, prob)
        M, prop = gale_shapley_incompleto(Lp, Lr)
        print(f"{n:8} {prob:5} {sum(len(L) for L in Lp.values()):10} {prop:11}")
```

### Salida

```text
ejemplo: {'A': 'Y', 'B': 'X', 'C': None} (4 propuestas)
estables del ejemplo: [{'A': 'Y', 'B': 'X', 'C': None}]
1500 instancias aleatorias: estable, óptimo para proponentes, propuestas <= sum |L_p|,
  mismos solos en todos los estables. (827 de ellas dejaban a algún proponente solo)

ejemplo, sin adaptar: se cae
ejemplo, reiniciando la lista: no termina

       generador  sin adaptar  reiniciando  adaptado
   completas n×n         0.0%         0.0%      0.0%
 incompletas 0.8        46.5%        46.5%      0.0%
 incompletas 0.5        60.2%        60.2%      0.0%

 |P|=|R|  prob  sum |L_p|  propuestas
     100  0.05        525         238
     100   0.5       4984         476
    1000  0.05      50053        6432
    1000   0.5     499380        7301
```

Tres comentarios sobre la salida.

**Los errores plantados son invisibles con las pruebas de C3.** Con listas completas $n \times n$ las dos versiones rotas aciertan siempre: nadie agota su lista, y el lema de C3 que dejaron de cumplir vale. En cuanto las listas son incompletas, fallan en casi la mitad de los casos o más. Y fallan **exactamente** en las instancias donde algún proponente debe quedar solo (lo comprueba el `assert`). Es la lección de C3 otra vez: el lema de C3 tenía una hipótesis, listas completas, y lo que no cubre esa hipótesis es justo lo que hay que probar.

**Las dos fallas tienen la forma que anuncia la sección 4.** Sin adaptar, el algoritmo se sale de la lista. Reiniciando, el potencial deja de bajar y no termina.

**El potencial es solo una cota.** En la última tabla, con listas densas (prob 0,5) se hacen muchas menos propuestas que $\sum_p |L_p|$, igual que en C3 Gale-Shapley con listas al azar hacía unas $n \ln n$ propuestas (243,7 para $n = 60$) y no las $n^2$ de la cota. El caso típico no es la garantía.

## 8. Costo

- **Vueltas:** a lo sumo $\sum_p |L_p|$ propuestas y $|P|$ rendiciones (sección 4).
- **Cada vuelta en $O(1)$**, con las dos estructuras de C3: `siguiente[p]`, el puntero en la lista de $p$, y `rango[r][p]`, la lista de $r$ invertida.
- **Total:** $O\big(\sum_p |L_p| + |P|\cdot|R|\big)$, contando la construcción de `rango`, que lee las listas completas de los receptores. Es **lineal en el tamaño de la entrada**, como el $O(n^2)$ de C3 lo es para $2n$ listas de largo $n$.
- **Sin la tabla `rango`:** cada comparación de pretendientes busca en la lista del receptor y cuesta $O(|P|)$, y el costo sube a $O\big(|P| \cdot \sum_p |L_p|\big)$; con listas completas, el $O(n^3)$ de C3.
- **Peor caso:** con listas completas son $n^2$ propuestas, y no se puede mejorar en ese caso: es la cota $\Omega(n^2)$ de Ng y Hirschberg (C3).
- **Espacio:** $O(|P|\cdot|R|)$ por `rango`, más $O(|P| + |R|)$ para `siguiente`, `pareja_r` y `libres`.

---

**Uso de IA**: implementación de algoritmos, generación de casos de prueba y correcciones de redacción.
