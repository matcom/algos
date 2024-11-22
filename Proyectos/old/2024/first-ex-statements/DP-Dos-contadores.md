# DP

## Dos contadores

Tienes $2$ contadores $a$ y $b$, ambos inicializados en $0$. También tienes un puntaje inicializado en $0$.

Al inicio de cada minuto, desde el minuto $1$ hasta el minuto $N$, debes incrementar ya sea $a$ o $b$ en $1$.

Adicionalmente, hay $M$ eventos. El evento $i$ ocurre en el minuto $T_i + 0.5$ y tiene tipo $C_i$ $(C_i \in \{1, 2\})$.

En cada evento, los contadores o el puntaje se actualizan de la siguiente manera:

```cpp
if (type == 1):
    if (a > b):
        score = score + 1;
    else:
        a = 0;
        b = 0;
else:
    if (a < b):
        score = score + 1;
    else:
        a = 0;
        b = 0;
```

Tu tarea es maximizar el puntaje después de que hayan pasado $N$ minutos.

### Statement

Tienes dos contadores $a$ y $b$ y un puntaje $S$, todos inicialmente en $0$.
Durante $N$ minutos, necesitas incrementar $a$ o $b$ en $1$.
También hay $M$ eventos, cada uno de dos tipos:

- Un evento de tipo $1$ incrementa $S$ en $1$ si $a > b$, y establece $a = b = 0$ de lo contrario.
- Un evento de tipo $2$ incrementa $S$ en $1$ si $a < b$, y establece $a = b = 0$ de lo contrario.

¿Cuál es el máximo puntaje final posible que puedes lograr?

### Solution

Sea $d = a - b$ la diferencia entre $a$ y $b$.
Note que cada evento verifica si la diferencia es positiva o negativa, luego incrementa el puntaje en $1$ o reinicia $d$ a $0$.

Además, en cada minuto, podemos aumentar o disminuir $d$ en $1$.

Idealmente, queremos mantener $d$ lo más cercano posible a $0$, para que podamos cambiar su signo rápidamente si es necesario para un evento.
De hecho, es suficiente mantener $-2 \leq d \leq 2$ en todo momento.

Prueba
Armados con este conocimiento, resolvamos el problema.

Usaremos programación dinámica: sea $dp(i, x)$ el puntaje máximo después de $i$ minutos si $d = x$.
Las transiciones son las siguientes:

Primero, necesitamos aumentar o disminuir $d$ en $1$. Es decir,
$dp(i, x) = \max(dp(i - 1, x - 1), dp(i - 1, x + 1))$.
Luego, necesitamos procesar un evento en este momento, si hay alguno.
Supongamos que hay un evento de tipo $1$. Esto cambia los valores de la siguiente manera:

- Si $x > 0$, entonces sumamos $1$ a $dp(i, x)$.
- $dp(i, 0) = \max(dp(i, 0), dp(i, -1), dp(i, -2))$, ya que los valores negativos se fuerzan a $0$.
- $dp(i, x) = -\infty$ para $x < 0$, ya que es imposible tener un valor negativo de $d$ después de este minuto.

Un evento de tipo $2$ se maneja de manera similar.

Los casos base para esta función son $dp(0, 0) = 0$ y $dp(0, x) = -\infty$ para $x \neq 0$.
La respuesta final es el valor máximo de $dp(N, x)$ para algún $x$.

Dado que solo importa $-2 \leq x \leq 2$, tenemos $5N$ estados y transiciones $O(1)$ para cada uno, lo que lleva a una solución $O(N)$.

COMPLEJIDAD TEMPORAL:
$O(N)$ por caso de prueba.
