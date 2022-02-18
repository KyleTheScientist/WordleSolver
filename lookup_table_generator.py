import time
import json
from multiprocessing import Pool
from solver import Solver
import pandas
from utils import Timer, Counter, Average

"""
Generates the table of color codes for each pair of words
in the solutions list and caches the result in a file
so that these computations do not need to be made at
runtime by the solver.
"""

def get_code(word, solution):
        if solution == None:
            code = input("Input the color code (ex. bbyyg): ")
            return code
        code = ""
        for i in range(len(word)):
            if word[i] not in solution:
                code += 'b'
            elif solution[i] != word[i]:
                code += 'y'
            else:
                code += 'g'
        return code

if __name__ == "__main__":
    with open("data/solutions.txt") as f:
        all_solutions = f.read().upper().split()

    table = []
    length = len(all_solutions)

    iavg = Average()
    javg = Average()
    ic = Counter(length)

    for i in range(length):
        table.append([])
        itimer = Timer()
        jc = Counter(length)
        for j in range(length):
            jtimer = Timer()

            table[i].append(get_code(all_solutions[i], all_solutions[j]))

            javg += jtimer()
            jc()
            print(f"{ic} {iavg} | {jc} {javg}", end='\r')
        ic()
        iavg += itimer()

    with open("data/code_lookup.json", 'w') as f:
        f.write(json.dumps(table))


