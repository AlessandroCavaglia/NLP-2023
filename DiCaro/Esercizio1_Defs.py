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

    print(average_length(dataset['door']))
    print(average_length(dataset['ladybug']))
    print(average_length(dataset['pain']))
    print(average_length(dataset['blurriness']))


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


    sentence = "The quick brown fox jumps over the lazy dog."

    print(lemmatized_tokens(sentence))

    # Intersezione lessicale
    # overlap = lemmas1.intersection(lemmas2)
    # overlap_count = len(overlap)
    # Usare 1/min(due definizioni)

    # Fare post processing
