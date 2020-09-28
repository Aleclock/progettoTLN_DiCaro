import os
import nltk
from nltk.stem import WordNetLemmatizer
from nltk.corpus import brown
from leskUtils import lesk
from nltk.wsd import lesk as leskNLTK
import matplotlib.pyplot as plt
import numpy as np

from utils import *

#nltk.download('brown')


os.chdir("/Users/aleclock/Desktop/uni/TLN/dicaro/progettoTLN_DiCaro/es02_hanks")

class VerbInstance:
    def __init__(self, sentence, subjs, objs):
        self.sentence = sentence
        self.subjs = subjs
        self.objs = objs
        self.subjs_ss = []
        self.objs_ss = []


"""
Extract from Brown Corpus sentences containing chosen verb
https://www.nltk.org/_modules/nltk/corpus/reader/categorized_sents.html#CategorizedSentencesCorpusReader.sents
Input:
    verb: chosen verb
    verbs_pos: part-of-speech of verbs
Output:
    sentences: list of sentences (each sentence is a string)
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
                if word == verb:
                    sentences.append(" ".join(sent))
    return sentences



def main():

    # ---------------------------------------------
    # ----      0. SCELTA DEL VERBO TRANSITIVO - Scegliere un verbo transitivo (min valenza = 2)
    # ---------------------------------------------

    verbs_pos = ['VB', 'VBD', 'VBG', 'VBN', 'VBP', 'VBZ']
    personal_pronouns = ['i', 'you', 'he', 'she', 'we', 'they', 'them', 'him', 'her', 'us']
    #verb = "watch"
    #verb = "get"
    verb = "play"

    # ---------------------------------------------
    # ----      1. ESTRAZIONI FRASI - Recuperare da un corpus n istanze in cui esso viene usato
    # ---------------------------------------------

    #sentences = extractBrownSentences(verb, verbs_pos)
    #clear_file("./sentences_get.txt")
    #sentences = loadList("./sentences_watch.txt")
    #saveList("./sentences_get.txt", sentences)
    sentences = loadList("./sentences_play.txt")
    #sentences = loadList("./sentences_get.txt")

    print ("__ Loaded " + str(len(sentences)) + " sentences")

    instances = [] # List of verb istance [sentence, subj, obj, obl, subj_ss, obj_ss, obl_ss] ss: supersense

    #clear_file("./results.txt")

    for s in sentences[:]:

        # ---------------------------------------------
        # ----      2. PARSING
        # ---------------------------------------------
        
        tree = dependencyParsing (s) # Siccome ogni frase è una lista di termini è necessario unirle (perchè previsto da spacy)
        #printTreeTable(tree)
        subjects, objects = extractVerbSubjObj (verb, tree) # sentences arguments (fillers)

        vi = VerbInstance(s, subjects, objects)

        # ------------------------------------------------------
        # ----      3. DISAMBIGUAZIONE E CALCOLO SUPER SENSI
        # ------------------------------------------------------

        # Se ci sono i filler nella frase (valenza = 2), allora effettua la disambiguazione degli elementi (con Lesk)
        if subjects and objects: 
            #saveTree(tree, "./graph_play/", str(s[:20].replace(" ", "_")))
            #saveToFile("./results/filler_play.txt", str((subjects,objects)))

            for subj in subjects:
                if subj in personal_pronouns:
                    vi.subjs_ss.append ('noun.person')
                elif subj == 'it':
                    vi.subjs_ss.append ('noun.object')
                else:
                    #bestSense = lesk(subj, s) # personal lesk function
                    bestSense = leskNLTK(s, subj, 'n') # NLTK lesk funcion
                    if bestSense is not None:
                        vi.subjs_ss.append ((bestSense.lexname()))  # lexname() return WordNet supersense

            for obj in objects:
                if obj in personal_pronouns:
                    vi.objs_ss.append ('noun.person')
                elif obj == 'it':
                    vi.objs_ss.append ('noun.object')
                else:
                    #bestSense = lesk(obj, s)
                    bestSense = leskNLTK(s, obj, 'n')
                    if bestSense is not None:
                        vi.objs_ss.append (bestSense.lexname())

            instances.append(vi)

    print ("__ Parsing and disambiguation completed")
    
    # ---------------------------------------------
    # ----      4. CALCOLO DELLE FREQUENZE
    # ---------------------------------------------
    
    # Conteggio dei supersensi sui singoli argomenti
    freq_subj = getFrequency (instances, "subjs_ss")
    freq_obj = getFrequency (instances, "objs_ss")

    semClusters = []   # Semantic clusters frequency
    
    for i in instances:
        #saveToFile("./results/instances_play.txt", str((i.subjs_ss,i.objs_ss)))
        if i.subjs_ss != [] and i.objs_ss != []:
            for s in i.subjs_ss:
                for obj in i.objs_ss:
                    semClusters.append((s, obj))

    semClusters_freq = getFrequency(semClusters, "_")

    print ("Total sentences: " + str(len(instances)))
    print ("Number of semantic clusters " + str(len(semClusters_freq)))
    print ("\nfrequency of subjs: " + str(freq_subj) + "\n")
    print ("\nfrequency of obj: " + str(freq_obj) + "\n")
    print ("\nfrequency semantic clusters:" + str(semClusters_freq))

    fig, ax = plt.subplots()

    supersenses, frequencies = zip(*semClusters_freq[:15])
    y_axis = np.arange(len(supersenses))
    ax.barh(y_axis, frequencies, align='edge', color='gray', ecolor='black')
    ax.set_xlabel('Frequencies')
    ax.set_title('Semantic clusters (' + str(verb) + ")")
    ax.set_yticks(y_axis)
    ax.set_yticklabels(supersenses, fontsize=9)
    plt.subplots_adjust(left=0.25)
    plt.subplots_adjust(bottom=0.25)
    plt.show()

main()