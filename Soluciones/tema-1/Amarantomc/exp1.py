import sys

class TupleMinStack:
    def __init__(self):
        self.stack = []

    def push(self, x):
        if not self.stack:
            min_val = x
        else:
            min_val = min(x, self.stack[-1][1])
        self.stack.append((x, min_val))

    def pop(self):
        if not self.stack:
            raise IndexError("pop from empty stack")
        return self.stack.pop()[0]

    def top(self):
        if not self.stack:
            raise IndexError("top from empty stack")
        return self.stack[-1][0]

    def get_min(self):
        if not self.stack:
            raise IndexError("min from empty stack")
        return self.stack[-1][1]

# --- Casos de Prueba e Ilustración en Tabla ---
def probar_pila_tuplas():
    operaciones = [
        ("push", 5),
        ("push", 2),
        ("push", 8),
        ("min", None),
        ("push", 1),
        ("min", None),
        ("pop", None),
        ("min", None),
        ("pop", None),
        ("min", None),
        ("pop", None),
        ("min", None)
    ]

    pila = TupleMinStack()
    
    print(f"{'OPERACIÓN':<15} | {'ARG':<5} | {'ESTADO DE LA PILA (VAL, MIN)':<35} | {'MÍNIMO RETORNADO':<18}")
    print("-" * 81)

    for op, val in operaciones:
        res = "-"
        if op == "push":
            pila.push(val)
            res = f"insertado {val}"
        elif op == "pop":
            res = f"removido {pila.pop()}"
        elif op == "min":
            res = str(pila.get_min())
        
        stack_str = str(pila.stack)
        arg_str = str(val) if val is not None else ""
        
        print(f"{op:<15} | {arg_str:<5} | {stack_str:<35} | {res:<18}")

if __name__ == "__main__":
    probar_pila_tuplas()