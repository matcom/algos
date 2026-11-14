import ast
import os
import re
import subprocess
import sys
from pathlib import Path

SALIDA = re.compile(r"(<!-- salida: (.+?) -->\n)(.*?)(<!-- /salida -->)", re.S)
CODIGO = re.compile(r"(<!-- codigo: (.+?) -->\n)(.*?)(<!-- /codigo -->)", re.S)


def _correr(carpeta, orden, cache):
    if orden not in cache:
        script, *args = orden.split()


        entorno = dict(os.environ, PYTHONPATH=str(carpeta),
                       PYTHONIOENCODING="utf-8", PYTHONUTF8="1")
        r = subprocess.run([sys.executable, script, *args], cwd=carpeta, env=entorno,
                           capture_output=True, text=True, encoding="utf-8")
        if r.returncode != 0:
            raise RuntimeError(f"falló `{orden}`:\n{r.stderr}")
        cache[orden] = r.stdout.strip()
    return cache[orden]


def _fuente(carpeta, orden):
    archivo, nombres = orden.split(maxsplit=1)
    nombres = [n.strip() for n in nombres.split(",")]
    texto = (carpeta / archivo).read_text(encoding="utf-8")
    lineas = texto.splitlines()
    arbol = ast.parse(texto)
    trozos = {}
    for nodo in arbol.body:
        if isinstance(nodo, (ast.FunctionDef, ast.ClassDef)):
            nombre = nodo.name
        elif isinstance(nodo, ast.Assign) and isinstance(nodo.targets[0], ast.Name):
            nombre = nodo.targets[0].id
        else:
            continue
        inicio = min([nodo.lineno] + [d.lineno for d in getattr(nodo, "decorator_list", [])])
        trozos[nombre] = "\n".join(lineas[inicio - 1:nodo.end_lineno])
    faltan = [n for n in nombres if n not in trozos]
    if faltan:
        raise RuntimeError(f"{archivo} no define {', '.join(faltan)}")
    return "```python\n" + "\n\n".join(trozos[n] for n in nombres) + "\n```"


def regenerar(md):
    md = Path(md).resolve()
    carpeta = md.parent
    texto = md.read_text(encoding="utf-8")
    cache = {}
    texto = SALIDA.sub(lambda m: m[1] + _correr(carpeta, m[2], cache) + "\n" + m[4], texto)
    texto = CODIGO.sub(lambda m: m[1] + _fuente(carpeta, m[2]) + "\n" + m[4], texto)
    md.write_text(texto, encoding="utf-8")
    return len(cache)


def main(argv):
    raiz = Path(__file__).resolve().parent.parent
    archivos = argv or sorted(str(p) for p in raiz.glob("ejercicio-*.md"))
    for a in archivos:
        n = regenerar(a)
        print(f"{Path(a).name}: {n} salidas regeneradas")


if __name__ == "__main__":
    main(sys.argv[1:])
