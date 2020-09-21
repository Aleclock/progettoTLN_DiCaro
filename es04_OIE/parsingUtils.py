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

def extractMainVerb(tree):
    return next((t for t in tree if "ROOT" in t.dep_ and "VB" in t.tag_), None)

"""
Extract subjects and objects of verb selected
Input:
    verb: selected verb
    tree: dependency tree in which find elements
Output:
    subject: nominal subject of verb
    object: object of verb
    
https://spacy.io/api/token#attributes
https://spacy.io/api/annotation
https://stackoverflow.com/questions/39323325/can-i-find-subject-from-spacy-dependency-tree-using-nltk-in-python
"""
def extractVerbSubjObj (tree, verb):
    subjs = list(t for t in tree if str(t.head) == verb.text and "nsubj" in t.dep_)
    objs = list(t for t in tree if str(t.head) == verb.text and "obj" in t.dep_)

    if not objs:
        objs = list(t for t in tree if str(t.head) == verb.text and "ccomp" in t.dep_)

    return subjs, objs

"""
Recursive research of dependence of argument
Input:
    tree: dependence tree
    argument: argument to research
Output:
    set of dependence of argument
"""
def getDependency(tree, argument, limit):
    full_arg = set ()
    if limit > 0:
        for arg in [t for t in tree if str(t.head) == argument.text and t.head.i == argument.i]:
            full_arg |= set(getDependency(tree, arg, limit - 1))
    return full_arg | set([t for t in tree if str(t.head) == argument.text] + [argument])

def getArgDependency(tree, argument):
    dep = sorted ([argument] + [t for t in tree if str(t.head) == argument.text], key=lambda v: v.i)
    return dep

def geVerbDependency(tree, verb):
    return sorted([verb] + [t for t in tree if str(t.head) == verb.text and "aux" in t.dep_], key = lambda v: v.i)

def orderArguments(arguments):
    return sorted(arguments, key=lambda v: v.i)

def joinArg(tokens):
    #return " ".join([t.text for t in tokens if "punct" not in t.dep_])
    return " ".join([t.text for t in tokens])

def printTreeTable(tree):
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