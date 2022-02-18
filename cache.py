from random import uniform
import time
import importlib
import sys
from utils import Timer, Counter, Average
import json

def main():
    with open("data/solutions.txt") as f:
        all_solutions = f.read().upper().split()

    solver_module = importlib.import_module(sys.argv[1])

    scores = [0 for i in range(8)]
    solver = solver_module.WordleSolver(threshold=5)
    counter = Counter(len(all_solutions))

    for solution in all_solutions:
        counter()
        solver.set_solution(solution)
        solver.guess(0)
        solver.guess(1)
        with open(solver.cache_file, 'w') as f:
            f.write(json.dumps(dict(sorted(solver.cache.items()))))
        print(f"{counter} The solution is {solution}", end="\r")
        
    
if __name__ == "__main__":
    main()
