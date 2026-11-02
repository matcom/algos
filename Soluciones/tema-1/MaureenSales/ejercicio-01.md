# Ejercicio 1 — Una computadora mil veces más rápida

**Tema 1 · Diseño y Análisis de Algoritmos · MatCom 2026**
Temas: modelo RAM, notación asintótica, tamaño en bits · Dificultad: ★

---

## Enunciado

> ¿Cuánto crece el tamaño de entrada que se resuelve en una hora con un algoritmo $\Theta(n^2)$? ¿Y con uno $\Theta(n\log n)$? Estima los dos factores.

---

## 1. Planteamiento

Una computadora que hace $10^9$ operaciones por segundo, una hora de presupuesto, y el costo medido en operaciones del modelo RAM, no en segundos.

El algoritmo hace $T(n) = c\cdot f(n)$ operaciones. En una hora la máquina vieja paga $B = 3600\cdot 10^9 = 3{,}6\cdot 10^{12}$ operaciones y la nueva $1000\,B$. Sean $n_0$ y $n_1$ los mayores tamaños que resuelve cada una:

$$
c\,f(n_0) = B, \qquad c\,f(n_1) = 1000\,B
\qquad\Longrightarrow\qquad
\boxed{\;\frac{f(n_1)}{f(n_0)} = 1000\;}
$$

La constante $c$ se cancela. Las constantes dependen de decisiones arbitrarias sobre cómo contar ($5n+3$ o $4n+3$ en la suma de un arreglo), y por eso el análisis se queda con la forma de la función. Para $n^2$ la respuesta no depende ni de $c$ ni de la velocidad absoluta. Para $n\log n$ hay un matiz: la ecuación de arriba no tiene $c$, pero su solución depende de $n_0$, y $n_0$ sí depende de $c$ y de la velocidad. Así que la constante entra, aunque solo a través de $n_0$ y de forma muy débil.

## 2. Caso $\Theta(n^2)$

$$
\frac{n_1^2}{n_0^2} = 1000 \;\Longrightarrow\; n_1 = \sqrt{1000}\;n_0 \approx 31{,}62\,n_0 .
$$

El crecimiento es **multiplicativo y constante**: da igual cuánto era $n_0$. En general, para $f(n) = n^k$ el factor es $1000^{1/k}$: $\times 1000$ lineal, $\times 31{,}6$ cuadrático, $\times 10$ cúbico.

## 3. Caso $\Theta(n\log n)$

Ahora la ecuación es

$$
n_1 \log_2 n_1 = 1000\, n_0 \log_2 n_0
\qquad\Longrightarrow\qquad
\frac{n_1}{n_0} = 1000\cdot \frac{\log_2 n_0}{\log_2 n_1}.
$$

No tiene solución cerrada en funciones elementales, y el factor **depende de $n_0$**: no es un número fijo como en el caso cuadrático. Pero se puede encerrar entre dos cotas.

**Cota superior.** Como $n_1 \ge n_0$, $\log_2 n_1 \ge \log_2 n_0$, así que $n_1/n_0 \le 1000$.

**Cota inferior.** Por la cota superior, $\log_2 n_1 \le \log_2 n_0 + \log_2 1000$, así que

$$
\frac{n_1}{n_0} \;\ge\; 1000\cdot\frac{\log_2 n_0}{\log_2 n_0 + \log_2 1000} \;=\; \frac{1000}{1 + 9{,}97/\log_2 n_0}.
$$

**Estimación.** $n_0 \approx 9{,}86\cdot 10^{10}$ y $\log_2 n_0 \approx 36{,}5$:

$$
785 \;\lesssim\; \frac{n_1}{n_0} \;\le\; 1000 .
$$

Iterando una vez más la ecuación con la cota inferior ($\log_2 n_1 \approx 36{,}5 + \log_2 785 \approx 46{,}1$) sale $n_1/n_0 \approx 1000\cdot 36{,}5/46{,}1 \approx 791$, que es justo el cociente que da la tabla de abajo: $7{,}8\cdot 10^{13} / 9{,}86\cdot 10^{10} \approx 791$.

**Lectura.** El factor tiende a 1000 cuando $n_0 \to \infty$, porque $\log n_1/\log n_0 \to 1$, pero despacio: el logaritmo gana unos $\log_2 1000 \approx 10$ bits, y 10 sobre 36 no es poco. Un algoritmo $n\log n$ se comporta "casi" como uno lineal frente a una máquina más rápida, y muchísimo mejor que uno cuadrático: $791$ contra $31{,}6$.

## 4. Las dos respuestas en la tabla

Esta es la tabla que calcula el programa, con la columna de 1000× y el factor que pide el ejercicio:

```text
 costo        una hora          1000× más rápida      cómo crece n
 ───────────────────────────────────────────────────────────────────
 n            3.6e12            3.6e15                × 1000
 n log2 n     9.86e10           7.8e13                × ~791   (entre 785 y 1000)
 n^2          1.9e6             6.0e7                 × 31.6
 n^3          1.53e4            1.53e5                × 10
 2^n          41                51                    + 10      (suma, no multiplica)
```

La última fila no la pide el ejercicio, pero sirve de contraste: para un exponencial, mil veces más potencia de cómputo suma unas 10 unidades al tamaño de entrada, porque $2^{n+10}\approx 1000\cdot 2^n$.

## 5. El otro lado de la cuenta: los datos también crecen

El problema también se puede mirar desde el otro lado: si la máquina es 1000 veces más rápida y los datos son 1000 veces más grandes, ¿cuánto tarda cada algoritmo?

- $n^2$: el trabajo crece $1000^2 = 10^6$ veces y la máquina es $10^3$ veces más rápida: tarda **1000 veces más** que hoy.
- $n\log n$: el trabajo crece $1000\cdot\frac{\log_2(1000\,n_0)}{\log_2 n_0} \approx 1000\cdot \frac{46{,}5}{36{,}5} \approx 1270$ veces: tarda **1,27 veces** lo de hoy.

Con datos que crecen, un algoritmo cuadrático empeora con los años, y mejorar el algoritmo vale más que esperar por el hardware.

## 6. La conexión con el tamaño en bits

La misma cuenta, hecha con la unidad correcta, es la que muestra que la primalidad por división es exponencial. Prueba unos $\sqrt N = 2^{b/2}$ divisores si $N$ tiene $b$ bits, así que con la máquina nueva

$$
2^{b_1/2} = 1000\cdot 2^{b_0/2} \;\Longrightarrow\; b_1 = b_0 + 2\log_2 1000 \approx b_0 + 20 .
$$

Se le **suman** 20 bits al tamaño, como al $2^n$ de la tabla. En el valor de $N$ parecía un algoritmo sublineal ($\sqrt N$), y medido en bits se comporta como un exponencial.

---

## 7. Casos de prueba

Calculo $n_0$ y $n_1$ con búsqueda binaria y compruebo lo que demostré: el factor $\sqrt{1000}$ para $n^2$, las dos cotas y la estimación para $n\log n$, que la constante no importa, y la cuenta en bits de la primalidad.

```python
import math

def mayor_n(f, presupuesto):
    """Mayor n >= 1 con f(n) <= presupuesto (f creciente). Búsqueda binaria."""
    lo, hi = 1, 1
    while f(hi) <= presupuesto:      # buscar una cota superior
        hi *= 2
    # invariante: f(lo) <= presupuesto < f(hi)
    while hi - lo > 1:
        mid = (lo + hi) // 2
        if f(mid) <= presupuesto:
            lo = mid
        else:
            hi = mid
    return lo

B = 3600 * 10**9                     # una hora a 10^9 op/s
funciones = {
    "n":        lambda n: n,
    "n log2 n": lambda n: n * math.log2(n) if n > 1 else 1,
    "n^2":      lambda n: n * n,
    "n^3":      lambda n: n ** 3,
    "2^n":      lambda n: 2 ** n,
}

print(f"{'f(n)':10} {'n0':>18} {'n1':>22} {'n1/n0':>9} {'n1-n0':>22}")
res = {}
for nombre, f in funciones.items():
    n0, n1 = mayor_n(f, B), mayor_n(f, 1000 * B)
    res[nombre] = (n0, n1)
    print(f"{nombre:10} {n0:18,} {n1:22,} {n1/n0:9.2f} {n1-n0:22,}")

# --- n^2: factor sqrt(1000), independiente de n0 ---
n0, n1 = res["n^2"]
assert abs(n1 / n0 - math.sqrt(1000)) < 0.01

# --- n log n: entre la cota inferior y 1000, y la estimación de la sección 3 ---
n0, n1 = res["n log2 n"]
inferior = 1000 / (1 + math.log2(1000) / math.log2(n0))
estimacion = 1000 * math.log2(n0) / (math.log2(n0) + math.log2(inferior))
print(f"\nn log n: cota inferior {inferior:.1f} <= factor {n1/n0:.1f} <= 1000;"
      f" estimación iterada {estimacion:.1f}")
assert inferior <= n1 / n0 <= 1000
assert abs(estimacion - n1 / n0) < 1

# --- el factor de n log n depende de n0 y tiende a 1000 ---
for horas in [1e-6, 1, 1e6]:
    a = mayor_n(funciones["n log2 n"], B * horas)
    b = mayor_n(funciones["n log2 n"], 1000 * B * horas)
    print(f"presupuesto {B * horas:9.1e}: n0 = {a:.3g}, factor = {b / a:.1f}")

# --- la constante oculta: no cambia el factor de n^2; en n log n solo entra vía n0 ---
for c in (1, 7, 1000):
    cuad = lambda n: c * n * n
    nlog = lambda n: c * n * math.log2(n) if n > 1 else c
    a2, b2 = mayor_n(cuad, B), mayor_n(cuad, 1000 * B)
    a, b = mayor_n(nlog, B), mayor_n(nlog, 1000 * B)
    cota_c = 1000 / (1 + math.log2(1000) / math.log2(a))   # la cota inferior con ESE n0
    print(f"c = {c:5}:  factor n^2 = {b2/a2:.2f}   n0 = {a:.3g}, factor n log n = {b/a:.2f}"
          f" (cota inferior {cota_c:.1f})")
    assert abs(b2 / a2 - math.sqrt(1000)) < 0.01
    assert cota_c <= b / a <= 1000

# --- datos 1000 veces más grandes en la máquina nueva (sección 5) ---
n0 = res["n log2 n"][0]
print(f"\nn log n con datos x1000 y máquina x1000: tarda "
      f"{funciones['n log2 n'](1000 * n0) / (1000 * funciones['n log2 n'](n0)):.2f} veces lo de hoy")

# --- primalidad por división medida en bits: 2^(b/2) operaciones (sección 6) ---
b0 = mayor_n(lambda b: 2 ** (b / 2), B)
b1 = mayor_n(lambda b: 2 ** (b / 2), 1000 * B)
print(f"primalidad por división: {b0} bits -> {b1} bits (+{b1 - b0})")
assert b1 - b0 in (19, 20)
print("todas las pruebas pasaron")
```

### Salida

```text
f(n)                       n0                     n1     n1/n0                  n1-n0
n           3,600,000,000,000  3,600,000,000,000,000   1000.00  3,596,400,000,000,000
n log2 n       98,574,774,544     78,008,697,597,778    791.37     77,910,122,823,234
n^2                 1,897,366             60,000,000     31.62             58,102,634
n^3                    15,326                153,261     10.00                137,935
2^n                        41                     51      1.24                     10

n log n: cota inferior 785.6 <= factor 791.4 <= 1000; estimación iterada 791.5
presupuesto   3.6e+06: n0 = 2.04e+05, factor = 653.5
presupuesto   3.6e+12: n0 = 9.86e+10, factor = 791.4
presupuesto   3.6e+18: n0 = 6.45e+16, factor = 851.6
c =     1:  factor n^2 = 31.62   n0 = 9.86e+10, factor n log n = 791.37 (cota inferior 785.6)
c =     7:  factor n^2 = 31.62   n0 = 1.52e+10, factor n log n = 778.83 (cota inferior 772.4)
c =  1000:  factor n^2 = 31.62   n0 = 1.33e+08, factor n log n = 739.06 (cota inferior 730.3)

n log n con datos x1000 y máquina x1000: tarda 1.27 veces lo de hoy
primalidad por división: 83 bits -> 103 bits (+20)
todas las pruebas pasaron
```

La fila de $n\log n$ da los $9{,}86\cdot 10^{10}$ y $7{,}8\cdot 10^{13}$ de la tabla. Las tres líneas de "presupuesto" muestran que el factor de $n\log n$ no es una constante: sube hacia 1000 cuando el problema crece. Las tres líneas de "c" muestran el matiz de la sección 1: el factor de $n^2$ es $31{,}62$ con cualquier constante, y el de $n\log n$ cambia un poco con $c$ porque cambia $n_0$, pero siempre queda entre la cota inferior calculada con ese $n_0$ y 1000.

## 8. Conclusión

| algoritmo | qué le pasa a $n$ con una máquina 1000× más rápida |
|---|---|
| $\Theta(n^2)$ | se **multiplica** por $\sqrt{1000} \approx 31{,}6$, para todo $n_0$ |
| $\Theta(n\log n)$ | se multiplica por $1000\cdot\frac{\log n_0}{\log n_1}$: entre $\frac{1000}{1+\log_2 1000/\log_2 n_0}$ y $1000$; $\approx 791$ para una hora a $10^9$ op/s |

---

**Uso de IA**: implementación de algoritmos, generación de casos de prueba y correcciones de redacción.
