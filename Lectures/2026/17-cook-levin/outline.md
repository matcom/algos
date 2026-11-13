# Outline: Capítulo 17, Cook-Levin: SAT y 3-SAT

Estado: redactado por el workflow del libro (2026-11-13), pendiente de revisión.
Destino: `Lectures/2026/17-cook-levin/notas.md`, formato de libro.
Extensión objetivo: 5 500–7 000 palabras con el código.

Verificación: `.playground/libro-daa/verif/17/` (`cook.py`, `check1.py`, `check2.py`,
`check22.py`, `check3.py`). Todos los números de este outline salen de ahí.

## Idea del capítulo

El capítulo 16 dejó una receta sin su paso 2: para demostrar que $B$ es NP-completo
hace falta un $A$ que ya se sepa NP-completo. El primero no puede salir de una
reducción desde otro. Hay que reducirle **todos** los problemas de NP a la vez, y lo
único que tienen en común es la definición: una máquina de Turing no determinista que
decide en tiempo polinomial. Este capítulo escribe, para cada máquina $M$ y cada
entrada $w$, una fórmula en FNC que es satisfacible si y solo si $M$ acepta $w$. La
idea es que una computación es una tabla y que la corrección de una tabla se
comprueba mirando por una ventana de $2 \times 3$. Después, SAT $\le_p$ 3-SAT
partiendo cláusulas largas, y 3-SAT queda como punto de partida de los capítulos 18
y 19.

La máquina de Turing del capítulo 1, §3 vuelve aquí. El capítulo 1 la descartó para
medir costos porque cambia los exponentes; aquí la usamos porque es **local**: un paso
cambia a lo sumo tres celdas contiguas, y eso es lo que hace que la fórmula tenga
tamaño polinomial.

Error plantado: quitar de $\varphi_{\text{celda}}$ las cláusulas "a lo sumo un
símbolo". La fórmula sigue siendo satisfacible en todas las instancias sí, y además en
la única instancia no de cada largo. Medido: 1 respuesta equivocada de $2^n$ para
$n = 1, 2, 3, 4$. Una batería que solo prueba instancias sí no lo ve nunca; una al
azar con cadenas de largo 10 lo ve con probabilidad $1/1024$ por cadena. La frase de
la demostración que lo anunciaba: "por $\varphi_{\text{celda}}$, cada celda tiene
exactamente un símbolo, así que la asignación **es** una tabla".

## Convenciones fijadas (para que todo lo verificado valga)

- MTND: $Q$, $\Gamma \supseteq \Sigma \cup \{\_\}$, $q_0$, $q_a$, $\delta$ que a
  $(q, a)$ le da un conjunto de triples $(q', b, d)$ con $d \in \{\leftarrow,
  \rightarrow\}$. Se detiene cuando $\delta(q, a)$ es vacío; acepta si se detiene en
  $q_a$ ($q_a$ no tiene transiciones). En la celda de más a la izquierda, $\leftarrow$
  deja el cabezal donde está.
- Decide $L$ en tiempo $t(n)$: toda rama se detiene en a lo sumo $t(n)$ pasos y
  $w \in L$ si y solo si alguna rama acepta.
- Configuración como cadena: $\#\,u\,q\,v\,\#$, el cabezal sobre el primer símbolo de
  $v$. Tabla de $t+1$ filas y $t + 4$ columnas (dos bordes, el estado, $t + 1$ celdas de
  cinta: en $t$ pasos el cabezal visita a lo sumo $t+1$ celdas). Una fila detenida se
  repite.
- Ventana legal: una ventana de $2 \times 3$ que aparece, en las mismas columnas, en
  algún par (configuración, configuración siguiente) de alguna máquina de cualquier
  ancho. Es un conjunto finito que depende solo de $M$. Para el ejemplo se calcula
  enumerando configuraciones de 6 celdas; con 5, 6 y 7 celdas sale el mismo conjunto,
  182 ventanas (de $6^6 = 46\,656$ posibles).
- Ejemplo $M$: acepta las cadenas sobre $\{0, 1\}$ con algún 1, adivinando cuál.
  $\delta(q_0, 0) = \{(q_0, 0, \rightarrow)\}$,
  $\delta(q_0, 1) = \{(q_0, 1, \rightarrow), (q_a, 1, \rightarrow)\}$. $t(n) = n$.
  $C = Q \cup \Gamma \cup \{\#\}$ tiene 6 símbolos.

## Estructura

### 1. El primer problema NP-completo

- La receta del capítulo 16, §7 sin paso 2. El lema 3 transfiere, no crea.
- Hay que reducir todos los $L \in NP$ a SAT con un solo argumento. Lo común: el
  verificador, o la máquina no determinista (capítulo 16, §4).
- Cook (1971, STOC, pp. 151–158; comprobado en el escaneo del artículo): su teorema 1
  reduce todo conjunto aceptado por una MTND en tiempo polinomial a las tautologías en
  FND, construyendo una fórmula en FNC $A(w)$ satisfacible si y solo si $M$ acepta $w$.
  Levin (1973, Problemy Peredachi Informatsii 9(3), pp. 115–116; comprobado en
  mathnet): resultado del mismo tipo para problemas de búsqueda.

### 2. Máquinas de Turing no deterministas

- Definición con las convenciones de arriba. El árbol de ramas.
- Código: `sucesores`, simulación de todas las ramas. Para $w = 0110$: ramas y cuáles
  aceptan.
- **Figura**: el árbol de cómputo de $M$ sobre $0110$, calculado por el código.
- NP con verificadores = NP con máquinas. Las dos direcciones en un párrafo cada una:
  el certificado es la sucesión de elecciones; la máquina escribe el certificado
  eligiendo bit a bit y corre el verificador (que se simula en una MT con costo
  polinomial, capítulo 1, §3).

### 3. La tabla de configuraciones

- Configuración como cadena, por qué $t + 4$ columnas, filas repetidas tras detenerse.
- Código: la tabla de la rama que acepta para $0110$.
- **Figura**: la tabla con una ventana de $2 \times 3$ resaltada en el paso donde $M$
  adivina.

### 4. Ventanas de 2 × 3

- Un paso cambia a lo sumo las columnas $p-1, p, p+1$ alrededor del estado.
- Definición de ventana legal. Código: 182 ventanas legales.
- Experimento antes de la prueba: para una fila de arriba fija ($\# 0 q_0 1 0 \#$), de las
  46 656 filas de abajo posibles, las que tienen todas sus ventanas legales son
  exactamente las 2 sucesoras.
- **Lema 2** (local). Si la fila $i$ es una configuración con el estado a lo sumo en la
  columna $W - 4$ y todas las ventanas entre las filas $i$ e $i + 1$ son legales,
  entonces la fila $i+1$ es una sucesora de la fila $i$ (o su repetición si estaba
  detenida). Demostración: columnas lejos del estado, la ventana centrada en el estado,
  los bordes. El paso que se salta: la ventana centrada contiene $x$, $q$ y $a$, y eso
  es lo que hace falta para un movimiento a la izquierda.
- Por qué $2\times 2$ no basta (ejercicio 11): con movimientos a la izquierda hay filas
  de abajo no sucesoras que pasan todas las ventanas de $2\times 2$ (medido en
  `check22.py`).

### 5. Las cuatro familias de cláusulas

- Variables $x_{i,j,s}$. $\varphi_{\text{celda}}$ (al menos uno, a lo sumo uno),
  $\varphi_{\text{inicio}}$ (unitarias), $\varphi_{\text{acepta}}$ (una cláusula
  larga), $\varphi_{\text{mov}}$ (cada ventana legal).

### 6. Paso a FNC

- Las tres primeras ya están en FNC. La cuarta no: "la ventana es una de las 182".
- Distributividad: en general explota (ejercicio 3). Aquí no hace falta: cada ventana
  depende de $6|C| = 36$ variables, un número fijo.
- Forma ingenua: una cláusula por 6-tupla ilegal: 46 474 cláusulas por ventana.
  Constante no quiere decir chico.
- Forma agrupada por la fila de arriba: 446 cláusulas por ventana. Comprobado
  exhaustivamente sobre las 46 656 tuplas que las dos dicen lo mismo, y roto a
  propósito (quitar una ventana legal) para ver que la comprobación falla.

### 7. El experimento

- Código: fórmula para cada $w$ de largo 1 a 4, DPLL corto, satisfacible si y solo si
  $M$ acepta. Para $n = 4$: 240 variables, 11 353 cláusulas.
- Leer la rama de la asignación.
- Tamaños: exactos por familia, contra lo construido. **Figura**: variables y cláusulas
  contra $t$ en log-log, pendiente 2.

### 8. El teorema de Cook-Levin

- Enunciado y demostración: construcción, tamaño $O(t^2)$ cláusulas de tamaño
  constante salvo una de $O(t^2)$, $O(t^2 \log t)$ bits, tiempo polinomial; dirección
  ⇒ (la tabla de una rama que acepta satisface las cuatro familias); dirección ⇐
  (celda ⇒ tabla; inicio ⇒ fila 0; lema 2 por inducción ⇒ rama; acepta ⇒ la rama
  acepta). El paso que todo el mundo se salta: "es una tabla" usa el a lo sumo uno.
- Corolario: SAT es NP-completo (SAT ∈ NP por el capítulo 16, §4).

### 9. El error plantado

- Sin "a lo sumo uno". Medido: 1 de $2^n$ equivocada, siempre la cadena de ceros.
- Por qué: la unitaria $x_{0,j,0}$ dice que en la celda hay un 0, no que no haya un 1.
- Qué batería lo atrapa: las instancias no. La regla del capítulo 16, §13 otra vez.

### 10. 3-SAT

- Definición: cada cláusula con exactamente tres literales de variables distintas.
- El primer intento que falla: partir $(a \lor b \lor c \lor d)$ en
  $(a\lor b)\land(c \lor d)$. Arreglo con variable nueva.
- Construcción general, cláusulas de 2 literales con relleno; la de 1 literal queda
  para el ejercicio 5.
- **Figura**: la cadena de una cláusula de 6 literales con una asignación del código.
- **Teorema 4**: SAT $\le_p$ 3-SAT. Las dos direcciones. Tamaño lineal.
- Código: 300 fórmulas al azar, equivalencia por asignación de las variables
  originales (más fuerte que equisatisfacible). Romper la comprobación: quitar la
  última cláusula de la cadena da 1 asignación mala sobre 32.
- Cook ya lo hace en su teorema 2 (D₃), con el átomo nuevo $P$, en la forma dual.

### 11. 3-SAT como punto de partida

- 3-SAT ∈ NP, lema 3 del capítulo 16 ⇒ NP-completo.
- ¿Y 2-SAT? Está en P (capítulo 16, ejercicio 7). Cook anota en 1971 que $D_2$ está en
  P por Davis-Putnam. El ejercicio 7.
- Hacia adelante: el capítulo 18 (conjunto independiente, 3-coloración), 19 (ciclo
  hamiltoniano, suma de subconjuntos), 20 (ETH), 21 (7/8 de MAX-3SAT).

### 12. La regla

- Una fórmula solo dice lo que sus cláusulas prohíben. "Exactamente uno" son dos
  familias. Y una reducción se prueba en las instancias no.

## Ejercicios (11)

1. [traza] Contar variables y cláusulas en función de $t$, $|Q|$, $|\Gamma|$ y las
   cláusulas por ventana $K$; comprobar 11 353 para $t = 4$.
2. [traza] MTND que acepta las cadenas con dos ceros seguidos; su tabla para $1001$;
   comprobar la legalidad de la ventana del paso que adivina con un par real.
   *Cambio respecto a la semilla*: la semilla pedía la máquina de "contiene un 1", que
   es el ejemplo del cuerpo.
3. [entrada que rompe] Distributividad sobre $(x_1\land y_1)\lor\dots\lor(x_n\land y_n)$:
   $2^n$ cláusulas, y ninguna FNC equivalente sobre las mismas variables tiene menos.
4. [implementar y medir] Tseitin: CIRCUIT-SAT $\le_p$ SAT en tamaño lineal; implementar
   y medir contra la distributividad. *Cambio*: la semilla era "modelar"; se le añade
   la medición para tener un ejercicio de implementar y medir.
5. [demostración] Traza de la partición sobre la cláusula de 5 literales y sobre una
   de 1 literal; demostrar el relleno de 4 cláusulas; generalizar a $k$-SAT.
   *Cambio*: la semilla 5 (traza) y la 6 (demostrar la partición) se funden, porque
   la demostración de la partición está en el cuerpo (teorema 3).
6. [demostración] 3-SAT con cada variable a lo sumo tres veces (cláusulas de a lo sumo
   tres literales) sigue siendo NP-completo. *Nuevo*, para hacer pareja con el 10.
7. [cambio de hipótesis] ¿Por qué la partición no lleva de 3-SAT a 2-SAT?
8. [modelar] ★ NAE-3SAT es NP-completo. (Gadget comprobado en `check3.py`.)
9. [modelar] Exactamente-uno-3SAT es NP-completo. (Gadget comprobado.)
10. [demostración] SAT con cada variable a lo sumo dos veces está en P.
11. [entrada que rompe] Ventanas de $2 \times 2$: encontrar una máquina y una fila
    donde fallan. (Comprobado en `check22.py`.)

## Audios (unos 5 minutos cada uno)

| Audio | Secciones |
|---|---|
| 1 | §1 |
| 2 | §2 |
| 3 | §3 |
| 4–5 | §4 (lema 2 ocupa dos) |
| 6 | §5–§6 |
| 7 | §7 |
| 8 | §8 |
| 9 | §9 |
| 10 | §10 |
| 11 | §11–§12 |

## Decisiones que quiero confirmar

- La codificación con ventanas no es la de Cook (él usa variables de estado y de
  cabezal por paso). No cito ningún libro de texto para la de ventanas porque no la
  comprobé en una fuente primaria.
- No digo que Levin la descubrió "sin conocer" el trabajo de Cook: no lo comprobé.
- No uso el resultado de Karp (1972) de que 3-SAT está en su lista: no lo comprobé en
  el artículo.

## Revisión crítica contra la lista de errores de la guía

- (1) Las afirmaciones de costo: el tamaño de la fórmula está demostrado por conteo y
  medido. No digo nada de lo que *cuesta* resolver SAT salvo "nadie conoce un
  algoritmo polinomial" y la referencia a la ETH del capítulo 20, que es una hipótesis.
- (2) Las comprobaciones: la de la FNC por ventana y la de 3-SAT se rompen a propósito
  en el texto. La de "satisfacible si y solo si acepta" se rompe con el error plantado.
- (6) $O(t^2)$ cláusulas: se dan los conteos exactos, y la cláusula de
  $\varphi_{\text{acepta}}$ de $O(t^2)$ literales se dice.
- (7) Modelo: el tamaño de la fórmula se cuenta en bits ($O(t^2 \log t)$), no solo en
  cláusulas.
