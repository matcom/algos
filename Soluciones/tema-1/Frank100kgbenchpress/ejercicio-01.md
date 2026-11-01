# Ejercicio 1: Una computadora mil veces más rápida

**Enunciado:** ¿Cuánto crece el tamaño de entrada que se resuelve en una hora con un algoritmo \(\Theta(n^2)\)? ¿Y con uno \(\Theta(n\log n)\)? Estima los dos factores. (C1)

**Modelo:** Contamos operaciones en el modelo RAM, asumiendo que una computadora hace \(O(1)\) operaciones por paso. El presupuesto de tiempo es fijo (1 hora).

---

## 1. Algoritmo \(\Theta(n^2)\)

Sea \(T(n)=c\cdot n^2\) el costo del algoritmo en la computadora antigua y \(T'(n)=\frac{c}{1000}\cdot n^2\) el costo en la nueva computadora, que es 1000 veces más rápida.

Buscamos el factor de crecimiento \(k\) tal que el nuevo tamaño de entrada sea \(n'=k\cdot n\).

Igualamos los tiempos de ejecución para mantener el mismo presupuesto de una hora:

\[
c\cdot n^2=\frac{c}{1000}\cdot(k\cdot n)^2
\]

Simplificando \(c\) y \(n^2\) en ambos lados:

\[
1=\frac{k^2}{1000}
\]

\[
k^2=1000
\]

\[
k=\sqrt{1000}\approx31.62
\]

**Resultado:** El tamaño de entrada que se puede resolver aumenta en un factor aproximado de:

\[
\boxed{k\approx31.6}
\]

Es decir, la nueva computadora puede procesar entradas aproximadamente 31.6 veces más grandes que la anterior utilizando un algoritmo cuadrático.

---

## 2. Algoritmo \(\Theta(n\log_2 n)\)

Sea \(T(n)=c\cdot n\log_2 n\) el costo del algoritmo en la computadora antigua y \(T'(n)=\frac{c}{1000}\cdot n\log_2 n\) el costo en la nueva.

Al igual que en el caso anterior, buscamos el factor \(k\) tal que \(n'=k\cdot n\).

Igualamos los tiempos de ejecución:

\[
c\cdot n\log_2 n=
\frac{c}{1000}\cdot(k\cdot n)\log_2(k\cdot n)
\]

Simplificando \(c\) y \(n\):

\[
\log_2 n=
\frac{k}{1000}\log_2(kn)
\]

Aplicando la propiedad del logaritmo:

\[
\log_2 n=
\frac{k}{1000}(\log_2 k+\log_2 n)
\]

Multiplicando ambos lados por 1000:

\[
1000\log_2 n=k(\log_2 k+\log_2 n)
\]

Despejando \(k\):

\[
\boxed{
k=\frac{1000}{1+\frac{\log_2 k}{\log_2 n}}
}
\]

A diferencia del caso cuadrático, aquí el factor de crecimiento depende del tamaño inicial \(n\), por lo que necesitamos conocerlo para obtener un valor numérico más preciso.

### Estimación del factor

Para tamaños de entrada suficientemente grandes, el término \(\log_2 n\) crece y la proporción:

\[
\frac{\log_2 k}{\log_2 n}
\]

se hace cada vez más pequeña.

Por tanto, podemos aproximar:

\[
k\approx1000
\]

Sin embargo, para tamaños finitos, el factor es inferior a 1000.

Por ejemplo, si el tamaño inicial es \(n=10^6\):

\[
\log_2(10^6)\approx19.93
\]

Sustituyendo en la ecuación:

\[
k(19.93+\log_2 k)=19930
\]

Resolviendo numéricamente esta ecuación:

\[
\boxed{k\approx679.34}
\]

Por tanto, si la computadora antigua podía resolver una entrada de un millón de elementos, la nueva podría resolver aproximadamente:

\[
n'=679.34\cdot10^6
\]

Es decir, unos 679 millones de elementos.

Para observar cómo influye el tamaño inicial, podemos considerar otros ejemplos:

| Tamaño inicial \(n\) | Factor aproximado \(k\) |
|:---:|:---:|
| \(10^3\) | 524.5 |
| \(10^6\) | 679.3 |
| \(10^9\) | 757.6 |
| \(10^{12}\) | 805.1 |

**Resultado:** El tamaño de entrada aumenta en un factor que depende de \(n\), pero que se aproxima a 1000 a medida que el tamaño inicial crece.

---

## 3. Conclusión

| Complejidad | Factor de crecimiento del tamaño de entrada |
|:---|:---:|
| \(\Theta(n^2)\) | \(\sqrt{1000}\approx31.6\) |
| \(\Theta(n\log_2 n)\) | Depende de \(n\), pero se aproxima a 1000 |

**Lección de la C1:**

Un aumento de 1000 veces en la velocidad de una computadora no implica que todos los algoritmos puedan procesar entradas 1000 veces mayores.

El beneficio depende directamente de la complejidad del algoritmo. En uno cuadrático, el tamaño de entrada solamente aumenta unas 31.6 veces, mientras que en uno de complejidad \(n\log n\) puede aumentar varios cientos de veces, acercándose a un factor de 1000 para tamaños de entrada suficientemente grandes.

Esto demuestra que los algoritmos con menor crecimiento asintótico aprovechan mucho mejor los incrementos en la capacidad de procesamiento.