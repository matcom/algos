# Ejercicio 4: contador binario en una máquina de Turing

**Enunciado.** Demuestra con un potencial que n incrementos desde 0 cuestan O(n) pasos en total, aunque uno solo pueda costar Θ(log n).

El script `ejercicio-04.py` simula la máquina de Turing y comprueba el costo de cada incremento, el potencial y el total para varios valores de n.

## 1. La máquina

Para poder contar pasos necesitamos la máquina concreta. Es una máquina de Turing de una cinta que le suma 1 a un número escrito en binario. Escribo el número con el bit menos significativo primero (a la izquierda), y pongo una marca `#` en la celda anterior para saber dónde termina la cinta por la izquierda. Después del último bit hay blancos (`_`). Por ejemplo, el número 6 (110 en binario) queda así:

```
# 0 1 1 _ _ ...
  ^
  cabezal (en el bit menos significativo)
```

El cabezal empieza en el bit menos significativo y tiene que volver a él al terminar. La máquina tiene dos estados principales:

| estado | lee | escribe | se mueve | nuevo estado |
|---|---|---|---|---|
| sumar | 1 | 0 | derecha | sumar |
| sumar | 0 | 1 | izquierda | volver |
| sumar | _ | 1 | izquierda | volver |
| volver | 0 o 1 | lo mismo | izquierda | volver |
| volver | # | # | derecha | fin |

La idea es la del acarreo normal: mientras haya unos, los cambia por ceros y avanza. Cuando encuentra un 0 (o un blanco, si el número crece un bit) lo cambia por 1. Después vuelve hacia la izquierda hasta la marca `#` y da un paso a la derecha para quedar en el bit menos significativo.

## 2. Costo de un incremento

Sea k la cantidad de unos que hay al final del número (los que están pegados al bit menos significativo). Por ejemplo, 3 = 11 tiene k = 2, y 4 = 001 (escrito al revés) tiene k = 0.

- Estado sumar: pasa por los k unos y por el 0 (o blanco) que sigue, o sea k + 1 pasos.
- Estado volver: recorre las k posiciones de los unos que cambió, y la marca `#`, o sea k + 1 pasos.

Entonces un incremento con k unos al final cuesta exactamente 2k + 2 pasos.

Ejemplo con 3 → 4 (k = 2):

```
# 1 1 _     sumar:  1->0, 1->0, _->1     (3 pasos)
# 0 0 1     volver: 0, 0, #              (3 pasos)     total 6 = 2*2 + 2
```

**El peor caso de un solo incremento.** Pasa cuando el número es todo unos. Con b bits en 1 (valor 2^b − 1) el costo es 2b + 2, que es **Θ(log n)** porque b es más o menos log2 del valor. Un solo incremento puede costar eso.


Si cada incremento cuesta como mucho Θ(log n), entonces n incrementos cuestan a lo sumo n · Θ(log n) = O(n log n). Esto es cierto, pero muy pesimista: para que un incremento sea caro hace falta que el número tenga muchos unos al final, y eso no puede pasar muy seguido. Después de un incremento caro, esos unos se volvieron ceros, y el siguiente incremento es barato. La idea del potencial es medir exactamente eso.

## 4. Potencial

Cada 1 en la cinta es trabajo que se va a tener que pagar después: cuando llegue un acarreo, ese 1 se cambia por 0, y eso cuesta dos pasos (uno al ir y otro al volver). Por eso defino:

> **Potencial:** Φ = 2 · (cantidad de unos en la cinta)

- Al principio la cinta tiene el número 0, que no tiene unos, así que Φ₀ = 0.
- Φ nunca es negativo.

**Costo amortizado de un incremento.** Con k unos al final, el incremento cambia k unos por ceros y un 0 (o blanco) por un 1. La cantidad de unos cambia en 1 − k, entonces:

```
ΔΦ = 2 · (1 − k) = 2 − 2k
costo amortizado = costo real + ΔΦ = (2k + 2) + (2 − 2k) = 4
```

La k se cancela.Cada incremento tiene costo amortizado 4, sin importar cuántos unos haya al final.



## 5. Costo total

Sean c_i el costo real del incremento i y Φ_i el potencial después de él. Como c_i + Φ_i − Φ_(i−1) = 4, al sumar los n incrementos los potenciales se cancelan:

```
c_1 + c_2 + ... + c_n = 4n − (Φ_n − Φ_0) = 4n − Φ_n ≤ 4n
```

porque Φ₀ = 0 y Φ_n ≥ 0. Entonces **n incrementos desde 0 cuestan a lo sumo 4n pasos, o sea O(n)**.

Además, Φ_n = 2 · s(n), con s(n) la cantidad de unos de n en binario. Entonces el total es exactamente **4n − 2·s(n)**.

(Es importante que Φ₀ = 0 y que Φ nunca baje de 0. Si el potencial pudiera terminar por debajo de donde empezó, la suma no demostraría nada.)

## 6. Resultados del script

El script simula la máquina paso a paso. Primero muestra los primeros incrementos, con el costo real, el potencial antes y después, y el costo amortizado:

```
 i->i+1  k  costo real  phi antes  phi despues  amortizado
   0->1  0           2          0            2           4
   1->2  1           4          2            2           4
   2->3  0           2          2            4           4
   3->4  2           6          4            2           4
   4->5  0           2          2            4           4
   5->6  1           4          4            4           4
   6->7  0           2          4            6           4
   7->8  3           8          6            2           4
```

Después hace n incrementos desde 0, comprobando con `assert` en cada uno que el costo real es 2k + 2 y que el costo amortizado es 4:

```
       n  pasos totales  4n - 2s(n)  pasos/n  mas caro  2*log2(n)+2
      10             36          36     3.60         8            8
     100            394         394     3.94        14           14
    1000           3988        3988     3.99        20           20
   10000          39990       39990     4.00        28           28
  100000         399988      399988     4.00        34           34
```

Se ve que:
- El total coincide exactamente con 4n − 2·s(n).
- Los pasos por incremento se acercan a 4 (nunca pasan de 4), aunque el incremento más caro crece como log n (para n = 100000, un solo incremento cuesta 34 pasos).

## 7. Respuesta final

- Un incremento: cuesta 2k + 2 pasos, donde k es la cantidad de unos al final. En el peor caso es Θ(log n).
- Potencial: Φ = 2 · (cantidad de unos), con Φ₀ = 0 y Φ ≥ 0.
- Costo amortizado: 4 por incremento.
- n incrementos desde 0: cuestan 4n − 2·s(n) ≤ 4n pasos, o sea O(n).

Conclusión: aunque un incremento pueda costar Θ(log n), no puede pasar muchas veces seguidas: para que cueste mucho hay que haber juntado muchos unos, y cada uno de esos unos se pagó con sus propias 2 monedas cuando se creó. Por eso n incrementos no cuestan O(n log n) sino O(n), con un promedio de menos de 4 pasos por incremento.
