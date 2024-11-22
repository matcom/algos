# DP

## Tesoro pirata

En una isla desierta, un grupo de piratas ha trazado un mapa lleno de senderos secretos. Cada sendero tiene un tesoro escondido en alguna parte de su trayecto. Los piratas de la tripulación del infame capitán Jack Navarro quieren esconderse en las intersecciones de los senderos para vigilar sus tesoros. En una intersección se pueden cruzar dos senderos o más. Todas las intersecciones tienen unas palmeras a las que los piratas se pueden encaramar. Mientras más alta la palmera, más difícil es subirse y por tanto más costo tiene.

Tu misión es ayudar a los piratas a encontrar el conjunto mínimo de intersecciones donde deben esconderse para poder vigilar todos los senderos que llevan a sus tesoros y que el costo de subirse en las palmas sea mínimo.

### Statement

Given a weighted graph, find the minimum weight subset of vertices that covers all edges.

### Solution

Reduces from: Vertex Cover
Reduction Idea: Transform the unweighted vertex cover problem into a weighted version by assigning weights based on the original vertex cover, ensuring that the minimum weight solution corresponds to the vertex cover.
