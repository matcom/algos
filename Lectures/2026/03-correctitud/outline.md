# Outline: Conferencia 3, demostrar que un algoritmo es correcto

Estado: aprobado y redactado (2026-09-28). Las notas están en `notas.md`.
Destino: `Lectures/2026/03-correctitud/notas.md` + PDF con scriptorium.
Extensión objetivo: 4 800–5 400 palabras, como la conferencia 2. Dos algoritmos con
demostración completa y una variante con error.

## Idea de la clase

La conferencia 2 mostró que una batería de pruebas puede pasar en verde sobre un
algoritmo incorrecto, y que la demostración es la que dice dónde buscar. Esta clase
da las herramientas para escribir esa demostración. Son tres, y cada una responde una
pregunta distinta:

- **Invariante**: qué se mantiene verdadero en cada vuelta. Da la correctitud parcial.
- **Potencial**: qué cantidad decrece en cada vuelta y no puede bajar para siempre.
  Da la terminación.
- **Contradicción sobre el primer fallo**: si el resultado fuera malo, habría un
  primer momento en que algo salió mal, y ese momento es imposible. Da estabilidad y
  optimalidad.

Los dos algoritmos están elegidos porque su correctitud no se ve a simple vista. El
voto mayoritario de Boyer-Moore tiene un invariante que no es el primero que uno
escribe: el primero es verdadero pero no inductivo, y hay que reforzarlo. Gale-Shapley
necesita las tres herramientas en el mismo algoritmo, y además es no determinista: la
demostración tiene que valer para cualquier orden de ejecución.

El hilo que une las secciones es la frase de la conferencia 2, "probar verifica que
implementaste lo que pensaste, no que pensaste bien", pero ahora del lado constructivo:
cómo se escribe la demostración que sí lo verifica.

## Estructura

Cada sección tiene el tamaño de un audio de unos 5 minutos, salvo las marcadas.

### 1. Qué significa "correcto"

- La especificación como contrato: precondición (qué entradas acepta), postcondición
  (qué relación hay entre entrada y salida).
- Correctitud parcial ("si termina, la salida es correcta") y terminación. Correctitud
  total = las dos. Son demostraciones separadas y usan herramientas distintas.
- Las tres herramientas de la clase, enunciadas una vez con nombre propio. Debajo de
  las tres está la inducción de la conferencia 2.
- Conexión con Estructuras de Datos: el invariante de la búsqueda binaria
  ("si el elemento está, está en `[lo, hi)`") ya lo usaban sin nombrarlo.

### 2. El problema de la mayoría

- Enunciado: dado un arreglo de $n$ elementos, devolver el que aparece más de $n/2$
  veces, o decir que no hay ninguno.
- La precisión que cambia todo: los elementos solo se pueden comparar por igualdad.
  No hay orden, así que no se puede ordenar; y si fueran cadenas enormes o registros,
  hashearlos tampoco es gratis. Objetivo: $O(n)$ tiempo y $O(1)$ memoria extra.
- Las soluciones obvias y por qué no alcanzan: contar cada elemento, $\Theta(n^2)$;
  ordenar y tomar el del medio, $O(n \log n)$ y necesita orden; tabla hash, $O(n)$
  memoria.
- **Cómo se le ocurre a uno.** La idea de cancelación: si tacho dos elementos
  distintos, la mayoría sigue siendo mayoría en lo que queda, porque perdió a lo sumo
  uno de los dos. Ejemplo chico a mano con una fila de votos, antes de ver código.

### 3. Boyer-Moore: el algoritmo

- Un candidato y un contador. Si el contador es 0, el elemento actual pasa a ser
  candidato. Si coincide con el candidato, suma; si no, resta. Segunda pasada: contar
  el candidato y verificar que supera $n/2$.
- Traza sobre el ejemplo de la sección 2. **Figura**: la fila de votos con las parejas
  canceladas unidas por un arco y los sobrevivientes marcados.
- Crédito: Boyer y Moore, informe técnico de 1981, publicado en 1991. Lo demostraron
  con su propio demostrador automático de teoremas, que es un detalle que vale la pena
  contar en una clase sobre demostraciones.

### 4. Boyer-Moore: el invariante (sección larga, uno o dos audios)

- **El invariante que uno escribe primero**: "si el prefijo procesado tiene mayoría,
  el candidato es esa mayoría". Es verdadero (es el teorema aplicado al prefijo), pero
  no se puede demostrar por inducción tal como está: la mayoría del prefijo $i+1$ no
  tiene por qué ser la del prefijo $i$, y la hipótesis no dice nada útil cuando el
  prefijo no tiene mayoría. Lección: un invariante tiene que ser **inductivo**, no solo
  verdadero, y a veces hay que reforzarlo para que lo sea.
- **El invariante reforzado**: el prefijo procesado se puede partir en parejas de
  elementos distintos más $c$ copias del candidato, donde $c$ es el contador. Es la
  idea de cancelación de la sección 2, escrita como invariante.
- Demostración de las tres partes: inicialización ($c=0$, prefijo vacío),
  mantenimiento (tres casos: $c=0$, coincide, no coincide y se empareja con una copia),
  y conclusión.
- La conclusión: si $m$ es mayoría y el candidato final no es $m$, entonces $m$ solo
  aparece en las parejas, a lo sumo una vez en cada una, o sea a lo sumo
  $(n-c)/2 \le n/2$ veces. Contradicción. Por tanto, **si hay mayoría, es el
  candidato**.
- Complejidad: dos pasadas, $O(n)$ tiempo, $O(1)$ memoria. Cota mínima trivial: todo
  algoritmo tiene que leer cada elemento, porque cambiar uno solo puede cambiar la
  respuesta. Es óptimo.

### 5. El error que la demostración anuncia

- La variante con el atajo: saltarse la segunda pasada y devolver el candidato si el
  contador final es positivo, o "no hay mayoría" si es 0.
- La mitad es correcta. Si hay mayoría, el contador final no puede ser 0 (la cuenta de
  la sección 4 lo prueba). Así que $c = 0$ implica "no hay mayoría". Lo falso es la
  recíproca: $c > 0$ no implica mayoría. Contraejemplo mínimo: `[a, b, c]` termina con
  candidato `c` y contador 1.
- **Código ejecutable**: las dos versiones contra un oráculo por fuerza bruta, con tres
  generadores de pruebas:
  - Arreglos con una mayoría plantada, que es el generador que casi todo el mundo
    escribe: el atajo pasa todas.
  - Arreglos aleatorios sobre un alfabeto de dos símbolos: el atajo pasa todas. Con dos
    símbolos el contador final es exactamente la diferencia entre las dos cuentas, y el
    atajo nunca se equivoca (verificado por enumeración para $n \le 12$).
  - Arreglos aleatorios sobre tres o más símbolos: falla en una fracción grande
    (entre 7 % y 72 % según $n$, medido por enumeración).
- La moraleja, que conecta con la conferencia 2: aquí las pruebas sí atrapan el error,
  pero solo si alguien prueba el caso "no hay mayoría". La demostración dice que ese
  caso existe, porque su conclusión arranca con "si hay mayoría". Leer la hipótesis de
  un teorema es leer la lista de casos que hay que probar.

### 6. El emparejamiento estable

- Enunciado: $n$ proponentes y $n$ receptores, cada uno con una lista de preferencias
  estricta y completa sobre el otro lado. Un emparejamiento perfecto es **inestable** si
  hay un proponente $a$ y un receptor $b$, no emparejados entre sí, que se prefieren
  mutuamente antes que a sus parejas. Buscamos uno estable.
- Que exista no es obvio. Con un solo grupo (el problema de los compañeros de cuarto)
  hay entradas de cuatro personas sin emparejamiento estable. Queda como ejercicio, pero
  se menciona aquí para que la existencia se vea como algo que hay que demostrar.
- Motivación real: la asignación de residentes a hospitales en Estados Unidos usa este
  esquema desde los años 50; Gale y Shapley lo publicaron en 1962, y Roth y Shapley
  recibieron el Nobel de Economía en 2012.
- **Cómo se le ocurre a uno.** El primer intento es reparar: mientras haya una pareja
  inestable, emparejarlos a ellos dos y dejar solos a sus ex. Esa reparación local
  puede ciclar para siempre (Knuth, 1976; se da un ejemplo en el ejercicio 6). La
  terminación no es gratis, y eso motiva un algoritmo donde algo avance siempre en la
  misma dirección.
- **Figura**: una instancia $3 \times 3$ con las listas y un emparejamiento inestable,
  con la pareja que lo bloquea marcada.

### 7. Gale-Shapley: el algoritmo y su terminación

- El algoritmo de aceptación diferida: mientras haya un proponente libre que no le ha
  propuesto a todos, le propone al mejor receptor de su lista al que todavía no le ha
  propuesto. El receptor acepta si está libre o si prefiere al nuevo; si cambia, deja
  libre al anterior.
- Es no determinista: no dice qué proponente libre va primero. Todo lo que se demuestre
  tiene que valer para cualquier elección.
- Dos invariantes de monotonía, cada uno de una línea:
  - Un receptor, una vez comprometido, no vuelve a quedar libre, y su pareja solo
    mejora.
  - Un proponente propone en orden decreciente de preferencia, así que sus parejas solo
    empeoran.
- **Terminación por potencial**: el número de pares $(a, b)$ tales que $a$ todavía no
  le ha propuesto a $b$. Empieza en $n^2$, baja en 1 con cada propuesta y nunca es
  negativo. A lo sumo $n^2$ iteraciones.
- **Termina con un emparejamiento perfecto**: si al final hubiera un proponente libre,
  le habría propuesto a todos; por el primer invariante los $n$ receptores estarían
  comprometidos, con $n$ proponentes distintos, pero solo quedan $n-1$. Contradicción.
- Conexión hacia adelante: la conferencia 4 usa la palabra "potencial" para otra cosa,
  pagar costo amortizado. Es la misma idea de una cantidad que se mueve en una sola
  dirección.

### 8. Gale-Shapley: estabilidad

- Por contradicción, en un párrafo. Si $(a, b)$ bloquea el resultado, $a$ prefiere $b$
  a su pareja final, así que le propuso a $b$ antes. En algún momento $b$ rechazó a
  $a$ por alguien mejor, y por el primer invariante la pareja final de $b$ es al menos
  tan buena como ese. Entonces $b$ no prefiere a $a$. Contradicción.
- Corolario: todo mercado bipartito con listas completas y estrictas tiene un
  emparejamiento estable. El algoritmo es la demostración de existencia.
- **Código ejecutable**: Gale-Shapley con la tabla de rangos inversa, un verificador
  de estabilidad por fuerza bruta ($O(n^2)$ pares), y miles de instancias aleatorias
  sin ninguna pareja bloqueante. Conteo de propuestas contra la cota $n^2$.

### 9. Gale-Shapley: optimalidad para quien propone (sección larga)

- La pregunta: hay muchos emparejamientos estables. ¿Cuál devuelve el algoritmo, y
  depende del orden en que se elijan los proponentes?
- Definición: $b$ es **pareja válida** de $a$ si existe algún emparejamiento estable
  donde están juntos. $\text{mejor}(a)$ es la mejor pareja válida de $a$.
- **Teorema**: el algoritmo empareja a cada $a$ con $\text{mejor}(a)$, sin importar el
  orden de ejecución.
- **Demostración por el primer rechazo.** Supongamos que en alguna ejecución algún
  proponente es rechazado por una pareja válida. Tomemos el primer rechazo de ese tipo:
  $b$ rechaza a $a$ en favor de $a'$, y existe un estable $M'$ con $(a, b)$. En $M'$,
  $a'$ está con algún $b'$. En el momento del rechazo, $a'$ todavía no había sido
  rechazado por ninguna pareja válida, porque este es el primer rechazo así. Como $a'$
  propone en orden, $a'$ prefiere $b$ a $b'$. Y $b$ prefiere $a'$ a $a$. Entonces
  $(a', b)$ bloquea a $M'$, que era estable. Contradicción.
- La técnica tiene nombre en el resto del curso: tomar el primer (o el menor)
  contraejemplo y mostrar que no puede existir. Vuelve en los algoritmos golosos.
- Corolarios: el resultado no depende del orden de ejecución; y es el peor posible para
  los receptores (ejercicio 5).
- **Código ejecutable**: el mismo conjunto de instancias corrido con órdenes de
  ejecución distintos (cola, pila, aleatorio) da siempre el mismo emparejamiento; y
  enumerando todos los emparejamientos estables en instancias chicas, el de
  Gale-Shapley es el mejor para cada proponente.
- Una observación que no es técnica: quién propone decide quién gana. En la asignación
  de residentes el cambio de que propusieran los residentes en vez de los hospitales
  fue una decisión de diseño con consecuencias reales (1998).

### 10. Complejidad y cota mínima (sección corta)

- $O(n^2)$ con dos estructuras: un puntero por proponente al siguiente receptor de su
  lista, y una tabla `rango[b][a]` para que cada receptor compare dos pretendientes en
  $O(1)$. Sin la tabla, cada comparación cuesta $O(n)$ y el total sube a $O(n^3)$.
  Otra vez, como en la conferencia 2, la idea es la misma y el costo lo decide la
  implementación.
- La entrada mide $2n^2$, así que el algoritmo es lineal en el tamaño de la entrada.
- Cota mínima: Ng y Hirschberg (1990) demostraron que encontrar un emparejamiento
  estable requiere $\Omega(n^2)$ consultas a las listas en el peor caso. Se cita sin
  demostrar. Gale-Shapley es óptimo en ese modelo.

### 11. Qué atrapa cada herramienta

- Tabla de cierre: qué pregunta responde cada herramienta, dónde apareció hoy y qué
  error atrapa.
  - Invariante: correctitud parcial; atrapa el atajo de Boyer-Moore porque su
    conclusión tiene una hipótesis.
  - Potencial: terminación; atrapa la reparación local que cicla.
  - Primer fallo: estabilidad y optimalidad; atrapa la idea de que el resultado
    depende del orden.
- Hacia adelante: conferencia 4 (potencial para costo amortizado), Tema 2 (el primer
  contraejemplo en los argumentos de intercambio de los golosos).

### 12. Resumen

Viñetas, una por idea que hay que recordar.

### Ejercicios

1. Traza Boyer-Moore sobre un arreglo dado y escribe la partición en parejas y
   sobrevivientes que promete el invariante en cada paso.
2. Misra-Gries: generaliza Boyer-Moore para encontrar todos los elementos que aparecen
   más de $n/k$ veces usando $k-1$ contadores. Enuncia el invariante y demuéstralo.
3. Demuestra que con un alfabeto de dos símbolos el contador final de Boyer-Moore es la
   diferencia entre las dos cuentas, y que por tanto el atajo de la sección 5 nunca se
   equivoca.
4. Compañeros de cuarto: exhibe cuatro personas con preferencias tales que no existe
   emparejamiento estable. Di qué paso de la demostración de la sección 8 deja de valer
   cuando hay un solo grupo.
5. Demuestra que Gale-Shapley le da a cada receptor su **peor** pareja válida.
6. Construye una instancia en la que la reparación local de parejas inestables de la
   sección 6 cicla.
7. Una búsqueda binaria con `lo = mid` en lugar de `lo = mid + 1`: encuentra una
   entrada donde no termina y di cuál es el potencial que deja de decrecer.
8. Un proponente miente sobre sus preferencias. ¿Puede conseguir una pareja mejor que
   la que le da Gale-Shapley con su lista verdadera? ¿Y un receptor?

## Audios (para el guion de grabación)

| Audio | Secciones | Minutos |
|---|---|---|
| 1 | 1 | 4 |
| 2 | 2 y 3 | 5 |
| 3 | 4, el invariante que no funciona y el reforzado | 5 |
| 4 | 4, la conclusión, y 5 | 6 |
| 5 | 6 | 5 |
| 6 | 7 | 5 |
| 7 | 8 y 9 | 7 |
| 8 | 10, 11 y cierre | 4 |

Total estimado: 40 minutos, al ritmo de la conferencia 2.

## Decisiones que quiero confirmar

- **La sección 9 completa en la clase.** La optimalidad es la demostración más difícil
  y la que más muestra la técnica del primer fallo. La alternativa es enunciarla en el
  audio y dejar la demostración como lectura, como hiciste con el algoritmo aleatorio
  de la conferencia 2. Las notas la llevan completa en cualquier caso.
- **Proponentes y receptores**, en vez de hombres y mujeres (Gale-Shapley) o residentes
  y hospitales (el caso real, que además tiene cupos). Uso los nombres abstractos y
  menciono los residentes como motivación.
- **Sin cota de memoria para una sola pasada.** Hay resultados de streaming que dicen
  que decidir si existe mayoría en una sola pasada necesita memoria lineal, lo que
  justificaría la segunda pasada. No lo he verificado contra una fuente primaria, así
  que no entra salvo que lo quieras y lo busque.
- **La historia del cambio de 1998** en la asignación de residentes (sección 9) la
  quiero verificar contra fuente antes de redactar. Si no aparece una fuente primaria,
  se cae.

Resueltas el 2026-09-28: todo aprobado como está. Las dos afirmaciones sin fuente
(memoria de una sola pasada y el cambio de 1998) quedaron fuera de las notas.
