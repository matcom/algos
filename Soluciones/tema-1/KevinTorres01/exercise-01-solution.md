# Ejercicio 1 — Una computadora 1000 veces más rápida

**Diseño y Análisis de Algoritmos · Tema 1 · Curso 2026**

> Una computadora 1000 veces más rápida. ¿Cuánto crece el tamaño de entrada que se resuelve en una hora con un algoritmo Θ(n²)? ¿Y con uno Θ(n log n)? Estima los dos factores. (C1)

---

## 1. Modelo

Trabajamos en el modelo de costo de la Conferencia 1 (word RAM). Como es habitual con notación asintótica, no nos interesan las constantes multiplicativas ni los segundos reales: lo que importa es cómo crece la cantidad de trabajo con el tamaño de la entrada. Los logaritmos se toman en base 2 salvo que se indique otra cosa.

## 2. Definiciones

**Sobre el algoritmo.**

- $f(m)$ es la cantidad de operaciones elementales que ejecuta **el algoritmo** cuando procesa una entrada de tamaño $m$. Es una propiedad del algoritmo, no de la computadora. Las dos máquinas que comparamos ejecutan el mismo algoritmo, así que sobre la misma entrada de tamaño $m$ realizan exactamente la misma cantidad de operaciones, $f(m)$. Lo que distingue a las máquinas es cuántas operaciones pueden hacer por unidad de tiempo, no cuántas hay que hacer.

**Sobre las máquinas.**

- $v$ es la cantidad de operaciones por hora que realiza la computadora vieja.
- $v' = 1000\,v$ es la cantidad de operaciones por hora que realiza la computadora nueva. “1000 veces más rápida” significa exactamente esto: en el mismo tiempo hace 1000 veces más operaciones. No significa que resuelva entradas 1000 veces más grandes; eso es justamente lo que hay que calcular.
- $c = v \times 1\text{ hora}$ es la cantidad de operaciones que la computadora vieja puede ejecutar en una hora. Es un dato del hardware: un número positivo, arbitrario pero fijo. No lo elegimos ni necesitamos conocerlo.
- $c' = v' \times 1\text{ hora} = 1000\,c$ es la cantidad de operaciones que la computadora nueva puede ejecutar en una hora.

**Sobre los tamaños máximos.**

- $n$ es el mayor tamaño de entrada que la computadora vieja logra procesar en una hora:
  $$
  n := \max\{\,m : f(m) \le c\,\}.
  $$
- $n'$ es el mayor tamaño de entrada que la computadora nueva logra procesar en una hora:
  $$
  n' := \max\{\,m : f(m) \le c'\,\}.
  $$

Estas son definiciones, no supuestos: $n$ y $n'$ quedan determinados por $f$, $c$ y $c'$. El objetivo del ejercicio es calcular el factor $k := n'/n$, que indica cuántas veces más grande es la entrada que entra en una hora al cambiar la computadora.

## 3. La frontera y la igualdad $f(n)=c$

Por ser $n$ el mayor tamaño cuyo trabajo todavía cabe en la capacidad $c$, se cumple

$$
f(n) \le c \quad\text{y}\quad f(n+1) > c.
$$

Es decir: en $n$ el trabajo entra, y con un elemento más ya no. Si se permite que el tamaño sea real (o, equivalentemente, en el modelo asintótico donde se ignoran los términos de orden inferior), la frontera es el punto donde el trabajo iguala la capacidad:

$$
f(n) = c. \tag{1}
$$

Esto no es forzar una igualdad arbitraria: es la traducción al modelo asintótico de la definición de frontera. Si $n$ fuera entero y $f(n) < c < f(n+1)$, la diferencia entre $c$ y $f(n)$ es menor que el salto $f(n+1)-f(n)$, que para las funciones de este ejercicio ($m^2$, $m\log m$) es un término de orden inferior a $f(n)$. Ese término desplaza $n$ en menos de un elemento, lo que es un factor $1+O(1/n)$ que tiende a 1 y no afecta el cociente $n'/n$ en el límite.

Lo mismo vale para la máquina nueva, por la misma definición de frontera aplicada a la capacidad $c'$:

$$
f(n') = c' = 1000\,c. \tag{2}
$$

Nótese que $c$ es un símbolo, no un número que haya que inventar: aparece en las definiciones de $n$ y $n'$, y se cancela al comparar ambas fronteras.

## 4. Relación fundamental entre $n$ y $n'$

De (1) se despeja $c = f(n)$. Sustituyendo en (2):

$$
\boxed{\,f(n') = 1000\,f(n)\,} \tag{3}
$$

Esta es la única ecuación que se usa en todo el ejercicio. La capacidad $c$ desapareció: no importa cuánto valga, la relación entre $n$ y $n'$ depende solo de $f$. Lo único que cambia entre los dos casos es la función $f$, que describe cómo crece el trabajo del algoritmo con el tamaño de la entrada.

## 5. Caso $\Theta(n^2)$: $f(m) = m^2$

Sustituyendo en (3):

$$
(n')^2 = 1000\,n^2.
$$

Como $n$ y $n'$ son positivos, se puede tomar raíz cuadrada en ambos lados:

$$
n' = \sqrt{1000}\,n = 10\sqrt{10}\,n.
$$

Por lo tanto

$$
\boxed{\;k = \frac{n'}{n} = 10\sqrt{10} \approx 31.62\;}
$$

**Observaciones.**

- El factor es **exacto y constante**: no depende de $n$ ni de $c$. La razón es que $m^2$ es **homogénea**: escalar la entrada por $k$ escala el trabajo por $k^2$, sin importar desde qué $n$ se parta. La $n$ se cancela en la ecuación.
- El número es coherente: $31.62^2 \approx 1000$, porque si el tamaño crece por un factor $k$, el trabajo crece por $k^2$, y se busca que el trabajo crezca por 1000.
- La cancelación de $c$ es explícita: de $n^2=c$ sale $n=\sqrt{c}$, y de $(n')^2=1000c$ sale $n'=\sqrt{1000c}=\sqrt{1000}\sqrt{c}$; al dividir, $\sqrt{c}$ se cancela.

**Resultado del caso cuadrático.** Una computadora 1000 veces más rápida permite, con un algoritmo cuadrático, procesar en una hora entradas **unas 31.6 veces más grandes**.

## 6. Caso $\Theta(n\log n)$: $f(m) = m\log_2 m$

Sustituyendo en (3):

$$
n'\log_2 n' = 1000\,n\log_2 n. \tag{4}
$$

A diferencia del caso cuadrático, la incógnita $n'$ aparece dos veces: una como factor y otra dentro del logaritmo. Eso convierte a (4) en una ecuación trascendente, sin solución elemental. Antes de intentar resolverla, conviene preguntarse si existe un factor $k$ constante que sirva para todo $n$, como en el caso anterior.

### 6.1 Intento de factor constante

Escribimos $n' = k\,n$ en (4) y dividimos entre $n$:

$$
k\log_2(kn) = 1000\log_2 n.
$$

Usando $\log_2(kn)=\log_2 k+\log_2 n$:

$$
k\log_2 k + k\log_2 n = 1000\log_2 n.
$$

Agrupando los términos que contienen $\log_2 n$:

$$
k\log_2 k = (1000-k)\log_2 n. \tag{5}
$$

### 6.2 Demostración de que no existe un factor constante

Supongamos que existiera un $k$ constante que satisface (5) para todo $n$. Entonces el lado izquierdo $k\log_2 k$ sería un número fijo, mientras que el lado derecho $(1000-k)\log_2 n$ crece con $n$. Una constante no puede ser igual a algo que crece. Contradicción.

Por lo tanto, **ningún $k$ constante satisface la ecuación para todo $n$**: el factor tiene que depender de $n$. En otras palabras, para un algoritmo $n\log n$ **no existe un único número $k$** que responda la pregunta del ejercicio; el factor $k(n)$ es una función del tamaño de partida.

### 6.3 Por qué la $n$ no se cancela

La razón es estructural. En el caso cuadrático, $m^2$ es homogénea: escalar la entrada por $k$ escala el trabajo por $k^2$, y la $n$ se cancela al dividir. En $m\log m$ eso no pasa: al escalar la entrada por $k$, el trabajo no se escala por un factor que dependa solo de $k$, sino que aparece $\log n$ mezclado con $\log k$ en el término $\log_2(kn)=\log_2 k+\log_2 n$. Ese término sobrante es el que impide cancelar la $n$, y es exactamente lo que aparece en (5). La falta de homogeneidad de $m\log m$ es la causa de que el factor herede una dependencia con el punto de partida.

### 6.4 Qué sí se puede afirmar

Aunque no exista un $k$ constante, la ecuación (5) **determina unívocamente** un factor para cada $n$. En efecto, para $n>1$ definimos

$$
F_n(k) := k\log_2(kn) - 1000\log_2 n,
$$

cuya raíz es la solución de (5). Derivando (regla del producto):

$$
F_n'(k) = \log_2(kn) + \frac{1}{\ln 2} > 0
$$

para todo $k>0$ (si $\log_2(kn)$ es negativo, el término $\frac{1}{\ln 2}\approx 1.44$ lo compensa). Por lo tanto, $F_n$ es estrictamente creciente. Además $F_n(0^+)=-1000\log_2 n<0$ para $n>1$, y $F_n(1000)=1000\log_2 1000>0$. Por el teorema del valor intermedio, existe exactamente una raíz $k^*(n)\in(0,1000)$. Es decir: para cada $n$ hay un factor, es único, y está entre 0 y 1000, pero **no es el mismo para todo $n$**.

De (5) se deducen además los límites:

- Cuando $n\to 1^+$, el lado derecho $(1000-k)\log_2 n\to 0$, lo que obliga a $k\log_2 k\to 0$ y por lo tanto $k\to 1$.
- Cuando $n\to\infty$, el lado derecho $\to\infty$, lo que obliga a $1000-k\to 0$ y por lo tanto $k\to 1000$.

Por lo tanto, el factor $k(n)$ recorre el intervalo $(1,1000)$: empieza cerca de 1 para tamaños pequeños y se acerca a 1000 para tamaños grandes, con convergencia logarítmica y, por lo tanto, extremadamente lenta.

## 7. Conclusión

| Complejidad del algoritmo | ¿Existe $k$ constante? | Factor $k=n'/n$ |
|---|---|---|
| $\Theta(n)$ | Sí | $1000$ (exacto) |
| $\Theta(n^2)$ | Sí | $10\sqrt{10}\approx 31.62$ (exacto, independiente de $n$) |
| $\Theta(n\log n)$ | **No** | $k=k(n)$, único en $(1,1000)$ que resuelve $k\log_2 k=(1000-k)\log_2 n$; va de $1$ a $1000$ cuando $n$ crece |

De aquí se deduce que el factor de mejora sobre el tamaño de entrada nunca coincide con el factor de mejora del hardware, salvo en el caso lineal. Cuanto más rápido crece el algoritmo, menos se aprovecha la mejora de la máquina:

- un algoritmo cuadrático apenas gana un factor $\sqrt{1000}\approx 31.62$, exacto y universal;
- uno $n\log n$ no tiene un factor universal: el factor depende del tamaño de partida y solo se aproxima a 1000 de forma logarítmica.

La diferencia entre ambos casos no es de método, sino de naturaleza matemática: $m^2$ es homogénea y permite cancelar $n$; $m\log m$ no lo es, y por eso el factor hereda una dependencia con $n$. Por lo tanto, la lección de la Conferencia 1 que este ejercicio ilustra es que la mejora del hardware se traduce en una mejora del tamaño resoluble **según el orden de crecimiento del algoritmo**, y que es indispensable fijar un modelo de costo en operaciones, y no en segundos, para que la pregunta esté bien planteada.