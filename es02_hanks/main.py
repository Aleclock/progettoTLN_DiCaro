import os
import nltk
from nltk.stem import WordNetLemmatizer
from nltk.corpus import brown
from leskUtils import lesk

from utils import *

#nltk.download('brown')


os.chdir("/Users/aleclock/Desktop/uni/TLN/dicaro/progettoTLN_DiCaro/es02_hanks")

class VerbInstance:
    def __init__(self, sentence, subjs, objs, obls):
        self.sentence = sentence
        self.subjs = subjs
        self.objs = objs
        self.obls = obls
        self.subjs_ss = []
        self.objs_ss = []
        self.obls_ss = []

def loadList(path):
    sentences_list = []
    file = open(path,"r",encoding="utf-8")
    for line in file.readlines():
        sentences_list.append(line.replace("\n", ""))
    file.close()
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
        file.write(" ".join(i) + "\n")
    file.close()

def saveToFile(path, string):
    file = open(path, 'a')
    file.write (str(string) + "\n")
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
https://www.nltk.org/_modules/nltk/corpus/reader/categorized_sents.html#CategorizedSentencesCorpusReader.sents
Input:
    verb: chosen verb
    verbs_pos: part-of-speech of verbs
Output:
    sentences: list of sentences, each sentence is a list of words
"""
def extractBrownSentences(verb, verbs_pos):
    lemmatizer = WordNetLemmatizer()

    list_sent = brown.sents() #  Return all sentences in the corpus or in the specified file(s).
    sentences = []
    for sent in list_sent:
        tags = dict(nltk.pos_tag(sent))
        for word in sent:
            if tags[word] in verbs_pos:
                word = lemmatizer.lemmatize(word, 'v')
                if word in verb:
                    sentences.append(sent)
    return sentences

def main():

    # ---------------------------------------------
    # ----      0. SCELTA DEL VERBO TRANSITIVO - Scegliere un verbo transitivo (min valenza = 2)
    # ---------------------------------------------

    verbs_pos = ['VB', 'VBD', 'VBG', 'VBN', 'VBP', 'VBZ']
    #verb = ["watch", "watching", "watched", "watches"]
    verb = ["send", "sent", "sending"]

    # ---------------------------------------------
    # ----      1. ESTRAZIONI FRASI - Recuperare da un corpus n istanze in cui esso viene usato
    # ---------------------------------------------

    #sentences = extractBrownSentences(verb, verbs_pos)
    #clear_file("./sentences.txt")
    #saveList("./sentences00.txt", sentences)
    # TODO valutare di salvare le frasi come testo e non come lista (così non serve fare il join nella funzione dependencyParsing())
    #sentences = loadList("./sentences00.txt")
    sentences = loadList("./sentences_ref.txt")

    # ---------------------------------------------
    # ----      2. PARSING
    # ---------------------------------------------

    instances = [] # List of verb istance [sentence, subj, obj, obl, subj_ss, obj_ss, obl_ss] ss: supersense

    for s in sentences[:20]:
        #print (s)
        istance = []

        tag = getPOS(s)
        tree = dependencyParsing (s) # Siccome ogni frase è una lista di termini è necessario unirle (perchè previsto da spacy)
        subjects, objects, obls = extractVerbSubjObj (verb, tree) # sentences arguments
        saveToFile("./results.txt", (subjects, objects, obls))

        vi = VerbInstance(s, subjects, objects, obls)

        # ------------------------------------------------------
        # ----      2.1 DISAMBIGUAZIONE E CALCOLO SUPERSENSI
        # ------------------------------------------------------

        if subjects or objects: # Se esiste il soggetto o l'oggetto nella frase, allora effettua la disambiguazione degli elementi (con Lesk)
            #saveToFile("./results.txt", vi.sentence)
            for subj in subjects:
                #print (">>subj: " + subj)
                bestSense = lesk(subj, s)
                if bestSense is not None:
                    vi.subjs_ss.append ((bestSense.lexname()))  # con lexname() si ottiene il supersenso
                else:
                    print ("subj NONE " + subj)
            for o in objects:
                #print (">>obj: " + o)
                bestSense = lesk(o, s)
                if bestSense is not None:
                    vi.objs_ss.append (bestSense.lexname())
                else:
                    print ("obj NONE " + o)
            for o in obls:
                #print (">>obl: " + o)
                bestSense = lesk(o, s)
                if bestSense is not None:
                    vi.obls_ss.append (bestSense.lexname())
                else:
                    print ("obls NONE " + o)
    
            instances.append(vi)

        print ("\n----\n")
    
    # ---------------------------------------------
    # ----      4. CALCOLO DELLE FREQUENZE
    # ---------------------------------------------
    
    # Conteggio dei supersensi sui singoli argomenti
    freq_subj = getFrequency (instances, "subjs_ss")
    freq_obj = getFrequency (instances, "objs_ss")
    freq_obl = getFrequency (instances, "obls_ss")

    co_count = []   # Semantic frequency
    for i in instances:
        for s in i.subjs_ss if i.subjs_ss else [None]:
            for obj in i.objs_ss if i.objs_ss else [None]:
                for obl in i.obls_ss if i.obls_ss else [None]:
                    co_count.append((s, obj, obl))

    co_count_freq = getFrequency(co_count, "_")

    print ("Total sentences: " + str(len(instances)))
    print ("frequency of subjs: " + str(freq_subj) + "\n")
    print ("frequency of obj: " + str(freq_obj) + "\n")
    print ("frequency of obl: " + str(freq_obl) + "\n")

main()