# Outline: Conferencia 4, análisis amortizado

Estado: aprobado y redactado (2026-09-29). Las notas están en `notas.md`.
Destino: `Lectures/2026/04-amortizado/notas.md` + PDF con scriptorium.
Extensión objetivo: 6 500–7 500 palabras. Es más larga que las conferencias 2 y 3
porque el plan pide dos demostraciones completas, splay y union-find, además del
ejemplo de la cola. Decidido el 2026-09-28: las notas llevan las dos completas, y el
reparto en audio se decide aparte.

## Idea de la clase

La conferencia 3 usó un potencial que solo baja, para demostrar que un algoritmo
termina. Esta usa un potencial que sube y baja, para pagar las operaciones caras con
lo ahorrado en las baratas. La pregunta cambia de "cuánto cuesta la peor operación" a
"cuánto cuesta una secuencia de $m$ operaciones, en el peor caso, dividido por $m$".

La distinción tiene que quedar clara desde el principio, porque es lo que se confunde:
el costo amortizado **no es un promedio sobre entradas aleatorias**. Es una garantía
de peor caso sobre secuencias. No hay probabilidad en ninguna parte de la clase.

El hilo son tres estructuras en orden creciente de dificultad. La cola con dos pilas
muestra los tres métodos (agregado, contabilidad, potencial) sobre algo donde los tres
son cortos. Los splay trees muestran el potencial en serio, con un error plantado que
la demostración explica. Union-find muestra que un potencial no siempre es una
fórmula: a veces es un argumento de conteo por grupos.

## Estructura

### 1. La peor operación miente

- Ejemplo de apertura: un arreglo dinámico que duplica su capacidad. Un `append` cuesta
  $\Theta(n)$ en el peor caso y, sin embargo, $n$ `append` cuestan $O(n)$ en total.
  Analizar operación por operación da $O(n^2)$, que es verdadero e inútil.
- Definición: el costo amortizado de una operación es cualquier cantidad $\hat c_i$
  tal que $\sum_{i=1}^m c_i \le \sum_{i=1}^m \hat c_i$ para **toda** secuencia. Es una
  cota de peor caso sobre la secuencia.
- Lo que el costo amortizado no es: un caso promedio. Se dice explícitamente y se
  vuelve a decir al final.
- Conexión con Estructuras de Datos: la lista de Python y el `vector` de C++ ya
  funcionan así. Ahí se enunció el $O(1)$ amortizado, y aquí se demuestra.

### 2. La cola con dos pilas: tres métodos

- La estructura: se encola en una pila de entrada y se desencola de una pila de salida.
  Cuando la de salida está vacía se vuelca la de entrada entera. Un `desencolar` cuesta
  $\Theta(n)$ en el peor caso.
- **Agregado**: cada elemento se apila, se mueve y se desapila a lo sumo una vez cada
  cosa, así que $m$ operaciones cuestan a lo sumo $3m$.
- **Contabilidad**: se cobra 3 por `encolar` y 1 por `desencolar`. Cada elemento de la
  pila de entrada guarda el crédito de 2 que paga su mudanza y su salida. El invariante
  es que el crédito nunca es negativo.
- **Potencial**: $\Phi = 2 \cdot |\text{entrada}|$. El costo amortizado es
  $\hat c_i = c_i + \Phi_i - \Phi_{i-1}$. La condición que hace que la suma funcione es
  $\Phi_m \ge \Phi_0$, y se señala porque es el paso que todo el mundo olvida.
- Cómo se relacionan: el crédito de la contabilidad, sumado sobre toda la estructura,
  es el potencial. El potencial es la contabilidad sin nombres.
- **Código ejecutable**: la cola instrumentada sobre 100 000 operaciones aleatorias.
  Medido en `.playground`: la operación más cara cuesta 9 173 y el promedio es 1,5.
- **Figura**: el costo real paso a paso (picos) y el costo amortizado constante, con
  el potencial debajo subiendo y cayendo. La figura recibe la secuencia medida.

### 3. Qué es un buen potencial

- Tres condiciones: arranca en 0 (o en algo fijo), nunca es negativo, y sube cuando
  la estructura se "desordena" de una manera que una operación futura va a tener que
  pagar.
- Cómo se le ocurre a uno: preguntar qué deuda está acumulando la estructura. En la
  cola, los elementos que todavía no se mudaron. En un árbol, los caminos largos que
  todavía no se recorrieron.
- Conexión con la conferencia 3: allí el potencial solo bajaba y contaba vueltas.
  Aquí baja en las operaciones caras y sube en las baratas.

### 4. Splay trees: el algoritmo

- Motivación: un árbol binario de búsqueda sin información de balance que se reordena
  solo según los accesos, y que aun así garantiza $O(\log n)$ amortizado.
- **Cómo se le ocurre a uno.** La primera idea es mover el nodo accedido a la raíz con
  rotaciones simples, que es la heurística de Allen y Munro (1978). La idea es buena
  (lo que se usa mucho queda arriba), pero no alcanza, y la sección 6 mide cuánto no
  alcanza.
- El splay de Sleator y Tarjan (1985) sube el nodo de dos en dos, con tres casos:
  zig (el padre es la raíz), zig-zig (nodo y padre del mismo lado) y zig-zag (de lados
  distintos). La diferencia con subir a la raíz está solo en el caso zig-zig: se rota
  primero el padre y después el nodo.
- **Figura**: los tres casos de rotación, como diagrama de demostración.
- **Código ejecutable**: splay y subir a la raíz, con un contador de rotaciones.

### 5. Splay trees: el lema de acceso (sección larga)

- Pesos y rangos: $s(x)$ es el número de nodos en el subárbol de $x$, y
  $r(x) = \log_2 s(x)$. El potencial es $\Phi = \sum_x r(x)$.
- **Lema de acceso** (Sleator y Tarjan): el costo amortizado de hacer splay de $x$ en
  un árbol con raíz $t$ es a lo sumo $3(r(t) - r(x)) + 1 = O(\log n)$. Es el enunciado
  exacto del artículo, verificado.
- Demostración por casos. Por cada paso, el costo amortizado es a lo sumo
  $3(r'(x) - r(x))$ en zig-zig y zig-zag, y $3(r'(x) - r(x)) + 1$ en zig. Los pasos
  se telescopian y el zig ocurre una sola vez, al final.
- El único ingrediente no trivial: si $a + b \le c$, entonces
  $\log a + \log b \le 2 \log c - 2$, por la concavidad del logaritmo. Se demuestra
  aparte en dos líneas. Lo usan zig-zig y zig-zag: ese $-2$ es lo que paga las dos
  rotaciones del paso.
- **Por qué subir a la raíz falla, leído en la demostración.** Una rotación simple
  tiene costo amortizado a lo sumo $1 + r'(x) - r(x)$, igual que el zig. Subir a la
  raíz hace $d$ rotaciones simples, y los $d$ unos no se telescopian: la cota que
  sale es $d + (r(t) - r(x))$, que es $O(d)$ y no $O(\log n)$. En zig-zag, splay hace
  las mismas dos rotaciones que subir a la raíz y la desigualdad paga el $+2$. En
  zig-zig solo lo paga si se rota primero el padre. Esa es toda la diferencia entre
  las dos heurísticas.
- Consecuencia: $m$ accesos sobre $n$ nodos cuestan
  $O((m + n) \log n)$ en total. El término $n \log n$ es el potencial inicial, porque
  el árbol puede arrancar como un camino.

### 6. El error que la demostración anuncia

- El experimento: un árbol camino con $n$ nodos, y se acceden las claves en orden,
  cinco rondas.
- Medido en `.playground`: splay cuesta unos 5,3 por acceso para $n = 100$, 400 y
  1600, mientras que subir a la raíz cuesta $n/2$ por acceso (51,5, 201,5 y 801,5).
  Es $\Theta(n)$ contra constante.
- **Figura**: el árbol después de tres accesos con cada heurística, dibujado desde el
  estado real. Splay deja el camino con la profundidad aproximadamente a la mitad;
  subir a la raíz deja otro camino.
- Moraleja: las dos heurísticas pasan cualquier prueba de correctitud (el árbol sigue
  siendo de búsqueda y el nodo termina en la raíz). La diferencia es solo de costo, y
  solo aparece en secuencias adversas. La demostración dice cuál es la secuencia: la
  que hace que el zig-zig se repita, que es un camino.
- Guardar la frase de Sleator y Tarjan: el splay "reduce aproximadamente a la mitad la
  profundidad de cada nodo del camino", y subir a la raíz no.

### 7. Union-find: lo que ya sabían y lo que falta

- Repaso rápido: bosque de árboles con puntero al padre, `find` sube hasta la raíz,
  `union` cuelga una raíz de la otra. Unión por rango y compresión de caminos.
- Medido en `.playground`, sobre 16 384 elementos:
  - Sin heurísticas, una cadena cuesta unos 8 192 pasos por operación.
  - Solo unión por rango, con árboles binomiales construidos a propósito, llega a
    profundidad exactamente $\log_2 n$ y cada `find` al fondo cuesta $\log_2 n$.
  - Con las dos heurísticas, 1,2 pasos por operación en operaciones aleatorias, y
    alrededor de 1 en el caso binomial.
- **Figura**: un camino antes y después de un `find` con compresión, desde el estado
  real.
- La pregunta de la clase: por qué, con las dos, el costo es casi constante.

### 8. Union-find: la cota $O(m \log^* n)$ (sección larga)

- Tres propiedades del rango, cada una con una demostración de pocas líneas:
  - El rango crece estrictamente al subir hacia la raíz.
  - Un nodo de rango $r$ es raíz de un subárbol con al menos $2^r$ nodos, en el
    momento en que deja de ser raíz.
  - Hay a lo sumo $n / 2^r$ nodos de rango $r$. En particular, ningún rango pasa de
    $\log_2 n$.
- $\log^* n$: cuántas veces hay que aplicar $\log_2$ para bajar de 1. Para
  $n \le 2^{65536}$ vale a lo sumo 5. Tabla de valores.
- Grupos de rango: el grupo $g$ contiene los rangos del intervalo $(k, 2^k]$, con las
  torres de dos como fronteras. Hay a lo sumo $\log^* n$ grupos.
- El conteo, que es un potencial por grupos: cada paso de un `find` sube de un nodo a
  su padre. Si el padre está en otro grupo, se cobra a la operación, y hay a lo sumo
  $\log^* n$ de esos por `find`. Si está en el mismo grupo, se cobra al nodo. Cada
  vez que se le cobra a un nodo, la compresión le da un padre de rango mayor, así que
  un nodo del grupo $(k, 2^k]$ paga a lo sumo $2^k$ veces antes de que su padre salga
  del grupo. Por la tercera propiedad, el grupo tiene a lo sumo $n / 2^k$ nodos, y en
  total paga a lo sumo $n$. Sumando los grupos, $n \log^* n$.
- Total: $O(m \log^* n + n \log^* n)$.
- Hopcroft y Ullman (1973), verificado.

### 9. La cota de Tarjan y la cota mínima (sección corta)

- Tarjan (1975) afinó la cota a $O(m \, \alpha(m, n))$, donde $\alpha$ es una inversa
  de la función de Ackermann, y demostró que ese es el costo exacto de este algoritmo.
  Se enuncia sin demostrar.
- Fredman y Saks (1989) demostraron que ninguna estructura puede hacerlo mejor en el
  modelo de sondeo de celdas: $\Omega(\alpha)$ amortizado por operación. Se enuncia,
  verificado, y se conecta con la conferencia 5, que es la de cotas mínimas.
- La moraleja práctica: $\alpha(n) \le 4$ para cualquier $n$ que quepa en el universo
  observable. En la práctica es constante, y la diferencia con una constante es un
  teorema, no una medición.

### 10. Cierre

- El costo amortizado es una garantía de peor caso sobre secuencias. Vuelve en el
  Tema 2 (estructuras que usan los algoritmos de grafos) y en la conferencia 21, que
  sí tiene probabilidad, para marcar la diferencia.
- Qué potencial tuvo cada estructura, y qué deuda medía.

### 11. Resumen

Viñetas.

### Ejercicios

1. Arreglo dinámico que duplica al llenarse y se reduce a la mitad al quedar a un
   cuarto. Encuentra un potencial y demuestra $O(1)$ amortizado. ¿Por qué reducir
   a la mitad al quedar a la mitad no funciona?
2. Contador binario con incremento y decremento: muestra una secuencia que cuesta
   $\Theta(\log n)$ por operación. ¿Qué cambia si solo se incrementa?
3. Implementa una cola doble (deque) con dos pilas y analízala.
4. Demuestra que en un splay tree, acceder a las $n$ claves en orden cuesta $O(n)$
   con splay (el teorema del acceso secuencial, en una versión débil) y
   $\Theta(n^2)$ con subir a la raíz, desde un camino.
5. Union-find con unión por rango pero olvidando incrementar el rango cuando los dos
   rangos son iguales. ¿Qué cota da? ¿Y si además hay compresión?
6. Demuestra que la unión por tamaño (en vez de rango) también da profundidad
   $O(\log n)$.
7. Calcula $\log^* n$ y $\alpha(n)$ para $n = 2^{16}, 2^{65536}$.
8. Una estructura garantiza $O(1)$ amortizado por operación. Da un ejemplo de
   aplicación donde eso no sirve y hace falta $O(1)$ en el peor caso por operación.

## Audios (tentativo)

| Audio | Secciones | Minutos |
|---|---|---|
| 1 | 1 y 3 | 5 |
| 2 | 2 | 6 |
| 3 | 4 | 5 |
| 4 | 5 | 7 |
| 5 | 6 | 4 |
| 6 | 7 | 4 |
| 7 | 8 | 8 |
| 8 | 9 y 10 | 4 |

Total estimado: 43 minutos.

## Decisiones que quiero confirmar

- **El arreglo dinámico como apertura** (sección 1), antes de la cola del plan. Es
  la estructura amortizada que usan todos los días, y deja la cola para mostrar los
  tres métodos. Se puede quitar y abrir directo con la cola.
- **Tamaños en vez de pesos** en el lema de acceso: $s(x)$ cuenta nodos. El artículo
  usa pesos arbitrarios, que dan más teoremas (optimalidad estática, dedo dinámico),
  pero los pesos unitarios bastan para $O(\log n)$. Menciono que existen.
- **La cota de $\log^*$ se demuestra entera**, la de Ackermann se enuncia. Es lo que
  dice el plan.
- **Por qué falla subir a la raíz (sección 5).** Lo explico leyendo en qué paso de la
  demostración se rompe la desigualdad, y lo mido en la sección 6. No doy una cota
  mínima formal de $\Theta(n)$ para esa heurística, porque es el ejercicio 4.
- **$\alpha(n) \le 4$ "para cualquier $n$ del universo observable"** es la forma
  habitual de decirlo en los libros. Antes de redactar verifico el umbral exacto en
  CLRS y lo dejo como número.

Resueltas el 2026-09-29: todo aprobado como está. El umbral de $\alpha$ no se cita:
las notas lo derivan de la definición ($A_3(1) = 2047$, $A_4(1) > 2^{2048}$).
