import time
import json
from multiprocessing import Pool
from solver import Solver

class SimpleSolver(Solver):

    def __init__(self):
        with open("data/simple_cache.txt", "r") as f:
            self.cache = json.loads(f.read())
        super().__init__()

    def guess(self, guess_count):
        if guess_count == 0:
            self.last_word = "RAISE"
        else:
            code = self.get_code(self.last_word, self.solution)

            self.solutions = self.get_remaining_solutions(self.last_word, code)
            if self.manual:
                print(f"{len(self.solutions)} possible solution{'s' if len(self.solutions) != 1 else ''}")

            if guess_count == 1 and code in self.cache:
                self.last_word = self.cache[code]
            else:
                self.last_word = self.get_best_word(attempting_solve=True)
                if guess_count == 1:
                    self.cache[code] = self.last_word
                    with open("data/simple_cache.txt", 'w') as f:
                        f.writelines([f'"{k}": "{v}",\n' for k, v in self.cache.items()])
        return self.last_word

    def get_best_word(self, attempting_solve=True):
        scores = {}
        count = 0
        for solution in self.solutions:
            count += 1
            for s in (self.solutions if attempting_solve else self.all_solutions):
                rs = self.get_remaining_solutions(s, self.get_code(s, solution))
                if s not in scores:
                    scores[s] = len(rs)
                else:
                    scores[s] += len(rs)
        scores = self.sort_dictionary(scores, False)
        best_word = self.break_tie(list(scores.items()))
        return best_word

    def break_tie(self, options):
        scores = {}
        best = options[0][1]
        for k, v in options:
            if v != best: continue
            scores[k] = self.score_word(k, self.get_solution_letter_weights())
        scores = self.sort_dictionary(scores)
        return list(scores.keys())[0]

    def score_word(self, word, weights):
        score = 0
        found = []
        for i in range(len(word)):
            c = word[i]
            if c in found: continue
            if c in weights[i]:
                score += weights[i][c]
            found.append(c)
        return score

    def get_solution_letter_weights(self):
        frequencies = [{} for _ in range(5)]
        for i in range(5):
            for solution in self.solutions:
                char = solution[i]
                if char not in frequencies[i]:
                    frequencies[i][char] = 1
                else:
                    frequencies[i][char] += 1

        for i in range(len(frequencies)):
            frequencies[i] = self.sort_dictionary(frequencies[i])

        return frequencies
