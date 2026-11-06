# Ejercicio 3: pila con mínimo en O(1)

> Una pila con una operación `minimo` que cuesta O(1) en el peor caso. Diseña la estructura, enuncia el invariante que la hace correcta y da el costo de cada operación. (C3)



## La estructura

Después de un `pop`, la pila queda exactamente igual que antes del último `push`, y en ese momento ya conocíamos el mínimo. Entonces guardo con cada elemento un número: el mínimo de todo lo que hay desde ese elemento hacia abajo, incluyéndolo. Cada nivel de la pila es un par (elemento, mínimo hasta aquí).

Numero los niveles desde el fondo: el nivel 1 es el fondo y el nivel k es el tope.

- `push(x)`: si la pila está vacía, apilo (x, x). Si no, sea m el segundo número del tope. Si x ≥ m, apilo (x, m); si x < m, apilo (x, x). O sea, apilo (x, mín(x, m)).
- `pop()`: quito el par del tope y devuelvo su elemento.
- `tope()`: devuelvo el elemento del par del tope.
- `minimo()`: devuelvo el segundo número del par del tope.



## Invariante

> Para cada nivel i de la pila, el segundo número del par en el nivel i es el mínimo de los elementos de los niveles 1, 2, …, i.

**Inicialización.** La pila vacía no tiene niveles, así que se cumple.

**Mantenimiento.** `tope` y `minimo` no cambian la pila. Quedan `push` y `pop`.

- `push(x)` sobre una pila de k niveles. Los niveles 1…k no cambian, así que siguen cumpliéndolo. Falta el nivel nuevo k + 1:
  - Si k = 0, el par es (x, x), y el mínimo del único nivel es x.
  - Si k ≥ 1, por el invariante m es el mínimo de los niveles 1…k. El mínimo de los niveles 1…k+1 es el menor entre ese mínimo y x, o sea mín(m, x). Hay dos casos: si x ≥ m, el mínimo hasta el nivel k + 1 es m; si x < m, es x. En los dos es lo que guarda el par nuevo.
- `pop()` sobre una pila de k niveles. Quita el nivel k. Lo que afirma el invariante para el nivel i solo depende de los niveles 1…i, y el pop no toca los niveles 1…k−1: ni sus pares ni los elementos que tienen debajo. Como el invariante ya se cumplía para ellos por hipótesis, se sigue cumpliendo.

**Conclusión.** `minimo()` devuelve el segundo número del tope, el nivel k. Por el invariante con i = k, es el mínimo de los niveles 1…k, que son toda la pila.

## Costo

Cada operación hace una cantidad fija de pasos: mirar el tope, una comparación y apilar o desapilar un par. Las cuatro cuestan **O(1) en el peor caso**, no amortizado. La memoria es O(k) para k elementos.

## Experimentos

`ej03_pila_minimo.py` implementa la estructura y la prueba de dos formas:

- 2000 secuencias al azar de push y pop, con valores entre −20 y 20. Después de cada operación comprueba el invariante en todos los niveles y compara `minimo()` con el mínimo calculado recorriendo la pila. No falla nunca.


```
40,701 operaciones al azar: invariante y minimo() correctos siempre
casos de borde (sacar el mínimo, mínimo repetido): correctos
```

---
*Declaración de uso de IA: usé un asistente de IA (Claude) para escribir el código y las pruebas, y como tutor (explicaciones, pistas y corrección de mi redacción). El diseño de la estructura y la demostración son míos.*
