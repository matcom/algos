---
author:
- Rodrigo
---

Sheyla, Lázaro y la libreta de chismes.

A Sheyla le gusta el chisme. De hecho, le gusta a tal punto que tiene
una libreta con todos los secretos de su aula de los que se ha ido
enterando con el paso de los años. Los chismes da la libreta están
ordenados por tiempo de descubrimiento y separados en 8 categorías
distintas (vergonzoso, para enorgullecerse, amoroso, etc).

Por otro lado, las vueltas de la vida han llevado a Lázaro a volverse
presidente del aula y, para mantener su poder, ha decidido que
resultaría conveniente conocer secretos de sus compañeros (quéin sabe,
pueden resultar útiles) y le ha pedido ayuda a Sheyla. Sin embargo,
Lázaro es un poco raro y también ha decidido que no necesita todos los
secretos de la libreta, sino un subconjunto de estos que cumpla con las
siguientes condiciones:

Sea $A$ una cadena con enteros entre 1 y 8. Cada índice representa un
chisme de la libreta (en el mismo orden en que aparece) y cada valor
representa el tipo de chisme asociado a este. Además, la cadena $S$
representa el subconjunto que Lázaro quiere conocer.

-   Para cada par de tipos de chismes $t_1$, $t_2$ distintos, La
    cantidad de chismes de tipo $t_1$ en $S$ puede diferir de la
    cantidad de chismes de tipo $t_2$ en no más de 1 elemento.

-   Si un chisme de tipo $t$ aparece en $S$, todos los chismes de tipo
    $t$ de $S$ deben formar un segmento continuo. Estos chismes no son
    necesariamente continuos en la cadena $A$.

Para ayudar a Lázaro y Sheyla, reciba la cadena $A$ representando a la
libreta, y calcule el tamaño de la mayor cadena $S$ posible.

