# Ejercicio 12 ★★★ — Gale-Shapley con listas incompletas (C3)

> Gale-Shapley con listas incompletas: cada proponente lista solo a algunos receptores, y prefiere quedarse solo antes que con uno que no listó. Adapta el algoritmo, su potencial y la definición de pareja bloqueante. ¿Sigue siendo estable el resultado? Demuéstralo.

## 1. El problema adaptado

- $n_A$ proponentes y $n_B$ receptores. Cada proponente $a$ tiene una lista estricta $L_a$ con **algunos** receptores; cada receptor $b$, una lista estricta $L_b$ (que puede ser completa o también incompleta; el caso del enunciado es el de listas completas para los receptores, y lo cubrimos como caso particular).
- $a$ y $b$ son **mutuamente aceptables** si $b\in L_a$ y $a\in L_b$. Cada uno prefiere estar solo antes que con alguien que no está en su lista.
- Un **emparejamiento** $M$ es un conjunto de parejas disjuntas **mutuamente aceptables**. Puede haber gente sola. Escribimos $M(x)=\varnothing$ si $x$ está solo.

**Pareja bloqueante (adaptada).** $(a,b)$, no emparejados entre sí, bloquean $M$ si:
1. son mutuamente aceptables;
2. $a$ está solo, o prefiere $b$ a $M(a)$;
3. $b$ está solo, o prefiere $a$ a $M(b)$.

$M$ es **estable** si no tiene parejas bloqueantes. (Con listas completas y $n_A=n_B$ esta definición coincide con la de la conferencia, porque todos quedan emparejados.)

## 2. Algoritmo

Mientras haya un proponente libre **al que le quede alguien en su lista**, ese proponente le propone al mejor receptor de su lista al que todavía no le propuso. El receptor rechaza si no lista al proponente. Si lo lista y está libre, acepta. Si tiene pareja y prefiere al nuevo, cambia, y el anterior queda libre. Si no, rechaza.

La función `gale_shapley_incompleto(pref_a, pref_b)` implementa esa regla con una cola de proponentes libres que todavía tienen a quién proponer, y para cada receptor una tabla `rango` con la posición de cada proponente en su lista (si no aparece, lo rechaza). El parámetro `orden` elige qué proponente libre actúa primero (cola, pila o al azar), para comprobar que el resultado no depende de eso. Devuelve el emparejamiento (`None` para quien queda solo) y el número de propuestas.

> Código: [ejercicio-12.py](ejercicio-12.py), parte 1.

Lo que cambió respecto de la conferencia: (1) el receptor rechaza a quien no lista; (2) un proponente que agotó su lista **se queda solo** y sale del juego; (3) el ciclo termina cuando ningún libre tiene a quién proponer.

## 3. Invariantes

- **(I1)** Un receptor, una vez comprometido, no vuelve a quedar libre, y su pareja solo mejora en su lista.
- **(I2)** Cada proponente propone en orden decreciente de su lista y nunca dos veces al mismo.
- **(I3)** Toda pareja del emparejamiento es mutuamente aceptable: $a$ solo propone a receptores de $L_a$, y $b$ solo acepta proponentes de $L_b$.

Las tres se leen en el código, como en la C3 §7.

## 4. Potencial y terminación

$$\Phi=\sum_a\big(|L_a|-\text{siguiente}[a]\big)=\#\{(a,b): b\in L_a \text{ y } a \text{ todavía no le propuso a } b\}.$$

Al principio $\Phi=\sum_a|L_a|=:L$ (el total de las listas de proponentes). Cada vuelta es exactamente una propuesta nueva y baja $\Phi$ en 1. Además $\Phi\ge0$, y un proponente solo está en la cola si su término es $\ge1$. **El ciclo termina después de a lo sumo $L$ vueltas.**

Diferencia con la conferencia: allí había que demostrar aparte que `siguiente[a]` nunca se sale de la lista ("termina con un emparejamiento perfecto"). Aquí **sí puede agotarse**, y el algoritmo lo maneja dejando a ese proponente solo. Ya no se garantiza un emparejamiento perfecto, y no debe garantizarse, porque puede no existir uno aceptable.

## 5. Estabilidad

**Teorema.** El emparejamiento que devuelve el algoritmo es estable con la definición adaptada, para cualquier orden de ejecución.

**Demostración.** Por (I3), $M$ solo tiene parejas aceptables. Supongamos que $(a,b)$ bloquea $M$: son mutuamente aceptables, $a$ está solo o prefiere $b$ a $M(a)$, y $b$ está solo o prefiere $a$ a $M(b)$.

*Paso 1: $a$ le propuso a $b$.*
- Si $a$ tiene pareja $M(a)$ y prefiere $b$: por (I2), $a$ propone en orden decreciente y terminó con $M(a)$, así que antes le propuso a $b$.
- Si $a$ está solo: al terminar el ciclo, $a$ no está en la cola, así que agotó su lista y le propuso a todos, incluido $b$ (que está en $L_a$ porque son aceptables).

*Paso 2: $b$ terminó con alguien que prefiere a $a$.* Cuando $a$ le propuso a $b$, como $a\in L_b$, el receptor $b$ lo aceptó o lo rechazó por tener a alguien mejor. Si lo rechazó, $b$ ya estaba comprometido con alguien que prefiere a $a$. Si lo aceptó y $a$ no terminó con $b$, más tarde $b$ lo cambió por alguien que prefiere. En los dos casos, por (I1), $b$ termina comprometido (no solo) con alguien que prefiere a $a$.

Eso contradice la condición 3. ∎

**Respuesta:** sí, el resultado sigue siendo estable.

**Extra: sigue siendo óptimo para quien propone.** El mismo argumento del primer fallo de la C3 §9 funciona con un caso más. Si $b$ rechaza a un $a$ para el que es pareja válida, a cambio de $a'$, y en el emparejamiento estable $M'$ con $(a,b)\in M'$ el proponente $a'$ **está solo**, entonces $(a',b)$ bloquea $M'$: $a'$ lista a $b$ (le propuso) y prefiere $b$ a estar solo, y $b$ prefiere $a'$ a $a$.

## 6. Costo

$\le L$ propuestas, cada una $O(1)$ (con la tabla de rangos como diccionario, $O(1)$ esperado; con una matriz de rangos, $O(1)$ en el peor caso pero $O(n_An_B)$ de memoria). Construir los rangos cuesta $O(\sum_b|L_b|)$. Total: **lineal en el tamaño de la entrada** (la suma de los largos de las listas).

## 7. Casos de prueba y validación

Verificador de estabilidad con la definición adaptada, y enumerador de **todos** los emparejamientos (para instancias pequeñas):

> Código: [ejercicio-12.py](ejercicio-12.py), parte 2.

Un ejemplo a mano. $a_2$ solo lista a $b_0$, que lo tiene último, y termina solo:

> Código: [ejercicio-12.py](ejercicio-12.py), parte 3.

```text
resultado: {'a0': 'b1', 'a1': 'b0', 'a2': 'solo'} en 4 propuestas
pares bloqueantes: []
estables posibles: [[1, 0, None]]
```

**Pruebas al azar.** Listas incompletas en los dos lados, tamaños distintos y las tres estrategias de ejecución. Comprobamos que el resultado es estable, que no depende del orden, que es óptimo para los proponentes, que hay a lo sumo $L$ propuestas, y que todos los estables emparejan al mismo conjunto de personas (un resultado clásico, que verificamos experimentalmente):

> Código: [ejercicio-12.py](ejercicio-12.py), parte 4.

```text
1500 instancias: estable, independiente del orden, óptimo para proponentes, <= L propuestas, y mismos emparejados en todos los estables
```

## Resumen

- **Pareja bloqueante:** mutuamente aceptables, y cada uno está solo o prefiere al otro antes que a su pareja.
- **Algoritmo:** el receptor rechaza a quien no lista; quien agota su lista se queda solo.
- **Potencial:** propuestas que faltan, $\Phi=\sum_a(|L_a|-\text{siguiente}[a])\le L$.
- **Estable:** sí. Si $(a,b)$ bloqueara, $a$ le propuso a $b$ (por su orden, o porque agotó la lista), y $b$ terminó con alguien que prefiere.
