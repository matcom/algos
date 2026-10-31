import math
import random


def closest_pair_sort(xs):
    # Ordenar y mirar los vecinos (conferencia 2, seccion 3). O(n log n) comparaciones.
    s = sorted(xs)
    return min(b - a for a, b in zip(s, s[1:]))


def closest_pair_grid(xs, seed=0, shuffle=True, stats=None, trace=None):
    # El algoritmo incremental aleatorio de la conferencia 2 (seccion 9), en una dimension.
    # Rejilla de celdas de largo delta/2 guardada en un diccionario (tabla hash).
    # stats cuenta reconstrucciones, celdas consultadas y puntos reinsertados; trace guarda cada insercion.
    pts = list(xs)
    if shuffle:
        random.Random(seed).shuffle(pts)
    if stats is not None:
        stats.update(rebuilds=0, lookups=0, rebuilt_points=0)
    delta = abs(pts[0] - pts[1])
    if delta == 0:
        return 0
    side = delta / 2
    cell = lambda p: math.floor(p / side)         # la parte entera: lo que el modelo algebraico no tiene
    grid = {cell(p): p for p in pts[:2]}
    for i in range(2, len(pts)):
        p = pts[i]
        before, c = delta, cell(p)
        for dc in (-2, -1, 0, 1, 2):              # el bloque de 5 celdas
            if stats is not None:
                stats["lookups"] += 1
            q = grid.get(c + dc)
            if q is not None and abs(p - q) < delta:
                delta = abs(p - q)
        if delta == 0:                            # un repetido: la respuesta es 0
            return 0
        if delta < before:                        # delta bajo: reconstruir la rejilla
            side = delta / 2
            grid = {cell(q): q for q in pts[:i + 1]}
            if stats is not None:
                stats["rebuilds"] += 1
                stats["rebuilt_points"] += i + 1
        else:
            grid[c] = p
        if trace is not None:
            trace.append((p, delta, delta < before, dict(grid)))
    return delta


def has_duplicates(xs):
    # Distincion de elementos resuelta con el par mas cercano: hay repetidos si y solo si la
    # distancia minima es 0. Es la reduccion de la conferencia 2 (seccion 8).
    return closest_pair_grid(xs) == 0
