# DP

## Banco

Gustaw es el gerente principal de un gran banco. Tiene acceso ilimitado al sistema de bases de datos del banco y, con unos pocos clics, puede mover cualquier cantidad de dinero de las reservas del banco a su propia cuenta privada. Sin embargo, el banco utiliza un sofisticado sistema de detección de fraude impulsado por IA, lo que hace que robar sea más difícil.

Gustaw sabe que el sistema antifraude detecta cualquier operación que supere un límite fijo de M euros, y estas operaciones son verificadas manualmente por un número de empleados. Por lo tanto, cualquier operación fraudulenta que exceda este límite es detectada, mientras que cualquier operación menor pasa desapercibida.

Gustaw no conoce el límite M y quiere descubrirlo. En una operación, puede elegir un número entero X y tratar de mover X euros de las reservas del banco a su propia cuenta. Luego, ocurre lo siguiente.

Si X≤M, la operación pasa desapercibida y el saldo de la cuenta de Gustaw aumenta en X euros.  
De lo contrario, si X>M, se detecta el fraude y se cancela la operación. Además, Gustaw debe pagar X euros de su propia cuenta como multa. Si tiene menos de X euros en la cuenta, es despedido y llevado a la policía.  
Inicialmente, Gustaw tiene 1 euro en su cuenta. Ayúdalo a encontrar el valor exacto de M en no más de 105 operaciones sin que sea despedido.

Entrada:
Cada prueba contiene múltiples casos de prueba. La primera línea contiene el número de casos de prueba t (1≤t≤1000).

Para cada caso de prueba, no hay entrada previa a la primera consulta, pero puedes estar seguro de que M es un número entero y 0≤M≤1014.

Salida:
Para cada caso de prueba, cuando sepas el valor exacto de M, imprime una única línea con el formato "! M". Después de eso, tu programa debe proceder al siguiente caso de prueba o terminar, si es el último.

### Statement

Un sistema antifraude detecta cualquier operación mayor a un límite M fijo.

Se desconoce el valor de M y se pueden realizar operaciones moviendo una cantidad X de euros. Si X≤M, la operación no es detectada y el saldo aumenta en X euros. Si X>M, el fraude es detectado, la operación es cancelada y se debe pagar X euros. Si el saldo es menor a X euros, ocurre el despido y se reporta a la policía.

Se comienza con 1 euro en la cuenta. Se deben realizar no más de 105 operaciones para encontrar el valor exacto de M.

entrada:
Múltiples casos de prueba con número de casos t (1≤t≤1000). No hay entrada previa, pero M es un número entero con 0≤M≤1014.

salida:
Imprimir "! M" cuando se sepa el valor exacto de M.

### Solution

Nuestra solución consta de dos partes. Primero, encontrar un límite superior para $M$. Para lograr esto, intentamos consultar $1$, $2$, $4$, $8$, y así sucesivamente hasta que fallemos. Después de la primera consulta fallida, tendremos $0$ euros y sabremos que la respuesta está en algún segmento $[2^k, 2^{k+1})$. Esto toma como máximo $47$ consultas.

Ahora uno podría hacer algo como la siguiente búsqueda binaria: tomar el borde izquierdo de nuestro segmento de dinero, luego en cada consulta intentar el borde izquierdo y luego el medio. Si las consultas son exitosas, todo bien, de lo contrario perdemos $\frac{L + R - L}{2}$, donde $L$ se toma al principio de esta iteración, y todo $\frac{R - L}{2}$ no puede sumar algo mayor que el borde izquierdo inicial que obtuvimos, porque inicialmente $R - L = L$, y cada vez que $R - L$ disminuye a la mitad. Sin embargo, esta solución requiere otras $2\log(10^{14})$ consultas, lo cual es demasiado.

Dividamos el segmento en dos partes desiguales a veces. Nota que si el lado izquierdo de la partición no excede la mitad del segmento, entonces ese extra $L$ que tenemos es suficiente para cubrir todos nuestros gastos. También usemos que de hecho obtenemos un extra $M \approx \frac{L + R}{2}$ después de consultas medias exitosas.

Queremos que nuestro algoritmo se vea como lo siguiente. Sea el segmento actual igual a $[l, r]$ y el saldo actual sea al menos $l \cdot y + (r - l)$ para algún entero $y$. Entonces, si $y = 0$, consultamos $l$, y si $y > 1$, consultamos lo que queramos en el segmento. Es fácil ver que después de una consulta fallida nuestro saldo es al menos $l \cdot (y - 1) + (r - l)$ (para nuevos $l$ y $r$), y después de una consulta exitosa, pensaremos que nuestro saldo es al menos $l \cdot (y + 1) + (r - l)$ (para nuevos $l$ o $r$). Lo último no siempre es el caso, lo discutiremos más adelante.

Ahora nuestro saldo se describe por el único entero $y$. Sea $dp[x][y]$ igual al máximo $d$ para que sea posible encontrar la respuesta en $[l, l + d]$ teniendo $y \cdot l + d$ dinero inicialmente. Entonces $dp[x][y] = dp[x - 1][y - 1] + dp[x - 1][y + 1]$, es fácil de calcular y seguir en la solución. Se puede demostrar que $dp[k][0] = \binom{k}{k / 2}$. Esto implica que $k \leq 49$. Esto suma hasta $97$ consultas.

Ahora recuerda que, si procedemos de $(l, r, y)$ a $(m, r, y + 1)$, entonces nuestro saldo era $y \cdot l + (r - l)$ y se convirtió en $y \cdot l + m$, mientras que necesitamos $(y + 1) \cdot m$ para nuestras estimaciones. Por lo tanto, necesitamos algo de dinero extra para cubrir tales "gastos". Se puede probar que no exceden tres de los $L$ iniciales, lo que da un total de $100$ consultas.
