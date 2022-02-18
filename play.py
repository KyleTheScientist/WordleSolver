import time
import json
from multiprocessing import Pool
from wordle_solver import WordleSolver
import colorama
from colorama import Fore, Back, Style

colorama.init()
def main():
    solver = WordleSolver(threshold=10)
    while True:
        solver.set_solution(None)
        guesses = 0
        guess = ""
        while len(solver.solutions) != 1:
            try:
                guess = solver.guess(guesses)
            except:
                break
            guesses += 1
            string = f"{Fore.GREEN}The solution is: " if len(solver.solutions) == 1 else f"{Fore.YELLOW}Try: "
            if len(solver.solutions) <= 5:
                print(*solver.solutions)
            print("=" * 10)
            print(string + guess + Fore.RESET)
            print("=" * 10)
        input(f"{Fore.MAGENTA}~Press enter to play again~{Fore.RESET}")
        for _ in range(5): print()


if __name__ == "__main__":
    main()
