# Solución Ejercicio 11

Sea Q[i][c] el mayor valor usando los primeros i objetos con capacidad c:

Q[0][c] = 0
Q[i][c] = Q[i-1][c]     si w_i > c
Q[i][c] = max(Q[i-1][c], Q[i-1][c - w_i] + v_i)  si w_i <= c

La respuesta se encuentra en la posición Q[n][W]. La tabla tiene (n+1)(W+1) celdas y cada una cuesta O(1), así que el algoritmo hace Θ(nW) operaciones. Es Θ y no solo O ya que la recurrencia llena la tabla al completo, sea cual sea nuestra entrada.

def mochila(w, v, W):
    Q = [0] * (W + 1)
    celdas = 0
    for wi, vi in zip(w, v):
        for c in range(W, wi - 1, -1):
            Q[c] = max(Q[c], Q[c - wi] + vi)
            celdas += 1
    return Q[W], celdas

Escribir un entero x >= 1 en binario ocupa log2(x) + 1 bits. La entrada completa ocupa:

L = Σ (⌊log2(w_i)⌋ + 1) + Σ (⌊log2(v_i)⌋ + 1) + (⌊log2(W)⌋ + 1)

Ahora llamemos b a los bits de W, por ende b = ⌊log2(x)⌋ + 1. L depende de log W, no de W. Al revés, W es exponencial en b:

2^(b-1) <= W < 2^b

Multiplicar W por 1000 solo añade unos 10 bits a la entrada, pero multiplica por 1000 el trabajo del algoritmo.

Ahora nos podemos preguntar, ¿es polinomial? pues Nope.
Un algoritmo es polinomial si su costo está acotado por p(L), donde p es algún polinomio y L el tamaño de la entrada en bits.

Tomemos entradas con n = 2 objetos de pesos y valores pequeños y W = 2^(b-1), entonces:
- Tamaño de la entrada: L <= c*b para alguna constante c.
- Costo: Θ(nW) = Θ(2^(b-1))

Para cualquier polinomio p, 2^(b-1) > p(O(b)) a partir de cierto b, esto se debe a que cualquier exponencial supera a todo polinomio.
Por tanto el costo no está acotado por un polinomio en L, es exponencial en el tamaño de la entrada.

Esto se llama pseudopolinomial, es decir, el costo es polinomial en valor numérico de W pero exponencial en su longitud en bits.

