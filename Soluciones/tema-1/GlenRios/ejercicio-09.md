# Problema 9 ★★

**Enunciado.** Una mezcla "optimizada" de dos listas ordenadas de largo $n$ deja de comparar cuando a la primera lista le queda un solo elemento, y lo pone al final. Cuenta cuántas comparaciones hace en el peor caso. Sin probarla, usa la sección 6 de la conferencia 5 para decidir si es correcta, y construye con el adversario la entrada en la que falla.

## Solución formal

**Algoritmo.** Sean $A$ y $B$ dos listas ordenadas de largo $n$. La mezcla estándar usa un bucle `while i < n and j < n`, saca el menor de $A[i]$ y $B[j]$ en cada paso, y cuando una lista se agota copia el resto de la otra sin comparar. Su peor caso es $2n-1$ comparaciones.

La mezcla **optimizada** cambia la condición del bucle a `while i < n-1 and j < n`. Es decir, para cuando a $A$ le queda un solo elemento ($i = n-1$), y en ese momento lo coloca al final de la salida, después de copiar los elementos restantes de $B$.

**Conteo de comparaciones en el peor caso.** El bucle puede terminar de dos maneras.

*Caso 1: termina porque $i = n-1$ (a $A$ le queda un elemento).* Se han sacado $n-1$ elementos de $A$ y $j$ elementos de $B$, con $0 \le j \le n-1$. Cada iteración hace una comparación, así que el número total es $(n-1) + j$. El máximo se alcanza con $j = n-1$:
$$
(n-1) + (n-1) = 2n - 2.
$$

*Caso 2: termina porque $j = n$ (B agotada).* Se han sacado los $n$ elementos de $B$ y $i$ elementos de $A$. Pero como el bucle sigue mientras $i < n-1$, en el momento en que se agota $B$ se tiene $i \le n-2$. El número de comparaciones es $n + i$, y el máximo se alcanza con $i = n-2$:
$$
n + (n-2) = 2n - 2.
$$

**Peor caso global.**
$$
\max(2n-2,\ 2n-2) = 2n - 2.
$$
Por tanto, la mezcla optimizada hace a lo sumo $2n-2$ comparaciones, **una menos** que la mezcla estándar y que la cota mínima de $2n-1$.

**¿Es correcta?** **No.** El caso 1 es problemático. Cuando el bucle sale porque a $A$ le queda un elemento, $B$ todavía puede tener elementos sin sacar. La optimización los copia y luego coloca $A[n-1]$ al final **sin compararlo** con ellos. Esto es incorrecto si $A[n-1]$ es menor que alguno de esos elementos, porque entonces $A[n-1]$ debería ir antes.

**Ejemplo mínimo ($n=2$).** $A = [1, 2]$, $B = [3, 4]$.
- Mezcla estándar: compara $1$ vs $3$ → sale $1$; compara $2$ vs $3$ → sale $2$; copia $3, 4$. Resultado: $1, 2, 3, 4$. Correcto.
- Mezcla optimizada: una comparación ($1$ vs $3$, sale $1$). Ahora $i = 1 = n-1$, el bucle termina. Copia $B = [3, 4]$ y pone $2$ al final. Resultado: $1, 3, 4, 2$. **Incorrecto.**

**La cota mínima y la entrada del adversario.** La sección 6 de la Conferencia 5 demuestra que mezclar dos listas ordenadas de largo $n$ requiere $\Omega(2n-1)$ comparaciones en el peor caso. El adversario responde como si la entrada fuera la **intercalada perfecta**:
$$
a_0 < b_0 < a_1 < b_1 < \cdots < a_{n-1} < b_{n-1}.
$$
En esa entrada, la mezcla optimizada hace exactamente $2n-2$ comparaciones: se alternan los elementos hasta que le quedan $a_{n-1}$ y $b_{n-1}$, el bucle termina, copia $b_{n-1}$ y pone $a_{n-1}$ al final. Pero $a_{n-1} < b_{n-1}$, así que el orden queda mal.

**Conclusión.** La mezcla optimizada es incorrecta. Su peor caso es $2n-2$ comparaciones, **una menos que la cota mínima de $2n-1$**, lo cual ya es señal suficiente de que está mal. La cota mínima revela el error sin necesidad de probar el algoritmo, y la entrada del adversario (la intercalada perfecta) es exactamente donde falla.