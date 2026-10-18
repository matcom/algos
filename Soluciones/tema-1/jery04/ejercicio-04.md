# Ejercicio 4: Contador binario en una máquina de Turing y su costo amortizado

> **Enunciados:** Diseña una máquina de Turing de una cinta que sume 1 a un número escrito en binario, con el cabezal empezando en el bit menos significativo. ¿Cuántos pasos da en el peor caso? Si se aplica $m$ veces seguidas empezando desde 0, ¿cuántos pasos da en total?
> **Ejercicio 4 (C1, C4):** El contador binario en una máquina de Turing, del ejercicio 7 de la conferencia 1. Demuestra con un potencial que $m$ incrementos desde 0 cuestan $O(m)$ pasos en total, aunque uno solo pueda costar $\Theta(\log m)$.

## 1. Definición del modelo y la representación

**Modelo de cómputo.** Se emplea una máquina de Turing con una única cinta y alfabeto $\{0, 1, \square\}$. Cada operación elemental —leer, escribir y desplazar el cabezal— se contabiliza como un paso. El cabezal se posiciona inicialmente en el bit menos significativo (LSB) y, tras cada incremento, debe regresar a esa misma posición.

**Forma de representar el contador.** El número se almacena en binario, con el LSB ocupando la casilla $b_0$; los bits se recorren de izquierda a derecha como $b_0, b_1, b_2, \ldots$, donde el bit $b_i$ tiene peso $2^i$. Inmediatamente a la izquierda de $b_0$ se coloca un blanco $\square$ que señala el inicio de la representación. A la derecha del bit más significativo (MSB) solo hay blancos. El contador arranca en $0$: la cinta contiene un único $0$ en $b_0$ y blancos en ambas direcciones.

**Procedimiento de incremento.** Estando el cabezal en $b_0$:

1. Se avanza a la derecha mientras se encuentren $1$, sustituyendo cada uno por $0$.
2. Al topar con el primer $0$ (o con un blanco), se escribe $1$.
3. Se retrocede hasta volver a $b_0$.

## 2. Construcción de la máquina de Turing

Se utilizan cuatro estados:

- $q_{\text{start}}$: estado inicial, con el cabezal en $b_0$.
- $q_{\text{carry}}$: se propaga el acarreo hacia la derecha.
- $q_{\text{back}}$: se regresa hacia $b_0$.
- $q_{\text{halt}}$: el incremento ha finalizado.

**Tabla de transiciones:**

| Estado | Lee | Escribe | Mueve | Nuevo estado |
|---|---|---|---|---|
| $q_{\text{start}}$ | $0$ | $1$ | — | $q_{\text{halt}}$ |
| $q_{\text{start}}$ | $1$ | $0$ | R | $q_{\text{carry}}$ |
| $q_{\text{carry}}$ | $1$ | $0$ | R | $q_{\text{carry}}$ |
| $q_{\text{carry}}$ | $0$ | $1$ | L | $q_{\text{back}}$ |
| $q_{\text{carry}}$ | $\square$ | $1$ | L | $q_{\text{back}}$ |
| $q_{\text{back}}$ | $0$ o $1$ | — | L | $q_{\text{back}}$ |
| $q_{\text{back}}$ | $\square$ | — | R | $q_{\text{halt}}$ |

El estado $q_{\text{back}}$ desplaza el cabezal hacia la izquierda hasta localizar el blanco previo a $b_0$, y luego avanza una casilla a la derecha para quedar justo sobre $b_0$.

## 3. Coste de un incremento aislado

Sea $t$ la cantidad de unos consecutivos a partir de $b_0$; es decir, $b_0, b_1, \ldots, b_{t-1}$ valen $1$ y $b_t$ es $0$ (o blanco).

**Situación $t \geq 1$:**

- La transición desde $q_{\text{start}}$ cambia el primer $1$ por $0$ y desplaza el cabezal a $b_1$: 1 transición.
- Estando en $q_{\text{carry}}$, cada uno de los $t-1$ unos restantes pasa a $0$ y el cabezal avanza: $t-1$ transiciones.
- En $q_{\text{carry}}$, el primer $0$ (o blanco) en $b_t$ se transforma en $1$ y el cabezal retrocede: 1 transición.
- En $q_{\text{back}}$, el cabezal recorre desde $b_{t-1}$ hasta el blanco a la izquierda de $b_0$ (esto es, $t$ posiciones) y luego una más a la derecha hasta $b_0$: $t+1$ transiciones.

Sumando:

$$C(t) = 1 + (t-1) + 1 + (t+1) = 2t + 2.$$

**Situación $t = 0$:** El cabezal encuentra un $0$ en $b_0$, lo cambia por $1$ y se detiene sin desplazarse.

$$C(0) = 1.$$

La expresión $2t + 2$ no cubre el caso $t = 0$; allí el coste es $1$.

## 4. Peor caso para un incremento individual

Es útil distinguir dos cantidades:

- $n$: el valor actual del contador.
- $m$: el número total de incrementos que se aplicarán desde $0$.

El número de bits de $n$ es $k = \lfloor \log_2 n \rfloor + 1$. Un incremento presenta $t$ unos consecutivos desde $b_0$ justamente cuando $n \equiv 2^t - 1 \pmod{2^{t+1}}$. En el peor escenario, $n$ puede tener hasta $k$ unos consecutivos, de modo que:

$$C_{\text{peor}}(n) = 2k + 2 = \Theta(\log n).$$

Al ejecutar $m$ incrementos desde $0$, los valores que se van obteniendo son $0, 1, 2, \ldots, m$. El caso más costoso entre ellos corresponde a algún $n \leq m$ con muchos unos consecutivos al final; en particular, el valor $n = 2^k - 1$ con $2^k - 1 \leq m < 2^{k+1} - 1$ produce $k = \Theta(\log m)$ unos consecutivos. Por consiguiente, el incremento más caro entre los $m$ realizados es $\Theta(\log m)$.

## 5. Análisis amortizado con potencial

Definimos el potencial:
$$\Phi = 2 \cdot \operatorname{popcount}(n),$$
donde $\operatorname{popcount}(n)$ es la cantidad de bits en $1$ de la representación binaria del valor actual del contador.

Inicialmente, $n = 0$, así que $\Phi_0 = 0$. Al final de los $m$ incrementos, $n = m$ y $\Phi_m = 2 \cdot \operatorname{popcount}(m) \geq 0$.

Consideremos un incremento con $t$ unos consecutivos desde $b_0$.

- **Costo real.** $C(t) = 2t + 2$ si $t \geq 1$; $C(0) = 1$.
- **Cambio de potencial.** Se pierden $t$ unos (cada uno aportaba $2$ al potencial) y se gana $1$ uno nuevo (que aporta $2$). Así,
  $$\Delta \Phi = 2(1 - t).$$

**Costo amortizado:**

- Si $t \geq 1$:
  $$\widehat C(t) = C(t) + \Delta \Phi = (2t+2) + 2(1-t) = 4.$$

- Si $t = 0$:
  $$\widehat C(0) = 1 + 2 = 3.$$

Por tanto, **en todos los casos**:
$$\widehat C_i \leq 4.$$

## 6. Suma amortizada y cota $O(m)$

La suma de los $m$ costos amortizados es:
$$\sum_{i=1}^{m} \widehat C_i = \sum_{i=1}^{m} C_i + \Phi_m - \Phi_0.$$

Como $\Phi_0 = 0$ y $\Phi_m \geq 0$:
$$\sum_{i=1}^{m} C_i = \sum_{i=1}^{m} \widehat C_i - \Phi_m \leq 4m - \Phi_m \leq 4m.$$

Por tanto:
$$\boxed{\sum_{i=1}^{m} C_i = O(m).}$$

> **Nota.** No se puede escribir $\sum \widehat C_i = 4m$ porque cuando $t=0$ el costo amortizado es $3$, no $4$. Lo correcto es la **desigualdad** $\widehat C_i \leq 4$ y luego $\sum \widehat C_i \leq 4m$. La conclusión $O(m)$ es la misma.

## 7. Cota más fuerte: $\Theta(m)$ y fórmula exacta

Como cada incremento requiere al menos una transición (la que escribe el nuevo bit), se tiene:
$$m \leq \sum_{i=1}^{m} C_i \leq 4m.$$

De donde:
$$\boxed{\sum_{i=1}^{m} C_i = \Theta(m).}$$

**Cota exacta.** Sea $t_i$ el número de unos consecutivos antes del incremento $i$-ésimo. Se tiene:
- $\sum_{i=1}^m t_i = m - \operatorname{popcount}(m)$ (cada uno de los $m$ nuevos $1$ creados, salvo los que quedan al final, se convierte después en $0$).
- Exactamente $\lfloor m/2 \rfloor$ incrementos tienen $t_i \geq 1$ (los que parten de un valor impar), y los restantes $\lceil m/2 \rceil$ tienen $t_i = 0$.

Por tanto:
$$\sum_{i=1}^m C_i = \sum_{t_i \geq 1}(2t_i + 2) + \sum_{t_i = 0} 1
= 2\sum_{i=1}^m t_i + 2\left\lfloor \frac{m}{2} \right\rfloor + \left\lceil \frac{m}{2} \right\rceil.$$

Sustituyendo $\sum t_i = m - \operatorname{popcount}(m)$ y usando $\lceil m/2 \rceil = m - \lfloor m/2 \rfloor$:
$$\boxed{\sum_{i=1}^m C_i = 3m + \left\lfloor \frac{m}{2} \right\rfloor - 2\operatorname{popcount}(m).}$$

Esta fórmula es exacta y confirma que el crecimiento es lineal en $m$.

## 8. Conclusiones

- **Peor caso individual:** un incremento puede costar $\Theta(\log n)$, donde $n$ es el valor actual del contador. Entre $m$ incrementos desde $0$, el peor es $\Theta(\log m)$.
- **Costo amortizado:** usando $\Phi = 2 \cdot \operatorname{popcount}(n)$, cada incremento tiene costo amortizado $\leq 4$.
- **Costo total:** $\sum_{i=1}^m C_i = O(m)$; de hecho $\Theta(m)$.
- **Respuesta al Ejercicio 7:** $m$ incrementos desde $0$ cuestan $\Theta(m)$ pasos totales, aunque un incremento aislado cueste $\Theta(\log m)$.