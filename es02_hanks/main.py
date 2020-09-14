import os
import ast 
import nltk
from nltk.stem import WordNetLemmatizer
from nltk.corpus import brown

from utils import *

#nltk.download('brown')


os.chdir("/Users/aleclock/Desktop/uni/TLN/dicaro/progettoTLN_DiCaro/es02_hanks")

def loadList(path):
    sentences_list = []
    file = open(path,"r",encoding="utf-8")
    for line in file.readlines():
        sentences_list.append(ast.literal_eval(line))
    return sentences_list

"""
Save the annotation in form:    type, frame_name, element, synset
Input:
    path: path of file
    list: list
"""
def saveList (path, list):
    file = open(path, 'a')
    for i in list:
        file.write(str(i) + "\n")
    file.close()

"""
Delete file in path
Input: 
    path: path of file
"""
def clear_file(path):
    os.remove(path)

"""
Extract from Brown Corpus sentences containing chosen verb
Input:
    verb: chosen verb
    verbs_pos: part-of-speech of verbs
Output:
    sentences: list of sentences, each sentence is a list of words
"""
def extractBrownSentences(verb, verbs_pos):
    lemmatizer = WordNetLemmatizer()

    list_sent = brown.sents()
    sentences = []
    for sent in list_sent:
        tags = dict(nltk.pos_tag(sent))
        for word in sent:
            if tags[word] in verbs_pos:
                word = lemmatizer.lemmatize(word, 'v')
                if word == verb:
                    sentences.append(sent)
    return sentences

def main():
    #verbs = ["watch", "watching"]

    # ---------------------------------------------
    # ----      0. SCELTA DEL VERBO TRANSITIVO - Scegliere un verbo transitivo (min valenza = 2)
    # ---------------------------------------------

    verbs_pos = ['VB', 'VBD', 'VBG', 'VBN', 'VBP', 'VBZ']
    #verb = "watch"
    verb = ["send", "sent", "sending"]

    # ---------------------------------------------
    # ----      1. ESTRAZIONI FRASI - Recuperare da un corpus n istanze in cui esso viene usato
    # ---------------------------------------------

    #sentences = extractBrownSentences(verb, verbs_pos)
    #clear_file("./sentences.txt")
    #saveList("./sentences.txt", sentences)
    # TODO valutare di salvare le frasi come testo e non come lista (così non serve fare il join nella funzione dependencyParsing())
    sentences = loadList("./sentences.txt")

    # ---------------------------------------------
    # ----      2. PARSING E DISAMBIGUAZIONE
    # ---------------------------------------------

    for s in sentences[:]:
        tag = getPOS(s)
        tree = dependencyParsing (" ".join(s)) # Siccome ogni frase è una lista di termini è necessario unirle (perchè previsto da spacy)
        subjects, objects, obls = extractVerbSubjObj (verb, tree)
        print ("----")


main()