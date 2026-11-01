from pathlib import Path
import matplotlib.pyplot as plt

BLANCO = "_"

# Tabla de transiciones: (estado, simbolo_leido) -> (simbolo_escrito, desplazamiento, nuevo_estado)
TRANSICIONES = {
    ("acarreo", "1"): ("0", -1, "acarreo"),
    ("acarreo", "0"): ("1", +1, "volver"),
    ("acarreo", BLANCO): ("1", +1, "volver"),
    ("volver", "0"): ("0", +1, "volver"),
    ("volver", BLANCO): (BLANCO, -1, "fin"),
}


class MaquinaContador:
    def __init__(self):
        # La posicion 0 corresponde al bit menos significativo (LSB)
        self.cinta = {0: "0"}
        self.cabezal = 0

    def leer(self, pos):
        return self.cinta.get(pos, BLANCO)

    def incrementar(self):
        """Ejecuta un incremento completo desde el estado 'acarreo' hasta 'fin'."""
        estado = "acarreo"
        pasos = 0
        while estado != "fin":
            simbolo = self.leer(self.cabezal)
            escribir, mover, estado = TRANSICIONES[(estado, simbolo)]
            self.cinta[self.cabezal] = escribir
            self.cabezal += mover
            pasos += 1
        return pasos

    def cadena_binaria(self):
        min_pos = min(self.cinta.keys())
        bits = "".join(self.leer(i) for i in range(min_pos, 1))
        return bits.lstrip(BLANCO)

    def valor(self):
        return int(self.cadena_binaria(), 2)

    def cantidad_unos(self):
        return sum(1 for v in self.cinta.values() if v == "1")


def unos_al_final(v):
    t = 0
    while v & 1:
        v >>= 1
        t += 1
    return t


if __name__ == "__main__":
    # 1. Traza detallada de los primeros 8 incrementos (de 0 a 8)
    M_traza = MaquinaContador()
    phi_ant = 2 * M_traza.cantidad_unos()
    acum = 0
    print("=== Traza paso a paso de los incrementos i = 1..8 ===")
    print(f"{'i':>2} | {'De -> A':>9} | {'Cinta final':>11} | {'t':>2} | {'c_i':>4} | "
          f"{'Phi_i':>5} | {'dPhi':>5} | {'c_hat':>5} | {'Total':>5}")
    print("-" * 72)
    for i in range(1, 9):
        v_ant = M_traza.valor()
        t = unos_al_final(v_ant)
        c_i = M_traza.incrementar()
        phi_i = 2 * M_traza.cantidad_unos()
        dphi = phi_i - phi_ant
        c_hat = c_i + dphi
        acum += c_i
        print(f"{i:>2} | {f'{v_ant} -> {i}':>9} | {M_traza.cadena_binaria():>11} | {t:>2} | "
              f"{c_i:>4} | {phi_i:>5} | {dphi:>+5} | {c_hat:>5} | {acum:>5}")
        phi_ant = phi_i
    print()

    # 2. Verificacion exhaustiva hasta m = 2^14 - 1 = 16383
    M = MaquinaContador()
    total = 0
    peor_paso = 0
    phi = 0

    costos_128 = []
    phis_128 = []
    totales_128 = []

    limite = (1 << 14) - 1
    print("=== Resumen para distintos valores de m ===")
    print(f"{'m':>7} | {'Pasos totales':>14} | {'Cota 4m':>10} | {'Prom. c_i':>10} | {'Max c_i':>8}")
    print("-" * 60)

    for k in range(1, limite + 1):
        antes = M.valor()
        t = unos_al_final(antes)
        c = M.incrementar()

        assert M.cabezal == 0 and M.valor() == antes + 1
        assert c == 2 * t + 2

        nuevo_phi = 2 * M.cantidad_unos()
        assert c + (nuevo_phi - phi) == 4

        phi = nuevo_phi
        total += c
        peor_paso = max(peor_paso, c)
        assert total == 4 * k - 2 * bin(k).count("1")

        if k <= 128:
            costos_128.append(c)
            phis_128.append(phi)
            totales_128.append(total)

        if k in (8, 16, 64, 100, 1000, 1024, 10_000, limite):
            print(f"{k:>7} | {total:>14} | {4 * k:>10} | {total / k:>10.4f} | {peor_paso:>8}")

    print("\nVerificacion completada en 16 383 incrementos: costo amortizado = 4 y formula 4m - 2s(m) exactos.")

    # 3. Generacion de la grafica en 2 paneles para m = 1..128
    ms = list(range(1, 129))
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11.5, 4.4))

    # Panel 1: Costo real c_i, potencial Phi_i y costo amortizado c_hat = 4
    ax1.vlines(ms, 0, costos_128, color="#1f77b4", alpha=0.45, lw=1.2)
    ax1.plot(ms, costos_128, "o", color="#1f77b4", markersize=3.5, label="Costo real c_i = 2t + 2")
    ax1.plot(ms, phis_128, "-", color="#ff7f0e", lw=1.6, label="Potencial Phi_i = 2 s(i)")
    ax1.axhline(4, color="#d62728", linestyle="--", lw=2.0, label="Costo amortizado c_hat_i = 4")
    ax1.set_title("Costo real, potencial y costo amortizado (i = 1..128)")
    ax1.set_xlabel("Incremento i")
    ax1.set_ylabel("Pasos de la maquina de Turing")
    ax1.set_xlim(0, 130)
    ax1.set_ylim(0, 18)
    ax1.grid(True, alpha=0.3)
    ax1.legend(loc="upper left", fontsize=8.5)

    # Panel 2: Costo acumulado real vs cota superior 4m (y promedio acumulado en eje secundario)
    cota_4m = [4 * m for m in ms]
    ax2.plot(ms, cota_4m, "--", color="#555555", lw=1.8, label="Cota superior 4m")
    ax2.plot(ms, totales_128, "-", color="#2ca02c", lw=2.0, label="Costo acumulado exacto 4m - 2s(m)")
    ax2.fill_between(ms, totales_128, cota_4m, color="#ff7f0e", alpha=0.22,
                     label="Ahorro acumulado Phi_m = 2s(m)")
    ax2.set_title("Costo total acumulado frente a la cota lineal 4m")
    ax2.set_xlabel("Numero de incrementos m")
    ax2.set_ylabel("Pasos acumulados")
    ax2.set_xlim(0, 130)
    ax2.grid(True, alpha=0.3)
    ax2.legend(loc="upper left", fontsize=8.5)

    plt.tight_layout()
    salida_png = Path(__file__).with_name("ejercicio-04.png")
    plt.savefig(salida_png, dpi=150)
    print(f"Grafica guardada en {salida_png.name}")
