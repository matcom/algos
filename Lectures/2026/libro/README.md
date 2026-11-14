# El libro de Diseño y Análisis de Algoritmos

Las conferencias del curso 2026 se publican como un solo libro, con cada conferencia
como un capítulo: el capítulo N es la conferencia N de `../plan.md`. Este directorio es
el proyecto de [scriptorium](https://github.com/gia-uh/scriptorium) que lo construye.
Hay dos salidas:

- `daa.pdf`, el libro completo. Se construye en local y se sube al repositorio.
- `sitio/`, la documentación en línea. La construye el workflow `libro` en cada push a
  `main` y la publica en <https://matcom.github.io/algos/>, con el PDF al lado.

El libro tiene tres partes. Cada una abre con una página (`parte-N.md`) y cierra con un
resumen de ideas: `../tema-1/resumen.md`, `../resumen-parte-2/notas.md` y
`../resumen-parte-3/notas.md`. Al final va el epílogo, `../24-epilogo/notas.md`.

## Agregar o cambiar un capítulo

El procedimiento completo, con el formato y la comprobación por capítulo, está en
`know-how/escribiendo-un-capitulo-del-libro.md`. En corto:

1. El capítulo vive en `Lectures/2026/<NN>-<tema>/notas.md` y empieza con
   `# Título {#chap-<tema>}`, sin frontmatter. El número lo pone el libro. En el texto,
   las referencias van como "el capítulo N, §M".
2. Sus figuras nuevas van en `Lectures/2026/figuras_NN.py`, con ids prefijados por el
   slug del capítulo.
3. Agrégalo a `files:` en `scriptorium.yaml`, en su lugar.
4. Los bloques de código corren con este directorio como directorio de trabajo, y el
   primer bloque de cada capítulo pone `..` (`Lectures/2026`) en `sys.path`.
5. Construye y verifica, como dice la sección siguiente.
6. Sube el capítulo, `daa.pdf` y `.scriptorium/freeze.json`.

## Construir

Hace falta scriptorium 0.14.0 con el extra `pdf`, y `uv` para el intérprete de los
bloques (Python 3.14 con tesserax):

```bash
uv tool install --force 'scriptorium[pdf] @ git+https://github.com/gia-uh/scriptorium@v0.14.0'
cd Lectures/2026/libro
scriptorium render scriptorium.yaml          # daa.pdf y sitio/
```

Después:

```bash
pdftotext daa.pdf - | grep -ci traceback     # los que el texto muestra a propósito
pdftotext daa.pdf - | grep -c '^Figura '     # una por figura
```

Un bloque que falla no rompe el render: scriptorium pinta el traceback dentro del libro.
Por eso hay que contar los tracebacks.

Construye siempre en local antes de subir a `main`: el push publica el sitio.

## La caché

`.scriptorium/freeze.json` guarda la salida de cada bloque, con su código como clave.
Se sube al repositorio por dos razones: los capítulos ya publicados conservan sus
números al reconstruir, y el sitio que construye el workflow muestra los mismos tiempos
que el PDF. Editar la prosa no vuelve a correr nada. Editar un bloque lo vuelve a
correr, a él y a los bloques `continue` que vienen después. La caché no ve `figuras.py`
ni `figuras_NN.py`: después de cambiar una figura, borra de `freeze.json` las entradas
de los bloques que la dibujan.

Los tiempos que miden los capítulos dependen de la carga de la máquina. Si un capítulo
se vuelve a medir, hay que comprobar que la prosa siga diciendo lo que imprimen sus
bloques.

## Lo que el libro ajusta del tema

`libro.css` pone en español las etiquetas del tema `book` y hace que una referencia a
una figura diga "figura N" en el PDF; `html-refs:` en `scriptorium.yaml` hace lo mismo en
el sitio. El sitio toma su idioma de `lang: es`.
