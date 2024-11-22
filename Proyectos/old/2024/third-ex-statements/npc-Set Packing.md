# DP

## Estrategia de Batallones en la Guerra

En medio de una gran guerra, los generales están planeando una estrategia con sus batallones. Cada batallón controla un área específica del territorio, y algunos de estos territorios pueden superponerse, lo que crea conflictos de control entre los batallones.

Dada una colección finita $C$ de territorios controlados por los batallones, y un número entero positivo $k \leq |C|$, tu misión es determinar si es posible organizar al menos $k$ batallones de manera que cada uno controle un territorio completamente distinto de los demás, es decir, sin superposiciones ni conflictos entre ellos.

### Statement

Dada una colección finita C de conjuntos y un entero positivo $k \leq |C|$. ¿Tiene C al menos k conjuntos mutuamente disjuntos?

### Solution

Reduces from: Exact Cover
Reduction Idea: Construct an instance of set packing from an exact cover problem by ensuring that the sets in the packing problem correspond to the subsets in the exact cover, maintaining disjointness.
