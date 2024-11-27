# Problemas NP, NP-Completo, NP-Hard

Asumiendo que los siguientes problemas ya se han demostrado como NP-Completos:

- SAT
- 3-Sat
- Clique
- Conjunto independiente
- Vertex Cover
- Subset Sum
- Mochila
- Hamilton (Dirigido)
- Viajante

Demuestre que los siguientes problemas son NP-Hard o NP-Completos, según corresponda.

### Set cover

Dado un conjunto $X$ y una colección S de subconjuntos de $X$, el problema consiste en determinar si existe un subcolector $S' \subseteq S$ tal que cada elemento de $X$ aparezca exactamente una vez en los subconjuntos de $S'$.

### Clique

Un clique es un subgrafo completo dentro de un grafo. Formalmente, un clique en un grafo $G=(V,E)$ es un subconjunto de vértices $C \subseteq V$, tal que todos los pares de vértices en $C$ están conectados directamente por una arista. En otras palabras, todos los vértices del clique están mutuamente conectados.

Hallar el clique de mayor tamaño en un grafo.

### Cobertura de Clique

Dado un grafo $G=(V,E)$, una cobertura de cliques es un conjunto de cliques $\{C_1,C_2,…,C_k\}$ tal que cada arista $(u,v) \in E$ pertenece a al menos uno de estos cliques.

El objetivo del problema de cobertura de cliques es encontrar el número mínimo de cliques necesarios para cubrir todas las aristas del grafo.

### Numero Cromático

El número cromático de un grafo es el número mínimo de colores necesarios para colorear los vértices del grafo de manera que dos vértices adyacentes no compartan el mismo color.

Hallar el número cromático en un grafo.

### Conjunto Dominante

En un grafo $G=(V,E)$, un conjunto de vértices $D \subseteq V$ es un conjunto dominante si cada vértice de $V$ que no está en $D$ es adyacente a al menos un vértice en $D$.

Una partición de los vértices $V$ en $k$ conjuntos $D_1,D_2,…,D_k$​ es una partición domática si cada $D_i$​ (para $i=1,2,…,k$) es un conjunto dominante. El numero dominante es la cardinalidad del menor conjunto dominante de $G$.

Hallar el numero dominante de $G$.

### Número Domatic

El número de domatic de un grafo $G$, denotado como $domatic(G)$, es el número máximo $k$ tal que los vértices de $G$ pueden dividirse en $k$ conjuntos disjuntos $D_1,D_2,…,D_k$ donde cada $D_i$​ es dominante.

Hallar el número de Domatic de un grafo.

### Ancho de Banda

Dado un grafo $G=(V,E)$ y una disposición lineal de sus vértices representada como una función $f:V→\{1,2,…,|V|\}$, el ancho de banda de $G$ para esa disposición es:

$$max⁡\{|f(u)-f(v)| : (u,v) \in E\}$$

El problema consiste en encontrar una disposición $f$ que minimice este valor, es decir, reducir al mínimo la distancia máxima en la disposición lineal entre los extremos de las aristas del grafo.

### Retroalimentación de Vértices

Dado un grafo $G=(V,E)$, un conjunto de retroalimentación de vértices es un subconjunto de vértices $F \subseteq V$ tal que al eliminar todos los vértices en $F$ (y sus aristas incidentes), el grafo resultante no contiene ciclos (es un grafo acíclico o un bosque, si es no dirigido).

El objetivo del problema es encontrar el conjunto de retroalimentación de vértices de tamaño mínimo.

### Retroalimentación de Arcos

Dado un grafo $G=(V,E)$, un conjunto de retroalimentación de arcos es un subconjunto de arcos $F \subseteq E$ tal que al eliminar todos los arcos en $F$, el grafo resultante no contiene ciclos (es un grafo acíclico o un bosque, si es no dirigido).

El objetivo del problema es encontrar el conjunto de retroalimentación de arcos de tamaño mínimo.

### 3D Matching

El problema se basa en encontrar un emparejamiento dentro de un conjunto tridimensional.

Supongamos que tienes tres conjuntos disjuntos: $X$, $Y$, y $Z$, cada uno de tamaño $n$. También tienes un conjunto $T$ de ternas de la forma $(x,y,z)$, donde $x \in X$, $y \in Y$, y $z \in Z$.

El objetivo es determinar si existe un subconjunto de $T$ de tamaño $n$ (es decir, nn ternas) tal que cada elemento de $X$, $Y$, y $Z$ aparezca exactamente una vez en las ternas seleccionadas.

### Dimensión Bipartita

Para un grafo $G=(V,E)$, la dimensión bipartita $b(G)$ es el menor entero $k$ tal que las aristas de $G$ pueden particionarse en k conjuntos $E1,E2,…,Ek$ donde cada subgrafo $Gi=(V,Ei)$ es bipartito.

Determinar la dimensión bipartita de un grafo cualquiera.

### Numero de Intersección

Sea $G=(V,E)$ un grafo no dirigido con $V$ como el conjunto de vértices y $E$ como el conjunto de aristas. El número de intersección de $G$, denotado como $int(G)$, es el mínimo entre las cardinalidades de una colección de conjuntos $\{S_v​:v \in V\}$, tal que:

1. A cada vértice $v \in V$ se le asigna un conjunto $S_v$​.
2. Existe una arista $(u,v) \in E$ si y solo si $S_u \cap S_v \neq \emptyset$.

En otras palabras, el número de intersección mide cuántos conjuntos son necesarios para representar todas las relaciones (aristas) entre los vértices mediante intersecciones de conjuntos.

### Subgrafo Máximo Bipartito

El problema consiste en encontrar dado un grafo $G=(V,E)$ el subgrafo $G'=(V',E')$ con $V' \subseteq V$ y $E' \subseteq E$ de forma que $G'$ sea bipartito y $|E'|$ es máximo.

### Máximo Corte

Sea $G=(V,E)$ un grafo con aristas ponderadas. Un corte es una division de los vertices en dos conjuntos $T$ y $V-T$. El costo de un corte es la suma de los pesos de las aristas que van de $T$ a $V-T$. El problema trata de encontrar el corte de mayor costo de un grafo.
