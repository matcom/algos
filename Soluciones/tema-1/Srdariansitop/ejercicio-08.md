# Pregunta 8:
El elemento que aparece más de n/3 veces. Generaliza Boyer-Moore con dos candidatos, enuncia el invariante reforzado y demuéstralo. Después describe la versión que devuelve los candidatos con contador positivo sin verificarlos, y busca un generador de pruebas que no la atrape. Cuidado: el análogo del generador binario de la conferencia 3 sí la atrapa.

---

# Planteamiento

**Problema.** Dado un arreglo $A$ de $n$ elementos que solo se pueden comparar por igualdad, devolver todos los elementos que aparecen **más de $n/3$ veces**.

**Convenciones.**

- Un elemento es **pesado** si aparece más de $n/3$ veces.
- Hay a lo sumo **dos** pesados. Con tres pesados habría más de $3 \cdot \frac{n}{3} = n$ elementos, que es imposible. Por eso bastan dos candidatos.
- El estado del algoritmo es $(c_1, k_1, c_2, k_2)$: dos candidatos con sus contadores. Si $k_j = 0$, el casillero $j$ está **vacío** y el valor de $c_j$ no significa nada.
- Meta: tiempo $O(n)$ y memoria extra $O(1)$.

---

# Generalización: Boyer-Moore con dos candidatos

## La idea de cancelación

En Boyer-Moore con $n/2$ se tachaban **parejas** de elementos distintos, porque un elemento no puede aparecer dos veces en una pareja de distintos. Para $n/3$ se tachan **ternas** de elementos distintos entre sí.

Un elemento aparece a lo sumo **una vez** en cada terna. Si se tachan $t$ ternas, cada elemento pierde a lo sumo $t$ copias. Si $v$ es pesado, entonces $\#v > n/3$. Tras tachar $t$ ternas queda un arreglo de $n - 3t$ elementos en el que $v$ tiene al menos $\#v - t$ copias. Mientras queden elementos, $v$ sigue superando el tercio de lo que queda:

$$\#v - t > \frac{n}{3} - t = \frac{n - 3t}{3}.$$

Se pueden seguir tachando ternas de distintos hasta que no quede ninguna. Lo que sobrevive usa a lo sumo **dos** valores distintos, y si hay pesados tienen que estar entre ellos.

## Cómo se hace sin guardar lo tachado

Se recuerdan solo dos "casilleros": un candidato con su contador cada uno. Al leer $x$, se aplican estas reglas **en este orden de prioridad**:

| Regla | Condición | Efecto |
|---|---|---|
| R1 | $k_1 > 0$ y $x = c_1$ | $k_1 \leftarrow k_1 + 1$ |
| R2 | $k_2 > 0$ y $x = c_2$ | $k_2 \leftarrow k_2 + 1$ |
| R3 | $k_1 = 0$ | $c_1 \leftarrow x,\ k_1 \leftarrow 1$ |
| R4 | $k_2 = 0$ | $c_2 \leftarrow x,\ k_2 \leftarrow 1$ |
| R5 | ninguna anterior | $k_1 \leftarrow k_1 - 1,\ k_2 \leftarrow k_2 - 1$ |

R5 es la cancelación. Se llega a ella solo cuando $k_1 > 0$, $k_2 > 0$, $x \ne c_1$ y $x \ne c_2$. Entonces $x$, $c_1$ y $c_2$ forman una terna de distintos, y se tacha una copia de cada candidato junto con $x$.

**Por qué las reglas piden $k_j > 0$.** Un casillero vacío puede conservar un valor viejo. Si R1 y R2 no comprobaran $k_j > 0$, un $x$ igual a un valor viejo se trataría como "copia" de un candidato que ya no existe. Y si R3 o R4 colocaran a $x$ en un casillero vacío cuando el otro casillero ya tiene ese mismo valor, quedaría $c_1 = c_2$ con ambos contadores positivos. Eso rompería R5, porque la terna dejaría de ser de distintos.

## Algoritmo completo

1. **Primera pasada.** Aplicar las reglas R1 a R5 a cada elemento de $A$, de izquierda a derecha, partiendo de $k_1 = k_2 = 0$.
2. **Segunda pasada.** Para cada candidato con contador positivo, contar sus apariciones en $A$ y devolverlo solo si supera $n/3$.

## Ejemplo a mano

Sea $A = (A, B, A, C, A, B, D, A, B)$ con $n = 9$. Un elemento es pesado si aparece más de $3$ veces. $A$ aparece 4 veces y es pesado. $B$ aparece 3 veces y no lo es, porque $3 > 3$ es falso.

| paso | $x$ | regla | $(c_1,k_1)$ | $(c_2,k_2)$ |
|---|---|---|---|---|
| 1 | A | R3 | (A,1) | (·,0) |
| 2 | B | R4 | (A,1) | (B,1) |
| 3 | A | R1 | (A,2) | (B,1) |
| 4 | C | R5 | (A,1) | (B,0) |
| 5 | A | R1 | (A,2) | (B,0) |
| 6 | B | R4 | (A,2) | (B,1) |
| 7 | D | R5 | (A,1) | (B,0) |
| 8 | A | R1 | (A,2) | (B,0) |
| 9 | B | R4 | (A,2) | (B,1) |

Al final sobreviven $A$ con contador 2 y $B$ con contador 1. $A$ está entre los candidatos, como promete el teorema. La segunda pasada cuenta 4 para $A$ y 3 para $B$, y se queda solo con $A$.

**Complejidad.** Dos pasadas, tiempo $O(n)$, memoria $O(1)$ (cuatro variables). Con $k-1$ casilleros y tachando grupos de $k$ distintos se obtiene el algoritmo de Misra-Gries para el umbral $n/k$.

---

# Invariante

## Enunciado

Sea $A[1..i]$ el prefijo procesado y $(c_1, k_1, c_2, k_2)$ el estado después de procesarlo.

**Invariante reforzado $I(i)$:**

1. $k_1 \ge 0$ y $k_2 \ge 0$.
2. Si $k_1 > 0$ y $k_2 > 0$, entonces $c_1 \ne c_2$.
3. El prefijo $A[1..i]$ se puede partir en **$t$ ternas de elementos distintos entre sí**, más $k_1$ copias de $c_1$, más $k_2$ copias de $c_2$, y nada más. En particular, $i = 3t + k_1 + k_2$.

## Por qué hace falta reforzar

La frase natural es "si un elemento es pesado en el prefijo, es un candidato con contador positivo". Es verdadera, pero no es inductiva. Si el prefijo no tiene pesados, la hipótesis no dice nada sobre el estado, y sin embargo el siguiente elemento puede crear un pesado en el prefijo siguiente.

La partición en ternas guarda la información de cancelación que sí se sostiene sola. La condición 2 hace que, en R5, los tres elementos sean de verdad distintos.

## Demostración

**Inicialización ($i = 0$).** El prefijo es vacío y $k_1 = k_2 = 0$. Son cero ternas y cero copias, y la condición 2 es vacía.

**Mantenimiento.** Supongamos $I(i)$ y sea $x = A[i+1]$. Cada regla produce un caso.

- **R1** ($k_1 > 0$, $x = c_1$). El contador $k_1$ sube en 1 y $x$ es una copia más de $c_1$. Las ternas no cambian y los candidatos tampoco, así que 1, 2 y 3 se mantienen.
- **R2** ($k_2 > 0$, $x = c_2$, y no se aplicó R1). Es igual que R1 con el casillero 2.
- **R3** ($k_1 = 0$, y no se aplicó R2). Se pone $c_1 := x$ y $k_1 := 1$. La partición nueva es la anterior más una copia de $x = c_1$. Para la condición 2, si $k_2 > 0$ entonces $x \ne c_2$, porque en caso contrario se habría aplicado R2. Así que $c_1 \ne c_2$.
- **R4** ($k_1 > 0$, $k_2 = 0$, y no se aplicó R1). Se pone $c_2 := x$ y $k_2 := 1$. Como R1 no se aplicó, $x \ne c_1$, luego $c_1 \ne c_2$. La partición nueva es la anterior más una copia de $x = c_2$.
- **R5** ($k_1 > 0$, $k_2 > 0$, $x \ne c_1$, $x \ne c_2$). Por la condición 2 de $I(i)$, $c_1 \ne c_2$. Entonces $x$, $c_1$ y $c_2$ son tres elementos distintos. Como $k_1, k_2 \ge 1$, la partición tiene al menos una copia de cada uno. Tomo una copia de $c_1$ y una de $c_2$, y las junto con $x$ en una terna nueva. Quedan $t+1$ ternas, $k_1 - 1$ copias de $c_1$ y $k_2 - 1$ copias de $c_2$, que es exactamente el estado que deja R5. Los contadores siguen siendo $\ge 0$, y si alguno llega a 0 su parte de la condición 2 pasa a ser vacía.

Los cinco casos son exhaustivos: si no se aplica ninguna de R1 a R4, entonces $k_1 > 0$, $k_2 > 0$, $x \ne c_1$ y $x \ne c_2$, que es R5. Por tanto $I(i+1)$ se cumple. $\square$

## Conclusión

**Teorema.** *Si $v$ aparece más de $n/3$ veces en $A$, entonces al terminar la primera pasada $v \in \{c_j : k_j > 0\}$.*

*Demostración.* Por contradicción. Supongamos que $v$ es pesado y que no es ningún candidato con contador positivo. Por $I(n)$, $A$ se parte en $t$ ternas de distintos, $k_1$ copias de $c_1$ y $k_2$ copias de $c_2$. Las copias sueltas son de $c_1$ o de $c_2$, y las de un casillero con $k_j = 0$ no existen. Como $v$ no es candidato con contador positivo, ninguna copia suelta es de $v$. Entonces $v$ aparece solo dentro de las ternas, y en cada una a lo sumo una vez, porque sus tres elementos son distintos. Por tanto

$$\#v \le t = \frac{n - k_1 - k_2}{3} \le \frac{n}{3},$$

lo que contradice que $v$ sea pesado. $\blacksquare$

## Corrección del algoritmo completo

El teorema garantiza que todo pesado está entre los candidatos con contador positivo. La segunda pasada cuenta cada uno y se queda con los que superan $n/3$. Así se devuelven **exactamente** los pesados: ninguno se pierde, por el teorema, y ninguno falso sobrevive, por el conteo.

Como en la conferencia, la conclusión empieza con "si hay pesado". Lo que esa hipótesis no cubre es lo que la segunda pasada protege.

---

# La otra versión 

## Descripción

Es la misma primera pasada, con las reglas R1 a R5, pero la salida es directamente el conjunto

$$S = \{c_j : k_j > 0\},$$

sin contar nada. Tiene tiempo $O(n)$ en una sola pasada.

## Qué mitad es correcta

Por el teorema, el atajo **nunca pierde un pesado**: no tiene falsos negativos. Lo que falla es la recíproca. Que $k_j > 0$ no implica que $c_j$ sea pesado, así que puede haber **falsos positivos**.

## Contraejemplo mínimo

Sea $A = (A, B, C, D)$, con $n = 4$ y umbral $n/3 = 4/3$. Los dos primeros elementos ocupan los casilleros. $C$ cancela una terna y deja ambos contadores en 0. $D$ ocupa un casillero con contador 1. El atajo devuelve $\{D\}$, pero $D$ aparece una sola vez y $1 > 4/3$ es falso. En este arreglo no hay pesados.

## El análogo del generador binario SÍ lo atrapa

Con dos símbolos nunca existen tres elementos distintos, así que R5 no se aplica jamás. Los dos casilleros se llenan con los dos símbolos y los contadores son exactamente sus cuentas. El atajo devuelve **siempre ambos símbolos**.

Pero el menos frecuente no siempre es pesado. Por ejemplo, $A = (A, A, B)$ tiene $n = 3$, y $B$ aparece una vez, con $1 > 1$ falso. El atajo devuelve $\{A, B\}$ y la respuesta correcta es $\{A\}$. Cualquier arreglo binario donde un símbolo aparezca $\le n/3$ veces lo delata, y eso ocurre con frecuencia. A diferencia del caso $n/2$, donde el binario era ciego al atajo, aquí es el generador que lo atrapa.

## El generador que no lo atrapa: dos pesados plantados

**Construcción.** Para $n \ge 4$, sea $m = \lfloor n/3 \rfloor + 1$, que cumple $m > n/3$. Se eligen dos símbolos distintos $a$ y $b$ al azar. Se coloca $m$ veces $a$, $m$ veces $b$, y los $n - 2m$ lugares restantes se rellenan con símbolos aleatorios. Después se mezcla todo.

Se necesita $2m \le n$, y eso se cumple para todo $n \ge 4$. Para $n = 3$ no cabe: $m = 2$ y $2m = 4 > 3$.

Un ejemplo con $n = 9$ es $m = 4$: ocho posiciones ocupadas por $a$ y $b$ más una libre, como $A\,A\,A\,A\,B\,B\,B\,B\,C$ mezclado.

**Por qué el atajo es indistinguible del algoritmo correcto sobre estos arreglos.**

1. Todo arreglo generado tiene **exactamente dos** pesados: $a$ y $b$. Más de dos es imposible, y el relleno solo puede aumentar sus cuentas.
2. Por el teorema, ambos están en $S$.
3. $S$ tiene a lo sumo dos elementos, porque hay solo dos casilleros.
4. Luego $S = \{a, b\}$, que es exactamente la respuesta correcta.

No queda espacio para un falso positivo: los dos casilleros ya están ocupados por los pesados verdaderos. Es el mismo mecanismo de la "mayoría plantada" de la conferencia. Todos los arreglos cumplen la hipótesis del teorema, y sobre esos el atajo es correcto por la mitad buena del argumento.


# Código(Extra 08)

**01_planteamiento.png.** Fija el problema. A la izquierda, una barra que representa las $n$ posiciones del arreglo muestra por qué no pueden existir tres pesados: tres bloques de "más de $n/3$" no caben y se salen de la barra, así que hay a lo sumo dos y bastan dos candidatos. A la derecha, el arreglo de ejemplo ($n=9$) con las cuentas de cada letra frente a la línea del umbral $n/3=3$. $A$ (4 apariciones) la supera y $B$ (3) queda justo en el umbral, así que no es pesado. Abajo están las convenciones: el estado $(c_1,k_1,c_2,k_2)$, que $k=0$ significa casillero vacío, y la meta de $O(n)$ en tiempo y $O(1)$ en memoria.

**02_cancelacion.gif.** Explica la idea de fondo, sin casilleros todavía. Sobre el arreglo de ejemplo se van tachando ternas de elementos distintos, una por una. En cada paso se muestra cuántos elementos quedan y si $A$ sigue superando el tercio de lo que sobrevive. La clave es que una terna de distintos le quita a lo sumo una copia a cualquier valor, así que un pesado sigue siéndolo: $\#v-t>(n-3t)/3$. Al final quedan a lo sumo dos valores distintos, y ahí tienen que estar los pesados.

**03_algoritmo.gif.** Es la traza del algoritmo paso a paso. Arriba se recorre el arreglo con un marcador. En el centro están los dos casilleros, con el candidato y su contador dibujado como fichas. Abajo se indica qué regla (R1–R5) se aplica en cada paso y qué hace, y la tira de reglas resalta la activa. Cuando entra R5 se ve la terna tachada. Los dos últimos fotogramas muestran el fin de la primera pasada y la segunda pasada, que cuenta de verdad: $A$ pasa con 4 y $B$ se descarta con 3.

**04_reglas.png.** Resume el algoritmo como árbol de decisión: R1 y R2 (sumar a un candidato existente), R3 y R4 (ocupar un casillero vacío) y R5 (cancelar la terna). El panel lateral explica por qué importa el orden. Si R3 se evaluara antes que R2, una $x=A$ podría ocupar el casillero 1 mientras $A$ ya está en el 2, y quedaría $c_1=c_2$. Entonces R5 tacharía una "terna" con elementos repetidos y se rompería el invariante.

**05_invariante.gif.** Muestra el invariante reforzado en acción. En cada paso, el prefijo leído se dibuja partido en ternas de distintos, $k_1$ copias de $c_1$ y $k_2$ copias de $c_2$. Los bloques nuevos aparecen resaltados, y en R5 se ve cómo se arma la terna nueva con una copia de cada casillero más $x$. Debajo se comprueba en vivo la igualdad $i=3t+k_1+k_2$ y las tres condiciones (contadores no negativos, $c_1\ne c_2$ si ambos son positivos, y partición exacta). Es la demostración por inducción hecha visible.

**06_teorema.png.** Dibuja la conclusión del invariante, por contradicción. Si un pesado $v$ no fuera candidato, solo podría aparecer dentro de las ternas, y en cada una a lo sumo una vez. Con el ejemplo numérico ($n=12$, $t=3$) resulta $\#v\le t=(n-k_1-k_2)/3\le n/3$. Eso choca con $\#v>n/3$, como muestra el gráfico del máximo posible de $C$ frente al umbral. Por eso la primera pasada nunca pierde un pesado, aunque pueda dejar candidatos que no lo son.

**07_atajo_vs_generadores.png.** Cierra con la versión sin verificar. A la derecha, los contraejemplos mínimos: `A B C D` devuelve $\{D\}$ cuando la respuesta correcta es $\varnothing$, y `A A B` devuelve $\{A,B\}$ cuando la correcta es $\{A\}$. A la izquierda, el porcentaje de arreglos donde cada generador de pruebas delata el atajo: binario 23,4 %, cinco símbolos 69,2 %, un pesado plantado 60,1 % y dos pesados plantados 0 %. El cuadro inferior explica por qué el último no lo atrapa: con exactamente dos pesados, los dos casilleros ya están ocupados por ellos y no queda lugar para un falso positivo.