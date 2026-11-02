# Ejercicio 2: búsqueda binaria (invariante, potencial y cota de información)

Enunciado : Da el invariante y el potencial de la búsqueda binaria, y la cota de información que la hace óptima.

El script `ejercicio-02.py` comprueba el invariante, el potencial y la cota para todos los n de 1 a 200.

## 1. El algoritmo

Tenemos un arreglo A ordenado con n elementos distintos y un valor x. El algoritmo solo puede comparar x con elementos de A, y cada comparación responde <, = o >. El costo es la cantidad de comparaciones (este es el modelo de comparaciones).

```python
def busqueda_binaria(A, x):
    lo, hi = 0, len(A)
    while lo < hi:
        m = (lo + hi) // 2
        if x == A[m]:
            return ("está", m)
        if x < A[m]:
            hi = m
        else:
            lo = m + 1
    return ("hueco", lo)
```

Si x no está, devuelve el hueco donde cabría (hueco i quiere decir entre A[i-1] y A[i]). Un ejemplo con A = [10, 20, 30, 40, 50, 60, 70] y x = 45:

```
lo = 0, hi = 7, p = 7, m = 3, A[m] = 40   (x > 40, lo = 4)
lo = 4, hi = 7, p = 3, m = 5, A[m] = 60   (x < 60, hi = 5)
lo = 4, hi = 5, p = 1, m = 4, A[m] = 50   (x < 50, hi = 4)
lo = 4, hi = 4, p = 0  -> x cae en el hueco 4
```

## 2. Invariante

Invariante:todos los elementos de A[:lo] son menores que x y todos los de A[hi:] son mayores que x.

De aquí se saca lo anterior: lo que queda afuera de A[lo:hi] es distinto de x, así que si x está, tiene que estar adentro.

 Al empezar lo = 0 y hi = n, y A[:0] y A[n:] están vacíos. Se cumple.

 Supongamos que se cumple antes de una vuelta y miramos A[m]:
- Si x == A[m], devolvemos m y terminamos.
- Si x < A[m], como A está ordenado, todo lo que está de m en adelante es mayor que x. Al hacer hi = m, el invariante sigue valiendo (lo de la izquierda no cambió).
- Si x > A[m], todo lo que está hasta m es menor que x. Al hacer lo = m + 1, también sigue valiendo.

Al terminar si salió por x == A[m], devuelve la posición correcta. Si salió porque lo = hi, el invariante dice que todo lo de la izquierda de lo es menor que x y todo lo que está desde lo es mayor, así que x no está y cae en el hueco lo, que es lo que devuelve. Esto prueba que la respuesta es correcta si el algoritmo termina.

## 3. Potencial

El potencial es **p = hi - lo**, el tamaño del rango donde todavía puede estar x. Es un entero que no es negativo (el ciclo solo sigue si p > 0).

En cada vuelta p baja, porque m queda dentro del rango y lo descartamos:
- si x < A[m], el nuevo rango es [lo, m), que tiene p // 2 elementos,
- si x > A[m], el nuevo rango es [m+1, hi), que tiene a lo sumo p // 2 elementos.

Entonces p baja siempre, y un entero no negativo no puede bajar para siempre, así que el algoritmo termina.

Además, en cada vuelta el rango se reduce por lo menos a la mitad. En el ejemplo de arriba, p fue 7, 3, 1, 0. Si empezamos con n, después de k vueltas queda a lo sumo n / 2^k, y p llega a 0 cuando 2^k > n. Eso pasa a más tardar en la vuelta número log2(n) + 1 (redondeando log2(n) hacia abajo), que es igual a ceil(log2(n+1)). Comprobación: con n = 7 son 3 vueltas y con n = 8 son 4.

Como cada vuelta hace una sola comparación,la búsqueda binaria hace a lo sumo ceil(log2(n+1)) comparaciones.

## 4. Costo

- **Tiempo:** por la sección 3 hay a lo sumo ceil(log2(n+1)) vueltas. Cada vuelta hace una comparación y una cantidad constante de operaciones más (calcular m y cambiar lo o hi), que son operaciones con índices menores que n y cuestan O(1). Entonces la búsqueda binaria cuesta a lo sumo ceil(log2(n+1)) comparaciones, o sea **O(log n)**. En el mejor caso cuesta 1 comparación (x está justo en el medio), y en el peor caso exactamente ceil(log2(n+1)).
- **Memoria:** solo guarda lo, hi, m y x, sin copiar el arreglo. Son **O(1)** celdas extra, sin importar n.

Comparado con recorrer el arreglo de punta a punta, que cuesta O(n) comparaciones, la búsqueda binaria es muchísimo más rápida: con n = 1000 son 10 comparaciones contra hasta 1000.

## 5. Cota de información

Probar que ningún algoritmo que solo compare puede hacerlo con menos.

Primero un ejemplo pequeño. Sea A un arreglo con 3 elementos y supongamos que x no está en A. Entonces x cae en uno de 4 huecos(antes del primero, entre cada par de vecinos, o después del último). Cada comparación le dice al algoritmo si x es menor o mayor que un elemento de A, o sea una respuesta con dos opciones. Veamos cuántos huecos se pueden separar con cada cantidad de comparaciones:

```
comparaciones   secuencias de respuestas posibles     huecos que se pueden separar
      1         <, >                                  2
      2         <<, <>, ><, >>                        4
      3         8 secuencias                          8
```

Con 1 comparación solo se pueden separar 2 huecos, y hay 4, así que no alcanza. Con 2 comparaciones hay 4 secuencias, justo para los 4 huecos. Entonces para n = 3 hacen falta 2 comparaciones, que es ceil(log2(4)).

En general, cada comparación duplica la cantidad de secuencias de respuestas que pueden darse, así que con k comparaciones hay a lo sumo 2^k secuencias distintas. Si hay más de 2^k huecos, dos de ellos reciben las mismas respuestas y el algoritmo no los puede diferenciar (en 5.2 se ve por qué sí los tiene que diferenciar). Por tanto hace falta que 2^k sea al menos la cantidad de huecos.

¿Por qué solo miro los x que no están? Una comparación puede dar tres respuestas (<, = o >), no dos. Pero "=" solo puede salir cuando x está en A. Si miro solo los x que no están, "=" nunca aparece y cada comparación tiene dos respuestas, como en el ejemplo. Esto es válido porque la cota es para el peor caso: si con algunos x el algoritmo ya necesita k comparaciones, entonces en el peor caso necesita al menos k.
 
Por distincion de casos :

Si x no está, cae en uno de los n + 1 huecos: antes del primero, entre cada par de vecinos, o después del último. Hay que ver que el algoritmo tiene que diferenciar todos estos casos.

Supongamos que dos valores x1 y x2 que caen en huecos distintos reciben exactamente las mismas respuestas durante toda la ejecución. Entre sus dos huecos hay un elemento a de A con x1 < a < x2. El algoritmo nunca comparó con a (si lo hubiera hecho, x1 habría recibido "<" y x2 ">", y las respuestas serían distintas). Entonces, si buscamos x = a, recibe las mismas respuestas que x1 y x2 en todas las comparaciones y el algoritmo dice "no está", cuando a sí está. El algoritmo se equivoca.

Por tanto, cada uno de los n + 1 huecos tiene que terminar con una secuencia de respuestas distinta.


Con k comparaciones y dos respuestas posibles en cada una hay a lo sumo 2^k secuencias de respuestas distintas. Necesitamos al menos n + 1, entonces:

```
2^k >= n + 1   =>   k >= log2(n+1)   =>   k >= ceil(log2(n+1))
```

(k es un entero, por eso se redondea hacia arriba.) Esto vale para el peor caso de cualquier algoritmo que solo compare.


La búsqueda binaria hace a lo sumo ceil(log2(n+1)) comparaciones y ningún algoritmo puede hacer menos. Las dos cotas son iguales, así que la búsqueda binaria es óptima y su costo en el peor caso es exactamente ceil(log2(n+1)).

## 6. Resultados del script

El script prueba, para cada n, todos los valores x posibles (los que están y todos los huecos). En cada vuelta comprueba con `assert` el invariante y que p baje (y quede en la mitad o menos). Después mide el peor caso:

```
    n  huecos  cota  peor caso  2^cota
    1       2     1          1       2
    2       3     2          2       4
    3       4     2          2       4
    4       5     3          3       8
    7       8     3          3       8
    8       9     4          4      16
   15      16     4          4      16
   16      17     5          5      32
  100     101     7          7     128
 1000    1001    10         10    1024

Para todo n de 1 a 200: peor caso = ceil(log2(n+1))
```

El peor caso medido siempre es igual a la cota. Además 2^cota siempre es mayor o igual que n + 1, o sea que alcanzan las secuencias de respuestas para todos los huecos.

## 7. Respuesta final

- **Invariante:** todos los elementos de A[:lo] son menores que x y todos los de A[hi:] son mayores que x.
- **Potencial:** p = hi - lo, que se reduce al menos a la mitad en cada vuelta.
- **Costo:** O(log n) comparaciones en el peor caso (exactamente ceil(log2(n+1))) y O(1) de memoria extra.
- **Cota de información:** hay n + 1 huecos que el algoritmo tiene que distinguir, y con k comparaciones de dos respuestas solo se distinguen 2^k casos. Entonces hacen falta al menos ceil(log2(n+1)) comparaciones.

**Conclusión:** como el costo de la búsqueda binaria coincide con la cota inferior, ningún algoritmo que compare puede buscar en un arreglo ordenado con menos comparaciones. Por ejemplo, con n = 1000 elementos alcanzan 10 comparaciones, y con 9 es imposible.
