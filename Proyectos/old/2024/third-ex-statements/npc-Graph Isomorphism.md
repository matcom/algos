# DP

## Transformación de Redes de Esqueletos

Alex el nigromante se dedicaba a unir huesos de criaturas muertas para armar esqueletos bizarros. Cada hueso se une a al menos otro por conexiones mágicas y está nombrado con un número entero.

De pronto, moviendo huesos por aquí y por allá, creó una criatura tan horrorosa que parecía salida de la mismísima Australia, pero muerta. Alex sintió amor a primera vista, completa fascinación.

Con una criatura tan horrenda, el resto de sus creaciones palidecían en comparación, pero desmantelarlas representaba un desperdicio de componentes mágicos. De pronto se le ocurrió una idea. Quizás podía convertir alguna de sus otras criaturas en una copia (o al menos algo medio parecido) de esta bizarra genialidad sólo renombrando los huesos que las conformaban. Para él, una criatura es parecida a otra cuando todos sus huesos dos a dos están conectados a exactamente la misma cantidad de huesos y estos huesos conectados tienen los mismos nombres dos a dos.

Ayude a Alex a encontrar un método con el que saber si un esqueleto arbitrario puede convertirse en una copia parecida a su criatura favorita sólo cambiándole los nombres a sus huesos.

### Statement

Given two graphs, determine whether one graph can be transformed into the other by renaming vertices.

### Solution

Reduces from: Clique
Reduction Idea: Construct two graphs where the existence of a clique in one graph corresponds to an isomorphism in the other, allowing the determination of isomorphism through clique detection.
