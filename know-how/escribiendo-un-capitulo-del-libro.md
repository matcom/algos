---
date: 2026-11-13
type: know-how
when: agregar, cambiar o comprobar un capítulo del libro de DAA 2026 (Lectures/2026/libro), sus figuras o sus referencias cruzadas, o reconstruir y publicar el libro
---

# Escribiendo un capítulo del libro

Las conferencias de 2026 se publican como un libro: el capítulo N es la conferencia N
de `Lectures/2026/plan.md`. Cómo se escribe una conferencia (outline, voz, error
plantado, experimento) está en [escribiendo-una-conferencia](escribiendo-una-conferencia.md),
y cómo se dibuja una figura en [ilustrando-una-conferencia](ilustrando-una-conferencia.md).
Este documento cubre lo que cambia cuando la conferencia es un capítulo del libro.
Cómo se construye el libro entero está en `Lectures/2026/libro/README.md`.

## El formato de libro

- `notas.md` empieza con `# Título {#chap-<slug>}`, sin frontmatter, sin "Conferencia N:"
  en el título y sin el bloque `::: meta`. El número lo pone el libro.
- En la prosa se dice "el capítulo N" y "este capítulo", nunca "la conferencia N" ni
  "esta clase". "Conferencia" solo aparece cuando se habla del curso. Una sección se
  cita como "el capítulo 2, §7", y lo citado tiene que estar en esa sección.
- El primer bloque es el de preparación, invisible (`echo=false output=asis`), y hace
  `sys.path.insert(0, os.path.abspath(".."))`. Así el capítulo corre igual desde su
  carpeta de comprobación y desde `libro/`, que son hermanas de las carpetas de
  capítulo.
- Al final van `## Resumen`, en viñetas, y `## Ejercicios`, con al menos diez
  ejercicios numerados. El enunciado no trae la respuesta.
- No se sube un `notas.pdf` por capítulo. El PDF del libro, `daa.pdf`, lo construye el
  CI y se publica en <https://matcom.github.io/algos/daa.pdf>; el de un capítulo suelto
  sale de su comprobación (abajo).

## Las figuras: `figuras_NN.py`

Las figuras nuevas del capítulo NN van en `Lectures/2026/figuras_NN.py` (dos dígitos),
que importa de `figuras` lo que necesite (`from figuras import _figura`). No se edita
`figuras.py` para un solo capítulo. Cada figura recibe el estado que calculó el código
del capítulo, no números escritos a mano.

`_figura(canvas, ident, pie)` antepone `fig-` al `ident`. El `ident` lleva el slug del
capítulo como prefijo (`ident="fft-mariposa"`, citado `@fig-fft-mariposa`), porque en
el libro todos los ids comparten un espacio y dos capítulos con `fig-arbol` chocan.

## La comprobación: `_check-NN`

Un capítulo se comprueba solo antes de entrar al libro. Crea
`Lectures/2026/_check-NN/` (está en `.gitignore`) con este `check.yaml`:

```yaml
theme: book
lang: es
css: ../libro/libro.css
vars:
  title: "Comprobación"
  figure-label: "Figura"
  figure-ref-label: "figura"
execute:
  timeout: 600
  interpreters:
    python: ["uv", "run", "--quiet", "--python", "3.14", "--with", "tesserax", "python", "-"]
files:
  - ../NN-<slug>/notas.md
outputs:
  pdf:
    format: pdf
    file: notas.pdf
```

Desde `_check-NN/`:

```bash
rm -rf .scriptorium && scriptorium render check.yaml     # lee el código de salida directo
pdftotext notas.pdf - | grep -ci traceback                # 0, salvo los que el texto muestra a propósito
pdftotext notas.pdf - | grep -c '^Figura '                # las figuras que pusiste
pdftoppm -r 60 -png notas.pdf /tmp/cap-NN/p               # mira cada página con figura
```

La caché no ve los módulos: después de tocar `figuras_NN.py`, borra `.scriptorium`
otra vez. Cada número que cita la prosa tiene que aparecer en la salida del PDF.

## Entrar al libro

1. Agrega el capítulo a `files:` de `libro/scriptorium.yaml`, en su lugar.
2. Construye el sitio en `libro/` (`scriptorium render scriptorium.yaml --only sitio`)
   y cuenta tracebacks y figuras, como dice su README. Comprueba también que ningún id
   de figura ni de capítulo se repita. El PDF completo necesita unos 3,5 GB de memoria:
   constrúyelo con `--only libro` solo en una máquina que los tenga.
3. Sube el capítulo, su `figuras_NN.py` y `libro/.scriptorium/freeze.json` en el mismo
   commit. `daa.pdf` no se sube: lo construye el CI.

Construye siempre el sitio en local antes del push: el push a `main` publica el sitio y
el PDF, y un bloque que falla en el workflow sale con su traceback en la web.

Los tiempos que mide un capítulo dependen de la carga de la máquina. La caché conserva
los que se revisaron; si un bloque cambia y se vuelve a medir, relee la prosa que cita
esos números.
