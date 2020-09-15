import nltk
import spacy
from spacy import displacy
from pathlib import Path
import collections

"""
Get part-of-speech of sentence
Input:
    sentence: sentence as string
Output:
    pos_tags: list of tuple (term, POS)
"""
def getPOS(sentence):
    pos_tags = nltk.pos_tag(nltk.word_tokenize(sentence), tagset='universal')
    return pos_tags


"""
https://spacy.io/usage/linguistic-features
"""
def dependencyParsing (sentence):
    print (sentence)
    nlp = spacy.load('en_core_web_sm')
    doc = nlp(sentence)
    #saveTree(doc, "./dependency_plot.png")
    printTreeTable(doc)
    return doc

"""
https://spacy.io/api/token#attributes

obl: oblique nominal
"""
def extractVerbSubjObj (verb, tree):
    verbAddress = next(t.text for t in tree if t.text in verb) # for each token (t) in tree, if t.text is equal to verb get its index (next() get first element) 
    """subjects = list(t.text for t in tree if str(t.head) == verbAddress and "nsubj" in t.dep_ and "NN" in t.tag_)
    objects = list(t.text for t in tree if str(t.head) == verbAddress and "obj" in t.dep_ and "NN" in t.tag_)
    obls = list(t.text for t in tree if str(t.head) == verbAddress and "obl" in t.dep_ and "PRP" not in t.tag_)"""
    subjects = list(t.text for t in tree if str(t.ancestors) == verbAddress and "nsubj" in t.dep_ and "NN" in t.tag_)
    objects = list(t.text for t in tree if str(t.ancestors) == verbAddress and "obj" in t.dep_ and "NN" in t.tag_)
    obls = list(t.text for t in tree if str(t.ancestors) == verbAddress and "obl" in t.dep_ and "PRP" not in t.tag_)
    #print (subjects, objects, obls)

    return subjects, objects, obls


def getFrequency (instances, arg):
    count = []
    if arg == "subjs_ss":
        count = collections.Counter([s for i in instances for s in i.subjs_ss]).most_common()
    elif arg == "objs_ss":
        count = collections.Counter([s for i in instances for s in i.objs_ss]).most_common()
    elif arg == "obls_ss":
        count = collections.Counter([s for i in instances for s in i.obls_ss]).most_common()
    elif arg == "_":
        count = collections.Counter(instances).most_common()
    return count

"""
Save an .svg image of tree
Input:
    doc: tree
    path: path where to save file
"""
def saveTree(doc, path):
    svg = displacy.render(doc, style="dep")
    output_path = Path(path) # you can keep there only "dependency_plot.svg" if you want to save it in the same folder where you run the script 
    output_path.open("w", encoding="utf-8").write(svg)

"""
Print in terminal a table containing tree token information
Input: 
    tree: part-of-speech of sentence (tree)
"""
def printTreeTable(tree):
    # TODO valutare di usare PrettyTable
    print ("=================================================================================")
    print("Index", "\t | ", "Text", "\t\t | ","POS", "\t | " , "TAG",  "\t | " , "Head", "\t | ", "Syntactic dep")
    print ("=================================================================================")
    for token in tree:
        print(token.i, "\t | ", token.text, "\t\t | ",token.pos_, "\t | " , token.tag_,  "\t | " , token.head , "\t | " , token.dep_)
        #token.dep_,token.shape_, token.is_alpha, token.is_stop)
        #print (token.text, token.tag_, token.head.text, token.dep_)"""
