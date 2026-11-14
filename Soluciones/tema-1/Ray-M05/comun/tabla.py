def _es_numero(texto):
    t = texto.replace(",", "").replace(" ", "").replace("×", "").replace("%", "")
    t = t.replace("−", "-").replace("≈", "").replace("(", "").replace(")", "")
    try:
        float(t)
        return True
    except ValueError:
        return False


def tabla_md(encabezados, filas, alineacion=None):
    filas = [[str(c) for c in f] for f in filas]
    if alineacion is None:
        alineacion = "".join(
            "d" if filas and all(_es_numero(f[j]) for f in filas) else "i"
            for j in range(len(encabezados))
        )
    separador = {"i": ":---", "d": "---:", "c": ":---:"}
    lineas = [
        "| " + " | ".join(encabezados) + " |",
        "|" + "|".join(separador[a] for a in alineacion) + "|",
    ]
    lineas += ["| " + " | ".join(f) + " |" for f in filas]
    return "\n".join(lineas)


def num(x, decimales=1):
    return f"{x:,.{decimales}f}"


def cientifica(x, cifras=3):
    if x == 0:
        return "0"
    mantisa, exponente = f"{x:.{cifras - 1}e}".split("e")
    superindices = str.maketrans("-0123456789", "⁻⁰¹²³⁴⁵⁶⁷⁸⁹")
    return f"{mantisa} × 10{str(int(exponente)).translate(superindices)}"


def potencia(base, exponente):
    superindices = str.maketrans("-0123456789", "⁻⁰¹²³⁴⁵⁶⁷⁸⁹")
    return f"{base}{str(exponente).translate(superindices)}"
