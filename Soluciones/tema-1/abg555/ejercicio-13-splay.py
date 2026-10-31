import math


class Node:
    def __init__(self, key):
        self.key, self.left, self.right, self.parent = key, None, None, None


def rotate(x):
    # Sube x un nivel rotando la arista con su padre. Preserva el orden.
    p, g = x.parent, x.parent.parent
    if p.left is x:
        p.left, x.right = x.right, p
        if p.left:
            p.left.parent = p
    else:
        p.right, x.left = x.left, p
        if p.right:
            p.right.parent = p
    p.parent, x.parent = x, g
    if g:
        if g.left is p:
            g.left = x
        else:
            g.right = x


def splay(x):
    # Sube x a la raiz con pasos zig, zig-zig y zig-zag. Devuelve las rotaciones.
    rotations = 0
    while x.parent:
        p, g = x.parent, x.parent.parent
        if g is None:                                  # zig
            rotate(x)
            rotations += 1
        elif (g.left is p) == (p.left is x):           # zig-zig: primero el padre
            rotate(p)
            rotate(x)
            rotations += 2
        else:                                          # zig-zag
            rotate(x)
            rotate(x)
            rotations += 2
    return rotations


def move_to_root(x):
    # Subir a la raiz con rotaciones simples (Allen y Munro).
    rotations = 0
    while x.parent:
        rotate(x)
        rotations += 1
    return rotations


def find(root, key):
    x = root
    while x.key != key:
        x = x.left if key < x.key else x.right
    return x


def path(n):
    # El arbol inicial: n en la raiz, cada clave hija izquierda de la siguiente.
    nodes = [Node(k) for k in range(1, n + 1)]
    for k in range(1, n):
        nodes[k].left, nodes[k - 1].parent = nodes[k - 1], nodes[k]
    return nodes[-1]


def subtree_sizes(root):
    # Tamano del subarbol de cada nodo, sin recursion (el arbol puede ser un camino largo).
    order, stack = [], [root]
    while stack:
        x = stack.pop()
        order.append(x)
        for c in (x.left, x.right):
            if c:
                stack.append(c)
    size = {}
    for x in reversed(order):
        size[x] = 1 + (size[x.left] if x.left else 0) + (size[x.right] if x.right else 0)
    return size


def potential(root):
    # Phi = suma de log2(tamano del subarbol) sobre todos los nodos.
    return sum(math.log2(s) for s in subtree_sizes(root).values())


def is_bst(root):
    keys, stack, x = [], [], root
    while stack or x:
        while x:
            stack.append(x)
            x = x.left
        x = stack.pop()
        keys.append(x.key)
        x = x.right
    return keys == sorted(keys)


def access_sequence(n, keys, reorganize=splay, watch=None):
    # Accede a las claves en el orden dado, empezando desde un camino de n nodos.
    # Devuelve el costo de cada acceso (rotaciones, o 1 si ya es la raiz).
    # Si se pasa una lista en watch, guarda (costo, Phi antes, Phi despues, rango de x antes).
    root, costs = path(n), []
    for k in keys:
        x = find(root, k)
        if watch is not None:
            size = subtree_sizes(root)
            phi_before, r_x = sum(math.log2(s) for s in size.values()), math.log2(size[x])
        c = max(reorganize(x), 1)
        root = x
        if watch is not None:
            watch.append((c, phi_before, potential(root), r_x))
        costs.append(c)
    return costs
