# Soluciones del Tema 1: Fundamentos

**Estudiante:** Samy R. Sosa (`SammyRSosa`)  
**Asignatura:** Diseño y Análisis de Algoritmos · Ciencia de la Computación · MatCom · 2026

---

## Índice de ejercicios

| Ejercicio | Tema principal | Solución escrita | Código y pruebas | Visualizaciones |
|---|---|---|---|---|
| **01** | Computadora $1000\times$ más rápida ($\Theta(n^2)$ y $\Theta(n \log n)$) | [ejercicio-01.md](ejercicio-01.md) | [ejercicio-01.py](ejercicio-01.py) | [ejercicio-01.png](ejercicio-01.png) |
| **02** | Búsqueda binaria: invariante, potencial y cota de información | [ejercicio-02.md](ejercicio-02.md) | [ejercicio-02.py](ejercicio-02.py) | [ejercicio-02.png](ejercicio-02.png) |
| **03** | Pila con `minimo` en $O(1)$ de peor caso | [ejercicio-03.md](ejercicio-03.md) | [ejercicio-03.py](ejercicio-03.py) | [ejercicio-03.png](ejercicio-03.png) |
| **04** | Contador binario en máquina de Turing ($O(m)$ amortizado) | [ejercicio-04.md](ejercicio-04.md) | [ejercicio-04.py](ejercicio-04.py) | [ejercicio-04.png](ejercicio-04.png) |
| **05** | Detección de ciclos con dos punteros (Floyd) | [ejercicio-05.md](ejercicio-05.md) | [ejercicio-05.py](ejercicio-05.py) | [ejercicio-05.png](ejercicio-05.png) |
| **06** | Búsqueda en matriz ordenada por filas y columnas y adversario | [ejercicio-06.md](ejercicio-06.md) | [ejercicio-06.py](ejercicio-06.py) | [ejercicio-06.png](ejercicio-06.png) |
| **07** | Mediana de dos arreglos ordenados en $O(\log n)$ | [ejercicio-07.md](ejercicio-07.md) | [ejercicio-07.py](ejercicio-07.py) | [ejercicio-07.png](ejercicio-07.png) |
| **08** | Elementos con frecuencia $> n/3$ (Boyer-Moore con dos candidatos) | [ejercicio-08.md](ejercicio-08.md) | [ejercicio-08.py](ejercicio-08.py) | [ejercicio-08.png](ejercicio-08.png) |
| **09** | Mezcla "optimizada" y contraejemplo por adversario | [ejercicio-09.md](ejercicio-09.md) | [ejercicio-09.py](ejercicio-09.py) | [ejercicio-09.png](ejercicio-09.png) |
| **10** | Par más cercano en 1D: reducción $\Omega(n \log n)$ y rejilla $O(n)$ | [ejercicio-10.md](ejercicio-10.md) | [ejercicio-10.py](ejercicio-10.py) | [ejercicio-10.png](ejercicio-10.png) |
| **11** | Mochila 0/1 ($O(nW)$), tamaño en bits y complejidad pseudopolinomial | [ejercicio-11.md](ejercicio-11.md) | [ejercicio-11.py](ejercicio-11.py) | [ejercicio-11.png](ejercicio-11.png) |
| **12** | Gale-Shapley con listas incompletas | [ejercicio-12.md](ejercicio-12.md) | [ejercicio-12.py](ejercicio-12.py) | [ejercicio-12.png](ejercicio-12.png), [ejercicio-12-anim.gif](ejercicio-12-anim.gif) |
| **13** | Camino splay accedido en orden | [ejercicio-13.md](ejercicio-13.md) | [ejercicio-13.py](ejercicio-13.py) | [ejercicio-13.png](ejercicio-13.png) |
| **14** | Ciclo completo sobre búsqueda de un pico local (1D y 2D) | [ejercicio-14.md](ejercicio-14.md) | [ejercicio-14.py](ejercicio-14.py) | [ejercicio-14.png](ejercicio-14.png), [ejercicio-14-anim.gif](ejercicio-14-anim.gif), [ejercicio-14.html](ejercicio-14.html) |

---

## Declaración de uso de herramientas de IA

En cumplimiento de la política del curso (Conferencia 1, sección 10: *"Puedes usar herramientas de IA para implementar algoritmos, generar casos de prueba y depurar, y tienes que declarar que las usaste. Las demostraciones de correctitud, los análisis de complejidad, las cotas mínimas, las reducciones y las garantías de aproximación o probabilísticas se escriben a mano"*), declaro el uso de IA:

1. **Interfaz interactiva en HTML/CSS/JavaScript ([`ejercicio-14.html`](ejercicio-14.html)):** maquetación de las tres pestañas interactivas, renderizado en SVG del árbol de decisión sobre la familia unimodal $U_k$ y controles de simulación paso a paso para el problema del pico en 1D y 2D.
2. **Código de trazado gráfico con `matplotlib` y baterías de casos de prueba en los scripts `.py`:** generación de los gráficos multipanel (`.png`), animaciones cuadro a cuadro (`.gif`) y arneses de verificación automática contra oráculos.