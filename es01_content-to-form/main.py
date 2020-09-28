import os
import csv
from Similarity import *
from prettytable import PrettyTable

# cd /Users/aleclock/Desktop/uni/TLN/dicaro/progettoTLN_DiCaro/es01_content-to-form

os.chdir("/Users/aleclock/Desktop/uni/TLN/dicaro/progettoTLN_DiCaro/es01_content-to-form")

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
   
    for d in definitions[:]: # for each term definitions

        # ---------------------------------------------
        # ----  Determinazione lemmi e synset associati
        # ---------------------------------------------
        lemmas = getCommonTerms(preProcess(d))
        synsets = getSynsetsFromLemma(lemmas[:10], 3, 3) # most n common lemmas, hyponyms limit, hypernyms limit

        # ---------------------------------------------
        # ----  Calcolo del miglior senso
        # ---------------------------------------------
        best_sense, overlap, all_sense = getBestSense(synsets,lemmas)
        algo_terms.append (best_sense)  
        all_sense = sorted(all_sense, key=lambda sense: sense[1], reverse=True)
    
    # ---------------------------------------------
    # ----  Stampa dei risultati
    # ---------------------------------------------
    table = PrettyTable()
    table.field_names = ["Correct term", "Calculated term", "Definition"]
    table.align["Correct term"] = "l"
    table.align["Calculated term"] = "l"
    table.align["Definition"] = "l"

    for i in range(len(correct_terms)):
        table.add_row([correct_terms[i],str(algo_terms[i]), getDefinition(algo_terms[i])])

    print(table)

main()