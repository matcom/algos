# Algoritmos de grafos

## Nociones elementales

- Definición de grafo
  - Nodo
  - Arista
  - In-degree, out-degree
- Representaciones computacionales de grafos
  - Lista de adyacencia
  - Matriz de adyacencia
  - Matriz de incidencia
- Grafos dirigidos y no-dirigidos
- Grafos ponderados
- Multigrafos

## Algoritmos de búsqueda

- Búsqueda no informada
  - No ponderada
    - BFS
    - DFS
  - Ponderada
    - Costo uniforme (Djikstra)

- Búsqueda informada (los vimos en IA)
  - Greedy
  - A*, Bidirectional A*, ...

## Estructura

- Orden topológico
  En un DAG, obtener un orden donde cada nodo ocurra antes que sus predecesores.

- Componentes conexas (no-dirigido) y fuertemente conexas (dirigido)
  Dividir el grafo en subgrafos donde todos los nodos están conectados.

## Minimum spanning tree

- Definición de árbol abarcador
- Noción de corte, arista de cruce, arista segura
- Algoritmos
  - Genérico: encontrar mágicamente una arista segura
  - Kruskal: escoger la arista de menor peso que une cualquiera de los árboles MST.
    Ordenar las aristas por peso, usar un disjoint-set para encontrar la menor arista que no crea un ciclo
  - Prim: escoger la arista de menor peso que añade un nuevo nodo al MST
    Usar un heap para escoger el nodo más cercano al corte

## Shortest paths

- Tipos de problemas
  - Single-source single-destination
  - Single-source multiple-destination
  - All-pairs

- Propiedades
  - Subestructura óptima
  - Aristas de costo negativo (ciclos de costo negativo)
  - Caminos simples

- Relajación
  Si en el camino (s,v) la arista (u,v) permite disminuir el costo de s~v

- Algoritmos
  - Relajación:
    - Bellman-Ford: relajar todas las aristas de forma consecutiva N-1 veces
    - DAG: relajar los vértices en orden topológico
    - Dijsktra: escoger el vértice menor que cruza el corte y relajar todas las artistas
  - Floyd-Warshall: resolver dinámicamente el mejor camino i~j con a lo sumo k vértices
