# Ejercicio 12: Gale-Shapley con listas incompletas

> ★★★ Gale-Shapley con listas incompletas: cada proponente lista solo a algunos
> receptores, y prefiere quedarse solo antes que con uno que no listó. Adapta el
> algoritmo, su potencial y la definición de pareja bloqueante. ¿Sigue siendo
> estable el resultado? Demuéstralo. (C3)

**Código:** [`ejercicio-12.py`](ejercicio-12.py). Prueba el algoritmo adaptado en 3000
instancias contra una fuerza bruta que enumera todos los emparejamientos estables, con
tres órdenes de ejecución y el potencial vigilado. Además muestra que el algoritmo
original se cae con listas incompletas, y que la definición vieja de pareja
bloqueante no ve los errores de esta versión.

**Respuesta corta:** sí, el resultado sigue siendo estable, con la definición de
pareja bloqueante adaptada. Hay que cambiar tres cosas: un proponente que agota su
lista se queda solo, el potencial cuenta las propuestas que quedan en las listas (no
$n^2$), y una pareja bloqueante puede incluir a alguien que está solo.

## El problema

Hay proponentes $a$ y receptores $b$, no necesariamente la misma cantidad. Cada
proponente $a$ tiene una lista $L(a)$ con **algunos** receptores, ordenada de mejor a
peor. Los receptores que no están en $L(a)$ son **inaceptables** para $a$: prefiere
quedarse solo antes que estar con ellos. Cada receptor ordena a los proponentes de
mejor a peor, como en la conferencia 3.

El script trata también el caso más general en que los receptores tienen listas
incompletas. Lo único que cambia es que un receptor rechaza a quien no está en su
lista. Todo lo que sigue vale igual, y lo señalo donde hace falta.

**Emparejamiento.** Ya no puede ser perfecto: si $a$ solo lista a $b_1$ y $b_1$ prefiere
a otro, $a$ se queda solo. Un emparejamiento $M$ es ahora un conjunto de parejas
$(a, b)$ donde cada uno aparece a lo sumo una vez y **cada pareja es aceptable**:
$b \in L(a)$. Escribimos $M(a)$ para la pareja de $a$, y $M(a) = \text{solo}$ si no tiene.
Para $a$, estar solo es peor que cualquier receptor de su lista y mejor que
cualquiera que no esté en ella.

## La nueva definición de pareja bloqueante

**Definición.** $(a, b)$ es una **pareja bloqueante** de $M$ si $b \in L(a)$, $(a, b)$
no está en $M$, y:

1. $a$ está solo, o prefiere $b$ a $M(a)$; y
2. $b$ está solo, o prefiere $a$ a $M(b)$.

(En el caso general se pide también que $a$ esté en la lista de $b$.) $M$ es
**estable** si no tiene parejas bloqueantes.

Respecto de la conferencia 3 cambian dos cosas, y las dos vienen de la frase "prefiere
quedarse solo":

- **Las parejas inaceptables quedan prohibidas.** Si $M$ pusiera a $a$ con un $b$ que
  no listó, $a$ preferiría romper y quedarse solo. Ese es un bloqueo de una sola
  persona. Por eso exigimos que todas las parejas de $M$ sean aceptables.
- **Estar solo cuenta.** En la conferencia 3 todos tenían pareja, así que "prefiere
  $b$ a su pareja" siempre tenía sentido. Ahora una pareja bloqueante puede estar
  formada por dos personas solas que se aceptan, o por una persona sola y otra que la
  prefiere a su pareja. Si la definición solo mirara a los que tienen pareja, esos
  bloqueos no se verían. La última sección muestra un error que **solo** produce bloqueos
  de ese tipo.

## El algoritmo adaptado

```python
def gale_shapley(pref_a, pref_b):
    rango = [{a: lugar for lugar, a in enumerate(lista)} for lista in pref_b]
    siguiente = [0] * len(pref_a)
    pareja_de_b = [None] * len(pref_b)
    libres = deque(a for a in range(len(pref_a)) if pref_a[a])   # (1)
    while libres:
        a = libres.popleft()
        b = pref_a[a][siguiente[a]]
        siguiente[a] += 1
        actual = pareja_de_b[b]
        if a not in rango[b]:                                     # (2)
            rechazado = a
        elif actual is None or rango[b][a] < rango[b][actual]:
            pareja_de_b[b], rechazado = a, actual
        else:
            rechazado = a
        if rechazado is not None and siguiente[rechazado] < len(pref_a[rechazado]):
            libres.append(rechazado)                              # (3)
    ...
```

Los cambios respecto de la conferencia 3 están marcados:

1. Un proponente con la lista vacía ni siquiera entra a la cola: se queda solo.
2. En el caso general, un receptor rechaza a quien no está en su lista. Si las listas
   de los receptores son completas, esta rama nunca se usa.
3. **El cambio importante.** Un proponente rechazado o desplazado vuelve a la cola
   solo si le quedan receptores en su lista. Si ya le propuso a todos, se queda solo,
   porque prefiere eso a cualquiera que no listó.

### Un ejemplo

$a_0$ lista $b_0, b_1$; $a_1$ lista solo $b_0$; $a_2$ lista $b_0, b_1$. El receptor
$b_0$ prefiere $a_1 > a_2 > a_0$, y $b_1$ prefiere $a_0 > a_2 > a_1$.

| paso | propone | a quién | tenía | se queda con | qué pasa |
|---|---|---|---|---|---|
| 1 | a0 | b0 | nadie | a0 | acepta |
| 2 | a1 | b0 | a0 | a1 | cambia; a0 vuelve a la cola (le queda b1) |
| 3 | a2 | b0 | a1 | a1 | rechaza; a2 vuelve a la cola (le queda b1) |
| 4 | a0 | b1 | nadie | a0 | acepta |
| 5 | a2 | b1 | a0 | a0 | rechaza; a2 agotó su lista y se queda solo |

Resultado: $a_0$–$b_1$, $a_1$–$b_0$ y $a_2$ solo, en 5 propuestas. Es estable. $a_2$
está solo, pero los dos receptores que acepta prefieren a su pareja actual antes que a
él: $b_0$ tiene a $a_1$, que prefiere a $a_2$, y $b_1$ tiene a $a_0$, que también.

## Los invariantes

Son los de la conferencia 3, más uno nuevo:

- **I1.** Un receptor, una vez que acepta a alguien, nunca vuelve a quedar solo, y su
  pareja solo mejora. Solo cambia de pareja si llega alguien que prefiere.
- **I2.** Cada proponente propone en el orden de su lista, de mejor a peor, y nunca
  repite una propuesta, porque `siguiente[a]` solo avanza.
- **I3 (nuevo).** Todas las parejas son aceptables: $b$ solo puede tener como pareja a
  alguien que le propuso, y $a$ solo le propone a receptores de $L(a)$. (En el caso
  general, la rama (2) asegura además que $a$ esté en la lista de $b$.)
- **I4 (nuevo).** Todo proponente que está en la cola tiene $\text{siguiente}[a] < |L(a)|$,
  es decir, le queda al menos un receptor por proponer. Al principio vale por (1),
  porque solo entran los que tienen lista no vacía, y se mantiene por (3), porque solo
  se vuelve a encolar a quien le quedan receptores.

## Terminación: el potencial adaptado

En la conferencia 3, $\Phi$ era la cantidad de pares $(a, b)$ tales que $a$ todavía no
le propuso a $b$, que empezaba en $n^2$. Ahora $a$ solo le puede proponer a los de su
lista, así que

$$\Phi = \sum_a \big(|L(a)| - \text{siguiente}[a]\big) = \text{propuestas que quedan por hacer}.$$

- **Empieza** en $\ell = \sum_a |L(a)|$, el largo total de las listas, que puede ser mucho
  menor que $n^2$.
- **Baja exactamente 1** en cada vuelta del ciclo, porque cada vuelta hace una
  propuesta y `siguiente[a]` avanza en 1.
- **Nunca es negativo**, porque `siguiente[a]` no pasa de $|L(a)|$: por I4, cuando $a$
  propone todavía le quedan receptores.

Por lo tanto el ciclo termina después de a lo sumo $\ell$ propuestas. El script
verifica en cada propuesta que $\Phi$ bajó exactamente 1 y sigue siendo $\ge 0$.

**El lema que se rompe.** La conferencia 3 tenía que demostrar que "`siguiente[a]` nunca
se sale de la lista", y lo hacía así: si $a$ quedara libre después de proponerle a los
$n$ receptores, los $n$ estarían comprometidos con $n$ proponentes distintos, pero $a$
está libre. Esa demostración **usa que $a$ le propuso a todos los receptores**, es
decir, que su lista es completa. Con listas incompletas el lema es falso: un
proponente puede agotar su lista y quedar libre. Por eso el algoritmo original se cae.
El script corre el código de la conferencia 3 en instancias de $5 \times 5$ con listas
incompletas, y **en el 62,6 % se cae con `IndexError`**, al leer más allá del final de
una lista. El cambio (3) e I4 reemplazan a ese lema.

**Costo.** Cada propuesta cuesta $O(1)$, con el rango de cada receptor en un diccionario.
El total es $O(\ell)$ propuestas, más el trabajo de armar los rangos, que es lineal en
el largo de las listas de los receptores. Es lineal en el tamaño de la entrada:

```
    n   largo de cada lista  cota Σ|L(a)|  propuestas       n²
   10                     3            30          18      100
   10                     5            50          17      100
  100                     3           300         196    10000
  100                    50          5000         380    10000
 1000                     3          3000        1832  1000000
 1000                   500        500000        5474  1000000
```

## Estabilidad

**Teorema.** El emparejamiento $M$ que devuelve el algoritmo adaptado es estable, para
cualquier orden de ejecución.

*Demostración.* Por I3, todas las parejas de $M$ son aceptables. Falta ver que no hay
parejas bloqueantes. Supongamos que $(a, b)$ lo es: $b \in L(a)$, $a$ está solo o
prefiere $b$ a $M(a)$, y $b$ está solo o prefiere $a$ a $M(b)$.

**Paso 1: $a$ le propuso a $b$.** Hay dos casos.
- Si $a$ terminó con pareja $M(a)$ y prefiere $b$, entonces $b$ está antes que $M(a)$ en
  $L(a)$. Por I2, $a$ le propuso a $b$ antes que a $M(a)$.
- Si $a$ terminó solo, el ciclo terminó sin que $a$ estuviera en la cola. Si tenía la
  lista vacía, no puede ser $b \in L(a)$. Si no, $a$ estuvo en la cola, y la única forma
  de salir para siempre es el cambio (3): lo rechazaron o desplazaron cuando ya no le
  quedaban receptores. Así que le propuso a toda su lista, y en particular a $b$.

**Paso 2: después de esa propuesta, $b$ tuvo siempre a alguien mejor que $a$.** Cuando
$a$ le propuso a $b$, $b$ lo rechazó en ese momento o lo aceptó y más tarde lo cambió.
(En el caso general, si $b$ lo rechazó por no tenerlo en su lista, $(a, b)$ no es
aceptable para $b$ y no puede bloquear.) En los dos casos fue porque $b$ tenía o
recibió a alguien que prefería a $a$. Por I1, desde ese momento $b$ nunca vuelve a
estar solo y su pareja solo mejora. Así que al final $b$ tiene pareja, y prefiere
$M(b)$ a $a$.

Esto contradice la condición 2 de la pareja bloqueante: $b$ no está solo y no prefiere
$a$ a $M(b)$. $\square$

La demostración es la de la conferencia 3 con un caso más en el paso 1: el de $a$ solo.
Ese caso es justo el que necesita el cambio (3): $a$ solo se queda fuera de la cola
**después** de proponerle a toda su lista.

## Otras propiedades, comprobadas por fuerza bruta

El script enumera **todos** los emparejamientos estables de cada instancia (hasta
$5 \times 5$) y verifica tres cosas más en las 3000 instancias:

- **No depende del orden.** Con cola, con pila y al azar sale el mismo emparejamiento.
- **Es óptimo para los proponentes**, como en la sección 9 de la conferencia 3: cada proponente
  tiene en $M$ la mejor pareja que tiene en cualquier emparejamiento estable.
- **Los que se quedan solos son siempre los mismos.** En todos los emparejamientos
  estables de una instancia, el conjunto de personas sin pareja es el mismo. Se conoce
  como el teorema de los hospitales rurales (Gale y Sotomayor, 1985; Roth, 1986). Aquí
  solo lo verificamos en instancias chicas, no lo demostramos.

## El error que la nueva definición atrapa

Un error fácil de cometer al adaptar el código: cuando un receptor cambia de pareja,
olvidarse de volver a poner en la cola al desplazado. El script lo prueba en 2000
instancias de $5 \times 5$ con las dos definiciones de pareja bloqueante:

| verificador | emparejamientos inestables que detecta |
|---|---|
| definición nueva (cuenta a los que están solos) | 892 de 892 (100 %) |
| definición de la conferencia 3 (solo mira a los que tienen pareja) | 0 de 892 (0 %) |

La definición vieja no ve **ninguno**. El error siempre produce lo mismo: un proponente
desplazado que queda solo aunque todavía tiene receptores en su lista, y la pareja
bloqueante que eso crea siempre incluye a alguien solo. El contraejemplo más chico:

- $a_0$ lista $b_0, b_1$; $a_1$ lista $b_0$; $b_0$ prefiere $a_1$ a $a_0$; $b_1$ solo
  acepta a $a_0$.
- $a_0$ le propone a $b_0$, que acepta. $a_1$ le propone a $b_0$, que cambia a $a_0$ por
  $a_1$, y $a_0$ queda olvidado.
- Resultado: $a_1$–$b_0$, y $a_0$ y $b_1$ solos. $(a_0, b_1)$ es una pareja bloqueante:
  los dos están solos y se aceptan. El algoritmo correcto los empareja.

Es la misma lección de la sección 5 de la conferencia 3: la demostración dice qué probar. El caso
nuevo de la demostración de estabilidad es "$a$ terminó solo", y las pruebas tienen
que mirar justo a los que terminan solos.

## Resumen

| | |
|---|---|
| Emparejamiento | ya no es perfecto; todas las parejas tienen que ser aceptables |
| Pareja bloqueante | (a, b) aceptable, y cada uno está solo o prefiere al otro |
| Cambio en el algoritmo | quien agota su lista sale de la cola y se queda solo |
| Potencial | Φ = propuestas que quedan en las listas; empieza en el largo total de las listas y baja 1 por propuesta |
| Lema que se rompe | "siguiente[a] no se sale de la lista": el original se cae en el 62,6 % |
| ¿Estable? | sí; la demostración agrega el caso "a terminó solo" |
| Además | no depende del orden, óptimo para proponentes, los solos son siempre los mismos |
| Error plantado | olvidar al desplazado: la definición vieja no lo detecta nunca |
