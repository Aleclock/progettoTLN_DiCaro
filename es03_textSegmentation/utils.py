import nltk
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords
import re
import math
import numpy


def getSimilarity(vector1, vector2):
    similarity = []
    for v1 in vector1:
        for v2 in vector2:
            wo = getWeightedOverlap(v1,v2) # square of Weighted Overlap
            similarity.append (wo)
    return max(similarity) if len(similarity) > 0 else 0


"""
Allow to calculate the Semantic similarity. Implementation of Weight Overlap (Pilehvar et al.)
Input:
    vect1: Nasari vector (topic)
    vect2: Nasari vector (paragraph)
Output:
    square-rooted Weighted Overlap, or 0
"""
def getWeightedOverlap(vect1, vect2):
    keys_overlap = list(vect1.keys() & vect2.keys()) # keys in common
    if len(keys_overlap) > 0:
        n = sum(1 / (rank(q, list(vect1)) + rank(q, list(vect2))) for q in keys_overlap)
        d = sum(list(map(lambda x: 1 / (2 * x), list(range(1, len(keys_overlap) + 1)))))
        return math.sqrt(n/d)
    return 0

"""
Input:
    q: key of nasari vector
    v: Nasari vector
Output:
    index of the element q in v
"""
def rank(q, v):
    for i in range(len(v)):
        if v[i] == q:
            return i + 1


"""
Create a list of Lexical Nasari vector associated to all words of sentence
Input: 
    sentence: string
    nasari: Nasari dictionary
Output:
    list of Nasari vectors
"""
def getNasariVectors(sentence, nasari):
    topic = bagOfWord(sentence)
    vectors = []
    for word in topic:
        if word in nasari.keys():
            vectors.append(nasari[word])
    return vectors

"""
Clear the string in input (lower case, lemmatizer) and create a vector of the word of the string
Input:
    sentence: string
Output:
    vector of words
"""
def bagOfWord(tokens):
    lemmatizer = WordNetLemmatizer()
    punct = {',', ';', '(', ')', '{', '}','[',']', ':', '?', '!', '*','&',"'s"}
    stop_words = set(stopwords.words('english'))
    return [lemmatizer.lemmatize(w) for w in tokens if not w in stop_words and not w in punct]

"""
Load the nasari dictionary
Input: 
    path: file in input
Output: 
    concepts: dizionario {word: {term:score}}
"""
def loadNasari(path):
    concepts = {}

    # Allow to create a dictionary with the form:   nasari_word: {nasari_lexic:nasari_score}
    with open(path, 'r', encoding='utf8') as file:
        for line in file.readlines():
            tokens = line.split(";")
            lexical_dict = {}

            for token in tokens[2:]:
                token_part = token.split("_")
                if len(token_part) > 1:
                    lexical_dict[token_part[0]] = token_part[1]

            concepts[tokens[1].lower()] = lexical_dict
    file.close()

    return concepts