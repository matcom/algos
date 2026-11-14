# Tema 1: soluciones de los ejercicios

Mauricio Medina Hernández · C412 · Diseño y Análisis de Algoritmos, MatCom, 2026

Soluciones de los 14 ejercicios del resumen del Tema 1. Cada ejercicio tiene un md con
el enunciado, lo que se pide, las demostraciones paso a paso y una sección
«Verificación con código», y un `.py` que imprime cada tabla y cada número que cita
el md.

## Índice

| | Ejercicio | Qué se demuestra |
|---|---|---|
| 1 | [Una computadora mil veces más rápida](ejercicio-01.md) | Con costo $c\,n^2$ el tamaño crece $\sqrt{1000} \approx 31{,}6$ veces, para todo $n_0$. Con $c\,n\log_2 n$ el factor $k$ cumple $k(1 + \log_2 k/\log_2 n_0) = 1000$: va de $524{,}5$ a $805{,}1$ para $n_0$ entre $10^3$ y $10^{12}$, y tiende a $1000$. |
| 2 | [Búsqueda binaria](ejercicio-02.md) | Invariante, potencial $hi - lo$ que baja a la mitad, y la cota de información con los $n+1$ huecos: $\lceil \log_2(n+1) \rceil$ comparaciones, óptima. |
| 3 | [Pila con mínimo en $O(1)$](ejercicio-03.md) | Dos pilas paralelas y el invariante $m[i] = \min\{v[0..i]\}$: las tres operaciones cuestan $O(1)$ en el peor caso. La variante que guarda solo los mínimos nuevos necesita `≤`: con `<` falla cuando el mínimo se repite. |
| 4 | [Contador binario en una máquina de Turing](ejercicio-04.md) | Un incremento cuesta $2t + 2$ pasos. Con $\Phi = 2\cdot(\text{unos})$ el costo amortizado es exactamente $4$, y $m$ incrementos cuestan $4m - 2s_2(m)$. |
| 5 | [Detección de ciclos de Floyd](ejercicio-05.md) | El invariante «slow $= x_k$, fast $= x_{2k}$» y tres demostraciones, dos de ellas con un potencial distinto cada una: devuelve `True` si y solo si hay ciclo, y siempre termina. Sin ciclo hace $\lfloor n/2 \rfloor$ vueltas; con ciclo, $k^\ast = \lambda\lceil \max(\mu,1)/\lambda \rceil \le n$. |
| 6 | [Búsqueda en una matriz ordenada](ejercicio-06.md) | La escalera hace a lo sumo $2n - 1$ comparaciones, y un adversario sobre la antidiagonal obliga a cualquier algoritmo a hacer al menos $n$. |
| 7 | [Mediana de dos arreglos ordenados](ejercicio-07.md) | Generalizando al $k$-ésimo menor: exactamente $\lceil \log_2 n \rceil + 1$ comparaciones en toda entrada, y la cota de información ($2n$ medianas posibles) da lo mismo. |
| 8 | [Elementos que aparecen más de $n/3$ veces](ejercicio-08.md) | Dos candidatos que cancelan tríos, con el invariante reforzado $i = 3t + k_1 + k_2$: ninguna respuesta se pierde. La versión sin verificar es incorrecta, y el generador «plantada de dos» no la atrapa nunca. |
| 9 | [La mezcla «optimizada»](ejercicio-09.md) | Hace a lo sumo $2n - 2$ comparaciones, menos que la cota $2n - 1$ de cualquier mezcla, así que no puede ser correcta. Falla exactamente cuando el máximo está en $B$, en la mitad de las entradas. |
| 10 | [Par más cercano en una dimensión](ejercicio-10.md) | $\Omega(n \log n)$ en árboles algebraicos por reducción desde la distinción de elementos (demostrado para pruebas lineales). La rejilla aleatorizada cuesta $O(n)$ esperado porque sale del modelo: usa parte entera, tabla hash y azar. |
| 11 | [La mochila en $O(nW)$](ejercicio-11.md) | El algoritmo es correcto y cuesta $\Theta(nW)$, que es exponencial en los bits de $W$: es pseudopolinomial, como la primalidad por división. |
| 12 | [Gale–Shapley con listas incompletas](ejercicio-12.md) | El potencial cuenta propuestas pendientes y proponentes libres, y da a lo sumo $n^2 + n$ iteraciones. Con la pareja bloqueante adaptada, el resultado es estable en cualquier orden de ejecución. |
| 13 | [Splay tree sobre un camino](ejercicio-13.md) | El lema de acceso da a lo sumo $4n\log_2 n + n$ rotaciones. Subir a la raíz cuesta exactamente $(n-1)(n+2)/2$. La cota no es ajustada: el costo real es $\Theta(n)$, unas $4{,}4$ rotaciones por acceso. |
| 14 | [Torres de Hanoi](ejercicio-14.md) | El algoritmo recursivo hace $2^n - 1$ movimientos y ninguna solución hace menos. Con cuatro varillas la cota deja de valer: el mínimo es $1, 3, 5, 9, 13, 17, 25$ para $n = 1, \dots, 7$, y el algoritmo de Frame–Stewart lo alcanza para $n \le 9$. |

## Algoritmos y cotas mínimas

En los ejercicios que demuestran una cota mínima, esta es la comparación con el
algoritmo. Cada cota vale en el modelo que se indica.

| Ejercicio | Algoritmo | Cota mínima (modelo) | ¿Coinciden? |
|---|---|---|---|
| 2 | búsqueda binaria: $\lceil \log_2(n+1) \rceil$ | $\lceil \log_2(n+1) \rceil$ (comparaciones, información) | sí, exactamente |
| 6 | escalera: $2n - 1$ | $n$ (comparaciones con $x$, adversario) | en el orden, $\Theta(n)$ |
| 7 | $k$-ésimo menor: $\lceil \log_2 n \rceil + 1$ | $\lceil \log_2 n \rceil + 1$ (comparaciones, información) | sí, exactamente |
| 9 | mezcla normal: $2n - 1$ | $2n - 1$ (comparaciones, adversario) | sí, exactamente; la «optimizada» hace $2n - 2$ y por eso es incorrecta |
| 10 | ordenar y mirar vecinos: $O(n \log n)$ | $\Omega(n \log n)$ (árboles de decisión algebraicos) | sí, en el orden; la rejilla, $O(n)$ esperado, está fuera del modelo |
| 13 | splay: $\Theta(n)$ medido; cota del lema $4n\log_2 n + n$ | $2n - 2$ (cada acceso cuesta al menos una rotación) | en el orden, $\Theta(n)$, por el teorema del acceso secuencial (citado) |
| 14 | recursivo: $2^n - 1$ | $2^n - 1$ (movimientos legales, tres varillas) | sí, exactamente |

## Archivos

- `ejercicio-NN.md`: la solución del ejercicio NN.
- `ejercicio-NN.py`: su código. Imprime las tablas que cita el md y comprueba con
  `assert` lo que se puede comprobar en cada caso.
- `figuras.py` y `figuras/`: las figuras de los md, y cinco animaciones (dos en el
  ejercicio 2, y una en el 5, el 6 y el 13). Cada una se dibuja a partir de lo que calcula el `.py` de su ejercicio, en
  una versión para tema claro y otra para tema oscuro.
- `test_tema1.py`: 45 pruebas. Para cada ejercicio comprueba que el `.py` imprime lo
  que cita el md, y verifica los teoremas en casos pequeños, muchas veces en todos los
  casos de un tamaño.

## Cómo ejecutar

Hace falta Python 3. Los ejercicios y las pruebas no usan bibliotecas externas; las
figuras usan `matplotlib` (que trae `numpy` y `Pillow`). Los comandos se corren desde
esta carpeta.

Un ejercicio:

```bash
python3 ejercicio-07.py
```

Todas las pruebas (tardan unos dos minutos):

```bash
python3 test_tema1.py
```

Regenerar las figuras (todas, o solo las de algunos ejercicios):

```bash
python3 figuras.py
```

```bash
python3 figuras.py 6 9
```
