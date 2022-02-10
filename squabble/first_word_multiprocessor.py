import time
import json
from multiprocessing import Pool, Manager, managers
from solver import Solver

class FirstWordSolver(Solver):

    def __init__(self):
        super().__init__()

    def get_best_word(self):
        num_processes = 5
        manager = Manager()
        log = manager.list()
        scores = manager.dict()
        for solution in self.all_solutions:
            scores[solution] = 0
        
        partitioned_solutions = []
        partition_length = len(self.solutions)//num_processes
        for p in range(num_processes - 1):
            partitioned_solutions.append((
                p, 
                self.solutions[p * partition_length: (p + 1) * partition_length],
                scores,
                log
            ))
        
        p += 1
        partitioned_solutions.append((
            p, 
            self.solutions[p * partition_length:], 
            scores,
            log
        ))

        with Pool(num_processes) as p:
            p.map(self.score_words, partitioned_solutions)

        print("The best word is:")
        print(scores[0])

    def score_words(self, package):
        count = 0
        alias, solutions, scores, log = package
        print(f"{alias} | {len(scores)}")
        for solution in self.all_solutions:
            start = time.time()
            for s in solutions:
                rs = self.get_remaining_solutions(s, self.get_code(s, solution))
                scores[s] += len(rs)
            count += 1
            print(f"{alias} | Simulated {solution} in {int(time.time() - start)} seconds | ({count} / {len(solutions)}) solutions simulated")
            if alias == 0:
                try:
                    self.write_scores(self.sort_dictionary(dict(scores), False))
                except Exception as e:
                    print(e)
                

    def write_scores(self, scores):
        with open(f"scores.txt", 'w') as f:
            f.write(json.dumps(scores))

    def log(self, message):
        with open(f"output.txt", 'w') as f:
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
