import math

def norm(vec):
    '''Return the norm of a vector stored as a dictionary,
    as described in the handout for Project 3.
    '''

    sum_of_squares = 0.0
    for x in vec:
        sum_of_squares += vec[x] * vec[x]

    return math.sqrt(sum_of_squares)

def cosine_similarity(vec1,vec2):
    dot_product = 0
    magnitudes_1 = 0
    magnitudes_2 = 0

    for key in vec1:
        if(key in vec2):
            dot_product += vec1[key] * vec2[key]
        magnitudes_1 += vec1[key]**2

    for key in vec2:
        magnitudes_2 += vec2[key]**2

    return dot_product/(magnitudes_1*magnitudes_2)**(1/2)


def build_semantic_descriptors(sentences):
    new_dict = {}
    for sentence in sentences:
        #removes duplicates
        fixed_sentence = list(set(sentence))
        for word1 in fixed_sentence:
            for word2 in fixed_sentence:
                if(word1 not in new_dict):
                    new_dict[word1] = {}
                if(word2 != word1):
                    if(word2 in new_dict[word1]):
                        new_dict[word1][word2] += 1
                    else:
                        new_dict[word1][word2] = 1
    return new_dict


def build_semantic_descriptors_from_files(filenames):
    texts = []
    for filename in filenames:
        text = open(filename, "r", encoding="latin1").read().lower()
        text = text.replace("\n"," ")
        #text = text.replace('"',"")
        text = text.replace(",","")
        text = text.replace("-"," ")
        text = text.replace("--"," ")
        text = text.replace(":","")
        text = text.replace(";","")

        text = text.replace("?",".")
        text = text.replace("!",".")
        text = text.split(".")

        for i in range(len(text)):
            text[i] = text[i].split()
            texts.append(text[i])

    new_dict = build_semantic_descriptors(texts)

    return new_dict



def most_similar_word(word, choices, semantic_descriptors, similarity_fn):
    max_index = 0
    max_similarity = -1
    similarity_score = 0

    if word not in semantic_descriptors:
        return choices[max_index]

    for i in range(len(choices)):
        if(choices[i] not in semantic_descriptors):
            similarity_score = -1
        else:
            similarity_score = similarity_fn(semantic_descriptors[word],semantic_descriptors[choices[i]])

        if(similarity_score > max_similarity):
            max_similarity = similarity_score
            max_index = i

    return choices[max_index]

def run_similarity_test(filename,semantic_descriptors,similarity_fn):
    text = open(filename,"r",encoding="latin1").read()
    text = text.split("\n")
    del text[-1]
    correct_answers = 0
    total_questions = len(text)
    new_list = []

    for i in range(len(text)):
        new_list.append(text[i].split())

    for i in range(len(new_list)):
        word = new_list[i][0]
        answer = new_list[i][1]
        choices = new_list[i][2:]
        if(most_similar_word(word,choices,semantic_descriptors,similarity_fn) == answer):
            correct_answers += 1
    return float((correct_answers/total_questions)*100)

#sem_descriptors = build_semantic_descriptors_from_files(["wp.txt","sw.txt"])
#res = run_similarity_test("test.txt", sem_descriptors, cosine_similarity)
#print(res, "of the guesses were correct")

#build_semantic_descriptors_from_files(["sample_case.txt"])














