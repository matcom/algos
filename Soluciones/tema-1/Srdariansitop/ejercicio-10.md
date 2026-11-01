## Sección Pregunta 10

**Par más cercano en una dimensión.** Demuestra Ω(n log n) en árboles de decisión algebraicos por reducción desde distinción de elementos. Después di qué algoritmo de la conferencia 2 rompe la cota, en qué modelo, y adáptalo a una dimensión.

---

## Sección Demostración en árboles de decisión algebraicos por reducción desde distinción de elementos

### 1. Definiciones

**Modelo.** Un árbol de decisión algebraico de grado d sobre ℝⁿ es un árbol ternario. Cada nodo interno está etiquetado con un polinomio f ∈ ℝ[x₁,…,xₙ] de grado ≤ d y tiene tres hijos, según f(x) < 0, f(x) = 0 o f(x) > 0. Cada hoja está etiquetada con una respuesta. Un árbol *resuelve* un problema si, para toda entrada x ∈ ℝⁿ, la hoja a la que llega x lleva la respuesta correcta. Su costo es su profundidad, el número máximo de pruebas de signo en una rama.

**Distinción de elementos (ED).** Dados x₁,…,xₙ ∈ ℝ, responder "distintos" si xᵢ ≠ xⱼ para todo i ≠ j, y "hay iguales" en caso contrario.

**Par más cercano en una dimensión (PC1).** Dada una lista x₁,…,xₙ ∈ ℝ con n ≥ 2 (puede tener repetidos, como admite la sección 2 de la conferencia), responder un par de índices (i,j) con i ≠ j que minimice |xᵢ − xⱼ|. En caso de empate vale cualquiera de los pares mínimos.

La respuesta de PC1 es un par de índices, es decir, una etiqueta de hoja. No es un número calculado, porque el modelo solo ramifica por signos. El valor de la distancia se recupera después como |xᵢ − xⱼ|.

**Teorema (Ben-Or, 1983, citado).** Para cada d fijo existen c > 0 y n₀ tales que, para n ≥ n₀, todo árbol de decisión algebraico de grado ≤ d que resuelve ED sobre ℝⁿ tiene profundidad ≥ c·n log n.

### 2. Enunciado

**Teorema.** PC1 requiere Ω(n log n) en árboles de decisión algebraicos. Es decir, para cada d existen c′ > 0 y n₀ tales que todo árbol de grado ≤ d que resuelve PC1 sobre ℝⁿ, con n ≥ n₀, tiene profundidad ≥ c′·n log n.

### 3. Demostración

**Paso 1: la reducción.** Dada la entrada x = (x₁,…,xₙ) de ED, la entrada de PC1 es la misma lista x.

- Esta transformación es la identidad: cuesta 0 pruebas de signo y 0 operaciones.
- Es todavía más simple que la de la sección 8, que pasaba de ℝ a ℝ² con xᵢ ↦ (xᵢ, 0). Aquí el problema ya vive en la recta.
- Como los polinomios del árbol de PC1 se evalúan directamente sobre x, el grado no cambia.

**Paso 2 (lema de correctitud).** Sea x ∈ ℝⁿ y sea (i,j), con i ≠ j, un par que minimiza |xᵢ − xⱼ|. Entonces x tiene dos elementos iguales si y solo si xᵢ = xⱼ.

- (⇐) Si xᵢ = xⱼ con i ≠ j, hay dos iguales.
- (⇒) Si hay dos iguales, existen a ≠ b con xₐ = x_b, y entonces min_{k≠l} |xₖ − xₗ| = 0. Como (i,j) alcanza el mínimo, |xᵢ − xⱼ| = 0, o sea xᵢ = xⱼ. ∎

El lema vale aunque haya empates en PC1, porque cualquier par mínimo sirve. Si el mínimo es 0, todo par mínimo tiene distancia 0.

**Paso 3: construcción del árbol de ED.** Sea 𝒯 un árbol de grado ≤ d y profundidad T(n) que resuelve PC1 sobre ℝⁿ. Construimos 𝒯′ así:

- Conservamos todos los nodos internos de 𝒯.
- Reemplazamos cada hoja de 𝒯 etiquetada con (i,j) por un nodo interno que prueba el signo del polinomio xᵢ − xⱼ, que tiene grado 1 ≤ d. Su hijo "= 0" es una hoja "hay iguales" y sus hijos "< 0" y "> 0" son hojas "distintos".

**Paso 4: 𝒯′ resuelve ED.** Sea x ∈ ℝⁿ. El camino de x en 𝒯 es el mismo que en 𝒯′ hasta la hoja de 𝒯, que lleva un par (i,j) correcto para PC1 sobre x. Por el lema del paso 2, x tiene iguales si y solo si xᵢ − xⱼ = 0, que es exactamente lo que decide el nodo añadido. Por tanto 𝒯′ responde bien en toda entrada.

**Paso 5: costo.** La profundidad de 𝒯′ es T(n) + 1, con grado ≤ d, porque d ≥ 1 y el polinomio añadido tiene grado 1.

**Paso 6: contradicción.** Supongamos T(n) = o(n log n). Entonces, para n suficientemente grande, T(n) + 1 < c·n log n, con c y n₀ las constantes de Ben-Or para ese d. Pero 𝒯′ es un árbol de grado ≤ d que resuelve ED con profundidad T(n) + 1 < c·n log n, lo que contradice el teorema de Ben-Or. Luego T(n) ≠ o(n log n), y en concreto T(n) ≥ c′·n log n para constantes adecuadas. ∎

**Observaciones.**

1. **La cota es ajustada.** Ordenar y recorrer los n − 1 huecos consecutivos es un árbol algebraico de profundidad O(n log n) (lema de la sección 3). Por tanto PC1 es Θ(n log n) en este modelo.
2. **Sobre la hipótesis "lista con repetidos".** La reducción necesita entradas con repetidos, porque ahí es donde la respuesta de PC1 es 0. Si PC1 se definiera solo sobre conjuntos, no estaría definido sobre las entradas "hay iguales", y la reducción no tendría sentido tal cual.
3. **Lo que se usa del teorema de Ben-Or.** Solo se usa como caja negra, como en la conferencia. La demostración original cuenta las n! componentes conexas del conjunto "todos distintos" y las acota con Milnor–Thom: un árbol de profundidad h y grado d tiene a lo sumo 3ʰ hojas, cada una con a lo sumo d(2d−1)ⁿ⁺ʰ⁻¹ componentes, de donde h = Ω(log n!) = Ω(n log n).

---

## Sección Algoritmo que rompe la cota, modelo y adáptalo a tu dimensión

### 1. Qué algoritmo rompe la cota

Es **el algoritmo incremental aleatorio de la sección 9**, con rejilla en tabla hash (ideas de Rabin, versión de Kleinberg–Tardos §13.7). Los demás quedan dentro del modelo y no rompen nada:

- La fuerza bruta (sección 4) solo compara distancias, y cuesta Θ(n²).
- Divide y vencerás (secciones 5 a 7) solo ordena, compara y suma, y cuesta O(n log n). Es óptimo en el modelo, no lo rompe.
- En una dimensión, ordenar y mirar consecutivos es otro árbol algebraico de profundidad O(n log n).

### 2. En qué modelo

El algoritmo vive en una **RAM aleatorizada con función parte entera (⌊·⌋), direccionamiento indirecto y tablas hash de tiempo esperado O(1)**, donde cada una de esas operaciones cuesta una unidad. Su costo, O(n), es un costo **esperado**.

### 3. Por qué se sale del modelo de la cota

Cada punto es un argumento sólido, y ninguno de ellos es "el azar":

**(a) La parte entera no es un árbol algebraico.** El algoritmo calcula ⌊x/δ⌋ para convertir un punto en el índice de su celda.

- Una prueba de signo solo decide si un polinomio es negativo, cero o positivo.
- Para entradas en [0, M], ⌊x⌋ toma M + 1 valores distintos. Un árbol de profundidad h tiene a lo sumo 3ʰ hojas, así que calcular ⌊x⌋ exige profundidad ≥ log₃(M + 1), que crece sin cota con la magnitud de la entrada y no con n.
- La parte entera tampoco es polinomio ni función continua.

**(b) El direccionamiento indirecto no existe en el árbol.** El algoritmo usa el índice calculado como dirección para consultar la tabla hash.

- Un árbol no tiene memoria direccionable. Su única operación es ramificar según el signo de un polinomio de la entrada.
- Emular un acceso a una tabla de m celdas con direcciones que dependen de los datos obligaría al árbol a ramificar Ω(log m) veces, en lugar de una.

**(c) El azar no es lo que rompe la cota.** Grigoriev, Karpinski, Meyer auf der Heide y Smolensky (1996) probaron que ED sigue requiriendo Ω(n log n) en árboles algebraicos aleatorizados. Por la reducción de arriba, PC1 también. Barajar solo sirve para que se esperen pocas reconstrucciones.

**(d) No hay contradicción con el teorema anterior.** Este teorema habla de árboles algebraicos, y el algoritmo no es uno. Son dos modelos distintos, y el segundo es estrictamente más poderoso para este problema. Una cota mínima siempre viene con su modelo pegado.

### 4. Adaptación a una dimensión

**Diseño de la rejilla.** Sea δ la distancia mínima entre los puntos ya insertados. Dividimos la recta en celdas semiabiertas de longitud δ:

celda(q) = ⌊q/δ⌋, que corresponde al intervalo [kδ, (k+1)δ).

En 2D la celda tenía lado δ/2 para que su diagonal fuera < δ. En 1D basta longitud δ, porque no hay diagonal.

**Invariante: cada celda contiene a lo sumo un punto.**

- Dos puntos de la misma celda [kδ, (k+1)δ) están a distancia estrictamente menor que δ.
- Pero δ es la mínima distancia entre los puntos insertados, así que eso es imposible. ∎

**Búsqueda local: solo hay que mirar 3 celdas.**

- Si |p − q| < δ, entonces |p/δ − q/δ| < 1.
- Dos números reales que difieren en menos de 1 tienen partes enteras que difieren en a lo sumo 1.
- Luego q está en la celda de p o en una vecina, es decir, en k − 1, k o k + 1, con k = ⌊p/δ⌋.
- Cada celda tiene a lo sumo un punto por el invariante, así que son a lo sumo 3 accesos a la tabla. En 2D eran 25.

**Algoritmo.**

1. Permutar los puntos al azar: p₁,…,pₙ.
2. δ ← |p₁ − p₂| y par ← (p₁,p₂). Si δ = 0, devolver 0, porque ya no puede bajar. Si no, rejilla ← {⌊p₁/δ⌋ ↦ p₁, ⌊p₂/δ⌋ ↦ p₂}.
3. Para i = 3,…,n:
   - Sea k = ⌊pᵢ/δ⌋. Consultar las celdas k − 1, k, k + 1. Para cada q hallado con |pᵢ − q| < δ, actualizar δ ← |pᵢ − q| y par ← (pᵢ, q).
   - Si δ no bajó, insertar pᵢ en la celda k.
   - Si δ bajó, devolver 0 si δ = 0. Si no, reconstruir la rejilla con lado δ′ para p₁,…,pᵢ, donde δ′ es el nuevo δ.
4. Devolver (δ, par).

```python
import math, random

def par_mas_cercano_1d(X, semilla=0):
    pts = list(X)
    random.Random(semilla).shuffle(pts)
    d = abs(pts[0] - pts[1])
    par = (pts[0], pts[1])
    if d == 0:
        return 0.0, par
    rejilla = {math.floor(q / d): q for q in pts[:2]}
    for i in range(2, len(pts)):
        p = pts[i]
        k, antes = math.floor(p / d), d
        for c in (k - 1, k, k + 1):              # solo 3 celdas
            q = rejilla.get(c)
            if q is not None and abs(p - q) < d:
                d, par = abs(p - q), (p, q)
        if d < antes:                             # δ bajó: reconstruir
            if d == 0:
                return 0.0, par
            rejilla = {math.floor(q / d): q for q in pts[:i + 1]}
        else:
            rejilla[k] = p
    return d, par
```

La implementación usa aritmética exacta idealizada. Con flotantes, el redondeo de q/d podría violar el invariante en casos límite.

**Correctitud (por inducción sobre i).** La hipótesis es que, tras insertar i puntos, δ es la mínima distancia entre ellos y la rejilla cumple el invariante.

- *Base.* Para i = 2, δ = |p₁ − p₂| es la mínima distancia, y los dos puntos están en celdas distintas, porque su distancia es exactamente δ y no menor.
- *Paso.* Al llegar pᵢ, cualquier punto q con |pᵢ − q| < δ está en las celdas k − 1, k o k + 1, y la rejilla las contiene todas por la hipótesis. Si el algoritmo no encuentra ninguno, la mínima distancia no cambia. Si encuentra alguno, se queda con el menor, que es la nueva mínima distancia, porque la mínima del conjunto ampliado es el mínimo entre la anterior y las distancias de pᵢ a los demás, y solo las menores que δ importan.
- *Rejilla.* Si δ no cambia, insertar pᵢ en su celda mantiene el invariante: si la celda ya tuviera un punto, estaría a distancia < δ de pᵢ, y habría sido detectado y habría bajado δ. Si δ bajó, la rejilla se reconstruye con el nuevo δ, que es la mínima distancia entre los i puntos, así que el invariante vale por el argumento de arriba.

**Costo esperado.**

- Cada inserción cuesta O(1): 3 consultas a la tabla hash más una inserción.
- Una reconstrucción en el paso i cuesta O(i).
- **Análisis hacia atrás.** Fijemos el conjunto S = {p₁,…,pᵢ} sin importar el orden en que llegó. Hay reconstrucción en el paso i si y solo si el δ de S es estrictamente menor que el de S ∖ {pᵢ}. Eso ocurre si y solo si todos los pares mínimos de S contienen a pᵢ.
- En 1D los empates pueden ser muchos, por ejemplo puntos equiespaciados, así que hay que verlo con cuidado. La intersección de todos los pares mínimos está contenida en uno cualquiera de ellos, y por tanto tiene a lo sumo 2 elementos.
- Como el orden es una permutación uniforme, pᵢ es uniforme entre los i elementos de S. Entonces Pr[reconstruir en el paso i] ≤ 2/i.
- Por linealidad de la esperanza:

𝔼[costo] = O(n) + Σᵢ₌₃ⁿ (2/i)·O(i) = O(n) + Σᵢ O(1) = O(n).

- El número esperado de reconstrucciones es ≤ Σ 2/i ≈ 2 ln n, igual que en la conferencia.
- La memoria es O(n).

**Resumen.** En una dimensión el algoritmo es más simple que en 2D: celdas de longitud δ en lugar de δ/2, 3 celdas a mirar en lugar de 25, y el mismo costo esperado O(n). Resuelve PC1 en tiempo lineal esperado en el modelo RAM con parte entera y hash, mientras que en árboles de decisión algebraicos es imposible hacerlo en menos de Ω(n log n).

## Código

**1. `fig1_problema.png` (el problema).** Dibuja 9 puntos aleatorios en la recta con el par más cercano marcado en rojo y su distancia d. Debajo, un gráfico de barras con los n−1 huecos consecutivos del orden, donde la barra roja es el mínimo. Muestra que PC1 pide un par de índices (i, j) y que, tras ordenar, la respuesta está entre los huecos consecutivos.

**2. `fig2_reduccion.png` (la reducción ED ≤ PC1).** Es un diagrama de la demostración. La entrada de ED pasa por la identidad, con 0 pruebas, al árbol T que resuelve PC1. Cada hoja (i, j) se sustituye por un nodo que prueba el signo de xᵢ − xⱼ, con tres hijos: "<0 distintos", "=0 hay iguales" y ">0 distintos". El panel de la derecha resume la conclusión: T′ resuelve ED con profundidad T(n)+1, y por Ben-Or, PC1 = Ω(n log n).

**3. `fig3_componentes_cota.png` (de dónde sale la cota).** A la izquierda, para n=3, el plano x₁+x₂+x₃=0 cortado por las rectas xᵢ=xⱼ en 3! = 6 regiones, cada una rotulada con su orden. Son las componentes conexas de "todos distintos". A la derecha, la curva log₃(n!) comparada con n log₂ n, con n y con n(n−1)/2. Ilustra que un árbol de profundidad h tiene como mucho 3ʰ hojas, y que con n! componentes hace falta h ≥ log₃ n! = Ω(n log n).

**4. `fig4_modelo_floor.png` (por qué el algoritmo sale del modelo).** A la izquierda, la función ⌊x/δ⌋ como escalera discontinua frente a la recta x/δ, que sí es polinomio. A la derecha, la profundidad mínima log₃(M+1) que necesitaría un árbol para calcular ⌊x⌋ con x∈[0,M], que crece con la magnitud M, frente al costo 1 de la operación en la RAM. Es el argumento (a) de la sección 2: la parte entera no es una prueba de signo.

**5. `fig5_rejilla_1d.png` (la rejilla en una dimensión).** Muestra la recta dividida en celdas de longitud δ, con puntos ya insertados y un punto nuevo en naranja. Las celdas k−1, k y k+1 aparecen en amarillo, porque solo en ellas puede haber un punto a distancia menor que δ. Un texto recuerda el invariante de que cada celda tiene como mucho un punto, y el título que son 3 celdas en 1D frente a 25 en 2D.

**6. `fig6_algoritmo_incremental.gif` (animación paso a paso).** Ejecuta el algoritmo incremental aleatorio sobre 11 puntos y tiene 20 cuadros. En cada paso se ven la rejilla de lado δ, el punto que llega, las 3 celdas consultadas, el par más cercano actual en rojo y el valor de δ. Cuando δ baja, el cuadro lo indica con "se reconstruye la rejilla". Si δ no baja, indica que el punto se inserta en O(1). El último cuadro da el resultado.

**7. `fig7_costos_experimentales.png` (experimento de costo).** Mide el algoritmo con contadores de operaciones para n entre 100 y 25 600, promediando 15 semillas. A la izquierda, en escala log-log, la rejilla queda por debajo de n log₂ n y de n(n−1)/2. A la derecha, las operaciones por elemento son casi constantes, alrededor de 6, y las reconstrucciones medidas quedan por debajo de la cota teórica 2 ln n. Confirma el O(n) esperado, pero es una medición en una RAM con ⌊·⌋ y hash, no una violación de la cota en árboles algebraicos.