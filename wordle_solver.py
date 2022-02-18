import time
import json
from multiprocessing import Pool
from solver import Solver
from utils import Average, Counter, Timer

class WordleSolver(Solver):

    def __init__(self, threshold=5):
        self.threshold = threshold
        self.cache_file = f"data/second_guess_cache_{threshold}.json"
        try:
            with open(self.cache_file, "r") as f:
                self.cache = json.loads(f.read())
        except:
            self.cache = {}
        super().__init__()

    def guess(self, guess_count):
        guess_timer = Timer()
        if guess_count == 0:
            self.last_word = self.index_of("RAISE")
        else:
            code = self.get_code(self.last_word, self.solution, manual=self.manual)
            self.solutions = self.get_remaining_solutions(self.last_word, code)
            self.log(f"{len(self.solutions)} possible solution{'s' if len(self.solutions) != 1 else ''}")

            attempting_solve = len(self.solutions) <= self.threshold
            if not attempting_solve and guess_count == 1 and code in self.cache:
                self.last_word = self.cache[code]
            else:
                self.last_word = self.get_best_word(attempting_solve=attempting_solve)
                if guess_count == 1 and not attempting_solve:
                    self.cache[code] = self.last_word
        self.log(f"Guess took {guess_timer}")
        return self.string(self.last_word)

    def get_best_word(self, attempting_solve=True):
        candidates = (self.solutions if attempting_solve else self.all_solutions)
        scount = Counter(len(self.solutions))
        ccount = Counter(len(candidates))
        stimer = Timer()
        ctimer = Timer()
        s_average = Average()
        c_average = Average()

        scores = {c: 0 for c in candidates}
        for solution in self.solutions:
            stimer.reset()
            ccount.reset()
            scount()
            for candidate in candidates:
                ctimer.reset()
                ccount()
                code = self.get_code(candidate, solution)
                rs = self.get_remaining_solutions(candidate, code)
                scores[candidate] += len(rs)
                c_average += ctimer()
                status_string = f"Possible solutions: {scount} {s_average():.3f} | Guesses: {ccount} {c_average():.6f}"
                self.log(status_string, end='\r')
            s_average += stimer()
        self.log(' ' * 80, end='\r')
        scores = self.sort_dictionary(scores, False)
        best_word = self.break_tie(list(scores.items()))
        return best_word

    def break_tie(self, options):
        scores = {}
        best = options[0][1]
        for k, v in options:
            if v != best: continue
            scores[k] = self.score_word(k, self.get_solution_letter_weights())
        return self.sort_keys(scores)[0]

    def score_word(self, word, weights):
        score = 0
        found = []
        string = self.string(word)
        for i in range(len(string)):
            c = string[i]
            if c in found: continue
            if c in weights[i]:
                score += weights[i][c]
            found.append(c)
        return score

    def get_solution_letter_weights(self):
        frequencies = [{} for _ in range(5)]
        for i in range(5):
            for solution in self.solutions:
                char = self.string(solution)[i]
                if char not in frequencies[i]:
                    frequencies[i][char] = 1
                else:
                    frequencies[i][char] += 1

        for i in range(len(frequencies)):
            frequencies[i] = self.sort_dictionary(frequencies[i])

        return frequencies

    def log(self, message, end='\n'):
        if self.manual:
            print(message, end=end)