import nltk
import matplotlib.pyplot as plt
import re
import itertools
import pandas as pd
import numpy as np


from utils import * 

#cd /Users/aleclock/Desktop/uni/TLN/dicaro/progettoTLN_DiCaro/es03_textSegmentation


"""
Load document in path line by line
Input:
    path: file path
Output:
    document as string
"""
def loadDocument(path):
    with open(path) as file:
        lines = file.readlines()
    return ''.join(lines)

"""
Apply text windowing, divide a text into windows with specified number of words
TODO valutare di dividere il testo in frasi
Input:
    document: document to tokenize/divide
    length: windows dimension
Output:
    sequences: list of windows
"""
def textWindowing(document, length):
    sequences = []
    tokens = re.split("\.\s+", document)
    tokens = [nltk.word_tokenize(sentence.lower()) for sentence in tokens]
    #tokens = nltk.word_tokenize(document.lower())
    #print (tokens)
    j = 0
    for i in range(length, len(tokens) + 1, length):
        #sequences.append(list(itertools.chain(tokens[j:i])))
        window = sum(tokens[j:i],[])
        sequences.append(window)
        j = i
    
    if len(tokens) != j:
        diff = len(tokens) - j
        sequences.append(sum(tokens[-diff:],[]))
    return sequences

def main():
    #doc = loadDocument("./document.txt")
    doc = loadDocument("./text_italy00.txt")
    print ("Number of sentences: " + str(len(doc)))

    sequences = textWindowing(doc, 5) # get text windows (20: size windows)

    print ("Number of windows: " + str(len(sequences)))

    nasari = loadNasari("./asset/dd-small-nasari-15.txt")

    similarities = []

    for i in range(1, len(sequences) - 1):
        prev = getNasariVectors(sequences[i - 1], nasari) # previus sentence
        current = getNasariVectors(sequences[i], nasari)
        foll = getNasariVectors(sequences[i + 1], nasari) # following sentence

        sim_prev = getSimilarity(current, prev)
        sim_foll = getSimilarity(current, foll)

        similarities.append((sim_prev + sim_foll) / 2)

    breackSentences = [
        "The islands of Sardinia, Corsica, Sicily and Malta were added to Italy by Diocletian in 292 AD",
        "Nearly half a million Italians (including civilians) died in the conflict, and the Italian economy had been all but destroyed; per capita income in 1944 was at its lowest point since the beginning of the 20th century",
        "These territories are the comuni of: Livigno, Sexten, Innichen, Toblach (in part), Chiusaforte, Tarvisio, Graun im Vinschgau (in part), which are all part of the Danube's drainage basin, while the Val di Lei constitutes part of the Rhine's basin and the islands of Lampedusa and Lampione are on the African continental shelf",
        "The rest of the seats were taken by Five Star Movement, Matteo Renzi's Democratic Party along with Achammer and Panizza's South Tyrolean People's Party & Trentino Tyrolean Autonomist Party in a centre-left coalition and the independent Free and Equal party",
    ]

    values = []
    for s in breackSentences:
        for i in range(1, len(sequences) - 1):
            tokenized = nltk.word_tokenize(s.lower())

            if set(tokenized).issubset(sequences[i]):
                values.append(i)
        
        """result = [i for i in sequences[i] if i.startswith(tuple(tokenized))]
        print (len(result), len(tokenized))
        print ("--")"""
        
    """# https://stackoverflow.com/questions/48023982/pandas-finding-local-max-and-min
    df = pd.DataFrame(similarities, columns=['data'])
    minimum = df.data[(df.data.shift(1) > df.data) & (df.data.shift(-1) > df.data)]

    print (minimum)"""

    plt.plot(similarities)
    for val in values:
        plt.axvline(x= val, ls = "--", color='k', linewidth=1)
    plt.show()
    

main()