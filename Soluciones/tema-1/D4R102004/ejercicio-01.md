# Ejercicio 1: una computadora mil veces más rápida

> ¿Cuánto crece el tamaño de entrada que se resuelve en una hora con un algoritmo Θ(n²)? ¿Y con uno Θ(n log n)? Estima los dos factores. (C1)

## Planteamiento

Sea p el presupuesto: la cantidad de operaciones que la máquina vieja hace en una hora. La máquina nueva hace 1000·p.

- n₁ es el tamaño más grande que se resuelve con la máquina vieja: costo(n₁) = p.
- n₂ es el tamaño más grande que se resuelve con la máquina nueva: costo(n₂) = 1000·p.
- El factor es f = n₂ / n₁: cuántas veces más grande es el problema que se puede resolver.

Ignoro las constantes del Θ: si el costo es c·g(n), la constante c aparece a los dos lados de costo(n₂) = 1000·costo(n₁) y se cancela.

## Caso n²

n₁² = p, así que n₁ = √p. Y n₂² = 1000·p, así que n₂ = √1000 · √p = √1000 · n₁.

**f = √1000 ≈ 31.6**, sin importar cuánto valga p. Si el problema crece 31.6 veces, el costo n² crece 31.6 × 31.6 ≈ 1000 veces

## Caso n log n


### Intuición con números

Si n₁ es un millón, su costo es 10⁶ · log₂ 10⁶ ≈ 10⁶ · 20 = 20 millones, y el presupuesto nuevo es 20 mil millones. Un problema mil veces más grande (mil millones) costaría 10⁹ · 30 = 30 mil millones: no alcanza. Al agrandar el problema, el logaritmo también crece (de 20 a 30), cada elemento sale más caro, y por eso el factor no llega a 1000. Alcanza para más o menos 20/30 de lo necesario: f ≈ 667.

### La ecuación del factor

Las dos condiciones son n₁·log n₁ = p y n₂·log n₂ = 1000·p, así que

n₂ · log n₂ = 1000 · n₁ · log n₁.

Sustituyendo n₂ = f·n₁ y usando log(f·n₁) = log f + log n₁:

f·n₁·(log f + log n₁) = 1000·n₁·log n₁

y simplificando n₁:

**f · log f = (1000 − f) · log n₁**

Tampoco se despeja f exacto, pero esta ecuación alcanza para acotarlo por arriba y por abajo.

### Cota de arriba: f < 1000

Como f > 1 (la máquina nueva resuelve problemas más grandes), log f > 0 y el lado izquierdo es positivo. Entonces el lado derecho también lo es, y como log n₁ > 0, tiene que ser 1000 − f > 0. **f < 1000.**

### Cota de abajo

Como f < 1000, log₂ f < log₂ 1000 ≈ 10. Cambiando log f por 10 en la ecuación, el lado derecho crece:

(1000 − f) · log n₁ < 10 · f

Pasando lo que tiene f a un lado: f · (10 + log n₁) > 1000 · log n₁, y dividiendo entre 10 + log n₁ > 0:

**f > 1000 · log n₁ / (log n₁ + 10)**

### Resultado

1000 · log n₁ / (log n₁ + 10) < f < 1000

Cuando n₁ crece, log n₁ / (log n₁ + 10) se acerca a 1, así que el factor aumenta acercándose a 1000, pero sin llegar nunca. A diferencia del caso n², el factor depende de n₁.

Con una máquina de 10⁹ operaciones por segundo durante una hora, p = 3.6 · 10¹², n₁ ≈ 10¹¹ y log₂ n₁ ≈ 36.5:

**785 < f < 1000**

| n₁ | log₂ n₁ | cota de abajo |
|---|---|---|
| mil | 10 | 500 |
| un millón | 20 | 667 |
| 10¹¹ (una hora) | 36.5 | 785 |

## Experimento

`ej01_crecimiento.py` busca el n más grande con costo(n) ≤ presupuesto para la máquina vieja y para la nueva:

```
 n log n: n1 = 9.857e+10  n2 = 7.801e+13  factor = 791.4
     n^2: n1 = 1.897e+06  n2 = 6.000e+07  factor = 31.6
```

El factor de n² coincide con √1000, y el de n log n, 791, cae dentro de las cotas, cerca de la de abajo.

## Conclusión

Con una máquina mil veces más rápida, el algoritmo cuadrático resuelve problemas solo 31.6 veces más grandes, siempre. El de n log n resuelve problemas casi 1000 veces más grandes (785 a 1000 veces para lo que cabe en una hora).

---
*Declaración de uso de IA: usé un asistente de IA (Claude) para escribir el código de experimentación, y como tutor (explicaciones, pistas y corrección de mi redacción). El análisis y las cotas son míos.*
