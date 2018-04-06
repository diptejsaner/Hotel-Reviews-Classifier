import json
import string
import sys
import math

f = open(sys.argv[1], "r", encoding='utf8')

probabilities = {}

classes_map = {
    "True": 0,
    "Fake": 1,
    "Pos": 2,
    "Neg": 3
}

tokens_in_class = {
    "True": 0,
    "Fake": 0,
    "Pos": 0,
    "Neg": 0
}

classes_prior_probability = {
    "True": 0,
    "Fake": 0,
    "Pos": 0,
    "Neg": 0
}

table = str.maketrans({key: None for key in string.punctuation})


def tokenize(s):
    return s.translate(table).rstrip()


line_count = 0

for line in f:
    line = tokenize(line)
    tokens = line.split(" ")

    line_token_count = 0
    class1 = ""
    class2 = ""

    for token in tokens:
        if line_token_count == 1:
            class1 = token
            classes_prior_probability[class1] += 1

        if line_token_count == 2:
            class2 = token
            classes_prior_probability[class2] += 1

        elif line_token_count > 2:
            token = token.lower()

            if token not in probabilities:
                probabilities[token] = [0, 0, 0, 0]

            probabilities[token][classes_map[class1]] += 1
            probabilities[token][classes_map[class2]] += 1
            tokens_in_class[class1] += 1
            tokens_in_class[class2] += 1

        line_token_count += 1
    line_count += 1

f.close()

# delete top 2 high frequency and low frequency tokens
high_freq_token = ""
low_freq_token = ""
for i in range(2):
    maxp = -1
    minp = 99999999999
    p = 0
    for token in probabilities:
        p = probabilities[token][0] + probabilities[token][1]
        if p > maxp:
            maxp = p
            high_freq_token = token
        if p < minp:
            minp = p
            low_freq_token = token
    del probabilities[high_freq_token]
    del probabilities[low_freq_token]


# convert to probabilities and do add one smoothing
for token in probabilities:
    for c in tokens_in_class:
        i = classes_map[c]
        probabilities[token][i] = math.log2((probabilities[token][i] + 1) / (tokens_in_class[c] + len(probabilities)))

for c in classes_prior_probability:
    classes_prior_probability[c] = math.log2(classes_prior_probability[c] / line_count)

with open('nbmodel.txt', 'w', encoding='utf8') as fp:
    fp.write(json.dumps(probabilities, ensure_ascii=False))
    fp.write("\n")
    fp.write(json.dumps(classes_prior_probability, ensure_ascii=False))