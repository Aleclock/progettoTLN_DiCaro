import nltk
from nltk.corpus import wordnet as wn
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
import statistics
import itertools

from collections import Counter

# TODO provare questo per calcolo similarità: SequenceMatcher, similarità del coseno

def getSimilarity(definition):
    similarities = []
    for d1 in definition:
        for d2 in definition:
            if (d1 != d2 and d1 and d2):
                overlap = getOverlap(set(d1), set(d2))
                similarities.append (overlap / (min(len(d1),len(d2))))
    return statistics.mean(similarities)

"""
Input: lista di definizioni per un termine (formato lista di liste di termini)
Output: TODO
"""
def getCommonTerms(dProcessed, limit):
    d = list(itertools.chain.from_iterable(dProcessed)) # Unisce le liste in un'unica lista
    dict_of_words = Counter(d)  # Dizionario con le occorrenze dei termini nelle varie definizioni
    # TODO ripartire da qui, ritornnare le limit parole più comuni
    return dict_of_words[:limit]

    """for w,value in dict_of_words.items():
        print (w,value)"""



""" 
Apply sentence pre-process
- stopword remuval
- puntualization removal
- lemmatization 
Input:
    definitions: list of definitions of a term
Output:
    list of lists of words
"""
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
        #tokens = list(set(ps.stem(t) for t in tokens)) 
        processed.append(tokens)
    return processed

def getOverlap(d1, d2):
    intersection = d1.intersection(d2)
    return len(intersection)