# Ejercicio 10: par más cercano en una dimensión

> Par más cercano en una dimensión. Demuestra Ω(n log n) en árboles de decisión algebraicos por reducción desde distinción de elementos. Después di qué algoritmo de la conferencia 2 rompe la cota, en qué modelo, y adáptalo a una dimensión. (C2, C5)

## Los problemas

**Par más cercano en 1D.** Dados n números reales (n puntos sobre una recta), hallar la menor distancia |xᵢ − xⱼ| entre dos de ellos. Con [7, 2, 11, 4], el par más cercano es 2 y 4, a distancia 2.

**Distinción de elementos.** Dados n números reales, decidir si hay dos iguales.

**Teorema (Ben-Or, 1983).** Distinción de elementos requiere Ω(n log n) en el modelo de árboles de decisión algebraicos: algoritmos que solo pueden hacer cuentas con los números de la entrada (sumar, restar, multiplicar) y ramificar según el signo del resultado.

## Parte 1: la cota Ω(n log n), por reducción

Si hay dos números iguales, están en el mismo punto de la recta y su distancia es 0: el par más cercano es ese par, con distancia 0. Con [7, 2, 7, 4], el par más cercano es 7 y 7. Y si todos son distintos, cualquier par está a distancia mayor que 0. Entonces:

> hay dos iguales ⟺ la distancia del par más cercano es 0.

**La reducción.** Para resolver distinción de elementos con un algoritmo de par más cercano: le paso la misma lista, sin cambiarla, y miro lo que devuelve. Si es 0, respondo "hay dos iguales"; si es mayor que 0, respondo "no". La transformación no cuesta nada y al final hay una sola comparación con 0, que es una prueba de signo permitida en el modelo.

**La cota.** Supongamos que el par más cercano se pudiera resolver en menos de n log n pasos (en o(n log n)) en este modelo. Le paso cualquier lista: si me devuelve 0 hay dos iguales, y si devuelve algo mayor que 0, no. Así respondería "¿hay dos iguales?" para cualquier lista en menos de n log n pasos, más una comparación. Eso es imposible por el teorema de Ben-Or. Entonces **el par más cercano en 1D requiere Ω(n log n)** en árboles de decisión algebraicos.

Ordenar y mirar los pares consecutivos (sección 3 de la conferencia 2) cuesta O(n log n), así que en este modelo ese algoritmo es óptimo.

## Parte 2: el algoritmo que rompe la cota

Es el **algoritmo incremental aleatorio de la rejilla** de la sección 9 de la conferencia 2 (Rabin; versión de Kleinberg y Tardos), con costo esperado O(n). No contradice la parte 1, porque la cota vale para un modelo, y este algoritmo hace cosas que el modelo no permite:

- **Calcula la parte entera ⌊x / lado⌋** para saber en qué caja cae un número. Eso no es una suma, ni una resta, ni una multiplicación, ni una comparación: no es un polinomio, y un árbol de decisión algebraico no la puede evaluar.
- **Usa ese resultado como dirección** en una tabla hash ("dame lo que hay en la caja 4"), y va directo a esa caja sin comparar con nada. Un árbol de decisión no tiene acceso indirecto: solo ramifica según signos.

Trabaja en el modelo **word RAM con parte entera y tablas hash**, y es aleatorio: el O(n) es el costo **esperado**, no el peor caso. Es como decir "nadie corre 100 metros en 5 segundos": la regla era corriendo, y en moto sí se puede.

## Parte 3: el algoritmo adaptado a una dimensión

**Idea.** En vez de comparar cada número con todos los demás, los guardo en cajitas por zona. Cuando llega un número nuevo, solo lo comparo con los de las cajas cercanas.

**Algoritmo.**

1. Mezclar los números al azar: x₁, …, xₙ.
2. δ = |x₁ − x₂|, la mejor distancia hasta ahora. (Si es 0, hay repetidos y termino.)
3. Cajas de lado δ/2: el número x va a la caja ⌊x / (δ/2)⌋, guardada en una tabla hash.
4. Para cada xᵢ, con i = 3, …, n:
   - calcular su caja c y mirar las **5 cajas** c − 2, …, c + 2;
   - si alguna tiene un número a distancia menor que δ, δ baja a esa distancia y se rehacen todas las cajas con el lado nuevo;
   - si no, xᵢ va a su caja.

**Ejemplo** con [3, 10, 6, 7.5, 1], ya mezclados:

- 3 y 10: δ = 7, cajas de lado 3.5. El 3 en la caja 0 y el 10 en la caja 2.
- Llega el 6, caja 1. Cerca están el 3 (distancia 3) y el 10 (distancia 4). Como 3 < 7, δ = 3 y se rehacen las cajas con lado 1.5: el 3 en la 2, el 6 en la 4 y el 10 en la 6.
- Llega el 7.5, caja 5. Cerca están el 6 (distancia 1.5) y el 10 (distancia 2.5). δ = 1.5, y se rehacen las cajas con lado 0.75.
- Llega el 1, caja 1. Las cajas cercanas están vacías, δ no cambia, y el 1 se queda en su caja.
- Resultado: δ = 1.5, entre el 6 y el 7.5.

**A lo sumo un número por caja.** Dos números en la misma caja están a distancia menor que δ/2, el lado de la caja, que es menor que δ. Pero δ es la distancia mínima entre los números ya metidos. Contradicción. Si aparece un par más cercano, el algoritmo baja δ y rehace las cajas, justamente para que esto siga siendo cierto.

**Por qué alcanzan 5 cajas.** Un número a distancia menor que δ de xᵢ puede estar hasta δ hacia la izquierda o hacia la derecha, y como cada caja mide δ/2, δ son dos cajas. Entonces está en la caja de xᵢ o a lo sumo dos cajas a cada lado. Si no aparece en esas 5, no existe: los números de las cajas lejanas están a más de δ. En el plano son 5 × 5 = 25 cajas, cinco en cada eje; en la recta, 5.

**Costo.** Cada inserción sin cambio de δ mira 5 cajas, cada una con a lo sumo un número: O(1). Rehacer las cajas en el paso i cuesta O(i). Por el análisis hacia atrás de la sección 9 de la conferencia 2, la probabilidad de rehacer en el paso i es a lo sumo 2/i: fijado el conjunto de los primeros i números, δ baja en el paso i solo si el último en llegar es uno de los dos del par más cercano. El costo esperado es entonces O(n) + Σ (2/i)·O(i) = O(n), con unas 2 ln n reconstrucciones en promedio.

## Experimentos

`ej10_par_cercano_1d.py` implementa la rejilla en 1D, el algoritmo de ordenar y la reducción a distinción de elementos. Los compara contra la fuerza bruta en 3000 instancias, con y sin números repetidos, sin fallos, y comprueba en cada paso que no hay dos números en la misma caja. Después cuenta las reconstrucciones y mide tiempos:

```
        n  reconstr.  2 ln n   rejilla   ordenar
    1,000       10.7    13.8    0.001s    0.000s
   10,000       19.0    18.4    0.006s    0.001s
  100,000       20.0    23.0    0.084s    0.020s
1,000,000       25.0    27.6    1.667s    0.310s
```

Las reconstrucciones siguen a 2 ln n, como predice el análisis. Pero en Python ordenar es más rápido que la rejilla en todos estos tamaños: `sorted` está escrito en C y la rejilla hace muchas operaciones de Python por número (parte entera, tabla hash, cinco consultas). El O(n) de la rejilla le gana al O(n log n) de ordenar solo cuando n es tan grande que el log n compensa esa diferencia de constantes. La cota mínima y el algoritmo que la rompe son afirmaciones sobre modelos; cuál es más rápido en una máquina concreta depende también de las constantes.

---
*Declaración de uso de IA: usé un asistente de IA (Claude) para escribir el código de experimentación, y como tutor (explicaciones, pistas y corrección de mi redacción). La reducción y las justificaciones son mías.*
