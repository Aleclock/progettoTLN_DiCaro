import os
import nltk
from nltk.corpus import brown

from parsingUtils import *

#cd /Users/aleclock/Desktop/uni/TLN/dicaro/progettoTLN_DiCaro/es04_OIE
os.chdir("/Users/aleclock/Desktop/uni/TLN/dicaro/progettoTLN_DiCaro/es04_OIE")

"""
Extract sentences from Brown corpus
Input:
    limit: number of sentences to retrieve
Output:
    sentences: list of sentences
"""
def extractSencenses(limit):
    sentences = []
    list_sent = brown.sents(categories = "hobbies")
    for sent in list_sent[:limit]:
        sentences.append(" ".join(sent))
    return sentences

def clear_file(path):
    os.remove(path)

def saveString (path, str):
    file = open(path, 'a')
    file.write(str + "\n")
    file.close()
    

def main():

    # ---------------------------------------------
    # ----      0. Extract sentences
    # ---------------------------------------------

    sentences = extractSencenses(30)

    for s in sentences:

        # ---------------------------------------------
        # ----      1. Calculate dependency tree, main verb and fillers
        # ---------------------------------------------
        
        tree = dependencyParsing (s)
        verb = extractMainVerb(tree)
        if verb:
            subjs, objs = extractVerbSubjObj (tree, verb) # sentences arguments (fillers)

            #printTreeTable(tree)
            #saveTree(tree, "./output/", str(sentences.index(s)) + "_hobbies")

            if subjs and objs:

                # ---------------------------------------------
                # ----      2. Calculate verbal phrase and arguments (arg1, arg2)
                # ---------------------------------------------

                verbalPhrase = getVerbDependency(tree, verb)

                for sub in subjs:
                    #print ([t.text for t in sub.subtree])
                    #arg1 = getArgDependency(tree, sub)
                    arg1 = orderArguments(getDependency(tree, sub, 1))
                for obj in objs:
                    #arg2 = getArgDependency(tree, obj)
                    #print ([t.text for t in obj.subtree])
                    arg2 = orderArguments(getDependency(tree, obj, 1))

                arg1 = joinArg(arg1)
                verbalPhrase = joinArg(verbalPhrase)
                arg2 = joinArg(arg2)
                
                print (s)
                print ([arg1, verbalPhrase, arg2])
                print ("----")

main()