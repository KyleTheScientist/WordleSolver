from random import uniform
import time
import importlib
import sys
from utils import Timer, Counter, Average

def main():
    with open("data/solutions.txt") as f:
        all_solutions = f.read().upper().split()

    solver_module = importlib.import_module(sys.argv[1])

    scores = [0 for i in range(8)]
    solver = solver_module.WordleSolver(threshold=10)
    count = 1
    test_timer = Timer()
    solution_timer = Timer()
    counter = Counter(len(all_solutions))
    solution_average = Average()
    for solution in all_solutions:
        solution_timer.reset()
        print(f"{counter} The solution is {solution}", end="")
        counter()
        solver.set_solution(solution)
        guesses = 0
        guess = ""
        while guess != solution:
            guess = solver.guess(guesses)
            guesses += 1
            if guesses > 6:
                print(f" | Failed!", end="")
                with open("data/failures.txt", 'a') as f:
                    f.write(solution + "\n")
                break
        scores[guesses] += 1
        solution_average += solution_timer()
        print(f" | Solution took {solution_timer} ({solution_average})")
    for i in range(len(scores)):
        print(f"{i}: {scores[i]}")
    print(f"Test took {test_timer}")

if __name__ == "__main__":
    main()
