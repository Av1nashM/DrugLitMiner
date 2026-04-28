import csv

def load_vocabulary(filepath):
    vocab = set()
    with open(filepath, 'r', encoding="utf-8") as f:
        reader = csv.reader(f, delimiter='\t')
        for row in reader:
            if row:
                drug_name = row[0].strip().lower()
                if drug_name:
                    vocab.add(drug_name)
                
    return vocab        
        