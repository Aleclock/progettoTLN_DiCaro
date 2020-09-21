import nltk
from nltk.stem import WordNetLemmatizer
import spacy
from spacy import displacy
from pathlib import Path
import os, os.path
import collections
from prettytable import PrettyTable

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
Extract a dependency parse from a sentence (with spaCy https://spacy.io/usage/linguistic-features)
Input:
    sentence: sentence to parse
Output:
    dependency tree
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
https://spacy.io/api/annotation
https://stackoverflow.com/questions/39323325/can-i-find-subject-from-spacy-dependency-tree-using-nltk-in-python
"""
def extractVerbSubjObj (verb, tree):
    subj_dept = ['nsubj', 'nsubjpass']
    obj_dept = ['dobj', 'obj']

    lemmatizer = WordNetLemmatizer()
    verbAddress = next(t.text for t in tree if lemmatizer.lemmatize(t.text, 'v') == verb)
    subjects = list(t.text for t in tree if str(t.head) == verbAddress and t.dep_ in subj_dept)
    objects = list(t.text for t in tree if str(t.head) == verbAddress and t.dep_ in obj_dept) # and "NN" in t.tag_)
    #subjects = list(t.text for t in tree if str(t.head) == verbAddress and "nsubj" in t.dep_ and "NN" in t.tag_)
    #objects = list(t.text for t in tree if str(t.head) == verbAddress and "obj" in t.dep_ and "NN" in t.tag_)
    return subjects, objects


"""
Calculate frequency of most common WordNet supersense. 
Input:
    istances: list of instances with the form (sentence, subjs, objs, subjs_ss, objs_ss)
    arg: argument to consider (subjs_ss: subject supersense, objs_ss: object supersense, _: consider the whole istance)
"""
def getFrequency (instances, arg):
    count = []
    if arg == "subjs_ss":
        a = [s for i in instances for s in i.subjs_ss]
        print ("subjs_ss " + str(len(a)))
        count = collections.Counter([s for i in instances for s in i.subjs_ss]).most_common()
    elif arg == "objs_ss":
        b = [s for i in instances for s in i.objs_ss]
        print ("objs_ss " + str(len(b)))
        count = collections.Counter([s for i in instances for s in i.objs_ss]).most_common()
    elif arg == "_":
        count = collections.Counter(instances).most_common()
    return count

"""
Save an .svg image of dependency tree
Input:
    doc: tree
    path: folder path (necessary for counting index, number of file in folder)
    file_name: name of file
"""
def saveTree(doc, path, file_name):
    svg = displacy.render(doc, style="dep")
    output_path = Path(path + str(len(os.listdir(path))) + "_" + file_name + ".svg")
    output_path.open("w", encoding="utf-8").write(svg)

"""
Print in terminal a table containing tree token information
Input: 
    tree: part-of-speech of sentence (tree)
"""
def printTreeTable(tree):
    table = PrettyTable()
    table.field_names = ["Index", "Text", "POS", "TAG", "Head", "Syntactic dep"]
    for token in tree:
        table.add_row([str(token.i), str(token.text), str(token.pos_), str(token.tag_), str(token.head), str(token.dep_)])
    print(table)

# ----------------------------------------------------
# Following funcions allow to load or save file
# ----------------------------------------------------

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
        file.write(i + "\n")
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