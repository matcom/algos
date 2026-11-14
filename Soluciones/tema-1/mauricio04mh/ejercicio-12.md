# Ejercicio 12. Gale–Shapley con listas incompletas

Dificultad: ★★★ · Código: [`ejercicio-12.py`](ejercicio-12.py)

---

## Enunciado

> Gale–Shapley con listas incompletas: cada proponente lista solo a algunos receptores, y prefiere quedarse solo antes que con uno que no listó. Adapta el algoritmo, su potencial y la definición de pareja bloqueante. ¿Sigue siendo estable el resultado? Demuéstralo.

## Qué se pide

1. Adaptar el algoritmo de aceptación diferida a listas incompletas.
2. Adaptar el **potencial** y demostrar la terminación.
3. Adaptar la definición de **pareja bloqueante**.
4. Demostrar que el resultado es estable.

**Mapa.** Se parte del algoritmo de Gale–Shapley de la Conferencia 3 y se cambia lo mínimo para que admita listas incompletas. Después hay tres demostraciones, una por cada pregunta del enunciado: (1) con un **potencial**, que el algoritmo termina; (2) con la nueva definición de **pareja bloqueante**, qué significa que un emparejamiento sea estable ahora que hay gente sin pareja; (3) por contradicción, que el resultado es **estable**.

## Preliminares

**Datos.**

- Hay $n$ proponentes y $n$ receptores.
- Cada proponente $a$ tiene una lista $L_a$ de algunos receptores, de mejor a peor. Los que no están en $L_a$ son **inaceptables** para $a$.
- Cada receptor ordena a **todos** los proponentes (como en la Conferencia 3).

**Emparejamiento.** Cada proponente tiene a lo sumo un receptor y cada receptor a lo sumo un proponente. Una pareja $(a,b)$ solo es válida si $b \in L_a$. **Puede quedar gente sin pareja**: con listas completas todos terminaban emparejados, ahora un proponente puede quedarse solo.

**Reglas sobre quedarse solo.**

1. Un proponente prefiere estar solo antes que con alguien que no listó.
2. Un receptor libre acepta a cualquiera que le proponga: prefiere cualquier proponente a quedarse solo.

**Notación.** Para un emparejamiento $M$, $M(a)$ es el receptor de $a$ (o «nadie») y $M(b)$ el proponente de $b$ (o «nadie»).

**Gale–Shapley con listas completas** (Conferencia 3, §7–§9). Los proponentes proponen de su favorito hacia abajo; un receptor se queda con la mejor propuesta recibida. El potencial es el número de pares $(a,b)$ a los que $a$ todavía no ha propuesto (§7); la estabilidad se demuestra por contradicción (§8); y la optimalidad para quien propone, con el argumento del primer fallo, implica que el resultado es el mismo en cualquier orden de ejecución (§9).

**Ejemplo A.** Con $a_1: [b_1]$ y $a_2: [b_1, b_2]$, y ambos receptores prefiriendo $a_1$ sobre $a_2$:

1. $a_1$ propone a $b_1$: libre, acepta.
2. $a_2$ propone a $b_1$: $b_1$ prefiere a $a_1$, rechaza.
3. $a_2$ propone a $b_2$: libre, acepta.

Resultado: $a_1$–$b_1$ y $a_2$–$b_2$.

**Ejemplo B.** Con $a_1: [b_1]$ y $a_2: [b_1]$, y $b_1$ prefiriendo $a_2$ sobre $a_1$:

1. $a_1$ propone a $b_1$: acepta.
2. $a_2$ propone a $b_1$: prefiere a $a_2$, deja a $a_1$ y acepta a $a_2$.
3. $a_1$ queda libre y **ya no tiene a quién proponer**: su lista se acabó.

Resultado: $a_2$–$b_1$; $a_1$ se queda solo (también $b_2$, al que nadie propuso).

---

## El algoritmo adaptado

Los ejemplos A y B muestran el único cambio que hace falta: en el B, $a_1$ se queda sin receptores a quienes proponer y el algoritmo tiene que saber parar.

La única diferencia: un proponente libre cuya lista se agotó **deja de proponer y se queda soltero**.

```python
def gale_shapley_incompleto(listas_a, pref_b):
    # listas_a[a]: receptores aceptables para a, de mejor a peor
    # pref_b[b]:   todos los proponentes, de mejor a peor
    n = len(listas_a)
    rango = [[0] * n for _ in range(n)]
    for b in range(n):
        for lugar, a in enumerate(pref_b[b]):
            rango[b][a] = lugar
    siguiente = [0] * n                 # a quién le propone a a continuación
    pareja_de_b = [None] * n
    libres = list(range(n))
    while libres:
        a = libres.pop()
        if siguiente[a] == len(listas_a[a]):
            continue                    # lista agotada: a se queda solo
        b = listas_a[a][siguiente[a]]
        siguiente[a] += 1
        actual = pareja_de_b[b]
        if actual is None:
            pareja_de_b[b] = a
        elif rango[b][a] < rango[b][actual]:
            pareja_de_b[b] = a
            libres.append(actual)
        else:
            libres.append(a)
    return pareja_de_b
```

La línea nueva es `if siguiente[a] == len(listas_a[a]): continue`. Con listas completas esa situación era imposible; ahora es normal.

**Ejemplo con tres proponentes.** $a_1: [b_1]$, $a_2: [b_1, b_2]$, $a_3: [b_1]$, y $b_1$ prefiere $a_3 > a_2 > a_1$. Para la traza se elige siempre al libre situado más a la izquierda de la lista, que es `orden="cola"` en [`ejercicio-12.py`](ejercicio-12.py); el código de arriba toma el último (empieza en $a_1, a_2, a_3$):

| iteración | quién actúa | qué pasa | libres después |
|---|---|---|---|
| 1 | $a_1$ | propone a $b_1$, libre, acepta | $a_2, a_3$ |
| 2 | $a_2$ | propone a $b_1$, que lo prefiere a $a_1$; $a_1$ queda libre | $a_3, a_1$ |
| 3 | $a_3$ | propone a $b_1$, que lo prefiere a $a_2$; $a_2$ queda libre | $a_1, a_2$ |
| 4 | $a_1$ | su lista se agotó: se queda solo | $a_2$ |
| 5 | $a_2$ | propone a $b_2$, libre, acepta | (ninguno) |

Resultado: $a_3$–$b_1$, $a_2$–$b_2$ y $a_1$ solo.

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="figuras/ejercicio-12-emparejamiento-oscuro.svg">
  <img src="figuras/ejercicio-12-emparejamiento-claro.svg" alt="Pares aceptables y parejas del resultado en el ejemplo con tres proponentes">
</picture>

**Figura 1.** El resultado del ejemplo. Las líneas son los pares aceptables (los de las listas $L_a$) y las gruesas son las parejas: $a_3$–$b_1$ y $a_2$–$b_2$. $a_1$ agotó su lista y queda solo, y $b_3$ no está en ninguna lista.

---

## El potencial y la terminación

La primera pregunta es si el algoritmo adaptado termina siempre. Se responde como en la Conferencia 3, con un potencial que baja en cada iteración.

Con listas completas, el potencial era el número de propuestas que faltan. Ahora hay iteraciones que no proponen nada (la del proponente con la lista agotada), así que hay que contar también a los libres.

**Definición.**

$$\Phi = \sum_a \bigl(|L_a| - \text{siguiente}[a]\bigr) + |\text{libres}|.$$

El primer sumando cuenta las propuestas que faltan; el segundo, los proponentes libres.

**Teorema 1.** Para cualquier orden de elección, $\Phi$ es un entero $\ge 0$ que baja al menos $1$ en cada iteración, y empieza en $\Phi_0 = \sum_a |L_a| + n \le n^2 + n$. Por tanto el algoritmo termina en a lo sumo $n^2 + n$ iteraciones, es decir, $O(n^2)$.

**Demostración.** Cada iteración saca un proponente $a$ de `libres`.

**Caso 1: la lista de $a$ está agotada.**

**Paso 1.** No se propone nada y $a$ no vuelve a `libres`.

**Paso 2.** La suma de propuestas que faltan no cambia y $|\text{libres}|$ baja en $1$.

**Paso 3.** $\Phi$ baja en $1$.

**Caso 2: $a$ propone.**

**Paso 1.** $\text{siguiente}[a]$ sube en $1$: la suma baja en $1$.

**Paso 2.** $|\text{libres}|$ baja en $1$ al sacar a $a$, y sube en $1$ si alguien (el propio $a$ o su pareja anterior) queda libre; en el peor caso no cambia.

**Paso 3.** $\Phi$ baja al menos $1$.

Como $\Phi$ es un entero $\ge 0$ y baja al menos $1$ en cada iteración, el algoritmo termina. Al inicio, $\text{siguiente}[a] = 0$ y todos están libres: $\Phi_0 = \sum_a |L_a| + n \le n\cdot n + n$. $\blacksquare$

**Comprobación** (ejemplo de tres proponentes): $\sum |L_a| = 1 + 2 + 1 = 4$, $n = 3$, $\Phi_0 = 7$.

| tras la iteración | propuestas que faltan | libres | $\Phi$ |
|---|---|---|---|
| 0 | 4 | 3 | 7 |
| 1 | 3 | 2 | 5 |
| 2 | 2 | 2 | 4 |
| 3 | 1 | 2 | 3 |
| 4 | 1 | 1 | 2 |
| 5 | 0 | 0 | 0 |

El algoritmo hizo $5$ iteraciones y $5 \le 7$.

---

## La pareja bloqueante

La segunda pregunta es qué significa «estable» cuando hay gente sin pareja. En el resultado de la sección anterior, $a_1$ quedó solo y $b_2$ también. ¿Eso es estable? Depende de si alguna pareja que no está formada preferiría estarlo. Eso es una pareja bloqueante, y la definición hay que adaptarla.

**Definición adaptada.** Sea $M$ un emparejamiento. Un par $(a,b)$ con $b \in L_a$ que no están juntos en $M$ es **bloqueante** si:

1. **$a$ prefiere a $b$ sobre su situación en $M$:** o $a$ está solo, o $b$ aparece antes que $M(a)$ en $L_a$.
2. **$b$ prefiere a $a$ sobre su situación en $M$:** o $b$ está libre, o $b$ prefiere a $a$ sobre $M(b)$.

Un emparejamiento es **estable** si no tiene ninguna pareja bloqueante.

**Qué cambia respecto a la conferencia.**

- «Estar solo» ahora es una situación, peor que cualquier pareja aceptable.
- Un par con $b \notin L_a$ nunca bloquea, porque $a$ prefiere quedarse solo antes que con $b$: falla la condición 1. (En el ejemplo anterior, $(a_1, b_2)$ no bloquea.)

**Ejemplo.** En el resultado $a_3$–$b_1$, $a_2$–$b_2$, $a_1$ solo:

- $(a_1, b_1)$ cumple la condición 1 ($a_1$ prefiere a $b_1$ sobre estar solo) pero falla la 2 ($b_1$ prefiere a $a_3$ sobre $a_1$): no bloquea.
- $(a_2, b_1)$ cumple la 1 ($b_1$ está antes que $b_2$ en $L_{a_2}$) y falla la 2 ($b_1$ prefiere a $a_3$ sobre $a_2$): no bloquea.

---

## El resultado es estable

Con la definición lista, se puede probar la tercera pregunta. La idea es suponer que existe una pareja bloqueante $(a,b)$ y ver que obliga a $b$ a terminar con alguien mejor que $a$, lo que contradice que $(a,b)$ bloquee. Para ello se usan tres hechos sobre cómo se comporta el algoritmo.

**Tres hechos del algoritmo.**

- **I1.** Un receptor que recibe su primera propuesta queda emparejado para siempre, y desde ahí su pareja solo mejora: solo cambia de pareja por alguien a quien prefiere (la condición `rango[b][a] < rango[b][actual]`).
- **I2.** Cada proponente propone en orden, de su favorito hacia abajo (`siguiente[a]` solo sube).
- **I3 (estado final).** Al terminar, cada proponente está emparejado o tiene su lista agotada. (El `while` solo termina cuando `libres` está vacío, y un proponente deja `libres` sin pareja únicamente al agotar su lista.)

**Lema 1.** El resultado es un emparejamiento válido.

**Demostración.** Cada receptor guarda una sola pareja (`pareja_de_b[b]`), y un proponente solo propone a receptores de su lista, así que toda pareja es válida. Además, en todo momento cada proponente está en `libres`, o es la pareja de un único receptor, o agotó su lista y no es pareja de nadie: solo propone mientras está en `libres`, sale de `libres` al ser aceptado, y vuelve a `libres` cuando un receptor lo cambia por otro. Por tanto no hay dos receptores con el mismo proponente. $\blacksquare$

**Teorema 2.** El emparejamiento $M$ que devuelve el algoritmo es estable, para cualquier orden de ejecución.

**Demostración (por contradicción).** Supón que $(a,b)$ es una pareja bloqueante de $M$.

**Paso 1.** Por la condición 1, $a$ prefiere a $b$ sobre su situación final: o termina con alguien peor que $b$, o termina solo.

**Paso 2.** En los dos casos, $a$ **le propuso a $b$**.

- Si terminó con $b' = M(a)$ peor que $b$: por I2, $a$ propuso a $b$ antes que a $b'$.
- Si terminó solo: por I3 agotó su lista, y $b \in L_a$.

**Paso 3.** Cuando $a$ le propuso a $b$, $b$ no se quedó con $a$ hasta el final: o lo rechazó en ese momento, o lo aceptó y después lo cambió por alguien a quien prefería. En ambos casos, desde ese momento $b$ tiene una pareja a la que prefiere sobre $a$.

**Paso 4.** Por I1, la pareja de $b$ solo mejora a partir de ahí. Entonces $b$ termina emparejado con $M(b)$ y prefiere a $M(b)$ sobre $a$. En particular $b$ no está libre al final.

**Paso 5.** Esto contradice la condición 2 de la pareja bloqueante. Por tanto no hay ninguna. $\blacksquare$

**Observación.** La demostración no usa el orden en que se eligen los proponentes libres, así que vale para cualquier ejecución. Que el *resultado mismo* no dependa del orden es un teorema de la Conferencia 3, §9, para listas completas (el algoritmo da a cada proponente su mejor pareja válida); aquí se comprueba experimentalmente (en «Verificación con código»), sin demostrarlo.

---

## Verificación con código

El archivo [`ejercicio-12.py`](ejercicio-12.py) ejecuta los ejemplos, y en $4000$ instancias aleatorias con $n \le 8$ y listas incompletas, corre el algoritmo con $4$ órdenes de elección distintos, busca parejas bloqueantes con la definición de «La pareja bloqueante» y compara los resultados entre órdenes.

```
Ejemplo A: ([0, 1], 3)
Ejemplo B: ([1, None], 3)
Tres proponentes, cola: [2, 1, None] iteraciones 5 bloqueantes []

4000 instancias aleatorias (n <= 8), 4 órdenes de ejecución cada una:
  sin parejas bloqueantes en todas; el resultado no depende del orden
  máx. iteraciones observadas: 28  (cota n^2 + n)
  proponentes que quedaron solos en total: 4482
```

(La salida lista, para cada receptor $b_1, b_2, \dots$, el índice —desde $0$— de su proponente, y el número de iteraciones.) En ninguna de las $4000$ instancias hay parejas bloqueantes, el resultado fue el mismo con los cuatro órdenes, el máximo de iteraciones observado ($28$) queda por debajo de la cota $n^2 + n$, y hubo $4482$ proponentes que terminaron solos, de modo que el caso nuevo (lista agotada) se ejercita de verdad.

## Resumen de resultados

1. **Modelo:** listas incompletas para los proponentes; un proponente prefiere quedarse solo antes que con alguien que no listó; puede quedar gente sin pareja.
2. **Algoritmo:** el de aceptación diferida, con una línea nueva: un proponente libre con la lista agotada se queda soltero.
3. **Potencial:** $\Phi = \sum_a(|L_a| - \text{siguiente}[a]) + |\text{libres}|$; baja al menos $1$ por iteración y empieza en a lo sumo $n^2 + n$: termina en $O(n^2)$.
4. **Pareja bloqueante:** $(a,b)$ con $b \in L_a$, no emparejados, donde $a$ prefiere a $b$ sobre su situación (incluyendo estar solo) y $b$ prefiere a $a$ sobre la suya (incluyendo estar libre).
5. **Estabilidad:** el resultado es estable para cualquier orden: si $(a,b)$ bloqueara, $a$ le habría propuesto a $b$ y $b$ terminaría con alguien mejor (I1), contra la condición 2.

## Referencias

- Conferencia 3, §6: emparejamiento estable y pareja bloqueante.
- Conferencia 3, §7: Gale–Shapley, aceptación diferida y terminación por potencial.
- Conferencia 3, §8: estabilidad por contradicción.
- Conferencia 3, §9: optimalidad para quien propone (primer fallo); el resultado no depende del orden.
