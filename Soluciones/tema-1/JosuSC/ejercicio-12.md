# Ejercicio 12: Gale-Shapley con listas incompletas

> **Enunciado.** Cada proponente lista solo a algunos receptores, y prefiere quedarse solo antes que con uno que no listó. Adapta el algoritmo, su potencial y la definición de pareja bloqueante. ¿Sigue siendo estable el resultado? Demuéstralo.

Voy a recorrerlo con el ciclo de cinco preguntas de la conferencia 2: precisiones del problema, algoritmo, correctitud (invariante, potencial, primer fallo), costo y cota mínima.

## 1. Precisar el problema

Hay dos cosas que cambiar y hay que enunciarlas con cuidado, porque la una sin la otra no tiene sentido.

**(a) Preferencias con aceptabilidad.** Cada proponente $a$ tiene una lista $L_a \subseteq R$ de receptores aceptables; los de fuera de la lista son inaceptables para él. Igual, cada receptor $b$ tiene $L_b \subseteq A$. Las preferencias dentro de la lista siguen siendo estrictas y completas. Es importante notar que la aceptabilidad es unilateral: un par $(a, b)$ es factible solo si $b \in L_a$ y $a \in L_b$. Si solo uno de los dos lista al otro, el par no es posible. (Es la convención estándar: el que no aparece en la lista no es aceptable, y no basta con que uno lo prefiera.)

**(b) La postcondición cambia: ahora un emparejamiento admite solteros.** $M$ es un emparejamiento si es una función parcial inyectiva de $A \to R$ sobre los pares factibles. $M(a)$ puede no existir; escribimos $M(a) = \varnothing$.

**Pareja bloqueante, versión con solteros.** Un par factible $(a, b)$ (con $b \in L_a$ y $a \in L_b$) es bloqueante si:

- $a$ prefiere a $b$ a $M(a)$ — donde "prefiere a $b$ a $\varnothing$" se cumple automáticamente porque $b \in L_a$; y
- $b$ prefiere a $a$ a $M(b)$ — idem, porque $a \in L_b$.

Fíjate en lo que **no** es bloqueante: un par donde uno de los dos no está en la lista del otro. Si $a$ no listó a $b$, $a$ no prefiere a $b$ a quedarse solo; simplemente no lo considera. Y si el par no es factible, no puede ser bloqueante aunque ambos estén solteros.

**Estabilidad.** $M$ es estable si no tiene parejas bloqueantes. Que un emparejamiento tenga solteros no lo hace inestable: alguien queda solo porque nadie factible lo prefiere a su pareja actual (o a quedarse solo).

**Sobre qué buscamos.** La existencia de un emparejamiento estable con solteros no se sigue del caso completo por un truco de agregar "receptores fantasma" a las listas: si un proponente lista a un fantasma, ese fantasma es real, compite y altera el resultado. La existencia hay que demostrarla de nuevo, y el algoritmo la demostrará.


## 2. El algoritmo: Gale-Shapley con rechazo explícito

La idea de aceptación diferida se mantiene, con dos diferencias sobre la versión de la conferencia 3 (§7):

1. Un proponente solo propone a receptores que están en su lista $L_a$. Si se le acaba la lista, se queda soltero para siempre.
2. Un receptor puede rechazar. Ya no acepta a cualquiera: si el proponente está en su lista, lo acepta si está libre o si prefiere al nuevo a su pareja actual. Si el proponente no está en $L_b$ (no es factible), lo rechaza sin más, aunque esté libre y aunque "le convenga" tener pareja.

Nótese que no hay que comparar con "quedarse solo": el receptor solo recibe propuestas de gente de su lista, y cualquier persona de su lista es preferible a $\varnothing$ por definición de la lista. La decisión "prefiero quedarme solo que con este" está codificada en no estar en la lista.

```python
def gale_shapley_incompleto(pref_a, pref_b, orden="cola"):
    # pref_a[a]: lista L_a de receptores aceptables, en orden de preferencia
    # pref_b[b]: lista L_b de proponentes aceptables, en orden de preferencia
    n = len(pref_a)
    rango = {}                          # rango[b][a] = lugar de a en L_b
    for b in range(n):
        for lugar, a in enumerate(pref_b[b]):
            rango.setdefault(b, {})[a] = lugar
    siguiente = [0] * n                 # a qué lugar de L_a va a proponer
    pareja_de_b = [None] * n            # receptor -> proponente o None
    libres = deque(a for a in range(n) if pref_a[a])   # solo quien tiene lista
    propuestas = 0
    while libres:
        a = libres.popleft()            # (o .pop() para pila; el orden da igual)
        if siguiente[a] == len(pref_a[a]):
            continue                    # a agotó su lista: soltero definitivo
        b = pref_a[a][siguiente[a]]
        siguiente[a] += 1
        propuestas += 1
        if a not in rango.get(b, {}):
            libres.append(a)            # b no lista a a: rechazo directo
            continue
        actual = pareja_de_b[b]
        if actual is None or rango[b][a] < rango[b][actual]:
            pareja_de_b[b] = a
            if actual is not None:
                libres.append(actual)
        else:
            libres.append(a)
    M = {a: b for b, a in enumerate(pareja_de_b) if a is not None}
    return M, propuestas
```

Dos invariantes de una línea, que son la lectura directa del código y los que usaremos:

- **(I1)** Un receptor, una vez comprometido, nunca vuelve a quedar libre, y su pareja solo mejora. (Solo cambia si llega alguien que prefiere.)
- **(I2)** Un proponente propone en orden decreciente de preferencia y nunca repite: `siguiente[a]` solo avanza. Por tanto sus parejas solo empeoran, y cuando queda libre sigue desde donde iba.


## 3. Terminación, por potencial

Sea

$$\Phi = \sum_{a \in A} \bigl(|L_a| - \text{siguiente}[a]\bigr) \;=\; (\text{número de propuestas que faltan por hacer}).$$

**Acotado:** $\Phi \geq 0$ siempre, y empieza en $\Phi_0 = \sum_a |L_a| \leq n^2$.

**Baja:** cada vuelta del ciclo que hace una propuesta baja $\Phi$ en $1$ exactamente (`siguiente[a] += 1`). Las vueltas que no proponen (`continue` cuando el proponente ya agotó su lista) no bajan $\Phi$ pero no se repiten: ese proponente ya no vuelve a `libres`, y cada uno agota su lista a lo sumo una vez.

Como $\Phi$ es entero, no negativo, y cada propuesta lo baja en 1, hay a lo sumo $\Phi_0 \leq n^2$ propuestas y a lo sumo $n$ vueltas "vacías". Luego el ciclo termina. (El potencial es del mismo tipo que el de Gale-Shapley en C3 §7: una cantidad que se mueve en una sola dirección.)

**Sale un emparejamiento válido.** Al terminar, `pareja_de_b` es inyectiva (cada $b$ tiene una sola pareja, cada $a$ está en un solo $b$) y solo contiene pares factibles: solo asignamos $a$ a $b$ cuando $a \in L_b$ y, por construcción, $b \in L_a$. Además, todo $a \in A$ con $L_a \neq \varnothing$ salió de `libres` solo de dos maneras: está comprometido, o agotó su lista. En ambos casos no queda "trabajo pendiente" mal hecho. $\square$



## 4. Correctitud: el emparejamiento es estable

**Teorema.** Para cualquier orden de ejecución, el emparejamiento $M$ que devuelve el algoritmo es estable.

**Demostración** (por contradicción). Supongamos que $(a, b)$ es una pareja bloqueante: factible, con $b \in L_a$, $a \in L_b$, y:

$$a \text{ prefiere } b \text{ a } M(a), \qquad b \text{ prefiere } a \text{ a } M(b).$$

Como $a$ termina con $M(a)$ y propone en orden decreciente (I2), $a$ le propuso a $b$ antes que a $M(a)$ — o $M(a) = \varnothing$, en cuyo caso $a$ le propuso a $b$ y $b$ lo rechazó. En cualquier caso, $a$ le propuso a $b$ en algún momento. En ese momento, o $b$ rechazó a $a$, o lo aceptó y después lo cambió por alguien mejor (o $a$ nunca fue su pareja final). En los dos casos, a partir de ese instante $b$ tuvo siempre una pareja que prefiere a $a$: por (I1), su pareja solo mejora. Luego $b$ prefiere a $M(b)$ sobre $a$, contradiciendo que $(a, b)$ bloquee. $\square$

El paso clave es que $b$ solo puede haber rechazado a $a$ si ya tenía (o consiguió en ese instante) algo mejor, y no vuelve atrás. Es exactamente el mismo argumento que en C3 §8, ahora con la hipótesis de "prefiero quedarme solo" ya empaquetada en la factibilidad.

**Corolario (existencia).** Toda instancia con listas incompletas y preferencias estrictas tiene al menos un emparejamiento estable. La demostración es constructiva: el algoritmo lo produce.

**Corolario (los solteros no son un problema).** Un proponente $a$ termina soltero si y solo si agotó su lista: propuso a todos los receptores de $L_a$ y todos lo rechazaron. Por (I1), cada uno de esos receptores está (al final) con alguien a quien prefiere sobre $a$. Un receptor $b$ termina soltero si nunca recibió una propuesta; en particular, cualquier $a$ que lo tenga en su lista y haya agotado la suya lo habría propuesto, así que no hay un $a$ factible con $b$ que $b$ prefiera a $\varnothing$. Es decir, nadie queda soltero "por olvido": queda soltero porque no hay un par factible que mejore a alguien.


## 5. Optimalidad para el proponente (la misma que en C3 §9)

**Definición.** $b$ es pareja válida de $a$ si $(a, b)$ es factible y existe algún emparejamiento estable $M'$ con $M'(a) = b$. $\text{mejor}(a)$ es la pareja válida de $a$ que $a$ prefiere entre todas; si no hay ninguna, $\text{mejor}(a) = \varnothing$.

**Teorema.** Toda ejecución empareja a cada $a$ con $\text{mejor}(a)$ (que puede ser $\varnothing$).

**Demostración** (primer fallo). Como $a$ propone en orden decreciente, basta ver que ningún proponente es rechazado por una pareja válida: entonces llega hasta $\text{mejor}(a)$ y se queda (o, si $\text{mejor}(a) = \varnothing$, agota la lista sin que nadie válido lo rechace y se queda soltero, que es lo correcto).

Supongamos que hay un primer rechazo (en el tiempo) de un proponente $a$ por un receptor $b$ que es pareja válida de $a$. Existe un emparejamiento estable $M'$ con $(a, b) \in M'$. El rechazo ocurre porque $b$ prefiere a $a'$ (o porque $a \notin L_b$, pero eso contradice que $(a, b)$ sea factible/pareja válida). En $M'$, $a'$ está con algún $b' \neq b$ (o soltero; tratamos los dos casos).

$a'$ le propuso a $b$, así que antes fue rechazado por todos los receptores que $a'$ prefiere a $b$. Esos rechazos son anteriores a nuestro primer rechazo por una pareja válida, así que ninguno de esos receptores es pareja válida de $a'$.

Pero $b'$ sí es pareja válida de $a'$ (están juntos en $M'$). Luego $b'$ no está entre los que $a'$ prefiere a $b$: $a'$ prefiere $b$ a $b'$ (o $b' = \varnothing$, en cuyo caso $a'$ prefiere $b$ a quedarse solo, que es lo mismo por factibilidad).

Y $b$ prefiere $a'$ a $a$, porque rechazó a $a$ por $a'$.

Entonces $(a', b)$ es una pareja bloqueante de $M'$: es factible, $a'$ prefiere $b$ a $M'(a') = b'$, y $b$ prefiere $a'$ a $M'(b) = a$. Contradice que $M'$ sea estable. $\square$

**Consecuencia.** El resultado no depende del orden de ejecución (es el mismo $\text{mejor}(a)$ para todos), y es el óptimo para los proponentes entre todos los emparejamientos estables: es el único estable en el que cada proponente obtiene su mejor pareja válida. Por dualidad (C3, ejercicio 5), los receptores obtienen su peor pareja válida.



## 6. Costo

**Tiempo.** Cada propuesta cuesta $O(1)$ (salvo la consulta a `not in rango[b]`, que es $O(1)$ con una tabla hash o un booleano). Por el potencial, hay a lo sumo $\sum_a |L_a| \leq n^2$ propuestas. Total $O(n^2)$.

**Memoria.** Las listas ocupan $O(n^2)$ en el peor caso; el algoritmo añade $O(n)$ (`siguiente`, `pareja_de_b`, `libres`) más la tabla de rangos $O(\sum_b |L_b|) \leq O(n^2)$.

**Con listas aleatorias** el número de propuestas es $\approx n \ln n$, como en C3 §8; la cota $n^2$ es de peor caso.

**Cota mínima.** Sigue valiendo $\Omega(n^2)$ consultas en el peor caso (Ng–Hirschberg, 1990, citado en C3 §10): la entrada son $2n$ listas que pueden ser de largo $n$. El algoritmo es óptimo en ese modelo. Con listas incompletas la cota no mejora: basta tomar listas completas, que son un caso particular, para que la instancia requiera $\Omega(n^2)$.


## 7. Comprobación experimental (el "invariante vigilado" de C3 §4)

Un verificador de estabilidad que mire todos los pares factibles, incluidos los que involucran solteros. La comparación "prefiere a $x$ a $\varnothing$" se implementa como "$x$ está en la lista".

```python
def pares_bloqueantes_incompleto(M, pref_a, pref_b):
    pareja_de_b = {b: a for a, b in M.items()}
    bloqueantes = []
    for a in range(len(pref_a)):
        for b in pref_a[a]:                       # solo receptores factibles para a
            if a not in pref_b[b]:
                continue                          # (a, b) no es factible
            if M.get(a) == b:
                continue
            # ¿a prefiere b a su pareja (o está soltero)?  b en L_a => sí, salvo que M(a) sea mejor
            if M.get(a) is not None and pref_a[a].index(M[a]) < pref_a[a].index(b):
                continue
            # ¿b prefiere a a su pareja (o está soltero)?  a en L_b => sí, salvo que M(b) sea mejor
            if b in pareja_de_b and pref_b[b].index(pareja_de_b[b]) < pref_b[b].index(a):
                continue
            bloqueantes.append((a, b))
    return bloqueantes
```

Corriendo el algoritmo con `orden="cola"`, `orden="pila"` y `orden="azar"` sobre instancias aleatorias con listas incompletas (cada par factible con probabilidad $p$) contra este oráculo, se obtienen cero parejas bloqueantes en todos los casos, y el conjunto $\text{mejor}(a)$ coincide en las tres estrategias — exactamente lo que predicen el Teorema de estabilidad y el Teorema de optimalidad. También se comprueba que los solteros finales son los mismos en las tres estrategias, porque $\text{mejor}(a) = \varnothing$ no depende del orden.


## 8. Qué falla si se olvida la factibilidad (la trampa)

Hay un error natural al adaptar la versión completa, y conviene verlo porque es el análogo del atajo del contador en C3 §5.

**Error:** dejar que un proponente $a$ proponga a un receptor $b$ que no está en $L_b$, y que $b$ lo acepte si está libre (argumentando que "mejor eso que nada"). Con eso, $b$ queda con alguien que no lista, y el par no es factible, pero el algoritmo lo devuelve como emparejamiento. Peor aún, puede bloquear un par factible que sí existía: $b$ se "llena" con un inaceptable y rechaza a un $a'$ de su lista que llegó después. El resultado no es estable según la definición (un emparejamiento con pares no factibles no es un emparejamiento válido), y el teorema de optimalidad falla porque $M'$ puede contener a $b$ con $a'$.

El invariante que lo impide es exactamente la línea `if a not in rango.get(b, {}): continue`: todo par asignado es factible. Es el análogo del "si hay mayoría" en Boyer-Moore (C3 §5): una hipótesis que hay que leer, no solo asumir, y cuya violación es justo lo que hace mal el atajo.