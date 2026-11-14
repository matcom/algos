# Ejercicio 4

## Modelo y Funcionamiento de la Máquina

Consideramos la Máquina de Turing de una cinta definida en el Ejercicio 7 de la Conferencia 1. El contador almacena un número entero en binario. El cabezal inicia posicionado en el bit menos significativo (LSB) y la operación `incrementar` realiza las siguientes transiciones:

1. **Fase de ida (LSB $\to$ MSB):** El cabezal avanza a la izquierda. Si lee un bit `1`, lo reemplaza por `0` y continúa. En cuanto lee un `0` (o una celda en blanco `␣`), lo reemplaza por `1` y finaliza la modificación.
2. **Fase de vuelta (MSB $\to$ LSB):** El cabezal retrocede hacia la derecha exactamente el mismo número de celdas recorridas a la ida para finalizar de nuevo en el LSB.

### Costo real ($c_i$)
Sea $k_i$ la cantidad de unos consecutivos de menor peso en la representación binaria previa al $i$-ésimo incremento. 

El cabezal recorre $k_i$ bits `1` más $1$ bit `0` (o celda en blanco) a la ida, e idéntica distancia de regreso. El costo real en pasos de la $i$-ésima operación es:

$$c_i = 2(k_i + 1)$$


---

## Análisis Amortizado por el Método del Potencial

### Definición de la función de potencial ($\Phi$)
Definimos la función de potencial $\Phi_i$ del estado del contador tras la $i$-ésima operación como el doble de la cantidad total de bits `1` presentes en la cinta:

$$\Phi_i = 2 \cdot (\text{número de bits } 1 \text{ en el contador después del incremento } i)$$

### Propiedades de $\Phi$:
**$\Phi_i = 0$** (Debido a que los incrementos los hacemos partiendo de 0)

**$\Phi_i \ge \Phi_0$** (Dado que el número de bits `1` es no negativo, se cumple que $\Phi_i \ge 0$ para todo $i \ge 0$)

---

## Cálculo del Costo Amortizado ($\hat{c}_i$)

En la $i$-ésima operación de incremento con $k_i$ unos consecutivos al final:
* Se cambian $k_i$ bits `1` por `0` (se pierden $k_i$ unos).
* Se cambia $1$ bit `0` (o `␣`) por `1` (se gana $1$ uno).

La variación de potencial $\Delta \Phi_i = \Phi_i - \Phi_{i-1}$ es:

$$\Delta \Phi_i = 2 \cdot (1 - k_i)$$

Calculamos el costo amortizado $\hat{c}_i$:

$$\hat{c}_i = c_i + \Delta \Phi_i$$
$$\hat{c}_i = 2(k_i + 1) + 2(1 - k_i)$$
$$\hat{c}_i = 2k_i + 2 + 2 - 2k_i = 4$$

El costo amortizado por cada incremento es estrictamente constante: $\hat{c}_i = 4 = O(1)$.

---

## Costo Total para $m$ Incrementos

El costo real total $T(m)$ de ejecutar $m$ incrementos consecutivos desde 0 es:

$$T(m) = \sum_{i=1}^{m} c_i$$

Por la propiedad telescópica del potencial:

$$\sum_{i=1}^{m} c_i = \sum_{i=1}^{m} \hat{c}_i - (\Phi_m - \Phi_0)$$

Dado que $\Phi_m \ge 0$ y $\Phi_0 = 0$:

$$T(m) \le \sum_{i=1}^{m} \hat{c}_i = \sum_{i=1}^{m} 4 = 4m$$

$$T(m) = O(m)$$

---

## Solo un incremento 
Sabemos que para representar a $m$ en binario necesitamos una cantidad de bits $b = \lfloor \log_2 m \rfloor + 1$.  Cuando el contador contiene solo unos (ej. $111\dots1_2$), $k_i = b$, tenemos que pasar por todas y cada una de estas celdas que contienen `1`,  sustituirlas por `0` y escribir un `1` en el `␣` a la izquierda de las mismas. Para devolver el cabezal a su posicion de origen, debemos  pasar nuevamente por estas, duplicando así la cantidad de pasos totales. Esto nos estaría dando un costo de $2(\lfloor \log_2 m \rfloor + 2) =  \Theta(\log m)$

