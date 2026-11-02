**Resumen:** No, no es polinomial en el tamaño de la entrada. $O(nW)$ es polinomial en el *valor* de $W$, pero $W$ ocupa solo $\lceil \log_2 (W+1) \rceil$ bits, así que la complejidad temporal es exponencial en la longitud en bits de $W$,es *pseudo-polinomial* para ser exactos. La división de prueba (trial division) es pseudo-polinomial exactamente de la misma forma: su tiempo es polinomial en el *valor* del número, pero exponencial en su longitud en bits.

## Mochila (knapsack)


**Tamaño de la entrada.** Una instancia tiene pesos $w_1,\dots,w_n$, valores $v_1,\dots,v_n$ y capacidad $W$, todos escritos en binario:

$$N = \sum_{i=1}^{n} \lceil\log_2 (w_i+1)\rceil + \sum_{i=1}^{n} \lceil\log_2 (v_i+1)\rceil + \lceil\log_2 (W+1)\rceil .$$

**Complejidad temporal en función de $N$.** Sea $b = \lceil \log_2 (W+1) \rceil$ el número de bits de $W$. Entonces $W \approx 2^{b}$ y

$$O(nW) = O(n \cdot 2^{b}) ,$$

que es exponencial en $b$, y $b \le N$.

**Esto no es solo una cota superior floja.** El algoritmo estándar llena una tabla de $n$ filas y $W+1$ columnas, por lo que toma tiempo $\Omega(nW)$. Tomemos la familia con $n = k$ objetos, $W = 2^k$ y todos los pesos y valores a lo sumo $2^k$. Entonces:

- El tamaño de la entrada es $N = O(k^2)$ bits.
- El tiempo de ejecución es $\Omega(k \cdot 2^k) = 2^{\Omega(\sqrt{N})}$.

Ningún polinomio $p(N)$ acota esto, así que el algoritmo **no es polinomial**. Solo es polinomial cuando $W$ se codifica en unario, o cuando $W \le \text{poly}(n)$.

**Ojo:** esto es una afirmación sobre el *algoritmo*, no sobre el problema. La mochila es NP-hard (su versión de decisión es NP-completa), así que un algoritmo verdaderamente polinomial implicaría $\text{P} = \text{NP}$. Como existe un algoritmo pseudo-polinomial, se dice que es *débilmente* NP-hard.

## Primalidad por división

```python
def is_prime(m):
    if m < 2:
        return False
    d = 2
    while d * d <= m:
        if m % d == 0:
            return False
        d = d + 1
    return True
```

El ciclo se ejecuta aproximadamente $\sqrt{m}$ veces. Si $m$ tiene $b = \lceil\log_2 (m+1)\rceil$ bits, entonces $m \approx 2^{b}$ y el número de iteraciones es aproximadamente $2^{b/2}$. Esto es polinomial en $m$ pero exponencial en $b$, que es el verdadero tamaño de la entrada.

## Qué tienen en común

- **Mismo defecto:** el tiempo de ejecución es un polinomio en el *valor* numérico de un número de la entrada, no en su *longitud*. Ambos serían polinomiales con codificación unaria.
- **Misma trampa:** un número de $b$ bits puede tener un valor de $2^b$, así que "lineal en el número" es exponencial en el tamaño de la entrada. Duplicar la longitud de la entrada eleva el valor al cuadrado.
- **Distinto estatus:** pseudo-polinomial no significa que el problema sea difícil. La primalidad está en P gracias a otro algoritmo (AKS, 2002, que es polinomial en $b$), mientras que para la mochila no se conoce ningún algoritmo polinomial, y uno implicaría $\text{P} = \text{NP}$.