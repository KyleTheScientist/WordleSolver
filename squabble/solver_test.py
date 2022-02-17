from random import uniform
import time
import importlib
import sys

def main():
    with open("data/solutions.txt") as f:
        all_solutions = f.read().upper().split()

    solver_module = importlib.import_module(sys.argv[1])

    scores = [0 for i in range(8)]
    solver = solver_module.WordleSolver(threshold=10)
    count = 1
    test_start_time = time.time()
    for solution in all_solutions[0:10]:
        start = time.time()
        print(f"The solution is {solution} ({count}/{len(all_solutions)})")
        count += 1
        solver.set_solution(solution)
        guesses = 0
        guess = ""
        while guess != solution:
            guess = solver.guess(guesses)
            guesses += 1
            if guesses > 6:
                print(f"\nFailed! The word was {solution}")
                break
        scores[guesses] += 1
        print(f"Guess took {time.time() - start} second(s)")
    for i in range(len(scores)):
        print(f"{i}: {scores[i]}")
    print(f"Test took {time.time() - test_start_time}s")



def progress_bar(title, amount):
    stars = '*' * (round(amount * 20))
    if amount > 0:
        stripes = '-' * round((1 - amount) * 20)
    else:
        stripes = '-' * 20

    assert len(stars) + len(stripes) == 20
    print(title + ': |' + stars + '>' + stripes + '|', end = '\r')

if __name__ == "__main__":
    main()
