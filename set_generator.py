import time
import json
from multiprocessing import Pool
from solver import Solver

"""
Generates the table of words removed from the solutions list
by each combination of index, character, and color code and 
caches the information in a file so that these computations
do not need to be made at runtime by the solver.
"""

def invalid_char(index, character, code, solution):
    if code == 'b' and character in solution:
        return True
    elif code == 'y' and (character not in solution or character == solution[index]):
        return True
    elif code == 'g' and solution[index] != character:
        return True
    return False

def get_removed_solutions(index, character, code):
    removals = []
    for i in range(len(all_solutions)):
        if invalid_char(index, character, code, all_solutions[i]):
            removals.append(all_solutions[i])
    return removals

if __name__ == "__main__":
    with open("data/solutions.txt") as f:
        all_solutions = f.read().upper().split()

    removals = {}
    for index in range(5):
        # for character in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ':
        for character in 'E':
            for code in 'byg':
                key = f"{index}{character}{code}"
                removals[key] = get_removed_solutions(index, character, code)

    # print(removals['0Rb'])
    with open('data/removal_indices_test.txt', 'w') as f:
        f.write(json.dumps(removals))

