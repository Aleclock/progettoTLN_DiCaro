import spacy
from nltk.stem import WordNetLemmatizer
from spacy import displacy
from prettytable import PrettyTable
from pathlib import Path
import os, os.path

"""
Extract a dependency parse from a sentence (with spaCy https://spacy.io/usage/linguistic-features)
Input:
    sentence: sentence to parse
Output:
    doc: dependency tree
"""
def dependencyParsing (sentence):
    nlp = spacy.load('en_core_web_sm')
    return nlp(sentence)

"""
Extract subjects and objects of verb selected
Input:
    verb: selected verb
    tree: dependency tree in which find elements
Output:
    subject: nominal subject of verb
    object: object of verb
    
https://spacy.io/api/token#attributes
https://stackoverflow.com/questions/39323325/can-i-find-subject-from-spacy-dependency-tree-using-nltk-in-python
"""
def extractVerbSubjObj (tree):
    mainVerb = next(t.text for t in tree if "ROOT" in t.dep_ and "VB" in t.tag_)
    subjects = list(t.text for t in tree if str(t.head) == mainVerb and "nsubj" in t.dep_)
    objects = list(t.text for t in tree if str(t.head) == mainVerb and "obj" in t.dep_)

    # TODO ripartire da qui, se manca oggetto prendere qualcos'altr
    if not objects:
        print ("manca oggetto")

    return mainVerb





def printTreeTable(sentence, tree):
    table = PrettyTable()
    table.field_names = ["Index", "Text", "POS", "TAG", "Head", "Syntactic dep"]
    for token in tree:
        table.add_row([str(token.i), str(token.text), str(token.pos_), str(token.tag_), str(token.head), str(token.dep_)])
        #print(token.i, "\t | ", token.text, "\t\t | ",token.pos_, "\t | " , token.tag_,  "\t | " , token.head , "\t | " , token.dep_)
    print(table)

"""
Save an .svg image of dependency tree
Input:
    doc: tree
    path: folder path (necessary for counting index, number of file in folder)
    file_name: name of file
"""
def saveTree(doc, path, file_name):
    svg = displacy.render(doc, style="dep")
    output_path = Path(path + str(file_name + ".svg"))
    output_path.open("w", encoding="utf-8").write(svg)