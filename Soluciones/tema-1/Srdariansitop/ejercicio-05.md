# Pregunta 5 :
Detección de ciclos en una lista enlazada con dos punteros que avanzan a velocidades 1 y 2 (algoritmo de Floyd). Demuestra que se encuentran si y solo si hay un ciclo, con un invariante, y que termina, con un potencial. Da el costo.


## Sección 1. Modelo y lema clave

**Modelo.** Sea `f` = `next`. Definimos la sucesión de nodos a_i = fⁱ(h), mientras esté definida (a_{i+1} = nil si a_i es el último nodo). Solo hay dos casos posibles:

- **Caso A (sin ciclo):** existe un índice n con a_n = nil. Los nodos a_0, …, a_{n−1} son los n nodos de la lista.
- **Caso B (con ciclo):** la sucesión es infinita. Sean μ ≥ 0 (cola) y λ ≥ 1 (ciclo) los menores valores tales que a_{i+λ} = a_i para todo i ≥ μ. Los nodos a_0, …, a_{μ+λ−1} son distintos y n = μ + λ.

**Lema (caracterización de colisiones).** Sean i < j con ambos nodos definidos.

> a_i = a_j ⟺ estamos en el caso B, i ≥ μ y λ | (j − i).

*Demostración.*

- (⇐) Es la definición de μ y λ: para i ≥ μ, a_{i+mλ} = a_i para todo m ≥ 0.
- (⇒) Si a_i = a_j con i < j, entonces a_{i+m} = a_{j+m} para todo m (determinismo de `f`). La sucesión es periódica desde i y nunca llega a nil, luego estamos en el caso B. Por minimalidad de μ, i ≥ μ. Además, j − i es un período de la sucesión desde i, y los períodos son exactamente los múltiplos de λ (el período mínimo divide a todos los demás), luego λ | (j − i). ∎

*(En el caso A los nodos son todos distintos: a_i ≠ a_j siempre que i ≠ j.)*

---

## Sección 2. Invariante y corrección

**Invariante I(k).** Si el bucle completa k iteraciones sin devolver nada, entonces

> t = a_k, l = a_{2k}, y los nodos a_0, …, a_{2k} están definidos (no son nil).

*Demostración por inducción en k.*

- **Base (k = 0):** t = l = h = a_0.
- **Paso:** supongamos I(k) y que se entra a la iteración k+1. La guarda asegura l ≠ nil y l.next ≠ nil, o sea a_{2k+1} está definido. Entonces t ← t.next = a_{k+1} y l ← l.next.next = a_{2k+2} (definido o nil). Se cumple I(k+1) si el programa continúa, pues la guarda de la siguiente vuelta ya exige su definición. ∎

*Interpretación:* la liebre lleva a la tortuga una ventaja de exactamente k nodos, que crece **de 1 en 1** cada iteración.

**Teorema de corrección.** El algoritmo devuelve VERDADERO ⟺ la lista tiene ciclo.

*Demostración.* La iteración k ≥ 1 devuelve VERDADERO ⟺ a_k = a_{2k}. Como k < 2k, el Lema da:

> a_k = a_{2k} ⟺ (caso B) ∧ k ≥ μ ∧ λ | (2k − k) = k.

- **(⇒) Solo si hay ciclo.** Si devuelve VERDADERO, a_k = a_{2k} con k ≠ 2k (k ≥ 1), y por el Lema estamos en el caso B.
- **(⇐) Si hay ciclo, se encuentran.** En el caso B, todos los a_i están definidos, así que la guarda nunca falla. Basta mostrar que existe k ≥ 1 con k ≥ μ y λ | k. Tomamos

> k\* = λ · max(1, ⌈μ/λ⌉)

que es múltiplo de λ, es ≥ 1 y es ≥ μ. En k\* (o antes, si hay un k menor que cumpla lo mismo) se devuelve VERDADERO. ∎

**Por qué funciona (intuición de la ventaja).** Dentro del ciclo, la distancia de la tortuga a la liebre es D_k = k mod λ. Como cambia de 1 en 1, recorre todos los residuos 0, 1, …, λ−1 sin saltarse el 0. Con velocidades 1 y 3 la distancia cambiaría de 2 en 2 y, con λ par, podría no tocar nunca el 0.

---

## Sección 3. Potencial, terminación y costo

### Potencial

**Caso A (sin ciclo).** Φ_k = n − 2k (nodos que faltan a la liebre para salir de la lista).

- Φ es un entero y decrece exactamente 2 por iteración.
- La guarda requiere que a_{2k+1} exista, es decir 2k + 1 ≤ n − 1, o sea **Φ_k ≥ 2**. Cuando Φ < 2 la guarda falla y el bucle termina.
- Por tanto el bucle hace exactamente ⌊n/2⌋ iteraciones y devuelve FALSO. (Nunca devuelve VERDADERO por el Lema.)

**Caso B (con ciclo).** Ψ_k = k\* − k, con k\* definido arriba.

- Mientras k < k\*, Ψ_k > 0 y la guarda no falla.
- Se descompone en dos fases, que explican de dónde sale:
  - *Fase 1 (tortuga en la cola):* hacen falta μ − k pasos para que la tortuga entre al ciclo.
  - *Fase 2 (ambas en el ciclo):* Ψ = (−k) mod λ es la distancia que le falta a la liebre para alcanzar a la tortuga. Decrece 1 por iteración y llega a 0 en a lo sumo λ − 1 pasos.
- Ψ es un entero ≥ 0 que decrece **exactamente 1 por iteración**, y al llegar a 0 se tiene k = k\* y se devuelve VERDADERO.

En ambos casos hay un entero acotado inferiormente que disminuye estrictamente en cada iteración, por lo que **el algoritmo siempre termina**.

### Costo

**Cota de iteraciones.** En el caso B:

- Si μ ≥ 1: μ ≤ k\* < μ + λ, luego k\* ≤ μ + λ − 1 < n.
- Si μ = 0: k\* = λ = n.

Entonces k\* ≤ n en todos los casos.

| Caso | Iteraciones | Avances de puntero |
|---|---|---|
| Sin ciclo | ⌊n/2⌋ | 3 por iteración, ≤ 1.5n |
| Con ciclo | k\* ≤ n | 3 por iteración, ≤ 3n |

- **Tiempo:** cada iteración hace 3 avances, 1 comparación y la guarda, todo O(1). Total **Θ(n)** en el peor caso (con n = μ + λ).
- **Espacio:** solo dos punteros, **O(1)**. Frente al método con tabla hash (O(n) de espacio) esta es su ventaja.

**Conclusión.** El invariante (t = a_k, l = a_{2k}) reduce "se encuentran" a la ecuación a_k = a_{2k}. El Lema la convierte en "hay ciclo ∧ k ≥ μ ∧ λ | k", lo que prueba el si y solo si. El potencial (n − 2k sin ciclo; k\* − k con ciclo) garantiza terminación en O(n) tiempo y O(1) espacio.

## Codigo (Extra 05)

El script genera, para cada caso del teorema, un **GIF animado** (un cuadro por iteración) y un **PNG** con el último cuadro. Con ciclo (μ=3, λ=5) la tortuga y la liebre se encuentran en k\* = 5; sin ciclo (n=7) la guarda `l.next ≠ nil` falla y devuelve FALSO. En cada cuadro se recalculan el invariante (t = a_k, l = a_2k), la distancia D = k mod λ y el potencial (Ψ = k\* − k con ciclo, Φ = n − 2k sin ciclo), así que se ve cómo se cumple la demostración paso a paso. Se usan dos casos porque el teorema tiene dos ramas, y los valores se eligieron para ejercitar los detalles clave: μ=3 y λ=5 muestran que la tortuga entra al ciclo antes del encuentro, y n=7 (impar) hace que la liebre se detenga sobre el último nodo y no sobre `nil`. Estas animaciones ilustran, pero no sustituyen la demostración formal, porque un ejemplo no prueba el caso general.