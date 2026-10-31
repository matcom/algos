# Ejercicio 5 ★★ — Detección de ciclos de Floyd (C3)

> Detección de ciclos en una lista enlazada con dos punteros que avanzan a velocidades 1 y 2 (algoritmo de Floyd). Demuestra que se encuentran si y solo si hay un ciclo, con un invariante, y que termina, con un potencial. Da el costo.

## Problema y notación

Una lista enlazada empieza en `cabeza`; cada nodo tiene un campo `sig` (siguiente o `None`). Llamamos $x_0=\text{cabeza}$, $x_{i+1}=x_i.\text{sig}$. Hay dos posibilidades:

- **Sin ciclo:** $x_0,\dots,x_{L-1}$ son nodos distintos y $x_{L-1}.\text{sig}=\text{None}$ ($L\ge0$ nodos).
- **Con ciclo:** hay una cola de $\mu\ge0$ nodos $x_0..x_{\mu-1}$ y un ciclo de $\lambda\ge1$ nodos $x_\mu..x_{\mu+\lambda-1}$, con $x_{\mu+\lambda}=x_\mu$. En general, $x_i=x_j$ con $i,j\ge\mu$ si y solo si $i\equiv j \pmod\lambda$. Hay $n=\mu+\lambda$ nodos.

**Hecho básico.** Si $x_i=x_j$ para algún $i<j$, la lista tiene ciclo: desde ahí la sucesión se repite para siempre y nunca llega a `None`. Por tanto, en una lista sin ciclo todas las posiciones son nodos distintos.

## Algoritmo

La función `floyd(cabeza)` avanza dos punteros desde la cabeza: la tortuga un nodo por vuelta y la liebre dos. Si la liebre llega a `None`, la lista no tiene ciclo; si los dos punteros caen en el mismo nodo, lo tiene. Devuelve si hay ciclo y cuántas vueltas dio, para comprobar esa cuenta en las pruebas.

> Código: [ejercicio-05.py](ejercicio-05.py), parte 1.

## Invariante

Antes de cada evaluación de la condición del ciclo, después de $k$ vueltas completas:

$$I(k):\quad \text{tortuga}=x_k,\quad \text{liebre}=x_{2k},\quad x_j\neq x_{2j}\ \text{ para } 1\le j\le k .$$

- **Inicialización** ($k=0$): las dos variables son $x_0$, y la tercera parte habla de un conjunto vacío.
- **Mantenimiento.** Si se entra al ciclo, la condición garantiza que $x_{2k}$ y $x_{2k+1}$ son nodos (no `None`), así que $x_{2k+2}=x_{2k+1}.\text{sig}$ está definido (es un nodo o `None`). También $x_{k+1}$ es un nodo, porque $k+1\le 2k+1$. Después de la vuelta, `tortuga` $=x_{k+1}$ y `liebre` $=x_{2k+2}$. Si son el mismo nodo, se devuelve. Si no, $x_{k+1}\ne x_{2(k+1)}$ y vale $I(k+1)$. (Si $x_{2k+2}$ es `None`, la comparación con la tortuga da distinto y en la siguiente evaluación el ciclo termina.)
- **Conclusión.**
  - Si devuelve `True` en la vuelta $k\ge1$: $x_k=x_{2k}$ con $k<2k$, así que **hay ciclo** (hecho básico).
  - Si devuelve `False`: el ciclo terminó porque `liebre` o `liebre.sig` es `None`, así que la lista llega a `None` y **no hay ciclo**.

Esto es la correctitud parcial: "si responde, responde bien". En particular, **sin ciclo nunca se encuentran**.

## Terminación (potenciales)

**Sin ciclo** (lista de $L$ nodos): $\Phi=L-2k$. Mientras el ciclo sigue, $x_{2k+1}$ existe, o sea $2k+1\le L-1$, y $\Phi\ge2$. Cada vuelta baja $\Phi$ en 2, así que termina. Número exacto de vueltas: $\lfloor L/2\rfloor$.

**Con ciclo:** la lista nunca llega a `None`, así que la única forma de salir es encontrarse. Hay que demostrar que eso pasa. Lo hacemos en dos fases, cada una con su potencial.

1. **Fase 1** (la tortuga todavía no entra al ciclo, $k<\mu$): $\Phi_1=\mu-k$. Baja en 1 por vuelta y es $\ge1$ en esta fase. Dura a lo sumo $\mu$ vueltas.
2. **Fase 2** ($k\ge\mu$, las dos dentro del ciclo): $\Phi_2=d_k$ = número de pasos que la liebre tiene que dar **hacia adelante en el ciclo** para llegar a la tortuga. Como la liebre está en la posición $2k$ y la tortuga en la $k$, $d_k=(k-2k)\bmod\lambda=(-k)\bmod\lambda\in\{0,\dots,\lambda-1\}$. En cada vuelta la tortuga avanza 1 y la liebre 2: **la distancia baja exactamente en 1**. Cuando llega a 0 están en el mismo nodo y el algoritmo devuelve `True`. La fase 2 dura a lo sumo $\lambda$ vueltas (una más que $\lambda-1$ solo si $\mu=0$, porque en $k=0$ no se comprueba).

Por lo tanto, **con ciclo se encuentran**, después de a lo sumo $\mu+\lambda=n$ vueltas. Concretamente, en la primera $k\ge\max(\mu,1)$ que es múltiplo de $\lambda$, porque $x_k=x_{2k}$ si y solo si $k\ge\mu$ y $\lambda\mid k$.

**Juntando:** se encuentran $\iff$ hay ciclo.

## Costo

| caso | vueltas | punteros seguidos |
|---|---|---|
| sin ciclo, $L$ nodos | $\lfloor L/2\rfloor$ | $\le 3\lfloor L/2\rfloor$ |
| con ciclo, $n=\mu+\lambda$ nodos | primer múltiplo de $\lambda$ que es $\ge\max(\mu,1)$; $\le n$ | $\le 3n$ |

Tiempo $O(n)$ y memoria $O(1)$: dos punteros y un contador. No hace falta marcar nodos ni guardar un conjunto de visitados (eso costaría $O(n)$ de memoria).

## Casos de prueba y validación

Herramientas de prueba: `lista(mu, lam)` construye una lista con una cola de $\mu$ nodos seguida de un ciclo de $\lambda$ nodos ($\lambda=0$ es una lista sin ciclo); `oraculo` detecta el ciclo guardando los nodos visitados en un conjunto, y `vueltas_esperadas` da cuántas vueltas debería hacer Floyd según la fórmula. Esta parte no imprime nada.

> Código: [ejercicio-05.py](ejercicio-05.py), parte 2.

Casos de borde a mano:

> Código: [ejercicio-05.py](ejercicio-05.py), parte 3.

```text
lista vacía                        ciclo=False vueltas=0
un nodo, sin ciclo                 ciclo=False vueltas=0
un nodo que se apunta a sí mismo   ciclo=True  vueltas=1
dos nodos en ciclo                 ciclo=True  vueltas=2
cola 1 + ciclo 1                   ciclo=True  vueltas=1
cola 5 + ciclo 3                   ciclo=True  vueltas=6
10 nodos sin ciclo                 ciclo=False vueltas=5
```

Prueba exhaustiva sobre todas las formas con $\mu,\lambda\le 40$, contra el oráculo y contra la fórmula de vueltas:

> Código: [ejercicio-05.py](ejercicio-05.py), parte 4.

```text
1681 formas de lista: respuesta correcta, vueltas exactas y siempre <= n
```

Invariante y potencial vigilados (fase 2: la distancia baja exactamente en 1 por vuelta):

> Código: [ejercicio-05.py](ejercicio-05.py), parte 5.

```text
invariante y potencial de la fase 2 comprobados en 600 listas con ciclo
```

**Extra: encontrar dónde empieza el ciclo y su largo.** Cuando se encuentran en la vuelta $k$, $\lambda\mid k$. Si un puntero vuelve a la cabeza y los dos avanzan de a 1, después de $j$ pasos están en $x_j$ y $x_{k+j}$, que coinciden por primera vez en $j=\mu$.

> Código: [ejercicio-05.py](ejercicio-05.py), parte 6.

```text
mu y lambda recuperados correctamente en 870 listas
```

## Resumen

- **Invariante:** tortuga $=x_k$, liebre $=x_{2k}$, y no se encontraron antes. Si se encuentran, $x_k=x_{2k}$ ⇒ ciclo. Si la liebre llega a `None` ⇒ no hay ciclo.
- **Potenciales:** sin ciclo, $L-2k$; con ciclo, $\mu-k$ y después la distancia en el ciclo $(-k)\bmod\lambda$, que baja exactamente 1 por vuelta.
- **Costo:** $\le n$ vueltas (3 punteros por vuelta), $O(n)$ tiempo, $O(1)$ memoria.
