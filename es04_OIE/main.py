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
    
    print ("Sentence | Triple")
    print ("------------ | ------------")

    for s in sentences:
        #print (s)

        tree = dependencyParsing (s)
        verb = extractMainVerb(tree)
        if verb:
            subjs, objs = extractVerbSubjObj (tree, verb) # sentences arguments (fillers)

            #printTreeTable(tree)
            #saveTree(tree, "./output/", str(sentences.index(s)))

            if subjs and objs:
                verbalPhrase = geVerbDependency(tree, verb)

                for sub in subjs:
                    #https://github.com/explosion/spaCy/issues/259
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

                print (s + " | [" + arg1 + "] <br/> [" + verbalPhrase + "] <br/> [" + arg2 + "]")

                #print ([arg1, verbalPhrase, arg2])
        #print ("----")

main()