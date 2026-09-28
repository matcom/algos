# Diseño y Análisis de Algoritmos

Material de la asignatura Diseño y Análisis de Algoritmos de la carrera de Ciencia de
la Computación, en MatCom, Universidad de La Habana. El repositorio es público y lo
leen los estudiantes: las notas de conferencia, los problemas y las orientaciones de
proyecto se publican tal como están aquí.

## Para quién

- **Los estudiantes del curso**, que leen las notas en PDF y los ejercicios. Todo
  lo que se escribe aquí es para ellos, en español.
- **Los profesores**, que preparan las conferencias y las graban en audio a partir de
  las notas.

## Qué es "terminado" para una conferencia

- El `outline.md` está aprobado, y su línea `Estado:` lo dice.
- `notas.md` se renderiza con scriptorium sin trazas de error dentro del PDF.
- Cada número que cita la prosa coincide con lo que imprime el código del documento.
- Las citas y las afirmaciones sobre casos pequeños están verificadas, y lo que no se
  pudo verificar no está en las notas.
- `notas.pdf` está en el commit, junto con el `.md` que lo genera.

## Dónde está cada cosa

- `Lectures/2026/`: el curso actual. `plan.md` fija qué entra en cada conferencia y
  el orden. Cada conferencia vive en `NN-tema/`, y `figuras.py` es el módulo de
  figuras que comparten todas.
- `Lectures/*.md`: notas de cursos anteriores, en inglés. Son material de consulta y
  no se editan como parte del curso 2026.
- `Problems/`: problemas de práctica por tema.
- `Proyectos/`: orientaciones de proyecto de cursos anteriores.
- `know-how/`: un procedimiento por tarea, con sus trampas.

## Cómo se trabaja

Los cambios van directo a `main`, sin issue ni PR. El material se publica al ritmo del
curso, y un PR pendiente retrasaría una conferencia que los estudiantes ya esperan.

No hay `make` ni CI. Las comprobaciones de una conferencia (render, trazas, figuras,
páginas y números) están en el know-how.

El menú de procedimientos se imprime con:

```bash
grep -m1 -H '^when:' know-how/*.md
```
