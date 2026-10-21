# Ejercicio 12: Gale-Shapley con listas incompletas

## Enunciado

**Ejercicio 12 ($`\star\star\star`$; C3).** Gale-Shapley con listas incompletas: cada proponente lista solo a algunos receptores, y prefiere quedarse solo antes que con uno que no listó. Adapta el algoritmo, su potencial y la definición de pareja bloqueante. ¿Sigue siendo estable el resultado? Demuéstralo.

## Respuesta corta

- **Modelo:** $`n`$ proponentes y $`m`$ receptores ($`n\ne m`$ permitido); $`L_a`$ es la lista ordenada de receptores aceptables para $`a`$ y $`L_b`$ la de proponentes aceptables para $`b`$. El par $`(a,b)`$ es *aceptable* si $`b\in L_a`$ y $`a\in L_b`$. El enunciado (solo los proponentes incompletos) es el caso $`L_b=A`$.

- **Algoritmo:** un proponente libre propone al siguiente de su lista; si la agota, queda solo para siempre; un receptor rechaza a quien no lista, y si no, se queda con el mejor entre el actual y el nuevo.

- **Potencial:** $`\Phi=\#\{(a,b):b\in L_a,\ a\text{ no le propuso a }b\}`$, con $`\Phi_0=\sum_a|L_a|`$, baja $`1`$ por propuesta: a lo sumo $`\sum_a|L_a|`$ propuestas.

- **Estabilidad:** *estable* $`=`$ individualmente racional $`+`$ sin pares bloqueantes. Sí, el resultado es estable, para cualquier orden de ejecución; en la demostración de C3 §8 hay un caso nuevo (el proponente que queda solo porque agotó su lista) y se resuelve igual.

- **Más fuerte:** cada proponente obtiene su *mejor pareja válida* (y queda solo si no tiene ninguna), demostrado con el primer fallo de C3 §9; y el teorema de los hospitales rurales (el conjunto de emparejados es el mismo en todo emparejamiento estable), demostrado en pocas líneas a partir de la optimalidad y de su reverso (la pesimalidad para los receptores) y comprobado exhaustivamente en $`4000`$ instancias.

Modelo: word RAM; la entrada son las listas, de tamaño $`\sum_a|L_a|+\sum_b|L_b|`$.

## Modelo

Notación de C3 §6–9. Hay *proponentes* $`a\in A`$, $`|A|=n`$, y *receptores* $`b\in B`$, $`|B|=m`$; no se pide $`n=m`$. Cada proponente $`a`$ tiene una lista estricta $`L_a\subseteq B`$, ordenada de mejor a peor: son los receptores *aceptables* para $`a`$. Cada receptor $`b`$ tiene una lista estricta $`L_b\subseteq A`$ de proponentes aceptables. Si $`b\notin L_a`$, $`a`$ prefiere quedarse solo antes que con $`b`$; igual para $`a\notin L_b`$.

**Aceptabilidad mutua.** El par $`(a,b)`$ es *aceptable* si $`b\in L_a`$ *y* $`a\in L_b`$. Solo los pares aceptables pueden formar parte de un emparejamiento razonable. Casos particulares: el *caso del enunciado* es $`L_b=A`$ para todo $`b`$ (los receptores lo listan todo), en el que $`(a,b)`$ es aceptable si y solo si $`b\in L_a`$; el caso de C3 son además $`n=m`$ y $`L_a=B`$.

Un *emparejamiento* $`\mathcal M`$ asigna a cada proponente a lo sumo un receptor y a cada receptor a lo sumo un proponente; $`\mathcal M(a)`$ es la pareja de $`a`$ ($`\varnothing`$ si está solo). $`a`$ *prefiere* $`b`$ a $`b'`$ si $`b`$ va antes que $`b'`$ en $`L_a`$.

## Las definiciones nuevas

1.  **Individualmente racional (IR):** todo par $`(a,\mathcal M(a))`$ de $`\mathcal M`$ es aceptable (nadie queda con alguien que no lista, ni con alguien que no lo lista a él).

2.  **Pareja bloqueante:** un par $`(a,b)`$ *mutuamente aceptable*, no emparejado entre sí, tal que (i) $`a`$ está solo o prefiere $`b`$ a $`\mathcal M(a)`$, y (ii) $`b`$ está solo o prefiere $`a`$ a $`\mathcal M(b)`$.

3.  **Estable:** $`\mathcal M`$ es IR y no tiene parejas bloqueantes.

En C3 con listas completas todo par es aceptable y IR vale gratis; la pareja bloqueante de C3 §6 es el caso en que $`a`$ y $`b`$ están emparejados con otros.

**Por qué hace falta (a).**

Sea $`A=\{a_1\}`$, $`B=\{b_1\}`$, con $`L_{a_1}=\varnothing`$ (no lista a nadie) y $`L_{b_1}=\{a_1\}`$. El emparejamiento $`\{a_1\!-\!b_1\}`$ *no tiene ninguna pareja bloqueante* en el sentido ingenuo: el único par posible ya está emparejado. Pero empareja a $`a_1`$ con alguien que no listó, y $`a_1`$ prefiere quedarse solo. No es estable. El emparejamiento vacío sí lo es (el único par no es mutuamente aceptable). La salida 2 lo muestra con el verificador. Sin la condición (a), la definición de estabilidad aprobaría emparejamientos donde alguien está peor que solo.

## El algoritmo adaptado

``` python
def gale_shapley(La, Lb):                       # La[a], Lb[b]: listas ordenadas (los aceptables)
    n, m = len(La), len(Lb)
    rango = [{a: lugar for lugar, a in enumerate(Lb[b])} for b in range(m)]   # solo los que b lista
    sig = [0] * n                                # a que lugar de su lista va a proponer a
    pareja_de_b = [None] * m
    libres = deque(a for a in range(n) if La[a])
    propuestas = 0
    while libres:
        a = libres.popleft()
        b = La[a][sig[a]]; sig[a] += 1; propuestas += 1
        actual = pareja_de_b[b]
        if a not in rango[b]:                    # b rechaza a quien no lista
            acepta = False
        elif actual is None or rango[b][a] < rango[b][actual]:
            acepta = True                        # libre, o prefiere a "a" a su pareja actual
        else:
            acepta = False
        if acepta:
            pareja_de_b[b] = a
            if actual is not None and sig[actual] < len(La[actual]):
                libres.append(actual)            # el desplazado vuelve a proponer...
        elif sig[a] < len(La[a]):
            libres.append(a)                     # ...si le quedan receptores en su lista
        # si agota su lista queda solo para siempre: no vuelve a la cola
    return pareja_de_b, propuestas
```

Las adaptaciones respecto a C3 §7: (1) la lista de $`a`$ es $`L_a`$ y puede ser vacía o corta; (2) un proponente solo vuelve a la cola si le quedan receptores en su lista, y si agota la lista *queda solo para siempre*; (3) el receptor rechaza a quien no lista; (4) el resto es igual: libre acepta, ocupado se queda con el mejor entre su pareja y el nuevo. El orden de los proponentes libres sigue siendo arbitrario.

**Una traza**

($`n=4`$, $`m=3`$; salida 1):

| proponente | lista $`L_a`$   | receptor | lista $`L_b`$   |
|:-----------|:----------------|:---------|:----------------|
| $`a_1`$    | $`b_1>b_2>b_3`$ | $`b_1`$  | $`a_2>a_3>a_1`$ |
| $`a_2`$    | $`b_1>b_3`$     | $`b_2`$  | $`a_1>a_4`$     |
| $`a_3`$    | $`b_1>b_2`$     | $`b_3`$  | $`a_1`$         |
| $`a_4`$    | $`b_2`$         |          |                 |

| paso | propone | a | tenía | resultado |
|---:|:---|:---|:---|:---|
| 1 | $`a_1`$ | $`b_1`$ | – | acepta |
| 2 | $`a_2`$ | $`b_1`$ | $`a_1`$ | acepta ($`a_1`$ queda libre) |
| 3 | $`a_3`$ | $`b_1`$ | $`a_2`$ | rechaza |
| 4 | $`a_4`$ | $`b_2`$ | – | acepta |
| 5 | $`a_1`$ | $`b_2`$ | $`a_4`$ | acepta ($`a_4`$ libre, pero ya agotó su lista: queda solo) |
| 6 | $`a_3`$ | $`b_2`$ | $`a_1`$ | rechaza ($`b_2`$ no lista a $`a_3`$; $`a_3`$ agotó su lista y queda solo) |

Resultado: $`a_1\!-\!b_2`$, $`a_2\!-\!b_1`$, $`a_3`$ y $`a_4`$ solos, $`b_3`$ sin pareja: $`6`$ propuestas, contra $`\sum|L_a|=8`$. El único emparejamiento estable, enumerando los $`73`$ posibles, es este.

## Terminación: el potencial

Sea $`\Phi`$ el número de pares $`(a,b)`$ con $`b\in L_a`$ tales que $`a`$ todavía no le propuso a $`b`$: $`\Phi=\sum_a(|L_a|-\texttt{sig}[a])`$. Al principio $`\Phi_0=\sum_a|L_a|`$. Cada vuelta del ciclo es *exactamente una propuesta*, a un receptor al que $`a`$ no le había propuesto (`sig`$`[a]`$ solo avanza), así que $`\Phi`$ baja en exactamente $`1`$. Y $`\Phi\ge0`$ siempre: un proponente solo está en la cola si `sig`$`[a]<|L_a|`$, de modo que `La[a][sig[a]]` existe. Entonces el ciclo termina después de a lo sumo $`\sum_a|L_a|`$ propuestas. Cuando termina, nadie está libre en la cola: todo proponente está emparejado o agotó su lista (ya no tiene a quién proponerle).

**Cota exacta y la identidad.**

Un proponente $`a`$ propone en el orden de su lista y se detiene al ser aceptado por última vez; si termina emparejado con $`\mathcal M(a)`$, hizo exactamente $`\mathrm{lugar}_a(\mathcal M(a))`$ propuestas (su posición en $`L_a`$, desde $`1`$), y si termina solo, hizo $`|L_a|`$. Entonces
``` math
\#\text{propuestas}=\sum_{a\text{ solo}}|L_a|+\sum_{a\text{ emparejado}}\mathrm{lugar}_a(\mathcal M(a))\ \le\ \sum_a|L_a| ,
```
con igualdad si y solo si todo proponente queda solo o con el *último* de su lista. La salida 3 comprueba la identidad en $`4000`$ instancias. Dos instancias en que se alcanza (salida 4): si ningún receptor lista a nadie, todos quedan solos y hay $`\sum|L_a|=7`$ propuestas; y con $`a_1\!:\![b_1,b_2]`$, $`a_2\!:\![b_1]`$, $`b_1\!:\!a_2>a_1`$, $`b_2\!:\!a_1`$ el resultado empareja a $`a_1`$ con el último de su lista y a $`a_2`$ con el único, y hay $`3=\sum|L_a|`$ propuestas. Con listas completas $`n\times n`$ la cota del potencial es $`n^2`$ y el máximo medido sobre *todas* las instancias es $`n^2-n+1`$ ($`3`$ para $`n=2`$, $`7`$ para $`n=3`$).

**Costo.**

Con la tabla `rango[b]` (un diccionario por receptor, que cuesta $`\sum_b|L_b|`$ en construirse), cada propuesta es $`O(1)`$ y el total es $`O\bigl(n+m+\sum_a|L_a|+\sum_b|L_b|\bigr)`$: lineal en el tamaño de la entrada.

## ¿Sigue siendo estable? Sí

Tres invariantes, que se demuestran leyendo el código:

1.  (receptores) Un receptor $`b`$, una vez que acepta a alguien, *nunca vuelve a quedar libre*, y su pareja solo cambia por alguien que prefiere. Su pareja solo mejora.

2.  (proponentes) $`a`$ propone solo a receptores de $`L_a`$ y en orden decreciente de preferencia: cada vez que queda libre sigue desde donde estaba, y sus parejas solo empeoran.

3.  (aceptabilidad) Todo par $`(a,b)`$ que se forma es mutuamente aceptable: $`b\in L_a`$ porque $`a`$ solo propone a su lista ($`I_2`$), y $`a\in L_b`$ porque $`b`$ rechaza a quien no lista.

**Teorema 1**. *El emparejamiento que devuelve el algoritmo es estable, para cualquier orden de ejecución.*

*Demostración.* *(a) IR.* Es $`I_3`$: el emparejamiento final solo contiene pares formados durante la ejecución, y todos son mutuamente aceptables.

*(b) Sin pares bloqueantes.* Por contradicción. Sea $`\mathcal M`$ el resultado y sea $`(a,b)`$ una pareja bloqueante: mutuamente aceptable, $`a`$ solo o prefiriendo $`b`$ a $`\mathcal M(a)`$, y $`b`$ solo o prefiriendo $`a`$ a $`\mathcal M(b)`$.

*Paso 1: $`a`$ le propuso a $`b`$.* Hay dos casos, y el segundo es el nuevo.

- *$`a`$ está emparejado con $`b'=\mathcal M(a)`$ y prefiere $`b`$ a $`b'`$.* Como propone en orden decreciente ($`I_2`$) y terminó con $`b'`$, le propuso a $`b`$, que va antes, antes que a $`b'`$.

- *$`a`$ está solo.* Al terminar el algoritmo nadie queda libre con lista pendiente, así que $`a`$ agotó su lista: le propuso a *todos* los receptores de $`L_a`$, y $`b\in L_a`$ porque $`(a,b)`$ es aceptable. Le propuso a $`b`$.

*Paso 2: $`b`$ lo rechazó.* Como $`a`$ le propuso a $`b`$ y no está emparejado con él al final, en algún momento $`b`$ rechazó a $`a`$, al recibir la propuesta o más tarde cuando lo cambió por alguien mejor. $`b`$ lista a $`a`$ (aceptabilidad), así que no fue un rechazo por “no listado”: $`b`$ rechazó a $`a`$ porque tenía, o pasó a tener, una pareja que prefiere a $`a`$.

*Paso 3: contradicción.* Por $`I_1`$, desde ese momento $`b`$ no vuelve a quedar libre y su pareja solo mejora. Entonces al final $`\mathcal M(b)`$ es una pareja que $`b`$ prefiere a $`a`$ (o es la misma que lo reemplazó). Pero $`b`$ estaba solo o prefería $`a`$ a $`\mathcal M(b)`$: contradicción. ◻

**Corolario.** Toda instancia con listas incompletas, aunque $`n\ne m`$ y los receptores también tengan listas incompletas, tiene un emparejamiento estable, y el algoritmo lo encuentra. El caso nuevo (proponente solo) no cambia nada porque “agotó su lista” hace que haya propuesto a todos los que podrían bloquear.

## Algo más fuerte

### Optimalidad para quien propone (el primer fallo de C3 §9)

**Definición.** Un receptor $`b`$ es *pareja válida* de $`a`$ si existe algún emparejamiento estable donde $`a`$ y $`b`$ están juntos. $`b^*(a)`$ es la pareja válida que $`a`$ prefiere.

**Teorema 2**. *En toda ejecución, cada proponente $`a`$ con alguna pareja válida queda emparejado con $`b^*(a)`$, y un proponente sin parejas válidas queda solo.*

*Demostración.* Basta ver que *ningún proponente es rechazado nunca por una pareja válida*. Supongamos que sí, y sea el primer rechazo de ese tipo en el tiempo: $`b`$ rechaza a $`a`$, con $`b`$ pareja válida de $`a`$, así que existe un estable $`\mathcal M'`$ con $`\mathcal M'(a)=b`$. $`b`$ rechaza a $`a`$ a cambio de $`a'`$ (al llegar la propuesta de $`a'`$ o al desplazar a $`a`$): $`a'`$ le propuso a $`b`$ y $`b`$ prefiere $`a'`$ a $`a`$; $`b\in L_{a'}`$ y $`a'\in L_b`$ (si no, $`b`$ no lo habría aceptado), de modo que $`(a',b)`$ es aceptable.

*Qué sabemos de $`a'`$.* $`a'`$ le propuso a $`b`$, así que antes fue rechazado por todos los receptores que prefiere a $`b`$. Esos rechazos son anteriores al nuestro, que es el primero hecho por una pareja válida, así que ninguno de ellos es pareja válida de $`a'`$. En $`\mathcal M'`$, $`a'`$ o está solo, o está con $`\mathcal M'(a')\ne b`$ (porque $`b`$ está con $`a`$), que es pareja válida de $`a'`$ (pues $`\mathcal M'`$ es estable) y por tanto *no* es uno de los que $`a'`$ prefiere a $`b`$: $`a'`$ prefiere $`b`$ a $`\mathcal M'(a')`$. En los dos casos $`a'`$ prefiere $`b`$ a lo que tiene en $`\mathcal M'`$.

*Qué sabemos de $`b`$.* En $`\mathcal M'`$, $`b`$ está con $`a`$, y prefiere $`a'`$ a $`a`$.

Entonces $`(a',b)`$, mutuamente aceptable, es una pareja bloqueante de $`\mathcal M'`$, que era estable. Contradicción.

Con eso: $`a`$ propone en orden decreciente y nunca es rechazado por una pareja válida, de modo que llega a $`b^*(a)`$ (los anteriores no son válidos) y $`b^*(a)`$ no lo rechaza ni lo desplaza (sería un rechazo por pareja válida): queda con $`b^*(a)`$. Si $`a`$ no tiene parejas válidas, no puede quedar emparejado: el resultado es estable (teorema 1) y su pareja sería válida. ◻

Consecuencias: el resultado *no depende del orden de ejecución* (porque $`b^*(a)`$ no depende de él), y los $`b^*(a)`$ forman un emparejamiento estable.

### Los hospitales rurales: el mismo conjunto de emparejados

Sea $`\mathcal M_0`$ el resultado del algoritmo. El *teorema de los hospitales rurales* (Gale y Sotomayor; Roth) dice que el conjunto de agentes emparejados es el mismo en todos los emparejamientos estables. Sale en pocas líneas de la optimalidad. Primero, el lema que aporta el lado de los receptores (es el reverso de la optimalidad, el ejercicio 5 de C3):

**Lema 1** (pesimalidad para los receptores). *Sea $`\mathcal M`$ un emparejamiento estable cualquiera y $`b`$ un receptor emparejado en $`\mathcal M_0`$, con $`a=\mathcal M_0(b)`$. Entonces $`b`$ está emparejado en $`\mathcal M`$ y prefiere $`\mathcal M(b)`$ a $`a`$, o lo iguala. Es decir, en $`\mathcal M_0`$ cada receptor emparejado queda con su *peor* pareja válida.*

*Demostración.* Supongamos que no: $`b`$ prefiere $`a=\mathcal M_0(b)`$ a $`\mathcal M(b)`$, o $`b`$ está solo en $`\mathcal M`$. Como $`\mathcal M_0(a)=b`$ y $`a`$ tiene una pareja válida, el teorema 2 da $`b=b^*(a)`$, la mejor pareja válida de $`a`$. En $`\mathcal M`$, $`a`$ está solo, o está con $`\mathcal M(a)`$, que es pareja válida de $`a`$ (porque $`\mathcal M`$ es estable) y distinta de $`b`$ (si $`\mathcal M(a)=b`$ sería $`\mathcal M(b)=a`$, y $`b`$ no preferiría $`a`$ a $`\mathcal M(b)`$). En los dos casos $`a`$ prefiere $`b=b^*(a)`$ a lo que tiene en $`\mathcal M`$. Y $`b`$ prefiere $`a`$ a $`\mathcal M(b)`$, o está solo. El par $`(a,b)`$ es mutuamente aceptable ($`\mathcal M_0`$ es IR, teorema 1). Entonces $`(a,b)`$ es una pareja bloqueante de $`\mathcal M`$, que era estable. Contradicción. ◻

**Teorema 3** (hospitales rurales). *Para todo emparejamiento estable $`\mathcal M`$, los mismos proponentes y los mismos receptores están emparejados en $`\mathcal M`$ y en $`\mathcal M_0`$.*

*Demostración.* Sean $`P(\mathcal M)`$ y $`R(\mathcal M)`$ los proponentes y receptores emparejados en $`\mathcal M`$, con $`|P(\mathcal M)|=|R(\mathcal M)|=|\mathcal M|`$.

1.  *Proponentes.* Si $`a\in P(\mathcal M)`$, $`\mathcal M(a)`$ es pareja válida de $`a`$; por la optimalidad (teorema 2) $`a`$ queda emparejado en $`\mathcal M_0`$. Entonces $`P(\mathcal M)\subseteq P(\mathcal M_0)`$ y $`|\mathcal M|\le|\mathcal M_0|`$.

2.  *Receptores.* Si $`b\in R(\mathcal M_0)`$, por el lema 1 $`b`$ está emparejado en $`\mathcal M`$. Entonces $`R(\mathcal M_0)\subseteq R(\mathcal M)`$ y $`|\mathcal M_0|\le|\mathcal M|`$.

3.  *Conteo.* De (i) y (ii), $`|\mathcal M|=|\mathcal M_0|`$. Como $`P(\mathcal M)\subseteq P(\mathcal M_0)`$ y tienen el mismo número de elementos, $`P(\mathcal M)=P(\mathcal M_0)`$; igual $`R(\mathcal M)=R(\mathcal M_0)`$.

 ◻

La verificación exhaustiva (sección 7) es la comprobación: en las $`4000`$ instancias, el conjunto de emparejados es el mismo en todos los estables, y la pesimalidad del lema 1 se cumple en todos.

## Comprobación experimental

Código: `ej12_gale_shapley.py`. El verificador de estabilidad es independiente del algoritmo (construye sus propios rangos y mira los $`n\cdot m`$ pares). La fuerza bruta enumera *todos* los emparejamientos parciales (hasta $`1546`$ para $`n=m=5`$) y se queda con los estables. Salida real:

<details>
<summary><code>ej12_salida.txt</code></summary>

```text
=== 1. Una instancia con n != m, listas incompletas, y su traza ===
  a1 lista: b1 > b2 > b3
  a2 lista: b1 > b3
  a3 lista: b1 > b2
  a4 lista: b2
  b1 lista: a2 > a3 > a1
  b2 lista: a1 > a4
  b3 lista: a1
  paso  a  propone a  tenia   se queda con  que pasa
     1  a1         b1      -           a1  acepta
     2  a2         b1     a1           a2  acepta
     3  a3         b1     a2           a2  rechaza
     4  a4         b2      -           a4  acepta
     5  a1         b2     a4           a1  acepta
     6  a3         b2     a1           a1  rechaza
  resultado: a1-b2, a2-b1, a3 solo, a4 solo (6 propuestas; suma |L_a| = 8)
  verificador independiente: individualmente racional = True, pares bloqueantes = []
  emparejamientos estables (fuerza bruta, 73 emparejamientos posibles): [['a1-b2', 'a2-b1', 'a3 solo', 'a4 solo']]

=== 2. Por que hace falta la racionalidad individual (a) ===
  a lista: (nadie); b lista: a1. Emparejamiento {a1-b1}: racional = False, pares bloqueantes en el sentido ingenuo = []
  Sin pares bloqueantes, pero a1 queda con alguien que no lista: no es estable. El vacio {a1 solo, b1 solo} si lo es: (True, [])
  Algoritmo sobre esa instancia: ([None], 0)

=== 3. Experimento principal: instancias aleatorias pequenas (n, m <= 5), TODOS los emparejamientos enumerados ===
  4000 instancias (3253 con n != m, 1000 con receptores de lista completa, 333 con emparejamiento vacio)
  (i)   el resultado de Gale-Shapley es estable (verificador independiente):                4000 de 4000
  (ii)  el resultado no depende del orden (cola, pila, dos azares; mismo M y mismas propuestas): 4000 de 4000
  (iii) optimo para quien propone (mejor pareja estable, o solo si no tiene ninguna):          4000 de 4000
  (iv)  hospitales rurales: mismo conjunto de emparejados en TODO emparejamiento estable:       4000 de 4000
  (iv') pesimalidad: en M0 cada receptor emparejado queda con su PEOR pareja valida (en todo estable lo iguala o mejora): 4000 de 4000
  (v)   propuestas = sum_{a solo} |L_a| + sum_{a emparejado} lugar de su pareja:                4000 de 4000
  (vi)  propuestas <= sum |L_a|:                                                               4000 de 4000

=== 4. Propuestas contra sum |L_a|: instancias grandes y la igualdad ===
      n     m  sum |L_a|  propuestas  cociente  proponentes solos
     50    50       2500         169     0.068                  0
     50    50        755         338     0.448                  7
    200   100       9879        7337     0.743                100
    100   200      10059         304     0.030                  0
    400   400      16010        2164     0.135                  0
    400   400      16088        7297     0.454                 67
  Igualdad propuestas = sum |L_a|: sucede exactamente cuando todo proponente queda solo o con el ULTIMO de su lista.
  (a) receptores con listas vacias: nadie acepta; propuestas 7 = sum |L_a| = 7
  (b) con emparejamientos: a1:[b1,b2], a2:[b1]; b1: a2>a1; b2: a1 -> M = [1, 0], propuestas 3 = sum |L_a| = 3 (a1 con el ultimo de su lista, a2 con el unico)
  Complejidad con listas completas (n x n), peor caso sobre TODAS las instancias de n = 2, 3:
    n=2: maximo de propuestas = 3  (n^2 - n + 1 = 3; la cota del potencial es n^2 = 4)
    n=3: maximo de propuestas = 7  (n^2 - n + 1 = 7; la cota del potencial es n^2 = 9)

=== 5. Verificar el teorema de los hospitales rurales a mano: un ejemplo con varios estables ===
  instancia 2x2 con dos estables: [['a1-b1', 'a2-b2'], ['a1-b2', 'a2-b1']]; Gale-Shapley: [0, 1]

=== 6. Variantes con error que parecen correctas ===
  V1 (el receptor acepta a quien no lista 'porque es mejor que estar solo'): instancia mas chica hallada: n=1, m=1
     listas a: [[0]], listas b: [[]]; resultado [0]: individualmente racional = False, bloqueantes = []
     instancia minima: a lista [b], b no lista a nadie: resultado [0] -> racional = False (b queda con un no listado)
     en 3000 instancias aleatorias, la variante no es estable en 1624 (54.1 %)
  V2 (el proponente que agoto su lista la reinicia): a lista [b], b no lista a nadie -> NO TERMINA (propuestas hechas: 5000, tope de pasos 5000)
     con una instancia donde el original termina (M = [1, 0]), la variante: [1, 0] (3 propuestas)
     en 500 instancias aleatorias pequenas, la variante no termina en 304 (60.8 %): el potencial ya no baja
     con listas COMPLETAS (el caso de la conferencia) ningun proponente agota su lista y la variante nunca se activa:
     500 de 500 instancias completas: la variante coincide con el original
```

</details>

**Casos elegidos.**

*Bordes:* lista vacía (el proponente queda solo desde el principio), receptor que no lista a nadie, $`n\ne m`$ ($`3253`$ de las $`4000`$ instancias), receptores de lista completa ($`1000`$, el caso del enunciado), emparejamiento vacío ($`333`$). *Típicas:* listas aleatorias con probabilidades de listado $`0{,}4`$ a $`1`$. *Adversariales:* las variantes con error de la sección siguiente.

## Variantes con error que parecen correctas

**V1: el receptor acepta a quien no lista “porque es mejor que estar solo”.**

Parece razonable (más emparejamientos, nadie queda solo). Rompe $`I_3`$ y por tanto (a): la instancia mínima es $`n=m=1`$ con $`L_a=[b]`$ y $`L_b=\varnothing`$. La variante empareja $`a`$ con $`b`$, que no lista a $`a`$; el emparejamiento no es IR. En $`3000`$ instancias aleatorias, la variante no es estable en $`1624`$ ($`54{,}1`$ %). La demostración lo anuncia: “$`a\in L_b`$ porque $`b`$ rechaza a quien no lista” es la mitad de $`I_3`$.

**V2: el proponente que agota su lista la reinicia.**

Parece razonable (“no se rinde”). Rompe la terminación: sin proponentes que quedan solos, $`\Phi`$ ya no baja en cada propuesta (se rehabilitan pares ya propuestos). La instancia mínima es $`n=m=1`$ con $`L_a=[b]`$ y $`L_b=\varnothing`$: $`a`$ le propone a $`b`$, $`b`$ lo rechaza, $`a`$ reinicia, … y no termina (la ejecución se corta a las $`5000`$ propuestas). En $`500`$ instancias aleatorias pequeñas no termina en $`304`$ ($`60{,}8`$ %). Con listas *completas* ($`n=m`$) la variante nunca se activa, porque ningún proponente agota su lista (queda emparejado antes), y coincide con el original en las $`500`$ instancias: es el caso en que las pruebas de C3 no la verían.

## Por qué este enfoque

**Una analogía.**

El mercado de residencias de C3, con hospitales rurales: algunos médicos solo aceptan ciertas plazas y algunos hospitales solo aceptan ciertos médicos. Un hospital que dice “no acepto a ese médico” se lo dice aunque tenga la plaza vacía; un médico que agotó su lista se queda sin plaza antes que aceptar un hospital que no listó. La estabilidad con (a) es: “nadie queda con alguien a quien no aceptaría, y nadie tiene un trato mejor que le acepten”.

**Otra visión.**

Las listas incompletas son listas completas donde *quedarse solo* es un elemento más: se lista a los aceptables y el resto va “después de estar solo” (inaceptable). Entonces “IR” es “nadie queda por debajo de estar solo”, y “pareja bloqueante con alguien solo” es la pareja bloqueante de C3 con ese elemento extra. Eso explica por qué (a) no es un capricho: es la comparación con la opción de no emparejarse.

**Por qué estos invariantes.**

$`I_1`$ y $`I_2`$ son los de C3 sin cambio; $`I_3`$ es el único nuevo y es lo que reemplaza “todos son aceptables” de las listas completas. El caso nuevo de la demostración, el proponente que queda solo, se cubre con la terminación: “agotó su lista” significa que propuso a todos los de $`L_a`$, incluido el $`b`$ del posible par bloqueante.

## Conclusión

- **Modelo:** $`n`$ proponentes, $`m`$ receptores, listas $`L_a`$, $`L_b`$ incompletas, pares aceptables si ambos se listan; el enunciado es $`L_b=A`$.

- **Algoritmo y potencial:** $`\Phi=\#`$ pares (listado, no propuesto), $`\Phi_0=\sum|L_a|`$, baja $`1`$ por propuesta: $`\le\sum_a|L_a|`$ propuestas, con la identidad exacta “solos: $`|L_a|`$; emparejados: el lugar de su pareja”.

- **Definiciones:** IR; pareja bloqueante entre mutuamente aceptables con “solo o prefiere”; estable $`=`$ IR $`+`$ sin bloqueantes.

- **Estabilidad:** sí, con $`I_1`$, $`I_2`$, $`I_3`$ y el argumento de C3 §8; el proponente solo queda cubierto por su lista agotada.

- **Más fuerte:** cada proponente obtiene su mejor pareja válida (primer fallo); hospitales rurales demostrado (optimalidad $`+`$ pesimalidad para receptores $`+`$ conteo) y verificado exhaustivamente.

- **Variantes:** el receptor que acepta a un no listado rompe IR ($`n=m=1`$); el proponente que reinicia su lista rompe la terminación.

Modelo: word RAM; tamaño de la entrada $`\sum_a|L_a|+\sum_b|L_b|`$.
