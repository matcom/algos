# Ejercicio 1 - Una computadora mil veces más rápida

> ¿Cuánto crece el tamaño de entrada que se resuelve en una hora con un algoritmo
> $\Theta(n^2)$? ¿Y con uno $\Theta(2^n)$? Estima los dos factores.


## 1. El problema

Sea $N$ el mayor tamaño de entrada que un algoritmo resuelve en una hora con la
computadora de hoy. Si una máquina **$s$ veces más rápida** hace el mismo trabajo en el
mismo tiempo, el presupuesto de operaciones pasa de $B$ a $sB$. El nuevo tamaño $N'$ es
el que satisface $\text{costo}(N') = s\,B = s\cdot\text{costo}(N)$. La pregunta es por
qué factor crece $N$, según la forma del costo. Aquí $s = 1000$.

## 2. Algoritmo $\Theta(n^2)$: el factor es $\sqrt{s}$

Con costo $c\,n^2$,
$$c\,N'^2 = s\cdot c\,N^2 \;\Longrightarrow\; N'^2 = s\,N^2 \;\Longrightarrow\;
\boxed{N' = \sqrt{s}\,N}.$$

Con $s = 1000$, el factor es $\sqrt{1000} \approx 31{,}6$. Diez veces más veloz solo
compra $\sqrt{10}\approx 3{,}16$ veces más tamaño. **El factor es multiplicativo pero
se abre la raíz:** más potencia bruta rinde cada vez menos en un algoritmo
polinomial de grado alto. En general, para $\Theta(n^k)$ el factor es $s^{1/k}$.

## 3. Algoritmo $\Theta(2^n)$: el factor es aditivo, $+\log_2 s$

Con costo $c\,2^n$,
$$c\,2^{N'} = s\cdot c\,2^{N} \;\Longrightarrow\; 2^{N'} = s\,2^{N} = 2^{\log_2 s}\,2^N
= 2^{N+\log_2 s} \;\Longrightarrow\; \boxed{N' = N + \log_2 s}.$$

Con $s = 1000$, $\log_2 1000 \approx 9{,}97$: la máquina mil veces más rápida añade
**unas 10 unidades** al tamaño de entrada, y no lo multiplica por nada. Es
lo que dice la conferencia 1, §7: *"el exponencial suma unas 10 unidades al tamaño de
entrada, porque $2^{n+10}\approx 1000\cdot 2^n$"*.

## 4. El contraste, en una tabla

| costo | ecuación | factor de crecimiento de $N$ | con $s=1000$ |
|---|---|---|---|
| $\Theta(n)$ | $N' = sN$ | $\times s$ | $\times 1000$ |
| $\Theta(n^2)$ | $N'^2 = sN^2$ | $\times \sqrt{s}$ | $\times 31{,}6$ |
| $\Theta(n^3)$ | $N'^3 = sN^3$ | $\times \sqrt[3]{s}$ | $\times 10$ |
| $\Theta(2^n)$ | $2^{N'}=s\,2^{N}$ | $+\log_2 s$ | $+9{,}97$ |

La diferencia de **naturaleza** es lo importante: en los polinomiales el tamaño se
**multiplica**; en el exponencial se **suma** una constante. Por eso mil veces más
cómputo le cambia la vida a un algoritmo lineal y casi nada a uno exponencial.

## 5. Figura - crecimiento de $N$ al acelerar la máquina

El eje horizontal es el factor de velocidad $s$ (escala log); el vertical, el factor
por el que crece el tamaño resoluble $N'/N$. Lineal sube como una recta; cuadrático, a
la mitad de pendiente; exponencial es casi plano (el aumento absoluto $\log_2 s$ es
ridículo frente al tamaño).

```
 N'/N
1000 |                                            ● lineal  (×s)
     |                                       ·
 100 |                              ·
     |                     ·
  32 |            ·  ·  ·  ·  ·  ·  ·  ·  ○ cuadrático (×√s)
  10 |      ·  ○
   3 |  ○ ·
   1 |□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□ exponencial (+log₂s ≈ plano)
     +---------------------------------------------------→ s
        10          100          1000
```

Leyenda: `●/·` lineal, `○` cuadrático, `□` exponencial. El exponencial apenas se
despega de 1 porque sumar 10 a un $N$ grande es un cambio relativo minúsculo.

## 6. Comprobación numérica

El siguiente código resuelve $\text{costo}(N')=s\cdot\text{costo}(N)$ por búsqueda
binaria, igual que el programa de la conferencia 1 §7, y confirma los factores.

```python
import math

def mayor_n(costo, presupuesto):
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

hora = 3600 * 10**9                      # presupuesto base de operaciones
costos = {
    "n":   lambda n: n,
    "n^2": lambda n: n * n,
    "n^3": lambda n: n ** 3,
    "2^n": lambda n: 2 ** n,
}
s = 1000
print(f"{'costo':>5} {'N (1x)':>12} {'N (1000x)':>12} {'factor':>10}")
for nombre, c in costos.items():
    N  = mayor_n(c, hora)
    Np = mayor_n(c, s * hora)
    if nombre == "2^n":
        print(f"{nombre:>5} {N:>12} {Np:>12} {f'+{Np-N}':>10}")
    else:
        print(f"{nombre:>5} {N:>12} {Np:>12} {f'x{Np/N:.1f}':>10}")
print(f"sqrt(1000) = {math.sqrt(1000):.2f}   1000^(1/3) = {1000**(1/3):.2f}   "
      f"log2(1000) = {math.log2(1000):.2f}")
```

**Salida:**

```
costo           N (1x)          N (1000x)     factor
    n    3600000000000   3600000000000000      x1000.0
  n^2          1897366           60000000      x31.6
  n^3            15326             153261      x10.0
  2^n               41                 51        +10
```

Los factores medidos - $\times1000$, $\times31{,}6$, $\times10$ y $+10$ - coinciden con
$s$, $\sqrt{s}$, $\sqrt[3]{s}$ y $\log_2 s$.

## 7. Respuesta

- **$\Theta(n^2)$:** el tamaño resoluble crece por un factor $\sqrt{s}=\sqrt{1000}\approx 31{,}6$.
- **$\Theta(2^n)$:** el tamaño resoluble crece en un sumando $\log_2 s=\log_2 1000\approx 10$.

Lo que concluye §7 de la conferencia 1: para un algoritmo exponencial, mil veces más
potencia de cómputo compra casi nada; mejorar el algoritmo vale más que esperar por el
hardware.
