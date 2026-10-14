## Ejercicio 13 ★★ — Splay tree en camino con accesos ordenados

### Enunciado con modelo

> En un splay tree que empieza como un camino de n nodos se accede a las claves 1, …, n en orden. Acota el costo total con el lema de acceso y la cuenta de la sección 5 de la conferencia 4, y compáralo con lo que mide la sección 6. ¿Es ajustada la cota? (C4)

**Modelo.** Splay tree con el potencial Φ = Σ log₂ s(x), donde s(x) es el número de nodos del subárbol de x. El costo de un acceso es el número de rotaciones. Trabajamos con el modelo de la Conferencia 4, secciones 4 a 6.

**Precisión del problema.** El splay tree empieza como un **camino**: n es la raíz, y cada clave i es hija izquierda de i+1. Esto significa que el árbol es una cadena 1 → 2 → … → n, con n en la raíz y 1 en la hoja más profunda. Se accede a las claves 1, 2, …, n en orden, una vez cada una.

### Cota con el lema de acceso

**Lema de acceso (Sleator y Tarjan).** El costo amortizado de hacer splay de un nodo x en un árbol con raíz t es a lo sumo 3(r(t) - r(x)) + 1 = O(log n), donde r(x) = log₂ s(x).

**Costo total de m accesos.** Para m accesos, la suma telescopia:

Σ cᵢ ≤ Σ (3(r(t) - r(xᵢ)) + 1) = 3 Σ (log₂ n - r(xᵢ)) + m.

Como r(xᵢ) ≥ 0, esto es a lo sumo 3m log₂ n + m = **O(m log n)**.

**Para m = n accesos, el costo total es O(n log n).**

### Cuenta con la sección 5

La sección 5 de la Conferencia 4 da la cuenta exacta del lema de acceso. Para el camino inicial, el potencial Φ₀ = Σ log₂ s(x) = log₂ n! ≈ n log₂ n. Después de los n accesos, el potencial Φ_final es el de un árbol balanceado, que es Θ(n).

La suma telescopia:

Σ cᵢ = Σ ĉᵢ - (Φ_final - Φ₀) ≤ n(3 log₂ n + 1) + Φ₀ = n(3 log₂ n + 1) + n log₂ n = **O(n log n)**.

### Comparación con la sección 6

La sección 6 de la Conferencia 4 mide el costo por acceso para splay y para subir a la raíz, con n = 100, 200, 400, 800, sobre **tres rondas completas** de accesos ordenados.

| n | splay | subir a la raíz | log₂ n |
|---|-------|-----------------|--------|
| 100 | 4.2 | 50.5 | 6.6 |
| 200 | 4.2 | 100.5 | 7.6 |
| 400 | 4.3 | 200.5 | 8.6 |
| 800 | 4.4 | 400.5 | 9.6 |

**Splay es plano:** el costo por acceso es ~4.2, independiente de n. **Subir a la raíz tiene pendiente 1:** el costo por acceso es ~n/2, que es Θ(n).

### ¿Es ajustada la cota O(n log n)?

**No, la cota es holgada.** El lema de acceso da O(n log n) para n accesos, pero el experimento mide ~4.2 rotaciones por acceso, que es **constante**. El costo total real es ~4.2n, no n log n. La cota O(n log n) es correcta pero no ajustada.

**¿Por qué la cota es holgada?** Porque el lema de acceso es para el peor caso sobre cualquier secuencia de accesos. La secuencia ordenada 1, 2, …, n es un caso favorable para splay: después del primer acceso a 1, el árbol se reorganiza de forma que los accesos siguientes son baratos. La cota O(n log n) cubre el peor caso, que no es esta secuencia.

**La cota ajustada para esta secuencia es Θ(n).** El experimento lo confirma: ~4.2n rotaciones en total.

### Costo

- **Cota del lema de acceso:** O(n log n) para n accesos.
- **Costo real medido:** ~4.2n para n accesos, que es Θ(n).
- **La cota es correcta pero no ajustada.**

### Cota mínima

Cada acceso debe al menos llegar al nodo, así que Ω(1) por acceso, Ω(n) en total. El splay hace Θ(n) en esta secuencia, que es óptimo.

### Código

**Archivo:** `codigo/ejercicio-13.py`

### Figura
**Archivo** ![](figuras/ejercicio-13-splay.png)
### Casos de prueba

| n | Splay | Subir a la raíz | log₂ n |
|---|-------|-----------------|--------|
| 100 | 4.2 | 50.5 | 6.6 |
| 200 | 4.2 | 100.5 | 7.6 |
| 400 | 4.3 | 200.5 | 8.6 |
| 800 | 4.4 | 400.5 | 9.6 |

**Splay es plano (~4.2), subir a la raíz tiene pendiente 1 (~n/2).** La cota O(n log n) del lema de acceso es holgada: el costo real es Θ(n).

### Conclusión

El lema de acceso da una cota O(n log n) para n accesos ordenados en un splay tree que empieza como camino. La cota es correcta pero **no ajustada**: el experimento mide ~4.2 rotaciones por acceso, que es Θ(n) en total, no Θ(n log n). La razón es que la secuencia ordenada es un caso favorable para splay: después del primer acceso a 1, el árbol se reorganiza y los accesos siguientes son baratos. La cota O(n log n) cubre el peor caso sobre cualquier secuencia, que no es esta.
