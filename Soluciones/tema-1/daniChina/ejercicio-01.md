# Ejercicio 1: una computadora mil veces más rápida

**Ejercicio 1.** ¿Cuánto crece el tamaño de entrada que se resuelve en una hora con un algoritmo Θ(n²)? ¿Y con uno Θ(n log n)? (la máquina nueva es 1000 veces más rápida)

## 1. Idea

Podemos pensar la hora como una cantidad fija de operaciones. Si la máquina nueva hace 1000 veces más operaciones en esa hora, quiero saber cuánto más grande puede ser n.

El costo de un algoritmo Θ(g(n)) lo modelo como c·g(n), donde c es una constante que no conozco. Como las dos máquinas corren el mismo algoritmo, c es la misma en las dos.

Sea T las operaciones que hace la máquina vieja en una hora, n el tamaño máximo que resuelve y n' el de la máquina nueva:

```
máquina vieja:  c·g(n)  = T
máquina nueva:  c·g(n') = 1000·T
```

Al dividir la segunda ecuación entre la primera, c y T se cancelan:

```
g(n') = 1000·g(n)        (1)
```

O sea que el resultado solo depende de la forma de g.

## 2. Caso Θ(n²)

Con g(n) = n², la ecuación (1) queda:

```
(n')² = 1000·n²
n' = √1000 · n
```

**Respuesta: el tamaño se multiplica por √1000 ≈ 31.6**, sin importar cuál era n.

## 3. Caso Θ(n log n)

Ahora (1) queda n'·log(n') = 1000·n·log(n). Aquí no puedo despejar n', porque aparece afuera y dentro del logaritmo. Entonces hago n' = k·n, donde k es el factor que busco:

```
k·n·log(k·n) = 1000·n·log(n)
k·(log k + log n) = 1000·log n        (dividí entre n)
k·(1 + log k / log n) = 1000          (dividí entre log n)        (2)
```

La base del logaritmo no importa, porque solo aparece el cociente log k / log n.

### Entre qué valores está k

Supongo n ≥ 1000.

- En (2), el paréntesis es mayor que 1 (porque k > 1), así que k < 1000.
- Como k < 1000 ≤ n, se cumple log k ≤ log n, y el paréntesis es a lo sumo 2. Entonces k ≥ 500.

Para n muy grande, log k / log n se acerca a 0, el paréntesis se acerca a 1 y k se acerca a 1000.

### Estimación a mano

De (2), k = 1000 / (1 + log₂k / log₂n). Como k < 1000, log₂k < log₂1000, y entonces:

```
k > 1000·log₂n / (log₂n + log₂1000)        (3)
```

Por ejemplo, con n = 10⁶: log₂n ≈ 19.93 y log₂1000 ≈ 9.97, así que k > 1000·19.93 / 29.9 ≈ 666.7.

### Valor más exacto

No pude despejar k, pero (2) se puede escribir como

```
k = 1000 / (1 + log₂k / log₂n)
```

La idea es empezar con k = 1000 (sabemos que k es menor, pero está cerca), calcular el lado derecho para obtener un k mejor, y repetir hasta que k casi no cambie.

Ejemplo con n = 10⁶ (log₂n ≈ 19.93):

```
paso 1: k = 1000 / (1 + log₂(1000)/19.93) = 666.67
paso 2: k = 1000 / (1 + log₂(666.67)/19.93) = 679.97
paso 3: k = 1000 / (1 + log₂(679.97)/19.93) = 679.31
paso 4: k = 679.34
```

Se estabiliza muy rápido, en unos 4 pasos ya casi no cambia. Hice un script (`ejercicio-01.py`) que repite esto para varios n:

```
     n  estimacion         k    n nuevo
  10^3       500.0     524.5  5.245e+05
  10^4       571.4     590.7  5.907e+06
  10^5       625.0     640.5  6.405e+07
  10^6       666.7     679.3  6.793e+08
  10^7       700.0     710.5  7.105e+09
  10^8       727.3     736.2  7.362e+10
  10^9       750.0     757.6  7.576e+11
```

Se puede observar que:
- k siempre está entre 500 y 1000, como demostré arriba.
- La estimación (3) siempre queda por debajo de k, y se acerca más cuando n crece.
- k aumenta con n y se acerca a 1000.

## 4. Conclusión

**Respuestas:**

- **Θ(n²):** el tamaño se multiplica por √1000 ≈ 31.6, sin importar el valor de n.
- **Θ(n log n):** el tamaño se multiplica por un factor k con 500 ≤ k < 1000. Depende de n: k ≈ 525 para n = 10³ y k ≈ 758 para n = 10⁹.

**Ejemplo:** si la máquina vieja resuelve n = 10⁶ en una hora, la nueva resuelve:

- con Θ(n²): n' ≈ 3.2·10⁷ (unas 32 veces más)
- con Θ(n log n): n' ≈ 6.8·10⁸ (unas 680 veces más)

**Conclusión:** una máquina 1000 veces más rápida no resuelve un problema 1000 veces más grande. Con n² se aprovecha muy poco de la mejora (31.6 de 1000), y con n log n se aprovecha bastante más (más de la mitad). Por eso, además de mejorar el hardware, conviene usar un algoritmo con menor complejidad.
