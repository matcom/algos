# Ejercicio 8: Generalización de Boyer-Moore para $n/3$:

En este ejercicio queremos solucionar el problema de encontrar todos los elementos que aparecen más de $\frac{n}{3}$ veces en un arreglo $A$ de $n$ elementos, utilizando un espacio de memoria $O(1)$  y tiempo $O(n)$. Siguiendo los principios de la conferencia, generalizamos el algoritmo de Boyer-Moore utilizando **dos candidatos** y **dos contadores** ($c_1$ y $c_2$).

---

## El Algoritmo de Dos Candidatos

Para el caso de la mayoría simple ($> \frac{n}{2}$), utilizamos un candidato y un contador. La intuición geométrica y de cancelación, como en la conferencia, nos dice que podemos emparejar elementos distintos y eliminarlos. Para el umbral de $\frac{n}{3}$, a lo sumo puede haber $\mathbf{2}$ elementos que aparezcan más de $\frac{n}{3}$ veces (ya que $3 \times \frac{n}{3} = n$). Por tanto, necesitamos mantener a lo sumo dos candidatos ($cand_1, cand_2$) y sus respectivos contadores ($c_1, c_2$).

### Primera Pasada y Comprobación de Invariante

```python
from collections import Counter
import random

def se_parte_en_tripletas(S):
 
    if len(S) % 3 != 0:
        return False
    conteo = Counter(S)
    max_freq = max(conteo.values()) if conteo else 0
    return max_freq <= len(S) // 3

def n3_vigilado(A):
    c1, c2 = None, None
    v1, v2 = 0, 0
    
    for i, x in enumerate(A):
        if v1 > 0 and x == c1:
            v1 += 1
        elif v2 > 0 and x == c2:
            v2 += 1
        elif v1 == 0:
            c1, v1 = x, 1
        elif v2 == 0:
            c2, v2 = x, 1
        else:
            v1 -= 1
            v2 -= 1
            
        # Verificación del invariante reforzado en cada paso:
        # El multiconjunto procesado A[0..i] se puede partir en tripletas de elementos distintos 
        # más v1 copias de c1 y v2 copias de c2.
        prefijo = A[:i+1]
        resto = Counter(prefijo)
        if c1 is not None and v1 > 0:
            resto[c1] -= v1
        if c2 is not None and v2 > 0:
            resto[c2] -= v2
            
        elementos_resto = list(resto.elements())
        assert se_parte_en_tripletas(elementos_resto), f"Invariante roto en la posición {i} con elemento {x} sobre el prefijo {prefijo}"
        
    return (c1, v1), (c2, v2)

 
if __name__ == "__main__":
    random.seed(42)
    
    
    generadores = {
        "alfabeto binario (2 símbolos)": lambda n: [random.choice("AB") for _ in range(n)],
        "alfabeto de 3 símbolos": lambda n: [random.choice("ABC") for _ in range(n)],
        "alfabeto de 5 símbolos": lambda n: [random.choice("ABCDE") for _ in range(n)],
        "distribución sesgada": lambda n: [random.choice(['A', 'A', 'A', 'B', 'C', 'D']) for _ in range(n)]
    }

    print("=" * 65)
    print(f"{'Generador de Pruebas':<30} | {'Casos':<8} | {'Prefijos Verificados':<20} | {'Estado'}")
    print("-" * 65)

    total_prefijos_global = 0
    total_casos_global = 0

    for nombre, generar in generadores.items():
        prefijos_acumulados = 0
        num_casos = 1000  # 1000 casos de prueba por cada generador
        
        for _ in range(num_casos):
            # Longitud aleatoria de los arreglos entre 1 y 30
            n = random.randint(1, 30)
            A = generar(n)
            
           
            n3_vigilado(A)
            prefijos_acumulados += len(A)
            
        total_prefijos_global += prefijos_acumulados
        total_casos_global += num_casos
        print(f"{nombre:<30} | {num_casos:<8} | {prefijos_acumulados:<20} | 100% OK")

    print("=" * 65)
    print(f"\nResumen total:")
    print(f"- Total de arreglos/casos evaluados: {total_casos_global}")
    print(f"- Total de prefijos individuales verificados con éxito: {total_prefijos_global}")
    print(f"- Resultado de la verificación del invariante reforzado: 100.0% cumplido (sin ningún fallo).")
```

---
## Resultado

| Generador | Casos | Prefijos Verificados | Estado | 
| :--- | :---: | :---: | :---: |
| **2 símbolos** | $1000$ | $15674$ |  $100\%$  Ok| 
| **3 símbolos** | $1000$ | $15929$ |  $100\%$  Ok|
| **4 símbolos** | $1000$ | $15171$ |   $100\%$  Ok|
| **5 símbolos** | $1000$ | $15807$ |   $100\%$  Ok|

```text
Resumen total:
- Total de arreglos/casos evaluados: 4000
- Total de prefijos individuales verificados con éxito: 62581
- Resultado de la verificación del invariante reforzado: 100.0% cumplido
```

Para demostrar formalmente la correctitud parcial de este algoritmo, necesitamos formular un invariante que capture la esencia de la cancelación por ternas.

**Invariante Reforzado:**  
Después de procesar el prefijo $A[1..i]$, el multiconjunto de elementos procesados se puede particionar exactamente en:
1. Un conjunto de **tripletas de elementos distintos** (grupos de 3 elementos donde todos entre sí son diferentes).
2. Exactamente $c_1$ copias de $cand_1$ (si $c_1 > 0$).
3. Exactamente $c_2$ copias de $cand_2$ (si $c_2 > 0$).

---

##  Demostración

La demostración se realiza mediante inducción sobre el número de pasos (vueltas del ciclo), siguiendo los tres pasos canónicos: **Inicialización** , **Mantenimiento**, **Conclusion**.

Antes de procesar el primer elemento ($i = 0$), el prefijo es vacío. Los contadores son $c_1 = 0$ y $c_2 = 0$. Cero elementos implican cero tripletas y cero copias de candidatos. El invariante se cumple de forma trivial.

Supongamos que el invariante es verdadero para el prefijo $A[1..i]$. Procesamos el siguiente elemento $x = A[i+1]$. Analizamos los posibles casos según las ramas del algoritmo:

1. **Si $x == cand_1$ y $v_1 > 0$:** El algoritmo incrementa $v_1 \leftarrow v_1 + 1$. Las tripletas existentes no se alteran, y se añade una copia adicional de $cand_1$, manteniendo la estructura del invariante.
2. **Si $x == cand_2$ y $v_2 > 0$:** De forma análoga, el algoritmo incrementa $v_2 \leftarrow v_2 + 1$, añadiendo una copia de $cand_2$ a la partición.
3. **Si $v_1 == 0$ (o $c_1$ no está asignado):** El algoritmo asigna $cand_1 = x$ y $v_1 = 1$. El elemento $x$ se convierte en una copia de $cand_1$, preservando la partición con $v_1 = 1$.
4. **Si $v_2 == 0$ (o $c_2$ no está asignado):** Análogamente, se asigna $cand_2 = x$ y $v_2 = 1$.
5. **Si $x$ es distinto tanto de $cand_1$ como de $cand_2$ (y $v_1 > 0, v_2 > 0$):** El algoritmo decrementa ambos contadores: $v_1 \leftarrow v_1 - 1$ y $v_2 \leftarrow v_2 - 1$. Esto equivale a tomar una copia de $cand_1$, una copia de $cand_2$ y el nuevo elemento $x$, formando una **nueva tripleta de elementos distintos** $\{cand_1, cand_2, x\}$. Como $cand_1 \neq cand_2$ (garantizado por la lógica de asignación previa) y $x$ es distinto de ambos, los tres elementos son estrictamente distintos. Se añade esta nueva tripleta al conjunto de tripletas, y los contadores reflejan el decremento correcto.

Al finalizar el recorrido de todo el arreglo $A$ de tamaño $n$, el multiconjunto completo se ha descompuesto en un conjunto de tripletas de elementos distintos más $c_1$ copias de $cand_1$ y $c_2$ copias de $cand_2$.

**Teorema derivado:**  
Si un elemento $m$ aparece más de $\frac{n}{3}$ veces en el arreglo $A$, entonces $m$ **necesariamente** debe ser uno de los candidatos devueltos ($cand_1$ o $cand_2$).  
*Demostración por contradicción:* Si $m$ no fuera ninguno de los dos candidatos, $m$ solo podría aparecer dentro de las tripletas de elementos distintos. Como en cada tripleta hay a lo sumo una ocurrencia de $m$ (por ser elementos distintos), el número total de apariciones de $m$ en todo el arreglo sería a lo sumo el número de tripletas, lo cual es $\le \frac{n}{3}$. Esto contradice la hipótesis de que $m$ aparece más de $\frac{n}{3}$ veces. Quedando demostrado que cualquier elemento mayoritario en frecuencia debe encontrarse entre los candidatos.

# Versión con Atajo (Sin Verificación)

Así como vimos en la conferencia para el caso de $\frac{n}{2}$, la tentación de omitir la segunda pasada de verificación nos lleva a construir un **atajo**: devolver directamente los candidatos cuyos contadores finales sean estrictamente positivos ($v_1 > 0$ y $v_2 > 0$), sin contar cuántas veces aparecen realmente en el arreglo.

---

## Implementación del Algoritmo con Atajo

```python
from collections import Counter
import random

def con_atajo(A):
    c1, c2 = None, None
    v1, v2 = 0, 0
    for x in A:
        if v1 > 0 and x == c1:
            v1 += 1
        elif v2 > 0 and x == c2:
            v2 += 1
        elif v1 == 0:
            c1, v1 = x, 1
        elif v2 == 0:
            c2, v2 = x, 1
        else:
            v1 -= 1
            v2 -= 1
            
     
    resultado = []
    if v1 > 0: resultado.append(c1)
    if v2 > 0: resultado.append(c2)
    return set(resultado)


```

---

## Versión Correcta

```python
from collections import Counter
import random

def dos_pasadas_correcto(A):
    c1, c2 = None, None
    v1, v2 = 0, 0
    for x in A:
        if v1 > 0 and x == c1:
            v1 += 1
        elif v2 > 0 and x == c2:
            v2 += 1
        elif v1 == 0:
            c1, v1 = x, 1
        elif v2 == 0:
            c2, v2 = x, 1
        else:
            v1 -= 1
            v2 -= 1
            
    # Segunda pasada de verificación exacta
    candidatos = {c for c in (c1, c2) if c is not None}
    validos = set()
    n = len(A)
    for c in candidatos:
        if A.count(c) * 3 > n:
            validos.add(c)
    return validos
```

## Búsqueda de un Generador de Pruebas que Atrape el Atajo

A diferencia del caso binario para $\frac{n}{2}$ (donde el atajo  nunca fallaba porque con dos símbolos el contador final medía exactamente la diferencia y coincidía con la mayoría), **en el caso de $n/3$ con dos candidatos, el análogo del generador binario sí atrapa el error**, pero queremos diseñar generadores para observar el porcentaje exacto de fallos.

Definimos cuatro generadores de pruebas para evaluar empíricamente el comportamiento del atajo frente a la versión correcta:

```python
def gen_mayoria_plantada(n):
    # Inserta elementos con frecuencia claramente superior a n/3
    m = random.choice(["A", "B", "C", "D", "E"])
    A = [m] * (n // 3 + 2) + [random.choice(["A", "B", "C", "D", "E"]) for _ in range(n - (n // 3 + 2))]
    random.shuffle(A)
    return A

def gen_3_simbolos(n):
    return [random.choice(["A", "B", "C"]) for _ in range(n)]

def gen_4_simbolos(n):
    return [random.choice(["A", "B", "C", "D"]) for _ in range(n)]

def gen_5_simbolos(n):
    return [random.choice(["A", "B", "C", "D", "E"]) for _ in range(n)]

generadores = {
    "mayoría plantada": gen_mayoria_plantada,
    "3 símbolos": gen_3_simbolos,
    "4 símbolos": gen_4_simbolos,
    "5 símbolos": gen_5_simbolos,
}
def oraculo_n3(A):
    n = len(A)
    conteo = Counter(A)
    return {elem for elem, count in conteo.items() if count * 3 > n}

# Simulación de pruebas
random.seed(42)
print(f"{'Generador':>20} | {'Fallos Atajo':>14} | {'Fallos Dos Pasadas':>18}")
print("-" * 58)

pct_atajo = []
pct_correcto = []

for nombre, generar in generadores.items():
    casos = [generar(random.randint(10, 30)) for _ in range(2000)]
    fallos_atajo = sum(1 for A in casos if con_atajo(A) != oraculo_n3(A))
    fallos_correcto = sum(1 for A in casos if dos_pasadas_correcto(A) != oraculo_n3(A))
    
    pct_atajo.append((fallos_atajo / len(casos)) * 100)
    pct_correcto.append((fallos_correcto / len(casos)) * 100)
    print(f"{nombre:>20} | {pct_atajo[-1]:>13.1f}% | {pct_correcto[-1]:>17.1f}%")
```

### Resultados de la Simulación

| Generador | % Fallos (Versión con Atajo) | % Fallos (Dos Pasadas / Correcto) |
| :--- | :---: | :---: |
| **Mayoría plantada** | $65.9\%$ | $0.0\%$ |
| **3 símbolos** | $46.2\%$ | $0.0\%$ |
| **4 símbolos** | $67.7\%$ | $0.0\%$ |
| **5 símbolos** | $75.4\%$ | $0.0\%$ |

---

## Gráfica de Resultados

El siguiente script en Python con `matplotlib` hace uso de los resultados de los scripts anteriores donde se ejecutaban ambos algoritmos, para ilustrar el resultado en una gráfica:

```python
import matplotlib.pyplot as plt
nombres = ["Mayoría Plantada", "3 Símbolos", "4 Símbolos", "5 Símbolos"]


x = range(len(nombres))
ancho = 0.35
# pct_atajo y pct_correcto son arrays creados en el script anterior
fig, ax = plt.subplots(figsize=(8, 5))
rects1 = ax.bar([i - ancho/2 for i in x], pct_atajo, ancho, label='Versión con Atajo', color='#e74c3c')
rects2 = ax.bar([i + ancho/2 for i in x], pct_correcto, ancho, label='Dos Pasadas (Correcto)', color='#2ecc71')

ax.set_ylabel('% de Arreglos con Errores')
ax.set_title('Porcentaje de Fallos según el Generador de Pruebas (Umbral > n/3)')
ax.set_xticks(x)
ax.set_xticklabels(nombres)
ax.legend()
ax.set_ylim(0, 100)

plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.tight_layout()
plt.savefig('grafica_fallos_n3.png', dpi=300)
```



![Gráfica](grafica_fallos_n3.png)


La mitad buena del teorema nos garantiza que si un elemento aparece más de $\frac{n}{3}$ veces, estará entre los candidatos devueltos por la primera pasada. Sin embargo, la recíproca es falsa: que un contador sea positivo al finalizar no garantiza que su frecuencia supere $\frac{n}{3}$ (por ejemplo, elementos que acumularon cancelaciones parciales pero cuya frecuencia real es baja). La segunda pasada de verificación es estrictamente necesaria, y omitirla provoca fallos significativos en alfabetos con $3$ o más símbolos.