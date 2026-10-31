BLANK = "_"

# Maquina que suma 1. El numero esta escrito en binario con el bit mas
# significativo a la izquierda, y el cabezal empieza y termina en el bit
# menos significativo. Una celda en blanco cuenta como 0.
#   (estado, simbolo leido) -> (simbolo a escribir, movimiento, estado nuevo)
INCREMENT = {
    ("carry", "1"): ("0", -1, "carry"),       # 1 + acarreo = 0, el acarreo sigue a la izquierda
    ("carry", "0"): ("1", +1, "back"),        # 0 + acarreo = 1, se acabo el acarreo
    ("carry", BLANK): ("1", +1, "back"),      # el numero crece un bit
    ("back", "0"): ("0", +1, "back"),         # volver a la derecha...
    ("back", "1"): ("1", +1, "back"),
    ("back", BLANK): (BLANK, -1, "halt"),     # ...hasta pasarse del ultimo bit, y un paso atras
}

# Variante para comparar: el cabezal empieza y termina en el bit MAS significativo.
INCREMENT_FROM_LEFT = {
    ("right", "0"): ("0", +1, "right"),       # ir hasta el final del numero
    ("right", "1"): ("1", +1, "right"),
    ("right", BLANK): (BLANK, -1, "carry"),
    ("carry", "1"): ("0", -1, "carry"),
    ("carry", "0"): ("1", -1, "left"),
    ("carry", BLANK): ("1", 0, "halt"),       # el numero crece un bit a la izquierda (y se queda ahi)
    ("left", "0"): ("0", -1, "left"),         # volver hasta el principio del numero
    ("left", "1"): ("1", -1, "left"),
    ("left", BLANK): (BLANK, +1, "halt"),
}


class TuringMachine:
    def __init__(self, table, start_state):
        self.table = table
        self.start_state = start_state
        self.tape = {}                         # posicion -> simbolo (lo que falta es blanco)
        self.head = 0

    def run(self):
        # Ejecuta la maquina desde start_state hasta halt. Devuelve los pasos.
        state, steps = self.start_state, 0
        while state != "halt":
            symbol = self.tape.get(self.head, BLANK)
            write, move, state = self.table[(state, symbol)]
            self.tape[self.head] = write
            self.head += move
            steps += 1
        return steps

    def value(self):
        # El numero escrito en la cinta.
        bits = "".join(self.tape[p] for p in sorted(self.tape) if self.tape[p] != BLANK)
        return int(bits, 2) if bits else 0

    def ones(self):
        return sum(1 for s in self.tape.values() if s == "1")

    def text(self):
        # La cinta como texto, con el cabezal marcado entre corchetes.
        posiciones = sorted(set(self.tape) | {self.head})
        celdas = []
        for p in range(posiciones[0], posiciones[-1] + 1):
            s = self.tape.get(p, BLANK)
            celdas.append(f"[{s}]" if p == self.head else f" {s} ")
        return "".join(celdas)


def counter():
    return TuringMachine(INCREMENT, "carry")


def counter_from_left():
    return TuringMachine(INCREMENT_FROM_LEFT, "right")
