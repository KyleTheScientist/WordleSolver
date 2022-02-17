import time
import json
from multiprocessing import Pool
from solver import Solver
import pandas
from utils import Timer, Counter, Average

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

    df = pandas.DataFrame(columns=all_solutions, index=all_solutions)
    length = len(all_solutions)

    iavg = Average()
    javg = Average()
    ic = Counter(length)

    for i in range(length):

        itimer = Timer()
        jc = Counter(length)

        for j in range(length):
            jtimer = Timer()

            df.set_value(i, j, get_code(all_solutions[i], all_solutions[j]))

            javg += jtimer()
            jc()
            print(f"{ic} {str(iavg)} | {jc} {str(javg)}", end='\r')
        ic()
        iavg += itimer()

    df.to_csv('data/code_lookup.df')


