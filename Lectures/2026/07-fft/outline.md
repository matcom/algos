# Outline: Capítulo 7, divide y vencerás: la transformada rápida de Fourier

Estado: redactado para el libro (2026-11-13), pendiente de revisión. El documento está en
`notas.md`.
Destino: `Lectures/2026/07-fft/notas.md`, capítulo del libro.
Extensión objetivo: 5 500–7 000 palabras con el código.
Verificación: los scripts `v1.py` a `v4.py` en `.playground/libro-daa/verif/07/`, y las
citas en `citas.txt` del mismo directorio.

## Idea del capítulo

El capítulo 6 bajó el costo de multiplicar de $n^2$ a $n^{\log_2 3}$ partiendo los
números en dos mitades. Este capítulo baja el de multiplicar **polinomios** a
$O(n \log n)$ con otra manera de partir. No parte el polinomio por la mitad de sus
coeficientes, sino en los coeficientes pares y los impares. Y no calcula el producto en
la representación de coeficientes: cambia a la representación por valores, donde
multiplicar cuesta $O(n)$, y paga el cambio de ida y de vuelta con divide y vencerás.

El modelo de costo se fija al principio y se repite al final: el $O(n \log n)$ cuenta
**operaciones sobre coeficientes**, cada una de costo 1, con aritmética exacta. Ni los
complejos en punto flotante ni los enteros del capítulo 1 cumplen eso gratis. El
capítulo mide dónde se rompe el punto flotante y arregla la aritmética con la variante
modular (NTT). Para enteros en el modelo por bit no se afirma $O(n \log n)$ con este
algoritmo: se citan Schönhage y Strassen (1971) y Harvey y van der Hoeven (2021), sin
demostración.

El error plantado es de tamaño: rellenar con ceros hasta la potencia de dos
$\ge \deg A + \deg B$ en vez de $> \deg A + \deg B$. El teorema de la §2 (un polinomio de
grado $d$ necesita $d + 1$ valores) lo anuncia.

## Estructura

### 1. Multiplicar polinomios

- El problema: $A$ y $B$ de grados $n-1$; $C = AB$, con $c_k = \sum_{i+j=k} a_i b_j$
  (la convolución). La ingenua, $n^2$ multiplicaciones de coeficientes.
- Modelo: cada operación sobre coeficientes cuesta 1 (modelo aritmético). Es el que
  vale para la §1 a la §8; la §10 lo pone en duda.
- Conexión hacia atrás: un entero en base 10 es un polinomio evaluado en 10, más los
  acarreos. El Karatsuba del capítulo 6 multiplica polinomios con la misma cuenta,
  $\Theta(n^{\log_2 3})$. El ejercicio 10 del capítulo 6 (Toom-3) ya proponía evaluar
  e interpolar.
- Código: `ingenua(a, b)`, que es el oráculo de todo el capítulo.

### 2. Coeficientes y valores

- Teorema: un polinomio de grado a lo sumo $d$ queda determinado por sus valores en
  $d+1$ puntos distintos. Demostración: la diferencia de dos candidatos tiene grado
  $\le d$ y $d+1$ raíces, así que es cero (un polinomio no nulo de grado $\le d$ tiene a
  lo sumo $d$ raíces, de Álgebra). Existencia por Lagrange.
- En valores, multiplicar cuesta $n$ multiplicaciones, **si** se tienen
  $\deg C + 1 = 2n-1$ puntos (ojo: no $n$). Primer anuncio del error plantado.
- El plan: evaluar, multiplicar punto a punto, interpolar. Evaluar con Horner en $2n$
  puntos cuesta $\Theta(n^2)$: la evaluación es el cuello de botella.

### 3. Cómo se le ocurre a uno: pares e impares

- $A(x) = A_{\text{par}}(x^2) + x \, A_{\text{impar}}(x^2)$, cada uno de grado $< n/2$.
- En $x$ y en $-x$ se reusan los mismos dos valores. Con puntos en parejas $\pm x$,
  evaluar en $n$ puntos se reduce a evaluar dos polinomios de la mitad en $n/2$ puntos.
- El intento con reales falla en el segundo nivel: $\{1,-1,2,-2\}$ al cuadrado da
  $\{1,4\}$, que no son parejas. Verificado en `v3.py`. Hace falta un conjunto que al
  elevarlo al cuadrado siga teniendo parejas: las raíces complejas de la unidad.

### 4. Las raíces de la unidad y el lema de la mitad

- $\omega_n = e^{2\pi i/n}$, las $n$ raíces $\omega_n^k$.
- Lema de la mitad, con demostración: para $n$ par, los cuadrados de las $n$ raíces
  $n$-ésimas son las $n/2$ raíces $n/2$-ésimas, cada una dos veces. Y
  $\omega_n^{k + n/2} = -\omega_n^k$: las parejas $\pm$ que pedía la §3.
- **Figura 1** (`fft-raices`): las 8 raíces en el círculo y sus cuadrados, que caen en
  las 4 raíces cuartas. Recibe los valores calculados por el código.

### 5. La FFT

- Definición de la DFT: $y_k = A(\omega_n^k)$.
- Código: `fft(a)` recursiva, de unas diez líneas. Probada contra `dft(a)` directa, que
  evalúa la definición.
- Traza a mano de $(1, 1, 0, 0)$: pares $(1,0)$, impares $(1,0)$, cada uno da $(1,1)$;
  combinar da $(2, 1+i, 0, 1-i)$.
- Costo: $T(n) = 2T(n/2) + \Theta(n) = \Theta(n \log n)$, por el Teorema Maestro del
  capítulo 6. La FFT es mergesort con otra combinación.

### 6. La inversa

- La DFT es la matriz de Vandermonde $V_{kj} = \omega_n^{kj}$.
- Lema de la suma: $\sum_{j=0}^{n-1} \omega_n^{jk} = 0$ si $n \nmid k$, $= n$ si
  $n \mid k$. Demostración por serie geométrica: el cociente $\omega_n^k \ne 1$.
- Teorema: $(V^{-1})_{jk} = \omega_n^{-jk}/n$. Demostración: el producto da el lema de
  la suma.
- Interpolar es la misma FFT con $\omega^{-1}$, dividida entre $n$.
- Código: `multiplicar(a, b)`, contra `ingenua` en 300 pares al azar.
- Atribución: Cooley y Tukey (1965); Gauss lo describió hacia 1805 en un manuscrito que
  no publicó en vida (Heideman, Johnson y Burrus, 1984).

### 7. El experimento: cuándo gana

- Tiempos de `ingenua` contra `multiplicar` para $n = 64$ a $2048$. Medido en `v3.py`:
  el cruce queda entre 128 y 256 en Python puro. El número exacto lo da el documento.

### 8. El error plantado

- `multiplicar_mal`: $N$ es la potencia de dos más chica con $N \ge \deg A + \deg B$.
- Teorema: falla exactamente cuando $d = \deg A + \deg B$ es una potencia de dos
  ($d \ge 1$). Demostración: si $d$ es potencia de dos, $N = d$ y faltan valores (el
  coeficiente $c_d$ se suma a $c_0$, porque $\omega^d = 1$); si no, $N > d$, es decir,
  $N \ge d+1$. Verificado contra la ejecución en todos los largos $\le 19$ (`v1.py`).
- Baterías: largos iguales potencia de dos $\ge 4$, nunca falla; largos al azar en
  $[1,10]$, 22,00 %; en $[1,100]$, 2,05 %; en $[1,1000]$, 0,20 % (fracciones exactas
  contadas con la caracterización).
- Moraleja: la batería que parece natural para una FFT (potencias de dos) es justo la
  que no lo ve. El teorema de la §2 lo dice sin probar nada.

### 9. La FFT iterativa

- Desenrollar la recursión: las hojas quedan en el orden de inversión de bits.
- Código: `invertir_bits` y `fft_iter`, por etapas de mariposas.
- **Figura 2** (`fft-mariposa`): el diagrama de mariposa de 8 puntos. Recibe la lista de
  mariposas (posiciones y exponente de $\omega$) que registró `fft_iter` al correr.
- La correctitud: la etapa $s$ deja en cada bloque de $2^s$ la DFT de la hoja
  correspondiente de la recursión. El invariante se demuestra en el ejercicio 9.
- Tiempo contra la recursiva.

### 10. Los números de punto flotante

- El modelo de la §1 suponía aritmética exacta. Un `float` tiene 53 bits.
- Experimento: base $10^k$, $k = 3..6$, $N = 2^4..2^{14}$, error máximo contra el
  producto exacto (sustitución de Kronecker con enteros de Python).
- **Figura 3** (`fft-error`): error contra $N$, una curva por $k$, la línea de $1/2$
  donde el redondeo da un entero equivocado. Medido en `v2.py`: $k=6$ se rompe en
  $N=2^{14}$ con 2 629 coeficientes equivocados.
- Lectura: el error crece con el coeficiente más grande, $\approx N B^2 / 2$, que se
  acerca a $2^{53}$. Ninguna afirmación de cota teórica del error: solo lo medido.

### 11. La NTT: raíces de la unidad módulo un primo

- Qué usaron las demostraciones: $\omega^n = 1$, $\omega^{n/2} = -1$ y el lema de la
  suma, que divide entre $\omega^k - 1$. Todo vale en $\mathbb{Z}_p$ si $\omega$ tiene
  orden exactamente $n$ y $p$ es primo. Demostración de $\omega^{n/2} = -1$: $x^2 = 1$
  tiene solo las raíces $\pm 1$ en un cuerpo.
- Existe un elemento de orden $n$ si $n \mid p - 1$ (raíz primitiva $g$,
  $\omega = g^{(p-1)/n}$).
- Ejemplo chico: $p = 17$, $g = 3$, $\omega_8 = 9$, $\omega_4 = 13$. NTT de
  $(1,2,3,4)$ en $\mathbb{Z}_{17}$ con $\omega = 13$: $(10, 6, 15, 7)$.
- Código: `raiz_primitiva`, `ntt`, `multiplicar_ntt` con $p = 998244353 = 119 \cdot
  2^{23} + 1$. Exacta si los coeficientes del producto son $< p$.
- Pollard (1971), "The fast Fourier transform in a finite field".

### 12. Aplicaciones: enteros grandes y sumas de pares

- Enteros grandes: dígitos en base $B$, producto con NTT, acarreo. Contra `*` de Python.
- El modelo otra vez: la versión del capítulo tiene un tamaño máximo (coeficientes
  $< p$, $N \le 2^{23}$). Para enteros de $b$ bits sin tope hay que hacer crecer la
  precisión. Schönhage y Strassen (1971): $O(b \log b \log \log b)$. Harvey y van der
  Hoeven (2021): $O(b \log b)$. Se citan, no se demuestran.
- Sumas de pares: $A, B \subseteq \{0, \dots, n\}$; el polinomio $\sum_{a \in A} x^a$;
  el coeficiente $c$ del producto cuenta las parejas con $a + b = c$. Ejemplo:
  $A = \{1,3,4\}$, $B = \{0,2,5\}$.

### 13. La regla

- Cambiar de representación cuando la operación es barata en la otra, y pagar el cambio
  con divide y vencerás. El costo se cuenta en un modelo, y el modelo hay que
  revisarlo con la máquina (punto flotante, enteros por bit).
- Hacia adelante: el capítulo 15 verifica productos de matrices con Freivalds; el
  capítulo 24 presenta 3SUM.

### 14. Resumen y ejercicios

1. [traza] La DFT de $(1, 2, 3, 4)$ a mano.
2. [demostración] La `fft` del capítulo hace exactamente $(n/2)\log_2 n$
   multiplicaciones por potencias de $\omega$.
3. [demostración] Aplicar la DFT dos veces da $n \cdot (a_0, a_{n-1}, \dots, a_1)$. ¿Qué
   devuelve una inversa que use $\omega$ en vez de $\omega^{-1}$?
4. [traza] 998244353 admite NTT de tamaño $2^{23}$; una raíz de orden 8.
5. [implementar y medir] Enteros de un millón de dígitos en base $10^k$ con FFT de punto
   flotante; para qué $k$ se rompe.
6. [entrada que rompe] Entradas para las que la FFT de punto flotante da un coeficiente
   entero equivocado con $N$ más chico que en la figura 3.
7. [cambio de hipótesis] $n = 3^k$: partir por restos módulo 3, el lema que reemplaza
   al de la mitad, la recurrencia.
8. [modelar] Patrón con comodines con tres convoluciones.
9. [demostración] El invariante de la FFT iterativa.
10. ★ [modelar] El polinomio mónico con raíces dadas en $O(n \log^2 n)$.

## Audios (para el guion de grabación)

| Audio | Secciones | Minutos |
|---|---|---|
| 1 | 1 y 2 | 6 |
| 2 | 3 y 4 | 6 |
| 3 | 5 | 5 |
| 4 | 6 | 6 |
| 5 | 7 y 8 | 6 |
| 6 | 9 | 5 |
| 7 | 10 y 11 | 7 |
| 8 | 12 y 13 | 5 |

Total estimado: 46 minutos.

## Cambios a las semillas del brief

- Semilla 2 (lema de la mitad) y semilla 3 (la inversa) se demuestran en el cuerpo
  (§4 y §6), porque el capítulo no se sostiene sin ellas. Se reemplazan por el conteo
  exacto de multiplicaciones y por la DFT aplicada dos veces.
- Semilla 7 (sumas de pares) es la aplicación de la §12, que pide el plan. Se reemplaza
  por el cambio de hipótesis $n = 3^k$, que faltaba en la mezcla.
- Semilla 9 (iterativa contra recursiva) está medida en la §9. Se reemplaza por la
  demostración del invariante de la iterativa, que el texto delega.

## Revisión contra la lista de errores de la guía

- Error 1 y 7: todo costo dice su modelo. $O(n \log n)$ es en operaciones sobre
  coeficientes; para enteros en el modelo por bit se citan los dos resultados y no se
  afirma nada del algoritmo del capítulo salvo que tiene un tamaño máximo.
- Error 2: la caracterización del error plantado se comprueba contra la ejecución en
  todos los pares de largos $\le 19$, no solo contra sí misma; el oráculo de la §10 es
  la sustitución de Kronecker, verificada contra `ingenua`.
- Error 3: el lema de la mitad dice por qué la recursión sigue: los puntos del nivel de
  abajo vuelven a formar parejas $\pm$. No "porque son la mitad".
- Error 4: las tres demostraciones prometidas (§2, §4, §6) y la caracterización de la
  §8 se escriben. La del invariante de la iterativa se anuncia como ejercicio, no como
  demostración del texto.
- Error 6: el $\Theta(n)$ de combinar incluye calcular $\omega^k$; se dice.
- Error 9: siete citas, todas comprobadas en Crossref (DOI) o en la fuente: Cooley y
  Tukey (Math. Comp. 19(90), 297–301, 1965), Heideman, Johnson y Burrus (IEEE ASSP
  Magazine 1(4), 14–21, 1984), Pollard (Math. Comp. 25(114), 365–374, 1971),
  Schönhage y Strassen (Computing 7, 281–292, 1971), Harvey y van der Hoeven (Annals
  of Mathematics 193(2), 563–617, 2021), Clifford y Clifford (IPL 101(2), 53–54, 2007).
  El dato de Gauss en 1805 viene de las notas de Burrus en fftw.org, que citan el
  artículo de 1984. Los asteroides que suelen acompañar la historia no se verificaron y
  no entran.
