import time
import json
from multiprocessing import Pool
from solver import Solver

class FirstWordSolver(Solver):

    def __init__(self):
        super().__init__()

    def get_best_word(self):
        num_processes = 3
        partitioned_solutions = []
        partition_length = len(self.solutions)//num_processes
        for p in range(num_processes - 1):
            partitioned_solutions.append((p, self.solutions[p * partition_length: (p + 1) * partition_length]))
        p += 1
        partitioned_solutions.append((p, self.solutions[p * partition_length:]))

        with Pool(num_processes) as p:
            p.map(self.score_words, partitioned_solutions)

    def score_words(self, package):
        scores = {}
        count = 0
        alias, solutions = package
        for solution in self.all_solutions:
            count += 1
            self.log(f"Simulating {solution} | ({count} / {len(solutions)}) solutions simulated", alias)
            for s in solutions:
                rs = self.get_remaining_solutions(s, self.get_code(s, solution))
                if s not in scores:
                    scores[s] = len(rs)
                else:
                    scores[s] += len(rs)
            self.write_scores(self.sort_dictionary(scores, False), alias)

    def write_scores(self, scores, alias):
        with open(f"scores_{alias}.txt", 'w') as f:
            f.write(json.dumps(scores))

    def log(self, message, alias):
        with open(f"output_{alias}.txt", 'a') as f:
            f.write(message + "\n")

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

if __name__ == "__main__":
    FirstWordSolver().get_best_word()
