# Ejercicio 8: el elemento que aparece más de n/3 veces

> Generaliza Boyer-Moore con dos candidatos, enuncia el invariante reforzado y demuéstralo. Después escribe la versión que devuelve los candidatos con contador positivo sin verificarlos, y busca un generador de pruebas que no la atrape. Cuidado: el análogo del generador binario de la conferencia 3 sí la atrapa. (C3)

Modelo: los elementos solo se comparan por igualdad, y queremos memoria O(1).

## Cuántas respuestas puede haber

Como máximo **dos** elementos aparecen más de n/3 veces. Si fueran tres, entre los tres sumarían más de n/3 + n/3 + n/3 = n votos, pero la lista tiene exactamente n. Por eso hacen falta dos candidatos (con la mayoría, más de n/2, el máximo era uno).

Ejemplo: en `A A B B C A B` (n = 7, n/3 ≈ 2.33), A y B aparecen 3 veces cada uno: los dos son respuesta.

## La idea: tachar ternas

Boyer-Moore tacha parejas de elementos distintos. Aquí se tachan **ternas de tres elementos distintos**. Si x aparece k > n/3 veces y tacho tres elementos distintos entre sí, a lo sumo uno de ellos es x. A x le quedan al menos k − 1 votos de n − 3, y k − 1 > n/3 − 1 = (n − 3)/3: sigue apareciendo más de un tercio en lo que queda.

## Algoritmo

```python
c1, k1 = None, 0
c2, k2 = None, 0
for x in A:
    if x == c1:
        k1 += 1                    # una copia más del candidato 1
    elif x == c2:
        k2 += 1                    # una copia más del candidato 2
    elif k1 == 0:
        c1, k1 = x, 1              # lugar libre: x pasa a ser candidato 1
    elif k2 == 0:
        c2, k2 = x, 1              # lugar libre: x pasa a ser candidato 2
    else:
        k1 -= 1                    # se tacha la terna (x, una copia de c1, una de c2)
        k2 -= 1
```

Segunda pasada: contar c1 y c2 en A y devolver los que aparecen más de n/3 veces.

Traza con `A A B B C A B`:

| elemento | (c1, k1) | (c2, k2) |
|---|---|---|
| A | (A, 1) | (–, 0) |
| A | (A, 2) | (–, 0) |
| B | (A, 2) | (B, 1) |
| B | (A, 2) | (B, 2) |
| C | (A, 1) | (B, 1) |
| A | (A, 2) | (B, 1) |
| B | (A, 2) | (B, 2) |

En el paso de la C se tacha la terna (C, una A, una B): la C que llega, una de las dos A acumuladas y una de las dos B. Al final quedan (A, 2) y (B, 2), y la segunda pasada cuenta 3 A y 3 B, los dos más de 7/3.

## Invariante reforzado

> Después de procesar un prefijo, ese prefijo se puede partir en **ternas de tres elementos distintos**, más **k1 copias de c1**, más **k2 copias de c2**. Además, si k1 > 0 y k2 > 0, entonces c1 ≠ c2.

**Inicialización.** El prefijo vacío: cero ternas, k1 = k2 = 0.

**Mantenimiento.** Llega x. Un caso por cada rama del `if`:

- **x = c1:** x es una copia más de c1, y k1 sube en 1.
- **x = c2:** igual con c2.
- **k1 = 0** (y x no es c2): en la partición no hay copias de c1, así que x pasa a ser la única copia del nuevo c1, con k1 = 1. Como x ≠ c2, sigue valiendo c1 ≠ c2.
- **k2 = 0** (y x no es c1): igual con c2.
- **else:** k1 > 0, k2 > 0 y x no es c1 ni c2. Se forma la terna nueva (x, c1, c2), con una de las copias de c1 y una de las de c2, que existen porque k1, k2 > 0. Sus tres elementos son distintos, porque ya preguntamos al inicio del `if` si x era c1 o c2, y c1 ≠ c2 por el invariante. Quedan k1 − 1 y k2 − 1 copias, que es lo que dejan los contadores.

**Conclusión.** Al terminar, A entero se parte en ternas de distintos, más k1 copias de c1 y k2 copias de c2. Supongamos que x aparece más de n/3 veces, pero no es c1 con k1 > 0 ni c2 con k2 > 0. Entonces x solo aparece dentro de las ternas, y en cada una como mucho una vez, porque sus elementos son distintos. Hay (n − k1 − k2)/3 ≤ n/3 ternas, así que x aparece como mucho n/3 veces. Contradicción.

> **Teorema.** Todo elemento que aparece más de n/3 veces es c1 o c2, con su contador positivo.

Con la segunda pasada, el algoritmo es correcto. Costo: dos pasadas, **O(n)** tiempo y **O(1)** memoria (dos candidatos y dos contadores).

## El atajo: devolver los candidatos sin verificar

```python
def atajo(A):
    c1, k1, c2, k2 = primera_pasada(A)
    return {c for c, k in ((c1, k1), (c2, k2)) if k > 0}
```

El teorema solo da una dirección: los que aparecen más de n/3 veces son candidatos con contador positivo. Lo contrario es falso: un candidato con contador positivo no tiene por qué aparecer más de n/3 veces.

- `A B C D`: se tacha la terna (A, B, C) y D queda con contador 1, pero aparece 1 vez de 4, no más de 4/3. El atajo devuelve {D}; la respuesta es {}.
- `A A A B`: como nunca hay tres elementos distintos, nunca se tacha una terna, y el atajo devuelve {A, B}. Pero B aparece 1 vez de 4, no más de n/3. Es el análogo del generador binario de la conferencia 3, y sí atrapa al atajo.

## Un generador incorrecto

El generador de mayoría plantada no atrapaba al atajo de Boyer-Moore, porque el teorema dice "si hay mayoría, es el candidato", y en esos arreglos siempre hay mayoría.

Aquí hay que plantar **dos** elementos con más de n/3 votos cada uno. Por el teorema, los dos terminan como c1 y c2, con contador positivo. Solo hay dos lugares, así que no queda ninguno para un candidato falso: el atajo se queda a la fuerza con los dos plantados, y esa es la respuesta correcta, porque no puede haber un tercero.

A diferencia de la conferencia 3, plantar uno solo no alcanza: el segundo lugar puede quedar ocupado por un candidato falso.

## Experimentos

`ej08_mas_de_un_tercio.py`:

- Comprueba el invariante reforzado en cada prefijo de 3000 arreglos al azar (23 792 prefijos). Para ver si un multiconjunto se parte en ternas de distintos, usa el análogo del lema de la conferencia 3: se parte si y solo si su tamaño es múltiplo de 3 y ningún elemento ocupa más de un tercio. Si se ordena y se agrupan las posiciones i, i + m, i + 2m (con m = tamaño/3), una terna con dos iguales significaría que ese elemento ocupa más de m posiciones seguidas.
- Compara el algoritmo verificado con el oráculo (contar todo): nunca falla.
- Mide con qué frecuencia falla el atajo con cada generador:

```
      generador   atajo  verificado
  dos plantados    0.0%        0.0%
   uno plantado   46.3%        0.0%
        binario   34.3%        0.0%
     3 símbolos   37.9%        0.0%
     5 símbolos   48.9%        0.0%
```

Con dos plantados el atajo es indistinguible del algoritmo correcto. Con todos los demás, incluido el binario y el de un solo plantado, falla en una fracción grande de los casos.

---
*Declaración de uso de IA: usé un asistente de IA (Claude) para escribir el código de experimentación, y como tutor (explicaciones de Boyer-Moore, pistas y corrección de mi redacción). El invariante, su demostración y el generador son míos.*
