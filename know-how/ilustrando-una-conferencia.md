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

Las llevan contadores de CSS, no números a mano. En `notas.css`:

```css
body { counter-reset: figura; }
figure { counter-increment: figura; margin: 5mm 0; text-align: center; }
figure svg { display: block; margin: 0 auto; }
figcaption { text-align: center; }
figcaption::before { content: "Figura " counter(figura) ". "; font-weight: 600; }
a.ref-fig::after { content: "figura " target-counter(attr(href url), figura); }
```

En la prosa, `@fig-empaquetamiento` resuelve a "figura 5" y funciona en las dos
direcciones, también hacia adelante. El `id` lo pone `figuras._figura`, que envuelve
el SVG en `<figure id="fig-…">` con su `<figcaption>`. **Ningún tema de scriptorium numera
figuras**: `base` da estilo a `figure` y `figcaption`, y el `a.ref-fig` de `book`
renderiza el texto del pie más el número de página, no un número de figura. El
esquema de contadores de arriba es nuestro, así que hay que copiarlo en el CSS de
cada conferencia hasta que alguien lo suba a `base`.

Tampoco sirve sacar la paleta del CSS: medido el 2026-09-25, WeasyPrint no resuelve
`currentColor` ni `var(--acento)` dentro de un SVG en línea, los dos caen a negro.
Los colores tienen que ir como hex literal en el Python.

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
