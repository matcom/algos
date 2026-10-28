# Ejercicio 8 ★★ — Elementos que aparecen más de $n/3$ veces (C3)

> El elemento que aparece más de $n/3$ veces. Generaliza Boyer-Moore con dos candidatos, enuncia el invariante reforzado y demuéstralo. Después escribe la versión que devuelve los candidatos con contador positivo sin verificarlos, y busca un generador de pruebas que no la atrape. Cuidado: el análogo del generador binario de la conferencia 3 sí la atrapa.

## Problema

Dado un arreglo $A$ de $n$ elementos que **solo se comparan por igualdad**, devolver todos los elementos que aparecen más de $n/3$ veces. Puede haber 0, 1 o 2 (tres de ellos sumarían más de $n$). Queremos $O(n)$ tiempo y $O(1)$ memoria.

## Algoritmo (Boyer-Moore con dos candidatos)

`primera_pasada(A)` recorre el arreglo una vez con dos candidatos y sus contadores: si $x$ es uno de los candidatos, suma 1 a su contador; si no, y algún contador está en 0, $x$ ocupa ese lugar; si no, resta 1 a los dos contadores (se descarta una terna de tres elementos distintos). `mas_de_un_tercio(A)` toma los candidatos con contador positivo y, en una segunda pasada, se queda solo con los que de verdad aparecen más de $n/3$ veces.

> Código: [ejercicio-08.py](ejercicio-08.py), parte 1.

**El orden de las ramas importa:** primero se pregunta si $x$ es igual a alguno de los dos candidatos, y solo después si hay un contador en 0. Así nunca quedan dos candidatos iguales.

## Invariante reforzado

Después de procesar el prefijo $A[1..i]$:

> **(I)** el prefijo se puede partir en **ternas de tres elementos distintos entre sí**, más $n_1$ copias de $c_1$, más $n_2$ copias de $c_2$; y $c_1\ne c_2$.

- **Inicialización.** Prefijo vacío: cero ternas, $n_1=n_2=0$ ($c_1=c_2=$`None`, pero no hay copias).
- **Mantenimiento.** Sea $x=A[i+1]$. Un caso por rama:
  1. $x=c_1$: una copia más de $c_1$, $n_1+1$.
  2. $x=c_2$ (y $x\ne c_1$): una copia más de $c_2$.
  3. $n_1=0$, $x\ne c_1,c_2$: el prefijo era ternas + $n_2$ copias de $c_2$. Ahora $x$ es la única copia de $c_1$. $c_1=x\ne c_2$.
  4. $n_2=0$, $n_1>0$, $x\ne c_1,c_2$: simétrico; $c_2=x\ne c_1$.
  5. $n_1,n_2>0$ y $x\ne c_1,c_2$: formamos la terna $\{x,c_1,c_2\}$ con una copia de cada candidato. Sus tres elementos son distintos ($c_1\ne c_2$ y $x$ distinto de ambos). Quedan $n_1-1$ y $n_2-1$ copias, que es lo que deja el algoritmo.

  En todas las ramas, cuando un candidato cambia, lo hace a un $x$ distinto del otro candidato. Así que $c_1\ne c_2$ se mantiene.
- **Conclusión.** Al final, $A$ = $T$ ternas + $n_1$ copias de $c_1$ + $n_2$ copias de $c_2$, con $3T+n_1+n_2=n$.

**Teorema.** *Si $m$ aparece más de $n/3$ veces, entonces $m$ es un candidato con contador positivo.*

Demostración. Si no lo fuera, todas las copias de $m$ estarían en las ternas, a lo sumo una por terna (los tres elementos de una terna son distintos). Entonces $m$ aparecería a lo sumo $T\le n/3$ veces. Contradicción. ∎

Como en la conferencia 3, el teorema tiene un "**si**": dice que los frecuentes están entre los candidatos, no que los candidatos sean frecuentes. Por eso hace falta la segunda pasada.

**Costo:** dos pasadas, $O(n)$ tiempo, $O(1)$ memoria (dos candidatos y dos contadores).

## La versión sin verificar, y el generador que no la atrapa

`atajo(A)` es la versión sin verificar: hace solo la primera pasada y devuelve los candidatos con contador positivo, sin contar cuántas veces aparecen.

> Código: [ejercicio-08.py](ejercicio-08.py), parte 2.

**Contraejemplo mínimo:** `A B B`. A entra como $c_1$, B como $c_2$, y la segunda B sube $n_2$. Final: $n_1=1$, $n_2=2$. El atajo devuelve {A, B}, pero A aparece 1 vez de 3, y $1\not>1$.

**Generador que no la atrapa: dos elementos plantados**, cada uno con más de $n/3$ copias. Por el teorema, los dos son candidatos con contador positivo. Como hay solo dos lugares de candidato, la salida del atajo es exactamente esos dos, que es lo correcto. Es el análogo de "mayoría plantada" de la C3 §5: todas las entradas cumplen la hipótesis del teorema, y sobre ellas la mitad "buena" del argumento basta.

**Por qué el análogo del generador binario sí la atrapa.** En la C3, con dos símbolos, "contador $>0$" equivalía a "es mayoría". Aquí el análogo sería un alfabeto pequeño (2 o 3 símbolos). Con $\{a,b,c\}$ cada terna tiene una copia de cada símbolo, y las cuentas finales son $T+n_1$, $T+n_2$ y $T$. Entonces $c_1$ es frecuente si y solo si
$$T+n_1>\frac{3T+n_1+n_2}{3}\iff 2n_1>n_2 ,$$
que **no** está garantizado por $n_1>0$. Con 2 símbolos no hay ternas ($T=0$) y sale la misma condición. `A B B` es justamente un caso binario con $n_1=1$, $n_2=2$.

## Casos de prueba y validación

Oráculo para las pruebas: `oraculo(A)` cuenta las apariciones de cada elemento con `Counter` y devuelve los que aparecen más de $n/3$ veces. Esta parte no imprime nada.

> Código: [ejercicio-08.py](ejercicio-08.py), parte 3.

Casos a mano:

> Código: [ejercicio-08.py](ejercicio-08.py), parte 4.

```text
           '': correcto=[]  atajo=[]  oráculo=[]
          'A': correcto=['A']  atajo=['A']  oráculo=['A']
         'AB': correcto=['A', 'B']  atajo=['A', 'B']  oráculo=['A', 'B']
        'ABB': correcto=['B']  atajo=['A', 'B']  oráculo=['B']
        'AAB': correcto=['A']  atajo=['A', 'B']  oráculo=['A']
        'ABC': correcto=[]  atajo=[]  oráculo=[]
      'AABBC': correcto=['A', 'B']  atajo=['A', 'B']  oráculo=['A', 'B']
  'ABCABCAAB': correcto=['A']  atajo=['A', 'B']  oráculo=['A']
   'AAABBBCC': correcto=['A', 'B']  atajo=['A', 'B']  oráculo=['A', 'B']
  'ABACADAEA': correcto=['A']  atajo=['A']  oráculo=['A']
```

**Invariante vigilado.** Un multiconjunto de tamaño $3t$ se parte en ternas de distintos si y solo si ningún elemento aparece más de $t$ veces. (Se ordena y se toman las posiciones $i$, $i+t$, $i+2t$. Si una terna repitiera un elemento, ese elemento ocuparía más de $t$ posiciones seguidas.)

> Código: [ejercicio-08.py](ejercicio-08.py), parte 5.

```text
invariante comprobado en 24459 prefijos, sin fallos
```

**La tabla de generadores** (como la Figura 3 de la C3):

> Código: [ejercicio-08.py](ejercicio-08.py), parte 6.

```text
       generador    atajo  con verificación
   dos plantados     0.0%              0.0%
     un plantado    47.1%              0.0%
         binario    33.9%              0.0%
      3 símbolos    37.5%              0.0%
      5 símbolos    49.8%              0.0%
```

Solo "dos plantados" no ve el error. Con un solo plantado el error aparece en casi la mitad de los casos, porque el segundo lugar de candidato queda ocupado por basura.

## Resumen

- **Invariante:** el prefijo = ternas de distintos + $n_1$ copias de $c_1$ + $n_2$ copias de $c_2$, con $c_1\ne c_2$.
- **Teorema:** si $m$ aparece $>n/3$ veces, es un candidato con contador positivo. Hace falta la segunda pasada.
- **Atajo sin verificar:** falla con `A B B`. Lo atrapan los alfabetos pequeños y "un plantado". Solo "dos plantados", que cumple siempre la hipótesis del teorema, no lo atrapa.
