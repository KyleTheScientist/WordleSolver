from time import time

class Average():
    def __init__(self):
        self.count = 0
        self.sum = 0

    def get(self):
        return self()

    def __call__(self):
        if self.sum == 0: return 0
        return self.sum / self.count

    def __iadd__(self, x):
        self.sum += x
        self.count += 1
        return self

    def __str__(self):
        return f"{self():.4f}"

class Counter():
    def __init__(self, cap):
        self.count = 0
        self.cap = cap

    def __str__(self) -> str:
        return f"({self.count}/{self.cap})"

    def __call__(self):
        self.count += 1
        return self.count

    def __iadd__(self, x):
        self.sum += x
        self.count += 1
        return self

    def reset(self):
        self.count = 0


class Timer():
    def __init__(self):
        self.start = time()

    def __call__(self):
        return time() - self.start

    def reset(self):
        self.start = time()

    def __str__(self) -> str:
        return f"{self():.4f}s"
