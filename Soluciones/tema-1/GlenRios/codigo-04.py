import os
RUTA = os.path.join("Soluciones", "tema-1", "GlenRios")
os.makedirs(RUTA, exist_ok=True)  # crea la carpeta si no existe

def incrementar(bits, head=0):
    """bits: lista de 0/1, LSB en índice 0. Devuelve pasos."""
    pasos = 0
    i = head
    while i < len(bits) and bits[i] == 1:
        bits[i] = 0
        pasos += 1  # leer, escribir, mover
        i += 1
    if i == len(bits):
        bits.append(1)
    else:
        bits[i] = 1
    pasos += 1  # leer, escribir 1
    pasos += i  # volver al LSB
    return pasos

m = 1000
bits = [0]
total = 0
for _ in range(m):
    total += incrementar(bits)
print(f"m={m}, pasos totales={total}, 3m={3*m}, popcount={sum(bits)}")