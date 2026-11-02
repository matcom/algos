# Problema 1 ★

**Enunciado.** ¿Cuánto crece el tamaño de entrada que se resuelve en una hora con un algoritmo $\Theta(n^2)$? ¿Y con uno $\Theta(n \log n)$? Estima los dos factores.

## Solución formal

Sea $T(n)$ el tiempo de ejecución del algoritmo y $H$ el presupuesto de tiempo (una hora). Para un algoritmo con $T(n) = c\,n^2$, si el presupuesto se multiplica por 1000, el nuevo tamaño $n'$ satisface:

$$
c\,(n')^2 = 1000\,c\,n^2 \quad\Longrightarrow\quad n' = \sqrt{1000}\,n \approx 31.62\,n.
$$

Por tanto, el factor de crecimiento es $\sqrt{1000} \approx 31.6$.

Para un algoritmo con $T(n) = c\,n\log n$, el nuevo tamaño $n'$ satisface:

$$
n'\log n' = 1000\,n\log n.
$$

Para $n$ grande, la solución se aproxima a $n' \approx 1000\,n$, de modo que el factor tiende a 1000. Para valores moderados de $n$, el factor es algo menor; por ejemplo, si $n = 10^6$ y $\log_2 n \approx 20$, entonces $n' \approx 5.7\cdot 10^8$, un factor cercano a 570. A medida que $n$ crece, el factor se acerca asintóticamente a 1000.

**Conclusión.** Con una computadora 1000 veces más rápida, un algoritmo cuadrático resuelve entradas $\sqrt{1000} \approx 31.6$ veces más grandes, mientras que uno $n\log n$ resuelve entradas casi 1000 veces más grandes (con factores menores para $n$ moderado).
