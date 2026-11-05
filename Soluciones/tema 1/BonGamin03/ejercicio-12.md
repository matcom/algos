# Ejercicio 12 

## El problema 

> **Enunciado:** Gale-Shapley con listas incompletas: cada proponente lista solo a algunos receptores, y prefiere quedarse solo antes que con uno que no listó. Adapta el algoritmo, su potencial y la definición de pareja bloqueante. ¿Sigue siendo estable el resultado? Demuéstralo.

---

### Especificación y Adaptaciones Formales

#### Modelo de Preferencias
- Sea $A = \{a_1, \dots, a_n\}$ el conjunto de proponentes y $B = \{b_1, \dots, b_m\}$ el de receptores.
- Cada $a \in A$ tiene una lista de preferencias **estricta e incompleta** sobre un subconjunto de receptores $L(a) \subseteq B$. Para $a$, cualquier receptor no incluido en $L(a)$ es inaceptable ($a$ prefiere estar solo que emparejado con $b \notin L(a)$).
- Análogamente, cada $b \in B$ tiene una lista estricta e incompleta $L(b) \subseteq A$. Para $b$, cualquier proponente no incluido en $L(b)$ es inaceptable.
- **Relación de Aceptación Mutua:** Un par $(a, b)$ es aceptable de forma mutua si y solo si $b \in L(a)$ y $a \in L(b)$.

#### Redefinición de Emparejamiento Estable (Listas Incompletas)
Un emparejamiento $M$ es un conjunto de parejas $(a, b) \in A \times B$ tal que cada agente tiene a lo sumo una pareja en $M$.

$M$ es **estable** si cumple dos condiciones:
**Racionalidad Individual:** Ningún agente está emparejado con alguien inaceptable. Para todo $(a, b) \in M$, $b \in L(a)$ y $a \in L(b)$.
**Ausencia de Parejas Bloqueantes:** No existe ningún par $(a, b) \in A \times B$ tal que:
   - $(a, b)$ sea mutuamente aceptable ($b \in L(a)$ y $a \in L(b)$).
   - $a$ prefiera a $b$ sobre su pareja actual en $M$ (o prefiere a $b$ por encima de estar solo si $a$ está soltero).
   - $b$ prefiera a $a$ sobre su pareja actual en $M$ (o prefiere a $a$ por encima de estar solo si $b$ está soltero).

---

### Adaptación del Algoritmo de Gale-Shapley

Modificamos el algoritmo para que un proponente solo haga propuestas a los receptores de su lista $L(a)$ que lo consideren aceptable (o alternativamente, si propone a un receptor $b \notin L(b)$, $b$ lo rechaza inmediatamente).

```python
from collections import deque

def gale_shapley_incompleto(pref_a, pref_b):
    """
    pref_a: dict {a: lista_ordenada_de_b_aceptables}
    pref_b: dict {b: lista_ordenada_de_a_aceptables}
    """
    n_a = len(pref_a)
    
    # Preprocesar rangos para receptores en O(|L(b)|)
    rango = {b: {a: i for i, a in enumerate(lista)} for b, lista in pref_b.items()}
    
    siguiente = {a: 0 for a in pref_a}
    pareja_de_b = {b: None for b in pref_b}
    libres = deque(pref_a.keys())
    
    while libres:
        a = libres.popleft()
        
        # Si a ya promedió/agotó toda su lista de aceptables L(a), se queda soltero
        if siguiente[a] >= len(pref_a[a]):
            continue
            
        b = pref_a[a][siguiente[a]]
        siguiente[a] += 1
        
        # Si 'a' no es aceptable para 'b' (a not in L(b)), b lo rechaza inmediatamente
        if a not in rango[b]:
            libres.append(a)
            continue
            
        actual = pareja_de_b[b]
        if actual is None:
            pareja_de_b[b] = a
        elif rango[b][a] < rango[b][actual]:
            pareja_de_b[b] = a
            libres.append(actual)
        else:
            libres.append(a)
            
    # Construir emparejamiento final
    M = []
    for b, a in pareja_de_b.items():
        if a is not None:
            M.append((a, b))
    return M
```

---

### Demostración de Terminación mediante Potencial

Siguiendo la teoría de la Conferencia 3, la terminación se demuestra encontrando una función de potencial $\Phi \in \mathbb{Z}_{\ge 0}$ que decrezca estrictamente en cada vuelta del ciclo principal.

#### Definición del Potencial:
Sea $\Phi$ la suma de las propuestas pendientes que los proponentes pueden hacer a los receptores de sus respectivas listas aceptables:

$$\Phi = \sum_{a \in A} (|L(a)| - \text{siguiente}[a])$$

#### Demostración:
**Cota Inferior:** Para todo paso de la ejecución, $0 \le \text{siguiente}[a] \le |L(a)|$, por lo que $\Phi \ge 0$. Inicialmente, $\Phi_0 = \sum_{a \in A} |L(a)| \le |A| \cdot |B|$

**Decrecimiento Estricto:** Cada iteración del ciclo `while` corresponde a un intento de propuesta de algún proponente $a$. En cada propuesta (sea aceptada, rechazada o declarada inaceptable por $b$), el valor de `siguiente[a]` se incrementa en $1$.
3. Por lo tanto, el potencial $\Phi$ decrece estrictamente en al menos 1 unidad por vuelta:
$$\Phi_{\text{nuevo}} = \Phi_{\text{anterior}} - 1$$
Como una cantidad entera no negativa no puede decrecer indefinidamente, el ciclo termina en a lo sumo $\Phi_0 \le |A| \cdot |B|$ vueltas.

---

### Demostración de Correctitud y Estabilidad

#### Invariantes Fundamentales del Algoritmo
- **Invariante 1 (Monotonía de Receptores):** Una vez que un receptor $b$ recibe su primera propuesta válida, permanece comprometido por el resto del algoritmo, y su pareja solo mejora estrictamente según su lista $L(b)$.

- **Invariante 2 (Monotonía de Proponentes):** Cada proponente $a$ propone en orden estrictamente decreciente de preferencia dentro de su lista $L(a)$.

#### Teorema: El emparejamiento resultado $M$ es siempre Estable.

#### Demostración:

**Parte A: Racionalidad Individual**
- Ningún proponente $a$ propone a alguien fuera de $L(a)$.
- Ningún receptor $b$ acepta a un proponente que no pertenezca a su lista $L(b)$ (el algoritmo descarta explícitamente el caso $a \notin L(b)$).
- Por ende, toda pareja en $M$ es mutuamente aceptable.

**Parte B: Ausencia de Parejas Bloqueantes (Por Contradicción)**
Supongamos que $M$ no es estable. Entonces existe una pareja bloqueante $(a, b) \in A \times B$.

Por definición de pareja bloqueante:
1. $(a, b)$ es mutuamente aceptable ($b \in L(a)$ y $a \in L(b)$).
2. $a$ prefiere a $b$ sobre su estado/pareja en $M$.
3. $b$ prefiere a $a$ sobre su estado/pareja en $M$.

Analicemos las decisiones tomadas por el algoritmo:
- Dado que $a$ prefiere a $b$ sobre su pareja final en $M$ (o sobre estar solo), por la **Monotonía del Proponente (Invariante 2)**, $a$ tuvo que haberle propuesto a $b$ antes de terminar el algoritmo.
- Como $a \in L(b)$, $b$ recibió la propuesta de $a$.
- Si $b$ terminó el algoritmo con una pareja $a' \neq a$ (o no se quedó con $a$), se debe a que $b$ rechazo la propuesta de $a$ (ya sea al recibirla o más adelante al cambiar a $a$ por un proponente mejor).
- Por la **Monotonía del Receptor (Invariante 1)**, la pareja final de $b$ en $M$ es al menos tan preferida por $b$ como el proponente que causó el rechazo de $a$.
- Por ende, $b$ prefiere a su pareja final en $M$ por encima de $a$.
- Esto **contradice** la suposición de que $b$ prefería a $a$ sobre su pareja en $M$.

Por lo tanto, no pueden existir parejas bloqueantes y el emparejamiento devuelto $M$ es **estable**. $\blacksquare$
