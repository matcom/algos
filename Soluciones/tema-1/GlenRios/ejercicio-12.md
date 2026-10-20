# Problema 12 ★★★

**Enunciado.** Gale-Shapley con listas incompletas: cada proponente lista solo a algunos receptores, y prefiere quedarse solo antes que con uno que no listó. Adapta el algoritmo, su potencial y la definición de pareja bloqueante. ¿Sigue siendo estable el resultado? Demuéstralo.

## Solución formal

**El problema.** Hay $n$ proponentes $a_1, \ldots, a_n$ y $n$ receptores $b_1, \ldots, b_n$. Cada proponente tiene una lista $L(a) \subseteq \{b_1, \ldots, b_n\}$ de receptores aceptables, ordenada estrictamente por preferencia. Cada receptor tiene una lista $L(b) \subseteq \{a_1, \ldots, a_n\}$ de proponentes aceptables, ordenada estrictamente. Un proponente prefiere quedarse solo antes que emparejarse con alguien que no esté en su lista; lo mismo para los receptores.

Un emparejamiento $M$ es una función parcial inyectiva que asigna a algunos proponentes un receptor y deja a otros solos, respetando que $b \in L(a)$ y $a \in L(b)$ para todo par $(a, b) \in M$.

**Pareja bloqueante.** Un par $(a, b)$ es bloqueante si se cumplen estas dos condiciones:
1. **Son mutuamente aceptables:** $b \in L(a)$ y $a \in L(b)$.
2. **Ambos prefieren estar juntos antes que con su situación actual.** Esto se traduce en alguna de estas cuatro posibilidades:
   - **Caso 1 (ambos solos):** $a$ está solo en $M$, y $b$ está sola en $M$.
   - **Caso 2 ($a$ solo, $b$ con pareja):** $a$ está solo en $M$, y $b$ está emparejada con $a' \neq a$ pero prefiere a $a$ (es decir, $a$ aparece antes que $a'$ en $L(b)$).
   - **Caso 3 ($a$ con pareja, $b$ sola):** $a$ está emparejado con $b' \neq b$ pero prefiere a $b$ (es decir, $b$ aparece antes que $b'$ en $L(a)$), y $b$ está sola en $M$.
   - **Caso 4 (ambos con pareja):** $a$ está emparejado con $b' \neq b$ y prefiere a $b$; y $b$ está emparejada con $a' \neq a$ y prefiere a $a$.

**Algoritmo adaptado**: Igual que Gale-Shapley pero:
- Un proponente $a$ solo propone a receptores de $L(a)$, en orden decreciente de preferencia.
- Un receptor $b$ solo acepta propuestas de proponentes en $L(b)$.
- Si $b$ recibe una propuesta de alguien que no está en $L(b)$, la rechaza.
- El algoritmo termina cuando no hay ningún proponente libre con receptores sin proponer en su lista.

**Potencial.** Sea
$$
\Phi = \bigl|\{\,(a, b) : b \in L(a),\ a \text{ todavía no le ha propuesto a } b\,\}\bigr|.
$$
Inicialmente $\Phi = \sum_a |L(a)| \le n^2$. Cada propuesta reduce $\Phi$ en 1, porque $a$ avanza al siguiente receptor de su lista. Como $\Phi \ge 0$, el número total de propuestas es a lo sumo $n^2$, y el algoritmo termina.

**Estabilidad.** Usamos el truco del dummy. Añadimos un receptor ficticio $b_0$ que cada proponente coloca al final de su lista, y un proponente ficticio $a_0$ que cada receptor coloca al final de su lista. Ahora todas las listas son completas. Corremos Gale-Shapley con las listas extendidas. El resultado es un emparejamiento $M'$ que empareja a todos (posiblemente con dummies).

Por el teorema clásico de Gale-Shapley, $M'$ es estable en el problema extendido: no existe un par $(a, b)$ con $b \in L(a) \cup \{b_0\}$ y $a \in L(b) \cup \{a_0\}$ tal que $a$ prefiera $b$ a $M'(a)$ y $b$ prefiera $a$ a $M'(b)$.

Al quitar los dummies, obtenemos un emparejamiento $M$ del problema original. Supongamos que $(a, b)$ es una pareja bloqueante en el original. Entonces $b \in L(a)$, $a \in L(b)$, y se cumple alguno de los 4 casos anteriores.

- Si $a$ está solo en $M$, entonces en $M'$ está emparejado con $b_0$. Como $b \in L(a)$, $a$ prefiere $b$ a $b_0$. Así que $a$ prefiere $b$ a $M'(a)$.
- Si $a$ está emparejado en $M$ con alguien peor que $b$, lo mismo: prefiere $b$ a $M'(a)$.
- Análogamente, $b$ prefiere $a$ a $M'(b)$.

Entonces $(a, b)$ sería una pareja bloqueante en el problema extendido, contradiciendo la estabilidad de $M'$. Por tanto, no existe pareja bloqueante en el original: $M$ es estable. $\square$

**Conclusión.** El algoritmo adaptado termina en a lo sumo $n^2$ propuestas y produce un emparejamiento estable, aunque no necesariamente perfecto: algunos proponentes o receptores pueden quedar solos. La definición de pareja bloqueante se adapta tratando "estar solo" como peor que cualquier pareja aceptable. La demostración se reduce al caso completo con el truco del dummy.