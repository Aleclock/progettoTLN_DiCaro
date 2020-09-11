import csv
#import Similarity as ss
from Similarity import *
from prettytable import PrettyTable

# cd /Users/aleclock/Desktop/uni/TLN/dicaro/progettoTLN_DiCaro/es00_Similarity

"""
Allow to load a csv file
Input:
    path: file path
Output:
    dataset: dictionary with following keys: conc_generic, conc_specific, abst_generic, abst_specific)
"""
def load_csv(path):
    dataset = {
        'conc_generic': [],
        'conc_specific': [],
        'abst_generic': [],
        'abst_specific': []
    }
    with open(path, 'r') as fileCSV:
        for row in fileCSV.readlines()[1:]:
            temp = row.split(";")
            temp[-1] = temp[-1].replace('\n', '')

            dataset["conc_generic"].append(temp[1])
            dataset["conc_specific"].append(temp[2])
            dataset["abst_generic"].append(temp[3])
            dataset["abst_specific"].append(temp[4])

    return dataset

def main():
    definitions = load_csv('./definizioni.csv')
    similarity = {
        'conc_generic': [],
        'conc_specific': [],
        'abst_generic': [],
        'abst_specific': []
    }

    # ---------------------------------------------
    # ----  CALCOLO SIMILARITA'
    # Per ogni set di definizioni (definizioni di un termine) vengono effettuate le seguenti operazioni:
    #   - preprocessing (tokenizzazione, rimozione stopword e punteggiatura, stemming)
    #   - calcolo similarità media tra le definizioni di un termine
    # ---------------------------------------------
    for d in definitions:
        dProcessed = preProcess(definitions[d])
        vSimilarity = getSimilarity(dProcessed)
        similarity[d].append(vSimilarity)

    table = PrettyTable()
    table.field_names = ["", "Abstract", "Concrete"]
    table.add_row(["Generic" , 
        round(similarity["abst_generic"][0],2), 
        round(similarity["conc_generic"][0],2)])

    table.add_row(["Specific", 
        round(similarity["abst_specific"][0],2), 
        round(similarity["conc_specific"][0],2)])
    print(table)

main()