"""Ejercicio 4: el contador binario en una maquina de Turing de una cinta (C1 ej. 7, C4).
Simulador real de MT: tabla de transiciones, cinta infinita a ambos lados, un paso = una transicion."""
import math

B = "B"   # blanco


class MT:
    def __init__(self, delta, inicial, parada):
        self.delta, self.inicial, self.parada = delta, inicial, parada
        self.pasos_ejecutados = 0

    def correr(self, cinta, pos, limite=10**7):
        """cinta: dict posicion->simbolo; pos: posicion del cabezal. Devuelve (cinta, pos, pasos)."""
        q, pasos = self.inicial, 0
        while q != self.parada:
            sim = cinta.get(pos, B)
            q, esc, mov = self.delta[(q, sim)]
            if esc == B:
                cinta.pop(pos, None)
            else:
                cinta[pos] = esc
            pos += -1 if mov == "L" else 1
            pasos += 1
            assert pasos <= limite
        return cinta, pos, pasos


# ---- incremento: bits MSB a la izquierda, LSB a la derecha; cabezal en el LSB al empezar y al terminar
INC = {
    ("c", "1"): ("c", "0", "L"),     # acarreo: 1 -> 0, seguir a la izquierda
    ("c", "0"): ("r", "1", "R"),     # fin del acarreo: 0 -> 1, empezar el regreso
    ("c", B):   ("r", "1", "R"),     # fin del acarreo en el borde: nuevo bit mas significativo
    ("r", "0"): ("r", "0", "R"),     # regreso hacia el LSB
    ("r", "1"): ("r", "1", "R"),     # (no se alcanza en una cinta bien formada; completa la tabla)
    ("r", B):   ("h", B, "L"),       # paso el LSB: un paso atras y parar sobre el LSB
}
DEC = {
    ("c", "0"): ("c", "1", "L"),     # prestamo: 0 -> 1, seguir a la izquierda
    ("c", "1"): ("r", "0", "R"),     # el 1 mas bajo pasa a 0; regreso
    ("r", "0"): ("r", "0", "R"),
    ("r", "1"): ("r", "1", "R"),
    ("r", B):   ("h", B, "L"),
}
MT_INC = MT(INC, "c", "h")
MT_DEC = MT(DEC, "c", "h")


def cinta_de(s):
    """Cadena de bits (MSB a la izquierda) -> cinta con el LSB en la posicion 0."""
    n = len(s)
    return {i - (n - 1): ch for i, ch in enumerate(s)}


def texto(cinta):
    if not cinta:
        return ""
    a, b = min(cinta), max(cinta)
    return "".join(cinta.get(i, B) for i in range(a, b + 1))


def unos(cinta):
    return sum(1 for v in cinta.values() if v == "1")


def valor(cinta):
    s = texto(cinta)
    return int(s, 2) if s else 0


def popcount(x):
    return bin(x).count("1")


def v2(x):
    return (x & -x).bit_length() - 1


print("=== 1. Tabla de transiciones del incremento (6 pares estado-simbolo, completa) ===")
print("  estados: c (acarreo, inicial), r (regreso), h (parada).  simbolos: 0, 1, B (blanco)")
for (q, s), (q2, e, m) in INC.items():
    print(f"  delta({q}, {s}) = ({q2}, {e}, {m})")

print()
print("=== 2. Un incremento paso a paso: 111 -> 1000 (c = 7 = 2^3 - 1, t = 3 unos finales; la cinta crece) ===")
cinta = cinta_de("111")
pos, q, pasos = 0, "c", 0
print(f"  paso  estado cabezal  cinta (cabezal marcado con [ ])")
def mostrar(cinta, pos, q, pasos):
    a = min(min(cinta), pos) - 1
    b = max(max(cinta), pos) + 1
    s = "".join(("[" + cinta.get(i, B) + "]") if i == pos else (" " + cinta.get(i, B) + " ") for i in range(a, b + 1))
    print(f"  {pasos:>4}  {q:>5}  {pos:>5}   {s}")
mostrar(cinta, pos, q, pasos)
while q != "h":
    q, esc, mov = INC[(q, cinta.get(pos, B))]
    if esc == B:
        cinta.pop(pos, None)
    else:
        cinta[pos] = esc
    pos += -1 if mov == "L" else 1
    pasos += 1
    mostrar(cinta, pos, q, pasos)
print(f"  pasos = {pasos} = 2(t+1) con t = 3;  cinta final {texto(cinta)}, cabezal en la posicion {pos} (el LSB)")
assert pasos == 8 and pos == 0

print()
print("=== 3. Simulador real: m incrementos seguidos desde 0, m = 1 .. 2^16 ===")
cinta = {0: "0"}                          # el numero 0
total = 0
fallos = 0
amort_mal = 0
maxcosto = (0, 0)
acum = {}
for c in range(0, 2 ** 16):
    # t = unos finales de c = v2(c+1)
    t = v2(c + 1)
    uno_antes = unos(cinta)
    cinta, pos, pasos = MT_INC.correr(cinta, 0)
    ok = (pasos == 2 * (t + 1) and pos == 0 and valor(cinta) == c + 1)
    fallos += not ok
    amort = pasos + 2 * (unos(cinta) - uno_antes)      # costo real + (Phi' - Phi), Phi = 2 * (numero de unos)
    amort_mal += (amort != 4)
    total += pasos
    m = c + 1
    if m in (1, 2, 3, 4, 5, 7, 8, 100, 1000, 1023, 1024, 2 ** 10 + 1, 2 ** 15, 2 ** 16 - 1, 2 ** 16):
        acum[m] = total
    if pasos > maxcosto[0]:
        maxcosto = (pasos, m)
print(f"  comprobaciones por incremento (pasos = 2(t+1), cabezal vuelve al LSB, cinta = c+1): fallos = {fallos}")
print(f"  costo amortizado (real + variacion de Phi = 2*unos) distinto de 4: {amort_mal} de 65536")
print(f"  {'m':>7} {'total de pasos':>15} {'4m - 2*s2(m)':>14} {'4m':>9}  {'s2(m)':>5}")
for m, tot in sorted(acum.items()):
    print(f"  {m:>7} {tot:>15} {4 * m - 2 * popcount(m):>14} {4 * m:>9}  {popcount(m):>5}")
    assert tot == 4 * m - 2 * popcount(m)
print(f"  mayor costo de un incremento hasta m = 2^16: {maxcosto[0]} pasos, en el incremento numero m = {maxcosto[1]} "
      f"(2(k+1) con k = 16)")

print()
print("=== 4. Formula del total para TODO m = 1..2^16 (acumulado del simulador) ===")
cinta = {0: "0"}
total = 0
malos = 0
for c in range(0, 2 ** 16):
    cinta, pos, pasos = MT_INC.correr(cinta, 0)
    total += pasos
    m = c + 1
    if total != 4 * m - 2 * popcount(m):
        malos += 1
    if total > 4 * m:
        malos += 1
print(f"  m = 1..65536: total == 4m - 2*s2(m) y total <= 4m: fallos = {malos}")
print("  Costo por incremento = 2(t+1), t = v2(c+1);  suma = 2m + 2*v2(m!) = 2m + 2(m - s2(m))  (Legendre)")
assert all(sum(2 * (v2(c + 1) + 1) for c in range(m)) == 4 * m - 2 * popcount(m) for m in range(1, 300))

print()
print("=== 5. Salida desde un contador que no esta en 0: c0 = 2^k - 1 ===")
for k, m in ((10, 1), (10, 2), (10, 100), (10, 1000), (16, 5)):
    c0 = 2 ** k - 1
    cinta = cinta_de(bin(c0)[2:])
    total = 0
    for _ in range(m):
        cinta, pos, pasos = MT_INC.correr(cinta, 0)
        total += pasos
    cota = 4 * m + 2 * popcount(c0) - 2 * popcount(c0 + m)       # real = 4m + Phi_0 - Phi_m
    print(f"  c0=2^{k}-1, m={m:>5} incrementos: pasos = {total:>6}; 4m + Phi_0 - Phi_m = {cota:>6}; 4m = {4 * m:>5}"
          f"   (media por operacion {total / m:.1f})")
    assert total == cota

print()
print("=== 6. Con decremento: la secuencia 2^k - 1  <->  2^k  ===")
print("  decremento: ('c',0)->(c,1,L) ('c',1)->(r,0,R); misma tabla de regreso.")
print("  Convencion de esta seccion: contador de ANCHO FIJO k+1 (como el contador de k bits del ej. 2 de C4),")
print("  con ceros a la izquierda permitidos: 2^k-1 se escribe 0 1^k y 2^k se escribe 1 0^k. La cinta no crece.")
for k in (4, 8, 10, 16):
    cinta = cinta_de("0" + "1" * k)          # 2^k - 1 con un cero a la izquierda
    ops = 1000
    total, costes = 0, []
    for i in range(ops):
        if i % 2 == 0:
            cinta, pos, pasos = MT_INC.correr(cinta, 0)
        else:
            cinta, pos, pasos = MT_DEC.correr(cinta, 0)
        assert pos == 0
        total += pasos
        costes.append(pasos)
    esperado = "1" + "0" * k
    print(f"  k={k:>2}: {ops} operaciones alternadas inc/dec: pasos totales = {total} = {total // ops} por operacion "
          f"(cada una 2(k+1) = {2 * (k + 1)}); cinta final = {texto(cinta).strip(B)[:12]}...")
    assert all(c == 2 * (k + 1) for c in costes)
print("  la misma cantidad de operaciones solo con incrementos cuesta < 4 por operacion (seccion 3).")
print("  Potencial Phi = 2*unos en esta secuencia:")
k = 10
cinta = cinta_de("0" + "1" * k)
for nombre, M in (("inc", MT_INC), ("dec", MT_DEC), ("inc", MT_INC), ("dec", MT_DEC)):
    antes = unos(cinta)
    cinta, pos, pasos = M.correr(cinta, 0)
    print(f"    {nombre}: pasos reales {pasos}, unos {antes} -> {unos(cinta)}, "
          f"amortizado = {pasos} + 2*({unos(cinta)} - {antes}) = {pasos + 2 * (unos(cinta) - antes)}")
print("  Sobre un ciclo (inc, dec) el estado vuelve al mismo y Phi telescopa: suma amortizada = suma real = 4(k+1).")
print(f"  Para cualquier potencial: amortizado medio por operacion = 4(k+1)/2 = 2(k+1) = {2 * (k + 1)} (k = {k}); no es O(1).")
