---
date: 2026-09-25
type: know-how
when: añadir, cambiar o depurar una figura de una conferencia; una figura sale en crudo como texto, se pinta 1000×1000, cae fuera de la página, o el bloque que la dibuja revienta con un NameError
---

# Ilustrando una conferencia

Las figuras se dibujan con [tesserax](https://github.com/apiad/tesserax) y se
imprimen dentro del documento de scriptorium. El módulo compartido es
`Lectures/2026/figuras.py`; la conferencia 2 es el ejemplo trabajado completo.

## El camino, en una frase

Un bloque de código de scriptorium escupe su stdout y **se re-parsea como
Markdown**; el HTML crudo pasa verbatim como una unidad atómica de la galera. Por
eso `print(str(canvas))` de tesserax entra al PDF como SVG vectorial, sin ficheros
intermedios y sin protocolo de figuras.

## La valla y el frontmatter

````markdown
---
theme: note
css: notas.css
execute:
  interpreters:
    python: ["uv", "run", "--quiet", "--with", "tesserax", "python", "-"]
---

```{python continue echo=false output=asis}
print(F.empaquetamiento(ident="empaquetamiento", pie="…"))
```
````

Las tres partes son obligatorias y cada una arregla un fallo concreto:

- **`output=asis`**. Sin él scriptorium escapa la salida y el SVG sale impreso como
  texto dentro de un `<pre>`.
- **`echo=false`**. Sin él el documento enseña el código que dibuja la figura, que
  no es lo que el estudiante viene a leer.
- **El intérprete `uv run --with tesserax`**. El `python3` del sistema está marcado
  como *externally managed* (PEP 668) y no acepta `pip install tesserax`. `uv run
  --with` resuelve el paquete en un entorno efímero y cacheado: con la caché
  caliente el arranque son 0.13 s por bloque, medidos.

## Numeración y referencias cruzadas

Las lleva scriptorium desde `adb91d1`. El tema `base` numera cualquier `<figure>` que
lleve `id="fig-…"` —el mismo id al que apunta `@fig-…`— y rellena la referencia en
las dos direcciones, también hacia adelante. Una `<figure>` sin ese id no se toca.

En el frontmatter, dos variables:

```yaml
vars:
  figure-label: "Figura"        # abre el pie: "Figura 5. El rectángulo…"
  figure-ref-label: "figura"    # va dentro de una frase: "el de la figura 5"
```

Son dos y no una porque en inglés "Figure 5" sirve en los dos sitios y en español no:
un pie abre una frase y una referencia va a mitad de otra. `figure-ref-label` cae a
`figure-label` si no se declara.

El `id` lo pone `figuras._figura`, que envuelve el SVG en `<figure id="fig-…">` con su
`<figcaption>`. En el CSS local no hace falta ningún contador; queda solo la
apariencia, que aquí es una línea:

```css
figure[id^="fig-"] { margin: 5mm 0; text-align: center; }
```

Antes de `adb91d1` no numeraba ningún tema y cada documento se escribía sus propios
contadores. Si te encuentras un `counter-reset: figura` en el CSS de una conferencia
vieja, bórralo: con la regla de `base` encima, el pie sale numerado dos veces.

Lo que sigue sin poderse hacer por CSS es el color. Medido el 2026-09-25, WeasyPrint
no resuelve `currentColor` ni `var(--acento)` dentro de un SVG en línea, los dos caen
a negro. La paleta tiene que ir como hex literal en el Python.

## La regla que hace que una figura no pueda mentir

**Una figura que ilustra un algoritmo recibe el estado que el algoritmo calculó.**
No se colocan puntos a mano. La figura de la franja recibe el `δ`, la franja y los
pares de cada mitad que salieron de correr el código; la de la rejilla recibe el
diccionario de celdas; las dos gráficas reciben los tiempos y las reconstrucciones
que el propio documento acaba de medir, por la variable `tiempos` que arranca en el
bloque de preparación. Una figura dibujada a mano puede contradecir al código de la
conferencia y nadie se entera hasta que lo nota un estudiante.

Corolario: las figuras 5 y 6 comparten `figuras.rectangulo_extremo()`, así que el
argumento de empaquetamiento y el orden por `y` son la misma configuración vista dos
veces, y no pueden desincronizarse.

## Las trampas, en el orden en que muerden

**El bloque de preparación va primero en el fichero.** Los bloques marcados
`continue` reejecutan en silencio todos los bloques anteriores de la cadena, y un
`continue` sin nada delante avisa (`continue block has no earlier python block`) y
corre solo. Si una figura de la sección 2 usa `random`, `random` tiene que importarse
antes de la sección 2, no en la sección 4 donde el estudiante lo ve. La solución es
un bloque invisible al principio del documento que importe `math`, `os`, `random`,
`sys` y `time`, meta `..` en `sys.path` e importe `figuras`.

**Una figura no puede usar una función que se define más abajo.** La figura de la
franja vive en la sección 5 y `_rec` se escribe en la sección 7. Calcular el `δ` de
cada mitad por fuerza bruta da el mismo número que devuelve la recursión en el primer
nivel, y además encaja con la narración: en la sección 5 todavía no hemos escrito el
algoritmo.

**El coste del render crece con el cuadrado de la cadena.** Cada `continue`
reejecuta todo lo anterior, así que un bucle de medición caro se paga una vez por
cada bloque posterior. La conferencia 2 tarda 1 m 25 s en frío y unos 35 s con la
caché de `freeze` caliente. Si se dispara, hay que bajar los tamaños de los bucles de
medición, no partir la cadena.

**El caché de `freeze` no ve `figuras.py`.** La clave del caché es el código del
bloque más el intérprete, no los módulos que el bloque importa. Editas una figura,
renderizas, y scriptorium devuelve rc=0 y un PDF **idéntico**. Comprobado el
2026-09-25 con un módulo de una línea: primer render "VERSIÓN UNO", edito el módulo a
"VERSIÓN DOS", segundo render "VERSIÓN UNO", borro `.scriptorium/freeze.json`, tercer
render "VERSIÓN DOS". Es el patrón de
[checks-that-cannot-fail](../../../vault/Atlas/Know-how/checks-that-cannot-fail.md)
en estado puro: el render verde no depende de lo que dice medir.

**Después de tocar `figuras.py`, `rm -rf .scriptorium` antes de renderizar.** Si no,
estás mirando el PDF de antes. Durante el trabajo de la conferencia 2 me salvó la
casualidad de que casi siempre editaba también el `.md` en el mismo paso, lo que sí
invalida el bloque.

**Un bloque sin marca corta la cadena.** Medido: bloque 1 define una variable, bloque
2 va sin `continue`, bloque 3 con `continue` y revienta con `NameError`. `continue`
reejecuta "los bloques desde el último sin marca", así que un bloque suelto en medio
deja huérfano todo lo anterior. Consecuencia práctica: **en un documento con cadena,
todas las figuras tienen que ir con `continue`**, aunque no necesiten nada de antes.
No se pueden mezclar figuras autosuficientes y bloques encadenados.

La condición de seguridad: **la regla vale mientras ningún bloque sin marca caiga
entre un `continue` y las definiciones que ese `continue` necesita.** Con cadenas de
dos o tres bloques se cumple casi siempre sin pensarlo; con una cadena larga se rompe
en cuanto metes un diagrama en medio.

Eso hace que la elección sea de documento, no de figura. Si todos tus bloques son
independientes —como las conferencias de Programación, donde cada uno se lee solo—
lo barato es que cada figura haga su propio `import figuras` y no encadenar nada: son
0.13 s de `uv run` por figura en vez de arrastrar la reejecución. Si tus figuras
necesitan el estado que calculó un bloque anterior, como aquí, la cadena es
obligatoria y el coste se paga.

**`uv run` no usa el Python del sistema.** Medido: `uv run --with tesserax` resuelve
3.13.1 y este zion corre 3.14.4. Si las notas imprimen trazas de error, o prometen
ser la versión que se usa en clase, hay que fijarla: `"--python", "3.14"` en el
intérprete del frontmatter.

**`canvas.fit(padding)` va después del `with`, nunca dentro.** Dentro no hay formas
que medir todavía y el SVG sale con `width="1000" height="1000"`.

**El `cwd` del bloque es el directorio del documento.** Por eso
`sys.path.insert(0, os.path.abspath(".."))` alcanza `Lectures/2026/`. No hace falta
ruta absoluta.

**Un bloque que revienta no rompe el render.** scriptorium pinta el traceback en
rojo dentro del PDF y sigue. Es un buen modo de fallo, pero significa que hay que
mirar el PDF: `pdftotext notas.pdf - | grep -ci traceback` tiene que dar 0.

## Verificar una figura

Renderizar no es comprobar. La secuencia que uso:

```bash
rm -rf .scriptorium                  # si tocaste figuras.py, el caché no lo ve
scriptorium render notas.md          # leer el rc directo, nunca por un pipe
pdftotext notas.pdf - | grep -ci traceback     # 0
pdftotext notas.pdf - | grep -c '^Figura '     # el número de figuras que esperas
pdftoppm -r 82 -png notas.pdf /tmp/x/p         # y mirar las páginas
```

Para iterar sobre varias figuras a la vez sale más barato una hoja de contacto: un
`.md` desechable en `.playground/` que importe `figuras` y las imprima todas
seguidas. Corregir colisiones de etiquetas a ojo es la mitad del trabajo, y en la
hoja de contacto cuesta 3 s por vuelta en vez de 85.

## Elegir la instancia que se dibuja

Una instancia aleatoria casi nunca ilustra lo que quieres. Medido para la
conferencia 2:

- Con 30 puntos uniformes el `δ` es tan pequeño que la franja es una raya invisible.
  Con 16 puntos y la semilla 1, `δ = 0.116` y la franja se ve, con 3 puntos dentro.
- En 2 400 instancias (4 tamaños × 600 semillas) **nunca** salió un par de la franja
  separado más de dos posiciones en el orden de `y`. Por eso la figura del orden por
  `y` usa la configuración extrema construida, y la prosa dice que lo es.
- La rejilla real es casi toda celdas vacías (9 ocupadas de unas 121), porque su lado
  es `δ/2`. La figura recorta una ventana alrededor del punto que se inserta, y el
  pie da los dos números, que es justo el argumento de por qué es una tabla hash.

Buscar la instancia con un script corto y dejar la semilla escrita en el documento
es más honesto que dibujar a mano lo que uno querría que pasara.
