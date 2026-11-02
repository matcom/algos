# Ejercicio 1 — Una computadora mil veces más rápida

**Uso de IA:** Se usó IA para preparar y revisar este borrador, generar código y casos
de prueba, y apoyar la depuración. Parte de la explicación matemática también recibió
asistencia de IA; esas partes todavía no son redacción propia. Antes de entregar,
reescribiré y verificaré por mi cuenta las demostraciones, análisis de costo y cotas,
según la regla del curso.


> ¿Cuánto crece el tamaño de entrada que se resuelve en una hora con algoritmos
> $\Theta(n^2)$ y $\Theta(n\log n)$? Estima los dos factores. (C1)

## 1. Presupuesto de operaciones

Sigo la normalización de la conferencia 1, §7: una computadora ejecuta
$10^9$ operaciones por segundo y se dispone de una hora. El presupuesto inicial es
$$B=3600\cdot10^9=3.6\cdot10^{12}\text{ operaciones}.$$
Una máquina 1000 veces más rápida dispone de $1000B$. Suponemos el mismo costo por
operación y buscamos el mayor $N$ para el que el costo del algoritmo cabe en el
presupuesto.

## 2. Algoritmo $\Theta(n^2)$

Si el costo es $cN^2$, la máquina rápida admite $N'$ tal que
$$cN'^2=1000\,cN^2\quad\Longrightarrow\quad
\frac{N'}{N}=\sqrt{1000}\approx31.62.$$
Así, el tamaño de entrada crece aproximadamente **31.6 veces**. El coeficiente $c$ se
cancela, siempre que sea el mismo para ambas máquinas.

Con el presupuesto de §1, C1, §7 obtiene $N=1,897,366$ y
$N'=60,000,000$, cuyo cociente es $31.6228$.

## 3. Algoritmo $\Theta(n\log n)$

En este caso $N'$ satisface
$$cN'\log_2N'=1000\,cN\log_2N.$$
El cociente $r=N'/N$ ya no se obtiene como una potencia fija de 1000, porque el logaritmo
cambia al crecer la entrada. Reordenando:
$$r=1000\,\frac{\log_2N}{\log_2N'}
  =1000\,\frac{\log_2N}{\log_2(rN)}.$$
Por tanto, el factor depende del tamaño inicial $N$. Para el mismo presupuesto de una
hora usado en §7 de C1, los valores son aproximadamente
$$N=98,574,774,544,\qquad N'=78,008,697,597,778,$$
y el factor es
$$\frac{N'}{N}\approx791.3657,$$
es decir, **unas 791.4 veces**. Es mucho más que el factor cuadrático, aunque algo menos
que 1000: el término $\log N$ también aumenta y consume parte del presupuesto extra.

## 4. Cálculo numérico

La búsqueda binaria de C1, §7 permite reproducir las estimaciones para un presupuesto
$B$ y otro $1000B$:

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

hora = 3600 * 10**9
s = 1000
costos = {
    "n^2": lambda n: n**2,
    "n log2 n": lambda n: n * math.log2(n),
}

for nombre, costo in costos.items():
    N = mayor_n(costo, hora)
    N_rapida = mayor_n(costo, s * hora)
    print(nombre, N, N_rapida, N_rapida / N)

# Para n log n, comparar el factor de entrada con el factor de velocidad.
costo = costos["n log2 n"]
N = mayor_n(costo, hora)
print()
print("factor de velocidad -> factor de entrada para n log2 n")
for s in [1, 10, 100, 1000, 10000]:
    print(f"{s:>5} -> {mayor_n(costo, s * hora) / N:.4f}")
```

La ejecución da:

| Costo | $N$ (1×) | $N'$ (1000×) | Factor $N'/N$ |
|---|---:|---:|---:|
| $n^2$ | $1.9\cdot10^6$ | $6.0\cdot10^7$ | $31.6$ |
| $n\log_2 n$ | $98,574,774,544$ | $78,008,697,597,778$ | $791.3657$ |

```mermaid
xychart-beta
    x-axis "log10(s)" [0, 1, 2, 3, 4]
    y-axis "N'/N" 0 --> 8000
    line [1, 9.1942, 85.0678, 791.3657, 7396.8279]
```

```text
factor de velocidad -> factor de entrada para n log2 n
    1 -> 1.0000
   10 -> 9.1942
  100 -> 85.0678
 1000 -> 791.3657
10000 -> 7396.8279
```

Para $n\log n$, el factor de entrada se acerca al factor de velocidad $s$ cuando el
tamaño inicial crece: en $r=N'/N$, la ecuación es
$r=s\,\log_2N/\log_2(rN)$, y la razón de logaritmos tiende a 1 si $N$ crece manteniendo
$s$ fijo.

## 5. Respuesta

- **$\Theta(n^2)$:** el tamaño resoluble se multiplica por $\sqrt{1000}\approx31.6$.
- **$\Theta(n\log n)$:** con el presupuesto de una hora de C1, §7, crece unas **791.4
  veces**. El factor no es universal: depende del tamaño inicial porque también crece
  $\log n$.
