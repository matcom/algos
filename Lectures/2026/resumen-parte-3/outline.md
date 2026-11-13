# Outline: Resumen de la Parte III, Intratabilidad

Estado: redactado (2026-11-13). El texto está en `notas.md`.
Destino: `Lectures/2026/resumen-parte-3/notas.md`, sección sin número del libro.
Extensión objetivo: 3 500–4 500 palabras, más los ejercicios.

## Para qué sirve

Documento de repaso, con la forma de `tema-1/resumen.md`. Tres usos: estudiar para
el examen, ver la Parte III entera de una vez (ideas que solo aparecen juntando
capítulos) y practicar con ejercicios que mezclan capítulos. Sin material nuevo, sin
código ejecutable y sin figuras nuevas. Remite por capítulo y sección.

## Estructura

### 1. El mapa de la parte

Dos mitades. Capítulos 16 a 19: ¿es difícil? (definiciones, el primer NP-completo,
reducciones a grafos y a números). Capítulos 20 a 23: ¿qué se hace si lo es? (exacto
exponencial, aproximación con razón, relajación lineal, esquemas). Una tabla: capítulo,
pregunta, herramienta, ejemplo trabajado, error plantado.

### 2. Lo que hay que llevarse de cada capítulo

Una idea por capítulo, la que usan los demás. No repite los resúmenes.

### 3. Cinco ideas que atraviesan la parte

1. **Un problema, ocho capítulos.** Tabla de vertex cover, mochila y TSP a lo largo de
   la parte: dónde se demuestra que es difícil, qué algoritmo exacto, qué
   aproximación, qué se sabe que no se puede.
2. **Los números deciden.** Pseudopolinomial (16) → la meta de 10^(n+k) dígitos (19,
   ejercicio 9) → la poda de mochila (20) → FPTAS y fuertemente NP-duro (23).
3. **Una cota calculable del óptimo hace dos trabajos.** Podar en el exacto (la
   mochila fraccionaria, 20 §3) y garantizar la razón (emparejamiento, máx t_j, árbol,
   relajación lineal, v_max). La relajación como cota general (22 §14).
4. **Una reducción lleva más que un sí o un no.** La misma idea de reducción se usa
   para: NP-completitud (16–19), la ETH (20 §12, depende de que el tamaño sea
   lineal), imposibilidad de aproximar con hueco (21 §9, 22 §2, 21 ej. 4) y fuerte
   NP-dureza (23 §8). Y lo que una reducción no conserva: la razón, el parámetro.
5. **Los ocho errores plantados.** Tabla. En 16–19 viven en la dirección "no ⇒ no" y
   las instancias sí no los ven. En 20–23 viven en la hipótesis de la cota y las
   entradas donde esa hipótesis vale sola no los ven. La comprobación que no puede
   fallar (22 §13).

### 4. Cómo se ve una respuesta completa

Dos respuestas modelo cortas, con material del libro: una NP-completitud (vertex
cover ≤ set cover, capítulo 18 §5) y una aproximación (vertex cover por
emparejamiento, capítulo 21 §3). La forma: pertenencia a NP, conocido, construcción y
costo, dos direcciones; y algoritmo, factibilidad, cota del óptimo, razón, tiempo.

### 5. Ejercicios

Diez, integradores, cada uno con los capítulos que usa y su dificultad. Mezcla: 2 de
traza, 3 de demostración, 2 de implementar y medir, 1 de entrada que rompe, 1 de
cambio de hipótesis, 1 de modelar. Ninguno repite un ejercicio de capítulo.

1. Traza: C5 por los cuatro tratamientos de vertex cover (16, 20, 21, 22).
2. Traza: una fórmula por las reducciones a independiente, 3-coloración y suma de
   subconjuntos; tamaños y la asignación en cada una (17, 18, 19).
3. Demostración: el complemento conserva el óptimo y no la razón (16, 21).
4. Demostración: dominante como set cover; por qué la razón 2 de k-center no pasa a
   dominante (18, 21).
5. Demostración: qué hipótesis refutaría cada resultado hipotético (16, 20, 21, 22, 23).
6. Entrada que rompe: Christofides sobre la clausura métrica para el TSP general (19, 22).
7. Cambio de hipótesis: los números en unario (16, 19, 20, 23).
8. Implementar y medir ★: branch and bound para vertex cover con la cota del
   emparejamiento y con la relajación (20, 21, 22).
9. Implementar y medir: 3-SAT → independiente → `independiente_max` contra la fuerza
   bruta; qué le hace la reducción a la base (17, 18, 20).
10. Modelar: un laboratorio con trabajos, servidores y rutas (11, 21, 22, 23).

## Verificación

- Cada número citado aparece en el capítulo que se cita (script
  `.playground/libro-daa/verif/R3/numeros.py`).
- El ejercicio 1 se corrió con el código de los capítulos 20 y 22
  (`verif/R3/e1_c5.py`): está bien planteado y tiene respuestas distintas en cada
  apartado.
- El ejercicio 9 se probó a tamaños chicos para fijar un rango que corre en segundos
  (`verif/R3/e9_pipeline.py`).
