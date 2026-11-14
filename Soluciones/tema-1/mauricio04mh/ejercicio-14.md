# Ejercicio 14. Las Torres de Hanoi: el algoritmo y la cota mínima coinciden

Dificultad: ★★★ · Código: [`ejercicio-14.py`](ejercicio-14.py)

---

## Enunciado

> Escoge un problema que no hayamos visto, recorre el ciclo completo de la conferencia 2 sobre él y consigue que el algoritmo y la cota mínima coincidan.

## Qué se pide

El ejercicio no da el problema: hay que elegirlo y llevarlo hasta el final. Se pide:

1. Un problema que no se haya tratado en las conferencias. Se elige **las Torres de Hanoi**.
2. Responder las cinco preguntas del ciclo de la Conferencia 2 (resumen, §11, y Figura 1 de la Conferencia 3), en orden:
   1. ¿Qué es el problema? (entrada, salida y modelo)
   2. ¿Qué algoritmo lo resuelve?
   3. ¿Por qué es correcto? (invariante y potencial, Conferencia 3)
   4. ¿Cuánto cuesta?
   5. ¿Se puede mejor? (cota mínima en un modelo explícito, Conferencia 5)
3. Que el costo del algoritmo y la cota mínima sean **la misma cantidad**. Entonces el algoritmo es óptimo y no queda nada por mejorar en ese modelo.

Resultado que se demuestra: con $n$ discos, el algoritmo recursivo hace exactamente $2^n - 1$ movimientos y ningún algoritmo puede hacer menos.

---

## Pregunta 1: el problema y su modelo

**Problema.** Hay tres varillas, numeradas $1, 2, 3$, y $n$ discos de tamaños distintos, numerados $1$ (el más pequeño) a $n$ (el más grande). Al principio los $n$ discos están en la varilla $1$, apilados con el más grande abajo. Un movimiento toma el disco de arriba de una varilla y lo pone en otra. **Regla:** nunca se pone un disco sobre uno más pequeño. Hay que llevar los $n$ discos a la varilla $3$ con el menor número de movimientos.

**Modelo.** Un estado indica en qué varilla está cada disco. El orden dentro de una varilla no hace falta guardarlo, porque la regla lo fuerza: es el de tamaño decreciente de abajo hacia arriba. Un movimiento legal cambia de varilla a un solo disco $i$ y exige que ningún disco menor que $i$ esté en la varilla de origen (si lo hubiera, $i$ no sería la cima) ni en la de destino (se pondría sobre uno menor). **El costo es el número de movimientos.** Una cota mínima habla de *toda* secuencia de movimientos legales, no solo de la del algoritmo.

**Notación.** En las pilas se escribe de abajo hacia arriba: $[3,2,1]$ es el disco $3$ abajo y el $1$ arriba.

**Ejemplos.**

- $n = 1$: un solo movimiento, $1 \to 3$.
- $n = 2$: el disco $1$ va a la varilla $2$, el disco $2$ va a la $3$, y el disco $1$ va a la $3$. Son $3$ movimientos.
- $n = 3$:

| movimiento | varilla 1 | varilla 2 | varilla 3 |
|---|---|---|---|
| (inicio) | [3,2,1] | [] | [] |
| 1. disco 1: 1→3 | [3,2] | [] | [1] |
| 2. disco 2: 1→2 | [3] | [2] | [1] |
| 3. disco 1: 3→2 | [3] | [2,1] | [] |
| 4. disco 3: 1→3 | [] | [2,1] | [3] |
| 5. disco 1: 2→1 | [1] | [2] | [3] |
| 6. disco 2: 2→3 | [1] | [] | [3,2] |
| 7. disco 1: 1→3 | [] | [] | [3,2,1] |

Con $n = 3$ discos bastan $7$ movimientos. Para $n = 1, 2, 3, \dots$ salen $1, 3, 7, \dots$ movimientos; se demostrará que la cantidad exacta es $2^n - 1$ y que no se puede menos.

---

## Pregunta 2: el algoritmo

Con el problema y su modelo claros, la pregunta es cómo resolverlo. La observación clave sale del ejemplo de $n = 3$: el disco grande se mueve una vez, en el medio, y antes y después se mueve una torre de dos discos.

**Idea.** Para mover el disco $n$ hay que apartar a los $n-1$ discos que tiene encima. Eso reduce el problema a sí mismo con un disco menos, dos veces:

1. Llevar los $n-1$ discos de arriba de `origen` a `auxiliar`.
2. Mover el disco $n$ de `origen` a `destino`.
3. Llevar los $n-1$ discos de `auxiliar` a `destino`, encima del disco $n$.

```python
def hanoi(n, origen, destino, auxiliar, movimientos):
    if n == 0:
        return
    hanoi(n - 1, origen, auxiliar, destino, movimientos)
    movimientos.append((n, origen, destino))
    hanoi(n - 1, auxiliar, destino, origen, movimientos)
```

Las llamadas recursivas intercambian los papeles de las varillas, y por eso la función las recibe como parámetros. La llamada `hanoi(n, 1, 3, 2, m)` resuelve el problema de «Pregunta 1: el problema y su modelo».

**Traza con $n = 3$.** `hanoi(3,1,3,2)` llama a `hanoi(2,1,2,3)`, que llama a `hanoi(1,1,3,2)`: mueve el disco $1$ de $1$ a $3$. Después mueve el disco $2$ de $1$ a $2$, y `hanoi(1,3,2,1)` mueve el disco $1$ de $3$ a $2$. Entonces el disco $3$ va de $1$ a $3$ y el resto repite la estructura. Salen exactamente los $7$ movimientos de la tabla.

**Fuerza bruta como oráculo** (Conferencia 2, §4). El algoritmo que siempre está disponible es explorar todos los estados. Hay $3^n$ estados (cada disco en una de tres varillas) y cada movimiento legal es una arista entre estados. Una búsqueda en anchura desde el estado inicial encuentra el camino más corto hasta el final. No necesita demostración de correctitud, pero cuesta $\Theta(3^n)$, y en «Verificación con código» sirve para contrastar la teoría.

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="figuras/ejercicio-14-estados-oscuro.svg">
  <img src="figuras/ejercicio-14-estados-claro.svg" alt="El grafo de los 27 estados con tres discos y el camino del algoritmo">
</picture>

**Figura 1.** El grafo de los $3^3 = 27$ estados con $n = 3$: cada nodo es un estado y cada arista, un movimiento legal. En las esquinas están los estados con todos los discos en una varilla. El camino resaltado es el del algoritmo: $7$ movimientos por el lado del triángulo que va de la varilla $1$ a la $3$.

---

## Pregunta 3: correctitud

La traza muestra que el algoritmo funciona con $n = 3$. Falta probar que funciona siempre.

Según la Conferencia 3 (§1), un algoritmo es correcto respecto a una especificación. Hay que demostrar por separado la correctitud parcial (si termina, cumple la postcondición) y la terminación.

### Especificación

Cuando `hanoi(n-1, …)` se ejecuta dentro de `hanoi(n, …)`, las varillas **no están vacías**: contienen discos mayores. Por eso la especificación habla de «la cima» de las varillas.

- **Precondición $\mathrm{Pre}(n)$.** Los discos $n, n-1, \dots, 1$ son los $n$ discos de arriba de `origen`, en ese orden, y todo disco que haya en `destino` o en `auxiliar` es mayor que $n$.
- **Postcondición $\mathrm{Post}(n)$.** Todos los movimientos fueron legales; los discos $n, \dots, 1$ quedaron arriba de `destino`, en ese orden; y ninguna otra pila cambió, salvo que `origen` perdió esos $n$ discos.

### Correctitud parcial

**Teorema 1.** Para todo $n \ge 0$ y tres varillas cualesquiera, si se cumple $\mathrm{Pre}(n)$ al llamar a `hanoi(n, origen, destino, auxiliar)`, al terminar se cumple $\mathrm{Post}(n)$.

**Demostración.** Por inducción sobre $n$. La propiedad que se mantiene en cada llamada recursiva es que su precondición se cumple.

**Paso 1. Caso base $n = 0$.** No hay discos ni movimientos, y $\mathrm{Post}(0)$ se cumple.

**Paso 2. Hipótesis.** Se supone el teorema para $n - 1$, con cualesquiera tres varillas. Sea $\mathrm{Pre}(n)$ cierta.

**Paso 3. Primera llamada** `hanoi(n-1, origen, auxiliar, destino)`.

- Los discos $n-1, \dots, 1$ son la cima de `origen`, porque son parte de los $n$ de arriba.
- Los discos de `auxiliar` y de `destino` son mayores que $n$, luego mayores que $n-1$.

Se cumple $\mathrm{Pre}(n-1)$. Por la hipótesis, los discos $n-1, \dots, 1$ quedan arriba de `auxiliar` y nada más cambia.

**Paso 4. El movimiento del disco $n$** de `origen` a `destino`. Ahora el disco $n$ es la cima de `origen`, y la cima de `destino` es mayor que $n$ (o `destino` está vacía). El movimiento es legal.

**Paso 5. Segunda llamada** `hanoi(n-1, auxiliar, destino, origen)`.

- Los discos $n-1, \dots, 1$ son la cima de `auxiliar`.
- En `destino` están el disco $n$ y discos mayores, y en `origen` solo discos mayores que $n$. Todo eso es mayor que $n-1$.

Se cumple $\mathrm{Pre}(n-1)$. Por la hipótesis, los discos $n-1,\dots,1$ quedan arriba de `destino`, encima del disco $n$.

**Paso 6. Conclusión.** Los discos $n, \dots, 1$ están arriba de `destino` en orden, todos los movimientos fueron legales y ninguna otra pila cambió. Se cumple $\mathrm{Post}(n)$. $\blacksquare$

En particular, `hanoi(n, 1, 3, 2)` lleva la torre completa de la varilla $1$ a la $3$ (las otras dos varillas están vacías, así que $\mathrm{Pre}(n)$ se cumple).

### Terminación

El potencial es el primer parámetro $n$. Es un entero no negativo, cada llamada recursiva lo reduce en $1$, y la llamada con $n = 0$ retorna sin llamar a nada. Por tanto la profundidad de la recursión es a lo sumo $n$ y el algoritmo termina (Conferencia 3, §1).

### El error que la demostración anuncia

La precondición parece sobrar. Es tentador escribir solo «`destino` y `auxiliar` están vacías». Esa especificación no se puede usar en el Paso 5: cuando empieza la segunda llamada, `destino` contiene el disco $n$. La inducción exige la condición más fuerte «lo que hay es mayor que $n$». El código lo comprueba en «Verificación con código»: con $n = 8$, de las $255$ llamadas, **$247$ entran con alguna de las otras dos varillas no vacía**.

---

## Pregunta 4: el costo

Demostrado que el algoritmo es correcto, se cuenta cuántos movimientos hace.

Cada llamada con $n \ge 1$ hace dos llamadas con $n-1$ y un movimiento. La llamada con $n = 0$ no hace ninguno. Sea $T(n)$ el número de movimientos:

$$T(0) = 0, \qquad T(n) = 2\,T(n-1) + 1.$$

**Teorema 2.** $T(n) = 2^n - 1$ para todo $n \ge 0$.

**Demostración.** Por inducción sobre $n$.

**Paso 1. Caso base.** $T(0) = 0 = 2^0 - 1$.

**Paso 2. Hipótesis.** $T(n-1) = 2^{n-1} - 1$.

**Paso 3. Sustitución.**

$$T(n) = 2\,(2^{n-1} - 1) + 1$$

**Paso 4. Desarrollo.**

$$T(n) = 2^n - 2 + 1 = 2^n - 1. \qquad\blacksquare$$

El algoritmo no mira nada de la entrada salvo $n$. No hay mejor ni peor caso: **hace siempre exactamente $2^n - 1$ movimientos**.

| $n$ | 1 | 2 | 3 | 4 | 5 | 6 | 10 | 20 | 64 |
|---|---|---|---|---|---|---|---|---|---|
| $T(n)$ | 1 | 3 | 7 | 15 | 31 | 63 | 1 023 | 1 048 575 | $\approx 1{,}8\cdot 10^{19}$ |

El costo es exponencial. Con $n = 64$ y un movimiento por segundo harían falta unos $5{,}9\cdot 10^{11}$ años. Esto concuerda con la Conferencia 1 (§7): para un algoritmo exponencial, mil veces más potencia de cómputo compra unas $10$ unidades de $n$. Además, ningún algoritmo que *escriba* la solución puede ser más rápido que su número de movimientos, así que lo que sigue es una cuestión sobre la longitud mínima de la solución.

---

## Pregunta 5: la cota mínima

El algoritmo hace $2^n - 1$ movimientos. La última pregunta es si alguna otra solución podría hacer menos. La respuesta sale de mirar qué obliga el disco más grande: sus movimientos separan la solución en tres partes.

**Modelo de la cota.** Una *solución* es cualquier secuencia de movimientos legales (en el sentido de «Pregunta 1: el problema y su modelo») que lleva el estado inicial al final. Su costo es su longitud. Un algoritmo que resuelva el problema produce una solución, así que acotar la longitud de *toda* solución acota a *todos* los algoritmos.

**Definición.** $M(n)$ es el mínimo número de movimientos de una secuencia legal que lleva $n$ discos apilados en una varilla $x$ a otra varilla $y \ne x$.

**Lema 1 (simetría).** $M(n)$ no depende del par $(x, y)$.

*Demostración.* Renombrar las varillas conserva las reglas. Una secuencia legal de $x$ a $y$ se convierte en una de $x'$ a $y'$ con la misma longitud. $\blacksquare$

**Lema 2 (el disco grande).** Cuando el disco $n$ cambia de la varilla $a$ a la varilla $b$, los otros $n-1$ discos están todos en la tercera varilla $c$.

*Demostración.*
1. Para salir de $a$, el disco $n$ debe ser la cima de $a$: no hay otro disco en $a$.
2. Para entrar a $b$, ningún disco menor puede estar en $b$. Todos los otros discos son menores, así que no hay ninguno en $b$.
3. Los $n-1$ discos restantes tienen que estar en $c$. $\blacksquare$

Este argumento es del tipo del adversario de la Conferencia 5 (§5): no cuenta hojas de un árbol, sino que usa las reglas para obligar a que cierto trabajo ocurra *antes* de otro.

**Teorema 3.** $M(n) \ge 2\,M(n-1) + 1$ y, por tanto, $M(n) \ge 2^n - 1$.

**Demostración.** Sea $S$ una secuencia legal que lleva $n$ discos de $x$ a $y$, y sea $z$ la tercera varilla. El disco $n$ cambia de varilla, así que tiene un primer movimiento $t_1$ y un último movimiento $t_k$ (pueden ser el mismo).

**Paso 1. Lo que ocurre antes de $t_1$.**
- Antes de $t_1$ el disco $n$ está quieto en $x$ y solo se mueven los discos $1, \dots, n-1$. El prefijo $S_1$ está formado por esos movimientos.
- Por el Lema 2, justo antes de $t_1$ los discos $1, \dots, n-1$ están todos en la varilla $c$ que no es $x$ ni el destino de $t_1$. Así $c \ne x$.
- Las reglas solo comparan un disco con discos menores. Como el disco $n$ es mayor que todos, que esté o no en juego no cambia la legalidad de los movimientos de los demás. Entonces $S_1$ es una secuencia legal del problema de $n-1$ discos de $x$ a $c$.
- Por el Lema 1 y la definición de $M$: $|S_1| \ge M(n-1)$.

**Paso 2. Lo que ocurre después de $t_k$.**
- Después de $t_k$ el disco $n$ ya está en $y$, y solo se mueven los discos $1, \dots, n-1$. Esos movimientos forman el sufijo $S_3$.
- Por el Lema 2, justo antes de $t_k$ los discos $1,\dots,n-1$ están todos en una varilla $c' \ne y$.
- Por la misma razón del Paso 1, $S_3$ lleva $n-1$ discos de $c'$ a $y$ con movimientos legales, y $|S_3| \ge M(n-1)$.

**Paso 3. Suma.** $S_1$, el movimiento $t_1$ y $S_3$ son partes disjuntas de $S$:

$$|S| \ge |S_1| + 1 + |S_3| \ge 2\,M(n-1) + 1.$$

Como $S$ era cualquier solución, $M(n) \ge 2\,M(n-1) + 1$.

**Paso 4. Inducción.** $M(0) = 0 = 2^0 - 1$. Si $M(n-1) \ge 2^{n-1} - 1$:

$$M(n) \ge 2\,(2^{n-1} - 1) + 1 = 2^n - 1. \qquad\blacksquare$$

El caso en que el disco $n$ se mueve más de una vez se cubre usando su primer y su último movimiento, que dejan fuera del conteo a $S_1$ y $S_3$ sin solaparlos.

---

## Conclusión: el algoritmo es óptimo

Por el Teorema 2, el algoritmo hace $T(n) = 2^n - 1$ movimientos. Por el Teorema 3, toda solución tiene al menos $2^n - 1$. Entonces

$$M(n) = T(n) = 2^n - 1,$$

el algoritmo es óptimo. Además, el código de «Verificación con código» cuenta con la búsqueda en anchura cuántas secuencias de longitud mínima existen: exactamente una para cada $n \le 10$, que es la del algoritmo. (Es una comprobación por cálculo para esos $n$, no parte de la demostración.)

**Las cinco preguntas, resumidas.**

| pregunta | respuesta |
|---|---|
| 1. problema | llevar $n$ discos de la varilla 1 a la 3, nunca uno grande sobre uno pequeño |
| 2. algoritmo | `hanoi`: $n-1$ al auxiliar, el grande al destino, $n-1$ encima |
| 3. correctitud | inducción con $\mathrm{Pre}/\mathrm{Post}$ (la precondición habla de «la cima»); terminación por el potencial $n$ |
| 4. costo | $T(n) = 2T(n-1)+1 = 2^n - 1$, siempre |
| 5. ¿mejor? | no: $M(n) \ge 2M(n-1)+1$, luego $M(n) \ge 2^n-1$ |

**Toda cota viene con un modelo** (Conferencia 2, §10 y §11). El Lema 2 usa que hay **tres** varillas: los $n-1$ discos pequeños *deben* estar todos en la única tercera varilla. Con cuatro varillas pueden repartirse entre dos, y la cota se rompe. El código calcula, por búsqueda en anchura, el mínimo con cuatro varillas para $n = 1, \dots, 7$:

| $n$ | 1 | 2 | 3 | 4 | 5 | 6 | 7 |
|---|---|---|---|---|---|---|---|
| 3 varillas, $2^n - 1$ | 1 | 3 | 7 | 15 | 31 | 63 | 127 |
| 4 varillas (BFS) | 1 | 3 | 5 | 9 | 13 | 17 | 25 |

Ya con $n = 3$ bastan $5$ movimientos, menos que $7$. La cota $2^n - 1$ vale para el modelo de tres varillas, no para el problema «mover discos» en general.

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="figuras/ejercicio-14-varillas-oscuro.svg">
  <img src="figuras/ejercicio-14-varillas-claro.svg" alt="Mínimo de movimientos con tres y con cuatro varillas, de n = 1 a 7">
</picture>

**Figura 2.** Los valores de la tabla: con cuatro varillas el mínimo crece mucho más despacio que $2^n - 1$.

### Extensión: el algoritmo de Frame–Stewart

¿Qué algoritmo alcanza los mínimos de la tabla con cuatro varillas? El de Frame–Stewart generaliza la idea recursiva: en lugar de apartar $n - 1$ discos, aparta solo los $k$ menores, y los $n - k$ grandes se mueven con tres varillas.

1. Llevar los $k$ discos menores de `origen` a una varilla auxiliar, con las cuatro varillas.
2. Llevar los $n - k$ discos restantes de `origen` a `destino` con el algoritmo de tres varillas. La varilla de los $k$ menores no se puede usar, porque todos sus discos son menores; quedan `origen`, `destino` y la otra auxiliar.
3. Llevar los $k$ menores de la auxiliar a `destino`, encima, otra vez con las cuatro varillas.

Si $FS(n)$ es el número de movimientos con el mejor $k$,

$$FS(0) = 0, \qquad FS(1) = 1, \qquad FS(n) = \min_{1 \le k < n}\bigl(2\,FS(k) + 2^{n-k} - 1\bigr).$$

**Es una cota superior.** Los tres pasos son secuencias legales: en los pasos 1 y 3 los discos mayores que $k$ no estorban, por la misma razón que en la «Pregunta 5» (las reglas solo comparan un disco con los menores), y en el paso 2 los $k$ menores están quietos en una varilla que no se usa. Así que con cuatro varillas el mínimo es a lo sumo $FS(n)$.

**Comparación con el mínimo exacto** (salida de [`ejercicio-14.py`](ejercicio-14.py), que además simula los movimientos y comprueba las reglas):

| $n$ | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 |
|---|---|---|---|---|---|---|---|---|---|
| Frame–Stewart | 1 | 3 | 5 | 9 | 13 | 17 | 25 | 33 | 41 |
| mínimo (BFS) | 1 | 3 | 5 | 9 | 13 | 17 | 25 | 33 | 41 |
| $k$ elegido | – | 1 | 1 | 1 | 2 | 3 | 3 | 4 | 5 |

El $k$ elegido es el menor que alcanza el mínimo de la recurrencia. Para $n \le 9$ el algoritmo hace exactamente el mínimo que da la búsqueda en anchura. Que coincida para todo $n$ no se demuestra aquí.

**Los incrementos.** El código comprueba hasta $n = 60$ que $FS(n) - FS(n-1) = 2^t$ cuando $t(t+1)/2 < n \le (t+1)(t+2)/2$: el incremento $2^t$ se repite $t + 1$ veces ($1$; $2, 2$; $4, 4, 4$; $8, \dots$). Por eso $FS(n)$ crece mucho más despacio que $2^n - 1$: con $n = 20$ son $289$ movimientos contra $1\,048\,575$.

---

## Verificación con código

El archivo [`ejercicio-14.py`](ejercicio-14.py) comprueba, con `assert` y sin azar:

1. el algoritmo y su traza para $n=3$;
2. el costo $T(n) = 2^n - 1 = 2T(n-1)+1$ para $n \le 12$;
3. $\mathrm{Pre}(n)$ al entrar y $\mathrm{Post}(n)$ al salir de **cada** llamada, incluido un subproblema con discos mayores ya colocados;
4. que la salida es un camino legal del estado inicial al final;
5. el oráculo: la búsqueda en anchura sobre los $3^n$ estados da el mínimo, y cuenta los caminos mínimos;
6. el Lema 2, en todos los estados legales;
7. el mínimo con cuatro varillas;
8. el algoritmo de Frame–Stewart: que sus movimientos son legales y que su número coincide con la recurrencia y con la búsqueda en anchura para $n \le 9$.

Resultados:

```
n = 3: 1:1->3 2:1->2 1:3->2 3:1->3 1:2->1 2:2->3 1:1->3
```

Costo del algoritmo:

| $n$ | movimientos | $2^n - 1$ | $2T(n-1)+1$ |
|---|---|---|---|
| 1 | 1 | 1 | 1 |
| 2 | 3 | 3 | 3 |
| 3 | 7 | 7 | 7 |
| 4 | 15 | 15 | 15 |
| 5 | 31 | 31 | 31 |
| 6 | 63 | 63 | 63 |
| 12 | 4095 | 4095 | 4095 |

Precondición y postcondición vigiladas con $n = 8$: en las $255$ llamadas se cumplen, y $247$ entran con otra varilla no vacía. En un subproblema con $n = 3$ y discos mayores en las tres varillas (`{1: [9, 8], 2: [7], 3: [6, 5, 3, 2, 1]}`) también se cumplen. Además, el algoritmo produce un camino legal hasta el estado final para $n \le 10$.

Búsqueda en anchura (oráculo):

| $n$ | estados $3^n$ | mínimo (BFS) | $2^n - 1$ | caminos mínimos | $2M(n-1)+1$ |
|---|---|---|---|---|---|
| 1 | 3 | 1 | 1 | 1 | 1 |
| 2 | 9 | 3 | 3 | 1 | 3 |
| 3 | 27 | 7 | 7 | 1 | 7 |
| 4 | 81 | 15 | 15 | 1 | 15 |
| 5 | 243 | 31 | 31 | 1 | 31 |
| 6 | 729 | 63 | 63 | 1 | 63 |
| 7 | 2187 | 127 | 127 | 1 | 127 |
| 8 | 6561 | 255 | 255 | 1 | 255 |
| 9 | 19 683 | 511 | 511 | 1 | 511 |
| 10 | 59 049 | 1023 | 1023 | 1 | 1023 |

Lema del disco grande: comprobado en los $3^n$ estados para $n \le 8$. Con $n = 8$ hay $6$ movimientos posibles del disco $8$ en todo el grafo, todos con los demás discos en la tercera varilla.

Mínimo con $4$ varillas por BFS, para $n = 1, \dots, 7$: $1, 3, 5, 9, 13, 17, 25$ (con $3$ varillas: $1, 3, 7, 15, 31, 63, 127$).

Frame–Stewart, para $n = 1, \dots, 9$: $1, 3, 5, 9, 13, 17, 25, 33, 41$ movimientos, igual que la búsqueda en anchura. Los incrementos siguen la regla de $2^t$ repetido $t + 1$ veces hasta $n = 60$, y $FS(20) = 289$.

El mínimo exacto calculado por fuerza bruta coincide con $2^n - 1$ en cada fila, que es lo que predicen a la vez el algoritmo (Teorema 2) y la cota (Teorema 3). La fuerza bruta explora $3^n$ estados, mientras que el algoritmo recursivo no explora ninguno: construye la solución directamente.

## Resumen de resultados

1. **Problema y modelo:** $n$ discos, tres varillas, movimientos legales; costo = número de movimientos.
2. **Algoritmo:** `hanoi(n)` mueve $n-1$ discos al auxiliar, el grande al destino y $n-1$ encima.
3. **Correctitud:** inducción con $\mathrm{Pre}(n)$ («los $n$ de arriba de `origen`; lo demás es mayor») y $\mathrm{Post}(n)$; terminación por el potencial $n$.
4. **Costo:** $T(n) = 2T(n-1) + 1 = 2^n - 1$, siempre.
5. **Cota mínima:** el disco $n$ solo se mueve con los otros $n-1$ en la tercera varilla; $M(n) \ge 2M(n-1)+1$, luego $M(n) \ge 2^n - 1$.
6. **Optimalidad:** $T(n) = M(n) = 2^n - 1$. La cota depende del modelo de tres varillas.
7. **Extensión:** con cuatro varillas, el algoritmo de Frame–Stewart hace $FS(n) = \min_k \bigl(2FS(k) + 2^{n-k} - 1\bigr)$ movimientos, el mínimo exacto para $n \le 9$.

## Referencias

- Conferencia 1, §7: por qué un algoritmo exponencial no se salva con más potencia de cómputo.
- Conferencia 2, §4 (fuerza bruta como oráculo), §10 (qué escondía el modelo) y §11 (las cinco preguntas del ciclo).
- Conferencia 3, §1: correctitud parcial, terminación, invariante y potencial.
- Conferencia 5, §5: adversario; el Lema 2 es un argumento del mismo tipo.
