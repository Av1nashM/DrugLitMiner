import spacy

def load_model():
    nlp = spacy.load("en_ner_bc5cdr_md") #load the pretrained model
    return nlp


def extract_drugs(text, nlp):
    doc = nlp(text)
    drugs = []
    for ent in doc.ents:
        if ent.label_ == "CHEMICAL":
            drugs.append(ent.text)
    return list(set(drugs))

def extract_diseases(text,nlp):
    doc = nlp(text)
    diseases = []
    for ent in doc.ents:
        if ent.label == "DISEASE":
            diseases.append(ent.text)
        return list(set(diseases))