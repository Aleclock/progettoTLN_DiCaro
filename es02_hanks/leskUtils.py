import nltk
from nltk.corpus import wordnet as wn
from nltk.corpus import stopwords

"""
Calulate beste sense of a word
Input:
    word
    sentence
Output:
    best_sense
"""
def lesk(word,sentences):

    best_sense = None
    max_overlap = 0
    context = bagOfWord(sentences)

    for sense in wn.synsets(word):
        if (best_sense is None):
            best_sense = sense

        signature = bagOfWord(sense.definition())
        examples = sense.examples()
        for ex in examples:
            signature.update(bagOfWord(ex))
        
        overlap = computeOverlap(signature, context)
        if (overlap > max_overlap):
            max_overlap = overlap
            best_sense = sense

    return best_sense

"""
Retrieve synonym from sense
Input: 
    sense
Output: 
    synonyms: list of synonyms
"""
def findSynonym (sense):    # Ritorna una lista di sinonimi
    synonyms = []
    #sense.lemma_names() # si ottiene lo stesso risultato con questa funzione 
    for l in sense.lemmas():
        synonyms.append(l.name())
    return synonyms

"""
Transforms the given sentence according to the bag of words approach, apply lemmatization, stop words and punctuation removal
Input:
    sent: str to transform
Output: 
    bag of words (context)
"""
def bagOfWord(sent):
    stop_words = set(stopwords.words('english'))
    punct = {',', ';', '(', ')', '{', '}', ':', '?', '!'}
    wnl = nltk.WordNetLemmatizer()
    tokens = nltk.word_tokenize(sent)
    tokens = list(filter(lambda x: x not in stop_words and x not in punct, tokens))
    return set(wnl.lemmatize(t) for t in tokens)

"""
Calculate overlap between two sets 
Input:
    signature: sense context
    context: sentence context
Output:
    length of intersection set
"""
def computeOverlap(signature, context):
    intersection = signature.intersection(context)
    return len(intersection)