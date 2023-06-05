import re
import spacy
from nltk.corpus import wordnet



VERB="hit"
CATEGORY_HEIGHT=3
MIN_SENTENCES=4


def parse_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        testo = file.read()
    # Utilizziamo un'espressione regolare per separare il testo in frasi
    # considerando il punto seguito da uno spazio come delimitatore delle frasi
    phrases = re.split('\n', testo)
    return phrases

def tokenize_sentences(dataset):
    tokenized_dataset=[]
    for sentence in dataset:
        tokenized_dataset.append(nlp(sentence))
    return tokenized_dataset

def extract_verb_parameters(tokenized_dataset, verb):
    verb_parameters=[]
    for sentence in tokenized_dataset:
        subject=None
        complement_object=None

        for token in sentence:
            if token.head.lemma_.lower() == verb:
                if token.dep_ == "nsubj":
                    subject = token.dataset_text
                elif token.dep_ == "dobj":
                    complement_object = token.dataset_text

        if subject!=None and subject!= '' and complement_object!=None and complement_object!= '':
            verb_parameters.append((subject,complement_object,sentence))
    return verb_parameters

def find_meaning_groups(verb_parameters):
    meanings={}
    for combination in verb_parameters:
        subj=combination[0]
        obj=combination[1]
        subj_meaning=wordnet.synsets(subj)
        obj_meaning = wordnet.synsets(obj)
        if(len(subj_meaning)>0 and len(obj_meaning)>0):
            subj_meaning=subj_meaning[0]
            obj_meaning=obj_meaning[0]
            break_loop=True
            while(break_loop):
                if(subj_meaning.max_depth() <= CATEGORY_HEIGHT):
                    break_loop=False
                else:
                    hypo=subj_meaning.hypernyms()
                    if(len(hypo)==0):
                        break_loop=False
                    else:
                        subj_meaning = hypo[0]
            break_loop = True
            while (break_loop):
                if (obj_meaning.max_depth() <= CATEGORY_HEIGHT):
                    break_loop = False
                else:
                    hypo = obj_meaning.hypernyms()
                    if (len(hypo) == 0):
                        break_loop = False
                    else:
                        obj_meaning = hypo[0]
            combination_name=(subj_meaning.name()+"--"+obj_meaning.name())
            if(combination_name in meanings):
                meanings[combination_name].append(combination)
            else:
                meanings[combination_name]=[]
                meanings[combination_name].append(combination)
    return meanings


if __name__ == "__main__":
    nlp = spacy.load("en_core_web_sm")
    file_path = 'Corpus3_HIT'
    dataset = parse_file(file_path)
    dataset = tokenize_sentences(dataset)
    verb_parameters=extract_verb_parameters(dataset,VERB)
    print("Total sentences: ",len(dataset),"Number of sentences parsed correctly: ",len(verb_parameters))
    meanings=find_meaning_groups(verb_parameters)
    print("Number of meanings: ",len(meanings))
    avg=0
    for key in meanings:
        if MIN_SENTENCES <= len(meanings[key]):
            print("MEANING: ",key)
            print("NUMBER OF SENTENCES: ",len(meanings[key]))
            print("SENTENCES: ",meanings[key])
            print("")
        avg += len(meanings[key])

    avg=avg/len(meanings)
    print("AVARAGE NUMBER OF SENTENCES FOR MEANING: ",avg)


