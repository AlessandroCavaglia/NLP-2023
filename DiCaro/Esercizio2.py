import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize
from nltk.tag import pos_tag
from nltk.corpus import wordnet
import statistics
import pandas as pd

RELEVANT_WORD_SIZE_FOR_GENUS = 5
MIN_SYNSET_HEIGHT = 2
MEANING_CANDIDATES_SIZE = 5
DEVIATION = 4

meaningCandidates = []


def average_length(list):
    lengths = [len(sublist) for sublist in list]
    avg_length = statistics.mean(lengths)
    return avg_length


def refine_dataset(dataset, k):
    for key in dataset:
        avg = int(average_length(dataset[key]))
        dataset[key] = [elem for elem in dataset[key] if abs(len(elem) - avg) <= k]
        avg = int(average_length(dataset[key]))


def parse_tsv_file(file_path):
    df = pd.read_csv(file_path, sep='\t')
    return df


def intersection(lst1, lst2):
    lst3 = [value for value in lst1 if value in lst2]
    return lst3


def calc_similarity(definition, lists):
    result = 0
    for list1 in lists:
        result += len(intersection(list1, definition)) / ((len(list1) + len(definition)) / 2)
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
    print("ELABORATING WORDS FROM DATASET ON ", len(sentences), " SENTENCES")
    words_dict = {}
    for sentence in sentences:
        for word in sentence:
            if (word in words_dict):
                words_dict[word] += 1
            else:
                words_dict[word] = 1
    my_list = list(words_dict.items())
    sorted_list = sorted(my_list, key=lambda x: x[1], reverse=True)
    print("ELABORATED WORDS, SHOWING FIRST", RELEVANT_WORD_SIZE_FOR_GENUS, " RELEVANT WORDS")
    for item in sorted_list[0:RELEVANT_WORD_SIZE_FOR_GENUS]:
        print(item)
    return sorted_list


def getSynsetsInOrderFromWordNet(words):
    print("ELABORATING SYNSET SEARCH ON ", len(words), " WORDS")
    synsetWithHeight = []
    for word in words:
        synsets = wordnet.synsets(word[0])
        for synset in synsets:
            if synset.max_depth() > MIN_SYNSET_HEIGHT:
                synsetWithHeight.append((synset.name(), synset.max_depth(), synset))
    sortedSynsetWithHeight = sorted(synsetWithHeight, key=lambda x: x[1])
    print("FOUND A TOTAL OF ", len(sortedSynsetWithHeight), " SYNSETS ")
    # for item in sortedSynsetWithHeight:
    #    print(item)
    return sortedSynsetWithHeight


def calcSimilarityForSynset(synset, sentences):
    if not any(synset.name() == item[0] for item in meaningCandidates):
        similarity = calc_similarity(lemmatized_tokens(synset.definition()), sentences)
        meaningCandidates.append((synset.name(), similarity))

    for hyponim in synset.hyponyms():
        if not any(hyponim.name() == item[0] for item in meaningCandidates):
            calcSimilarityForSynset(hyponim, sentences)


def getMeaningCandidatesFromSynsets(synsets, sentences):
    print("ELABORATING MEANING ON ", len(synsets), " WITH A TOTAL OF ", len(sentences), " DEFINITIONS")
    for synset in synsets:
        calcSimilarityForSynset(synset[2], sentences)
    sortedmeaningCandidates = sorted(meaningCandidates, key=lambda x: x[1], reverse=True)
    print("ELABORATED MEANING, SHOWING FIRST ", MEANING_CANDIDATES_SIZE, " RESULTS WITH SCORES: ")
    for item in sortedmeaningCandidates[0:MEANING_CANDIDATES_SIZE]:
        print(item)
    return sortedmeaningCandidates[0:MEANING_CANDIDATES_SIZE]


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
    print("Refining dataset removing sentences that are at least ", DEVIATION, " apart from avarage lenght")
    refine_dataset(dataset, DEVIATION)

    print("\n\n\n--- ELABORATING DOOR")

    doorWords = getWordsInOrder(dataset['door'])
    doorParentSynsetCandidates = getSynsetsInOrderFromWordNet(doorWords[0:RELEVANT_WORD_SIZE_FOR_GENUS])
    doorMeaningCandidates = getMeaningCandidatesFromSynsets(doorParentSynsetCandidates, dataset['door'])
    while (len(meaningCandidates) > 0):
        meaningCandidates.pop()
    print("\n\n\n--- ELABORATING LADYBUG")
    ladyBugWords = getWordsInOrder(dataset['ladybug'])
    ladyBugParentSynsetCandidates = getSynsetsInOrderFromWordNet(ladyBugWords[0:RELEVANT_WORD_SIZE_FOR_GENUS])
    ladyBugMeaningCandidates = getMeaningCandidatesFromSynsets(ladyBugParentSynsetCandidates, dataset['ladybug'])
    while (len(meaningCandidates) > 0):
        meaningCandidates.pop()
    print("\n\n\n--- ELABORATING PAIN")
    painWords = getWordsInOrder(dataset['pain'])
    painParentSynsetCandidates = getSynsetsInOrderFromWordNet(painWords[0:RELEVANT_WORD_SIZE_FOR_GENUS])
    painMeaningCandidates = getMeaningCandidatesFromSynsets(painParentSynsetCandidates, dataset['pain'])
    while (len(meaningCandidates) > 0):
        meaningCandidates.pop()
    print("\n\n\n--- ELABORATING BLURRINESS")
    blurrinessBugWords = getWordsInOrder(dataset['blurriness'])
    blurrinessParentSynsetCandidates = getSynsetsInOrderFromWordNet(blurrinessBugWords[0:RELEVANT_WORD_SIZE_FOR_GENUS])
    blurrinessMeaningCandidates = getMeaningCandidatesFromSynsets(blurrinessParentSynsetCandidates,
                                                                  dataset['blurriness'])


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
