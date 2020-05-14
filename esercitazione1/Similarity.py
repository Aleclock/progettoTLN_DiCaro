import nltk
from nltk.corpus import wordnet as wn
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
import statistics


def getSimilarity(definition):
    similarities = []
    for d1 in definition:
        for d2 in definition:
            if (d1 != d2 and d1 and d2):
                overlap = getOverlap(set(d1), set(d2))
                similarities.append (overlap / (min(len(d1),len(d2))))
    return statistics.mean(similarities)

""" Made the pre-process of a sentence
    - stopword remuval
    - puntualization removal
    - lemmatization 
    Return a list of words"""
def preProcess(definition):
    processed = []
    for d in definition:
        stop_words = set(stopwords.words('english'))
        punct = {',', ';', '(', ')', '{', '}', ':', '?', '!','.'}
        wnl = nltk.WordNetLemmatizer()
        ps = PorterStemmer()
        
        tokens = nltk.word_tokenize(d)
        tokens = list(filter(lambda x: x not in stop_words and x not in punct, tokens)) #and "'s" not in x
        tokens = list(set(wnl.lemmatize(t) for t in tokens))
        tokens = list(set(ps.stem(t) for t in tokens)) 
        processed.append(tokens)
    return processed

def getOverlap(d1, d2):
    intersection = d1.intersection(d2)
    return len(intersection)