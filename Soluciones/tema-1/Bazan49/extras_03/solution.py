class MinStack:
    """A stack data structure providing O(1) worst-case time for min()."""
    def __init__(self):
        self._stack = []

    def push(self, x: int) -> None:
        if not self._stack:
            self._stack.append((x, x))
        else:
            current_min = self._stack[-1][1]
            self._stack.append((x, min(x, current_min)))

    def pop(self) -> None:
        if self._stack:
            self._stack.pop()

    def top(self) -> int | None:
        if self._stack:
            return self._stack[-1][0]
        return None

    def min(self) -> int | None:
        if self._stack:
            return self._stack[-1][1]
        return None

    def __len__(self) -> int:
            return len(self._stack)