# Animaciones

Animaciones de [manim](https://www.manim.community/), al estilo de 3Blue1Brown: fondo
oscuro, texto y fórmulas en LaTeX, y pocos colores con un significado fijo (azul, el
estado del algoritmo; amarillo, lo que se mira; verde, lo decidido; rojo, el error;
dorado, el potencial). Cada una demuestra una sola idea y va dentro de la sección del
`.md` que explica. Cada escena corre el algoritmo de verdad y anima la traza que
produce: nada se coloca a mano, así que la animación no puede contradecir al código del
ejercicio.

| ejercicio | archivo | qué muestra |
|---|---|---|
| [1](../ejercicio-01.md) | `factor` | en escala logarítmica, con $n^2$ el tamaño avanza siempre $\sqrt{1000}$; con $n \log n$, depende de dónde se empieza |
| [2](../ejercicio-02.md) | `invariante` | lo que queda fuera de la ventana ya está decidido, y con la ventana vacía, el hueco |
| | `bits` | el tamaño de la ventana pierde por lo menos un bit por comparación |
| | `testigo` | dos huecos no comparten hoja, y once huecos piden altura 4 |
| | `estancada` | con `lo = m`, un candidato menor que $x$ deja la ventana quieta |
| [3](../ejercicio-03.md) | `paralela` | cada celda de $M$ es el mínimo del prefijo de $S$ |
| | `repetidos` | con `<`, el `pop` de un mínimo repetido vacía $M$ |
| [4](../ejercicio-04.md) | `monedas` | dos monedas por cada 1 pagan la ida y la vuelta: amortizado, 4 |
| | `cabezal` | desde el bit más significativo hay que caminar todo el número |
| [5](../ejercicio-05.md) | `invariante` | tortuga en $x_k$, liebre en $x_{2k}$; con y sin ciclo |
| | `potencial` | $\Phi$ baja de a uno, con el salto del cambio de fase |
| | `entrada` | desde el encuentro, dos punteros a velocidad 1 se cruzan en la entrada |
| [6](../ejercicio-06.md) | `escalera` | cada comparación descarta una fila o una columna |
| | `adversario` | las dos antidiagonales; `j > 0` deja una celda sin mirar |
| [7](../ejercicio-07.md) | `corte` | sí, sí, sí, no, no...: la búsqueda binaria del corte |
| | `centinela` | `A[-1]` es el último elemento, no $-\infty$ |
| [8](../ejercicio-08.md) | `trios` | copias vivas y tríos de distintos: el invariante (T) |
| | `orden-malo` | dos copias de B en lugares distintos, canceladas juntas |
| [9](../ejercicio-09.md) | `intercambio` | intercambiar dos vecinos no comparados cambia la salida y no las respuestas |
| | `optimizada` | el merge optimizado deja dos pares sin comparar |
| [10](../ejercicio-10.md) | `rejilla` | celdas de ancho $\delta$, tres consultas, reconstrucciones |
| | `hacia-atras` | el último en llegar reconstruye con probabilidad $2/i$ |
| | `orden-adversario` | sin azar, se reconstruye en cada paso |
| [11](../ejercicio-11.md) | `fila` | de mayor a menor contra de menor a mayor |
| | `bits` | un bit más de $W$ duplica la tabla |
| [12](../ejercicio-12.md) | `propuestas` | listas incompletas: $a_2$ agota su lista |
| | `verificador` | las bloqueantes del error tienen un proponente solo |
| [13](../ejercicio-13.md) | `primer-acceso` | los zig-zig parten el camino a la mitad |
| | `vuelve-al-camino` | el invariante (C), acceso por acceso |
| [14](../ejercicio-14.md) | `primer-si` | el arreglo no está ordenado; las respuestas, sí |
| | `adversario` | el adversario se queda con la mitad más grande |
| | `referencia-cero` | con $A[0]$, el arreglo sin rotar no tiene ningún sí |

Cada escena deja dos archivos, `ejercicio-NN-<archivo>.gif`, que GitHub muestra dentro
del `.md`, y `ejercicio-NN-<archivo>.mp4`, en mejor calidad, para la exposición.

## Cómo regenerarlas

Hace falta [uv](https://docs.astral.sh/uv/), que instala manim en un entorno aparte, una
distribución de LaTeX (TeX Live o MiKTeX), y ffmpeg para los GIF (sin ffmpeg se usa el GIF
de manim, de menor calidad):

```bash
uv run --python 3.13 --with manim python renderizar.py
```

Para regenerar solo algunas, se pasan los números de ejercicio: `renderizar.py 02 05`.
Para ver una escena sin tocar los archivos de la carpeta:

```bash
uv run --python 3.13 --with manim manim -ql ejercicio-05.py Invariante
```

`comun.py` tiene el estilo y los ayudantes que comparten todas las escenas. Los archivos
intermedios de manim quedan en `media/`, que no se versiona.
