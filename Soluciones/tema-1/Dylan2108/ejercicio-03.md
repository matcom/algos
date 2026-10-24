# Ejercicio 3: pila con `minimo` en $O(1)$

> ★ Una pila con una operación `minimo` que cuesta $O(1)$ en el peor caso. Diseña la
> estructura, enuncia el invariante que la hace correcta y da el costo de cada
> operación. (C3)

**Código:** [`ejercicio-03.py`](ejercicio-03.py). Tiene casos borde, 2000 secuencias
aleatorias con el invariante vigilado en cada paso y una variante con un error
plantado.

## Problema

Hay que mantener una pila de elementos de un orden total con estas operaciones:
`apilar(x)`, `desapilar()`, `tope()` y `minimo()`. Esta última devuelve el menor
elemento de la pila sin sacarlo. Cada operación tiene que costar $O(1)$ en el **peor
caso**, no amortizado. El modelo es el word RAM con comparaciones de costo 1.

## Idea

Recorrer la pila para hallar el mínimo cuesta $\Theta(n)$. Guardar solo una variable
con el mínimo actual tampoco basta, porque al desapilar el mínimo no sabemos cuál era
el anterior. La solución es que **cada celda recuerde el mínimo de la pila en el
momento en que se apiló**, es decir, el mínimo de ella misma y todo lo que tiene
debajo.

```python
class PilaMin:
    def __init__(self):
        self.celdas = []                      # pares (valor, mínimo hasta aquí)

    def apilar(self, x):
        m = x if not self.celdas else min(x, self.celdas[-1][1])
        self.celdas.append((x, m))

    def desapilar(self):
        return self.celdas.pop()[0]

    def tope(self):
        return self.celdas[-1][0]

    def minimo(self):
        return self.celdas[-1][1]
```

Un ejemplo de cómo queda la pila (el fondo está abajo):

```
apilar: 5, 3, 7, 3, 1

  tope →  │ 1 │ 1 │   ← minimo() = 1
          │ 3 │ 3 │
          │ 7 │ 3 │
          │ 3 │ 3 │
          │ 5 │ 5 │
          └───┴───┘
          valor  min
```

Si se desapila el 1, el nuevo tope dice que el mínimo es 3, y no hubo que buscar nada.

## Correctitud

Llamamos $v_0, \dots, v_{k-1}$ a los valores de la pila, de abajo arriba, y $m_i$ al
segundo componente de la celda $i$.

**Invariante.** $I: m_i = \min(v_0, \dots, v_i)$ para todo $0 \le i < k$.

**Inicialización.** La pila vacía cumple $I$ de forma trivial, porque no hay ningún
$i$.

**Mantenimiento.** Suponemos que se cumple $I$ y vemos que cada operación lo conserva.

- `apilar(x)` agrega la celda $k$ con $v_k = x$. Si la pila estaba vacía, $m_0 = x = \min(v_0)$. Si no, $m_k = \min(x, m_{k-1})$. Por $I$, $m_{k-1} = \min(v_0, \dots, v_{k-1})$, así que $m_k = \min(v_0, \dots, v_k)$. Las celdas de abajo no cambian, así
  que su parte de $I$ sigue cumpliéndose.
- `desapilar()` quita la celda $k-1$. $I$ habla de cada celda por separado y solo
  menciona lo que tiene debajo, así que quitar el tope no afecta a ninguna de las que
  quedan.
- `tope()` y `minimo()` no modifican nada.

**Conclusión.** Con $k \ge 1$, `minimo()` devuelve $m_{k-1} = \min(v_0, \dots, v_{k-1})$, que es el mínimo de toda la pila. La terminación es inmediata, porque
ninguna operación tiene ciclos.

### Por qué el invariante tiene que hablar de cada celda

La propiedad que queremos es "$m_{k-1}$ es el mínimo de la pila". Es verdadera, pero
sola **no es inductiva**. Al desapilar, la afirmación sobre el nuevo tope no se puede
deducir de la afirmación sobre el tope anterior. Para que la demostración funcione hay
que reforzarla a "**todas** las celdas cumplen lo mismo para su prefijo", que es $I$.
Es lo mismo que pasa con Boyer-Moore en la sección 4 de la conferencia 3: el invariante tiene que
ser inductivo, no solo verdadero.

## Costo

| operación   | comparaciones | tiempo (peor caso) |
|-------------|---------------|--------------------|
| `apilar`    | ≤ 1           | $O(1)$             |
| `desapilar` | 0             | $O(1)$             |
| `tope`      | 0             | $O(1)$             |
| `minimo`    | 0             | $O(1)$             |

La memoria es de $2k$ palabras para $k$ elementos.

**Un detalle del peor caso.** El `append` de una lista de Python cuesta $O(1)$
*amortizado*, porque cada cierto tiempo copia todo el arreglo a uno más grande
(conferencia 4). Para tener $O(1)$ en el peor caso, como pide el enunciado, la pila
debe ser una lista enlazada de celdas (cada `apilar` crea un nodo que apunta al
anterior) o un arreglo con capacidad máxima reservada de antemano. El invariante y la
demostración son los mismos en los dos casos.

## Pruebas

**Casos borde a mano.** En el script hay una pila vacía, una de un solo elemento,
mínimos repetidos (`5 3 7 3 1 1 9`) y desapilar hasta vaciar.

**Invariante vigilado.** Se generan 2000 secuencias aleatorias de 60 operaciones. En
cada paso se comprueba `minimo()` contra `min(lista)` y se recorre la pila completa
para verificar $I$. No hubo ningún fallo.

## El error que la demostración anuncia

Hay una variante muy conocida que ahorra memoria. Usa una pila auxiliar `mins` que solo
recibe un elemento cuando aparece un **nuevo** mínimo. Al desapilar, si el valor que
sale es igual al tope de `mins`, también se desapila de `mins`. La pregunta es si la
condición para apilar en `mins` debe ser `x < mins[-1]` o `x <= mins[-1]`.

El paso de la demostración que hay que mirar es el de `desapilar`. Ahí se quita de
`mins` cada vez que sale un valor igual a su tope. Para que eso sea correcto, cada copia
del mínimo que está en la pila tiene que tener su propia entrada en `mins`. Con `<`, un
mínimo repetido se apila una sola vez en `mins` pero se desapila de ahí con la primera
copia que sale. La demostración nos dice entonces qué probar: valores repetidos.

El contraejemplo más chico es `apilar(1), apilar(1), desapilar()`. La pila todavía
tiene un 1, pero `mins` quedó vacía y `minimo()` falla.

Las pruebas lo detectan o no según el generador. Estos son los porcentajes de
secuencias que fallan, sobre 2000 secuencias de 60 operaciones:

| generador                           | variante con `<` | con `<=` |
|-------------------------------------|------------------|----------|
| valores distintos (rango $10^9$)    | **0,0 %**        | 0        |
| valores en $0..99$                  | 20,2 %           | 0        |
| valores en $0..9$                   | 89,5 %           | 0        |
| valores en $\lbrace 0, 1 \rbrace$               | 100 %            | 0        |

Si uno prueba con números aleatorios grandes, que es lo primero que se escribe, la
variante pasa siempre, porque casi nunca hay repetidos. El error solo aparece cuando se
genera justo la estructura que la demostración señala.

## Nota: por qué `minimo` sí y `extraer_minimo` no

Es razonable preguntar si también se puede *extraer* el mínimo en $O(1)$. En el modelo
de comparaciones no se puede. Con `apilar` y `extraer_minimo` en $O(1)$ cada uno,
$n$ inserciones y $n$ extracciones ordenarían $n$ elementos en $O(n)$ comparaciones, y
eso contradice la cota $\Omega(n \log n)$ de la conferencia 5. Nuestra estructura puede
tener `minimo` en $O(1)$ porque solo **consulta** el mínimo, y lo que se saca siempre
es el tope, no el menor.
