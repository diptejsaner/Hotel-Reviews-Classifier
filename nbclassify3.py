import json
import string
import sys

table = str.maketrans({key: None for key in string.punctuation})


def tokenize(s):
    return s.translate(table).rstrip()


classes_map = {
    "True": 0,
    "Fake": 1,
    "Pos": 2,
    "Neg": 3
}

with open('nbmodel.txt', 'r', encoding='utf8') as f:
    data = f.readlines()
    probabilities = json.loads(data[0])
    prior_probabilities = json.loads(data[1])

outputFile = open("nboutput.txt", "w", encoding='utf8')
line_count = 0

with open(sys.argv[1]) as f:
    for line in f:
        line = tokenize(line)
        tokens = line.split(" ")

        line_token_count = 0
        class1 = ""
        class2 = ""
        review_id = ""
        observation_probability = [0, 0, 0, 0]
        i = 0

        for c in classes_map:
            i = classes_map[c]
            observation_probability[i] = prior_probabilities[c]

            for token in tokens:
                if line_token_count == 0:
                    review_id = token

                else:
                    token = token.lower()

                    if token in probabilities:
                        observation_probability[i] += probabilities[token][i]

                line_token_count += 1

        outputFile.write(review_id)
        if observation_probability[0] > observation_probability[1]:
            outputFile.write(" True")
        else:
            outputFile.write(" Fake")

        if observation_probability[2] > observation_probability[3]:
            outputFile.write(" Pos")
        else:
            outputFile.write(" Neg")
        outputFile.write("\n")
        line_count += 1

outputFile.close()