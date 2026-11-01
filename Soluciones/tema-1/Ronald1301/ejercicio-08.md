# Ejercicio 8 — El elemento que aparece más de $n/3$ veces

**Uso de IA:** Se usó IA para preparar y revisar este borrador, generar código y casos
de prueba, y apoyar la depuración. Parte de la explicación matemática también recibió
asistencia de IA; esas partes todavía no son redacción propia. Antes de entregar,
reescribiré y verificaré por mi cuenta las demostraciones, análisis de costo y cotas,
según la regla del curso.


> Generaliza Boyer-Moore con dos candidatos, enuncia el invariante reforzado y
> demuéstralo. Después escribe la versión que devuelve los candidatos con contador
> positivo **sin verificarlos**, y busca un generador de pruebas que **no** la atrape.
> Cuidado: el análogo del generador binario de la conferencia 3 sí la atrapa.


## 1. El problema

Dado un arreglo de $n$ elementos comparables solo por igualdad (C3, §2), devolver todos
los que aparecen **más de $n/3$ veces**. Puede haber **0, 1 o 2** de ellos (no caben
tres elementos que superen cada uno $n/3$). Queremos $O(n)$ tiempo y $O(1)$ memoria,
exactamente como Boyer-Moore pero con **dos** pares candidato-contador. Es el caso
$k=3$ del algoritmo de Misra-Gries (C3, ejercicio 2).

**Idea de cancelación generalizada** (C3, §2): si tacho **tres** elementos distintos a
la vez, cualquier elemento con más de $n/3$ copias sigue teniendo más de un tercio en
lo que queda. Con dos candidatos, "tres distintos" aparece cuando llega un elemento que
no coincide con ninguno de los dos candidatos vivos: se cancela una copia de cada uno.

## 2. El algoritmo

```python
def mas_de_n_tercios(A):
    # primera pasada: mantener 2 candidatos con cancelacion de a tres
    c1 = c2 = None
    k1 = k2 = 0
    for x in A:
        if c1 is not None and x == c1:
            k1 += 1
        elif c2 is not None and x == c2:
            k2 += 1
        elif k1 == 0:
            c1, k1 = x, 1
        elif k2 == 0:
            c2, k2 = x, 1
        else:                       # x distinto de ambos: cancelar uno de cada
            k1 -= 1
            k2 -= 1
    # segunda pasada: verificar
    res = []
    for c in {c1, c2} - {None}:
        if A.count(c) > len(A) // 3:
            res.append(c)
    return sorted(res, key=lambda v: (str(type(v)), v))
```

## 3. Invariante reforzado — guía para redactar la prueba (pendiente)

La demostración debes escribirla tú. Corrige el enunciado del invariante: cada tripleta
contiene tres valores distintos entre sí, pero no tiene que ser distinta de los
candidatos actuales.

Guía para la prueba:

1. Describe cómo cambia la partición cuando llega una copia de un candidato.
2. ¿Qué ocurre al llenar una posición cuyo contador está en cero? Recuerda que el valor
   anterior de esa posición tiene cero copias asignadas.
3. En la cancelación, ¿por qué los dos candidatos y el elemento nuevo son tres valores
   distintos?
4. Al terminar, usa $k_1+k_2+3T=n$. Si un valor mayoritario no fuera candidato,
   ¿cuántas copias suyas puede aportar cada tripleta? ¿Qué contradicción resulta?
## 4. Figura — cancelación de a tres

Arreglo A A B C A D A B A ($n=9$, umbral $>3$). Cada columna muestra el estado después
de procesar el elemento correspondiente.

~~~
paso:  1  2  3  4  5  6  7  8  9
x:     A  A  B  C  A  D  A  B  A
c1:    A  A  A  A  A  A  A  A  A
k1:    1  2  2  1  2  2  3  2  3
c2:    -  -  B  B  B  D  D  D  D
k2:    0  0  1  0  0  1  1  0  0
                 ↑        ↑     ↑
              C cancela  D llena  B cancela

Estado final: c1=A, k1=3; c2=D, k2=0.
Verificación exacta: A aparece 5 veces (>3); B aparece 2; D aparece 1.
Resultado correcto: [A].
~~~
## 5. La versión sin verificar y un generador que no la atrapa

La versión "atajo" devuelve los candidatos con contador positivo **sin** la segunda
pasada:

```python
def atajo_sin_verificar(A):
    c1 = c2 = None
    k1 = k2 = 0
    for x in A:
        if c1 is not None and x == c1: k1 += 1
        elif c2 is not None and x == c2: k2 += 1
        elif k1 == 0: c1, k1 = x, 1
        elif k2 == 0: c2, k2 = x, 1
        else: k1 -= 1; k2 -= 1
    return sorted({c for c, k in [(c1, k1), (c2, k2)] if c is not None and k > 0},
                  key=lambda v: (str(type(v)), v))
```

Es **incorrecta**: un contador positivo no implica superar $n/3$. El contraejemplo
mínimo A A B deja A y B con contador positivo; el atajo devuelve ambos, aunque solo A
aparece más de $n/3=1$ veces. El resultado correcto es [A].

**Generador que no atrapa.** Si siempre se plantan dos valores con más de $n/3$ copias,
ambos deben sobrevivir como candidatos; la rutina sin verificación devuelve esos dos
valores y no falla en esta familia. Esto no demuestra que el atajo sea correcto en
general.
## 6. Comprobación — el atajo pasa un generador plantado y falla con uno binario

~~~python
import random
def generador_que_no_atrapa(n, rng):
    """Planta dos valores con más de n/3 apariciones."""
    a, b = "X", "Y"
    cuota = n // 3 + 1
    arr = [a] * cuota + [b] * cuota
    arr += [rng.choice("PQRS") for _ in range(n - len(arr))]
    rng.shuffle(arr)
    return arr


def oraculo(A):
    from collections import Counter
    umbral = len(A) // 3
    return sorted({v for v, k in Counter(A).items() if k > umbral},
                  key=lambda v: (str(type(v)), v))

# (a) dos mayoritarios plantados: el generador no atrapa el atajo
rng = random.Random(3)
fallos_plantado = 0
for _ in range(20_000):
    n = rng.randint(6, 40)
    A = generador_que_no_atrapa(n, rng)
    fallos_plantado += atajo_sin_verificar(A) != oraculo(A)

# (b) generador binario de la conferencia 3: sí atrapa falsos positivos
rng_bin = random.Random(5)
fallos_binarios = 0
for _ in range(20_000):
    n = rng_bin.randint(1, 40)
    A = [rng_bin.choice("AB") for _ in range(n)]
    fallos_binarios += atajo_sin_verificar(A) != oraculo(A)

# (c) el generador de tres símbolos también atrapa
fallos_tres = 0
for _ in range(20_000):
    n = rng.randint(3, 40)
    A = [rng.choice("ABC") for _ in range(n)]
    fallos_tres += atajo_sin_verificar(A) != oraculo(A)

# El algoritmo que verifica los candidatos coincide con el oráculo.
ok = True
for _ in range(20_000):
    n = rng.randint(1, 40)
    A = [rng.choice("ABCDE") for _ in range(n)]
    ok &= mas_de_n_tercios(A) == oraculo(A)

print(f"atajo, generador plantado: {fallos_plantado} fallos de 20000")
print(f"atajo, generador binario: {fallos_binarios} fallos de 20000")
print(f"atajo, 3 símbolos: {fallos_tres} fallos de 20000")
print(f"algoritmo correcto (2 pasadas): sin fallos = {ok}")
~~~

**Salida** (semilla fija; ejecución local):

~~~text
atajo, generador plantado: 0 fallos de 20000
atajo, generador binario: 3813 fallos de 20000
atajo, 3 símbolos: 8976 fallos de 20000
algoritmo correcto (2 pasadas): sin fallos = True
~~~

El segundo candidato puede conservar un contador positivo aunque no supere $n/3$; por
eso el generador binario también encuentra fallos. El algoritmo completo vuelve a
contar las ocurrencias antes de devolverlos.
## 7. Resumen

- **Algoritmo:** Boyer-Moore con dos candidatos (Misra-Gries, $k=3$), $O(n)$ tiempo,
  $O(1)$ memoria, dos pasadas.
- **Invariante reforzado:** el prefijo se parte en $k_1$ copias de $c_1$, $k_2$ de
  $c_2$ y tripletas de distintos; prueba "si aparece $>n/3$, es candidato".
- **Atajo sin verificar:** incorrecto; un generador de "mayoría doble plantada" nunca
  lo atrapa, pero uno de tres símbolos uniformes sí — como anuncia la demostración.

