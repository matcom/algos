# Outline: Capítulo 16, P, NP y reducciones

Estado: aprobado y redactado (2026-11-13), dentro del workflow del libro. El documento
está en `notas.md`.
Destino: `Lectures/2026/16-p-np/notas.md`, capítulo del libro (sin PDF por conferencia).
Extensión objetivo: 5 500–7 000 palabras con el código.

## Idea del capítulo

Hasta el capítulo 15 la pregunta fue "¿qué tan rápido?". Para conjunto independiente
en un árbol el capítulo 11, §2 da $O(n)$; en un grafo cualquiera nadie conoce nada
mejor que probar subconjuntos. Este capítulo no resuelve eso: cambia la pregunta por
"¿es tan difícil como?", que sí se puede contestar. Las herramientas son tres
definiciones (P, NP por certificados, reducción polinomial) y una receta de
demostración. Los ejemplos son tres problemas de grafos que resultan ser el mismo
problema visto de tres maneras.

El capítulo **no** demuestra que ningún problema sea NP-completo: el primero necesita
Cook-Levin (capítulo 17), y conjunto independiente llega en el capítulo 18. Lo que
demuestra es que los tres problemas son equivalentes entre sí, y qué se seguiría de
eso. Las notas lo dicen con esas palabras para que nadie salga creyendo que hoy se
probó la dificultad.

El error plantado es una reducción que solo falla en una dirección: el complemento
calculado con pertenencia de pares ordenados. Pasa toda batería de instancias con
solución plantada, porque la dirección "sí ⇒ sí" sigue siendo verdad. La demostración
lo anuncia: la dirección "⇐" usa que toda arista del grafo construido es una no
arista del original.

## Estructura

### 1. Una pregunta que no sabemos contestar
- Capítulo 11, §2: conjunto independiente de peso máximo en un árbol en $O(n)$.
  Capítulo 11, §8–§10: el viajante en $O(2^n n^2)$. En grafos generales, conjunto
  independiente no tiene algoritmo polinomial conocido.
- Cambio de pregunta: de "cuánto cuesta" a "es tan difícil como". La herramienta es la
  reducción del capítulo 2, §8, leída en la segunda dirección (allí se anunció).

### 2. Decisión y optimización
- Definiciones de conjunto independiente, clique y vertex cover, como problemas de
  decisión con umbral $k$.
- Por qué basta la decisión: optimización ⇒ decisión es inmediato; decisión ⇒ valor
  óptimo por búsqueda binaria en $\lceil \log_2(n+1) \rceil$ llamadas.
- **Código ejecutable**: oráculo por fuerza bruta, búsqueda binaria, contador de
  llamadas; contra el máximo directo. Verificado en `verif/16/casos.py`: peor caso
  exacto $\lceil \log_2(n+1) \rceil$ para $n = 1, 2, 3, 7, 8, 100, 1000$.
- Encontrar el conjunto, no solo su tamaño, es el ejercicio 4.

### 3. La clase P
- Polinomial en el tamaño en bits (capítulo 1, §8). La robustez entre modelos
  (capítulo 1, §3): la frontera polinomial no depende del modelo razonable.
- Codificación: un número en unario infla la entrada; la mochila de $O(nW)$ es
  pseudopolinomial (capítulo 1, §8). Ejercicio 10.
- Ejemplos en P: caminos mínimos, emparejamiento bipartito (capítulo 13, §12),
  2-coloración por BFS.

### 4. NP: soluciones que se comprueban rápido
- Definición por certificados y verificador polinomial, con la cota del largo del
  certificado. La N es de "no determinista" (equivalencia con máquinas no
  deterministas: Karp 1972 la demuestra, verificado en el escaneo; el capítulo 17 la usa).
- Ejemplos: conjunto independiente, SAT en FNC (definición breve), compuestos.
- $P \subseteq NP$ (certificado vacío) y $NP \subseteq EXP$ (probar todos los
  certificados).
- **Código ejecutable**: verificador para independiente, y cuántos subconjuntos revisa
  la búsqueda frente a cuántos pares revisa el verificador.
- Asimetría: un "no" no tiene por qué tener certificado corto. co-NP en el ejercicio 8.

### 5. Reducción polinomial
- Definición de Karp (muchos a uno). Cook usó una noción más débil (Turing); Karp 1972
  lo dice en la p. 92, verificado.
- Lema: $A \le_p B$ y $B \in P$ ⇒ $A \in P$, con el paso que todos se saltan: la salida
  de $f$ mide a lo sumo $q(|x|)$, y el polinomio compuesto.
- Contrapositivo como herramienta de dificultad. Transitividad: ejercicio 3.
- **Figura**: las direcciones de una reducción y qué implica cada una.

### 6. NP-duro y NP-completo
- Definiciones. Teorema: si un NP-completo está en P, entonces P = NP (demostración).
- Lema: $A$ NP-completo, $A \le_p B$, $B \in NP$ ⇒ $B$ NP-completo (usa transitividad).
- NP-duro no está dentro de NP: el problema de la parada es NP-duro (reducción desde
  SAT, un párrafo) y no es decidible. Las versiones de optimización no son problemas de
  decisión.
- El primero no sale de una reducción: Cook 1971, capítulo 17.

### 7. La receta
- Cuatro pasos: $B \in NP$; elegir un $A$ conocido; construir $f$ polinomial; las dos
  direcciones de la equivalencia.
- La trampa de la dirección: se reduce **desde** el conocido **hacia** el nuevo.
  Ejercicio 5.

### 8. El experimento
- **Código ejecutable**: en los 1 099 grafos etiquetados con $n \le 5$, $\alpha(G) =
  \omega(\bar G)$ y $\alpha(G) + \tau(G) = n$ siempre (verificado).
- **Figura**: un grafo, su complemento, el mismo conjunto como independiente, clique y
  el resto como cubrimiento; calculado por el código.

### 9. Independiente ≤ₚ clique, y vuelta
- Construcción por complemento, $O(n^2)$; las dos direcciones; la inversa por simetría.
- **Código ejecutable**: la reducción contra el oráculo en grafos al azar.

### 10. Independiente ≤ₚ vertex cover
- Lema del complemento de conjuntos; $(G, k) \mapsto (G, n - k)$; las dos direcciones.
- Corolario: los tres problemas están en P o ninguno.

### 11. El error plantado
- Complemento con `(u, v) not in aristas`. Batería de soluciones plantadas y batería
  con aristas ordenadas: cero fallos. Aristas en orden arbitrario: falla en casi un
  tercio de las instancias "no" (283 de 900 con $n = 6$, 394 de 1356 con $n = 8$ en el
  script de verificación) y en ninguna "sí". Los números de las notas los imprime su
  propio código.
- Qué línea de la demostración lo anunciaba.

### 12. P contra NP
- Clay, 2000, siete problemas, un millón cada uno (verificado en claymath.org).
- Si P = NP: todo NP no trivial es NP-completo (demostración corta; $\emptyset$ y
  $\Sigma^*$ no pueden serlo); encontrar certificados también (ejercicio 9). Polinomial
  no quiere decir rápido en la práctica.
- Si P ≠ NP: ningún NP-completo en P; Ladner (1975) da problemas en NP − P que no son
  completos (verificado en el resumen).
- **Figura**: los dos diagramas.
- Karp 1972: 21 problemas, entre ellos clique y node cover; conjunto independiente no
  está en la lista (verificado en el escaneo de las pp. 94–96).

### 13. La regla
- "Una reducción se escribe desde lo que ya sabes difícil, y se demuestra en las dos
  direcciones". Lo que falta para que hoy sea dificultad: capítulos 17 y 18.

### Resumen y ejercicios

1. [traza] Certificado y verificador para clique, ciclo hamiltoniano, suma de
   subconjuntos; cuánto mide el certificado en bits.
2. [demostración] Clique ≤ₚ vertex cover directo, en las dos direcciones (cambiado:
   IS ≤ₚ VC quedó en el cuerpo).
3. [demostración] Transitividad de ≤ₚ.
4. [modelar] Autorreducibilidad de vertex cover.
5. [entrada que rompe] Reducción en la dirección equivocada.
6. [modelar] Ciclo hamiltoniano ≤ₚ camino hamiltoniano.
7. [modelar, implementar] 2-SAT en P por componentes fuertemente conexas.
8. [demostración] TAUTOLOGÍA en co-NP; si está en NP, NP = co-NP.
9. [cambio de hipótesis] Si P = NP, encontrar certificados en tiempo polinomial
   (cambiado: optimización de VC ya está en §2 y el ejercicio 4).
10. [demostración] Suma de subconjuntos en $O(nT)$: ¿contradice el capítulo 19?
11. [implementar y medir] Contar llamadas al oráculo en la autorreducción.

## Audios (tentativo)

| Audio | Secciones | Minutos |
|---|---|---|
| 1 | 1 y 2 | 6 |
| 2 | 3 y 4 | 7 |
| 3 | 5 | 5 |
| 4 | 6 y 7 | 6 |
| 5 | 8 y 9 | 6 |
| 6 | 10 y 11 | 6 |
| 7 | 12 y 13 | 6 |

Total estimado: 42 minutos.

## Decisiones que quiero confirmar

- **Sin Levin con año.** La página de Clay dice "Cook y Levin, 1971"; el artículo de
  Levin se publicó en 1973, y no lo pude comprobar en la fuente primaria. Las notas
  nombran solo a Cook (1971) y dejan a Levin para el capítulo 17.
- **Ningún "es NP-completo" demostrado aquí.** Se enuncia como lo que el capítulo 18
  hará.
- **Los números de la §11 los mide el propio documento** con otra semilla; la prosa
  cita lo que imprime.

Revisado contra la lista de errores de la guía (2026-11-13): (1) ninguna cota sin
demostrar, "nadie conoce" en lugar de "no existe"; (2) la verificación de `casos.py`
se rompió a propósito dos veces y falló; (3) la dirección de la reducción se explica
desde la implicación, no al revés; (4) cada demostración prometida se escribe; (6)
la búsqueda binaria se cuenta exacta; (7) todos los costos en bits; (9) cuatro citas
comprobadas.
