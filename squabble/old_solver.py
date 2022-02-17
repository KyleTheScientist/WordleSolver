import json
import time

class OldSolver:
    def __init__(self):
        with open("data/solutions.txt") as f:
            self.solutions_template = f.read().upper().split()
        with open("data/remaining.txt") as f:
            self.remaining = json.loads(f.read())
            for key in self.remaining.keys():
                self.remaining[key] = set(self.remaining[key])
        with open("data/removals.txt") as f:
            self.removals = json.loads(f.read())
            for key in self.removals.keys():
                self.removals[key] = set(self.removals[key])
        self.sum = 0
        self.count = 0
        self.set_solution(None)

    def set_solution(self, solution):
        self.solution = solution
        self.manual = self.solution is None

        self.solutions = self.solutions_template.copy()
        self.all_solutions = self.solutions_template.copy()

    def guess(self, guess_count):
        pass

    def get_code(self, word, solution):
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

    def get_remaining_solutions(self, word, code):
        start = time.time()
        remaining = set(self.solutions)
        for index in range(len(word)):
            key = f"{index}{word[index]}{code[index]}"
            remaining.difference_update(self.removals[key])
        self.sum += time.time() - start
        self.count += 1
        return list(remaining)

    def count_remaining_solutions(self, word, code):
        remaining = set(self.solutions)
        for index in range(len(word)):
            key = f"{index}{word[index]}{code[index]}"
            remaining.difference_update(self.removals[key])
        return len(remaining)

    def valid_char(self, index, word, code, solution):
        character = word[index]
        c = code[index]
        if c == 'b' and character in solution:
            return False
        elif c == 'y' and (character not in solution or character == solution[index]):
            return False
        elif c == 'g' and solution[index] != character:
            return False
        return True

    def sort_dictionary(self, dictionary, reverse=True):
        sort = sorted(dictionary, key=dictionary.get, reverse=reverse)
        result = {}
        for key in sort:
            result[key] = dictionary[key]
        return result
