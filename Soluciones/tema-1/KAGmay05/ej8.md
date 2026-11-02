## Problema 8
El elemento que aparece más de n/3 veces. Generaliza Boyer-Moore con dos candidatos, enuncia el invariante reforzado y demuéstralo. Después escribe la versión que devuelve los candidatos con contador positivo sin verificarlos, y busca un generador de pruebas que no la atrape. Cuidado: el
análogo del generador binario de la conferencia 3 sí la atrapa.

### Respuesta


### Primera idea: dos candidatos, reemplazar al de menor contador

Como puede haber hasta dos elementos que aparecen más de n/3 veces (tres no caben: sumarían más de n), hacen falta dos candidatos con dos contadores. La primera regla que se me ocurrió fue:

- si x coincide con un candidato, sumo en su contador;
- si x es distinto de los dos, reemplazo al candidato con menor contador por x;
- al final verifico contando, porque puede quedar un candidato que no cumpla.

La verificación final era correcta, pero la regla de reemplazo no. Contraejemplo (n = 11):

```
b b b a c a c a c a d
```

Solo a supera n/3 (4 > 11/3). b llega a contador 3 y se queda fijo; a y c se echan uno al otro del segundo puesto con contador 1, y al final entra d. Los candidatos finales son b y d, la verificación descarta a los dos y se pierde a. La verificación no puede rescatar a quien ya no está entre los candidatos.

El fallo de fondo: al reemplazar, el candidato echado pierde todo lo acumulado y el que se queda no "paga" nada por la llegada del elemento nuevo.

### Corrección: restar a los dos, reemplazar solo en cero

Volviendo al Boyer-Moore original (si llega uno distinto y el contador es positivo, se resta; solo se reemplaza cuando el contador es 0), la regla para dos candidatos queda:

1. Si x es igual a un candidato, sumo 1 en ese contador.
2. Si no, y algún contador está en 0, pongo x en ese puesto con contador 1.
3. Si no (x distinto de los dos y ambos contadores positivos), resto 1 a los dos y x no se guarda.

El orden importa: primero se pregunta por igualdad y después por el cero. Si se hiciera al revés, el mismo valor podría acabar ocupando los dos puestos.

```python
def candidatos(A):
    c1 = c2 = None
    k1 = k2 = 0
    for x in A:
        if x == c1:
            k1 += 1
        elif x == c2:
            k2 += 1
        elif k1 == 0:
            c1, k1 = x, 1
        elif k2 == 0:
            c2, k2 = x, 1
        else:
            k1 -= 1
            k2 -= 1
    return (c1, k1), (c2, k2)


def tercio(A):
    (c1, _), (c2, _) = candidatos(A)
    return sorted(c for c in {c1, c2}
                  if c is not None and 3 * A.count(c) > len(A))
```

Con el arreglo de antes, a sobrevive: los candidatos finales son d (1) y a (1), y la verificación devuelve [a].

---

## 2. Invariante reforzado

Es la misma idea de cancelación de la conferencia 3, pero con tríos en vez de parejas.

> Invariante. Después de procesar el prefijo A[0..i), ese prefijo se puede partir en
> - tríos de tres elementos distintos,
> - k1 copias de c1,
> - k2 copias de c2,
>
> y además c1 ≠ c2 (como valores, cuando no son None).

La parte "c1 ≠ c2" es el refuerzo que hace falta: sin ella, en el caso 3 no se podría asegurar que el trío formado sea de elementos distintos.

### Demostración

Inicialización. Prefijo vacío, k1 = k2 = 0: cero tríos y cero copias. c1 = c2 = None, que no es ningún elemento del arreglo.

c1 ≠ c2 se conserva siempre. Solo se asigna c1 := x o c2 := x en las ramas 2 y 3 del código (casos k1 == 0 y k2 == 0), y a ellas solo se llega si x ≠ c1 y x ≠ c2. Así que el valor nuevo nunca coincide con el otro candidato.

Mantenimiento. Supongamos el invariante para A[0..i) y procesemos x = A[i]. Un caso por rama:

- x = c1. k1 sube en 1 y x es una copia más de c1. (Si k1 era 0, antes había cero copias y ahora hay una.) Igual si x = c2.
- x distinto de ambos y k1 = 0. Como había cero copias del c1 viejo, reemplazarlo no deja nada colgado: la partición es la misma más una copia del nuevo c1 = x, con k1 = 1. Igual si k2 = 0.
- x distinto de ambos, k1 > 0 y k2 > 0. Formamos el trío {x, una copia de c1, una copia de c2}. Los tres son distintos: x ≠ c1, x ≠ c2 por la rama, y c1 ≠ c2 por el refuerzo. Quedan k1 − 1 y k2 − 1 copias, que es lo que el algoritmo deja en los contadores.

Al terminar, A completo se parte en t tríos de distintos, k1 copias de c1 y k2 copias de c2, con n = 3t + k1 + k2, así que t ≤ n/3.

Sea y un elemento que aparece más de n/3 veces. Si y no fuera un candidato con contador positivo, y solo aparecería dentro de los tríos, y a lo sumo una vez por trío (son distintos). En total, a lo sumo t ≤ n/3 veces. Contradicción.

Por lo tanto: todo elemento que aparece más de n/3 veces es uno de los candidatos y además tiene contador positivo. Esto garantiza que la segunda pasada no pierde a nadie.

Lo que el invariante no dice es lo contrario: que todo candidato con contador positivo sea frecuente. De ahí la sección siguiente.

---

## 3. La versión sin verificar (el atajo)

```python
def tercio_atajo(A):
    return sorted(c for c, k in candidatos(A) if k > 0)
```

Falla porque un contador positivo solo dice que sobraron copias tras cancelar tríos, no que haya más de n/3. Ejemplos:

| Entrada | Candidatos finales | Atajo devuelve | Correcto |
|---|---|---|---|
| `A A B` | A(2), B(1) | [A, B] | [A] (B aparece 1 = n/3, no más) |
| `b b b a c a c a c a d` | d(1), a(1) | [a, d] | [a] |

---

## 4. El generador que no la atrapa

### Por qué el análogo del binario sí la atrapa

En la conferencia 3 (mayoría, n/2), el generador binario no atrapaba al atajo: con solo dos símbolos, tras cancelar parejas lo único que queda son copias del candidato, y contador > 0 significa que el candidato aparece más que el otro símbolo, o sea, es mayoría. Con dos símbolos el atajo es correcto.

El análogo para dos candidatos sería generar con tres símbolos. Pero aquí ya no funciona. Con tres símbolos cada trío es exactamente {A, B, C}, así que cada símbolo aparece una vez por trío y

- apariciones de c1 = t + k1, con n = 3t + k1 + k2,
- c1 aparece más de n/3 veces ⟺ 3(t + k1) > 3t + k1 + k2 ⟺ 2·k1 > k2.

Es decir, que k1 sea positivo no basta; hace falta 2·k1 > k2. En A A B se tiene k_B = 1, k_A = 2, y 2·1 > 2 es falso, así que B tiene contador positivo pero no es frecuente. El atajo cae. (El binario también la atrapa, con el mismo ejemplo.)

### El generador: plantar dos frecuentes

```python
def dos_plantadas(n):
    m1, m2 = random.sample("ABCDE", 2)   
    k = n // 3 + 1                       
    if 2 * k > n:                        
        return [m1] * n
    A = [m1] * k + [m2] * k + [random.choice("ABCDE") for _ in range(n - 2 * k)]
    random.shuffle(A)
    return A
```

Por qué no la atrapa (demostración, no solo experimento). Si en A hay dos valores distintos que aparecen más de n/3 veces, por el invariante los dos son candidatos con contador positivo. Como solo hay dos puestos, no queda sitio para un candidato falso: el atajo devuelve exactamente esos dos, que es la respuesta correcta. Para n < 4 el generador devuelve un arreglo constante, con un único candidato positivo, y también acierta.

El generador "natural", que planta un elemento frecuente (el análogo de plantada), sí atrapa al atajo, porque deja libre el segundo puesto para un candidato falso. Hay que plantar dos.

### Resultados

Mismo experimento que en la conferencia (semilla 5, 4000 casos por generador, n entre 1 y 15), con el oráculo cambiado a n/3:

```python
def oraculo3(A):
    return sorted(x for x, k in Counter(A).items() if 3 * k > len(A))
```

| Generador | Atajo | Dos pasadas |
|---|---|---|
| una plantada | 47.4 % | 0.0 % |
| dos plantadas | 0.0 % | 0.0 % |
| binario | 33.8 % | 0.0 % |
| 3 símbolos | 37.7 % | 0.0 % |
| 4 símbolos | 44.9 % | 0.0 % |
| 5 símbolos | 50.2 % | 0.0 % |

Además lo comprobé exhaustivamente: la versión de dos pasadas acierta en todos los arreglos sobre {A, B, C, D} de longitud 1 a 8, y el atajo acierta en todos los arreglos (longitud 4 a 9) que tienen dos elementos frecuentes.

Moraleja: pasar las pruebas de dos plantadas al 100 % no dice nada de la corrección del atajo. El generador solo produce entradas donde el error no puede manifestarse.
