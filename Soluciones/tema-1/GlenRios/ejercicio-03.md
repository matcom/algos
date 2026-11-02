# Problema 3 ★

**Enunciado.** Diseña una pila con una operación `mínimo` que cuesta $O(1)$ en el peor caso. Enuncia el invariante que la hace correcta y da el costo de cada operación.

## Solución formal

**Estructura.** Se utilizan dos pilas: `principal` y `minimos`.

- `push(x)`: se apila $x$ en `principal`. Si `minimos` está vacía o $x \le$ `minimos.top()`, se apila $x$ en `minimos`.
- `pop()`: se desapila $x$ de `principal`. Si $x =$ `minimos.top()`, se desapila de `minimos`. Se devuelve $x$.
- `min()`: se devuelve `minimos.top()`.

**Invariante.** En todo momento, si `principal` no está vacía, `minimos.top()` es el mínimo de todos los elementos de `principal`. Además, `minimos` nunca está vacía cuando `principal` no lo está.

**Demostración del invariante.** Por inducción sobre el número de operaciones.

- *Inicialización:* ambas pilas están vacías, el invariante se cumple trivialmente.
- *Mantenimiento:*
  - En `push(x)`, el nuevo mínimo de `principal` es $\min(x, \text{mínimo anterior})$. Si $x$ es menor o igual que el mínimo anterior, se apila en `minimos`, quedando como nuevo tope; en caso contrario, el tope anterior sigue siendo el mínimo.
  - En `pop()`, si se elimina el mínimo actual, se desapila también de `minimos`, quedando en el tope el mínimo de los elementos restantes.
- *Conclusión:* al finalizar cualquier secuencia de operaciones, el invariante se mantiene.

**Costos.**

- `push`: $O(1)$ (a lo sumo 2 apilamientos).
- `pop`: $O(1)$ (a lo sumo 1 desapilamiento extra).
- `min`: $O(1)$.
- Memoria extra: $O(n)$.
