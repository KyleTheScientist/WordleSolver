class Solver:
    def __init__(self):
        with open("data/solutions.txt") as f:
            self.solutions_template = f.read().upper().split()
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
        remaining = []
        for s in self.solutions:
            valid = True
            for i in range(len(word)):
                if not self.valid_char(i, word, code, s):
                    valid = False
            if valid:
                remaining.append(s)
        return remaining

    def count_remaining_solutions(self, word, code):
        remaining = 0
        for s in self.solutions:
            valid = True
            for i in range(len(word)):
                if not self.valid_char(i, word, code, s):
                    valid = False
            if valid:
                remaining += 1
        return remaining

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
