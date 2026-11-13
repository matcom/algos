# Outline: Capítulo 15, Monte Carlo

Estado: redactado (2026-11-13) dentro del workflow del libro; pendiente de revisión.
Destino: `Lectures/2026/15-monte-carlo/notas.md`, en formato de libro.
Extensión objetivo: 5 500–7 000 palabras con el código.
Verificaciones: `.playground/libro-daa/verif/15/` (`v1.py` a `v4.py`).

## Idea del capítulo

El capítulo 8 fijó la respuesta y dejó aleatorio el tiempo. Este capítulo hace lo
contrario: el tiempo es fijo y la respuesta puede estar mal, con una probabilidad que
se acota **para toda entrada**. Dos algoritmos lo llevan:

- **Freivalds** verifica $AB = C$ en $O(n^2)$ operaciones por ronda, con error a lo
  sumo $1/2$ cuando $AB \ne C$ y ningún error cuando $AB = C$.
- **Karger** halla un corte mínimo global contrayendo aristas al azar. Una corrida
  acierta con probabilidad al menos $2/(n(n-1))$, que es poca, y la repetición la lleva
  a $1 - \delta$.

La herramienta común es la **amplificación**: con error de un solo lado, $k$ rondas
independientes llevan el error a $p^k$. La palabra que importa es *independientes*, y
el error plantado es justo quitarla.

El cierre: la probabilidad de error es parte de la garantía, como el $O(\cdot)$. Una
garantía Monte Carlo dice "para toda entrada, error $\le \delta$", y la $\delta$ la
elige quien usa el algoritmo, pagando $\log(1/\delta)$ repeticiones.

## Estructura

### 1. Fijar el tiempo, soltar la respuesta
- Las Vegas (capítulo 8) contra Monte Carlo. Definición con los cuantificadores en el
  mismo orden que en el capítulo 8, §1: $\max_x \Pr_r[\text{respuesta mal}] \le \delta$.
- Error de un lado y de dos lados, con nombre.
- Puente: el ejercicio 7 del capítulo 8 convierte Las Vegas en Monte Carlo con Markov.
  Al revés solo se puede si la respuesta se puede comprobar barato.

### 2. Verificar un producto de matrices: el intento que falla
- El problema y su costo: recalcular $AB$ cuesta $n^3$ multiplicaciones escalares
  con el algoritmo escolar. El capítulo 6 no trató Strassen para matrices: solo se dice
  que hay algoritmos con exponente menor que 3 y ninguno conocido con $O(n^2)$.
- Grafo no dirigido a red del capítulo 13: cada arista, dos arcos de capacidad 1.
  Max-Flow Min-Cut en el capítulo 13, §6; la cota de Dinic, §11.
- Modelo de costo (error 7 de la guía): contamos operaciones aritméticas sobre enteros
  de tamaño acotado.
- Intento: mirar $s$ entradas al azar de $C$. Si $C$ difiere en una sola entrada,
  la atrapa con probabilidad $1 - (1 - 1/n^2)^s$; con $n = 20$ y $s = n$, 4,9 %
  (`v3.py`). El error está donde no miramos.

### 3. Freivalds: el algoritmo y el experimento
- $r \in \{0,1\}^n$ al azar; comparar $A(Br)$ con $Cr$. Tres productos matriz-vector.
- Código, probado: con $C = AB$ responde siempre "sí"; con un error en una entrada,
  la fracción que pasa una ronda sale ≈ 0,50 (medido 0,5018 con 4 000 pruebas, `v3.py`).

### 4. Error a lo sumo 1/2
- Demostración por decisiones diferidas: $D = AB - C \ne 0$, $d_{ij} \ne 0$; fijadas
  todas las monedas menos $r_j$, a lo sumo un valor de $r_j$ anula $(Dr)_i$.
- El paso que se salta: la independencia de $r_j$ respecto de las demás monedas.
- Es exacta: $D$ con una sola entrada no nula da exactamente $1/2$. Enumerado: para
  $n = 2, 3$ y entradas en $\{-1, 0, 1\}$, el peor $\Pr[Dr = 0]$ es $1/2$ (`v1.py`).

### 5. Amplificar
- $k$ rondas independientes: error $\le 2^{-k}$. Demostración: producto de
  probabilidades de eventos independientes.
- **Figura** `mc-freivalds`: fracción de matrices con un error que pasan $k$ rondas,
  $k = 1..10$, contra $2^{-k}$, con la versión plantada al lado.

### 6. El error plantado: la misma moneda $k$ veces
- Variante que sortea $r$ una vez y lo comprueba $k$ veces.
- Medido: con un error en una entrada, pasa 10 rondas casi la mitad de las veces (0,49).
- Una batería con $C$ perturbada en muchas entradas no la ve: 0 de 4 000 pasan.
- La demostración de §5 decía "independientes"; esa palabra anunciaba el error.

### 7. Un lado y dos lados
- Freivalds: "no" siempre es verdad (testigo $r$ con $Dr \ne 0$); "sí" puede ser
  mentira. Regla de amplificación: "no" si alguna ronda dice "no".
- Con dos lados esa regla falla; la mayoría funciona y su análisis es el ejercicio 10.
- No damos clases de complejidad (RP, BPP): fuera del plan.

### 8. El corte mínimo global
- Multigrafo, corte, $\lambda(G)$. Contraste con el capítulo 13: el corte $s$-$t$ sale
  de Max-Flow Min-Cut; el global es el mínimo sobre $t$ con $s$ fijo, $n - 1$ flujos.
- Referencia: Ford-Fulkerson (capítulo 13, §4) desde un vértice de grado mínimo
  $\delta$, $\le \delta$ aumentos de $O(m)$ por flujo, $O(n\delta m) = O(m^2)$ en total.
  La cota general de Dinic, $O(n^3 m)$, es holgada aquí (revisión r1, B1).

### 9. Contraer una arista al azar
- El algoritmo de contracción. Cómo se le ocurre a uno: un corte mínimo tiene pocas
  aristas, así que una arista al azar casi nunca es de él.
- Implementación: barajar las aristas y recorrerlas como Kruskal (capítulo 10, §7) con
  union-find por rango y compresión (capítulo 4, §8), hasta dos componentes.
  Demostración corta de que la primera arista que no es lazo es uniforme entre las que
  no son lazos.
- Oráculo: fuerza bruta sobre los $2^{n-1} - 1$ cortes.
- **Figura** `mc-contraccion`: una corrida real sobre un grafo de 8 vértices (dos $K_4$
  y dos puentes, $\lambda = 2$, $m = 14$), los siete estados.

### 10. La cota $2/(n(n-1))$
- Teorema y demostración: grado mínimo $\ge k$ en todo multigrafo contraído, así que
  $\ge ki/2$ aristas con $i$ vértices; $\Pr[\text{tocar } C] \le 2/i$; producto
  telescópico $\prod_{i=3}^{n} (i-2)/i = 2/(n(n-1))$ (comprobado exacto hasta 11, `v1.py`).
- El paso que se salta: que un corte del grafo contraído es un corte del original, y
  por eso $\lambda$ no baja.
- **Figura** `mc-karger-exito`: probabilidad medida contra $n$, en escala log, para tres
  familias: ciclo (corte fijado: cae justo sobre la cota, exacto por enumeración para
  $n = 4, 5, 6$), ciclo con aristas dobles salvo dos (único corte mínimo) y dos
  cliques con un puente. Medido: razón éxito/cota entre 2 y 75 (`v2.py`).

### 11. Repetir hasta alta probabilidad
- $N$ corridas, quedarse con el menor: error de un lado en el valor. $(1-p)^N \le e^{-pN}$;
  $N = \lceil \binom n2 \ln(1/\delta) \rceil$ da error $\le \delta$. Para $n = 8$,
  $\delta = 0{,}01$: 129 corridas (`v4.py`).
- Costo total $O(n^2 m \log^* n \log(1/\delta))$: en grafos simples pierde contra los
  $O(m^2)$ de los flujos. La contracción entra por la técnica, no por rápida.
- Karger-Stein, $O(n^2 \log^3 n)$ (resumen del artículo), sí gana en grafos densos.
  Estado del arte, citas por Crossref: Karger 2000 (JACM 47(1), $O(m\log^3 n)$), Stoer y
  Wagner 1997 (JACM 44(4)), Kawarabayashi y Thorup (STOC 2015), Henzinger, Li, Rao y
  Wang (SODA 2024).
- Medido sobre el grafo de 8 vértices: éxito de una corrida 0,215 contra la cota 0,036.

### 12. Cierre
- Regla: la probabilidad de error es parte de la garantía, se acota para toda entrada,
  y se amplifica solo con monedas nuevas.
- Hacia adelante: el capítulo 16 define NP por certificados que se verifican; Freivalds
  verifica un certificado sin recalcularlo. El capítulo 21 vuelve al azar.

## Ejercicios

1. [demostración] Freivalds con $r \in \{0, \dots, q-1\}^n$: error $\le 1/q$, y una $D$
   que lo alcanza. (Cambia la semilla: la cota 1/2 se demuestra en el cuerpo.)
2. [traza] Rondas para error $< 10^{-9}$ con $q = 2$, y bits aleatorios gastados con
   $q = 2$ y $q = 2^{16}$.
3. [demostración] A lo sumo $n(n-1)/2$ cortes mínimos, y un grafo que lo alcanza.
4. [traza] Karger sobre el ciclo: probabilidad de éxito y de devolver un corte fijado.
5. [demostración] ★ Karger-Stein: recurrencias de tiempo y de probabilidad.
6. [entrada que rompe] Fermat y 561. (Corrige la semilla: 561 no engaña "siempre",
   sino con todo $a$ coprimo; con $a$ al azar en $1..560$ lo declara primo con
   probabilidad $320/560 \approx 0{,}57$, `v1.py`.)
7. [modelar] Igualdad de productos de formas lineales, con Schwartz-Zippel enunciado.
8. [modelar] Huellas módulo un primo al azar; la densidad de primos se comprueba con
   la criba en lugar de citarse.
9. [implementar y medir] Miller-Rabin contra la criba hasta $10^6$.
10. [cambio de hipótesis] Error de dos lados: por qué falla la regla de §7 y la mayoría.

## Audios

| Audio | Secciones | Minutos |
|---|---|---|
| 1 | 1 | 4 |
| 2 | 2 y 3 | 5 |
| 3 | 4 | 5 |
| 4 | 5 y 6 | 6 |
| 5 | 7 y 8 | 5 |
| 6 | 9 | 5 |
| 7 | 10 | 6 |
| 8 | 11 y 12 | 5 |

## Decisiones y lo que no entra

- Citas comprobadas: Karger (SODA 1993, en el PDF del artículo), Karger y Stein
  (JACM 43(4):601–640, 1996, Crossref), Schwartz (JACM 27(4):701–717, 1980) y Zippel
  (EUROSAM 1979, LNCS 72, Crossref). Freivalds (IFIP Congress 1977, pp. 839–842) no tiene
  copia en línea: solo bibliografías concordantes. Entra con autor, título y año.
- No entra Rosser-Schoenfeld ($\pi(x) > x/\ln x$): no se pudo leer la fuente. El
  ejercicio 8 hace contar los primos con la criba.
- No entra Stoer-Wagner ni ninguna afirmación de que Karger-Stein sea el mejor conocido.
- Tiempos de reloj: el capítulo cuenta operaciones, no segundos, porque las cuentas no
  dependen de la máquina.
