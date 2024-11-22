# Flujo

Red de flujo:
- Grafo dirigido con capacidad $c(u,v) >= 0$ en todas las aristas
- Fuente $(s)$ y sumidero $(t)$
- No existen aristas anti-paralelas (fácil de resolver insertando un nuevo vértice)

Flujo válido:
- Una asignación $f(u,v)$ que cumple que:
  - Respetar la capacidad de las aristas
    $f(u,v) <= c(u,v)$
  - Respetar la conservación de flujo
    $\sum_v f(u,v) = \sum_v f(v,u) \, \forall u \neq s,t$

> (Poner ejemplo)

Problema de flujo máximo: Maximizar el flujo $|f|$ que sale de $s$.

¿Cómo lo resolvemos? Primera intuición, ¡vamos a hacerlo greedy!

> (Hacer en pizarra)

Red residual:
- Grafo $G_f$ dirigido inducido por las aristas con $f(u,v) < c(e,v)$
- Adicionar todas las aristas de retroceso $f(v,u) > 0$

Camino de incremento: Un camino simple en $G_f$ de $s$ a $t$
- Todo camino de incremento implica que existe un flujo mayor posible
- Lema 1: Este flujo sigue siendo válido (¿por qué?)

Ford-Fulkerson:

```python
def ford_fulkerson_(G, find_path):
    f = {}

    while True:
        G_f = make_residual(G) # ¿se puede mantener en O(1)?
        p = find_path(G_f, s, t)

        if not p:
            break

        c[p] = min(c(u,v) for (u,v) in p) # arista crítica

        for (u,v) in p:
            f[u,v] += c(p)

    return f
```

¿Por qué es correcto Ford-Fulkerson?

- Todo flujo obtenido es válido (Lema 1)
- Si para, el flujo obtenido es maximal (trivial, sino, se podría seguir aumentando)
- Además, es máximo (a continuación)

Definición de corte:
- Partición de vértices $S,T$ donde $s \in S, t \in T$.
- Flujo del corte:
  $f(S,T) = \sum_{v\in S}\sum_{u \in T} f(u,v) -  \sum_{v\in S}\sum_{u \in T} f(v,u)$
- Capacidad del corte
  $c(S,T) = \sum_{v\in S}\sum_{u \in T} c(u,v)$

El problema del mínimo corte es encontrar el corte $(S,T)$ que minimiza $c(S,T)$.

Ahora podemos demostrar:
- El flujo en todo corte es el mismo, equivalente a $|f|$ (trabajar con la conservación).
- Por tanto, cualquier flujo en el grafo está limitado por la capacidad de todo corte.
- Por tanto, el flujo máximo del grafo es el flujo del corte mínimo.

🥳🥳🥳

Ahora, ¡eso no significa que Ford-Fulkerson siempre pare!:

Pero si las capacidades son enteras (o racionales, que es equivalente), entonces es fácil ver que tiene que parar (¿por qué?)

¿Qué costo tiene FF?
En cada iteración del ciclo más interno, hay que encontrar un camino: $O(E|f*|)$
Pero en general depende de cómo se escoja el camino de incremento.
El algoritmo es pseudo-polinomial (o débilmente polinomial)

¿Cuál es la mejor forma de escoger el camino?

Edmond-Karp

```python
def bfs(G):
    # ...

def edmond_karp(G):
    return ford_fulkerson(G, bfs)
```

¿Qué costo tiene?

Notar varias cosas:
- Siempre se escoge el camino de incremento de menor longitud de s~t
- La distancia de s~v en sucesivas iteraciones aumenta monotónicamente (prueba por contradicción)
- En todo camino de incremento siempre hay una arista crítica, que se elimina del grafo residual
- Para volver a aparecer en el grafo residual, hay que pasar flujo en el sentido inverso
- Por tanto, entre dos momentos en que la arista $(u,v)$ es crítica, la distancia de s~v en el grafo residual debe aumentar
- Cada arista crítica solo puede volverse crítica una cantidad $O(V)$ de veces

Luego a lo sumo se pueden hacer $O(VE)$ aumentos de flujo.
Por tanto el costo total es $O(VE^2)$.
El algoritmo es fuertemente polinomial.
Y no requiere entonces valores enteros de capacidad.

Un ejemplo de un problema interesante de flujo: Máximo emparejamiento bipartito.

> (Resolver en pizarra)
> (Demostrar reducción)
