## 1.  Una computadora mil veces más rápida (C1)

Presupuesto actual: $T = 3600 \cdot 10^9 = 3{,}6\cdot 10^{12}$ operaciones. Con la computadora nueva, $1000\,T$.

**$\Theta(n^2)$.** Si $n_0^2 = T$ y $n_1^2 = 1000\,T$, entonces
$$\frac{n_1}{n_0} = \sqrt{1000} \approx 31{,}6.$$
De $n_0 \approx 1{,}9\cdot 10^6$ se pasa a $n_1 \approx 6\cdot 10^7$. El factor no depende de $n_0$.

**$\Theta(n\log n)$.** Ahora $n_1 \log n_1 = 1000\, n_0 \log n_0$, así que
$$\frac{n_1}{n_0} = 1000 \cdot \frac{\log n_0}{\log n_1}.$$
El cociente de logaritmos es casi 1 porque $\log n_1 = \log n_0 + \log(n_1/n_0) \le \log n_0 + \log 1000 \approx \log n_0 + 10$. Con $n_0 \approx 9{,}86\cdot 10^{10}$, $\log n_0 \approx 36{,}5$:

- primera estimación: $1000 \cdot 36{,}5 / 46{,}5 \approx 785$;
- iterando una vez ($n_1 \approx 7{,}7\cdot 10^{13}$, $\log n_1 \approx 46{,}1$): $1000 \cdot 36{,}5/46{,}1 \approx 791$,

que es lo que da la tabla de C1 §7 ($7{,}8\cdot10^{13} / 9{,}86\cdot10^{10} \approx 791$).

**Lectura.** El algoritmo $n\log n$ aprovecha casi todo el factor 1000 (pierde solo el cociente de logaritmos, que tiende a 1 cuando $n$ crece). El cuadrático aprovecha solo su raíz cuadrada.