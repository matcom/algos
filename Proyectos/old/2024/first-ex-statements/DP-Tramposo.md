# DP

## Tramposo

Tito está pasando un curso de Diseño y Análisis de Algoritmos. Este año, por primera vez en la historia, los profesores han decidido evaluar el curso mediante un examen final y Tito se ha dado cuenta de que, a grandes rasgos, está frito. A pesar de ser un poco barco, es de hecho un muchacho inteligente y rápidamente se da cuenta de que su única forma de aprobar era hacer trampa. El día de la prueba, Tito se sentó en el asiento que estaba entre Hansel y Elena para fijarse, con la esperanza de que, uniendo las preguntas respondidas por cada uno, se pudiera formar un examen correcto.

El examen tiene $n$ preguntas, ordenadas en la hoja. Elena y Hansel pueden no ser capaces de responder cada uno el examen entero, pero todas las preguntas que responden están correctas. Se conoce cuáles preguntas respondió cada uno y se reciben como dos listas ordenadas de enteros entre $1$ y $n$. Tito tiene $p$ oportunidades para mirar hacia la izquierda (hoja de Hansel) o hacia la derecha (hoja de Elena) y su agilidad mental le alcanza para ver las respuestas de $k$ preguntas consecutivas (en cualquier posición) cada vez que echa una mirada a un examen.

Ayude a Tito a saber la cantidad máxima de preguntas que puede responder con su (tramposa) estrategia.

### Statement

Dado que hay $n$ preguntas y la persona puede mirar a lo sumo $p$ veces, con cada vistazo cubriendo a lo máximo $k$ preguntas consecutivas en la hoja de respuestas de uno de los dos genios, donde cada genio puede o no tener la respuesta correcta para ciertas preguntas:

Determina el número máximo de preguntas que la persona puede responder correctamente al copiar estratégicamente de las hojas de respuestas de los genios sin ser atrapada por el supervisor.

### Solution

Primero, observa que nunca es subóptimo mirar tantas preguntas consecutivas como sea posible. Es decir, simplemente mira $k$ preguntas consecutivas cada vez que decidas echar un vistazo, a menos que exceda el límite (pregunta $n$).

Sea $dp[i][j][a][b]$ el número de preguntas que puedes contestar correctamente al considerar las preguntas de $1$ a $i$, echando exactamente $j$ vistazos, con $a$ y $b$ siendo el número de preguntas restantes que pueden ser observadas como un beneficio de los vistazos previos. Como se mencionó antes, es óptimo mirar tantas preguntas consecutivas como sea posible, por lo que cuando decidimos mirar, compartimos este beneficio (de mirar) con las siguientes preguntas también, y se almacenan en $a$ y $b$, que indican cuántas de las próximas preguntas consecutivas se pueden mirar sin gastar un vistazo adicional. La respuesta se puede calcular en $O(npk^2)$. (Puedes ver en el código cómo.)

Sin embargo, $npk^2$ puede ser hasta $(1000) * (1000) * (50) * (50)  =  2,500,000,000$, por lo que la solución no cabrá en el límite de tiempo de $2$ segundos.

Esto se puede mejorar. Observa que si $p > 2 * \lceil n / k \rceil$, puedes mirar todas las preguntas en las hojas de respuestas de ambos genios, por lo que la respuesta se puede encontrar en $O(n)$ (o simplemente puedes fijar $p$ en $2 * \lceil n / k \rceil$ y ejecutar la programación dinámica). Al eliminar este caso, el tiempo de ejecución para la programación dinámica se convertirá en $O(npk^2) = O(n(n / k)k^2) = O(n^2k)$. Esto, efectivamente, se ajustará en el tiempo, ya que $n^2k$ es solo $(1000) * (1000) * (50)  =  50,000,000$.

El problema con el límite de memoria podría persistir, por lo que necesitarás optimizar el uso de la memoria. Por ejemplo, dado que solo necesitas $dp[i - 1][..][..][..]$ y $dp[i][..][..][..]$ al calcular $dp[i][..][..][..]$, podrías recordar solo las dos últimas filas. El uso de memoria será mucho menor. El uso del tipo de dato corto (`short`) en lugar de `int` también podría ayudar.

COMPLEJIDAD TEMPORAL:
$O(npk^2) = O(n(n / k)k^2) = O(n^2k)$
