import nltk
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords
import re
import math
import numpy


"""
Compute similarity between Nasari vectors using the Weighted overlap function
Input:
    vector1, vector2: Nasari vectors
Output:
    maxSimilarity: maximum value of square of Weighted Overlap
    mean: mean of all similarities
"""
def getSimilarity(vector1, vector2):
    similarity = []
    for v1 in vector1:
        for v2 in vector2:
            wo = getWeightedOverlap(v1,v2) # square of Weighted Overlap
            similarity.append (wo)
    mean = sum(similarity) / len(similarity) if len(similarity) > 0 else 0
    maxSimilarity = max(similarity) if len(similarity) > 0 else 0
    return maxSimilarity, mean

"""
Compute statistica overlap between two sentences, based on occurrance of common terms
Input:
    s1: sentence 1 (as list)
    s2: sentence 2 (as list)
Output:
    statistical similarity
"""
def getOverlap(s1,s2):
    s1 = bagOfWord(s1)
    s2 = bagOfWord(s2)
    return computeSimilarity(s1,s2)


def computeSimilarity(l1s, l2s):
    return float(len(set(l1s).intersection(l2s))) / min(len(l1s), len(l2s))


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
Calculate potential split points based on similarities values
Input:
    similarities: list of coesion values between windows
Ouput:
    split_points: ordered list of potential split points
"""
def getSplitPoints(similarities):
    split_points = []
    mean = sum(similarities) / len(similarities)
    for i in range(1, len(similarities) - 1):
        if (similarities[i] < mean) and (similarities[i] < similarities[i-1]) and (len(split_points)>0):
            #splits[-1] = (i,similarities[i])
            split_points.append((i,similarities[i]))
        elif (similarities[i] < mean) and ((i-1, similarities[i-1]) not in split_points):
            split_points.append((i,similarities[i]))
    return sorted(split_points, key=lambda x: x[1])

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