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

def get_removed_solutions(index, character, code):
    removals = []
    for i in range(len(all_solutions)):
        if not valid_char(index, character, code, all_solutions[i]):
            removals.append(i)
    return removals

if __name__ == "__main__":
    with open("data/solutions.txt") as f:
        all_solutions = f.read().upper().split()

    removals = {}
    for index in range(5):
        for character in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ':
            for code in 'byg':
                key = f"{index}{character}{code}"
                removals[key] = get_removed_solutions(index, character, code)

    with open('data/removal_indices.txt', 'w') as f:
        f.write(json.dumps(removals))

