import random
from collections import deque
import matplotlib.pyplot as plt
import numpy as np

def gale_shapley_incompletas(pref_a, pref_b):
    """
    Algoritmo de Gale-Shapley adaptado para listas incompletas.
    pref_a: dict {proponente: lista_de_preferencias}
    pref_b: dict {receptor: lista_de_preferencias}
    """
    # Truncar listas para asegurar aceptabilidad mutua
    pref_a_filtrada = {}
    for a, lista in pref_a.items():
        pref_a_filtrada[a] = [b for b in lista if b in pref_b and a in pref_b[b]]
        
    n_a = len(pref_a)
    n_b = len(pref_b)
    
    # Precomputar rangos de receptores para comparaciones O(1)
    rango_b = {}
    for b, lista in pref_b.items():
        rango_b[b] = {a: i for i, a in enumerate(lista)}
        
    siguiente_propuesta = {a: 0 for a in pref_a}
    pareja_de_b = {b: None for b in pref_b}
    
    libres = deque(list(pref_a.keys()))
    propuestas_totales = 0
    
    while libres:
        a = libres.popleft()
        idx = siguiente_propuesta[a]
        
        # Si el proponente agotó su lista de aceptables, se queda solo
        if idx >= len(pref_a_filtrada[a]):
            continue
            
        b = pref_a_filtrada[a][idx]
        siguiente_propuesta[a] += 1
        propuestas_totales += 1
        
        actual = pareja_de_b[b]
        if actual is None:
            pareja_de_b[b] = a
        elif rango_b[b][a] < rango_b[b][actual]:
            pareja_de_b[b] = a
            libres.append(actual)
        else:
            libres.append(a)
            
    # Construir emparejamiento final M (a -> b o None)
    M_a = {a: None for a in pref_a}
    for b, a in pareja_de_b.items():
        if a is None:
            continue
        M_a[a] = b
        
    return M_a, pareja_de_b, propuestas_totales

def verificar_estabilidad(M_a, M_b, pref_a, pref_b):
    """
    Verifica individual rationality y parejas bloqueantes.
    Devuelve lista de parejas bloqueantes encontradas.
    """
    bloqueantes = []
    
    # 1. Verificar Racionalidad Individual
    for a, b in M_a.items():
        if b is None:
            continue
        if b not in pref_a[a] or a not in pref_b[b]:
            return [("Inestabilidad Individual", a, b)]
            
    # 2. Buscar parejas bloqueantes externas
    for a, lista_a in pref_a.items():
        actual_b = M_a[a]
        # Elementos preferidos sobre actual_b
        if actual_b in lista_a:
            pref_a_superiores = lista_a[:lista_a.index(actual_b)]
        else:
            pref_a_superiores = lista_a  # Prefiere cualquiera de su lista sobre estar solo
            
        for b in pref_a_superiores:
            if a not in pref_b[b]:  # No es aceptable para b
                continue
            actual_a = M_b[b]
            if actual_a in pref_b[b]:
                pref_b_superiores = pref_b[b][:pref_b[b].index(actual_a)]
            else:
                pref_b_superiores = pref_b[b]
                
            if a in pref_b_superiores:
                bloqueantes.append((a, b))
                
    return bloqueantes

def ejecutar_experimentos():
    print("=" * 70)
    print(f"{'Tamaño':<8} | {'Propuestas':<10} | {'Solos (A)':<10} | {'Estable':<8}")
    print("=" * 70)
    
    random.seed(42)
    instancias = [10, 20, 50, 100, 200]
    propuestas_medid = []
    
    for n in instancias:
        proponentes = [f"a_{i}" for i in range(n)]
        receptores = [f"b_{j}" for j in range(n)]
        
        # Generar listas incompletas aleatorias (tamaño de lista entre 20% y 70% de n)
        pref_a = {}
        pref_b = {}
        for a in proponentes:
            k = random.randint(max(1, int(n * 0.2)), max(1, int(n * 0.7)))
            pref_a[a] = random.sample(receptores, k)
        for b in receptores:
            k = random.randint(max(1, int(n * 0.2)), max(1, int(n * 0.7)))
            pref_b[b] = random.sample(proponentes, k)
            
        M_a, M_b, props = gale_shapley_incompletas(pref_a, pref_b)
        bloq = verificar_estabilidad(M_a, M_b, pref_a, pref_b)
        
        solos_a = sum(1 for b in M_a.values() if b is None)
        es_estable = "SÍ" if len(bloq) == 0 else "NO"
        
        propuestas_medid.append(props)
        print(f"{n:<8} | {props:<10} | {solos_a:<10} | {es_estable:<8}")
    print("=" * 70)

import matplotlib.pyplot as plt
import numpy as np
import random

# Datos de la simulación
tamanios = np.array([10, 20, 50, 100, 150, 200])
propuestas_observadas = []
cotas_potencial = []

random.seed(42)
for n in tamanios:
    proponentes = [f"a_{i}" for i in range(n)]
    receptores = [f"b_{j}" for j in range(n)]
    
    pref_a = {a: random.sample(receptores, random.randint(int(n*0.2), int(n*0.6))) for a in proponentes}
    pref_b = {b: random.sample(proponentes, random.randint(int(n*0.2), int(n*0.6))) for b in receptores}
    
    # Calcular cota del potencial (longitud total de listas filtradas)
    cota = sum(len([b for b in pref_a[a] if a in pref_b[b]]) for a in pref_a)
    cotas_potencial.append(cota)
    
    # Ejecutar algoritmo
    M_a, M_b, props = gale_shapley_incompletas(pref_a, pref_b)
    propuestas_observadas.append(props)

# Generar Gráfico
plt.figure(figsize=(9, 5))
plt.plot(tamanios, cotas_potencial, 'ro--', label='Cota Teórica del Potencial (Φ₀)', linewidth=2)
plt.plot(tamanios, propuestas_observadas, 'bs-', label='Propuestas Reales (Ejecución)', linewidth=2)

plt.title('Complejidad Empírica vs. Potencial Teórico en Gale-Shapley Incompleto', fontsize=12)
plt.xlabel('Tamaño de la Instancia (n)', fontsize=11)
plt.ylabel('Número de Propuestas', fontsize=11)
plt.grid(True, linestyle=':', alpha=0.6)
plt.legend(fontsize=10)
plt.tight_layout()
plt.savefig('gale_shapley_incompleto_complejidad.png', dpi=300)