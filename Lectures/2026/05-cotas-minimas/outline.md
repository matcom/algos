# Outline: Conferencia 5, cotas mínimas

Estado: aprobado y redactado (2026-09-29). El documento está en `notas.md`.
Destino: `Lectures/2026/05-cotas-minimas/notas.md` + PDF con scriptorium.
Extensión objetivo: 5 000–6 000 palabras.

## Idea de la clase

La conferencia 2 cambió una vez la pregunta, de "cuánto cuesta este algoritmo" a
"cuánto cuesta cualquiera", y la respondió con una reducción desde un teorema que
citamos sin demostrar (Ben-Or). Esta clase da las herramientas para demostrar cotas
mínimas uno mismo, en el modelo de comparaciones, que es el más simple donde se puede
hacer todo con papel y lápiz.

Son dos herramientas y cada una tiene su límite:

- **Información**: un algoritmo de comparaciones es un árbol de decisión, y un árbol
  con $L$ hojas tiene altura al menos $\log_2 L$. Da la cota de ordenamiento, pero para
  el máximo da $\log_2 n$ cuando la verdad es $n - 1$.
- **Adversario**: un oponente que responde las comparaciones para que el algoritmo
  sepa lo menos posible. Da las cotas exactas de mezclar ($2n - 1$), del máximo
  ($n - 1$) y del segundo mayor ($n + \lceil \log_2 n \rceil - 2$).

La tercera herramienta, la reducción, ya la vimos en la conferencia 2, y es la que
domina el Tema 3.

El error plantado de esta clase cambia de lado. En las conferencias 2 a 4 la
demostración anunciaba el error de un algoritmo. Aquí la **cota mínima** lo detecta:
un algoritmo que usa menos comparaciones que una cota demostrada tiene que estar mal, y
la demostración del adversario dice en qué entrada.

## Estructura

### 1. De este algoritmo a cualquier algoritmo

- Qué hay que fijar para hablar de todos los algoritmos: el modelo. Aquí, el modelo de
  comparaciones: el algoritmo solo accede a los datos preguntando si $a_i < a_j$, y el
  costo es el número de preguntas.
- Recordatorio de la conferencia 2 (Ben-Or y la rejilla): una cota vale en su modelo.
  La sección 9 vuelve sobre esto.
- Las tres herramientas, con nombre: información, adversario y reducción.
- Conexión con Estructuras de Datos: la cota $\Omega(n \log n)$ de ordenamiento ya la
  vieron enunciada. Hoy se demuestra, y se ve hasta dónde llega la técnica.

### 2. Árboles de decisión

- Un algoritmo de comparaciones sobre entradas de tamaño $n$ es un árbol binario: cada
  nodo interno es una comparación, cada hoja una respuesta. El costo en el peor caso es
  la altura.
- **Figura**: el árbol de decisión de ordenamiento por inserción para $n = 3$, generado
  corriendo el algoritmo sobre las seis permutaciones y registrando las comparaciones.
  Tiene seis hojas y altura 3.
- Cómo se le ocurre a uno: el árbol es la lista de todas las ejecuciones posibles del
  algoritmo, pegadas por donde coinciden.

### 3. El argumento de información

- Un árbol binario de altura $h$ tiene a lo sumo $2^h$ hojas. Si el problema tiene $L$
  respuestas posibles que el algoritmo tiene que distinguir, $h \ge \log_2 L$.
- **Ordenamiento**: $L = n!$, así que $h \ge \log_2 n! \ge n \log_2 n - n \log_2 e$.
  Demostración de la segunda desigualdad sin Stirling, acotando la suma de logaritmos
  con una integral.
- **Código ejecutable**: el peor caso exacto de mergesort, contando comparaciones sobre
  todas las permutaciones para $n \le 8$ y sobre muestras para $n$ mayores, contra
  $\lceil \log_2 n! \rceil$. La diferencia es pequeña y es de orden lineal.
- Búsqueda en arreglo ordenado: $L = n + 1$ respuestas (las $n$ posiciones o "no
  está"), así que $\lceil \log_2 (n + 1) \rceil$, que la búsqueda binaria alcanza.

### 4. Cuándo la información no alcanza

- **Máximo**: hay $n$ respuestas posibles, y la información da $\log_2 n$. Todo el
  mundo sabe que hacen falta $n - 1$ comparaciones, pero el árbol no lo ve: cuenta
  respuestas, no el trabajo de descartar a los demás.
- **Mezclar dos listas ordenadas de largo $n$**: hay $\binom{2n}{n}$ resultados, y
  $\log_2 \binom{2n}{n} = 2n - \frac{1}{2}\log_2 n - O(1)$. Queda cerca de $2n - 1$
  pero no llega.
- **Segundo mayor**: $n(n-1)$ respuestas, cota de información $2 \log_2 n$. Muy lejos
  de la verdad.
- Moraleja: el argumento de información es una cota por el tamaño de la salida. Cuando
  el trabajo está en verificar y no en elegir, hace falta otra herramienta.

### 5. El adversario

- La idea: el algoritmo hace preguntas y un adversario las contesta. El adversario no
  tiene una entrada fija: solo tiene que contestar de forma consistente con **alguna**
  entrada. Si al final quedan dos entradas consistentes con respuestas distintas, el
  algoritmo no puede haber terminado.
- **El máximo, $n - 1$**: para certificar que $m$ es el máximo, cada uno de los otros
  $n - 1$ elementos tiene que haber perdido al menos una comparación, y cada
  comparación hace perder a lo sumo a uno que nunca había perdido. El adversario no
  necesita ninguna astucia aquí.
- Conexión con la conferencia 3: el adversario es un argumento por contradicción sobre
  todas las ejecuciones a la vez.

### 6. Mezclar: $2n - 1$

- El algoritmo de mezcla usa a lo sumo $2n - 1$ comparaciones.
- **El adversario**: responde como si la entrada fuera la intercalada perfecta
  $a_1 < b_1 < a_2 < b_2 < \dots < a_n < b_n$. Cada par vecino de esa cadena, que son
  $2n - 1$ pares, tiene que compararse: si un algoritmo no compara $a_i$ con $b_i$,
  intercambiarlos da otra entrada consistente con todas las respuestas y con un
  resultado distinto.
- **Figura**: la cadena intercalada con los $2n - 1$ pares forzados marcados.
- **Código ejecutable**: la mezcla sobre la entrada intercalada usa exactamente
  $2n - 1$. Es también el problema 8-6 de CLRS.

### 7. El segundo mayor: $n + \lceil \log_2 n \rceil - 2$ (sección larga)

- **El torneo**: los elementos juegan por parejas, los ganadores pasan de ronda, y el
  máximo sale en $n - 1$ comparaciones. El segundo mayor perdió contra el máximo en
  algún momento, así que está entre los que el máximo venció, que son a lo sumo
  $\lceil \log_2 n \rceil$. Su máximo cuesta $\lceil \log_2 n \rceil - 1$ más.
- **Figura**: el cuadro del torneo sobre una instancia real, con el camino del máximo
  y sus rivales marcados.
- **La cota mínima, por adversario.** Cualquier algoritmo tiene que hacer perder a
  $n - 1$ elementos (para saber el máximo), y además cada rival directo del máximo,
  salvo el segundo, tiene que perder contra alguien más. Si el máximo fue comparado con
  $k$ elementos, eso son al menos $n - 1 + k - 1$ comparaciones. El adversario obliga a
  $k \ge \lceil \log_2 n \rceil$ con una estrategia de pesos: cada elemento empieza con
  peso 1, gana la comparación el de mayor peso, y el ganador absorbe el peso del
  perdedor. El peso del máximo a lo sumo se duplica en cada comparación y al final vale
  $n$.
- **Código ejecutable**: el torneo contado sobre entradas aleatorias. Medido en
  `.playground`: el peor caso observado es exactamente la cota (9, 68 y 1032 para
  $n = 8, 64, 1024$).

### 8. La cota mínima como detector de errores

- El error plantado: un torneo que "ahorra" una comparación saltándose al rival de la
  primera ronda del máximo. Usa $n + \lceil \log_2 n \rceil - 3$ comparaciones, una
  menos que la cota.
- La cota dice que tiene que estar mal, sin mirar el código. La demostración dice
  dónde: en la entrada en que el segundo mayor es justo ese rival.
- **Código ejecutable**: medido en `.playground`, falla con probabilidad $1/(n-1)$: el
  14,6 % de las entradas para $n = 8$, el 1,6 % para $n = 64$ y el 0,07 % para
  $n = 1024$. Una batería de pruebas al azar con arreglos grandes no lo ve casi nunca.
- La moraleja cierra la serie de errores plantados del tema: una cota mínima es
  también una especificación. Un algoritmo más rápido que una cota demostrada está
  mal, aunque pase todas las pruebas.

### 9. Qué modelo (sección corta)

- El ordenamiento por conteo ordena $n$ enteros en $[0, k)$ en $O(n + k)$, por debajo
  de $n \log n$ cuando $k = O(n)$. No compara: usa los valores como índices, el mismo
  truco que la rejilla de la conferencia 2.
- **Código ejecutable**: conteo contra el `sorted` de Python en enteros pequeños.
- La regla de la conferencia 2, otra vez: una cota viene con su modelo pegado. La cota
  de Fredman y Saks de la conferencia 4 era en otro modelo más, el de sondeo de celdas.

### 10. Cierre del Tema 1

- Lo que queda después de cinco conferencias: medir en un modelo, recorrer el ciclo,
  demostrar correctitud, analizar costo, acotar por abajo. El documento de cierre del
  tema lo junta.
- El Tema 2 cambia de eje: las clases se organizan por técnica de diseño.

### 11. Resumen

### Ejercicios

1. Máximo y mínimo a la vez: diseña un algoritmo con $\lceil 3n/2 \rceil - 2$
   comparaciones y demuestra con un adversario que no se puede con menos.
2. Demuestra que decidir si un arreglo está ordenado requiere $n - 1$ comparaciones.
3. Mezclar una lista de largo $m$ con una de largo $n$: da la cota de información y un
   algoritmo que la alcance cuando $m = 1$.
4. Demuestra que la mediana de 5 elementos se puede hallar con 6 comparaciones y que
   con 5 no alcanza.
5. Distinción de elementos en el modelo de comparaciones: demuestra $\Omega(n \log n)$
   con un árbol de decisión. ¿Por qué no basta contar respuestas, que son solo dos?
6. El tercer mayor: extiende el torneo para hallarlo y cuenta cuántas comparaciones
   usa en el peor caso. ¿Qué dice la cota de información?
7. Radix sort ordena enteros de $b$ bits en $O(n b / \log n)$ pasos con dígitos de
   $\log_2 n$ bits. ¿En qué modelo? ¿Contradice la cota de la sección 3?
8. Un algoritmo de ordenamiento por comparaciones hace a lo sumo $n \log_2 n - 10n$
   comparaciones para todo $n$ grande. ¿Puede existir? Justifica con la sección 3.

## Audios (tentativo)

| Audio | Secciones | Minutos |
|---|---|---|
| 1 | 1 y 2 | 5 |
| 2 | 3 | 5 |
| 3 | 4 y 5 | 5 |
| 4 | 6 | 4 |
| 5 | 7 | 7 |
| 6 | 8 | 4 |
| 7 | 9 y 10 | 4 |

Total estimado: 34 minutos.

## Decisiones que quiero confirmar

- **Sin nombre para la cota del segundo mayor.** Suele atribuirse a Kislitsyn (1964),
  pero no la pude verificar en una fuente primaria, así que las notas la demuestran y
  no le ponen autor. La de mezclar sí está verificada (CLRS, problema 8-6).
- **La demostración del adversario de pesos, completa.** Es la parte difícil de la
  clase y la que más muestra la técnica. Las notas la llevan entera.
- **El árbol de decisión de la figura sale de correr ordenamiento por inserción**, no
  dibujado a mano. Es la regla del know-how de figuras.
- **La sección 10 cierra el tema en pocas líneas** y remite al documento de cierre,
  que tiene su propio outline.

Resueltas el 2026-09-29: todo aprobado como está.
