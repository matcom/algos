# Problema 8 ★★

**Enunciado.** El elemento que aparece más de $n/3$ veces. Generaliza Boyer-Moore con dos candidatos, enuncia el invariante reforzado y demuéstralo. Después escribe la versión que devuelve los candidatos con contador positivo sin verificarlos, y busca un generador de pruebas que no la atrape. Cuidado: el análogo del generador binario de la conferencia 3 sí la atrapa.

## Solución formal

**Algoritmo (generalización de Boyer-Moore).** Mantener dos candidatos $c_1, c_2$ y dos contadores $k_1, k_2$, inicialmente $0$. Para cada elemento $x$ del arreglo:
- Si $x = c_1$, incrementar $k_1$.
- Si $x = c_2$, incrementar $k_2$.
- Si $k_1 = 0$, hacer $c_1 = x$, $k_1 = 1$.
- Si $k_2 = 0$, hacer $c_2 = x$, $k_2 = 1$.
- En otro caso, decrementar $k_1$ y $k_2$.

Al final, los candidatos son $c_1$ y $c_2$. Luego se verifica cada uno contando sus ocurrencias.

**Invariante reforzado.** Después de procesar un prefijo del arreglo, el multiconjunto de elementos se puede particionar en:
- un conjunto de tripletas de elementos distintos entre sí,
- $k_1$ copias de $c_1$,
- $k_2$ copias de $c_2$.

*Demostración por inducción.*
- *Inicialización:* prefijo vacío, $k_1=k_2=0$, trivial.
- *Mantenimiento:* Supongamos el invariante para el prefijo $P$. Procesamos $x$.
  - Si $x = c_1$, añadimos $x$ a las copias de $c_1$: $k_1$ aumenta en 1.
  - Si $x = c_2$, análogamente.
  - Si $k_1 = 0$, hacemos $c_1 = x$ y $k_1 = 1$. Las copias anteriores de $c_1$ eran 0, así que solo añadimos una copia de $x$.
  - Si $k_2 = 0$, análogamente.
  - En otro caso, $x$ es distinto de $c_1$ y $c_2$, y $k_1, k_2 > 0$. Formamos una tripleta $(x, c_1, c_2)$ con una copia de cada uno, y la quitamos. Quedan $k_1-1$ copias de $c_1$ y $k_2-1$ de $c_2$.
  En todos los casos, el invariante se mantiene.

**Consecuencia.** Si un elemento $m$ aparece más de $n/3$ veces, entonces $m$ debe ser uno de los candidatos. En efecto, si $m$ no es candidato, solo puede aparecer en las tripletas, y cada tripleta contiene a lo sumo una copia de $m$. Sea $T$ el número de tripletas. Entonces $n = 3T + k_1 + k_2 \ge 3T$, así que $T \le n/3$. Por tanto, $m \le T \le n/3$, contradicción. Así, $m \in \{c_1, c_2\}$.

**Versión sin verificación (incorrecta).** Después de una pasada, devolver todos los candidatos con contador positivo, sin verificar sus frecuencias. Esto puede devolver elementos que no superan $n/3$.

**Generador de pruebas que no la atrapa.** Para que la versión incorrecta pase todas las pruebas, necesitamos generar entradas donde todo candidato con contador positivo realmente aparezca más de $n/3$ veces. Una forma es construir arreglos con exactamente un elemento $m$ que aparece $> n/3$ veces, y el resto de elementos aparecen en pares de elementos distintos que se cancelan entre sí. Por ejemplo, para $n$ impar, tomar $m$ repetido $k$ veces con $k > n/3$, y luego una secuencia de pares $(a,b)$ con $a \neq b$, $a,b \neq m$, ordenados de forma que cada $a$ sea seguido por un $b$ para que se decrementen mutuamente. Así, al final solo $m$ tendrá contador positivo. Este generador no produce casos donde un elemento con contador positivo tenga frecuencia $\le n/3$, por lo que la versión incorrecta acierta siempre. El generador binario (solo dos símbolos) sí atrapa el error, porque puede producir frecuencias exactamente $n/3$ o elementos con contador positivo pero frecuencia baja.

**Conclusión.** El algoritmo con dos candidatos y verificación final es correcto y encuentra todos los elementos que aparecen más de $n/3$ veces. La versión sin verificación es incorrecta, pero puede pasar desapercibida si las pruebas se generan de forma que eviten los casos conflictivos.