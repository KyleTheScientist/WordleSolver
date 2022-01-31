import time
import json
from multiprocessing import Pool
from hybrid_solver import HybridSolver

def main():
    solver = HybridSolver(threshold=1)
    guesses = 0
    guess = ""
    while len(solver.solutions) != 1:
        guess = solver.guess(guesses)
        guesses += 1
        print(f'\nTry: {guess}')



if __name__ == "__main__":
    main()
