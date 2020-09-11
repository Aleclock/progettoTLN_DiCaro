import nltk
from nltk.corpus import wordnet as wn
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
import statistics

# TODO provare questo per calcolo similarità: SequenceMatcher, similarità del coseno

"""
Calculate the mean similarity between each couple of definition
Input:
    definitions: list of definitions about one term
Output:
    similarity mean value
"""
def getSimilarity(definitions):
    similarities = []
    for d1 in definitions:
        for d2 in definitions:
            if (d1 != d2 and d1 and d2):
                overlap = getOverlap(set(d1), set(d2))
                similarities.append (overlap / (min(len(d1),len(d2))))
    return statistics.mean(similarities)

""" 
Made the pre-process of a sentence
- stopword remuval
- puntualization removal
- lemmatization 
- stemming
Input:
    definitions: list of definitions of a term
Output:
    list of lists of words
"""
def preProcess(definitions):
    processed = []
    for d in definitions:
        stop_words = set(stopwords.words('english'))
        punct = {',', ';', '(', ')', '{', '}', ':', '?', '!','.', "'s"}
        #wnl = nltk.WordNetLemmatizer()
        ps = PorterStemmer()
        
        tokens = nltk.word_tokenize(d.lower())
        tokens = list(filter(lambda x: x not in stop_words and x not in punct, tokens))
        #tokens = list(set(wnl.lemmatize(t) for t in tokens))
        tokens = list(set(ps.stem(t) for t in tokens)) 
        processed.append(tokens)
    return processed

"""
Get the overlap between two lists (two definitions)
Input:
    d1,d2: list of terms (set)
Output:
    intersection length
"""
def getOverlap(d1, d2):
    intersection = d1.intersection(d2)
    return len(intersection)