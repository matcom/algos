import random
from pathlib import Path
import matplotlib.pyplot as plt


class _Celda:
    __slots__ = ("valor", "minimo", "abajo")

    def __init__(self, valor, minimo, abajo):
        self.valor = valor
        self.minimo = minimo
        self.abajo = abajo


class PilaMin:
    """
    Pila enlazada donde cada celda almacena (valor, minimo_hasta_el_fondo).
    Garantiza O(1) en el peor caso para todas las operaciones.
    """

    def __init__(self):
        self.tope = None

    def vacia(self):
        return self.tope is None

    def apilar(self, x):
        m = x if (self.tope is None or x < self.tope.minimo) else self.tope.minimo
        self.tope = _Celda(x, m, self.tope)

    def desapilar(self):
        celda = self.tope
        self.tope = celda.abajo
        return celda.valor

    def cima(self):
        return self.tope.valor

    def minimo(self):
        return self.tope.minimo

    def como_lista_desde_fondo(self):
        pares = []
        actual = self.tope
        while actual is not None:
            pares.append((actual.valor, actual.minimo))
            actual = actual.abajo
        pares.reverse()
        return pares


class PilaMinDosPilas:
    """
    Variante con dos pilas (datos y minimos).
    Si estricto=False usa '<=' (correcta); si estricto=True usa '<' (defectuosa).
    """

    def __init__(self, estricto=False):
        self.datos = []
        self.minimos = []
        self.estricto = estricto

    def vacia(self):
        return not self.datos

    def apilar(self, x):
        self.datos.append(x)
        if not self.minimos:
            self.minimos.append(x)
        elif self.estricto and x < self.minimos[-1]:
            self.minimos.append(x)
        elif not self.estricto and x <= self.minimos[-1]:
            self.minimos.append(x)

    def desapilar(self):
        x = self.datos.pop()
        if self.minimos and x == self.minimos[-1]:
            self.minimos.pop()
        return x

    def cima(self):
        return self.datos[-1]

    def minimo(self):
        return self.minimos[-1] if self.minimos else None


def vigilar_invariante(semilla=1337, operaciones=4000):
    rng = random.Random(semilla)
    p = PilaMin()
    for _ in range(operaciones):
        if rng.random() < 0.55 or p.vacia():
            p.apilar(rng.randrange(40))
        else:
            p.desapilar()
        pares = p.como_lista_desde_fondo()
        for i in range(len(pares)):
            valores_prefijo = [pares[j][0] for j in range(i + 1)]
            assert pares[i][1] == min(valores_prefijo)


def primer_fallo(fabrica, max_ops, tam_universo, semilla):
    rng = random.Random(semilla)
    p = fabrica()
    espejo = []
    for k in range(1, max_ops + 1):
        if rng.random() < 0.52 or not espejo:
            x = rng.randrange(tam_universo)
            p.apilar(x)
            espejo.append(x)
        else:
            if p.desapilar() != espejo.pop():
                return k
        if espejo and p.minimo() != min(espejo):
            return k
    return None


if __name__ == "__main__":
    # 1. Traza paso a paso con minimos repetidos
    secuencia = [
        ("apilar", 5),
        ("apilar", 3),
        ("apilar", 7),
        ("apilar", 3),
        ("desapilar", None),
        ("desapilar", None),
        ("desapilar", None),
    ]
    p_pares = PilaMin()
    p_le = PilaMinDosPilas(estricto=False)
    p_lt = PilaMinDosPilas(estricto=True)

    print("=== Traza paso a paso con minimos repetidos ===")
    for idx, (op, val) in enumerate(secuencia, 1):
        if op == "apilar":
            p_pares.apilar(val)
            p_le.apilar(val)
            p_lt.apilar(val)
            desc = f"apilar({val})"
        else:
            v = p_pares.desapilar()
            p_le.desapilar()
            p_lt.desapilar()
            desc = f"desapilar() -> {v}"
        print(f"Paso {idx} ({desc:<16}): pares={p_pares.como_lista_desde_fondo()} | "
              f"min_le={p_le.minimos} (min={p_le.minimo()}) | "
              f"min_lt={p_lt.minimos} (min={p_lt.minimo()})")
    print()

    # 2. Verificacion del invariante estructural
    vigilar_invariante(semilla=1337, operaciones=4000)
    print("Invariante estructural comprobado celda por celda en 4000 operaciones: 0 fallos.\n")

    # 3. Comparacion de primera operacion con fallo segun el universo de valores
    variantes = [
        ("Pila enlazada de pares", PilaMin),
        ("Dos pilas con <=", lambda: PilaMinDosPilas(estricto=False)),
        ("Dos pilas con < (error)", lambda: PilaMinDosPilas(estricto=True)),
    ]
    print("=== Primera operacion con fallo en 25 000 pasos (--- si no falla) ===")
    print(f"{'Variante':>25} | {'Univ. 10^12':>13} | {'Univ. 1000':>12} | {'Univ. 10':>10}")
    print("-" * 69)
    for nombre, fab in variantes:
        f_dist = primer_fallo(fab, 25_000, 10**12, semilla=409)
        f_1000 = primer_fallo(fab, 25_000, 1000, semilla=409)
        f_10 = primer_fallo(fab, 25_000, 10, semilla=409)
        c_dist = "---" if f_dist is None else str(f_dist)
        c_1000 = "---" if f_1000 is None else str(f_1000)
        c_10 = "---" if f_10 is None else str(f_10)
        print(f"{nombre:>25} | {c_dist:>13} | {c_1000:>12} | {c_10:>10}")

    # 4. Generacion de la figura en 2 paneles
    # Panel 1: Traza de 30 operaciones donde se ve la desincronizacion de '<'
    rng_traza = random.Random(28)
    p_ok = PilaMin()
    p_mal = PilaMinDosPilas(estricto=True)
    pasos_t, cimas_t, min_real_t, min_mal_t = [], [], [], []
    for paso in range(1, 33):
        if rng_traza.random() < 0.56 or p_ok.vacia() or len(p_mal.datos) <= 1:
            x = rng_traza.randint(2, 9)
            p_ok.apilar(x)
            p_mal.apilar(x)
        else:
            p_ok.desapilar()
            p_mal.desapilar()
        pasos_t.append(paso)
        cimas_t.append(p_ok.cima())
        min_real_t.append(p_ok.minimo())
        # Si min_mal quedo vacia por el bug, ponemos NaN o su valor erroneo
        min_mal_t.append(p_mal.minimo() if p_mal.minimo() is not None else -1)

    # Panel 2: Tiempo medio hasta el primer fallo de '<' segun tamano del universo U
    universos = [4, 8, 16, 32, 64, 128, 256, 512]
    promedios_fallo = []
    repeticiones = 120
    for u in universos:
        total_k = 0
        for r in range(repeticiones):
            k = primer_fallo(lambda: PilaMinDosPilas(estricto=True), 50_000, u, semilla=8000 + r)
            total_k += (k if k is not None else 50_000)
        promedios_fallo.append(total_k / repeticiones)

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11.5, 4.4))

    ax1.plot(pasos_t, cimas_t, "o:", color="#888888", lw=1.3, markersize=4,
             label="Valor en la cima")
    ax1.step(pasos_t, min_real_t, where="post", color="#1f77b4", lw=2.3,
             label="Minimo real (PilaMin y <=)")
    ax1.step(pasos_t, min_mal_t, where="post", color="#d62728", linestyle="--", lw=2.0,
             label="Minimo reportado con '<' (defectuosa)")
    # Resaltar pasos con discrepancia
    pasos_err = [t for t, mr, mm in zip(pasos_t, min_real_t, min_mal_t) if mr != mm]
    vals_err = [mm for mr, mm in zip(min_real_t, min_mal_t) if mr != mm]
    ax1.scatter(pasos_err, vals_err, color="#d62728", zorder=5, s=45, label="Respuesta erronea")
    ax1.set_title("Desincronizacion al repetir el minimo (traza de 32 ops)")
    ax1.set_xlabel("Operacion k")
    ax1.set_ylabel("Valor del elemento")
    ax1.set_yticks(range(1, 11))
    ax1.grid(True, alpha=0.3)
    ax1.legend(loc="upper right", fontsize=8)

    ax2.plot(universos, promedios_fallo, "s-", color="#9467bd", lw=2, markersize=5,
             label="Promedio empirico (120 corridas)")
    ax2.set_xscale("log", base=2)
    ax2.set_yscale("log")
    ax2.set_title("Operaciones hasta el primer fallo de '<' vs universo U")
    ax2.set_xlabel("Tamano del universo de valores U (escala log2)")
    ax2.set_ylabel("Operaciones promedio hasta fallar (escala log)")
    ax2.grid(True, which="both", alpha=0.3)
    ax2.legend(loc="upper left", fontsize=8.5)

    plt.tight_layout()
    salida_png = Path(__file__).with_name("ejercicio-03.png")
    plt.savefig(salida_png, dpi=150)
    print(f"\nGrafica guardada en {salida_png.name}")
