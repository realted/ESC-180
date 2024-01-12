import math

def norm(vec):
    '''Return the norm of a vector stored as a dictionary, as
    described in the handout for Project 3.
    '''

    sum_of_squares = 0.0
    for x in vec:
        sum_of_squares += vec[x] * vec[x]

    return math.sqrt(sum_of_squares)

vec1 = {"a": 1, "b": 2, "c": 3}
vec2 = {"b": 4, "c": 5, "d": 6}

def cosine_similarity(vec1, vec2):

    vec1_key = list(vec1.keys())
    vec1_val = list(vec1.values())

    vec2_key = list(vec2.keys())
    vec2_val = list(vec2.values())

    numer = 0

    for i in range(len(vec1_key)):
        for j in range(len(vec2_key)):
            if (vec1_key[i] == vec2_key[j]):
                numer = vec1_val[i] * vec2_val[j] + numer

    denom1, denom2 = 0, 0

    for k in range(len(vec1_key)):
        denom1 += vec1_val[k] ** 2

    for l in range(len(vec2_key)):
        denom2 += vec2_val[l] ** 2


    simul = numer / math.sqrt(denom1*denom2)

    return simul

def build_semantic_descriptors(sentences):
    all_dict = {}
    for i in range (len(sentences)):
        for j in range (len(sentences[i])):
            if sentences[i][j] not in all_dict:
                new_word = {}
                for word in sentences[i]:
                    if word != sentences[i][j]:
                        if word in new_word:
                            new_word[word] += 1
                        else:
                            new_word[word] = 1
                    all_dict[sentences[i][j]] = new_word
            else:
                for word in sentences[i]:
                    if word != sentences[i][j]:
                        if word in all_dict[sentences[i][j]]:
                            all_dict[sentences[i][j]][word] += 1
                        else:
                            all_dict[sentences[i][j]][word] = 1
    return all_dict



def build_semantic_descriptors_from_files(filenames):
    sen_list = []
    for i in range(len(filenames)):
        store = []
        temp = open(filenames[i], "r", encoding="latin1").read().lower()
        temp = temp.replace("?", ".")
        temp = temp.replace("!", ".")
        temp = temp.replace("\n", " ")
        temp = temp.replace(",", " ")
        temp = temp.replace(";", " ")
        temp = temp.replace(":", " ")
        temp = temp.replace("-", " ")
        temp = temp.replace("<", " ")
        temp = temp.replace(">", " ")
        temp = temp.replace("---", " ")
        temp = temp.replace("--", " ")
        new_temp = temp.split(".")

        for j in new_temp:
            store.append(j.split())
        sen_list += store

    return build_semantic_descriptors(sen_list)

def most_similar_word(word, choices, semantic_descriptors, similarity_fn):

    score = []
    max = -1000
    for i in range(len(choices)):
        if choices[i] not in semantic_descriptors:
            score.append(-1)
        else:
            score.append(similarity_fn(semantic_descriptors[word], semantic_descriptors[choices[i]]))

        if (score[i] > max):
            max = score[i]
            max_idx = choices[i]

    return max_idx

def run_similarity_test(filename, semantic_descriptors, similarity_fn):
    text = open(filename, "r", encoding="latin1")
    match = 0
    total = 0

    for sentence in text.readlines():
        sentence = sentence.split()
        word = sentence[0]
        answer = sentence[1]
        choices = sentence[2:]
        total += 1

        if (answer == most_similar_word(word, choices, semantic_descriptors, similarity_fn)):
            match += 1

    return (match/total)*100