import re
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize
from nltk.tag import pos_tag
from sklearn.metrics.pairwise import cosine_similarity
import spacy
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

def parse_tsv_file(file_path):
    df = pd.read_csv(file_path, delimiter='\t', nrows=100)
    return df

if __name__ == "__main__":
    # Lettura input
    filename = 'eng_newscrawl-public_2018_10K/eng_newscrawl-public_2018_10K-sentences.txt'

    nltk.download('punkt')
    nltk.download('stopwords')
    nltk.download('wordnet')
    nltk.download('pattern')
    nltk.download('averaged_perceptron_tagger')

    dataset = parse_tsv_file(filename)
    print(dataset)
