# Resumen de la Parte III {.unnumbered #resumen-parte-3}

Este capítulo cierra la Parte III. No trae material nuevo. Junta en pocas páginas lo
que los capítulos 16 a 23 contaron por separado, muestra las ideas que solo se ven
mirándolos juntos, y termina con ejercicios que mezclan capítulos, en el estilo de las
preguntas del examen final. Cuando algo se cita, se dice de qué capítulo y sección
sale, para que puedas volver a la demostración completa.

## 1. El mapa de la parte

La Parte III tiene dos mitades. Los capítulos 16 a 19 contestan una pregunta: ¿cómo se
demuestra que un problema es difícil? Los capítulos 20 a 23 contestan la siguiente: si
lo es, ¿qué se puede hacer de todas formas?

| capítulo | pregunta | herramienta | ejemplo trabajado | error plantado |
|---|---|---|---|---|
| 16 | ¿qué quiere decir difícil? | P, NP, $\le_p$, NP-completo | independiente, clique, vertex cover | el complemento con aristas desordenadas |
| 17 | ¿cuál es el primero? | la tabla de configuraciones y sus ventanas | SAT, 3-SAT | quitar "a lo sumo uno" |
| 18 | ¿cómo se reduce a un grafo? | gadgets | independiente, 3-coloración, set cover | el segundo O conectado a $p_1$ |
| 19 | ¿y a números o recorridos? | filas que se recorren, columnas sin acarreo | ciclo hamiltoniano, TSP, suma de subconjuntos, mochila | holguras 1 y 2 con meta 3 |
| 20 | ¿exacto, pero mejor que la fuerza bruta? | poda, parámetro, recurrencia | mochila, vertex cover con $k$, independiente | la cota sin ordenar |
| 21 | ¿polinomial con garantía? | una cota calculable del óptimo | vertex cover, carga, k-center, set cover, MAX-3SAT | un extremo por arista |
| 22 | ¿y si la cota es un programa lineal? | árbol mínimo, emparejamiento, relajación | TSP métrico, vertex cover con pesos | redondear con `round` |
| 23 | ¿tan cerca como se quiera? | redondear la entrada, fuerte NP-dureza | mochila, makespan | el objeto que no cabe |

## 2. Lo que hay que llevarse de cada capítulo

Cada capítulo tiene su resumen al final. Aquí va una sola idea por capítulo: la que
usan los demás.

**Capítulo 16. Una reducción se escribe desde lo conocido hacia lo nuevo, y se
demuestra en las dos direcciones.** $A \le_p B$ con $A$ difícil dice que $B$ también
lo es; al revés no dice nada sobre $B$. La dirección "sí ⇒ sí" casi siempre se ve en
la construcción, y la que se olvida es la otra. Todo esto se mide en bits: un número
cuenta por la cantidad de dígitos con que se escribe, y por eso la tabla $O(nW)$ de la
mochila es pseudopolinomial y no polinomial.

**Capítulo 17. El primer NP-completo sale de la definición de NP.** Una rama de una
máquina no determinista es una tabla, una condición global sobre la tabla se comprueba
en ventanas de $2 \times 3$, y cada ventana es una fórmula de tamaño constante. De ahí
SAT, y partiendo cláusulas largas, 3-SAT, que es el punto de partida de todo lo
demás. La lección que se repite después: una fórmula solo dice lo que sus cláusulas
prohíben.

**Capítulo 18. Una reducción desde 3-SAT representa tres cosas: elegir, ser coherente
y cumplir cada cláusula.** Cada una es un gadget, y un gadget se verifica solo, por
enumeración, antes que la reducción entera. Con un triángulo por cláusula sale
conjunto independiente, y con él clique, vertex cover y set cover. Con la paleta
$T, F, B$ y el gadget de dos O sale 3-coloración.

**Capítulo 19. Las piezas de una reducción solo pueden comunicarse por donde la
demostración dice.** En el ciclo hamiltoniano, los vértices de separación impiden que
un ciclo entre a una cláusula por una fila y salga por otra. En suma de subconjuntos,
la base 10 impide los acarreos entre columnas. Con eso, once problemas NP-completos,
todos desde SAT, entre ellos TSP y mochila.

**Capítulo 20. Exacto no quiere decir fuerza bruta.** Branch and bound garantiza la
respuesta si la cota es una cota superior demostrada, y no garantiza el tiempo. El
parámetro saca la exponencial de $n$ y la pone en $k$: vertex cover en
$O(2^k(n + m))$. Una recurrencia demostrada da una base: $O(1{,}3803^n)$ para
conjunto independiente. Y la ETH dice que alguna base mayor que 1 es inevitable.

**Capítulo 21. Una razón de aproximación es una demostración contra una cota del
óptimo que se puede calcular.** El emparejamiento para vertex cover, $\max t_j$ y
$T/m$ para el balanceo de carga, $k + 1$ puntos lejanos para k-center, los precios
para set cover, el número de cláusulas para MAX-3SAT. La cota decide la razón, y
cuando la razón no mejora es casi siempre porque la cota no da más.

**Capítulo 22. La relajación lineal es la cota más general.** Basta escribir el
problema como programa entero y quitar la integralidad: el óptimo queda por debajo
del entero y se calcula en tiempo polinomial. Lo difícil pasa a ser redondear. El
mismo capítulo muestra la otra cara: sin desigualdad triangular, el TSP no admite
ninguna razón constante si P ≠ NP.

**Capítulo 23. Dónde se paga $\varepsilon$ lo deciden los números.** Si la tabla
exacta es pseudopolinomial y se deja redondear, hay FPTAS (la mochila). Si el problema
es fuertemente NP-duro, un FPTAS daría un algoritmo pseudopolinomial, y no hay FPTAS
si P ≠ NP; lo más que puede haber es un PTAS, que paga $\varepsilon$ en el exponente
(el makespan).

## 3. Cinco ideas que atraviesan la parte

### Un problema, varios capítulos

Tres problemas aparecen en casi todos los capítulos. Leído por columnas, cada uno
recorre la parte entera: se demuestra que es difícil, se resuelve exacto en tiempo
exponencial, se aproxima, y se sabe hasta dónde se puede aproximar.

| | vertex cover | mochila | TSP |
|---|---|---|---|
| es NP-completo | desde independiente (16, §10) y 3-SAT (18, §2) | desde suma de subconjuntos (19, §11) | desde ciclo hamiltoniano (19, §7), también métrico |
| exacto | $O(2^k(n + m))$ con parámetro $k$ (20, §8); $O(1{,}3803^n)$ con el conjunto independiente y el lema 5 del capítulo 16 (20, §11) | branch and bound (20, §2–5); tablas pseudopolinomiales (16, §3; 23, §2) | Held-Karp (11, §9) |
| aproximación | razón 2 por emparejamiento (21, §3); con pesos, razón 2 por relajación (22, §12) | FPTAS en $O(n^3/\varepsilon)$ (23, §3–5) | métrico: 2 con el doble árbol (22, §4), 3/2 con Christofides (22, §7–8) |
| lo que no se puede | razón $\sqrt 2 - \varepsilon$ es NP-dura (23, §12); sin $2^{o(N)}$ si vale la ETH (20, §12) | tiene FPTAS y tabla pseudopolinomial | general: ninguna razón constante (22, §2); métrico: menos de $123/122$ es NP-duro (22, §9) |

Tres cosas se ven en la tabla y en ningún capítulo solo.

La primera: **NP-completo no dice cuánto cuesta aproximar.** Los tres problemas son
NP-completos con la misma definición, y sus filas de aproximación no se parecen: la
mochila llega a $1 - \varepsilon$ para todo $\varepsilon$, vertex cover se queda entre
$\sqrt 2$ y 2, y el TSP general no tiene ninguna razón. La NP-completitud es una
afirmación sobre la versión de decisión, y la reducción que la demuestra no dice nada
de las razones. Lo que separa las filas lo dicen dos ideas de más abajo: los números
y las reducciones con hueco.

La segunda: **la misma estructura sirve en varias filas.** El emparejamiento es la cota
de la aproximación de vertex cover (21, §3), y un emparejamiento perfecto mínimo es la
pieza que Christofides agrega al árbol (22, §7). La relajación lineal de vertex cover
(22, §10) se reescribe con $z_v = 1 - x_v$ como la relajación de conjunto
independiente (22, §11), el mismo complemento del capítulo 16, §10.

La tercera: **el TSP métrico y el general son problemas distintos para la
aproximación, y el mismo para la decisión.** La reducción del capítulo 19, §7 da
distancias 1 y 2, que ya son métricas, así que los dos son NP-completos. Pero la
desigualdad triangular es lo que permite los atajos del doble árbol (22, §4), y sin
ella la reducción del capítulo 22, §2 abre un hueco que ninguna razón constante salva.
Una hipótesis que no cambia la decisión puede cambiar todo lo demás.

### Los números deciden

Un hilo que empieza en el capítulo 16 y termina en el 23 es el tamaño de los números.

- **Capítulo 16, §3.** Un número $W$ se escribe con $\log_2 W$ bits, así que $O(nW)$
  es exponencial en el tamaño de la entrada. Pseudopolinomial no es polinomial.
- **Capítulo 19, §8–9.** La reducción de 3-SAT a suma de subconjuntos usa números de
  $n + k$ dígitos, y la meta vale del orden de $10^{n+k}$. Tiene que ser así: el
  ejercicio 9 de ese capítulo demuestra que una reducción con metas polinomiales daría
  $P = NP$, porque la tabla del capítulo 16 la resolvería.
- **Capítulo 20, §5.** El error plantado de la cota sin ordenar no se ve con valores
  iguales a los pesos, que son justo las instancias que salen de la reducción de suma
  de subconjuntos a mochila: todas las densidades valen 1, y cualquier orden es el
  bueno.
- **Capítulo 23, §2–5.** La tabla por valores es pseudopolinomial en los valores, y el
  FPTAS la usa después de redondearlos: dividir los valores por
  $\mu = \varepsilon v_{\max}/n$ los deja todos por debajo de $n/\varepsilon$. El
  tiempo deja de depender de $v_{\max}$.
- **Capítulo 23, §7–9.** Un problema fuertemente NP-duro sigue siendo difícil con
  números polinomiales en el tamaño, así que no tiene algoritmo pseudopolinomial si
  P ≠ NP (teorema 3), ni FPTAS (corolario 6). 3-PARTICIÓN lo es, y por eso el
  makespan con $m$ libre también.

Juntos dicen algo que ninguno dice solo: **la mochila es difícil solo por sus
números.** Su NP-completitud necesita metas de $n + k$ dígitos, su algoritmo exacto
es polinomial si los números son chicos, y su FPTAS consiste en hacerlos chicos a
propósito pagando un error. Un problema fuertemente NP-duro no tiene esa salida, porque
achicar los números no lo hace fácil.

### Una cota del óptimo hace dos trabajos

Las dos mitades de la parte usan el mismo objeto: un número que se calcula rápido y
acota el óptimo.

| capítulo | problema | cota | uso |
|---|---|---|---|
| 20, §3 | mochila (maximizar) | la mochila fraccionaria, por arriba | podar en branch and bound |
| 21, §3 | vertex cover | un emparejamiento, por abajo | razón 2 |
| 21, §5–7 | balanceo de carga | $\max t_j$ y $T/m$, por abajo | razones $2 - 1/m$ y $4/3 - 1/(3m)$ |
| 22, §3 | TSP métrico | el árbol mínimo, por abajo | razón 2 |
| 22, §10–12 | vertex cover con pesos | la relajación lineal, por abajo | razón 2 |
| 23, §4 | mochila | $v_{\max}$, por abajo | razón $1 - \varepsilon$ |

En el exacto, la cota tiene que ser optimista: al maximizar, una cota superior de
todo lo que se puede completar desde un nodo permite descartarlo si no supera lo mejor
visto, y una cota que a veces queda por debajo descarta ramas buenas. En las
aproximaciones de minimizar de los capítulos 21 y 22 también es optimista,
$B \le \mathrm{OPT}$, y la demostración termina con $c \le \alpha B \le
\alpha\,\mathrm{OPT}$. La última fila es distinta: en la mochila, que se maximiza,
$v_{\max} \le \mathrm{OPT}$ es una cota pesimista, y no se compara con la salida sino
con el error del redondeo, que es menor que $n\mu = \varepsilon v_{\max} \le
\varepsilon\,\mathrm{OPT}$.

La mochila fraccionaria del capítulo 20 es la relajación lineal de la mochila 0-1,
como el capítulo 20, §6 dice de pasada: quita la condición $x_i \in \{0, 1\}$, y el
goloso por densidad la resuelve (20, lema 2). Es la misma idea que el capítulo 22
lleva a vertex cover con pesos, donde el óptimo fraccionario ya no se calcula con un
goloso sino con el simplex. Y en los dos casos el error plantado vive en el mismo
sitio: la cota se calcula con un atajo (sin ordenar en el capítulo 20, con `round` en
el 22) y el resultado deja de ser lo que la demostración necesita.

Hay un límite que solo se ve juntando el capítulo 22 con el 21. Si una razón se
demuestra comparando contra la cota $B$, no puede ser mejor que el peor cociente
$\mathrm{OPT}/B$. En el triángulo con pesos 1, la relajación de vertex cover vale
$3/2$ y el óptimo 2 (22, §10). Por eso la regla del capítulo 21 dice que para mejorar
la razón hay que mejorar la cota.

### Una reducción lleva más que un sí o un no

En la primera mitad, una reducción transporta una respuesta. En la segunda, la misma
técnica transporta otras cosas, y cada una pide algo más de la reducción.

- **Dificultad de decidir** (16 a 19). Basta que sea polinomial y que conserve la
  respuesta en las dos direcciones.
- **Tiempo exponencial** (20, §12). Para pasar la ETH de 3-SAT a conjunto
  independiente hace falta además que el tamaño de la salida sea **lineal**: la
  reducción del capítulo 18 da $3m$ vértices, y el lema de esparcimiento permite
  suponer $m = O(n)$. Si la reducción diera $N = n^2$ vértices, un algoritmo en
  $2^{o(N)}$ para el problema de llegada daría solo uno en $2^{o(n^2)}$ para 3-SAT, y
  la ETH no prohíbe eso.
- **Dificultad de aproximar** (21, §9; 22, §2; 21, ejercicio 4). La reducción produce
  instancias con un **hueco**: las instancias sí tienen óptimo a lo sumo un valor $b$,
  y las no, óptimo mayor que $\alpha b$. Una $\alpha$-aproximación
  distingue los dos casos y decide el problema original. En k-center, distancias 1 y
  2 dan el hueco de 2 (21, teorema 7). En el TSP general, el peso
  $(\alpha - 1)n + 2$ en las no aristas da el hueco que haga falta (22, teorema 1).
- **Dificultad con números chicos** (23, §8). Para pasar la fuerte NP-dureza de
  3-PARTICIÓN al makespan, la reducción tiene que producir números polinomiales en el
  tamaño, no solo en tiempo polinomial.

Y al revés: lo que una reducción **no** conserva. La reducción
$(G, k) \mapsto (G, n - k)$ del capítulo 16, §10 lleva vertex cover a conjunto
independiente y conserva el óptimo exacto. Pero no conserva el parámetro, como señala
el ejercicio 8 del capítulo 20, y no conserva la razón, como pide el ejercicio 3 de
este capítulo. La razón 2 y el algoritmo FPT de vertex cover no pasan a conjunto
independiente por esta reducción, y el libro no da ninguna de las dos cosas para
conjunto independiente.

### Los ocho errores plantados

En cada capítulo plantamos un error en una variante que parecía correcta.

| capítulo | error plantado | qué vieron las pruebas | qué lo anunciaba |
|---|---|---|---|
| 16, §11 | el complemento con aristas desordenadas | 204 fallos en 678 instancias no, ninguno en las 522 sí | toda arista construida es un par que no está en $E$ |
| 17, §9 | quitar "a lo sumo uno" | solo la cadena de ceros, la única instancia no de cada largo | cada celda tiene exactamente una variable verdadera |
| 18, §9 | el segundo O desde $p_1$ | dice sí a toda fórmula; solo lo ven las instancias no y los 8 casos del gadget | las dos entradas del segundo O son $F$ |
| 19, §10 | holguras 1 y 2 con meta 3 | toda fórmula tiene solución; las baterías con solución plantada no lo ven | lo que aportan las holguras es a lo sumo 3 |
| 20, §5 | la cota sin ordenar | la ven las instancias al azar; no la ven valores iguales a los pesos, ya ordenadas, ni capacidad para todo | el lema 2 usa el orden |
| 21, §4 | un extremo por arista | razón promedio 1,014 contra 1,692; ninguna pasa de 2 al azar, y con $k = 24$ paga 2,50 veces | las aristas que disparan una elección no comparten extremos |
| 22, §13 | redondear con `round` | la batería de la razón la aprueba en las 456 entradas; la del cubrimiento la atrapa en 74 | uno de los dos extremos vale **al menos** $1/2$ |
| 23, §6 | no filtrar el objeto que no cabe | 14 de 1 000 con instancias del capítulo 20, ninguna si todo cabe | $v_{\max} \le \mathrm{OPT}$ |

Leída por mitades, la tabla dice dos cosas distintas.

En los capítulos 16 a 19 el error vive siempre en la dirección "no ⇒ no" de la
reducción, y las instancias sí no lo ven nunca. La razón es la misma en los cuatro: la
dirección "sí ⇒ sí" se demuestra construyendo una solución, y la variante sigue
permitiendo esa solución. Lo que la variante rompe es una prohibición (un par que no
debe ser arista, una celda que no debe tener dos símbolos, una salida que no debe
quedar en $T$, una columna que no debe llenarse sola), y una prohibición solo se
nota en una instancia donde no hay solución.

En los capítulos 20 a 23 el error vive en una hipótesis de la cota, y las entradas
donde esa hipótesis se cumple sola no lo ven: densidades iguales hacen que todo orden
sea el ordenado, en grafos al azar la regla de un extremo gana en promedio, una batería de razón no mira si la salida es factible, y si todo cabe no
hay objeto que filtrar. El capítulo 22, §13 tiene además un caso que conviene
recordar aparte: la batería de la razón **no podía fallar**, porque la variante toma un
subconjunto de lo que toma el redondeo correcto. Una comprobación que no puede fallar
no comprueba nada; antes de confiar en una, rompe a propósito lo que mide y mira que
falle.

Las dos mitades llevan a la misma regla que la Parte I: la variante pasa las pruebas que uno escribe primero, y la demostración dice qué
entradas hacen falta. Pregúntale a cada paso de la demostración qué hipótesis usa, y
construye la entrada donde esa hipótesis falla.

## 4. Cómo se ve una respuesta completa

Un ejercicio de la Parte III pide casi siempre una de dos cosas: demostrar que un
problema es NP-completo, o dar un algoritmo con garantía para uno que lo es. Los dos
ejemplos que siguen están en el libro, y lo que importa aquí es la forma.

**Problema 1.** SET-COVER: dado un universo $U$, una familia de subconjuntos y un
entero $k$, ¿hay a lo sumo $k$ conjuntos de la familia cuya unión es $U$? Demostrar que es
NP-completo.

*Pertenencia a NP.* El certificado es la lista de a lo sumo $k$ conjuntos. El
verificador comprueba que son de la familia y que su unión es $U$, en tiempo
polinomial en el tamaño de la entrada.

*Problema conocido.* VERTEX-COVER, que es NP-completo (18, corolario 2).

*Construcción y costo.* Dado $(G, k)$ con $G = (V, E)$, el universo es $U = E$, cada
vértice $v$ da el conjunto $S_v$ de las aristas que lo tocan, y el número es el mismo
$k$. Son $|V|$ conjuntos con $2|E|$ elementos en total: tiempo lineal.

*Si la original es sí, la construida es sí.* Si $C$ es un vertex cover con $|C| \le k$, toda arista tiene un extremo
$v \in C$, y está en $S_v$. Los conjuntos $\{S_v : v \in C\}$ cubren $U$.

*Si la construida es sí, la original es sí.* Si $S_{v_1}, \dots, S_{v_j}$ con $j \le k$ cubren $U$, toda arista está en
algún $S_{v_i}$, es decir, toca a algún $v_i$. Entonces $\{v_1, \dots, v_j\}$ es un
vertex cover de tamaño a lo sumo $k$.

*Conclusión.* Por el lema 3 del capítulo 16, set cover es NP-completo.

**Problema 2.** Dar un algoritmo polinomial para vertex cover mínimo con razón
constante.

*Algoritmo.* Recorrer las aristas; si ninguno de los dos extremos está en $C$, meter
los dos (21, §3).

*Factibilidad.* Cuando el recorrido pasa por una arista, o ya tenía un extremo en $C$,
o los mete a los dos. Al final toda arista está cubierta.

*Cota del óptimo.* Las aristas que dispararon una elección no comparten extremos,
porque después de elegir una, sus dos extremos están en $C$ y ninguna arista que los
toque dispara otra. Forman un emparejamiento $M$, y todo cubrimiento contiene un
extremo distinto de cada arista de $M$: $\mathrm{OPT} \ge |M|$.

*Razón.* $|C| = 2|M| \le 2\,\mathrm{OPT}$.

*Tiempo.* $O(|V| + |E|)$ con un arreglo de marcas.

Esa es la forma: para la dificultad, pertenencia, conocido, construcción con su costo
y las dos direcciones escritas por separado; para la aproximación, algoritmo,
factibilidad, cota calculable del óptimo, razón y tiempo. La respuesta de un examen
no tiene que ser más larga que esto para un problema de este tamaño, y no puede
saltarse ninguno de esos pasos: los ocho errores de la tabla anterior viven cada uno
en un paso que alguien pensó que era obvio.

## Ejercicios

Cada ejercicio dice entre paréntesis qué capítulos usa. No llevan solución.

1. [traza] Sea $C_5$ el ciclo de vértices $0, 1, 2, 3, 4$ con aristas
   $(0,1), (1,2), (2,3), (3,4), (0,4)$, en ese orden. (a) Corre
   `cubrimiento_emparejamiento` del capítulo 21, §3. (b) Corre `cover_k` del capítulo
   20, §8 con $k = 2$ y con $k = 3$, y dibuja los dos árboles con su número de nodos.
   (c) Encuentra el óptimo de la relajación lineal del capítulo 22, §10 y demuestra
   que lo es, y aplica el redondeo del teorema 7 del capítulo 22. (d) Con el lema 5 del
   capítulo 16, da un conjunto independiente máximo. Escribe en una tabla el tamaño
   que devuelve cada método, el óptimo y la razón. ¿Cuál de los métodos con garantía
   2 queda más cerca de su garantía en esta entrada, y por qué? (16, 20, 21, 22)

2. [traza] Sea $\varphi = (x_1 \lor x_2 \lor \lnot x_3) \land (\lnot x_1 \lor x_2 \lor
   x_3)$. Construye las tres instancias: el grafo de conjunto independiente del
   capítulo 18, §2, el grafo de 3-coloración del capítulo 18, §8, y la tabla de suma de
   subconjuntos del capítulo 19, §8. Da el tamaño de cada una. Para la asignación
   $x_1 = x_3 = $ falso, $x_2 = $ verdadero, escribe la solución que le corresponde en
   cada instancia: el independiente, el coloreo y el subconjunto con sus holguras.
   ¿En cuál de las tres instancias hay más de una solución para esa misma asignación?
   (17, 18, 19)

3. [demostración] El algoritmo siguiente busca un conjunto independiente grande:
   calcula un vertex cover $C$ con `cubrimiento_emparejamiento` y devuelve $V - C$.
   (a) Demuestra que devuelve un conjunto independiente. (b) Da una familia de grafos,
   uno para cada $n$ par, donde devuelve el conjunto vacío y el máximo tiene $n/2$
   vértices; concluye que no tiene razón constante. (c) Demuestra que si el
   cubrimiento mínimo de $G$ tiene a lo sumo $n/3$ vértices, el conjunto que devuelve
   tiene al menos la mitad de los vértices de uno máximo. (d) El teorema 6 del
   capítulo 16 usa la misma relación entre los dos problemas. Explica qué conserva esa
   reducción y qué no, y por qué eso no contradice que la reducción sea correcta.
   (16, 21)

4. [demostración] Un **conjunto dominante** de $G$ es un $D \subseteq V$ tal que todo
   vértice está en $D$ o tiene un vecino en $D$. (a) Escribe el problema del dominante
   mínimo como un caso de set cover que conserva el costo de cada solución, y deduce un
   algoritmo polinomial de razón $H_n$. (b) El capítulo 21, §9 reduce el dominante a
   k-center con distancias 1 y 2, y k-center tiene una 2-aproximación. Un compañero
   concluye que el dominante mínimo tiene una aproximación de razón constante.
   Encuentra el paso que falla en su argumento: di qué mide la razón en cada problema y
   qué hace la reducción con cada medida. (18, 21)

5. [demostración] Para cada uno de los resultados hipotéticos siguientes, di si
   refutaría P ≠ NP, la ETH, la SETH, o ninguna de las tres, y demuéstralo citando la
   cadena de teoremas que usas. (a) Vertex cover en $O(1{,}1^k (n + m))$. (b) Conjunto
   independiente en $O(2^{\sqrt N})$ en grafos de $N$ vértices. (c) 3-SAT en
   $O(1{,}3^n)$. (d) Para todo $k$, $k$-SAT en $O(1{,}99^n)$. (e) Un FPTAS para el
   makespan con $m$ parte de la entrada. (f) Una $1{,}9$-aproximación polinomial para
   k-center métrico. (g) Un algoritmo polinomial para suma de subconjuntos cuando
   $T \le n^5$. (h) Una aproximación polinomial de razón $n$ para el TSP con
   distancias arbitrarias. (i) Una $1{,}5$-aproximación polinomial para vertex cover.
   (j) Una $1{,}4$-aproximación polinomial para vertex cover. (16, 20, 21, 22, 23)

6. [entrada que rompe] Un compañero propone una aproximación para el TSP con distancias
   simétricas arbitrarias: reemplazar cada $d(u, v)$ por $d^*(u, v)$, el costo del
   camino más corto de $u$ a $v$, correr Christofides con $d^*$, y devolver el
   recorrido que sale. Dice que, como $d^*$ es métrica, la razón es $3/2$. (a)
   Demuestra que $d^*$ es métrica. (b) Su afirmación contradiría el teorema 1 del
   capítulo 22 si P ≠ NP. Encuentra el paso de su argumento que falla. Después
   construye una entrada de cuatro ciudades y una ejecución de Christofides con $d^*$
   (un árbol mínimo, un emparejamiento mínimo y un circuito euleriano entre los que el
   algoritmo permite elegir cuando hay empates) cuyo recorrido, medido con $d$, cueste
   más que $3/2$ del óptimo. (c) Si se permite pasar más de una vez por una ciudad, y se
   quiere el paseo cerrado más barato que visite todas, demuestra que la propuesta sí
   da razón $3/2$. ¿Qué tiene que ver esto con los atajos del capítulo 22, §4? (19, 22)

7. [cambio de hipótesis] Supón que todos los números de la entrada se escriben en
   unario, de modo que el número $a$ ocupa $a$ símbolos. (a) Decide cuáles de estos
   problemas quedan en P: suma de subconjuntos, partición, mochila, 3-PARTICIÓN, el
   makespan con $m$ parte de la entrada, y el TSP con distancias 1 y 2. Justifica
   cada uno con un algoritmo o con un teorema del libro. (b) ¿Sigue siendo polinomial
   la reducción de 3-SAT a suma de subconjuntos del capítulo 19, §8, si su salida se
   escribe en unario? ¿Y la de 3-PARTICIÓN al makespan del capítulo 23, §8? (c) ¿Qué
   pasa con el FPTAS de la mochila del capítulo 23 en este modelo? (16, 19, 20, 23)

8. [implementar y medir] ★ Escribe un branch and bound para vertex cover mínimo, que
   ramifica en una arista como `cover_k` y poda un nodo cuando lo elegido más una cota
   inferior del grafo que queda no mejora lo mejor visto. Usa dos cotas: el tamaño de
   un emparejamiento maximal del grafo que queda (21, lema 1), y el óptimo de la
   relajación lineal con `relajacion` del capítulo 22, §11. (a) Demuestra que las dos
   son cotas inferiores válidas, y que para todo emparejamiento $M$ de un grafo la
   relajación vale al menos $|M|$. (b) Demuestra que el algoritmo es exacto, adaptando
   el teorema 3 del capítulo 20 a minimizar. (c) Mide nodos y tiempo con cada cota en
   grafos al azar de 10 a 30 vértices, y di cuándo compensa la cota más fuerte su
   costo. (20, 21, 22)

9. [implementar y medir] Compón la reducción de 3-SAT a conjunto independiente del
   capítulo 18, §2 con `independiente_max` del capítulo 20, §10, y úsalo para decidir
   fórmulas al azar con $n$ de 3 a 6 variables y $m = 2n$ y $m = 4n$ cláusulas. Cuenta
   las llamadas a `rec` y compáralas con los $2^n$ casos de la fuerza bruta sobre la
   fórmula y con la cota $2\alpha^{3m}$ del teorema 7 del capítulo 20. Explica lo que
   ves con el tamaño de la instancia que produce la reducción. ¿Por qué el teorema 8
   del capítulo 20 puede usar esta misma reducción para pasar la ETH, si como algoritmo
   es tan mala? (17, 18, 20)

10. [modelar] Un laboratorio de cómputo tiene cuatro servidores iguales y recibe cada
    noche unos 200 trabajos con su duración estimada. (a) Hay que repartirlos para que
    el último termine lo antes posible. (b) Algunas noches hay más trabajo del que
    cabe en 8 horas por servidor, y se aceptan los trabajos que más beneficio dan sin
    pasarse; supón primero un solo servidor. (c) Un técnico recorre cada mañana los 12
    locales donde están los equipos, con los tiempos de caminata entre ellos, y vuelve
    al inicio. Para cada parte, di qué problema de la Parte III es, qué algoritmo
    usarías (exacto, con razón o un esquema), qué garantía y qué tiempo tiene, y qué
    cambia si en lugar de 4 servidores fueran 200, o si en lugar de 12 locales fueran
    120. (11, 21, 22, 23)
