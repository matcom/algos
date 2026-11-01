## Pregunta 12

 Gale-Shapley con listas incompletas: cada proponente lista solo a algunos receptores, y prefiere quedarse solo antes que con uno que no listó. Adapta el algoritmo, su potencial y la definición de pareja bloqueante. ¿Sigue siendo estable el resultado? Demuéstralo. (C3)

---

## Adapta el algoritmo

**Modelo.** Sea $M$ el conjunto de proponentes y $W$ el de receptores. Cada $m \in M$ tiene una lista $L(m) \subseteq W$ ordenada estrictamente por preferencia. Decimos que $w$ es *aceptable* para $m$ si $w \in L(m)$. Un proponente prefiere cualquier $w \in L(m)$ a quedarse solo, y prefiere quedarse solo a cualquier $w \notin L(m)$. Los receptores ordenan estrictamente a los proponentes y prefieren a cualquiera de ellos a quedarse solos. (Si los receptores también tuvieran listas incompletas, la prueba es idéntica, con aceptabilidad mutua.)

**Cambio respecto al algoritmo clásico.** Un proponente puede agotar su lista sin haber conseguido pareja. En ese caso termina soltero, en lugar de proponer a una receptora que no listó.

**Algoritmo.**

```
Para cada m: p(m) ← 1          (posición de su próxima propuesta en L(m))
μ ← ∅                          (emparejamiento vacío)
Mientras exista m libre con p(m) ≤ |L(m)|:
    w ← L(m)[p(m)];  p(m) ← p(m) + 1
    si w está libre:
        μ ← μ ∪ {(m,w)}
    sino, sea m' = μ(w):
        si w prefiere m a m':
            μ ← (μ \ {(m',w)}) ∪ {(m,w)}      (m' queda libre)
        sino: m es rechazado (sigue libre)
Devolver μ
```

**Observaciones básicas.**
- Cada proponente propone en orden decreciente de preferencia y nunca repite receptora, porque $p(m)$ solo crece.
- Solo se propone a receptoras listadas, así que nadie queda emparejado con alguien inaceptable.
- $\mu$ es un emparejamiento válido: $m$ propone solo cuando está libre, y $w$ tiene a lo sumo una pareja, ya que cuando acepta a un nuevo $m$ suelta al anterior.
- Al terminar, cada proponente libre ha agotado su lista, es decir, ha propuesto a todas las receptoras de $L(m)$ y todas lo han rechazado o dejado.

---

## El Potencial

**Definición.** Para cada proponente $m$ sea $k_m$ el número de propuestas que ha hecho hasta ahora. Definimos

$$\Phi \;=\; \sum_{m \in M} \bigl(|L(m)| - k_m\bigr),$$

que es el número total de propuestas que aún quedan por hacer, es decir, las entradas de las listas no recorridas. El potencial original (número de pares no propuestos, $n^2$ al inicio) es el caso particular de listas completas.

**Teorema.** El algoritmo termina tras a lo sumo $\Phi_0 = \sum_{m}|L(m)|$ iteraciones, y $\Phi_0 \le n^2$ si $|M|=|W|=n$.

**Demostración.**
1. *Valor inicial.* $k_m = 0$ para todo $m$, luego $\Phi_0 = \sum_m |L(m)|$.
2. *Es entero y no negativo.* Un proponente solo propone si $p(m) \le |L(m)|$, es decir, si $k_m < |L(m)|$. Entonces $k_m \le |L(m)|$ siempre y cada sumando es $\ge 0$.
3. *Decrece estrictamente.* En cada iteración se elige un $m$ libre con $k_m < |L(m)|$ y se hace exactamente una propuesta. Solo cambia $k_m \mapsto k_m + 1$, así que $\Phi$ baja exactamente en 1, sea cual sea la respuesta de $w$ (acepta, desplaza o rechaza). Los demás $k_{m'}$ no cambian: que $m'$ quede libre no altera su $k_{m'}$.
4. *Conclusión.* Una sucesión de enteros no negativos que baja 1 en cada iteración no puede tener más de $\Phi_0$ iteraciones. Cuando el bucle se detiene, no existe un proponente libre con propuestas pendientes. $\blacksquare$

La complejidad es $O\!\left(\sum_m |L(m)|\right)$, que es lineal en el tamaño de la entrada, siempre que se guarde el ranking de cada receptora en una tabla para comparar en $O(1)$.

---

## La definición de pareja bloqueante

**Idea intuitiva.** Un par $(m,w)$ que no está emparejado entre sí es *bloqueante* si ambos preferirían estar juntos antes que con lo que tienen ahora. Si existiera, tendrían un incentivo para abandonar sus parejas y romper el emparejamiento. Un emparejamiento estable es aquel donde esto no puede pasar.

**Definición adaptada.** Sea $\mu$ un emparejamiento y escribimos $\mu(m)=\varnothing$ si $m$ está solo. El par $(m,w)$ es **bloqueante** para $\mu$ si se cumplen las tres condiciones:

1. $w \in L(m)$, es decir, $w$ es aceptable para $m$.
2. $m$ prefiere $w$ a su situación actual: $\mu(m)=\varnothing$, o $\mu(m)\in L(m)$ y $w$ está por encima de $\mu(m)$ en la lista de $m$.
3. $w$ prefiere $m$ a su situación actual: $\mu(w)=\varnothing$, o $w$ ordena a $m$ por encima de $\mu(w)$.

**Qué cambia.** La condición 1 es nueva. Un proponente soltero con $w$ en su lista y una $w$ que lo prefiere a su pareja forman un bloqueo, porque $m$ prefiere cualquier listada a estar solo. En cambio, $m$ nunca bloquea con una receptora que no listó, porque prefiere estar solo a estar con ella.

**Ejemplo.** Sea $L(m_1)=(w_1)$ y $L(m_2)=(w_1,w_2)$, y supongamos que $w_1$ prefiere $m_2$ a $m_1$. Tomemos $\mu=\{(m_1,w_1)\}$, con $m_2$ solo. Entonces $(m_2,w_1)$ es bloqueante: $w_1\in L(m_2)$, $m_2$ está solo y prefiere $w_1$, y $w_1$ prefiere $m_2$ a $m_1$. En cambio, el par $(m_1, w_2)$ no lo es, porque $w_2\notin L(m_1)$.

**Definición de estabilidad.** $\mu$ es **estable** si:
- (a) es *individualmente racional*: nadie está emparejado con una pareja inaceptable, y
- (b) no tiene ninguna pareja bloqueante.

---

## ¿Sigue siendo estable el resultado?

**Sí.** El emparejamiento $\mu$ que devuelve el algoritmo adaptado es estable.

**Lema 1 (las receptoras solo mejoran).** Si una receptora $w$ recibe alguna propuesta, desde ese momento está emparejada hasta el final, y su pareja solo cambia a otra que ella prefiere estrictamente.

*Prueba.* La primera propuesta que recibe se acepta porque estaba libre. Después, $w$ solo cambia de pareja en la rama "$w$ prefiere $m$ a $m'$", es decir, sustituye $m'$ por un $m$ estrictamente mejor. Nunca queda libre. $\square$

**Lema 2 (los proponentes bajan por su lista).** Cada $m$ propone en el orden de $L(m)$. Si al final $m$ está emparejado con $\mu(m)$, ha propuesto a todas las que están por encima de $\mu(m)$ en su lista, y todas lo rechazaron o lo dejaron. Si termina libre, ha propuesto a todas las de $L(m)$.

*Prueba.* Es consecuencia de que el puntero $p(m)$ solo avanza y de la condición de parada. $\square$

**Teorema.** $\mu$ es estable.

**Demostración.**

*(a) Racionalidad individual.* Cada $m$ propone solo a elementos de $L(m)$, así que si $(m,w)\in\mu$, entonces $w\in L(m)$. Las receptoras prefieren a cualquier proponente a estar solas. Luego nadie está con una pareja inaceptable.

*(b) Ausencia de parejas bloqueantes.* Supongamos, por contradicción, que $(m,w)$ es bloqueante para $\mu$.

Por la condición 1, $w \in L(m)$. Por la condición 2, $m$ prefiere $w$ a $\mu(m)$, y hay dos casos:

- Si $m$ termina libre, por el Lema 2 propuso a todas las receptoras de $L(m)$, en particular a $w$.
- Si $m$ termina con $\mu(m)$ por debajo de $w$ en su lista, por el Lema 2 propuso a $w$ antes que a $\mu(m)$.

En ambos casos **$m$ le propuso a $w$ en algún momento**. Cuando eso ocurrió, hay solo dos posibilidades:

- *$w$ rechazó a $m$*: estaba con una pareja $m^{*}$ que prefería estrictamente a $m$.
- *$w$ aceptó a $m$ y más tarde lo dejó*: lo sustituyó por un $m^{*}$ que prefiere estrictamente a $m$.

En ambos casos, justo después de esa interacción $w$ está emparejada con un $m^{*}\succ_w m$. Por el Lema 1, su pareja final $\mu(w)$ es igual a $m^{*}$ o mejor para ella que $m^{*}$. Por transitividad, $\mu(w) \succ_w m$, de modo que $w$ **no** prefiere $m$ a $\mu(w)$ (y en particular $w$ no está libre al final). Esto contradice la condición 3 del par bloqueante.

Por tanto no existe ninguna pareja bloqueante, y junto con (a), $\mu$ es estable. $\blacksquare$

**Comentario final.** El resultado clásico se conserva. Con listas incompletas puede haber proponentes (y receptoras) sin pareja, pero esto no rompe la estabilidad: un proponente soltero ya intentó con todas las receptoras que acepta, y ninguna lo prefiere a lo que tiene. Además, el emparejamiento es óptimo para los proponentes entre todos los estables, y el conjunto de agentes solteros es el mismo en todos los emparejamientos estables (teorema de los hospitales rurales).

## Código

**`fig1_modelo_listas_incompletas.png` (el problema).** Muestra el grafo bipartito de la instancia de ejemplo, con 4 proponentes y 4 receptores. Cada línea gris es una receptora listada, con su posición en la lista del proponente. Las líneas rojas punteadas con × son receptoras que el proponente no listó, con las que prefiere quedarse solo. A los lados aparecen las listas L(m) y las preferencias completas de cada receptora.

**`fig2_algoritmo_flujo.png` (Adapta el algoritmo).** Es el diagrama de flujo del algoritmo adaptado. Repite mientras exista un proponente libre con propuestas pendientes (p(m) ≤ |L(m)|), propone a la siguiente de su lista, y la receptora acepta, sustituye a su pareja o rechaza. Se resalta el cambio clave: solo se propone a listadas, y quien agota su lista termina soltero.

**`fig3_traza_algoritmo.gif` (animación paso a paso).** Ejecuta el algoritmo sobre la instancia de la figura 1, un paso por fotograma. Azul indica que la receptora acepta, naranja que desplaza a su pareja, rojo que rechaza, y verde marca las parejas actuales. Cada fotograma muestra el valor de Φ. El último fotograma da el resultado μ = {(m1,w2), (m2,w3), (m3,w1)}, con m4 y w4 solos.

**`fig4_potencial.png` (El Potencial).** A la izquierda, Φ(t) baja exactamente 1 en cada iteración, desde Φ₀ = 7 hasta 1, sin llegar nunca por debajo de 0. A la derecha, el mismo Φ(t) se descompone por proponente (|L(m)| − k_m) como una pila de barras que se va vaciando. Esto ilustra por qué hay a lo sumo Φ₀ iteraciones.

**`fig5_pareja_bloqueante.png` (definición de pareja bloqueante).** A la izquierda hay un ejemplo con μ = {(m1,w1)}. El par (m2,w1) es bloqueante porque m2 está solo, w1 está en su lista y w1 prefiere a m2. El par (m1,w2) no bloquea porque w2 no está en L(m1). A la derecha están las 3 condiciones de la definición adaptada y la definición de estabilidad.

**`fig6_demostracion_estabilidad.png` (¿Sigue siendo estable?).** Es el esquema de la demostración por contradicción. Si (m,w) fuera bloqueante, m le habría propuesto a w. Entonces w lo rechazó o lo sustituyó por un m* mejor para ella. Como la pareja de w solo mejora (Lema 1), μ(w) es mejor que m, lo cual contradice la condición 3. Concluye que no existe pareja bloqueante.

**`fig7_verificacion_experimental.png` (comprobación experimental).** Corre el algoritmo sobre 500 instancias aleatorias con listas incompletas (n = 8). A la izquierda, todas las ejecuciones quedan por debajo de la cota de iteraciones Φ₀. A la derecha, el algoritmo produjo pares bloqueantes en 0 de 500 instancias, mientras que un emparejamiento aleatorio válido los tuvo en las 500. Esto no sustituye a la demostración formal, pero la respalda.