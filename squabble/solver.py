import json
import time
class Solver:
    def __init__(self):
        with open("data/solutions.txt") as f:
            self.solution_strings = f.read().upper().split()

        with open("data/removal_indices.txt") as f:
            self.removals = json.loads(f.read())
            for key in self.removals.keys():
                self.removals[key] = set(self.removals[key])

        print("Building lookup table...")
        with open("data/code_lookup.json") as f:
            self.lookup_table = json.loads(f.read())
        print("Done!")

        self.sum = 0
        self.count = 0
        self.set_solution(None)

    def index_of(self, string):
        if string is None: return -1
        return self.solution_strings.index(string)

    def string(self, index):
        return self.solution_strings[index]

    def set_solution(self, string):
        self.manual = string
        self.solution = self.index_of(string)

        self.solutions = range(len(self.solution_strings))
        self.all_solutions = range(len(self.solution_strings))
        self.solutions_set = set(range(len(self.solution_strings)))

    def guess(self, guess_count):
        pass

    def get_code(self, word, solution):
        return self.lookup_table[solution][word]

    def get_remaining_solutions(self, word, code):
        start = time.time()
        remaining = self.solutions_set.copy()
        string = self.solution_strings[word]
        for index in range(len(string)):
            key = f"{index}{string[index]}{code[index]}"
            remaining.difference_update(self.removals[key])
        self.sum += time.time() - start
        self.count += 1
        return remaining

    def count_remaining_solutions(self, word, code):
        return len(self.get_remaining_solutions(word, code))

    def sort_dictionary(self, dictionary, reverse=True):
        result = {}
        for key in self.sort_keys(dictionary, reverse):
            result[key] = dictionary[key]
        return result

    def sort_keys(self, dictionary, reverse=True):
        return sorted(dictionary, key=dictionary.get, reverse=reverse)

