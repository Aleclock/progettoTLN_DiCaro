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
    
    for d in definitions: # for each term definitions
        dProcessed = preProcess(d)
        word = getCommonTerms(dProcessed,10)
        print ("----")
    
    """"
    table = PrettyTable()
    table.field_names = ["", "Abstract", "Concrete"]
    table.add_row(["Generic" , similarity["abst_generic"][0], similarity["conc_generic"][0]])
    table.add_row(["Specific", similarity["abst_specific"][0], similarity["conc_specific"][0]])
    print(table)"""

main()