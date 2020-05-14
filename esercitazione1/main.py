import csv
import Similarity as ss
from prettytable import PrettyTable

# cd /Users/aleclock/Desktop/uni/TLN/dicaro/progettoTLN_DiCaro/esercitazione1

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
    definizioni = load_csv('./definizioni00.csv')
    similarity = {
        'conc_generic': [],
        'conc_specific': [],
        'abst_generic': [],
        'abst_specific': []
    }

    for d in definizioni:
        dProcessed = ss.preProcess(definizioni[d])
        vSimilarity = ss.getSimilarity(dProcessed)
        similarity[d].append(vSimilarity)

    table = PrettyTable()
    table.field_names = ["", "Abstract", "Concrete"]
    table.add_row(["Generic" , similarity["abst_generic"][0], similarity["conc_generic"][0]])
    table.add_row(["Specific", similarity["abst_specific"][0], similarity["conc_specific"][0]])
    print(table)

main()