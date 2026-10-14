# Tema 1 · Soluciones de los ejercicios

Soluciones de los 14 ejercicios de "Tema 1: fundamentos. Resumen y ejercicios" (Diseño y Análisis de Algoritmos, MatCom, 2026). Cada informe sigue la forma de respuesta del §4 del resumen: el enunciado con su modelo, el algoritmo, el invariante con sus tres pasos, la terminación, el costo y, cuando se puede, la cota mínima con su modelo. Además trae código que reproduce cada tabla, pruebas y figuras.

## Índice

| | ejercicio | resultado central |
|---|---|---|
| 1 | [Una computadora mil veces más rápida](ejercicio-01.md) | Un costo c·n² gana √1000 ≈ 31,6 siempre. Uno c·n log n gana un factor que depende de n: ≈ 791 en la máquina de la C1. Con solo Θ el factor no queda fijado. |
| 2 | [Invariante, potencial y cota de la búsqueda binaria](ejercicio-02.md) | Óptima exacta: ⌈log₂(n+1)⌉ comparaciones para cada n, contra la cota de los n+1 huecos. |
| 3 | [Una pila con mínimo en O(1)](ejercicio-03.md) | Pares (valor, mínimo del prefijo). La versión compacta con `<` en lugar de `≤` falla solo cuando el mínimo se repite. |
| 4 | [El contador binario en una máquina de Turing](ejercicio-04.md) | Con Φ = 2·(unos), el costo amortizado es exactamente 4, y el total, 4m − 2·popcount(m). |
| 5 | [Detección de ciclos de Floyd](ejercicio-05.md) | El encuentro es exactamente en t* = λ·max(1, ⌈μ/λ⌉) ≤ μ + λ. Verificado sobre las 747 486 listas de hasta 6 nodos. |
| 6 | [Buscar en una matriz ordenada](ejercicio-06.md) | La búsqueda en escalera usa a lo sumo 2n − 1 comparaciones, y un adversario exige exactamente 2n − 1. |
| 7 | [La mediana de dos arreglos ordenados](ejercicio-07.md) | Una búsqueda binaria sobre una escalera de 2n − 1 comparaciones alcanza la cota de información ⌈log₂ 2n⌉ para todo n. |
| 8 | [Los elementos que aparecen más de n/3 veces](ejercicio-08.md) | Invariante de ternas de distintos. El generador de dos pesados es ciego a la versión sin verificar. |
| 9 | [La mezcla "optimizada"](ejercicio-09.md) | Hace 2n − 2 comparaciones, así que no puede ser correcta (C5, §6). Falla exactamente cuando el máximo está en B. |
| 10 | [Par más cercano en una dimensión](ejercicio-10.md) | Ω(n log n) por reducción, demostrada entera en árboles lineales. La rejilla en 1D hace en esperanza a lo sumo 2Hₙ − 3 reconstrucciones, exactamente si no hay empates. |
| 11 | [La mochila en O(nW) no es polinomial](ejercicio-11.md) | 2^Θ(s) en el tamaño en bits: pseudopolinomial, por el mismo mecanismo que la primalidad por división. |
| 12 | [Gale-Shapley con listas incompletas](ejercicio-12.md) | El resultado es estable y óptimo para los proponentes, y todos los emparejamientos estables dejan sola a la misma gente. |
| 13 | [Splay sobre un camino, accediendo en orden](ejercicio-13.md) | La cota del lema es O(n log n), y lo real es ≈ 4,41 n. El árbol vuelve exactamente al camino de partida. |
| 14 | [El ciclo completo: intersección de dos listas ordenadas](ejercicio-14.md) | Dos punteros con 2n − 1 comparaciones, y un adversario que exige exactamente 2n − 1. |

## Organización

- `ejercicio-XX.md`: el informe. Cada uno tiene una sección "Verificación: código y pruebas" que lista qué comprueba cada prueba, y termina con un resumen.
- `codigo/ejercicio_XX.py`: implementa los algoritmos e imprime todas las tablas del informe. Con `--figuras` regenera también las figuras.
- `codigo/test_ejercicio_XX.py`: las pruebas. Cada una comprueba una afirmación concreta del informe.
- `figuras/ejercicio-XX-*.png`: las figuras de los informes.

## Reproducir

Con Python 3 y `pytest`, `numpy` y `scipy` instalados (y `matplotlib` para las figuras):

```bash
cd codigo
python -m pytest
```

Son 135 pruebas, y tardan unos 15 segundos. Para ver las tablas de un ejercicio:

```bash
cd codigo
python ejercicio_07.py
```
