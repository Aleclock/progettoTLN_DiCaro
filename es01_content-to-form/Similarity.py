import nltk
from nltk.corpus import wordnet as wn
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
import statistics
import itertools
import os

from collections import Counter

"""
Input: lista di definizioni per un termine (formato lista di liste di termini)
Output: TODO
"""
def getCommonTerms(dProcessed):
    d = list(itertools.chain.from_iterable(dProcessed)) # Unisce le liste in un'unica lista
    most_common_words = [word for word, word_count in Counter(d).most_common()] # Dizionario con le occorrenze dei termini nelle varie definizioni
    #print (most_common_words)
    return most_common_words

"""
Genus-differentia mechanism: meccanismo che dice che per descrivere un concetto ci sono due cose da dire:
    - Genus, dice che per descrivere il concetto la prima cosa da fare è includerlo all’interno di una tassonomia. 
      Circoscrivere attraverso iperonimo il raggio d’azione;
        Per descrivere il mango, lo si circoscrive dicendo che è un frutto.
    - Differentia, tutto ciò che caratterizza quel concetto in maniera differenziale dagli altri. Si tratta della discriminante

Mentre il genus dice cos’è il concetto, il secondo dice cosa lo differenzia da tutti gli altri.
"""
def getSynsetsFromLemma(lemmas, hyponyms_limit, hypernyms_limit):
    concepts = []
    for l in lemmas:
        synsets = wn.synsets(l)
        concepts += synsets
        for s in synsets:
            concepts += get_hyponyms(s, hyponyms_limit)
            concepts += get_hypernyms(s, hypernyms_limit)
    #print (len(concepts))
    #print ([ (word,word_count) for word, word_count in Counter(concepts).most_common(10)])
    return set(concepts)


def get_hyponyms(synset, limit):
    hyponyms = set()
    if (limit > 0):
        for hyponym in synset.hyponyms():
            hyponyms |= set(get_hyponyms(hyponym, limit - 1))   # |= bitwise or, che sugli insiemi produce l'unione
    #return hyponyms
    return hyponyms | set(synset.hyponyms())

def get_hypernyms(synset, limit):
    hypernyms = set()
    if (limit > 0):
        for hypernym in synset.hypernyms():
            hypernyms |= set(get_hypernyms(hypernym, limit - 1))    # |= bitwise or, che sugli insiemi produce l'unione
    #return hypernyms
    return hypernyms | set(synset.hypernyms())

"""
Return best synset compared to context terms
Input:
    synsets: list of synset
    context: context of a term (composed of terms)
Output:
    best_sense
"""
def getBestSense(synsets,context):
    all_sense = []
    best_sense = None
    max_overlap = 0
    for sense in synsets:
        signature = getSynsetContext(sense)
        overlap = computeOverlap(signature, context) + 1
        all_sense.append((sense, overlap))
        if overlap > max_overlap:
            best_sense = sense
            max_overlap = overlap
    return best_sense, max_overlap, all_sense


"""
Create the context of a synset
The context include the definition and examples of synset
TODO: non prendo anche le definizioni degli iponimi/iperonimi in quanto quelli vengono analizzati da soli
Input:
    s: synset
Output:
    context
"""
def getSynsetContext(s):
    context = preProcess_synset(s.definition())
    for e in s.examples():
        context=list(set().union(context, preProcess_synset(e)))
    return context


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
        
        tokens = nltk.word_tokenize(d.lower())
        tokens = list(filter(lambda x: x not in stop_words and x not in punct, tokens))
        tokens = list(set(wnl.lemmatize(t) for t in tokens))
        #tokens = list(set(ps.stem(t) for t in tokens)) 
        processed.append(tokens)
    return processed


""" Made the pre-process of a sentence
    - stopword removal
    - puntualization removal
    - lemmatization
Input:
    d: sentence
Output:
    list of words
"""
def preProcess_synset(d):
    stop_words=set(stopwords.words('english'))
    punct={',', ';', '(', ')', '{', '}', ':', '?', '!', '.'}
    wnl=nltk.WordNetLemmatizer()
    ps=PorterStemmer()

    tokens=nltk.word_tokenize(d.lower())
    tokens=list(filter(lambda x: x not in stop_words and x not in punct, tokens))
    tokens=list(set(wnl.lemmatize(t) for t in tokens))
    #tokens=list(set(ps.stem(t) for t in tokens))
    return tokens

"""
Allow to determinate the Part-of-Speech of sentence
Input:
    sentence: name
Output:
    pos_tags: part-of-speech tags
"""
def getPOS(sentence):
    pos_tags=nltk.pos_tag(nltk.word_tokenize(sentence), tagset='universal')
    return pos_tags

"""
Retrieve the main term from a part-of-speech tagging
Input:
    pos: part-of-speech
Output:
    main term
"""
def getNouns(pos):
    terms = []
    for word, tag in pos:
        if tag == "NOUN":
            terms.append(word)
    return terms


"""
Calculate the overlap between two context
Input:
    signature: context of frame
    context: context of synset
Output:
    length of intersection
"""
def computeOverlap(signature, context):
    intersection= set(signature).intersection(set(context))
    return len(intersection)

def clear_file(path):
    os.remove(path)

def saveString (path, str):
    file = open(path, 'a')
    file.write(str + "\n")
    file.close()


# WORDNET FUNCTIONS

"""
Return lemmas of synset
"""
def getLemmas(synset):
    return synset.lemma_names()

def getDefinition(synset):
    return synset.definition()