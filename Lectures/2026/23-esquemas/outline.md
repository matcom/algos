# Outline: Capítulo 23, esquemas de aproximación

Estado: redactado (2026-11-13) dentro del flujo del libro. El documento está en `notas.md`.
Destino: `Lectures/2026/23-esquemas/notas.md`, formato de libro.
Extensión objetivo: 5 500–7 000 palabras con el código.
Verificación: `.playground/libro-daa/verif/23/` (`fptas.py`, `error.py`, `tiempo.py`,
`ptas.py`, `cota2.py`, `ej1.py`, `tres.py`; las fuentes en `fuentes/`).

## Idea del capítulo

El capítulo 21 dio razones fijas: 2, $4/3$, $H_n$. Este capítulo pide una familia de
algoritmos, uno por cada $\varepsilon > 0$, que llega a $1 \pm \varepsilon$ y paga en
tiempo. La pregunta que ordena todo es **dónde se paga** $\varepsilon$: en el exponente de
$n$ (PTAS) o como un factor polinomial en $1/\varepsilon$ (FPTAS). La respuesta la
deciden los números de la entrada. La mochila es difícil solo cuando sus números son
enormes, y redondearlos la vuelve fácil con una pérdida acotada. 3-partición es difícil
con números chicos, y para un problema así un FPTAS resolvería exacto en tiempo
pseudopolinomial, lo que da P = NP.

El error plantado es un FPTAS de mochila que no descarta los objetos que no caben. La
demostración de la razón usa $\mathrm{OPT} \ge v_{\max}$, que solo vale si el objeto
más valioso cabe. Falla en 14 de 1 000 instancias al azar de la batería del capítulo 20
y en ninguna de 1 000 donde todos los objetos caben; en una entrada construida devuelve 0 contra
un óptimo de 400.

## Estructura

### 1. Una familia de algoritmos
- Definiciones: esquema de aproximación (PTAS) para minimizar ($\le (1+\varepsilon)
  \mathrm{OPT}$) y maximizar ($\ge (1-\varepsilon)\mathrm{OPT}$), tiempo polinomial en
  $|I|$ para cada $\varepsilon$ fijo. FPTAS: polinomial en $|I|$ y en $1/\varepsilon$.
- Ejemplos de tiempos: $O(n^{1/\varepsilon})$ es PTAS y no FPTAS; $O(n^3/\varepsilon)$
  es FPTAS. Por qué la distinción importa: con $\varepsilon = 0{,}01$.
- Conexión: capítulo 21 (razón fija), capítulo 1, §8 (pseudopolinomial), capítulo 16, §3.

### 2. La tabla por valores
- La DP del capítulo 20 (`mochila_dp`) indexa por capacidad: $O(nW)$. La otra: para cada
  valor $x$, el menor peso con que se consigue exactamente $x$. $O(n V)$ con
  $V = \sum v_i \le n v_{\max}$. Pseudopolinomial en los valores.
- Código con reconstrucción por tabla de bits, contra fuerza bruta (medido: 800
  instancias de hasta 8 objetos, valor y conjunto iguales).
- Cómo se le ocurre a uno: si los valores fueran chicos, esta tabla sería barata.
  Entonces hagámoslos chicos.

### 3. Redondear los valores
- $\mu = \varepsilon v_{\max}/n$, $v'_i = \lfloor v_i/\mu \rfloor$. Resolver exacto con
  $v'$ y devolver ese conjunto.
- Aritmética entera para no perder el piso por coma flotante.
- **Figura** `esq-redondeo`: valores antes y después en una instancia de 8 objetos, la
  pérdida de cada uno menor que $\mu$. Semilla 21: FPTAS 235, óptimo 241, $\mu = 21/4$.
- El intento que falla primero: dividir por una constante fija; la pérdida no queda
  acotada en términos del óptimo.

### 4. La razón 1 − ε
- Teorema (Ibarra y Kim, 1975, la idea): valor $\ge (1-\varepsilon)\mathrm{OPT}$.
- Demostración: $\mu v'_i > v_i - \mu$; el conjunto devuelto es óptimo para $v'$; la
  pérdida es menor que $|S^*|\mu \le n\mu = \varepsilon v_{\max} \le \varepsilon
  \mathrm{OPT}$. El paso que se salta: $v_{\max} \le \mathrm{OPT}$ porque el objeto más
  valioso cabe solo, y para eso se descartan los que no caben.
- Comprobación: tres $\varepsilon$, 600 instancias cada uno; peor razón medida 0,808
  ($\varepsilon = 1/2$), 0,897 ($1/4$), 0,969 ($1/10$).

### 5. El tiempo
- Teorema: $O(n^3/\varepsilon)$. $v'_i \le \lfloor n/\varepsilon \rfloor$, la suma
  $\le n \lfloor n/\varepsilon \rfloor$, la tabla tiene $n$ filas.
- **Figura** `esq-tiempo`: tiempo medido con $n = 40$ y valores hasta $10^6$, contra
  $1/\varepsilon \in \{2, 4, 8, 16, 32\}$, log-log, pendiente cerca de 1. La DP exacta
  tendría del orden de $40 \cdot 2 \cdot 10^7$ celdas.

### 6. El error plantado: el objeto que no cabe
- Variante sin el filtro. Medido: batería del capítulo 20 ($W$ = suma/2), 14 fallos de
  1 000; batería donde todo cabe, 0 de 1 000; entrada construida (un objeto de valor
  1 000 que no cabe, diez de valor 40 y peso 1, $W = 10$): devuelve 0, óptimo 400.
- La demostración anunciaba dónde.

### 7. Números chicos, números grandes
- $\mathrm{Max}(I)$, codificación unaria. Fuertemente NP-duro: sigue NP-duro restringido
  a $\mathrm{Max}(I) \le p(|I|)$. Mochila no lo es si P ≠ NP (tiene la tabla).
- Teorema (Garey y Johnson, 1978): un problema fuertemente NP-duro no tiene algoritmo
  pseudopolinomial si P ≠ NP. Demostración de un párrafo.
- Los problemas sin números (vertex cover, 3-SAT, TSP con distancias 1 y 2) son
  fuertemente NP-duros sin más.

### 8. 3-partición y el makespan
- Definición de 3-PARTICIÓN ($3q$ números, $B/4 < a_i < B/2$, suma $qB$). Fuertemente
  NP-completo (Garey y Johnson; la demostración, larga, no se hace aquí).
- Teorema: el makespan con $m$ parte de la entrada es fuertemente NP-duro. Reducción
  con los mismos números, $m = q$, meta $B$. Cada máquina recibe exactamente tres.
- Contraste: con $m = 2$ es PARTICIÓN, que tiene tabla pseudopolinomial.

### 9. Un FPTAS resuelve exacto
- Teorema: objetivo entero y $\mathrm{OPT}(I) \le q(|I|, \mathrm{Max}(I))$; un FPTAS con
  $\varepsilon = 1/(q+1)$ da el óptimo en tiempo polinomial en $|I|$ y $\mathrm{Max}(I)$.
- Corolario: makespan con $m$ libre, vertex cover, TSP métrico no tienen FPTAS si
  P ≠ NP.
- Al revés para la mochila: el FPTAS con $\varepsilon = 1/(n v_{\max} + 1)$ es un algoritmo
  exacto en $O(n^4 v_{\max})$, peor que la tabla.

### 10. Balanceo con m fijo: un PTAS
- Algoritmo (Graham, 1969): las $k$ tareas más largas, óptimo por ramificación; las
  demás con la regla de Graham. $k = m(\lceil 1/\varepsilon \rceil - 1)$, el mínimo que pide
  el palomar (corregido en la revisión 1; antes $mq - 1$).
- Código, contra `carga_optima`. Medido: 300 entradas por $\varepsilon$, cota respetada;
  peor razón 1,123, 1,123 y 1,108 para $\varepsilon = 1, 1/2, 1/3$. Con $k = 0$ (LPT)
  y $\varepsilon = 1/5$, 1 violación: la comprobación puede fallar. Con $\varepsilon = 1/3$
  la cota coincide con la de LPT, $4/3 - 1/(3m)$.

### 11. La demostración y el costo
- Si la última tarea de la máquina más cargada es larga, $L \le \mathrm{OPT}$. Si es
  corta, $L \le T/m + (1 - 1/m)t_j$ y $\mathrm{OPT} \ge \lceil 1/\varepsilon\rceil t_j$.
  Resultado $(1 + (1-1/m)\varepsilon)$.
- Costo: $m^k$ asignaciones, tabla con $m = 2, 3, 5$ y $\varepsilon = 1/2, 1/4, 1/10$
  (para $m = 3$, $\varepsilon = 1/10$: $3^{27} \approx 7{,}6 \cdot 10^{12}$). PTAS, no FPTAS.
- Lo que se sabe más: Hochbaum y Shmoys (1987), PTAS con $m$ libre en
  $O((n/\varepsilon)^{1/\varepsilon^2})$; con $m$ fijo hay FPTAS por redondeo de la tabla
  de cargas (ejercicio 6; Sahni, 1976, aplica esa técnica). Con $m$ libre no hay FPTAS
  (§9).

### 12. El mapa de la Parte III y la regla
- **Figura** `esq-mapa`: por problema, la mejor garantía demostrada en el libro y lo que
  queda excluido si P ≠ NP: exacto, FPTAS, PTAS, razón constante, razón que crece,
  ninguna. Tras la revisión 1 no quedan huecos de clase: vertex cover (Dinur y Safra,
  2005, 1,3606), TSP métrico (123/122, cap. 22, §9) y TSP general (teorema 1 del cap. 22
  con $\alpha(n)$ calculable). Los huecos están dentro de la razón constante.
- La regla: dónde se paga $\varepsilon$ lo deciden los números.

## Ejercicios
1. [traza] FPTAS con $\varepsilon = 1/2$ sobre 5 objetos ($p = 7,1,8,4,4$;
   $v = 46,50,54,48,9$; $W = 10$). Óptimo redondeado único; verificado.
2. [modelar e implementar] Suma de subconjuntos por recorte de listas (semilla 5).
3. [demostración] $O(n^2/\varepsilon)$ con la cota $\max(\text{prefijo goloso},
   v_{\max})$, que cumple $\mathrm{OPT} \le 2\,\mathrm{LB}$ (medido: 0 violaciones en
   3 000; sin el mejor objeto, 21).
4. [demostración] Clique y coloración: sin FPTAS; coloración sin razón $< 4/3$.
5. [demostración] Empaquetamiento en cajas fuertemente NP-duro desde 3-partición, Next
   Fit con razón 2; sitúalo en el mapa.
6. ★ [demostración] FPTAS para makespan con $m$ fijo, contando el tiempo (semilla 7).
7. [entrada que rompe] FPTAS con $\mu = \varepsilon v_{\max}$ sin dividir por $n$:
   construir entrada con razón $< 1-\varepsilon$.
8. [cambio de hipótesis] k-center: sin PTAS con $k$ libre; con $k$ fijo, exacto polinomial;
   comparar con $m$ fijo (semilla 8 corregida).
9. [implementar y medir] Calidad del FPTAS contra el exacto; búsqueda de malas entradas.
10. [modelar] Presupuesto de proyectos y camiones con tres paquetes.

## Decisiones que quiero confirmar
- Semillas 2, 3, 4 y 10 del brief son teoremas del cuerpo (§4, §5, §9), así que los
  ejercicios piden variantes. La semilla 6 repetía el ejercicio 4 del capítulo 21: pasa a
  fuerza NP + Next Fit. La semilla 8 decía "no hay FPTAS" para k-center: tampoco hay PTAS,
  y con $k$ fijo hay algoritmo exacto; el ejercicio pide las tres cosas.
- No se verificó en la fuente primaria el tiempo exacto del FPTAS de Sahni (1976) para
  $m$ fijo, ni la página de la demostración de 3-partición en Garey y Johnson (1979):
  las notas no dan esos números.
- Se descartó un experimento sobre los estados de la tabla de cargas en 3-partición
  (`tres.py`): los conteos (6, 39, 121, 2 305, 4 491 para $q = 2..6$) son ruidosos y no
  mostraban nada que la demostración no diga mejor.
