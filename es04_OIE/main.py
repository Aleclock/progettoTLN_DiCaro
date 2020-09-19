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
    sentences = extractSencenses(15)
    
    # ---------------------------------------------
    # ----  CALCOLO SIMILARITA'
    # Per ogni frase estratta dal Brown, determino l'albero a dipendenze (tramite spacy), il verbo principale e i relativi soggetti/oggetti
    # ---------------------------------------------

    for s in sentences:
        tree = dependencyParsing (s) # Siccome ogni frase è una lista di termini è necessario unirle (perchè previsto da spacy)
        verb = extractVerbSubjObj (tree) # sentences arguments (fillers)
        #printTreeTable(s, tree)
        #saveTree(tree, "./output/", str(sentences.index(s)))
        print ("----")

main()