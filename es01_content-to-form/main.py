import csv
from Similarity import *
from prettytable import PrettyTable

# cd /Users/aleclock/Desktop/uni/TLN/dicaro/progettoTLN_DiCaro/es01_content-to-form

"""
Load csv file
Input:
    path: file path
Output:
    dataset: list of lists of definitions
"""
def load_csv(path):
    dataset = []
    with open(path, 'r') as fileCSV:
        for row in fileCSV.readlines()[1:]:
            temp = row.split(";")
            dataset.append(temp[1:])
    return dataset


def main():
    definitions = load_csv('./concept_definitions.csv')
    correct_terms = ["justice", "patience", "greed", "politics", "food", "radiator", "vehicle", "screw"] # solution
    algo_terms = []
    
    clear_file("out.txt")
    
    for d in definitions: # for each term definitions
        saveString("out.txt", "------------------------------------\n" + correct_terms[definitions.index(d)] + "\n------------------------------------")
        #lemmas = getCommonTerms(preProcess(d))
        lemmas = getCommonTerms(d)
        synsets = getSynsetsFromLemma(lemmas[:10], 3, 3) # most n common lemmas, hyponyms limit, hypernyms limit
        saveString("out.txt", "\n************************************\n" + str(lemmas) + "\n************************************\n\n")
        saveString("out.txt", "\n************************************\n" + str(synsets) + "\n************************************\n\n")
        best_sense, overlap = getBestSense(synsets,lemmas)
        algo_terms.append (best_sense)
        saveString("out.txt", "\n\n====================================\n" + str(best_sense) + " , " +  str(round(overlap,2)) + "\n====================================\n\n\n\n")
        print ("----")
    
    
    # PRINT RESULTS
    table = PrettyTable()
    table.field_names = ["Correct term", "Calculated term", "Definition"]
    table.align["Correct term"] = "l"
    table.align["Calculated term"] = "l"
    table.align["Definition"] = "l"

    for i in range(len(correct_terms)):
        #print(f"concept {i+1} : ({correct_terms[i]})\t -> {algo_terms[i]} | {getLemmas(algo_terms[i])}")
        #table.add_row([correct_terms[i],str(algo_terms[i]),getLemmas(algo_terms[i])])
        table.add_row([correct_terms[i],str(algo_terms[i]), getDefinition(algo_terms[i])])

    print(table)

main()