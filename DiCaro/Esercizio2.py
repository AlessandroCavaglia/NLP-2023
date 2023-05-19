import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize
from nltk.tag import pos_tag
from nltk.corpus import wordnet

import pandas as pd

RELEVANT_WORD_SIZE_FOR_PARENT=10
RELEVANT_WORD_SIZE_FOR_MEANING=20
RELEVANCE_TRESHOLD=0.2

meaningCandidates=[]

def parse_tsv_file(file_path):
    df = pd.read_csv(file_path, sep='\t')
    return df

def intersection(lst1, lst2):
    lst3 = [value for value in lst1 if value in lst2]
    return lst3

def calc_similarity(definition,lists):
    result = 0
    for list1 in lists:
            result += len(intersection(list1, definition)) / min(len(list1), len(definition))
    return result / (len(lists))

def lemmatized_tokens(text):
    tokens = word_tokenize(text.lower())
    stop_words = set(stopwords.words('english'))
    lemmas = []
    for token, tag in pos_tag(tokens):
        if token.isalpha() and token not in stop_words:
            if tag.startswith('VB'):
                lemmas.append(lemmatizer.lemmatize(token, pos='v'))
            else:
                lemmas.append(lemmatizer.lemmatize(token))
    return lemmas

def getWordsInOrder(sentences):
    words_dict={}
    for sentence in sentences:
        for word in sentence:
            if(word in words_dict):
                words_dict[word]+=1
            else:
                words_dict[word]=1
    my_list = list(words_dict.items())
    sorted_list = sorted(my_list, key=lambda x: x[1],reverse=True)
    for item in sorted_list:
        print(item)
    return sorted_list

def getSynsetsInOrderFromWordNet(words):
    synsetWithHeight=[]
    for word in words:
        synsets=wordnet.synsets(word[0])
        for synset in synsets:
            synsetWithHeight.append((synset.name(),synset.max_depth(),synset))
    sortedSynsetWithHeight = sorted(synsetWithHeight, key=lambda x: x[1])
    for item in sortedSynsetWithHeight:
        print(item)
    return sortedSynsetWithHeight

def calcSimilarityForSynset(synset,sentences,meaningCandidates):
    if(not any(synset.name() == item[0] for item in meaningCandidates)):
        similarity = calc_similarity(lemmatized_tokens(synset.definition()), sentences)
        if (similarity >= RELEVANCE_TRESHOLD):
            meaningCandidates.append((synset.name(), similarity))
        else:
            meaningCandidates.append((synset.name(), -1))

    for hyponim in synset.hyponyms():
        calcSimilarityForSynset(hyponim,sentences,meaningCandidates)



def getMeaningCandidatesFromSynsets(synsets,sentences):
    meaningCandidates=[]
    for synset in synsets:
        calcSimilarityForSynset(synset[2],sentences,meaningCandidates)

    meaningCandidates = [tuple for tuple in meaningCandidates if tuple[1] >= 0]

    sortedmeaningCandidates = sorted(meaningCandidates, key=lambda x: x[1])
    for item in sortedmeaningCandidates:
        print(item)
    return sortedmeaningCandidates


def elaborate_dataset(dataframe):
    dataset = {
        'door': [],
        'ladybug': [],
        'pain': [],
        'blurriness': []
    }
    dataframe = dataframe.iloc[:, 1:]  # Rimuovi la prima colona
    for index, row in dataframe.iterrows():
        for column in dataframe.columns:
            dataset[column].extend([lemmatized_tokens(row[column])])
    print("WORDS")
    doorWords=getWordsInOrder(dataset['door'])
    print("SYNSET")
    doorParentSynsetCandidates=getSynsetsInOrderFromWordNet(doorWords[0:RELEVANT_WORD_SIZE_FOR_PARENT])
    print("MEANING")
    doorMeaningCandidates=getMeaningCandidatesFromSynsets(doorParentSynsetCandidates,dataset['door'])

if __name__ == "__main__":
    # Lettura CSV
    file_path = 'TLN-definitions-23.tsv'
    df = parse_tsv_file(file_path)



    lemmatizer = WordNetLemmatizer()

    elaborate_dataset(df)

'''    nltk.download('punkt')
    nltk.download('stopwords')
    nltk.download('wordnet')
    nltk.download('pattern')
    nltk.download('averaged_perceptron_tagger')'''