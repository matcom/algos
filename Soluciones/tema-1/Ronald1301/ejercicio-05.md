# Ejercicio 5 — Detección de ciclos: dos punteros (algoritmo de Floyd)

**Uso de IA:** Se usó IA para preparar y revisar este borrador, generar código y casos
de prueba, y apoyar la depuración. Parte de la explicación matemática también recibió
asistencia de IA; esas partes todavía no son redacción propia. Antes de entregar,
reescribiré y verificaré por mi cuenta las demostraciones, análisis de costo y cotas,
según la regla del curso.


> Dos punteros avanzan a velocidades 1 y 2. Demuestra que se encuentran si y solo si
> hay un ciclo, con un invariante, y que termina, con un potencial. Da el costo.


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

## 2. Figura — cola y ciclo

~~~
  cabeza                         entrada E
    ● ──→ ● ──→ ● ──→ ● ──→ ● ──→ ● ──→ ● ──→ ●
                                  ↑                │
                                  └────── ← ● ← ● ←┘
  |<------ μ aristas ------>|   |<--- λ aristas --->|

Después de s iteraciones desde cabeza:
  tortuga: posición s
  liebre:  posición 2s
~~~

La notación de posiciones es sobre el recorrido desde la cabeza; dentro del ciclo se
toman módulo $\lambda$. Tras entrar ambos al ciclo, la liebre gana una posición por
iteración.
## 3. Terminación — guía para redactar el argumento (pendiente)

La prueba de terminación debes escribirla tú. Analiza por separado estas fases:

- **Sin ciclo:** define un potencial con el número de nodos que le faltan a la liebre
  para salir por None. ¿Cuánto baja por iteración completa?
- **Con ciclo:** antes de que ambos punteros entren, acota esa fase por la longitud de
  la cola $\mu$. Después define la distancia dirigida desde la liebre hasta la tortuga
  dentro del ciclo, con valores entre $0$ y $\lambda-1$. ¿Cómo cambia en una vuelta?
- Relaciona llegar a potencial cero con la condición de salida del algoritmo.
## 4. Correctitud — guía para redactar la prueba (pendiente)

La prueba debes escribirla tú. Completa por separado las dos direcciones:

- **Si hay ciclo:** sea $s$ un paso posterior a la entrada de la tortuga. ¿Qué posiciones
  del ciclo ocupan los dos punteros tras $s$ pasos? ¿Cómo cambia su distancia dirigida
  módulo $\lambda$ en cada iteración? ¿Qué implica cuando esa distancia llega a cero?
- **Si se encuentran:** en una lista sin ciclo, todos los nodos de la trayectoria son
  distintos. Después de $t\ge1$ iteraciones, ¿qué posiciones de esa trayectoria ocupan
  los punteros? Explica por qué no pueden ser el mismo nodo.
- El código compara **después** de mover los punteros. Relaciona ese detalle con
  $t\ge1$.

No llames “invariante” a la observación de posiciones distintas en el caso sin ciclo;
es un argumento directo sobre la trayectoria.
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

def construir(mu, lam=None):
    """Crea una cola de mu nodos o una estructura rho de cola mu y ciclo lam."""
    cantidad = mu if lam is None else mu + lam
    if cantidad == 0:
        return None
    nodos = [Nodo(i) for i in range(cantidad)]
    for i in range(cantidad - 1):
        nodos[i].siguiente = nodos[i + 1]
    if lam is not None:
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
    cabeza = construir(mu, lam) if con_ciclo else construir(n)
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
