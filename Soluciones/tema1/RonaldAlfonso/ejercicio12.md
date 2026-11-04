## 12.  Gale-Shapley con listas incompletas (C3)

**Problema.** Cada proponente $a$ tiene una lista estricta de *algunos* receptores; los que no lista le son **inaceptables**: prefiere quedarse solo. (Si los receptores también tienen listas incompletas, todo lo que sigue vale igual tomando "aceptable" como "cada uno lista al otro".) Un emparejamiento $M$ es ahora un conjunto de pares aceptables disjuntos; no tiene por qué ser perfecto, y alguien puede quedar solo.

**Pareja bloqueante, adaptada.** $(a, b)$, no emparejados entre sí, bloquea $M$ si:

1. $b$ está en la lista de $a$ (y $a$ en la de $b$, si los receptores tienen listas incompletas);
2. $a$ está solo, o prefiere $b$ a su pareja $M(a)$;
3. $b$ está solo, o prefiere $a$ a su pareja $M(b)$.

"Estar solo" se trata como una opción peor que cualquier pareja aceptable y mejor que cualquiera inaceptable. Hace falta además que nadie esté con alguien inaceptable, pero el algoritmo nunca forma esos pares.

**Algoritmo.** El mismo, con dos cambios: un proponente solo propone a receptores de su lista, y un proponente que agotó su lista queda solo para siempre.

```python
def gale_shapley_incompleto(pref_a, pref_b):
    rango = [{a: i for i, a in enumerate(pref_b[b])} for b in range(len(pref_b))]
    siguiente = [0] * len(pref_a)
    pareja_de_b = [None] * len(pref_b)
    libres = deque(range(len(pref_a)))
    while libres:
        a = libres.popleft()
        if siguiente[a] == len(pref_a[a]):
            continue                              # agotó su lista: queda solo
        b = pref_a[a][siguiente[a]]
        siguiente[a] += 1
        actual = pareja_de_b[b]
        if a not in rango[b]:                     # b no acepta a a
            libres.append(a)
        elif actual is None:
            pareja_de_b[b] = a
        elif rango[b][a] < rango[b][actual]:
            pareja_de_b[b] = a
            libres.append(actual)
        else:
            libres.append(a)
    return {a: b for b, a in enumerate(pareja_de_b) if a is not None}
```

**Los dos invariantes de C3 §7 siguen valiendo**, con la misma demostración: un receptor, una vez comprometido, no vuelve a quedar libre y su pareja solo mejora; un proponente propone en orden decreciente de su lista.

**Potencial.**
$$\Phi = \sum_a \big(\text{receptores de la lista de } a \text{ a los que todavía no les propuso}\big).$$
Empieza en $L = \sum_a |\text{lista}(a)|$, es entero y no negativo, y cada propuesta lo baja en 1 porque `siguiente[a]` solo avanza. Las vueltas que solo sacan de la cola a un proponente agotado no lo bajan, pero cada proponente se descarta así una sola vez. Hay a lo sumo $L$ propuestas y $L + n$ vueltas. Con la tabla de rangos, **tiempo $O(L + n)$**, lineal en el tamaño de la entrada.

Fíjate en lo que cambió respecto a C3: allí había que demostrar que ningún proponente agotaba su lista, para que `siguiente[a]` no se saliera; aquí agotar la lista es un final permitido, y el ciclo lo contempla.

**Teorema. El resultado es estable** (con la definición adaptada), para cualquier orden de ejecución.

*Demostración, por contradicción.* Sea $(a, b)$ bloqueante para el resultado $M$.

- Primero, $a$ le propuso a $b$. Si $a$ terminó solo, el algoritmo solo termina cuando todo proponente libre agotó su lista, así que $a$ le propuso a todos los de su lista, $b$ incluido. Si $a$ terminó con $M(a)$ y prefiere $b$, como propone en orden decreciente le propuso a $b$ antes que a $M(a)$.
- Como $a$ no terminó con $b$, en algún momento $b$ lo rechazó, al recibir la propuesta o más tarde. No fue por inaceptable, por la condición 1. Fue a cambio de alguien que $b$ prefiere a $a$.
- Por el primer invariante, desde ese momento $b$ está siempre comprometido y su pareja solo mejora. Al final $b$ no está solo y prefiere $M(b)$ a $a$. Contradice la condición 3. $\square$

Igual que en C3 §8, el algoritmo es la demostración de que **siempre existe un emparejamiento estable** en esta versión.

(Comprobado en 5000 instancias al azar con listas incompletas de los dos lados: ningún par bloqueante, nadie con pareja inaceptable, y propuestas $\le L$.)

---
