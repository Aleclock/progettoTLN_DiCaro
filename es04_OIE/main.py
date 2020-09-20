import nltk
from nltk.corpus import brown

from parsingUtils import *

#cd /Users/aleclock/Desktop/uni/TLN/dicaro/progettoTLN_DiCaro/es04_OIE

def extractSencenses(limit):
    sentences = []
    list_sent = brown.sents()
    for sent in list_sent[:limit]:
        sentences.append(" ".join(sent))
    return sentences
    

def main():
    sentences = extractSencenses(30)
    
    # ---------------------------------------------
    # ----  CALCOLO SIMILARITA'
    # Per ogni frase estratta dal Brown, determino l'albero a dipendenze (tramite spacy), il verbo principale e i relativi soggetti/oggetti
    # ---------------------------------------------

    for s in sentences:
        #print (s)

        tree = dependencyParsing (s) # Siccome ogni frase è una lista di termini è necessario unirle (perchè previsto da spacy)
        verb = extractMainVerb(tree)
        if verb:
            subjs, objs = extractVerbSubjObj (tree, verb) # sentences arguments (fillers)

            #printTreeTable(tree)
            #saveTree(tree, "./output/", str(sentences.index(s)))

            verbalPhrase = geVerbDependency(tree, verb)

            if subjs and objs:
                for sub in subjs:
                    #print ([t.text for t in sub.subtree])
                    #arg1 = getArgDependency(tree, sub)
                    arg1 = orderArguments(getDependency(tree, sub, 1))
                for obj in objs:
                    #arg2 = getArgDependency(tree, obj)
                    arg2 = orderArguments(getDependency(tree, obj, 1))
                                
                arg1 = joinArg(arg1)
                verbalPhrase = joinArg(verbalPhrase)
                arg2 = joinArg(arg2)

                print ([arg1, verbalPhrase, arg2])
        #print ("----")

main()