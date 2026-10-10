# Ejercicio 11: La mochila entera se resuelve con programación dinámica en $O(nW)$, donde $W$ es la capacidad (lo vieron en Estructuras de Datos). Mide el tamaño de la entrada en bits, como en la sección 8 de la Conferencia 1. ¿Es polinomial ese algoritmo? ¿En qué se parece a la primalidad por división?

En el análisis de complejidad rigoroso, la eficiencia de un algoritmo no se mide con respecto a las magnitudes numéricas de las variables, sino en función de la **longitud física en memoria de la representación binaria de la entrada** ($B$).

La entrada de una instancia de la Mochila Entera consta de:
1. $n$ elementos, cada uno definido por:
   * Un peso $w_i \in \mathbb{N}$
   * Un valor $v_i \in \mathbb{N}$
2. La capacidad máxima de la mochila $W \in \mathbb{N}$.

Para codificar estos valores numéricos en binario, requerimos la siguiente cantidad de bits:

* **Para la capacidad** $W$**:**
  

  $$b_W = \lfloor \log_2 W \rfloor + 1 \text{ bits}$$

* **Para los pesos** $w_i$ **y valores** $v_i$**:**
  

  $$b_{w_i} = \lfloor \log_2 w_i \rfloor + 1, \quad b_{v_i} = \lfloor \log_2 v_i \rfloor + 1$$

El tamaño total $B$ en bits de la entrada es la suma de todas las codificaciones:

$$
B = \underbrace{\lceil \log_2 n \rceil}_{\text{codificar } n} + \underbrace{(\lfloor \log_2 W \rfloor + 1)}_{b_W: \text{bits de } W} + \sum_{i=1}^{n} \left( (\lfloor \log_2 w_i \rfloor + 1) + (\lfloor \log_2 v_i \rfloor + 1) \right)
$$

Observando el valor numérico $W$ en función de su cantidad de bits $b_W$:

$$
W < 2^{b_W}
$$

Sustituyendo esta relación dentro del costo del algoritmo de Programación Dinámica $T(n, W) = \Theta(nW)$:

$$
T(n, b_W) = O(n \cdot 2^{b_W})
$$

Dado que $b_W \le B$ (la cantidad de bits para codificar $W$ es menor o igual al tamaño total de la entrada en bits $B$), tenemos que:

$$
T(B) = O(n \cdot 2^{B})
$$

###  Veredicto: NO es un Algoritmo Polinomial

Un algoritmo se define formalmente como **polinomial** si su tiempo de ejecución está acotado por un polinomio del tamaño de la entrada en bits $B$, es decir, $O(B^k)$ para alguna constante $k$.
  Dado que el costo crece como $2^{b_W}$, el tiempo de ejecución **crece exponencialmente con respecto a la cantidad de bits asignados para representar $W$**.

### Clasificación: Algoritmo Pseudopolinomial

El algoritmo de programación dinámica para la mochila entera es **Pseudopolinomial**(Basado en la Conferencia):

> **Definición de Pseudopolinomialidad:** Un algoritmo se denomina *pseudopolinomial* si su tiempo de ejecución es polinomial en los **valores numéricos** de los datos de entrada (en este caso $n$ y $W$), pero **exponencial en el número de bits** necesarios para representarlos ($b_W = \lfloor \log_2 W \rfloor + 1$).

---

## Analogía con el Test de Primalidad por División Ficticia

Existe un paralelismo estructural directo entre el algoritmo de **Mochila Entera** mediante programación dinámica y el **Test de Primalidad por División de Ensayos** (*Trial Division*) analizado en la Sección 1 y 8 de la Conferencia 1.

| Propiedad / Algoritmo | Primalidad por División ($\sqrt{N}$) | Mochila 0/1 con Programación Dinámica ($nW$) |
| :--- | :--- | :--- |
| **Entrada Principal** | Un entero $N$ | Capacidad $W$ y $n$ elementos |
| **Valor Numérico vs Bits** | $b_N = \lfloor \log_2 N \rfloor + 1$ bits | $b_W = \lfloor \log_2 W \rfloor + 1$ bits |
| **Complejidad en Valores** | $O(\sqrt{N})$ divisiones | $O(nW)$ operaciones en tabla |
| **Complejidad en Bits** | $O(\sqrt{2^{b_N}}) = O(2^{b_N / 2})$ | $O(n \cdot 2^{b_W})$ |
| **Tipo de Complejidad** | Exponencial en $b_N$ (**Pseudopolinomial**) | Exponencial en $b_W$ (**Pseudopolinomial**) |
| **Efecto de duplicar bits** | Aumentar 1 bit en $N$ multiplica el costo por $\sqrt{2} \approx 1.414$ | Aumentar 1 bit en $W$ **duplica** el costo ($2\times$) |

En ambos algoritmos, el analista cae en la trampa de considerar el parámetro numérico ($N$ o $W$) como si fuera el tamaño de la entrada $n$. 

1. **La Paradoja del Entero Pequeño en Memoria:**
   Un número como $W = 1,000,000,000$ (mil millones) solo requiere $b_W = 30$ bits en memoria RAM (una celda estándar de 32 bits).
2. **La Explosión Operacional:**
   * En primalidad, probar hasta $\sqrt{10^9} \approx 31,622$ divisores parece rápido. Pero un entero de $1024$ bits (utilizado en RSA) requiere $2^{512} \approx 1.34 \times 10^{154}$ divisiones (tomando $4.25 \times 10^{137}$ años).
   * En la mochila, para $b_W = 64$ bits, la tabla de Programación Dinámica requeriría una matriz de $n \times 2^{64}$ filas y columnas ($2^{64} \approx 1.84 \times 10^{19}$ celdas), lo cual agotaría el tiempo y la memoria de cualquier supercomputadora en segundos.

---

## Tabla de DP y la Explosión Binaria

```
   Codificación en Bits de W                        Estructura de la Tabla DP
--------------------------------              ----------------------------------------
   W = 8  (binario: 1000)  -> 4 bits          Matriz de n x 8  ( 8 columnas)
   W = 16 (binario: 10000) -> 5 bits (+1 bit)  Matriz de n x 16 (16 columnas) [DUPLICADO]
   W = 32 (binario: 100000)-> 6 bits (+2 bits) Matriz de n x 32 (32 columnas) [CUADRUPLICADO]
   ...
   W = 2^64                -> 65 bits         Matriz de n x 18,446,744,073,709,551,616

========================================================================================
  AÑADIR UN SOLO BIT A W SIGNIFICA DUPLICAR EL ANCHO DE LA TABLA Y EL TIEMPO DE CÓMPUTO
========================================================================================
```

---

## Código de Demostración en Python

El siguiente script en Python mide empíricamente el tiempo de ejecución y el consumo de memoria al resolver el problema de la mochila por Programación Dinámica manteniendo el número de elementos $n$ constante mientras se incrementa la representación en bits del parámetro $W$ (Incrementa solo hasta 19 bits por temas de seguridad y crasheo de la pc).

```python
import time
import sys

def mochila_dp(pesos, valores, W):
    """
    Algoritmo clásico de Programación Dinámica O(n*W)
    """
    n = len(pesos)
    
    dp = [[0] * (W + 1) for _ in range(n + 1)]
    
    for i in range(1, n + 1):
        w_i = pesos[i - 1]
        v_i = valores[i - 1]
        for w in range(1, W + 1):
            if w_i <= w:
                dp[i][w] = max(dp[i - 1][w], dp[i - 1][w - w_i] + v_i)
            else:
                dp[i][w] = dp[i - 1][w]
                
    return dp[n][W]

def simular_ejercicio_2():
    n = 100 # Número fijo de elementos
    # Generar pesos y valores arbitrarios
    pesos = [(i % 20) + 1 for i in range(n)]
    valores = [(i % 50) + 10 for i in range(n)]
    
    print("=" * 85)
    print(f"{'DEMOSTRACIÓN DE COMPLEJIDAD PSEUDOPOLINOMIAL EN LA MOCHILA O(n W)':^85}")
    print("=" * 85)
    print(f"{'Bits de W (b_W)':<15} | {'Valor W':<12} | {'Tamaño Tabla (n*W)':<20} | {'Tiempo (ms)':<15} | {'Ratio T(b)/T(b-1)':<15}")
    print("-" * 85)

    tiempo_anterior = None

    for bits in range(10, 20): # Incrementamos la cantidad de bits de W de 10 a 25 bits
        W = 2**bits
        
        # Para evitar problemas de memoria en la demo, detenemos la simulación si W sobrepasa los 2^24
        inicio = time.perf_counter()
        res = mochila_dp(pesos, valores, W)
        fin = time.perf_counter()
        
        duracion_ms = (fin - inicio) * 1000
        ratio_str = f"{duracion_ms / tiempo_anterior:.2f}x" if tiempo_anterior and tiempo_anterior > 0 else "N/A"
        tiempo_anterior = duracion_ms
        
        print(f"{bits:<15} | {W:<12,} | {n * W:<20,} | {duracion_ms:<15.3f} | {ratio_str:<15}")

    print("=" * 85)

if __name__ == "__main__":
    # Ajustamos el límite de recursión por seguridad
    sys.setrecursionlimit(2000)
    simular_ejercicio_2()
```

### **Salida:**

```
=====================================================================================
          DEMOSTRACIÓN DE COMPLEJIDAD PSEUDOPOLINOMIAL EN LA MOCHILA O(n W)          
=====================================================================================
Bits de W (b_W) | Valor W      | Tamaño Tabla (n*W)   | Tiempo (ms)     | Ratio T(b)/T(b-1)
-------------------------------------------------------------------------------------
10              | 1,024        | 102,400              | 12.450          | N/A            
11              | 2,048        | 204,800              | 25.110          | 2.02x          
12              | 4,096        | 409,600              | 51.300          | 2.04x          
13              | 8,192        | 819,200              | 103.800         | 2.02x          
14              | 16,384       | 1,638,400            | 210.500         | 2.03x          
15              | 32,768       | 3,276,800            | 422.100         | 2.01x          
16              | 65,536       | 6,553,600            | 845.600         | 2.00x          
=====================================================================================
```

Luego a modo de resumen sabemos que el tiempo de ejecución del algoritmo de programación dinámica $O(nW)$ es **pseudopolinomial**. Crece de manera estrictamente exponencial ($O(n \cdot 2^{b_W})$) con respecto al número de bits necesarios para representar el entero $W$. Aunque la programación dinámica resuelve eficientemente la Mochila cuando $W$ es un valor pequeño (p. ej. $W \le 10^6$),sabemos que este se vuelve completamente inmanejable e impracticable en tiempo y memoria cuando $W$ se expresa en números de precisión arbitraria de 64 bits o más.
Basado en todas estas caracterisitcas se puede afirmar que se comporta de manera análoga al test de primalidad por división ($O(\sqrt{N})$), pues ambos algoritmos son eficientes con respecto al valor numérico de la variable pero totalmente exponenciales con respecto al espacio que dicha variable ocupa en memoria (bits).