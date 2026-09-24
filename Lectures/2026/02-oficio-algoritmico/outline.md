# Outline — Conferencia 2: el oficio algorítmico

Estado: aprobado y redactado (2026-09-24). Las notas están en `notas.md`.
Destino: `Lectures/2026/02-oficio-algoritmico/notas.md` + PDF con scriptorium.
Extensión objetivo: 3 800–4 200 palabras (la conferencia 1 tiene 3 270; esta lleva
tres algoritmos y tres demostraciones).

## Idea de la clase

La conferencia 1 fijó cómo se mide. Esta fija cómo se trabaja. En vez de enunciar el
ciclo *problema → algoritmo → correctitud → complejidad → cota mínima* y pasar a otra
cosa, lo recorremos entero, una vez, sobre un solo problema: el par de puntos más
cercanos en el plano. Cada vuelta del ciclo deja una plantilla que el resto del curso
reusa.

El problema está elegido para que las cinco etapas tengan contenido real: la fuerza
bruta es obvia y cara, el algoritmo bueno tiene una demostración de correctitud que no
se adivina, la complejidad necesita un truco de implementación para salir bien, hay
una cota mínima demostrable, y hay un algoritmo que la rompe. Ese último punto es el
que hace la clase: obliga a decir que una cota mínima es una afirmación *sobre un
modelo*, no sobre el problema.

## Estructura

### 1. Las cinco preguntas

- El ciclo como espina del curso, enunciado una vez y con nombre propio.
- Qué significa cada pregunta y por qué ninguna se puede saltar: un algoritmo sin
  demostración es una conjetura, un análisis sin cota mínima no sabe si vale la pena
  seguir buscando.
- Aviso de método: hoy lo recorremos entero sobre un problema; de la conferencia 6 en
  adelante el ciclo es implícito y las clases se organizan por técnica.

### 2. El problema

- Enunciado formal: dados $n$ puntos en $\mathbb{R}^2$, devolver el par que minimiza
  la distancia euclidiana. Salida: el par, o la distancia.
- Precisiones que un enunciado tiene que dar y normalmente no se dan: qué pasa con
  empates, qué pasa con puntos repetidos, qué se cuenta como operación (comparar dos
  distancias al cuadrado evita la raíz y no cambia el orden).
- Qué **no** es este problema: "para cada punto, su vecino más cercano" es otro
  problema, más caro en general. Distinguirlos es parte del oficio.

### 3. Calentamiento en una dimensión

- $n$ números en la recta. Ordenar y mirar pares consecutivos.
- **Lema:** el par más cercano es consecutivo en el orden. Demostración de dos líneas
  por contradicción. Es la primera demostración de correctitud de la clase y es corta
  a propósito: fija la forma que va a tener la larga.
- Costo $O(n \log n)$, dominado por el ordenamiento.
- La observación que organiza el resto de la clase: en la recta hay un orden total y
  "cerca" implica "vecino en el orden". En el plano no hay tal orden, y ahí empieza
  la dificultad.

### 4. Fuerza bruta

- Recorrer los $\binom{n}{2}$ pares. Correcto por agotamiento, sin nada que demostrar.
- $\Theta(n^2)$, y por qué eso es una cota superior *y* inferior de **este algoritmo**,
  no del problema. Primera aparición de la distinción que la sección 7 explota.
- **Código ejecutable:** implementación + tiempos medidos para $n$ creciente, hasta
  donde se hace impracticable. Sirve de oráculo para verificar los dos algoritmos
  siguientes.

### 5. Divide y vencerás: el algoritmo

- Ordenar por $x$, partir por la mediana en $P_I$ y $P_D$, resolver cada mitad,
  $\delta = \min(\delta_I, \delta_D)$.
- El caso que no cubre la recursión: el par más cercano con un punto de cada lado.
  Ambos tienen que estar en la franja de ancho $2\delta$ alrededor de la recta de
  corte.
- Por qué la franja no basta por sí sola: puede contener los $n$ puntos, así que
  compararlos todos contra todos devuelve el $O(n^2)$.

### 6. Divide y vencerás: la correctitud

El corazón de la clase y la demostración larga.

- **Lema de la franja.** Ordenados los puntos de la franja por $y$, cada punto solo
  necesita compararse con los 7 siguientes.
- Demostración por empaquetamiento: si dos puntos de la franja están a distancia
  $< \delta$, difieren en $y$ en menos de $\delta$, así que ambos caen en un
  rectángulo de $\delta \times 2\delta$. Ese rectángulo se parte en 8 cuadrados de
  lado $\delta/2$, cuyo diámetro es $\delta/\sqrt{2} < \delta$, de modo que cada
  cuadrado contiene a lo sumo un punto. El rectángulo tiene entonces a lo sumo 8
  puntos, y 7 comparaciones bastan.
- Dónde se usa la hipótesis de inducción: los puntos de un mismo lado están a
  distancia $\ge \delta$ entre sí, y eso es lo que hace que el empaquetamiento
  funcione. Señalarlo explícitamente, porque es el paso que se salta todo el mundo.
- Correctitud completa por inducción fuerte sobre $n$, con el caso base $n \le 3$.
- Comentario sobre el 7: es una cota, no el óptimo; el ejercicio 2 pide afinarla.

### 7. Divide y vencerás: la complejidad

- Recurrencia ingenua: si la franja se ordena por $y$ en cada nivel,
  $T(n) = 2T(n/2) + O(n \log n) = O(n \log^2 n)$.
- El arreglo: mantener la lista ordenada por $y$ y mezclarla al subir, como en
  merge sort. Queda $T(n) = 2T(n/2) + O(n)$, y el Teorema Maestro da
  $\Theta(n \log n)$.
- La moraleja: el algoritmo no cambió, cambió la implementación. La separación entre
  la idea y su costo es parte del oficio.
- Memoria $O(n)$.
- **Código ejecutable:** implementación completa, verificación contra la fuerza bruta
  sobre entradas aleatorias, y tiempos que muestran dónde se cruzan las dos curvas.
- Crédito: Bentley y Shamos, 1976.

### 8. La cota mínima

Cambio de pregunta: de "cuánto cuesta este algoritmo" a "cuánto cuesta cualquiera".

- **Distinción de elementos**: dados $n$ reales, ¿hay dos iguales? Teorema de Ben-Or
  (1983): requiere $\Omega(n \log n)$ en árboles de decisión algebraicos.
- Qué es un árbol de decisión algebraico, en una definición que se pueda usar: cada
  nodo evalúa el signo de un polinomio de grado acotado en las coordenadas de la
  entrada y ramifica según el resultado. Capta comparar, sumar, multiplicar y medir
  distancias — es decir, todo lo que hacen las secciones 4 a 7.
- **La reducción:** $x_i \mapsto (x_i, 0)$. Los $x_i$ son todos distintos si y solo si
  la distancia del par más cercano es $> 0$. La transformación cuesta $O(n)$, así que
  un algoritmo para par más cercano en $o(n \log n)$ daría uno para distinción de
  elementos en $o(n \log n)$.
- Conclusión: el algoritmo de la sección 7 es óptimo en ese modelo, y la búsqueda se
  acabó. Primera reducción del curso, y la misma mecánica que el Tema 3 va a usar
  para NP-completitud, con otro objetivo. Decirlo.

### 9. Romper la cota

- El algoritmo incremental aleatorio (Rabin 1976; la versión que damos es la de
  Kleinberg y Tardos §13.7).
- Permutar los puntos al azar. Manteniendo $\delta$ = distancia del par más cercano
  entre los $i$ primeros, guardar los puntos en una rejilla de celdas de lado
  $\delta/2$.
- **Invariante:** cada celda contiene a lo sumo un punto, porque dos puntos en la
  misma celda están a distancia $\le \delta/\sqrt{2} < \delta$.
- Insertar $p_{i+1}$: cualquier punto a distancia $< \delta$ de él está en el bloque
  de $5 \times 5$ celdas centrado en la suya, 25 consultas de costo $O(1)$. Si no
  encuentra nada, $\delta$ no cambia y la inserción cuesta $O(1)$. Si encuentra algo,
  $\delta$ baja y hay que reconstruir la rejilla entera, $O(i)$.
- **Análisis hacia atrás:** fijado el conjunto $\{p_1, \dots, p_{i+1}\}$, su par más
  cercano está determinado; el paso $i+1$ reconstruye solo si $p_{i+1}$ es uno de los
  (a lo sumo) dos puntos de ese par. Como el orden es una permutación uniforme,
  la probabilidad es $\le 2/(i+1)$.
- Costo esperado: $\sum_i \frac{2}{i+1} \cdot O(i) = O(n)$. El número esperado de
  reconstrucciones es $\approx 2 \ln n$, que es el número que el código va a medir.
- **Código ejecutable:** implementación, verificación contra la fuerza bruta, y conteo
  empírico de reconstrucciones contra la predicción $2 \ln n$.

### 10. Qué escondía el modelo

- No hay contradicción. El algoritmo de la sección 9 hace dos cosas que un árbol de
  decisión algebraico no puede: calcular $\lfloor x/\delta \rfloor$, que es
  discontinua y no polinomial, y usar direccionamiento indirecto para guardar la
  rejilla en una tabla hash.
- Conexión hacia atrás con la conferencia 1: la máquina de Turing, la RAM y la word
  RAM daban respuestas distintas a "cuánto cuesta". Aquí el modelo decide qué es
  posible, no solo qué cuesta.
- La regla que se lleva el estudiante: una cota mínima siempre viene con un modelo
  pegado, y la primera pregunta ante una es cuál es ese modelo y qué deja fuera.
- Hacia adelante: la conferencia 5 hace cotas mínimas en serio, la 21 vuelve sobre los
  algoritmos aleatorios, y el Tema 3 usa reducciones para lo contrario de lo que se
  usaron hoy.

### 11. Resumen

Viñetas, una por etapa del ciclo, redactadas como lo que hay que recordar y no como
índice de la clase.

### Ejercicios

1. Demostrar formalmente el lema unidimensional de la sección 3.
2. El lema de la franja da 7. Demostrar la mejor constante que se pueda y exhibir una
   configuración de puntos que la alcance.
3. Par más cercano en $\mathbb{R}^3$: ¿en qué se convierte la franja? Diseñar el
   algoritmo y analizarlo.
4. El par más *lejano* (diámetro del conjunto): ¿funciona el mismo divide y vencerás?
   Decir exactamente qué paso falla.
5. Par más cercano bicromático (un punto rojo y uno azul): ¿sobrevive el lema de la
   franja? Justificar.
6. Implementar el algoritmo de la sección 9, contar reconstrucciones para
   $n = 10^3, 10^4, 10^5$ y comparar con $2 \ln n$.
7. Construir una entrada y un orden de inserción que fuercen al algoritmo de la
   sección 9 a $\Theta(n^2)$, y explicar por qué la permutación aleatoria lo evita.
8. La reducción de la sección 8 va de distinción de elementos a par más cercano.
   ¿Existe la contraria? ¿Qué se podría concluir si existiera?

## Decisiones que quiero confirmar

- **Cuatro algoritmos en una clase** (1-D, fuerza bruta, divide y vencerás,
  aleatorio) es mucho para 90 minutos si se demuestra todo en la pizarra. La
  alternativa es dejar la sección 9 como lectura orientada y solo enunciar el
  resultado en clase. Las notas la llevan completa en cualquiera de los dos casos.
- **Ben-Or sin demostrar.** La cota $\Omega(n \log n)$ para distinción de elementos se
  enuncia y se cita; su demostración usa cotas de Milnor-Thom sobre el número de
  componentes conexas de una variedad y no cabe aquí. Lo que sí se demuestra es la
  reducción. Me parece el reparto correcto, pero es una decisión.
- **Empaquetamiento con 8 cuadrados**, que da la cota 7. Es la presentación de CLRS.
  Kleinberg y Tardos usan una caja distinta y llegan a 15. Uso 7 y menciono que la
  constante depende de cómo se parta el rectángulo.
