from random import uniform
from hybrid_solver import HybridSolver
from simple_solver import SimpleSolver

def main():
    with open("data/solutions.txt") as f:
        all_solutions = f.read().upper().split()

    scores = [0 for i in range(8)]
    solver = HybridSolver(threshold=2)
    # solver = SimpleSolver()
    count = 1
    for solution in all_solutions:
        print(f"The solution is {solution} ({count}/{len(all_solutions)})", end="\r")
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
    print()
    for i in range(len(scores)):
        print(f"{i}: {scores[i]}")



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
