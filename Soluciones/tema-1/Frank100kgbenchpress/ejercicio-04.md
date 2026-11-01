# Ejercicio 4: El contador binario en una máquina de Turing (Análisis Amortizado)

**Enunciado:** Demuestra con un potencial que \(m\) incrementos desde 0 cuestan \(O(m)\) pasos en total, aunque uno solo pueda costar \(\Theta(\log m)\). Es la pregunta que la conferencia 1 dejó abierta. (C1, C4)

**Modelo:** Máquina de Turing de una cinta. El contador se representa en binario. Para simplificar el análisis, contamos los pasos correspondientes al acarreo: recorrer los bits en 1, cambiarlos a 0 y modificar el siguiente bit a 1.

---

## 1. El peor caso de una sola operación

Supongamos que el contador tiene el valor \(2^k-1\), es decir, todos sus bits son 1.

Por ejemplo, para \(k=4\):

\[
1111_2+1=10000_2
\]

Al incrementar el contador, el cabezal debe:

1. Leer el primer bit 1, cambiarlo por 0 y desplazarse a la izquierda.
2. Leer el segundo bit 1, cambiarlo por 0 y desplazarse a la izquierda.
3. Repetir el procedimiento hasta haber cambiado los \(k\) bits a 0.
4. Al llegar al siguiente bit (0 o una celda en blanco), escribir un 1.

Por tanto, una sola operación puede requerir:

\[
c=k+1
\]

Como el número de bits necesarios para representar un valor \(m\) es del orden de \(\log_2 m\), en el peor caso una operación individual puede costar:

\[
\boxed{\Theta(\log m)}
\]

Sin embargo, esto no significa que todas las operaciones tengan ese costo. La mayoría de los incrementos modifican solamente uno o dos bits.

---

## 2. Análisis amortizado con el método del potencial (C4)

El análisis amortizado permite demostrar que, aunque algunas operaciones individuales sean costosas, el costo total de una secuencia de operaciones puede ser pequeño.

Para ello, utilizamos una función de potencial que representa el trabajo acumulado o crédito disponible en la estructura.

### Definición del potencial

Sea \(\Phi_i\) el número de bits en 1 que tiene el contador después de la \(i\)-ésima operación de incremento.

Definimos:

\[
\boxed{\Phi_i=\text{número de bits en 1 después de la operación }i}
\]

Esta función cumple dos propiedades:

- Inicialmente, el contador vale 0, por lo que:

  \[
  \Phi_0=0
  \]

- Como la cantidad de bits en 1 nunca puede ser negativa:

  \[
  \Phi_i\geq 0
  \]

### Costo real de una operación (\(c_i\))

Supongamos que, antes de incrementar el contador, existen \(t\) bits consecutivos en 1 en las posiciones menos significativas.

Al sumar 1:

- Los \(t\) bits en 1 se convierten en 0.
- El siguiente bit (0 o una nueva posición en blanco) se convierte en 1.

Por tanto, el costo real de la operación es:

\[
\boxed{c_i=t+1}
\]

### Cambio de potencial (\(\Delta\Phi_i\))

Antes de la operación teníamos \(t\) bits en 1 en la parte menos significativa.

Después de incrementar:

- Se pierden \(t\) unos.
- Se gana un nuevo 1.

Por tanto, el cambio de potencial es:

\[
\Delta\Phi_i=\Phi_i-\Phi_{i-1}
\]

\[
\boxed{\Delta\Phi_i=1-t}
\]

### Costo amortizado (\(a_i\))

El costo amortizado se define como la suma del costo real y el cambio de potencial:

\[
a_i=c_i+\Delta\Phi_i
\]

Sustituyendo las expresiones anteriores:

\[
a_i=(t+1)+(1-t)
\]

Simplificando:

\[
\boxed{a_i=2}
\]

**Conclusión de la operación individual:**

Cada incremento tiene un costo amortizado constante de 2, independientemente de la cantidad de bits que haya que modificar durante el acarreo.

---

## 3. Costo total para \(m\) incrementos

Queremos demostrar que el costo real total de realizar \(m\) incrementos desde cero es \(O(m)\).

Para ello, utilizamos la propiedad telescópica de los costos amortizados:

\[
a_i=c_i+\Phi_i-\Phi_{i-1}
\]

Sumando para las \(m\) operaciones:

\[
\sum_{i=1}^{m}a_i=
\sum_{i=1}^{m}c_i+
\sum_{i=1}^{m}(\Phi_i-\Phi_{i-1})
\]

La suma de los cambios de potencial se simplifica porque los términos intermedios se cancelan:

\[
\sum_{i=1}^{m}a_i=
\sum_{i=1}^{m}c_i+\Phi_m-\Phi_0
\]

Sabemos que:

- Cada operación tiene un costo amortizado de 2:

  \[
  \sum_{i=1}^{m}a_i=2m
  \]

- El potencial inicial es cero:

  \[
  \Phi_0=0
  \]

- El potencial final es no negativo:

  \[
  \Phi_m\geq0
  \]

Sustituyendo:

\[
2m=\sum_{i=1}^{m}c_i+\Phi_m
\]

Despejando el costo real total:

\[
\sum_{i=1}^{m}c_i=2m-\Phi_m
\]

Como \(\Phi_m\geq0\):

\[
\sum_{i=1}^{m}c_i\leq2m
\]

Por tanto:

\[
\boxed{\sum_{i=1}^{m}c_i=O(m)}
\]

Además, cada incremento modifica al menos el bit menos significativo, por lo que cada operación tiene un costo real de al menos una unidad. En consecuencia:

\[
\sum_{i=1}^{m}c_i\geq m
\]

Combinando ambas cotas:

\[
\boxed{T(m)=\Theta(m)}
\]

Esto demuestra que el costo total de los \(m\) incrementos es lineal.

---

## 4. ¿Por qué funciona el análisis amortizado?

La idea fundamental es que los bits en 1 representan un crédito acumulado que permite pagar los acarreos futuros.

Cada vez que un bit cambia de 0 a 1, aumenta el potencial en una unidad. Posteriormente, cuando ese bit cambia de 1 a 0 como consecuencia de un acarreo, el potencial disminuye y ese crédito ayuda a compensar el costo de la operación.

Además, podemos observar que:

- El bit menos significativo cambia en todos los incrementos.
- El segundo bit cambia cada dos incrementos.
- El tercer bit cambia cada cuatro incrementos.
- El cuarto bit cambia cada ocho incrementos.

Y así sucesivamente.

La cantidad total de cambios puede expresarse mediante una serie geométrica:

\[
m+\frac{m}{2}+\frac{m}{4}+\frac{m}{8}+\cdots
\]

Esta serie está acotada por:

\[
m\left(1+\frac12+\frac14+\frac18+\cdots\right)
\]

Como la serie geométrica converge a 2:

\[
\boxed{T(m)\leq2m}
\]

Esto coincide con el resultado obtenido mediante el método del potencial.

### Nota sobre los movimientos del cabezal

El análisis anterior cuenta los pasos correspondientes al acarreo.

Si también se incluye el regreso del cabezal al bit menos significativo, el costo total sigue siendo \(O(m)\), siempre que el regreso recorra únicamente el segmento utilizado durante el acarreo.

En efecto, si \(t_i\) es la cantidad de unos consecutivos que se modifican en el incremento \(i\), se cumple:

\[
\sum_{i=1}^{m}t_i
=
\sum_{j\geq1}\left\lfloor\frac{m}{2^j}\right\rfloor
<m
\]

Por tanto, tanto los movimientos de ida como los de regreso tienen un costo total lineal.

Un recorrido completo de todos los bits del contador en cada incremento sí podría producir un costo de \(\Theta(m\log m)\), pero ese recorrido adicional no es necesario para implementar el contador binario.

---

## 5. Conclusión

Hemos demostrado que, aunque un incremento individual del contador binario puede costar \(\Theta(\log m)\) en el peor caso, realizar \(m\) incrementos consecutivos desde cero tiene un costo total de:

\[
\boxed{T(m)=\Theta(m)}
\]

El método del potencial demuestra que cada operación tiene un costo amortizado constante:

\[
\boxed{a_i=2}
\]

Por tanto, el costo amortizado por incremento es:

\[
\boxed{O(1)}
\]

Esto no significa que cada operación individual cueste \(O(1)\) en el peor caso, sino que el costo promedio sobre cualquier secuencia de \(m\) incrementos desde cero está acotado por una constante.

**La idea fundamental del análisis amortizado es que las operaciones baratas acumulan crédito para financiar las operaciones costosas posteriores.**