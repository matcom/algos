# Outline: Tema 1, resumen y ejercicios

Estado: aprobado y redactado (2026-09-29). El documento está en `resumen.md`.
Destino: `Lectures/2026/tema-1/resumen.md` + PDF con scriptorium.
Extensión objetivo: 3 000–3 500 palabras, más los ejercicios.

## Para qué sirve

Es un documento de repaso, no una conferencia más. Tiene tres usos:

- Estudiar para el examen: en pocas páginas, qué hay que saber del tema y cómo se
  relacionan las cinco conferencias.
- Ver el tema entero de una vez. Cada conferencia contó su parte, y hay ideas que solo
  se ven juntando varias (el modelo, las pruebas contra las demostraciones).
- Practicar con ejercicios que mezclan conferencias, del estilo de las preguntas del
  examen final.

No trae material nuevo, ni código ejecutable, ni figuras nuevas. Remite a las
conferencias por número y sección.

## Estructura

### 1. El mapa del tema

- Una tabla: las cinco preguntas del ciclo de la conferencia 2, qué conferencia da la
  herramienta para cada una, el ejemplo trabajado y el error típico que atrapa.

| pregunta | conferencia | herramienta | ejemplo | error que atrapa |
|---|---|---|---|---|
| ¿cómo se mide? | 1 | modelo RAM, notación asintótica, tamaño en bits | primalidad por división | llamar polinomial a algo exponencial en bits |
| ¿qué algoritmo? | 2 | el ciclo completo | par más cercano | saltarse etapas |
| ¿es correcto? | 3 | invariante, potencial, primer fallo | Boyer-Moore, Gale-Shapley | el atajo del contador |
| ¿cuánto cuesta? | 4 | análisis amortizado | cola, splay, union-find | subir a la raíz |
| ¿se puede mejor? | 5 | información, adversario, reducción | ordenar, mezclar, segundo mayor | el torneo que ahorra una comparación |

### 2. Lo que hay que llevarse de cada conferencia

Un párrafo por conferencia, con la regla que resume cada una. No repite el resumen de
cada conferencia: dice qué papel juega en el tema.

- **Conferencia 1.** Se mide en un modelo, y el tamaño de la entrada son bits. El word
  RAM es el modelo por defecto.
- **Conferencia 2.** El ciclo de cinco preguntas, y la primera cota mínima, que resultó
  ser una afirmación sobre un modelo.
- **Conferencia 3.** Correcto quiere decir parcial más terminación. Un invariante tiene
  que ser inductivo, no solo verdadero.
- **Conferencia 4.** El costo amortizado es una garantía de peor caso sobre secuencias,
  y un potencial mide una deuda.
- **Conferencia 5.** La información cuenta respuestas, el adversario cuenta trabajo, y
  una cota mínima también sirve de especificación.

### 3. Cuatro ideas que atraviesan el tema

1. **Toda cota viene con un modelo.** El caso se repite cinco veces: la máquina de
   Turing contra la RAM (C1), la multiplicación de costo 1 (C1), Ben-Or contra la
   rejilla (C2), el sondeo de celdas de Fredman y Saks (C4), las comparaciones contra
   el conteo (C5).
2. **Las pruebas no bastan, y la demostración dice dónde buscar.** Una tabla con los
   cuatro errores plantados, cuánto fallan en las pruebas y qué paso de la demostración
   los anunciaba:

   | conferencia | error plantado | cuánto falla en pruebas al azar | lo anuncia |
   |---|---|---|---|
   | 2 | 1 vecino en lugar de 7 | ~1 % de las instancias pequeñas, 0 de las grandes | el lema de la franja |
   | 3 | el atajo del contador | 0 % con mayoría plantada o alfabeto binario | la hipótesis "si hay mayoría" |
   | 4 | subir a la raíz | la cota falla en 4 de 1500 accesos mezclados | el caso zig-zig del lema de acceso |
   | 5 | el torneo que ahorra una comparación | $1/(n-1)$: 0,07 % con $n = 1024$ | la cota del adversario |

   Los números salen de las notas de cada conferencia, y el documento dice de dónde.
3. **Experimentar antes de demostrar.** El invariante vigilado (C3), el lema de acceso
   ejecutado (C4), el barrido de constantes (C2). El experimento propone y la
   demostración decide.
4. **El caso típico no es la garantía.** La franja casi nunca tiene 8 puntos (C2),
   Gale-Shapley hace unas $n \ln n$ propuestas y no $n^2$ (C3), una sola operación de
   una estructura amortizada puede costar $\Theta(n)$ (C4).

### 4. Cómo se ve una respuesta completa

- Un ejemplo resuelto entero, de media página, como modelo de lo que se espera en un
  ejercicio: **el máximo de $n$ elementos**. Enunciado, algoritmo, correctitud por
  invariante, costo exacto $n - 1$, cota mínima $n - 1$ por adversario.
- Es deliberadamente fácil, para que lo que se vea sea la forma de la respuesta.

### 5. Ejercicios del tema

Trece ejercicios, marcados por dificultad (★ a ★★★), y cada uno toca al menos dos
conferencias. No llevan solución: las soluciones bien presentadas cuentan para la
evaluación, como se dijo en la conferencia 1.

1. ★ Una computadora mil veces más rápida y un algoritmo $\Theta(n^2)$ contra uno
   $\Theta(n \log n)$: cuánto crece el tamaño resoluble en cada caso. (C1)
2. ★ Da invariante y potencial para la búsqueda binaria, y la cota de información que
   la hace óptima. (C3, C5)
3. ★ Pila con operación `mínimo` en $O(1)$: diseño, invariante y costo. (C3, C4)
4. ★★ El contador binario en una máquina de Turing del ejercicio 7 de la conferencia 1:
   demuestra que $m$ incrementos desde 0 cuestan $O(m)$ pasos, con un potencial. Cierra
   la pregunta que la conferencia 1 dejó abierta. (C1, C4)
5. ★★ Detección de ciclo en una lista enlazada con dos punteros (Floyd): invariante,
   terminación por potencial y costo. (C3)
6. ★★ Búsqueda en una matriz $n \times n$ ordenada por filas y por columnas: algoritmo
   $O(n)$ y cota mínima $\Omega(n)$ por adversario. (C2, C5)
7. ★★ Mediana de dos arreglos ordenados de largo $n$ en $O(\log n)$: algoritmo,
   correctitud y cota de información. (C2, C3, C5)
8. ★★ El elemento que aparece más de $n/3$ veces: generaliza Boyer-Moore, demuestra el
   invariante y di qué atajo sería el error análogo al de la conferencia 3. (C3)
9. ★★ Máximo y mínimo con $\lceil 3n/2 \rceil - 2$ comparaciones, y la cota por
   adversario. (C5)
10. ★★★ Par más cercano en una dimensión: demuestra $\Omega(n \log n)$ en árboles de
    decisión algebraicos por reducción desde distinción de elementos, y di qué
    algoritmo de la conferencia 2 rompe la cota en otro modelo. (C2, C5)
11. ★★★ Un arreglo dinámico que se encoge: encuentra el potencial, y explica por qué
    encoger a la mitad al quedar a la mitad da $\Theta(n)$ por operación. (C4)
12. ★★★ Union-find sin unión por rango, solo con compresión: mide el costo sobre
    entradas adversas y compáralo con la cota de la conferencia 4. (C4)
13. ★★★ Diseña un problema, un algoritmo y una cota mínima que coincidan, y recorre el
    ciclo completo de la conferencia 2 sobre él. Es el formato del examen.

## Decisiones que quiero confirmar

- **Dónde vive**: `Lectures/2026/tema-1/`, con `resumen.md` y su PDF. Si prefieres que
  vaya en `Problems/`, lo muevo.
- **Sin soluciones.** Encaja con la regla de que las soluciones de los estudiantes
  cuentan para la evaluación.
- **El ejemplo resuelto del máximo** es el único contenido "nuevo". Da la forma de una
  respuesta completa. Se puede quitar.
- **Algunos ejercicios repiten con otro ángulo ejercicios de las conferencias** (el 9
  es el 1 de la conferencia 5, el 11 es el 1 de la conferencia 4). Los dejo porque en
  un repaso conviene que estén juntos, pero los puedo cambiar por otros.

Resueltas el 2026-09-29: todo aprobado como está.
