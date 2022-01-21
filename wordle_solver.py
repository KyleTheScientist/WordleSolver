import time
import json
from multiprocessing import Pool

def main():
    with open("solutions.txt") as f:
        solutions = f.read().upper().split()
    
    word = "RAISE"
    while True:
        print(f'\nTry: {word}')
        code = input("Input the color code (ex. bbyyg): ")
        solutions = get_remaining_solutions(word, code, solutions)
        print(f"{len(solutions)} possible solution{'s' if len(solutions) > 1 else ''}")
        scores = {}
        for solution in solutions:
            for s in solutions:
                rs = get_remaining_solutions(word, get_code(s, solution), solutions)
                if s not in scores:
                    scores[s] = len(rs)
                else:
                    scores[s] += len(rs)
        scores = sort_dictionary(scores, False)
        word = break_tie(list(scores.items()))

with open("letter_frequencies.txt") as f:
    letter_weights = json.loads(f.read())

def break_tie(options):
    scores = {}
    best = options[0][1]
    for k, v in options:
        if v != best: continue
        scores[k] = score_word(k)
    scores = sort_dictionary(scores)
    # print(scores)
    return list(scores.keys())[0]

        
def score_word(word):
    score = 0 
    found = []
    for c in word:
        if c in found: continue
        score += letter_weights[c]
        found.append(c)
    return score
    
def get_remaining_solutions(word, code, all_solutions):
    remaining = []
    for s in all_solutions:
        valid = True
        for i in range(len(word)):
            character = word[i]
            c = code[i]
            if c == 'b' and character in s:
                valid = False
                break
            elif c == 'y' and (character not in s or character == s[i]):
                valid = False
                break
            elif c == 'g' and s[i] != character:
                valid = False
                break
        if valid:
            remaining.append(s)
    return remaining

def count_remaining_solutions(word, code, all_solutions):
    remaining = 0
    for s in all_solutions:
        valid = True
        for i in range(len(word)):
            character = word[i]
            c = code[i]
            if c == 'b' and character in s:
                valid = False
                break
            elif c == 'y' and character not in s:
                valid = False
                break
            elif c == 'g' and s[i] != character:
                valid = False
                break
        if valid:
            remaining += 1
    return remaining

def get_code(word, solution):
    code = ""
    for i in range(len(word)):
        if word[i] not in solution:
            code += 'b'
        elif solution[i] != word[i]:
            code += 'y'
        else:
            code += 'g'
    return code

def sort_dictionary(dictionary, reverse=True):
    sort = sorted(dictionary, key=dictionary.get, reverse=reverse)
    result = {}
    for key in sort:
        result[key] = dictionary[key]
    return result

def progress_bar(title, amount):
    stars = '*' * (round(amount * 20))
    if amount > 0:
        stripes = '-' * round((1 - amount) * 20)
    else:
        stripes = '-' * 20

    assert len(stars) + len(stripes) == 20
    print(title + ': |' + stars + '>' + stripes + '|', end = '\r')

if __name__ == "__main__":
    main()
