---
date: 2026-09-28
type: know-how
when: escribir, revisar o volver a renderizar las notas de una conferencia de DAA 2026, desde el outline hasta el PDF publicado
---

# Escribiendo una conferencia

Qué entra en cada conferencia lo fija `Lectures/2026/plan.md`. Cómo se dibujan las
figuras está en [ilustrando-una-conferencia](ilustrando-una-conferencia.md). Este
documento cubre lo que queda entre los dos: cómo se escribe una conferencia y cómo se
publica. Salió de las conferencias 2 y 3, que son los ejemplos trabajados.

## El camino

1. **`outline.md` primero, y se aprueba antes de redactar.** Lleva la idea de la
   clase, la estructura por secciones, los ejercicios, la tabla de audios y una
   lista final de **decisiones que quiero confirmar**. Esa lista es donde van las
   dudas de alcance y las afirmaciones que todavía no tienen fuente.
2. **Verificar antes de escribir el outline.** Toda afirmación sobre casos pequeños
   ("con dos símbolos el atajo nunca falla") se comprueba por enumeración con un
   script en `.playground/`. Toda cita (autor, año, resultado) se busca en la fuente
   primaria. Lo que no se pudo verificar no entra en las notas: queda en la lista de
   decisiones, y si nadie lo pide, se cae.
3. **`notas.md` según el outline aprobado.** Después se renderiza y se verifica como
   dice el documento de figuras. Al terminar, la línea `Estado:` del outline pasa a
   "aprobado y redactado".
4. **Commit del directorio completo:** `outline.md`, `notas.md`, `notas.css` (copia de
   la de la conferencia anterior) y `notas.pdf`. La caché `.scriptorium/` no se sube.

## Cómo está hecha una sección

Cada sección tiene el tamaño de un audio de unos 5 minutos. Una demostración larga
puede ocupar dos. Dentro de una sección, el orden es este:

- **Dónde estamos.** El problema o el paso del ciclo, en una o dos frases.
- **Un ejemplo chico antes de la prueba.** Una fila de votos a mano, una traza de
  $4 \times 4$, el mejor caso y el peor caso. La demostración formaliza algo que el
  estudiante ya vio pasar.
- **Cómo se le ocurre a uno**, cada vez que aparece un algoritmo. Casi siempre
  arranca por el intento que falla primero, y el fallo motiva el paso siguiente. En
  la conferencia 2, la franja que vuelve a $n^2$. En la 3, el invariante verdadero
  que no es inductivo y la reparación de parejas que cicla.
- **La demostración**, marcando el paso que todo el mundo se salta.
- **Código que se ejecuta y mide.** Nunca pseudocódigo. Cada algoritmo se prueba
  contra un oráculo de fuerza bruta.

## Lo que lleva cada conferencia

- **Un error plantado.** Es una variante del algoritmo que parece correcta, junto con
  la medición de qué baterías de pruebas no la atrapan: 1 vecino en lugar de 7 en la
  conferencia 2, y el atajo del contador en la 3. La prosa dice qué parte de la
  demostración anunciaba el error. Es la manera de mostrar para qué sirve demostrar,
  en vez de afirmarlo.
- **El experimento antes de la demostración.** Un invariante con `assert`, un barrido
  de constantes, una traza. El experimento propone el enunciado y la demostración
  decide si es cierto. Las dos cosas van en las notas.
- **Conexiones con nombre y número.** Hacia atrás, con las conferencias anteriores y
  con lo que el plan asume de Estructuras de Datos. Hacia adelante, con la
  conferencia del plan donde la idea vuelve ("la conferencia 4 usa la palabra
  potencial para otra cosa").
- **Un cierre que es una regla**, no un índice. En la conferencia 2 es "una cota
  mínima viene con un modelo pegado". En la 3 es la tabla de qué error atrapa cada
  herramienta.
- **Resumen en viñetas**, una por cosa que hay que recordar.
- **Ocho ejercicios.** Incluyen lo que se sacó del cuerpo de la clase (compañeros de
  cuarto), un "construye la entrada que lo rompe" y un "¿y si cambio esta hipótesis?".

Las conferencias 2 y 3 salieron entre 5 400 y 6 000 palabras con el código, lo que
son unos 40 minutos de audio. El outline lleva una tabla que reparte las secciones en
audios de unos 5 minutos, para que el guion de grabación salga de ahí.

## Voz

Se tutea al estudiante ("fíjate", "hazlo a mano"). Los términos técnicos van en
español cuando existe el término ("pareja bloqueante", "potencial"), con el nombre
en inglés solo si el estudiante lo va a buscar así. Los nombres de los personajes son
neutros: proponentes y receptores, no hombres y mujeres. Cada número que aparece en
la prosa es uno que imprime el código del propio documento.

## Tocar una conferencia ya publicada

Una conferencia publicada tiene lectores que citan páginas, y audios que citan
páginas y números. Para cambiarla hay tres reglas:

- **Renderizar con la caché puesta, y saber qué invalida.** Un bloque sale de
  `.scriptorium/freeze.json` solo si ni él ni **ningún bloque anterior de su cadena**
  cambió. Cambiar un bloque, aunque sea solo el texto del pie de una figura, obliga a
  volver a correr todos los bloques `continue` que vienen después, y los tiempos se
  miden de nuevo. Pasó el 2026-09-29: corregir el pie de dos figuras de la sección 6
  de la conferencia 2 cambió 1,254 s por 1,766 s y 0,706 s por 0,847 s en las
  secciones 7 y 9, que son números que citan los audios. Borrar `.scriptorium`
  produce el mismo efecto sobre el documento entero. Si una corrección se puede hacer
  en prosa, fuera de los bloques, hazla ahí.
- **Si hubo que tocar un bloque, restaurar las mediciones publicadas.** La caché
  acumula entradas y no borra las viejas. Antes de renderizar, copia
  `freeze.json`. Después del render, cada bloque que se volvió a medir tiene dos
  entradas con el mismo tipo de salida: la vieja (más arriba en el dict, en el orden
  de inserción) y la nueva (de las últimas). Búscalas por un texto de su salida
  (`"1.254s"`, `'id="fig-tiempos"'`), copia la salida vieja sobre la clave nueva y
  renderiza otra vez. Después comprueba que los números sean idénticos a los de la
  versión publicada, y compara píxel a píxel (`pdftoppm` y `cmp`) las páginas con
  figuras que dependen de mediciones.
- **Comparar el mapa de páginas antes y después:**

  ```bash
  for p in $(seq 1 $(pdfinfo notas.pdf | awk '/Pages/{print $2}')); do
    pdftotext -f $p -l $p notas.pdf - |
      grep -E '^[0-9]+\. [A-ZÁÉÍÓÚ][a-zá-ú]|^Figura [0-9]+\.' | sed "s/^/p$p /"
  done
  ```

  Se corre sobre la copia publicada y sobre la nueva, y se hace `diff`. Lo que se
  movió se le dice a quien publica, porque es lo que tiene que corregir en el canal.
- **Comparar los números medidos.** Se extraen las tablas de salida de las dos
  versiones con `pdftotext -layout` y se comparan. Una diferencia que no sea solo de
  espaciado significa que se re-midió algo.

Un párrafo nuevo a mitad de la conferencia 2 movió dos cosas de página, las dos
después del párrafo. Ninguna de las páginas que citaban los audios cambió, y eso se
supo gracias al `diff`.
