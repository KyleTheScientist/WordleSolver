import json

def sort_dictionary(dictionary, reverse=True):
    sort = sorted(dictionary, key=dictionary.get, reverse=reverse)
    result = {}
    for key in sort:
        result[key] = dictionary[key]
    return result

with open("data/solutions.txt") as f:
    solutions = f.readlines()
    frequencies = [{} for _ in range(5)]
    for i in range(5):
        for solution in solutions:
            solution = solution.strip()
            char = solution[i]
            if char not in frequencies[i]:
                frequencies[i][char] = 1
            else:
                frequencies[i][char] += 1

for i in range(len(frequencies)):
    frequencies[i] = sort_dictionary(frequencies[i])

with open("data/letter_frequencies_indexed.txt", "w") as f:
    f.write(json.dumps(frequencies))


