# DP

## La misión intergaláctica: El enigma de los subuniversos

En un rincón distante del universo conocido, la nave **Exploradora 7** se dirigía hacia una nebulosa olvidada, una región misteriosa que contenía fragmentos de realidades paralelas. El capitán **Zarath** y su equipo de científicos estaban encargados de resolver un antiguo enigma interdimensional dejado por una civilización extinta: la **Pregunta de los Subuniversos**.

En este sector del cosmos, se decía que existía un conjunto de **subuniversos**, cada uno representado por una dimensión alternativa al **Universo Primario** con algunas leyes físicas derivadas de este. Todas las leyes de cualquiera de los **subuniversos** estaban en el primario, pero no necesariamente los **subuniversos** tenían todas las leyes del **Universo primario**.

El objetivo de la misión era descubrir si era posible utilizar un subconjunto específico de estas dimensiones para reconstruir el **Universo Primario**, de forma que cada aspecto esencial de la realidad solo fuera influido por una dimensión alternativa única.

El ingeniero jefe **Kala**, mirando la pantalla de datos cuánticos (para que suenen más interesantes), exclamó: "¡El enigma está claro! Nos han dado un **conjunto maestro** de leyes, al que llamaremos $$ U $$ (**Universo Primario**), y una colección de dimensiones alternativas, a la que llamaremos $$ S $$. Ahora, la verdadera cuestión es: ¿podemos encontrar una subcolección de estas dimensiones, que cubra cada ley del **Universo Primario** exactamente una vez?"

El equipo de la **Exploradora 7** sabía que el destino de la misión, y quizás del propio universo, dependía de la respuesta correcta.

### Statement

Given a set $$ U $$ and a collection of subsets $$ S $$, is there a subcollection of $$ S $$ that covers every element of $$ U $$ exactly once?

### Solution

Reduces from: 3-SAT
Reduction Idea: Construct subsets corresponding to the literals in the clauses of a 3-SAT instance. Each subset contains elements representing the literals, ensuring that a satisfying assignment corresponds to an exact cover.
