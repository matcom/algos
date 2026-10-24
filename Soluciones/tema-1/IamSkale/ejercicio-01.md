# Ejercicio 1 ★ — Una computadora mil veces más rápida (C1)

> ¿Cuánto crece el tamaño de entrada que se resuelve en una hora con un algoritmo $\Theta(n^2)$? ¿Y con uno $\Theta(n\log n)$? Estima los dos factores.


## Planteamiento

Suponemos que el costo es $T(n)\approx c\cdot g(n)$ operaciones para $n$ grande, y que la máquina actual hace $V$ operaciones por segundo. En una hora el presupuesto es $P = 3600\,V$ operaciones. La máquina nueva tiene presupuesto $1000P$.

Sea $n$ el mayor tamaño que se resuelve hoy, $c\,g(n)=P$, y sea $n'$ el que se resuelve con la máquina nueva, $c\,g(n') = 1000P$. Dividiendo, **la constante $c$ se cancela**:

$$\frac{g(n')}{g(n)} = 1000.$$

### Caso $\Theta(n^2)$

$$\frac{n'^2}{n^2}=1000 \;\Longrightarrow\; n' = \sqrt{1000}\,n \approx 31{,}62\,n.$$

El factor es exactamente $\sqrt{1000}$, sin importar la constante, la velocidad de la máquina ni el tamaño actual.

### Caso $\Theta(n\log n)$

Escribimos $n' = f\cdot n$ y buscamos $f$:

$$f n \log_2(f n) = 1000\, n\log_2 n \;\Longrightarrow\; f\,(\log_2 n + \log_2 f) = 1000\log_2 n \;\Longrightarrow\; f = \frac{1000}{1+\dfrac{\log_2 f}{\log_2 n}}.$$

De ahí salen dos conclusiones:

1. $f<1000$ siempre (el denominador es mayor que 1), y $f\to 1000$ cuando $n\to\infty$, porque $\log_2 f/\log_2 n\to 0$.
2. Como $f\le 1000$, $\log_2 f\le \log_2 1000\approx 9{,}97$, así que
$$\frac{1000}{1+9{,}97/\log_2 n}\;\le\; f\;<\;1000 .$$

Con la máquina de la conferencia 1, sección 7 ($V=10^9$ op/s, una hora): $P=3{,}6\cdot10^{12}$, $n\approx 9{,}86\cdot10^{10}$, $\log_2 n\approx 36{,}5$. Iterando la ecuación de punto fijo desde $f=1000$:

$$f_1 = \frac{1000}{1+9{,}97/36{,}5}\approx 785,\quad f_2=\frac{1000}{1+9{,}62/36{,}5}\approx 791,\quad f_3\approx 791.$$

**El factor es $\approx 791$**: el algoritmo $n\log n$ aprovecha casi toda la mejora (un 79 %), muy lejos del 3 % ($31{,}6/1000$) del cuadrático.

A diferencia del caso cuadrático, este factor depende un poco del tamaño $n$ en el que se esté trabajando (y por tanto de $c$ y de $V$), pero para cualquier tamaño realista está entre 700 y 1000.

## Código de validación

Usamos el mismo programa de búsqueda binaria de la conferencia 1 (§7) para encontrar el mayor $n$ con $\text{costo}(n)\le$ presupuesto. Con él calculamos, para varias funciones de costo ($n$, $n\log n$, $n^2$, $n^3$, $2^n$), el mayor tamaño que se resuelve en una hora a $10^9$ op/s, el que se resuelve con un presupuesto 1000 veces mayor, y el factor entre los dos.

> Código: [ejercicio-01.py](ejercicio-01.py), parte 1.

```text
   costo       actual        1000x     factor
       n      3.6e+12      3.6e+15       1000
 n log n     9.86e+10      7.8e+13      791.4
     n^2      1.9e+06        6e+07      31.62
     n^3     1.53e+04     1.53e+05         10
     2^n           41           51      1.244
```

Comprobamos las dos fórmulas contra lo medido:

> Código: [ejercicio-01.py](ejercicio-01.py), parte 2.

```text
n hoy = 9.86e+10, factor por la fórmula = 791.4, factor medido = 791.4
```

El factor de $n\log n$ depende (poco) de la velocidad de partida; el de $n^2$ no:

> Código: [ejercicio-01.py](ejercicio-01.py), parte 3.

```text
    op/s  n hoy (n log n)  factor n log n  factor n^2
   1e+06         1.33e+08           739.1       31.62
   1e+09         9.86e+10           791.4       31.62
   1e+12          7.8e+13           826.5       31.62
   1e+15         6.45e+16           851.6       31.62
```

## Conclusión

- $\Theta(n^2)$: el tamaño resoluble crece en un factor $\sqrt{1000}\approx 31{,}6$.
- $\Theta(n\log n)$: crece en un factor un poco menor que 1000; con $10^9$ op/s y una hora, $\approx 791$. En general $f = 1000/(1+\log_2 f/\log_2 n)$, que tiende a 1000.
- Mientras mejor (más cercano a lineal) es el algoritmo, más aprovecha el hardware nuevo. Mil veces más potencia le da casi todo al $n\log n$ y apenas un 3 % al cuadrático.
