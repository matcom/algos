# Outline: Capítulo 13, flujo máximo con Dinic

Estado: redactado (2026-11-13) por el workflow del libro, pendiente de revisión.
Destino: `Lectures/2026/13-dinic/notas.md`, en formato de libro.
Extensión objetivo: 5 500–7 000 palabras con el código.
Verificación: `.playground/libro-daa/verif/13/` (`flujo.py` es el núcleo;
`v1_oraculo.py`, `v2_ejemplo.py`, `v3_fases.py`, `v4_escalera.py`, `v5_ejercicios.py`
y `capitulo.py`, que es el código del capítulo antes de pasarlo a las notas).

## Idea del capítulo

El capítulo 10, §10, dejó el emparejamiento bipartito como intersección de dos matroides
y mostró que el goloso solo garantiza la mitad. Aquí se resuelve exacto, como caso
particular de un problema más general: el flujo máximo en una red.

El hilo es el ciclo de siempre, con un giro. El intento natural (empujar flujo por
caminos mientras quepa) se atasca, y lo que falta es poder **deshacer**: la red residual.
Con ella, Ford-Fulkerson es correcto, y la demostración de correctitud es el teorema
Max-Flow Min-Cut, que además da el certificado de optimalidad: un corte con la misma
capacidad. El costo es el problema: el número de aumentos depende de las capacidades.
Dinic lo arregla trabajando por fases sobre el grafo de niveles, y la cota $O(V^2 E)$
sale de un solo invariante: la distancia de $s$ a $t$ en la residual sube en cada fase.

El error plantado ataca justo ese invariante. Una línea del recorrido en profundidad
(avanzar el puntero de arista actual también después de un empuje parcial) deja el
valor del flujo siempre correcto, pero el flujo de la fase deja de ser bloqueante. Las
pruebas contra el oráculo no lo ven nunca; un `assert` sobre la distancia lo ve en
280 de las 1 000 redes de la batería del capítulo (en `v1_oraculo.py`, 332 de 3 000 redes al azar), y una familia construida le saca $k^2$ fases
donde Dinic hace una.

## Estructura

### 1. Redes y flujos

- Red: grafo dirigido, capacidades enteras no negativas, fuente $s$ y sumidero $t$.
  Flujo: capacidad y conservación. Valor $|f|$.
- El ejemplo del capítulo, con seis vértices $s, a, b, c, d, t$ y ocho aristas:
  $s{\to}a$ 3, $s{\to}b$ 9, $b{\to}a$ 2, $a{\to}c$ 3, $a{\to}d$ 9, $b{\to}c$ 9,
  $c{\to}t$ 4, $d{\to}t$ 7. Salió de una búsqueda (`v2_ejemplo.py`) con cuatro
  condiciones: el goloso se atasca, Dinic hace tres fases, una fase usa una arista
  inversa y el corte mínimo no es trivial.
- Conexión hacia atrás: capítulo 10, §10 (emparejamiento como dos matroides).

### 2. El goloso que se atasca

- Cómo se le ocurre a uno: buscar un camino de $s$ a $t$ con capacidad sobrante,
  empujar el mínimo, repetir. Código: `ford_fulkerson(..., inversas=False)` con BFS.
- En el ejemplo: $s a c t$ (3), $s b c t$ (1), $s b a d t$ (2), valor 6, y ningún camino
  más. Hay un flujo de valor 9 (el que da la §4), que el código comprueba válido.
- El goloso no se equivoca en un camino: se equivoca en no poder retirar los 3 que
  mandó por $a{\to}c$.

### 3. La red residual

- Definición: por cada arista $(u, v)$, residual hacia adelante $c - f$ y hacia atrás
  $f$. Empujar por la inversa es deshacer.
- La representación del código: cada arista y su gemela en posiciones $2i$ y $2i+1$,
  la gemela de `e` es `e ^ 1`. El flujo de la arista $i$ es `cap[2i+1]`.
- **Figura 1**: el flujo de valor 6 del goloso y su red residual, con el camino
  $s b c a d t$ que usa la inversa $c{\to}a$.

### 4. Ford-Fulkerson

- El mismo código con `inversas=True`: cuatro aumentos y valor 9. El cuarto es
  $s b c a d t$ por 3.
- Terminación con capacidades enteras: cada aumento sube el valor en al menos 1, y el
  valor está acotado por la suma de las capacidades que salen de $s$. Integralidad:
  todos los flujos intermedios son enteros. Las dos cosas se demuestran en la sección.
- El número de aumentos puede depender de las capacidades: el ejercicio 3.

### 5. Cortes

- Corte $(S, T)$ con $s \in S$, $t \in T$; capacidad $c(S, T)$.
- **Lema 1**: $|f| = f(S, T) - f(T, S)$ para todo corte, sumando la conservación sobre
  $S$. **Lema 2**: $|f| \le c(S, T)$.
- Código: el oráculo de fuerza bruta (los $2^{V-2}$ lados de $s$). En el ejemplo, 9.

### 6. Max-Flow Min-Cut

- **Teorema** (Ford y Fulkerson, 1956). Equivalen: (1) $f$ es máximo; (2) no hay
  camino de $s$ a $t$ en la residual; (3) $|f| = c(S, T)$ para algún corte. Demostración
  completa de las tres implicaciones; el paso que todo el mundo se salta es que las
  aristas de $T$ a $S$ llevan flujo 0 (si no, su inversa estaría en la residual y el
  extremo en $T$ sería alcanzable).
- Corolario: Ford-Fulkerson es correcto, y el lado $S$ se lee de la residual final.
- **Figura 3**: el corte mínimo $S = \{s, b, c\}$ con sus tres aristas saturadas
  ($s{\to}a$ 3, $b{\to}a$ 2, $c{\to}t$ 4) y la arista $a{\to}c$, de $T$ a $S$, con
  flujo 0. Va aquí y no al final porque es la demostración hecha dibujo.

### 7. Caminos más cortos y grafo de niveles

- La búsqueda en anchura que usamos es Edmonds-Karp (1972). Lo que cambia con Dinic:
  calcular las distancias una vez y empujar por todos los caminos más cortos.
- Grafo de niveles: aristas residuales con $\ell(v) = \ell(u) + 1$. Flujo bloqueante:
  todo camino de $s$ a $t$ en el grafo de niveles tiene una arista saturada.
- **Figura 2**: el grafo de niveles de la fase 1 del ejemplo y su flujo bloqueante de
  valor 4 ($s a c t$ 3, $s b c t$ 1). El grafo de niveles admite 7, así que
  bloqueante no es máximo, y no hace falta que lo sea.

### 8. Dinic

- Código: BFS de niveles y DFS con puntero de arista actual `it[u]`. Una fase termina
  cuando la DFS desde $s$ devuelve 0.
- Traza en el ejemplo: fases de distancia 3, 4 y 5 con 4, 2 y 3.
- Oráculo: 500 redes al azar de 4 a 8 vértices y 500 en capas contra el corte de fuerza bruta. El goloso falla en 0 de las al azar y en 34 de las en capas: la uniforme casi nunca lo atasca.
- Conexión: la versión que se enseña como "algoritmo de Dinic" es la modificación de
  Shimon Even y Alon Itai (Dinitz, 2006). El original: Dinitz, Doklady 1970.

### 9. La distancia sube en cada fase

- Experimento primero: un `assert` de que las distancias de las fases crecen
  estrictamente, sobre las mismas redes.
- **Lema 3**: durante una fase toda arista residual cumple $\ell(v) \le \ell(u) + 1$
  (las nuevas son inversas de aristas de nivel y bajan un nivel). Al final de la fase
  todo camino de $s$ a $t$ tiene al menos $d + 1$ aristas. El paso clave: una arista con
  $\ell(v) = \ell(u) + 1$ en la residual nueva es del grafo de niveles y no saturada;
  si el camino solo tuviera esas, el flujo no era bloqueante.
- Consecuencia: a lo sumo $V - 1$ fases.

### 10. El error plantado: avanzar el puntero de más

- La variante: `it[u] += 1` también después de un empuje que no saturó la arista.
  Parece inofensiva, porque la arista "ya se usó".
- Medición (`v1_oraculo.py`, 3 000 redes): el valor es correcto en todas, la distancia
  deja de crecer en 332, y en 1 hay más de $V - 1$ fases. En el capítulo, con el número
  de redes que se corra ahí.
- Por qué el valor nunca falla: la variante sigue siendo Ford-Fulkerson con caminos más
  cortos, y termina solo cuando no hay camino. Lo que se rompe es la palabra
  "bloqueante" del Lema 3.
- Familia construida (`v3_fases.py`): $s{\to}a$ con $k^2$, $a{\to}b_i$ con $k$,
  $b_i{\to}c_j$ con 1, $c_j{\to}t$ con $k$. Dinic: 1 fase. La variante: $k^2$ fases
  (4, 16, 64, 256 para $k = 2, 4, 8, 16$), con $V = 2k + 3$.

### 11. El costo de una fase

- **Lema 4**: una fase cuesta $O(VE)$. Cada aumento satura al menos una arista del
  grafo de niveles, que no vuelve a tener capacidad en la fase (su inversa baja un
  nivel), así que hay a lo sumo $E$ aumentos de a lo sumo $V - 1$ pasos. Los pasos que
  no llegan a $t$ terminan en un retroceso que avanza un puntero, y los punteros
  avanzan a lo sumo $E$ veces en total. Con la BFS, $O(VE)$.
- **Teorema**: Dinic cuesta $O(V^2 E)$.
- Edmonds-Karp como corolario del Lema 3: mientras la distancia vale $d$, todo camino
  más corto vive en el grafo de niveles de cuando la distancia llegó a $d$, y cada
  aumento satura una de sus aristas para siempre. $O(VE)$ aumentos, $O(VE^2)$.

### 12. Capacidades unitarias y Hopcroft-Karp

- Red unitaria: capacidades 1, sin aristas antiparalelas, y cada vértice distinto de
  $s$ y $t$ tiene una sola arista de entrada o una sola de salida. La red del
  emparejamiento bipartito lo es.
- **Lema 5**: la residual de una red unitaria es unitaria (demostración por casos sobre
  si pasa flujo por el vértice).
- **Lema 6**: la capacidad residual de un corte es $c(S,T) - |f|$, así que lo que falta
  por enviar es $|f^*| - |f|$. Descomposición de un flujo entero en caminos; en una red
  unitaria, caminos sin vértices internos comunes.
- **Teorema**: Dinic sobre una red unitaria hace a lo sumo $2\sqrt{V} + 1$ fases, cada
  una en $O(E)$: $O(E\sqrt{V})$. Con $p = \lceil \sqrt V \rceil$ fases la distancia es
  al menos $p + 1$, quedan a lo sumo $V/p$ caminos, y cada fase suma al menos 1.
- El emparejamiento bipartito por Dinic es el algoritmo de Hopcroft y Karp (1973).
  Código: emparejamiento con oráculo de fuerza bruta en grafos chicos.
- Medición (`v4_escalera.py`): la familia escalera (caminos con $m = 1, \dots, k$
  aristas de emparejamiento, en un orden que deja libre el extremo) hace $k$ fases con
  $V = k^2 + k + 2$: la cota se alcanza hasta un factor 2. Medido $k = 2, \dots, 32$.
- Sin la condición de grado: capacidades unitarias en general dan $O(E \sqrt E)$
  (ejercicio 5) y $O(V^{2/3} E)$ (Even y Tarjan, 1975, sin demostración aquí).

### 13. La regla

- Una cota de costo que sale de un invariante se prueba con el invariante, no con la
  salida. La salida de las dos versiones de la §10 es idéntica.
- Hacia adelante: el capítulo 14 cambia de idea (preflujos) con la misma cota; el
  capítulo 15 contrasta el corte $s$-$t$ con el corte global de Karger; el epílogo trae
  el flujo en tiempo casi lineal (Chen, Kyng, Liu, Peng, Probst Gutenberg y Sachdeva,
  FOCS 2022; JACM 2025). Orlin (STOC 2013) da $O(VE)$.

### Resumen

### Ejercicios

1. [traza] Dinic a mano sobre la red de 6 vértices
   $s{\to}a$ 4, $s{\to}b$ 8, $b{\to}a$ 1, $a{\to}c$ 4, $a{\to}d$ 2, $b{\to}c$ 7,
   $c{\to}t$ 9, $d{\to}t$ 9, $d{\to}b$ 2, en el orden de la lista. Después, el corte
   mínimo leído de la residual final. (Verificado: fases de distancia 3, 4, 5 con 9,
   1, 1; valor 11; $S = \{s, a, b, c\}$.)
2. [traza] Hopcroft-Karp sobre $x_0{:}\{y_2, y_3, y_4\}$, $x_1{:}\{y_1, y_2, y_3\}$,
   $x_2{:}\{y_2\}$, $x_3{:}\{y_1\}$, $x_4{:}\{y_2\}$. Fases y emparejamiento; leer de la
   residual un cubrimiento por vértices del mismo tamaño y demostrar que lo es (König).
   (Verificado: fases 3, 5, 7 con 2, 1, 1; tamaño 4; cubrimiento
   $\{x_0, x_1, x_3, y_2\}$.)
3. [entrada que rompe] El diamante con capacidades $C$ y la arista central 1: una
   elección de caminos que hace $2C$ aumentos. (Verificado para $C = 1, 5, 100$.) ¿Y
   con BFS?
4. [demostración] Edmonds-Karp por aristas críticas: cada arista es crítica a lo sumo
   $V/2$ veces. Otra demostración de $O(VE)$ aumentos, sin fases.
5. [demostración] ★ Capacidades 1 sin la condición de grado y sin antiparalelas: a lo
   sumo $2\sqrt{E}$ fases.
6. [demostración] Menger por desdoblamiento de vértices.
7. [modelar] Flujo con cotas inferiores reducido a flujo máximo.
8. [modelar] Selección de proyectos con ganancias y prerrequisitos como corte mínimo.
9. [cambio de hipótesis] Capacidades reales: qué demostraciones usan enteros y cuáles
   no; Dinic termina, la §4 no alcanza para Ford-Fulkerson.
10. [implementar y medir] Edmonds-Karp contra Dinic en redes al azar y en redes de
    capas, contando aristas examinadas.

## Audios (tentativo)

| Audio | Secciones | Minutos |
|---|---|---|
| 1 | 1 y 2 | 5 |
| 2 | 3 y 4 | 6 |
| 3 | 5 y 6 | 7 |
| 4 | 7 y 8 | 6 |
| 5 | 9 | 5 |
| 6 | 10 | 5 |
| 7 | 11 | 5 |
| 8 | 12 | 7 |
| 9 | 13 | 2 |

Total estimado: 48 minutos.

## Decisiones que quiero confirmar

- **$O(E\sqrt V)$ solo para redes unitarias.** El plan dice "redes de capacidad unitaria
  en $O(E\sqrt V)$". Eso es falso en general (error 1 de la guía): con capacidades 1 y
  sin la condición de grado, Even y Tarjan (1975) dan $O(V^{2/3} E)$ y el argumento de
  fases da $O(E\sqrt E)$; su resumen dice además que esas cotas son ajustadas para Dinic.
  El capítulo da $O(E\sqrt V)$ para la red con un solo arco de entrada o de salida por
  vértice, que es el caso bipartito, y deja $\sqrt{E}$ como ejercicio.
- **Semilla 4 cambiada.** "Demuestra que la distancia nunca baja y sube tras cada fase"
  es el Lema 3 del cuerpo. El ejercicio 4 pasa a la demostración de Edmonds-Karp por
  aristas críticas.
- **Semillas 2 y 7 fundidas, y una de modelar menos.** La guía pide 1 o 2 de modelar y
  las semillas traían cuatro. El corte del ejercicio 1 entra como su segunda parte;
  Hopcroft-Karp sobre una instancia pasa a traza con König; Menger pasa a demostración.
  Entra un ejercicio de cambio de hipótesis (capacidades reales), que faltaba.
- **Mediciones por conteo, no por tiempo.** Fases, aumentos y pasos son exactos y no
  dependen de la carga de la máquina.
- **Citas verificadas** (Crossref y Math-Net): Ford y Fulkerson, *Canadian J. Math.* 8
  (1956); Dinitz, *Doklady Akademii Nauk SSSR* 194(4) (1970); Edmonds y Karp, *J. ACM*
  19(2) (1972); Hopcroft y Karp, *SIAM J. Comput.* 2(4) (1973); Even y Tarjan, *SIAM J.
  Comput.* 4(4) (1975), resumen leído; Dinitz, LNCS 3895 (2006), resumen leído; Orlin,
  STOC 2013; Chen y otros, FOCS 2022 y *J. ACM* 72(3) (2025); Menger, *Fundamenta
  Mathematicae* 10 (1927). No entra: Elias, Feinstein y Shannon (1956), Karzanov (1973)
  y la atribución exacta del puntero de arista actual, que no verifiqué.
