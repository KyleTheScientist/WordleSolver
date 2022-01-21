import json

def sort_dictionary(dictionary, reverse=True):
    sort = sorted(dictionary, key=dictionary.get, reverse=reverse)
    result = {}
    for key in sort:
        result[key] = dictionary[key]
    return result

with open("solutions.txt") as f:
    solutions = f.read()
    frequencies = {}
    for char in solutions:
        if char not in frequencies:
            frequencies[char] = 1
        else:
            frequencies[char] += 1
    
frequencies = sort_dictionary(frequencies)
with open("letter_frequencies.txt", "w") as f:
    f.write(json.dumps(frequencies))


