# Ejercicio 12: Gale-Shapley con listas incompletas

**Enunciado:** Gale-Shapley con listas incompletas: cada proponente lista solo a algunos receptores, y prefiere quedarse solo antes que con uno que no listó. Adapta el algoritmo, su potencial y la definición de pareja bloqueante. ¿Sigue siendo estable el resultado? Demuéstralo. (C3)

**Modelo:** Emparejamiento estable. Tenemos un conjunto de proponentes \(H\) (hombres) y receptores \(M\) (mujeres). Cada persona tiene una lista de preferencias que puede ser incompleta. Si alguien no aparece en la lista de otra persona, se considera inaceptable. Todos prefieren estar solteros antes que emparejarse con alguien inaceptable.

---

## 1. Adaptación del algoritmo de Gale-Shapley

El algoritmo original de Gale-Shapley puede adaptarse a listas incompletas introduciendo el concepto de **aceptabilidad mutua**.

Una pareja \((h,m)\) es mutuamente aceptable si:

\[
m\in preferencias_H[h]
\]

y:

\[
h\in preferencias_M[m]
\]

Solo permitimos propuestas entre personas que se consideran mutuamente aceptables.

Además, si un proponente agota todas sus opciones, permanece soltero y deja de participar en el algoritmo.

### Algoritmo

```python
from collections import deque

def gale_shapley_incompleto(H, M, preferencias_H, preferencias_M):

    # Construimos los rankings de las mujeres.
    # Un número menor representa una mayor preferencia.
    ranking_M = {
        m: {h: i for i, h in enumerate(preferencias_M[m])}
        for m in M
    }

    # Conservamos únicamente las parejas mutuamente aceptables,
    # respetando el orden original de preferencias de cada hombre.
    listas_validas = {
        h: [
            m for m in preferencias_H[h]
            if h in ranking_M[m]
        ]
        for h in H
    }

    # Hombres libres que todavía tienen propuestas disponibles.
    libres = deque(
        h for h in H if listas_validas[h]
    )

    # Mujer -> hombre con quien está comprometida.
    comprometidos = {}

    # Índice de la siguiente mujer a la que propondrá cada hombre.
    siguiente = {h: 0 for h in H}

    while libres:
        h = libres.popleft()

        # Propuesta a la siguiente mujer de su lista.
        m = listas_validas[h][siguiente[h]]
        siguiente[h] += 1

        if m not in comprometidos:
            # La mujer está libre: acepta la propuesta.
            comprometidos[m] = h

        else:
            actual = comprometidos[m]

            # La mujer compara al nuevo proponente
            # con su pareja provisional.
            if ranking_M[m][h] < ranking_M[m][actual]:

                # Acepta al nuevo hombre.
                comprometidos[m] = h

                # El anterior queda libre si todavía
                # tiene mujeres a las que proponer.
                if siguiente[actual] < len(listas_validas[actual]):
                    libres.append(actual)

            else:
                # Rechaza al nuevo hombre.
                # Este continúa si tiene opciones disponibles.
                if siguiente[h] < len(listas_validas[h]):
                    libres.append(h)

    return comprometidos
```

El diccionario `comprometidos` contiene el emparejamiento final. Los hombres que no aparecen como valores y las mujeres que no aparecen como claves permanecen solteros.

### Propiedades del algoritmo

- Solo se realizan propuestas entre personas mutuamente aceptables.
- Cada hombre propone siguiendo el orden de su lista.
- Ningún hombre realiza dos veces la misma propuesta.
- Las mujeres solamente cambian a una pareja que prefieren estrictamente más que la actual.
- Si un hombre agota sus opciones, permanece soltero.

---

## 2. Potencial (Terminación)

Para demostrar que el algoritmo termina, utilizamos una función de potencial que mide la cantidad de propuestas que todavía pueden realizarse.

Sea \(L_h\) la lista de preferencias mutuamente aceptables del hombre \(h\).

Definimos:

\[
\boxed{
\Phi=
\sum_{h\in H}
\left(
|L_h|-siguiente[h]
\right)
}
\]

Donde `siguiente[h]` representa la posición de la próxima mujer a la que puede proponer el hombre \(h\).

### Demostración

**1. Inicialización:**

Al comienzo, ningún hombre ha realizado propuestas.

Por tanto:

\[
siguiente[h]=0
\]

para todos los hombres.

El potencial inicial es:

\[
\Phi_0=\sum_{h\in H}|L_h|
\]

Este valor es finito porque las listas de preferencias contienen una cantidad finita de personas.

**2. Decremento:**

En cada iteración del ciclo `while`, un hombre libre realiza una propuesta a la siguiente mujer de su lista.

Después de realizarla:

\[
siguiente[h]\leftarrow siguiente[h]+1
\]

Por tanto, el potencial disminuye exactamente en una unidad:

\[
\boxed{\Phi_{\text{nuevo}}=\Phi_{\text{anterior}}-1}
\]

Si una mujer rechaza una propuesta o abandona a su pareja actual, los hombres afectados pueden volver a la cola de libres, siempre que tengan opciones pendientes.

Estas operaciones no aumentan el potencial, porque no se deshacen propuestas anteriores.

**3. Conclusión:**

El potencial es un entero no negativo que comienza con un valor finito y disminuye exactamente en una unidad en cada iteración.

Por tanto, el algoritmo debe terminar después de un número finito de propuestas.

El número máximo de propuestas está acotado por:

\[
\sum_{h\in H}|L_h|
\]

Si existen \(n\) hombres y \(n\) mujeres, este valor es como máximo:

\[
n^2
\]

Por tanto, el algoritmo termina en:

\[
\boxed{O(n^2)}
\]

propuestas como máximo.

---

## 3. Adaptación de la definición de pareja bloqueante

En el problema original, una pareja bloqueante era un hombre y una mujer que no estaban emparejados entre sí, pero que se preferían mutuamente sobre sus parejas actuales.

Con listas incompletas debemos incorporar explícitamente la aceptabilidad mutua y la posibilidad de permanecer solteros.

### Definición de pareja bloqueante

Una pareja \((h,m)\) es bloqueante para un emparejamiento \(S\) si se cumplen simultáneamente las siguientes condiciones:

1. \(h\) y \(m\) no están emparejados entre sí en \(S\).
2. Son mutuamente aceptables:

   \[
   m\in preferencias_H[h]
   \]

   y:

   \[
   h\in preferencias_M[m]
   \]

3. El hombre \(h\) prefiere a \(m\) sobre su situación actual, ya sea su pareja o permanecer soltero.
4. La mujer \(m\) prefiere a \(h\) sobre su situación actual, ya sea su pareja o permanecer soltera.

Un emparejamiento es **estable** si no existe ninguna pareja bloqueante.

Es importante observar que una pareja que no es mutuamente aceptable nunca puede ser bloqueante, porque al menos una de las dos personas prefiere permanecer soltera.

---

## 4. Demostración de estabilidad (Correctitud)

**Teorema:** El emparejamiento producido por el algoritmo adaptado de Gale-Shapley con listas incompletas es estable.

### Demostración por contradicción

Supongamos que el algoritmo termina con un emparejamiento \(S\) que no es estable.

Entonces existe una pareja bloqueante \((h,m)\).

Por la definición de pareja bloqueante:

- \(h\) y \(m\) son mutuamente aceptables.
- El hombre \(h\) prefiere a \(m\) sobre su pareja final o sobre permanecer soltero.
- La mujer \(m\) prefiere a \(h\) sobre su pareja final o sobre permanecer soltera.

**1. El hombre necesariamente propuso a la mujer.**

Como los hombres realizan propuestas siguiendo el orden de sus preferencias, si \(h\) prefiere a \(m\) sobre su situación final, necesariamente tuvo que proponerle antes de quedar emparejado con una mujer que prefiere menos.

Si termina soltero, también tuvo que proponer a todas las mujeres de su lista de preferencias mutuamente aceptables.

Por tanto:

\[
\boxed{h\text{ propuso a }m}
\]

**2. Analizamos qué sucedió con la propuesta.**

Cuando \(h\) propuso a \(m\), podían ocurrir dos situaciones:

- La mujer \(m\) rechazó a \(h\) porque ya estaba comprometida con un hombre al que prefería más.
- La mujer \(m\) aceptó inicialmente a \(h\), pero posteriormente lo abandonó por otro hombre al que prefería más.

En ambos casos, la mujer termina manteniendo una pareja que prefiere sobre \(h\).

Esto se debe a una propiedad fundamental de Gale-Shapley:

\[
\boxed{\text{Las mujeres nunca empeoran su pareja provisional}}
\]

Una vez que una mujer acepta una propuesta, solamente puede cambiar a una pareja que prefiera estrictamente más. Nunca vuelve a estar soltera.

Por tanto, al finalizar el algoritmo, \(m\) tiene una pareja que prefiere sobre \(h\).

**3. Contradicción:**

Llegamos a una contradicción, porque habíamos supuesto que \((h,m)\) era una pareja bloqueante, lo cual exige que la mujer \(m\) prefiera a \(h\) sobre su situación final.

Pero acabamos de demostrar que:

\[
m\text{ prefiere a su pareja final sobre }h
\]

Por tanto, no puede existir ninguna pareja bloqueante.

En consecuencia:

\[
\boxed{\text{El emparejamiento producido es estable}}
\]

---

## 5. Conclusión

La adaptación de Gale-Shapley a listas incompletas sigue garantizando un emparejamiento estable, aunque algunas personas terminen solteras.

El algoritmo solamente permite propuestas entre personas mutuamente aceptables. Si un hombre agota su lista, permanece soltero; si una mujer recibe una propuesta, solamente la acepta cuando es aceptable y mejora su situación actual.

El potencial basado en las propuestas pendientes demuestra que el algoritmo termina después de un número finito de iteraciones.

Finalmente, la demostración por contradicción establece que no puede existir ninguna pareja mutuamente aceptable que prefiera estar junta antes que conservar el resultado final.

Por tanto:

\[
\boxed{\text{Gale-Shapley con listas incompletas produce un emparejamiento estable}}
\]

La complejidad temporal sigue siendo:

\[
\boxed{O(n^2)}
\]

en el caso de \(n\) proponentes y \(n\) receptores, y el algoritmo necesita espacio adicional para almacenar las propuestas, los compromisos y las estructuras auxiliares.

**La idea fundamental:** permitir que las personas permanezcan solteras no destruye la estabilidad de Gale-Shapley. Lo importante es respetar la aceptabilidad mutua y mantener la propiedad de que los receptores nunca empeoran sus parejas provisionales.