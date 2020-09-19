import nltk
import matplotlib.pyplot as plt
import re
import numpy as np
import os

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

def saveString (path, str):
    file = open(path, 'a')
    file.write(str + "\n")
    file.close()

def clear_file(path):
    os.remove(path)

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
    print ("Number of sentences: " + str(len(tokens)))
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
    doc = loadDocument("./text_italy01.txt")

    splitPoints = 5
    windows_size = 5
    sequences = textWindowing(doc, windows_size) # get text windows (5: sentences in each windows)

    print ("Number of windows: " + str(len(sequences)))

    #nasari = loadNasari("./asset/dd-small-nasari-15.txt")
    nasari = loadNasari("./asset/dd-nasari.txt")

    result_path = "./output/results_text_italy01_w5.txt"

    clear_file(result_path)

    saveString(result_path, "**************************************")
    saveString(result_path, "Info:")
    saveString(result_path, "./text_italy01.txt")
    saveString(result_path, "./asset/dd-nasari.txt")
    saveString(result_path, "Windows size: " + str(windows_size))
    saveString(result_path, "Number of windows: " + str(len(sequences)))
    saveString(result_path, "**************************************\n\n")

    similarities = []
    similarities_mean = []
    similarities_correlation = [] # based on statistica occurrence

    for i in range(1, len(sequences) - 1):
        prev = getNasariVectors(sequences[i - 1], nasari) # previus sentence
        current = getNasariVectors(sequences[i], nasari)
        foll = getNasariVectors(sequences[i + 1], nasari) # following sentence

        max_sim_prev, mean_sim_prev = getSimilarity(current, prev)
        max_sim_foll, mean_sim_prev = getSimilarity(current, foll)

        corr_prev = getOverlap(sequences[i], sequences[i-1])
        corr_foll = getOverlap(sequences[i], sequences[i+1])

        saveString(result_path, "\nWindow n:\t" + str(i))
        saveString(result_path, "---------------------------\n")
        saveString(result_path, "Prev: \n" + str(sequences[i - 1]) + "\n")
        saveString(result_path, "Curr: \n" + str(sequences[i]) + "\n")
        saveString(result_path, "Foll: \n" + str(sequences[i + 1]) + "\n")

        saveString(result_path, "++++ Similarity \b")
        saveString(result_path, "\tMax similarity: \t" + str(round(max_sim_prev,2)) + " , " + str(round(max_sim_foll,2)) + " | \t" + str(round((max_sim_prev + max_sim_foll) / 2,2)))
        saveString(result_path, "\tStatistic similarity: \t" + str(round(corr_prev,2)) + " , " + str(round(corr_foll,2)) + " | \t" + str(round((corr_prev + corr_foll) / 2,2)))

        similarities.append((max_sim_prev + max_sim_foll) / 2)
        similarities_mean.append((mean_sim_prev + mean_sim_prev) / 2)
        similarities_correlation.append((corr_prev + corr_foll) / 2)

    #minimum = (np.diff(np.sign(np.diff(similarities))) > 0).nonzero() [0] + 1 # local min

    split_maxSimilarity = getSplitPoints(similarities)
    split_corrSimilarity = getSplitPoints(similarities_correlation)

    #splits = numpy.argsort(splits) # Returns the indices that would sort an array
    split_maxSimilarity = split_maxSimilarity[:splitPoints]
    split_corrSimilarity = split_corrSimilarity[:splitPoints]

    # text_italy01.txt
    breackSentences = [
        "The islands of Sardinia, Corsica, Sicily and Malta were added to Italy by Diocletian in 292 AD",
        "These territories are the comuni of: Livigno, Sexten, Innichen, Toblach (in part), Chiusaforte, Tarvisio, Graun im Vinschgau (in part), which are all part of the Danube's drainage basin, while the Val di Lei constitutes part of the Rhine's basin and the islands of Lampedusa and Lampione are on the African continental shelf",
        "The 1814 Congress of Vienna restored the situation of the late 18th century, but the ideals of the French Revolution could not be eradicated, and soon re-surfaced during the political upheavals that characterised the first part of the 19th century",
        "Italy has a strong cooperative sector, with the largest share of the population (4,5%) employed by a cooperative in the EU",
        "As of 2016, Italian films have also won 12 Palmes d'Or (the second-most of any country), 11 Golden Lions and 7 Golden Bears"
    ]

    values = []
    for s in breackSentences:
        for i in range(0, len(sequences)):
            tokenized = nltk.word_tokenize(s.lower())
            if set(tokenized).issubset(sequences[i]):
                values.append(i)
        
    """result = [i for i in sequences[i] if i.startswith(tuple(tokenized))]
    print (len(result), len(tokenized))
    print ("--")"""

    # Plot similarities

    plt.xlabel("Sequence number ( windows size = " + str(windows_size) + ")")
    plt.ylabel("Coesion")

    plt.plot(similarities, color = "k", linewidth=1)
    #plt.axhline(y = mean, color = "k" , ls = ":", linewidth = 0.5)
    
    for val in values:
        plt.axvline(x= val, ls = "-", color='r', linewidth=2)
    for split in split_maxSimilarity:
        plt.axvline(x= split[0], ls = "-", color='g', linewidth=1.5)
    """for mini in minimum:
        plt.axvline(x= mini, ls = ":", color='brown', linewidth=1)"""

    plt.axvline(x= values[0], ls = "-", color='r', linewidth=1, label = "Correct breakpoints")
    plt.axvline(x= split_maxSimilarity[0][0], ls = "-", color='g', linewidth=1, label = "Calculated breakpoints")
    plt.legend()

    # Plot similarities and similarities_correlation values

    fig, axs = plt.subplots(2)
    axs[0].plot(similarities, color = "k", linewidth=1)
    axs[1].plot(similarities_correlation, color = "k", linewidth=1)

    for val in values:
        axs[0].axvline(x= val, ls = "-", color='r', linewidth=2)
        axs[1].axvline(x= val, ls = "-", color='r', linewidth=2)
    for split in split_maxSimilarity:
        axs[0].axvline(x= split[0], ls = "-", color='g', linewidth=1.5)
    for split in split_corrSimilarity:
        axs[1].axvline(x= split[0], ls = "-", color='g', linewidth=1.5)
    
    axs[0].axvline(x= values[0], ls = "-", color='r', linewidth=1, label = "Correct breakpoints")
    axs[0].axvline(x= split_maxSimilarity[0][0], ls = "-", color='g', linewidth=1, label = "Calculated breakpoints")
    axs[1].axvline(x= values[0], ls = "-", color='r', linewidth=1, label = "Correct breakpoints")
    axs[1].axvline(x= split_corrSimilarity[0][0], ls = "-", color='g', linewidth=1, label = "Calculated breakpoints")

    axs[0].set(xlabel = "", ylabel = "Coesion value")
    axs[1].set(xlabel = "Sequence number ( windows size = " + str(windows_size) + ")", ylabel = "Coesion value")

    handles, labels = axs[1].get_legend_handles_labels()
    fig.legend(handles, labels, loc='upper center', prop={'size': 9}, ncol=2)

    plt.show()
    

main()