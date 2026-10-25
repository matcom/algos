# Ejercicio 5 — Detección de ciclos: dos punteros (algoritmo de Floyd)

> Dos punteros avanzan a velocidades 1 y 2. Demuestra que se encuentran si y solo si
> hay un ciclo, con un invariante, y que termina, con un potencial. Da el costo.

*(Borrador preparado con asistencia de IA, siguiendo el formato de Agustin y los materiales del Tema 1.)*

## 1. El problema

Una lista enlazada: cada nodo tiene un `siguiente`, que puede ser otro nodo o `None`.
Dos formas posibles:

- **Sin ciclo** ("cola de rana"): termina en `None`.
- **Con ciclo** ("rho", ρ): una cola de $\mu$ nodos ($\mu\ge0$) que entra en un ciclo
  de $\lambda\ge1$ nodos.

Queremos decidir si hay ciclo en $O(n)$ tiempo y $O(1)$ memoria. El algoritmo de Floyd
(la "liebre y la tortuga"): la **tortuga** avanza 1 nodo por paso, la **liebre** 2. Si
hay ciclo, la liebre alcanza a la tortuga dentro de él; si no, la liebre llega a `None`.

```python
def tiene_ciclo(cabeza):
    lenta = rapida = cabeza
    while rapida is not None and rapida.siguiente is not None:
        lenta = lenta.siguiente                 # +1
        rapida = rapida.siguiente.siguiente     # +2
        if lenta is rapida:                     # se encontraron -> hay ciclo
            return True
    return False                                # rapida cayo en None -> sin ciclo
```

## 2. Figura — la forma ρ y el encuentro

```
        cola (μ nodos)                   ciclo (λ nodos)
   cabeza                       entrada
     ●──→●──→●──→●──→●──→●──→●──→ E ──→●──→●──→●
                                  ↑               │
                                  └───────●←──●←──┘
                                      (vuelve a E)

t = tortuga (paso 1),  h = liebre (paso 2)
paso 0:  t=E0  h=E0
...dentro del ciclo la liebre gana 1 posicion por paso sobre la tortuga,
   asi que la distancia (h - t) mod λ baja 1 cada paso hasta llegar a 0 = encuentro.
```

## 3. Terminación — el potencial

**Caso sin ciclo.** La liebre avanza 2 por iteración hacia `None`. El potencial
$\Phi = $ (número de nodos que quedan delante de la liebre hasta `None`) baja al menos
2 por vuelta y es $\ge 0$; en $\le n/2$ vueltas la liebre encuentra `None` y el ciclo
termina devolviendo `False`.

**Caso con ciclo.** Una vez que **ambos** punteros están dentro del ciclo (la tortuga
entra tras $\mu \le n$ pasos), define la **distancia dirigida**
$$\Phi = (\text{pos}(h) - \text{pos}(t)) \bmod \lambda,$$
medida a lo largo del ciclo en el sentido de avance. Cada vuelta la liebre gana una
posición sobre la tortuga ($+2-1=+1$), así que $\Phi$ **baja exactamente 1** módulo
$\lambda$, es decir baja 1 mientras sea $>0$. Es un entero en $\{0,\dots,\lambda-1\}$
que decrece: en $\le \lambda$ vueltas llega a $0$, que es el encuentro. El ciclo
termina devolviendo `True`.

En ambos casos el algoritmo termina en tiempo finito. $\square$

## 4. Correctitud — el invariante (⟺)

Hay que probar: **se encuentran $\iff$ hay ciclo.**

### (⇐) Si hay ciclo, se encuentran

> **Invariante** (una vez los dos punteros están dentro del ciclo): tras cada
> iteración, $\text{dist}(t,h) = (\text{pos}(h)-\text{pos}(t)) \bmod \lambda$ ha
> disminuido en 1 respecto de la iteración anterior.

- **Inicialización.** Cuando la tortuga entra al ciclo (paso $\mu$), la liebre ya está
  dentro (llegó antes, porque va más rápido). Sea $d_0$ la distancia inicial,
  $0 \le d_0 < \lambda$.
- **Mantenimiento.** En una vuelta la tortuga avanza 1 y la liebre 2; la distancia
  dirigida cambia en $(2-1)=1$, es decir $\text{dist} \leftarrow (\text{dist}-1)\bmod
  \lambda$ visto como "cuánto le falta a la liebre para alcanzar a la tortuga". Baja 1.
- **Conclusión.** Tras a lo sumo $\lambda$ vueltas, $\text{dist}=0$: los dos punteros
  ocupan el mismo nodo, `lenta is rapida` es verdadero y el algoritmo devuelve `True`.

La clave de que la liebre **no salte por encima** de la tortuga sin tocarla: la brecha
cambia de a 1 por paso, así que recorre todos los valores $d_0, d_0-1, \dots, 1, 0$ y
necesariamente pasa por $0$. (Si la liebre avanzara de a 3, la brecha bajaría de a 2 y
podría saltarse el 0 cuando $\lambda$ es par — por eso la velocidad 2 es la correcta.)

### (⇒) Si se encuentran, hay ciclo

> **Invariante** (siempre): si en algún momento `lenta is rapida` con ambos no nulos,
> entonces esa dirección se recorrió por dos caminos de longitudes distintas que
> terminan en el mismo nodo.

En una lista **sin** ciclo todos los nodos son distintos (cada `siguiente` lleva a un
nodo nuevo o a `None`), y la liebre, que va estrictamente por delante de la tortuga
(más pasos recorridos), nunca puede ocupar el mismo nodo que ella salvo en el inicio
antes de moverse. Como el algoritmo compara **después** de mover, un encuentro
`lenta is rapida` implica que un nodo es alcanzable por dos conteos de pasos distintos
($t$ pasos y $2t$ pasos con $t\ge1$), lo cual solo ocurre si algún `siguiente` vuelve
a un nodo ya visitado: eso **es** un ciclo. $\square$

Combinando (⇐) y (⇒): **se encuentran $\iff$ hay ciclo.**

## 5. Costo

| recurso | caso sin ciclo | caso con ciclo |
|---|---|---|
| tiempo | $\le n/2$ vueltas, $O(n)$ | $\mu + \lambda \le n$ vueltas, $O(n)$ |
| memoria extra | dos punteros, $O(1)$ | dos punteros, $O(1)$ |

En el caso con ciclo: la tortuga tarda $\mu$ pasos en entrar, y luego a lo sumo
$\lambda$ pasos más para el encuentro; $\mu+\lambda \le n$, así que **$O(n)$ tiempo,
$O(1)$ memoria**. Es la gran ventaja sobre marcar nodos visitados en una tabla hash,
que costaría $O(n)$ memoria.

## 6. Comprobación — contra un oráculo con conjunto visitado

```python
class Nodo:
    def __init__(self, v): self.v, self.siguiente = v, None

def construir(n, mu, lam):
    """Lista de n nodos; si lam>0, los ultimos lam forman un ciclo tras mu de cola."""
    nodos = [Nodo(i) for i in range(n)]
    for i in range(n - 1):
        nodos[i].siguiente = nodos[i + 1]
    if lam > 0:                                  # cerrar ciclo: ultimo -> nodo[mu]
        nodos[-1].siguiente = nodos[mu]
    return nodos[0]

def tiene_ciclo(cabeza):
    lenta = rapida = cabeza
    while rapida is not None and rapida.siguiente is not None:
        lenta = lenta.siguiente
        rapida = rapida.siguiente.siguiente
        if lenta is rapida:
            return True
    return False

def oraculo(cabeza):                             # O(n) memoria: conjunto de visitados
    vistos, x = set(), cabeza
    while x is not None:
        if id(x) in vistos: return True
        vistos.add(id(x)); x = x.siguiente
    return False

import random
random.seed(0)
casos = 0
for _ in range(5000):
    n = random.randint(1, 40)
    con_ciclo = random.random() < 0.5
    mu = random.randint(0, n - 1)
    lam = random.randint(1, n - mu) if con_ciclo else 0
    cabeza = construir(n, mu, lam)
    assert tiene_ciclo(cabeza) == oraculo(cabeza)
    casos += 1
print(f"{casos} listas aleatorias: Floyd coincide con el oraculo en todas")
```

**Salida:**

```
5000 listas aleatorias: Floyd coincide con el oraculo en todas
```

## 7. Resumen

- **Terminación (potencial):** sin ciclo, los nodos ante la liebre bajan $\ge2$ por
  vuelta; con ciclo, la brecha dirigida $(\text{h}-\text{t})\bmod\lambda$ baja 1 por
  vuelta.
- **Correctitud (⟺):** con ciclo la brecha llega a 0 (encuentro); sin ciclo la liebre
  cae en `None` y un encuentro sería imposible sin un nodo repetido.
- **Costo:** $O(n)$ tiempo, $O(1)$ memoria — mejor que marcar visitados.
