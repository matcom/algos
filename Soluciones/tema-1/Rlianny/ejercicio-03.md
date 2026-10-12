# Ejercicio 3: Pila con operación `min` en O(1) en el peor caso

## Idea
Llevar dos pilas en paralelo. `stack` es la pila normal del usuario. `stack_min` recibe, en cada `push`, el mínimo de todo lo que hay en `stack` hasta ese momento.

## Estructura
```
stack     = ()
stack_min = ()

push(num):
    stack.push(num)
    if stack_min.isEmpty() or num < stack_min.top:
        stack_min.push(num)
    else:
        stack_min.push(stack_min.top)

pop():            // precondición: stack no vacía
    stack.pop()
    stack_min.pop()

min():            // precondición: stack no vacía
    return stack_min.top
```

## Invariante
Sea n = |stack|. Se cumple siempre:

1. |stack_min| = n.
2. Para todo 1 ≤ i ≤ n (posición 1 = fondo): `stack_min[i] = min(stack[1..i])`, incluyendo el elemento i-ésimo.

## Por qué funciona
Por la naturaleza LIFO, tras un `pop` el estado de la pila es exactamente el que tenía antes del `push` correspondiente. Por eso basta guardar el mínimo en el momento del `push`: nunca hay que recalcularlo en el `pop`.

## Preservación del invariante
- **Inicio:** ambas pilas vacías, n = 0. El invariante se cumple vacuamente.
- **push, pila vacía:** tras el push, n = 1 y `stack_min[1] = num = min(stack[1..1])`. Los tamaños coinciden (1 y 1).
- **push, pila no vacía (n ≥ 1):** el nuevo elemento queda en la posición n+1 de ambas pilas (tamaños iguales). Por hipótesis, `stack_min[n] = min(stack[1..n])`. Se inserta `min(stack_min[n], num)`, que es exactamente `min(min(stack[1..n]), num) = min(stack[1..n+1])`. Las posiciones 1..n no cambian.
- **pop (n ≥ 1):** se elimina la posición n de ambas pilas, así que los tamaños siguen iguales (n-1). Para i ≤ n-1, `stack_min[i]` no cambia y depende solo de `stack[1..i]`, que tampoco cambia. Se cumple el invariante.
- **min (n ≥ 1):** no modifica nada. Por el invariante con i = n, `stack_min[n] = min(stack[1..n])`, que es el mínimo de toda la pila. Es correcta.

## Precondición
`pop` y `min` requieren n ≥ 1. Sobre una pila vacía no están definidas, porque no hay elemento que sacar ni mínimo que devolver. La implementación debe verificarlo o lanzar error.

## Costos (peor caso)
| Operación | Costo | Justificación |
|-----------|-------|---------------|
| `push`    | O(1)  | Dos `push` de pila, un `isEmpty`, un `top` y una comparación. Sin ciclos. |
| `pop`     | O(1)  | Dos `pop` de pila. |
| `min`     | O(1)  | Un `top` de pila. |

Cada operación hace una cantidad constante, independiente de n, de operaciones primitivas O(1) de pila. Esto supone que las primitivas son O(1) en el peor caso (lista enlazada, o arreglo de capacidad fija). Con un arreglo dinámico, `push` sería O(1) amortizado.

**Espacio extra:** O(n), porque `stack_min` tiene tantos elementos como `stack`.

## Variante con conteos (opcional)
`stack_min` guarda tuplas `(x, y)`: `x` es el mínimo y `y` cuántos elementos consecutivos de `stack` (desde el tope hacia abajo) tienen a `x` como mínimo. Las operaciones siguen siendo O(1). El espacio extra es O(1) en el mejor caso (una sola tupla) y O(n) en el peor (una por elemento).