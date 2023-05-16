import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize
from nltk.tag import pos_tag
import statistics
import pattern
import string
import csv
import pandas as pd


# Concreti
# Generico   ->  Door    Specifico   ->  LadyBug
# Astratto   ->  Pain    Specifico   ->  Blurriness


def parse_tsv_file(file_path):
    df = pd.read_csv(file_path, sep='\t')
    return df


def average_length(list):
    lengths = [len(sublist) for sublist in list]
    avg_length = statistics.mean(lengths)
    return avg_length


def intersection(lst1, lst2):
    lst3 = [value for value in lst1 if value in lst2]
    return lst3


def calc_similarity(lists):
    result = 0
    for list1 in lists:
        for list2 in lists:
            if list2 != list1:
                result += len(intersection(list1, list2)) / min(len(list1), len(list2))
    print(result / (pow(len(lists),2) - (len(lists))))

def refine_dataset(dataset,k):
    for key in dataset:
        avg = int(average_length(dataset[key]))
        print(avg,key,len(dataset[key]))
        dataset[key] = [elem for elem in  dataset[key] if abs(len(elem)-avg) <= k]
        avg = int(average_length(dataset[key]))
        print(avg, key, len(dataset[key]))


def prepare_dataset(dataframe):
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
    calc_similarity(dataset['door'])
    calc_similarity(dataset['ladybug'])
    calc_similarity(dataset['pain'])
    calc_similarity(dataset['blurriness'])
    refine_dataset(dataset,4)
    calc_similarity(dataset['door'])
    calc_similarity(dataset['ladybug'])
    calc_similarity(dataset['pain'])
    calc_similarity(dataset['blurriness'])



# Remove punctuation, capital letters, stop words, and lemmatize verbs to their base form
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


if __name__ == "__main__":
    # Lettura CSV
    file_path = 'TLN-definitions-23.tsv'
    df = parse_tsv_file(file_path)

    nltk.download('punkt')
    nltk.download('stopwords')
    nltk.download('wordnet')
    nltk.download('pattern')
    nltk.download('averaged_perceptron_tagger')

    lemmatizer = WordNetLemmatizer()

    prepare_dataset(df)

    # Intersezione lessicale
    # overlap = lemmas1.intersection(lemmas2)
    # overlap_count = len(overlap)
    # Usare 1/min(due definizioni)

    # Fare post processing
