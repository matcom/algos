# Introducción a NP-Completitud

- Problemas con solución $O(n^k)$ para $k$ constante.
  - Ejemplos: ...
  - Son problemas tratables (si la constante es chiquita, pero las constantes grandes son raras).
  - Muchos modelos de cómputo son polinomialmente equivalentes (TM-RAM-PRAM).
  - La composición de problemas polinomiales es polinomial.

- ¿Existen problemas estrictamente no polinomiales?
  - Fácil, problemas donde la salida es exponencial.
  - Pero la pregunta es existen problemas donde la salidad es polinomial, pero aún así no hay algoritmos polinomiales.
  - Esta es la pregunta P vs NP que vamos a intentar responder en esta clase.

- Intuitivamente, queremos decir que un problema es "difícil", y para ello vamos a usar reducciones.
  - Un problema A es tán "fácil" como un problema B si una solución a B me da una solución a A.
  - En este caso queremos que la solución a A sea a lo sumo polinomialmente más compleja que B.
  - Esto se llama una reducción polinomial de A a B.
  - Toda instancia de A se convierte en tiempo polinomial en instancia de B, y B se resuelve en tiempo polinomial, y la respuesta se transforma en tiempo polinomial.
  - Si sabemos que A no tiene solución polinomial, entonces B tampoco (¿por qué?)

- Problemas de decisión: donde la salida es $0$ o $1$.
  - ¿Por qué problemas de decisión? En general queremos problemas de optimización.
  - Coge un problema de optimización, dada una instancia $I$, encontrar el $R$ con mayor $V$, siempre se puede convertir, dada una instancia $I$, existe un $R$ con $V <= K$?.
  - Si el problema de optimización tiene solución polinomial, el de decisión también (¿cómo?), por tanto podemos demostrar sólo que las variantes de decisión son difíciles, y ya las de optimización lo serán.

## Problemas en P

- Problemas
  - Problema abstracto: Una asociación de Instancias a Respuestas
  - Problema concreto: Un encoding para cada instancia, un string binario (o un alfabeto de más símbolos)
  - Un algoritmo resuelve un problema concreto, en cierto encoding, y el T(n) se mide contra el tamaño del encoding (por eso `es_primo` sato no es polinomial!)

- Intuitivamente, queremos que el encoding específico no influya en si el algoritmo es polinomial o no.
  - Una función $f: \{0,1\}^* \rightarrow \{0,1\}^*$ es polinomialmente computable, si existe un algoritmo polinomial que dado cualquier string de entrada $x$, da como la salida $f(x)$ en tiempo polinomial.
  - Dos enconding $e_1$ y $e_2$ son polinomialmente equivalentes si existen funciones polinomialmente computables $f1(e1(s)) = e2(s)$ y $f_2(e2(s)) = e1(s)$.
  - ¿Podemos definiir un encoding natural razonablemente general?

*Lema 1*: Si tengo dos encoding polinomialmente equivalentes y un algoritmo polinomial en un encoding, también lo tengo en el otro.

> Con esto ya podemos dejar de hablar de encodings para hablar de complejidad polinomial (o no polinomial)

### Formalizando

- Los problemas de decisión son equivalentes a lenguajes
  - Coge un encoding cualquiera, define un lenguaje $L$ como el subconjunto de las cadenas en ese alfabeto tal que la salida es $1$.
  - El concepto decisión de un problema se convierte entonces en el problema de la palabra
  - Un algoritmo $A$ acepta una instancia, si $A(x) = 1$, y la rechaza si $A(x) = 0$.
  - Un algoritmo $A$ **acepta** un lenguaje $L$ si acepta todas las cadenas del lenguaje, pero eso no dice nada de las cadenas en $L^C$, puede rechazarlas, o puede quedarse en un ciclo infinito (esto es necesario, por Turing).
  - Un algoritmo $A$ **decide** un lenguaje $L$ si acepta toda cadena en $L$ y rechaza toda cadena en $L^C$.
  - Un lenguaje es aceptado (decidido) en tiempo polinomial si existe un algoritmo que lo acepta (decide) en tiempo polinomial.
  - Un algoritmo es una máquina de Turing, donde terminar en $1$ o $0$ implica terminar en un estado final o no.

*Teorema:* Si un lenguaje es aceptable en tiempo polinomial, también es decidible en tiempo polinomial.

Podemos definir entonces la clase $P$ como:

$P = \{L : L\textrm{ es aceptable en tiempo polinomial}\}$

## Problemas en NP

Vamos a definir ahora una clase aparentemente más flexible que $P$.

- Tenemos algoritmos que no sabemos ningún algoritmo polinomial
  - Ej: grafo hamiltoneano
  - ¿Cómo puedo convencerte de que un grafo es hamiltoneano?

- Sea $L$ un lenguaje, construyamos $L_p$ un lenguaje de pruebas, de la forma $(x,y)$ tal que $x \in L$, y $y$ es lo que llamamos un certificado o prueba de la pertenenecia de $x$ a $L$.
  - Por ejemplo, en el caso del ciclo hamiltoniano, $y$ es el ciclo.
  - Si $|y| = O(|x|^c)$ para cierta constante $c$ definida para todo el lenguaje, y
  - Existe un algoritmo $A(x,y)$ que decide el lenguaje $L_p$ en tiempo polinomial
  - Entonces $L$ es **verificable** en tiempo polinomial

$NP = \{L :\textrm{ Existe }L_p\textrm{ decidible en tiempo polinomial} \}$

NP significa **No-determinista polinomial**, por la siguiente idea, que es una forma alternativa de definirlo:

Existe una máquina de Turing no-determinista que acepta $L$ en tiempo polinomial.

- No determinista significa lo mismo que antes, que con el mismo símbolo en la cadena de entrada, hay transiciones hacia más de un estado.

- Si la máquina de Turing existe, entonces define $y$ es la secuencia de estados por la que pasa la máquina para decidir $x$.

- Si el problema es verificable en tiempo polinomial, entonces existe $L_p$ y por tanto hay un algoritmo $A$ y para cada $x$ hay un $y$ tal que $A(x,y)=1$. ¿Qué hacer?

## Problemas NP-Completos

- ¿Qué cosa es un problema NP-Completo?
  - Un problema tan difícil como todos los NP

- Una reducción polinomial de un lenguaje $L_1 \leq_p L_2$ es una función $f$ tal que $x \in L_1 \textrm{ i.i.f } f(x) \in L_2$

- Si $L \in NP$

- Definamos problema NP-Hard
  - Un problema es NP-Hard si todo problema en NP se reduce a él
  - Un lenguaje $L$ es NP-Hard si $L_i \leq_p L$ para todo lenguaje en $NP$.

- Un problema NP-Completo es un problema NP y NP-Hard.

- Notar que los NP-Hard no son de decisión, pero los NP-Completo sí.

- Por tanto la historia va a ser la siguiente:
  - Coge un problema, demuestra que está en P
  - Demuestra que se reduce a otro problema NP-Completo
  - Pero hace falta un problema NP-Completo inicial, ese lo veremos en la conferencia que viene.


## SAT y 3SAT

SAT es el problema de determinar si una fórmula CNF es satisfacible.

Demostrar que SAT es NP-Completo.

- Construir una fórmula que simula la máquina de Turing
- Por cada estado

## Aproximaciones

Para problemas de optimización

- p(n) aproximación max(C/C*,C*/C) >= 1
- aproximación polinomial
- esquema de aproximación (epsilon) -> (1+e) aproximacion
- esquema de aproximación polinomial (en n) y completamente polinomial (en n y en e)

### Ejemplos

Vertex cover: 2-approximation
TSP-euclideo: 2-approximation (prim + preorden)
No hay p-approximation para TSP general, reducción de Hamilton
Aproximación aleatoria para MAX-3SAT

Como se te ocurren estos algoritmos
- Prueba siempre una solución greedy
- Evalúa contra la solución exacta, para N creciente
- Si notas algún patrón, hora de demostrar

### Metaheurísticas (búsqueda en la frontera)

- Colonia de hormigas para TSP
- GRASP: empieza con un greedy, y búsqueda local
- Algoritmos poblacionales (genético vs probabilístico)
