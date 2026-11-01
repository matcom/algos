# Pregunta 1: 

Una computadora mil veces más rápida. ¿Cuánto crece el tamaño de entrada que se resuelve en una
hora con un algoritmo ? ¿Y con uno ? Estima los dos factores. 


A continuación presento mi resolución dividida en tres partes: demostración formal, explicación con ejemplo numérico y explicación de mi código.

---

## Demostración formal

Supongamos que la computadora original puede ejecutar como máximo $C$ operaciones en una hora. La nueva computadora, al ser mil veces más rápida, podrá ejecutar $1000 \cdot C$ operaciones en el mismo tiempo.

### Caso $O(n^2)$

En la máquina original, el tamaño máximo de entrada $N_1$ satisface:

$$
N_1^2 = C
$$

En la nueva máquina, el nuevo tamaño máximo $N_2$ satisface:

$$
N_2^2 = 1000 \cdot C
$$

Como $C = N_1^2$, sustituimos:

$$
N_2^2 = 1000 \cdot N_1^2
$$

Aplicando raíz cuadrada en ambos lados:

$$
N_2 = \sqrt{1000} \cdot N_1
$$

$$
N_2 \approx 31.62 \cdot N_1
$$

Por lo tanto, para un algoritmo cuadrático, el tamaño de entrada crece de forma multiplicativa por un factor aproximado de $31.62$.

En general, si la velocidad aumenta por un factor $k$, entonces:

$$
N_2 = \sqrt{k} \cdot N_1
$$

### Caso $O(2^n)$

En la máquina original:

$$
2^{N_1} = C
$$

En la nueva máquina:

$$
2^{N_2} = 1000 \cdot C
$$

Sustituyendo $C = 2^{N_1}$:

$$
2^{N_2} = 1000 \cdot 2^{N_1}
$$

Aplicando logaritmo en base 2:

$$
\log_2(2^{N_2}) = \log_2(1000 \cdot 2^{N_1})
$$

$$
N_2 = \log_2(1000) + N_1
$$

$$
N_2 \approx 9.966 + N_1
$$

En este caso, el crecimiento es aditivo. Una computadora mil veces más rápida solo permite agregar alrededor de 10 elementos más al tamaño de entrada.

En general, si la velocidad aumenta por un factor $k$:

$$
N_2 = N_1 + \log_2(k)
$$

---

## Explicación y ejemplo numérico

Para comprobar los resultados anteriores, tomemos un presupuesto base de operaciones:

$$
C = 1{,}000{,}000 = 10^6
$$

La nueva computadora, mil veces más rápida, tendrá:

$$
1000 \cdot C = 1{,}000{,}000{,}000 = 10^9
$$

### Algoritmo $O(n^2)$

En la máquina original:

$$
N_1^2 = 1{,}000{,}000
$$

$$
N_1 = \sqrt{1{,}000{,}000} = 1000
$$

En la nueva máquina:

$$
N_2^2 = 1{,}000{,}000{,}000
$$

$$
N_2 = \sqrt{1{,}000{,}000{,}000} \approx 31622
$$

El factor de crecimiento es:

$$
\frac{N_2}{N_1} = \frac{31622}{1000} \approx 31.622
$$

Y el valor teórico es:

$$
\sqrt{1000} \approx 31.6228
$$

Por lo tanto, para un algoritmo cuadrático, el tamaño de entrada pasa de 1000 a aproximadamente 31622 elementos.

### Algoritmo $O(2^n)$

En la máquina original:

$$
2^{N_1} = 1{,}000{,}000
$$

$$
N_1 = \lfloor \log_2(1{,}000{,}000) \rfloor = 19
$$

En la nueva máquina:

$$
2^{N_2} = 1{,}000{,}000{,}000
$$

$$
N_2 = \lfloor \log_2(1{,}000{,}000{,}000) \rfloor = 29
$$

El incremento es:

$$
N_2 - N_1 = 29 - 19 = 10
$$

El valor teórico es:

$$
\log_2(1000) \approx 9.9658
$$

Es decir, aunque la computadora sea mil veces más rápida, para un algoritmo exponencial solo se pueden resolver alrededor de 10 elementos adicionales.

### Comparación resumida

| Complejidad | $N_1$ original | $N_2$ nueva | Crecimiento |
|---|---:|---:|---|
| $O(n^2)$ | 1000 | 31622 | $\approx 31.62 \cdot N_1$ |
| $O(2^n)$ | 19 | 29 | $N_1 + 10$ |

La conclusión principal es que el impacto de mejorar el hardware depende mucho de la complejidad del algoritmo. En problemas cuadráticos la mejora ayuda bastante, pero en problemas exponenciales el efecto es marginal.

---

## Explicación de mi código

### Objetivo del código

El objetivo de este código es verificar de manera numérica los resultados analíticos obtenidos en el ejercicio, sin recurrir a la medición de tiempos reales de ejecución. Para ello, se define un presupuesto abstracto de operaciones $C$, correspondiente a la cantidad máxima de operaciones que una computadora puede realizar en una hora. Posteriormente, se simula una computadora mil veces más rápida, cuyo presupuesto es $1000 \cdot C$.

El código calcula el mayor tamaño de entrada $n$ que puede resolverse con dicho presupuesto para dos tipos de algoritmos:

- Un algoritmo con complejidad cuadrática $O(n^2)$, cuyo costo se modela como $n^2$.
- Un algoritmo con complejidad exponencial $O(2^n)$, cuyo costo se modela como $2^n$.

De esta forma, se busca comprobar experimentalmente, mediante conteo de operaciones, los factores de crecimiento predichos teóricamente: $\sqrt{1000}$ para el caso cuadrático y $\log_2(1000)$ para el caso exponencial.

Primero defino dos presupuestos:

```python
C_original = 1_000_000
C_nueva = 1000 * C_original
```

Luego calculo el mayor tamaño de entrada $n$ que puede resolverse con cada presupuesto.

### Para $O(n^2)$

Como el costo del algoritmo es $n^2$, busco el mayor entero $n$ tal que:

$$
n^2 \leq C
$$

En el código uso raíz cuadrada entera para no pasarme del presupuesto:

```python
import math

n2_original = math.isqrt(C_original)
n2_nueva = math.isqrt(C_nueva)
factor = n2_nueva / n2_original
teorico = math.sqrt(1000)
```

Esto me permite obtener:

- $n$ original = 1000
- $n$ nueva = 31622
- factor = 31.6220
- teórico = $\sqrt{1000} \approx 31.6228$

### Para $O(2^n)$

Como el costo es $2^n$, busco el mayor entero $n$ tal que:

$$
2^n \leq C
$$

En mi código lo hago con un ciclo:

```python
def max_exponencial(C):
    n = 0
    while 2 ** (n + 1) <= C:
        n += 1
    return n

n_exp_original = max_exponencial(C_original)
n_exp_nueva = max_exponencial(C_nueva)
incremento = n_exp_nueva - n_exp_original
teorico_exp = math.log2(1000)
```

Con esto obtengo:

- $n$ original = 19
- $n$ nueva = 29
- incremento = 10 elementos
- teórico = $\log_2(1000) \approx 9.9658$

### Código completo

```python
import math

def max_cuadratica(C):
    return math.isqrt(C)

def max_exponencial(C):
    n = 0
    while 2 ** (n + 1) <= C:
        n += 1
    return n

C_original = 1_000_000
C_nueva = 1000 * C_original

n2_original = max_cuadratica(C_original)
n2_nueva = max_cuadratica(C_nueva)
factor = n2_nueva / n2_original
teorico_cuad = math.sqrt(1000)

n_exp_original = max_exponencial(C_original)
n_exp_nueva = max_exponencial(C_nueva)
incremento = n_exp_nueva - n_exp_original
teorico_exp = math.log2(1000)

print(f"Presupuesto original: {C_original:,} operaciones")
print(f"Presupuesto nueva:    {C_nueva:,} operaciones")
print()
print("Algoritmo O(n^2)")
print(f"  n original = {n2_original}")
print(f"  n nueva    = {n2_nueva}")
print(f"  factor     = {factor:.4f}")
print(f"  teórico    = sqrt(1000) ≈ {teorico_cuad:.4f}")
print()
print("Algoritmo O(2^n)")
print(f"  n original = {n_exp_original}")
print(f"  n nueva    = {n_exp_nueva}")
print(f"  incremento = {incremento} elementos")
print(f"  teórico    = log2(1000) ≈ {teorico_exp:.4f}")
```

### Salida esperada

```text
Presupuesto original: 1,000,000 operaciones
Presupuesto nueva:    1,000,000,000 operaciones

Algoritmo O(n^2)
  n original = 1000
  n nueva    = 31622
  factor     = 31.6220
  teórico    = sqrt(1000) ≈ 31.6228

Algoritmo O(2^n)
  n original = 19
  n nueva    = 29
  incremento = 10 elementos
  teórico    = log2(1000) ≈ 9.9658
```

### Conclusiones

De esta forma, el código confirma los resultados analíticos y permite extraer las siguientes conclusiones sobre el impacto de aumentar la velocidad del hardware, que depende fuertemente de la complejidad temporal del algoritmo:

Para un algoritmo $O(n^2)$, un incremento de velocidad por un factor $k = 1000$ produce un crecimiento multiplicativo del tamaño de entrada dado por:

$$
N_2 = \sqrt{k} \cdot N_1 = \sqrt{1000} \cdot N_1 \approx 31.62 \cdot N_1.
$$

Por lo tanto, una computadora mil veces más rápida permite resolver entradas aproximadamente 31.62 veces más grandes.

Para un algoritmo $O(2^n)$, el mismo incremento de velocidad produce un crecimiento aditivo:

$$
N_2 = N_1 + \log_2(k) = N_1 + \log_2(1000) \approx N_1 + 9.97.
$$

Es decir, una computadora mil veces más rápida solo permite procesar alrededor de 10 elementos adicionales.

En consecuencia, se confirma que para problemas con complejidad exponencial las mejoras de hardware tienen un efecto marginal. La solución eficiente no consiste en aumentar la capacidad de cómputo, sino en diseñar mejores algoritmos, aplicar técnicas de optimización, heurísticas o programación dinámica.

Por tanto, este código valida numéricamente el análisis teórico y refuerza la conclusión principal del ejercicio: el crecimiento del tamaño de entrada frente a mejoras de hardware está determinado por la complejidad del algoritmo, no por la velocidad bruta de la máquina.



##  Código

Esta es la explicación de cada una de las visualizaciones generadas.

### Figura 1. Presupuesto de operaciones

`fig1_presupuesto_operaciones.png`

Representa la mejora de capacidad computacional entre ambas computadoras. Compara el presupuesto original de \\(10^6\\) operaciones con el nuevo presupuesto de \\(10^9\\). Su objetivo es mostrar visualmente que una computadora mil veces más rápida dispone de mil veces más operaciones para resolver un problema durante la misma hora.

### Figura 2. Comparación de tamaños de entrada

`fig2_tamanos_de_entrada.png`

Compara directamente cuánto crece el tamaño máximo de entrada para los dos algoritmos estudiados. En el caso cuadrático, pasa de 1000 a 31622 elementos, mientras que en el exponencial pasa de 19 a 29. Es la figura que mejor resume numéricamente la respuesta principal del ejercicio.

### Figura 3. Factores de crecimiento

`fig3_factores_de_crecimiento.png`

Representa las expresiones teóricas obtenidas en la demostración: \\(\sqrt{k}\\) para el algoritmo cuadrático y \\(\log_2(k)\\) para el exponencial. Se destaca especialmente el punto \\(k=1000\\), permitiendo observar cómo ambas funciones responden de manera diferente ante el mismo incremento de velocidad del hardware.

### Figura 4. Costos y presupuestos

`fig4_costos_y_presupuestos.png`

Muestra los costos de ejecución de ambos algoritmos junto con los presupuestos de operaciones de las dos computadoras. Las líneas horizontales representan los límites computacionales y las verticales señalan los tamaños máximos de entrada alcanzables. Permite comprender gráficamente por qué el crecimiento exponencial se vuelve tan restrictivo.

### Figura 5. Evolución animada de la mejora del hardware

`fig5_evolucion_mejora_hardware.gif`

GIF · 10 etapas

Esta animación muestra cómo evolucionan los resultados cuando el factor de velocidad aumenta progresivamente desde \\(k=1\\) hasta \\(k=1000\\). Presenta dos gráficos independientes: uno para el crecimiento multiplicativo del algoritmo cuadrático y otro para el incremento aditivo del exponencial. La última etapa permite visualizar la diferencia entre obtener aproximadamente 31.62 veces más entrada y solamente unos 10 elementos adicionales.

