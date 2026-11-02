# Solución Ejercicio 3

La idea sería (para que la operación mínimo cueste O(1) en el peor caso) es que la pila siempre sepa cuál es el mínimo en el momento que entró un nuevo elemento.

Tenemos nuestra pila S donde en cada posición tendremos un par de elemento: el valor v y el mínimo m de todos los valores en cuanto v entró a la pila lo cual sería (v,m)


class PilaMinimo:
    def __init__(self):
        self.S = []

    def push(self, x):
        if not self.S:
            m = x
        else:
            m = min(x, self.S[-1][1])

        self.S.append((x, m))

    
    def pop(self):
        return self.S.pop()[0]

    def tope(self):
        return self.S[-1][0]

    def minimo(Self):
        return self.S[-1][1]

Vamos a plantear nuestra Invariante "I":

I => toda posición i de la pila, con S[i] = (v_i, m_i), se cumple que m_i = minimo(v_0, v_1, ... , v_i )

Podemos observar que es inductivo ya que cada operación lo conserva sin suponer ninguna otra información sobre nuestra pila.

Inicialización:
----------------

La pila inicia vacía, así que I se cumple 

Actualización:
--------------

- push(x): las posiciones ya existentes no cambian por lo que siguen cumpliendo I. La nueva posición i, guarda m = min(x, m_(i-1)). Por lo planteado en I, en i-1, m_(i-1) = min(v_0, ..., v_(i-1)), luego al añadir x m = min(v_0, ..., v_(i-1), x) = min(v_0, ..., v_i).
Si la pila al inicio está vacía m = x.

- pop(): este quita la última posición. Cada m_i depende de las posiciones que son menores o iguales a él, así que las restantes posiciones siguen cumpliendo I.

- tope(): no modifica nada en la pila

- minimo(): no modifica nada en la pila

Por lo tanto si la pila no está vacía, el tope es la posición t y por I m_t = min(v_0, ..., v_t) que es el mínimo de toda la pila. Esto es lo que devuelve minimo(). Además, pop y tope son correctos porque v se guarda sin modificar.

Costo:
------

---------------------------------------------------------------------------------
Operación | Costo |    Why?                                                     |
--------------------------------------------------------------------------------|
push      |  O(1) | una comparación, una lectura del tope, una escritura final |
pop       |  O(1) | una lectura , un borrado al final                           |
tope      |  O(1) | una lectura                                                 |
minimo    |  O(1) | una lectura                                                 |
---------------------------------------------------------------------------------

