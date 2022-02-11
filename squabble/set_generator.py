import time
import json
from multiprocessing import Pool
from solver import Solver

def valid_char(index, character, code, solution):
    if code == 'b' and character in solution:
        return False
    elif code == 'y' and (character not in solution or character == solution[index]):
        return False
    elif code == 'g' and solution[index] != character:
        return False
    return True

def get_remaining_solutions(index, character, code):
        remaining = []
        for solution in all_solutions:
            if not valid_char(index, character, code, solution): continue
            remaining.append(solution)
        return remaining

if __name__ == "__main__":
    with open("data/solutions.txt") as f:
        all_solutions = f.read().upper().split()

    remaining = {}
    for index in range(5):
        for character in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ':
            for code in 'byg':
                key = f"{index}{character}{code}"
                remaining[key] = get_remaining_solutions(index, character, code)

    with open('data/remaining.txt', 'w') as f:
        f.write(json.dumps(remaining))

