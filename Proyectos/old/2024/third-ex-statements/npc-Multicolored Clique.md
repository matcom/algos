# DP

## Alianza de Robots Multicolores

En una futurística ciudad llena de robots, cada robot pertenece a una facción identificada por un color específico. Los robots de diferentes facciones están buscando formar una alianza estratégica. Esta alianza debe ser un grupo de robots donde todos estén conectados entre sí, y lo más importante: debe haber al menos un robot de cada color en esta alianza.

Dado un grafo donde cada vértice representa a un robot y cada vértice tiene un color que indica su facción, tu tarea es determinar si existe una "clique" (un grupo completamente conectado) que contenga al menos un robot de cada color.

¿Podrán los robots de todas las facciones unirse en una poderosa alianza multicolor?

### Statement

Given a graph where each vertex is assigned a color, does there exist a clique containing at least one vertex of each color?

### Solution

Reduces from: Clique
Reduction Idea: Transform an instance of the clique problem by assigning colors to vertices in a way that ensures finding a multicolored clique corresponds to finding a regular clique.
