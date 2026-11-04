## 4.  El contador binario en máquina de Turing (C1, C4)

**La máquina** (ejercicio 7 de C1). La cinta contiene un marcador $\triangleright$, y a su derecha el número con el bit menos significativo primero; a la derecha del último bit hay blancos. El cabezal empieza sobre el bit menos significativo.

| estado | lee | escribe | mueve | pasa a |
|---|---|---|---|---|
| $q_{\text{inc}}$ | 1 | 0 | → | $q_{\text{inc}}$ |
| $q_{\text{inc}}$ | 0 o ␣ | 1 | ← | $q_{\text{vuelta}}$ |
| $q_{\text{vuelta}}$ | 0 o 1 | (igual) | ← | $q_{\text{vuelta}}$ |
| $q_{\text{vuelta}}$ | $\triangleright$ | $\triangleright$ | → | $q_{\text{fin}}$ |

Si el número termina en $t$ unos, el incremento da $t$ pasos de acarreo, 1 paso escribiendo el 1, $t$ pasos de vuelta sobre los ceros recién escritos, y 1 paso para bajar del marcador. **Costo real: $c = 2t + 2$.** Para ir de $2^k - 1$ a $2^k$, $t = k$, así que un incremento suelto cuesta $\Theta(\log m)$ cuando el valor es del orden de $m$. Esa es la pregunta que C1 dejó abierta: sumando ingenuamente, $m$ incrementos costarían $O(m\log m)$.

**Potencial.** $\Phi = 2\cdot(\text{número de unos en la cinta})$.

- Empieza en $\Phi_0 = 0$ (el contador vale 0) y nunca es negativo.
- Un incremento con $t$ unos finales convierte $t$ unos en ceros y un 0 (o blanco) en 1: $\Delta\Phi = 2(1 - t)$.
- Costo amortizado: $\hat c = (2t+2) + 2(1-t) = 4$.

Por el telescopio de C4 §2, $\sum c_i = \sum \hat c_i - (\Phi_m - \Phi_0) \le 4m$. **Los $m$ incrementos cuestan $O(m)$ pasos.**

Qué deuda mide el potencial (C4 §3): cada 1 en la cinta es un acarreo futuro, y en la máquina de Turing cada acarreo cuesta *dos* pasos (ir y volver), por eso el factor 2. De hecho la cuenta es exacta: el total es $4m - 2\cdot\mathrm{popcount}(m)$ (por ejemplo, 36 pasos para $m = 10$; una simulación da 399 988 para $m = 10^5$).

Fíjate en qué cambió respecto al contador de C4 en el modelo RAM: la vuelta del cabezal duplica el costo de cada acarreo, pero es proporcional al acarreo, así que solo cambia la constante, no el orden.

---