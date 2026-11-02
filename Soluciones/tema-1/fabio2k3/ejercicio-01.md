# Solución ejercicio 1:

Partamos que f pertenece a Θ(g) si existe c1, c2 y n0 tal que f >= c1*g(n) y f <= c2*g(n) para todo n >= n0

Como Θ solo nos dice cómo crece el costo, no su valor exacto, vamos a modelarlo como c*g(n) operaciones

En nuestro caso como tenemos una máquina que es mil veces más rápida que la original, entonces esto implica que si la vieja hace c*g(n) operaciones la otra hará 1000*c*g(n) que es todo lo que le cabe en la hora es decir es igual a c*g(n').

Por lo tanto tenemos que: c*g(n') = 1000*c*g(n) 
                            g(n') = 1000*g(n)

Las máquinas hacen T operaciones por hora, en la vieja c*g(n) = T donde n es el tamaño máximo, y en la rápida como es 1000 veces más rápida será 1000 * T y aquí viene nuestro objetivo de encontrar n' que es el nuevo máximo.

Ahora vamos a analizar cada caso del ejercicio:

# Caso 1: Θ(n^2)

Como ya vimos anteriormente g(n') = 1000*g(n), solo nos queda sustituir cada variable:   g(n') = (n')^2
                                                                                        g(n) = n^2

=> (n')^2 = 1000*(n^2)
    n' = sqrt(1000) * n
    n'/n = sqrt(1000)  [sqrt(1000) es aproximadamente 31.6]
    n'/n es aproximadamente 31.6

Por lo tanto el tamaño se multiplica unas 31.6 veces, es decir una máquina mil veces más rápida el tamaño se multiplica por casi 32, sin importar cuál era n.

# Caso 2: Θ(n*logn)

Aquí tenemos que g(n) = n*logn y g(n') = (n')*log(n')

No podemos despejar n' ya que aparece normal como n' y dentro del logaritmo por lo que aplicaremos una sustitución n' = k*n, donde k es el factor que buscamos.

=>  k*n*log(k*n) = 1000*n*log(n)  / dividimos por n
    k*log(k*n) = 1000*log(n)
    k(log(k) + log(n)) = 1000 * log(n) / dividimos por log n
    k*(log(k)/log(n) + 1) = 1000

Como podemos observar no podemos aislar k, pero es una ecuación que tiene solución, así que podemos probar valores.

log(k)/log(n) + 1 > 1 , por lo que k tiene que ser menor que 1000

Si corremos nuestro script de python "ejercicio-01.py" (en este script hacemos una búsqueda binaria de k entre 1 y 1000, ya que el lado izquierdo de la ecuación solo crece si k crece) obtenemos los siguientes valores :


-------------------------------------------------------
n     |  k     |  k*(1 + logk / log n)   |  n_nuevo   |
------------------------------------------------------|
10^3  | 524.5  |    1000.000000          |  5.245e+05 |
10^4  | 590.7  |    1000.000000          |  5.907e+06 | 
10^5  | 640.5  |    1000.000000          |  6.405e+07 |
10^6  | 679.3  |    1000.000000          |  6.793e+08 |
10^7  | 710.5  |    1000.000000          |  7.105e+09 |
10^8  | 736.2  |    1000.000000          |  7.362e+10 |
10^9  | 757.6  |    1000.000000          |  7.576e+11 |
-------------------------------------------------------

Observemos que K crece despacio y se acerca a 1000 porque log(k)/log(n) tiende a 0 a medida que n crece

Por lo tanto podemos concluir que con un algoritmo Θ(nlogn) una máquina que es mil veces más rápida, aumenta su tamaño de 500 a 760 dependiendo de n, es decir aprovecha la mejora considerablemente a diferencia del algoritmo Θ(n^2) que solo lo multiplica aproximadamente 32 veces.