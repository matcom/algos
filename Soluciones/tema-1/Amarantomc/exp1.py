import pandas as pd

def mezcla_optimizada(A, B):
    i, j = 0, 0
    salida = []
    comparaciones = 0
    
    while (len(A) - i > 1) and (j < len(B)):
        comparaciones += 1
        if A[i] <= B[j]:
            salida.append(A[i])
            i += 1
        else:
            salida.append(B[j])
            j += 1

    if j < len(B):
        salida.extend(B[j:])
    if i < len(A):
        salida.append(A[-1])

    return salida, comparaciones

def mezclar_correcta(A, B):
    """Mezcla estándar de referencia O(n+m)"""
    i, j = 0, 0
    salida = []
    while i < len(A) and j < len(B):
        if A[i] <= B[j]:
            salida.append(A[i])
            i += 1
        else:
            salida.append(B[j])
            j += 1
    salida.extend(A[i:])
    salida.extend(B[j:])
    return salida

def construir_contraejemplo_adversario(n):
    """
    Construye la entrada adversarial donde a_n < b_n.
    A = [1, 2, ..., n-1, 2n - 1]
    B = [n, n+1, ..., 2n - 2, 2n]
    """
    A = list(range(1, n)) + [2 * n - 1]
    B = list(range(n, 2 * n - 1)) + [2 * n]
    return A, B

def probar_contraejemplos():
    casos = [2, 3, 4, 5, 8]
    reporte = []

    for n in casos:
        A, B = construir_contraejemplo_adversario(n)
        resultado_algoritmo, comps = mezcla_optimizada(A, B)
        resultado_esperado = mezclar_correcta(A, B)
        es_correcto = (resultado_algoritmo == resultado_esperado)

        reporte.append({
            "n": n,
            "Lista A": str(A),
            "Lista B": str(B),
            "Salida Algoritmo": str(resultado_algoritmo),
            "Salida Correcta": str(resultado_esperado),
            "¿Correcto?": es_correcto
        })

    df = pd.DataFrame(reporte)
    print(df.to_string(index=False))

if __name__ == "__main__":
    probar_contraejemplos()
