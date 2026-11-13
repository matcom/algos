# Outline: Capítulo 8, algoritmos aleatorios I: Las Vegas y costo esperado

Estado: redactado (2026-11-13), pendiente de revisión. El texto está en `notas.md`.
Destino: `Lectures/2026/08-las-vegas/notas.md`, capítulo 8 del libro.
Extensión objetivo: 5 500–7 000 palabras con el código.
Verificación: `.playground/libro-daa/verif/8/v1.py` y `v2.py` (todas las afirmaciones
sobre casos chicos y fórmulas exactas de abajo salen de ahí).

## Idea del capítulo

Hasta aquí el costo de un algoritmo era un número para cada entrada, y nos
quedábamos con el peor. En este capítulo el algoritmo tira monedas, y para cada entrada
su costo es una **variable aleatoria**. La respuesta, en cambio, es siempre correcta:
eso es un algoritmo **Las Vegas**. La garantía que se demuestra es el costo
**esperado** sobre las monedas del algoritmo, para la **peor** entrada.

La herramienta es una sola, usada tres veces: variables indicadoras y linealidad de la
esperanza, que no pide independencia.

- Quicksort aleatorio: $\mathbb{E}[C] = 2(n+1)H_n - 4n \le 2n \ln n$, exacto.
- Quickselect: $\mathbb{E}[C] \le 8n$ por fases, contra $3{,}29n$ medidos en la mediana.
- Hashing universal: largo esperado de una lista $\le 1 + n/m$ para todo conjunto de
  claves, con la familia $((ax + b) \bmod p) \bmod m$.

El hilo es **quién elige el azar**. Si lo elige el algoritmo y el adversario no lo ve,
la garantía vale para toda entrada. Si viene de la entrada (caso promedio), un
adversario la rompe. Y el amortizado del capítulo 4 no tiene azar.

El error plantado: quicksort aleatorio con partición en dos (iguales a la derecha). La
demostración asume claves distintas, y esa es la hipótesis que el error rompe: con
todas las claves iguales hace $n(n-1)/2$ comparaciones, y las pruebas con permutaciones
al azar no lo ven.

## Estructura

### 1. El azar dentro del algoritmo
- Ejemplo de entrada: la rejilla del capítulo 2, §9, siempre correcta, con
  reconstrucciones aleatorias. Eso es Las Vegas. Monte Carlo (capítulo 15) es lo otro:
  tiempo fijo, respuesta que puede fallar.
- Qué es el costo esperado: $\max_x \mathbb{E}_r[T(x, r)]$. El orden importa: primero
  la entrada, después la esperanza.
- Repaso: indicadoras, $\mathbb{E}[X_A] = \Pr[A]$, linealidad sin independencia.

### 2. Quicksort con pivote fijo
- Código que cuenta comparaciones (una por elemento y partición, $m - 1$ por
  partición de $m$). Partición en tres: menores, iguales, mayores.
- Primer intento, el primer elemento como pivote: con la entrada ordenada,
  $n(n-1)/2$. Con una permutación al azar, bien. El adversario conoce la regla.

### 3. Quicksort aleatorio: el experimento
- Mismo código, pivote `random.choice`. Oráculo `sorted`.
- 10 000 corridas con la misma entrada, $n = 200$: histograma, media contra
  $2n \ln n$ (figura). La media queda por debajo de $2n\ln n$: el experimento propone
  la fórmula exacta que demuestran las secciones 4 y 5.

### 4. Cuándo se comparan dos elementos
- Lema: $z_i$ y $z_j$ se comparan si y solo si el primer pivote elegido entre
  $z_i, \dots, z_j$ es uno de los dos. Probabilidad $2/(j - i + 1)$.
- Figura con una corrida real de $n = 12$: el orden en que cada rango fue pivote, y
  dos pares, uno comparado y otro no.
- Demostración completa, con el paso que se salta: mientras ningún elemento del
  intervalo es pivote, el intervalo entero viaja junto en el mismo subarreglo.

### 5. La suma
- $\mathbb{E}[C] = \sum_{i<j} 2/(j-i+1) = 2(n+1)H_n - 4n$, cuenta escrita.
- $H_n \le 1 + \ln n$ por la integral, y de ahí $\mathbb{E}[C] \le 2n\ln n$ para todo
  $n \ge 1$ (usa $\ln n \le n - 1$). Comprobación numérica que se rompe a propósito:
  con $1/(j-i+1)$ la cuenta no coincide con lo medido.
- Por qué $2n\ln n \approx 1{,}39\, n\log_2 n$: cerca de la cota del capítulo 5.

### 6. El error plantado: claves repetidas
- Partición en dos, iguales a la derecha. Pasa 500 pruebas con permutaciones al azar.
- Todas iguales, $n = 2\,000$: $1\,999\,000 = n(n-1)/2$ comparaciones. Enteros en
  $[0, 10)$: mucho más que en la versión de tres partes.
- Qué parte de la demostración lo anunciaba: la sección 4 ordenó $z_1 < \dots < z_n$.

### 7. Esperado, promedio y amortizado
- Tabla de tres garantías: quién elige el azar, para qué entradas vale.
- Desigualdad de Markov con demostración de dos líneas. Del histograma: la fracción
  medida de corridas por encima de $1{,}2$ veces la media, contra el $1/1{,}2$ de Markov.

### 8. Quickselect
- El mismo pivote al azar, pero se sigue en un solo lado. Hoare (1961), "Algorithm 65:
  Find". Oráculo `sorted`.
- Experimento: comparaciones medias divididas por $n$, según el rango $k$.

### 9. Quickselect cuesta $O(n)$ esperado
- Fases: la fase $j$ dura mientras el tamaño está en $((3/4)^{j+1} n, (3/4)^j n]$.
  Un pivote central (deja los dos lados $\le 3m/4$) aparece con probabilidad
  $\ge 1/2$: se demuestra contando. Esperanza de llamadas por fase $\le 2$. Total
  $\le 8n$.
- La cota es floja: lo medido es $3{,}29n$ en la mediana. El ejercicio 3 la
  baja a $4n$. Una cota superior no es el valor.
- Contra la mediana de medianas del capítulo 6: peor caso garantizado contra código
  corto y esperanza.

### 10. Hashing: toda función fija tiene una mala entrada
- Encadenamiento, $m$ cubetas. Palomar: si el universo tiene más de $(n-1)m$ claves,
  hay $n$ que caen en la misma cubeta.
- Definición de familia universal (Carter y Wegman, 1979). Teorema: largo esperado de
  la lista de $x$ $\le 1 + (n-1)/m$ si $x$ está, $\le n/m$ si no. Demostración por
  indicadoras.

### 11. Una familia universal
- Intento que falla: $(ax + b) \bmod m$. Las claves $x \equiv y \pmod m$ chocan siempre.
- La familia con el primo, y la demostración: $(a, b) \mapsto (r, s)$ es biyección.
- Figura: probabilidad de colisión de cada par para las dos familias.
- Medición: las claves $0, m, 2m, \dots$ con las dos familias, lista más larga.

### 12. Cierre
- El capítulo 2 tenía dos monedas: la permutación y la tabla hash.
- La regla: la garantía esperada vale para toda entrada mientras el azar lo ponga el
  algoritmo y el adversario no lo vea.
- Hacia adelante: capítulo 15 (Monte Carlo, amplificación), capítulo 21 (MAX-3SAT por
  linealidad).

### Resumen y 10 ejercicios

1. [traza] $n = 3$, exacto.
2. [demostración] Comparaciones esperadas en que participa el elemento de rango $k$.
3. [demostración ★] Quickselect $\le 4n$.
4. [demostración] Con $a = 0$ permitido: no universal; cota $1/m + 1/p$.
5. [entrada que rompe] Sin $b$: enumerar con $p, m$ chicos.
6. [entrada que rompe] Pivote del medio: entrada con $n(n-1)/2$.
7. [demostración] Markov: de esperado a $2T$ con probabilidad $\ge 1/2$, y $2kT$ con
   $1 - 2^{-k}$.
8. [modelar] Coleccionista de cupones.
9. [implementar y medir] Carga máxima con $n$ claves en $n$ cubetas.
10. [cambio de hipótesis] El adversario ve los bits.

## Decisiones

- **Semillas cambiadas.** La 2 del brief pedía demostrar el lema de $2/(j-i+1)$, que
  el texto demuestra (§4): pasa a pedir la participación del elemento de rango $k$. La
  4 pedía demostrar que la familia es universal, que el texto demuestra (§11): pasa a
  la variante con $a = 0$. La 6 pedía la entrada mala del primer pivote, que el texto
  muestra (§2): pasa al pivote del medio, verificado por fuerza bruta para $n \le 8$.
  La 7 decía "$kT$ con $1 - 2^{-k}$": con $k$ rondas de $2T$ es $2kT$.
- **$2n\ln n$ es cota, no valor.** Para $n = 200$ la media exacta es $1\,563$ y
  $2n\ln n$ es $2\,119$. Las notas dan la fórmula exacta y la cota.
- **Sin atribución del nombre "Las Vegas"** (se suele atribuir a Babai, 1979; no se
  pudo verificar en la fuente primaria).
- **La familia con el primo no se atribuye a Carter y Wegman** en su forma exacta:
  no se pudo leer el artículo. Se les atribuye la noción de familia universal, que
  está en el título.
- **El máximo de quickselect** se da medido y calculado exacto por recurrencia
  ($3{,}25n$ con $n = 300$), sin citar el límite $2 + 2\ln 2$.
