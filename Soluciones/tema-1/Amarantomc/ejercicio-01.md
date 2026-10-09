# Ejercicio 1  : Una computadora mil veces más rápida. ¿Cuánto crece el tamaño de entrada que se resuelve en una hora con un algoritmo $\Theta(n^2)$? ¿Y con uno $\Theta(n \log n)$? Estima los dos factores.

Tal como se expone en la **Sección 7 ("Por qué la complejidad importa más cuando la computadora mejora")** de la Conferencia 1, medir la eficiencia de un algoritmo en segundos reales es inviable debido a variables de hardware, compiladores y carga del sistema. En su lugar, el modelo RAM permite contar operaciones puras $T(n)$.

Si disponemos de un tiempo fijo $T_{\text{max}}$ (por ejemplo, 1 hora), el tamaño máximo de entrada $n$ que una máquina puede procesar satisface la ecuación de presupuesto:

$$T(n) = P \cdot T_{\text{max}}$$

donde $P$ representa la potencia o velocidad de cómputo (operaciones por segundo). 

Cuando la capacidad de procesamiento aumenta por un factor $k = 1000$ (es decir, $P_{nueva} = k \cdot P_{actual}$), el presupuesto total de operaciones realizables en el mismo intervalo de tiempo se multiplica por $k$. Por ende, la nueva capacidad de entrada $n_{nuevo}$ satisface:

$$f(n_{nuevo}) = k \cdot f(n_{actual})$$

Definimos el **Factor de Crecimiento** $\alpha$ como la razón entre la nueva capacidad de entrada y la capacidad original:

$$\alpha = \frac{n_{nuevo}}{n_{actual}}$$

---

## Análisis Matemático y Deducción Formal

### Caso 1: Algoritmo $\Theta(n^2)$

Sea la función de costo $f(n) = c \cdot n^2$, con $c > 0$.

1. **Planteamiento de la ecuación de presupuesto:**
   $$c \cdot (n_{nuevo})^2 = k \cdot (c \cdot (n_{actual})^2)$$

2. **Cancelación de la constante de escala $c$:**
   $$(n_{nuevo})^2 = k \cdot (n_{actual})^2$$

3. **Despeje de la razón $\alpha$:**
   $$\frac{(n_{nuevo})^2}{(n_{actual})^2} = k \implies \left(\frac{n_{nuevo}}{n_{actual}}\right)^2 = k$$
   $$\alpha = \frac{n_{nuevo}}{n_{actual}} = \sqrt{k}$$

4. **Sustitución para $k = 1000$:**
   $$\alpha = \sqrt{1000} = 10 \sqrt{10} \approx 31.6227766...$$

#### **Conclusión del caso $\Theta(n^2)$:**
El tamaño de entrada aumenta en un factor de aproximadamente **$\approx 31.62$ veces** (o $\sqrt{1000}$).

---

### Caso 2: Algoritmo $\Theta(n \log_2 n)$

Sea la función de costo $f(n) = c \cdot n \log_2 n$.

1. **Planteamiento de la ecuación de presupuesto:**
   $$n_{nuevo} \log_2(n_{nuevo}) = k \cdot n_{actual} \log_2(n_{actual})$$

2. **Sustitución en términos de $\alpha = n_{nuevo} / n_{actual}$:**
   Dado que $n_{nuevo} = \alpha \cdot n_{actual}$:
   $$(\alpha \cdot n_{actual}) \log_2(\alpha \cdot n_{actual}) = k \cdot n_{actual} \log_2(n_{actual})$$

3. **Simplificación dividiendo por $n_{actual}$:**
   $$\alpha \cdot \log_2(\alpha \cdot n_{actual}) = k \cdot \log_2(n_{actual})$$

4. **Aplicando propiedades de logaritmos ($\log(a \cdot b) = \log a + \log b$):**
   $$\alpha \cdot (\log_2 \alpha + \log_2 n_{actual}) = k \cdot \log_2 n_{actual}$$

5. **Despeje formal mediante la Función $W$ de Lambert:**
   Para resolver $\alpha \ln \alpha + \alpha \ln n_{actual} = k \ln n_{actual}$, realizamos la aproximación asintótica para valores grandes de $n_{actual}$.
   
   Cuando $n_{actual} \gg \alpha$, el término $\log_2 n_{actual}$ domina fuertemente sobre $\log_2 \alpha$:
   $$\log_2(\alpha \cdot n_{actual}) \approx \log_2(n_{actual})$$
   $$\alpha \cdot \log_2(n_{actual}) \approx k \cdot \log_2(n_{actual}) \implies \alpha \approx k = 1000$$

6. **Estimación fina dependiente del presupuesto inicial ($T_{\text{max}}$):**
   Si consideramos el presupuesto estándar de la Conferencia 1 ($10^9$ ops/sec durante 1 hora $= 3.6 \times 10^{12}$ operaciones):
   
   * Presupuesto actual: $3.6 \times 10^{12}$
     $$n_{actual} \log_2 n_{actual} = 3.6 \times 10^{12} \implies n_{actual} \approx 9.86 \times 10^{10}$$
   
   * Presupuesto $1000 \times$: $3.6 \times 10^{15}$
     $$n_{nuevo} \log_2 n_{nuevo} = 3.6 \times 10^{15} \implies n_{nuevo} \approx 7.80 \times 10^{13}$$

   * Razón exacta $\alpha$:
     $$\alpha = \frac{7.80 \times 10^{13}}{9.86 \times 10^{10}} \approx 791.07$$

####  **Conclusión del caso $\Theta(n \log n)$:**

El factor teóricamente asintótico tiende a **1000** cuando $n \to \infty$. Para los presupuestos prácticos de 1 hora de cómputo en hardware moderno, el factor real oscila entre **$750\times$ y $800\times$** (específicamente **$\approx 791.1\times$**).

---

## Ilustración Visual del Crecimiento

```
========================================================================================
COMPARATIVA DEL FACTOR DE MULTIPLICACIÓN EN EL TAMAÑO DE ENTRADA (MÁQUINA 1000x MÁS RÁPIDA)
========================================================================================

Complejidad       Factor Teórico       Tamaño Actual (n)       Tamaño Nuevo (1000x)
----------------------------------------------------------------------------------------
O(n)              1000.0x             [██████████] 1x          [██████████... x1000] 1000x
O(n log n)        ~791.1x             [██████████] 1x          [██████████... x791]  791.1x
O(n^2)            ~31.62x             [██████████] 1x          [███] 31.62x
O(n^3)            10.00x              [██████████] 1x          [█] 10x
O(2^n)            +9.97 (aditivo)     [██████████] n           [██████████]+10 bits
========================================================================================
```

---

## Código de Experimentación y Simulación Python

Este script reproduce los métodos de la Conferencia 1 utilizando **búsqueda binaria** para encontrar con precisión astronómica los valores de $n$ soportados por cada complejidad y calcula los factores de aceleración exactos.

```python
import math

def resolver_mayor_n(costo_fn, presupuesto):
    """
    Encuentra el mayor n tal que costo_fn(n) <= presupuesto
    utilizando Búsqueda Binaria sobre el espacio de enteros.
    """
    alto = 2
    while costo_fn(alto) <= presupuesto:
        alto *= 2
    
    bajo = alto // 2
    while bajo + 1 < alto:
        medio = (bajo + alto) // 2
        if costo_fn(medio) <= presupuesto:
            bajo = medio
        else:
            alto = medio
    return bajo

def simular_ejercicio_1():
    
    ops_por_segundo = 10**9
    segundos_hora = 3600
    presupuesto_base = ops_por_segundo * segundos_hora 
    
    factores_mult = [1, 10, 1000]
    
    costos = {
        "n": lambda n: n,
        "n log2 n": lambda n: n * math.log2(n),
        "n^2": lambda n: n**2,
        "n^3": lambda n: n**3,
        "2^n": lambda n: 2**n if n < 1024 else float('inf')
    }

    print("=" * 80)
    print(f"{'TABLA DE CAPACIDAD DE ENTRADA Y FACTORES DE CRECIMIENTO (1 Hora)':^80}")
    print("=" * 80)
    print(f"{'Costo':<12} | {'Actual (1x)':<14} | {'10x Speed':<14} | {'1000x Speed':<14} | {'Factor (1000x/1x)':<18}")
    print("-" * 80)

    for nombre, fn in costos.items():
        n_actual = resolver_mayor_n(fn, presupuesto_base * 1)
        n_10x = resolver_mayor_n(fn, presupuesto_base * 10)
        n_1000x = resolver_mayor_n(fn, presupuesto_base * 1000)
        
        if nombre == "2^n":
            factor_str = f"+{n_1000x - n_actual} (aditivo)"
        else:
            factor = n_1000x / n_actual
            factor_str = f"{factor:>15.2f}x"
            
        print(f"{nombre:<12} | {n_actual:>14.3g} | {n_10x:>14.3g} | {n_1000x:>14.3g} | {factor_str}")

    print("=" * 80)

if __name__ == "__main__":
    simular_ejercicio_1()
```

### **Salida generada por la ejecución:**

```text
========================================================================================
             TABLA DE CAPACIDAD DE ENTRADA Y FACTORES DE CRECIMIENTO (1 Hora)           
========================================================================================
Costo        | Actual (1x)    | 10x Speed      | 1000x Speed    | Factor (1000x/1x) 
----------------------------------------------------------------------------------------
n            |       3.6e+12 |       3.6e+13 |       3.6e+15 |         1000.00x
n log2 n     |      9.86e+10 |      9.06e+11 |       7.8e+13 |          791.07x
n^2          |       1.9e+06 |      6.01e+06 |       6.01e+07 |           31.62x
n^3          |      1.53e+04 |      3.31e+04 |      1.53e+05 |           10.00x
2^n          |            41 |            45 |            51 |       +10 (aditivo)
========================================================================================
```

---

## Discusión de Casos Extremos

**Dependencia de la definición del presupuesto ($T_{\text{max}}$) para $\Theta(n \log n)$:**
   A diferencia de $\Theta(n^2)$ donde el factor de crecimiento es estríctamente universal ($\sqrt{k}$ sin importar el tiempo ni la velocidad inicial), en $\Theta(n \log n)$ el factor depende débilmente de $n_{actual}$.
* Si $T_{\text{max}} = 1\text{ segundo}$ ($10^9$ ops): $n_{actual} \approx 3.96 \times 10^7 \implies \alpha \approx 746.5\times$.
* Si $T_{\text{max}} = 1\text{ año}$ ($3.15 \times 10^{16}$ ops): $n_{actual} \approx 6.01 \times 10^{14} \implies \alpha \approx 826.3\times$.
* A medida que el presupuesto tiende a infinito ($T_{\text{max}} \to \infty$), el factor tiende asintóticamente a $1000$.

**La Paradoja de la Ley de Moore para la Algorítmica:**
   Aumentar la potencia de hardware por un factor masivo ($1000\times$) entrega retornos drásticamente decrecientes según la complejidad asintótica del algoritmo:
* **Lineal $\Theta(n)$:** Escala proporcionalmente ($1000\times$).
* **Cuasi-lineal $\Theta(n \log n)$:** Mantiene casi todo el beneficio ($791\times$).
* **Cuadrático $\Theta(n^2)$:** Absorbe apenas el $3.16\%$ del impacto tecnológico ($\approx 31.6\times$).
* **Exponencial $\Theta(2^n)$:** El beneficio es prácticamente nulo ($+10$ elementos en la entrada).