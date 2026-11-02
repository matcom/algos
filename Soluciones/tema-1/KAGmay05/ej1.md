## Problema 1

Una computadora mil veces más rápida. ¿Cuánto crece el tamaño de entrada que se resuelve en una hora con un algoritmo $O(n^2)$? ¿Y con uno $O(n \log n)$? Estima los dos factores.

### Respuesta

Si en una hora, una computadora es 1000 veces más rápida, tomando como lo que se resolvía antes como n1 y la más rápida n2, se cumple que:
f(n2) = 1000* f(n1).

Para $O(n^2)$:

$$n_2^2 = 1000\, n_1^2 \;\Rightarrow\; n_2 = \sqrt{1000}\, n_1 \approx 31.6\, n_1$$

Factor ≈ 32. Aunque la máquina es mil veces más rápida, solo se resuelven entradas unas 32 veces más grandes.

Para $O(n \log n)$


$$n_2 \log n_2 = 1000\, n_1 \log n_1$$

Despeje de $n_2$. Dividimos ambos lados entre $\log n_2$:

$$n_2 = \frac{1000\, n_1 \log n_1}{\log n_2}$$

$n_2$ todavía aparece a la derecha, dentro del logaritmo. Como $\log$ crece muy lento, dentro del logaritmo podemos aproximar $n_2 \approx 1000\, n_1$:

$$\log n_2 \approx \log(1000\, n_1) = \log n_1 + \log 1000$$

Sustituyendo:

$$n_2 \approx 1000\, n_1 \cdot \frac{\log n_1}{\log n_1 + \log 1000}$$

Factor. El factor $k = n_2 / n_1$ depende de $n_1$:

$$k \approx 1000 \cdot \frac{\log n_1}{\log n_1 + \log 1000}$$

Con $\log_2 1000 \approx 9.97$:

| $n_1$ | $\log_2 n_1$ | factor $k$ |
|---|---|---|
| $10^6$ | $19.93$ | $\approx 667$ |
| $10^9$ | $29.90$ | $\approx 750$ |
| $9.86 \times 10^{10}$ (1 hora a $10^9$ ops/s) | $36.52$ | $\approx 786$ |
| $n_1 \to \infty$ | — | $\to 1000$ |

Factor ≈ 790, casi $1000$. 

Para comprobar estas estimaciones veamos el código visto en conferencia. Busca por búsqueda binaria el mayor $n$ que se resuelve con un presupuesto dado, suponiendo $10^9$ operaciones por segundo, y compara una máquina 10 y 1000 veces más rápida:

```python
import math

def mayor_n(costo, presupuesto):
    # el mayor n con costo(n) <= presupuesto, por búsqueda binaria
    alto = 2
    while costo(alto) <= presupuesto:
        alto *= 2
    bajo = alto // 2
    while bajo + 1 < alto:
        medio = (bajo + alto) // 2
        if costo(medio) <= presupuesto:
            bajo = medio
        else:
            alto = medio
    return bajo

costos = {
    "n log n": lambda n: n * math.log2(n),
    "n^2": lambda n: n ** 2,
}

hora = 3600 * 10**9

print(f"{'costo':>8} {'actual':>12} {'10x':>12} {'1000x':>12}")
for nombre, costo in costos.items():
    fila = [mayor_n(costo, hora * k) for k in (1, 10, 1000)]
    print(f"{nombre:>8} " + " ".join(f"{n:>12.3g}" for n in fila))
```

Salida:

```text
   costo       actual          10x        1000x
 n log n     9.86e+10     9.06e+11      7.8e+13
     n^2      1.9e+06        6e+06        6e+07
```
La columna 1000x confirma los dos factores: para $n^2$, $6 \times 10^7 / 1.9 \times 10^6 \approx 32$; para $n \log n$, $7.8 \times 10^{13} / 9.86 \times 10^{10} \approx 791$. La pequeña diferencia con $786$ viene de aproximar $\log n_2$.