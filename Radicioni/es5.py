from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

from nltk.stem import WordNetLemmatizer
from nltk.corpus import wordnet as wn
from nltk.tokenize import sent_tokenize
import numpy as np
from rouge import Rouge

import nltk

from scipy.spatial.distance import cosine

def load_nasari(filename):
    nasari={}
    with open(filename, 'r', encoding='utf-8') as file:
        for line in file:
            line=line.lower()
            line = line.strip().split(';')
            nasari[line[1]] = []
            for elem in line [2:]:
                elem = elem.strip().split('_')
                if len(elem) == 2:
                    nasari[line[1]].append((elem[0],float(elem[1])))
    return nasari

def count_sentences(text):
    sentence_tokens = sent_tokenize(text)
    num_sentences = len(sentence_tokens)
    return num_sentences

def calculate_weighted_overlap(vec1,vec2):
    overlap=0
    for elem_1 in vec1:
        for elem_2 in vec2:
            if(elem_1[0]==elem_2[0]):
                overlap+=elem_1[1]+elem_2[1]
    return overlap

def get_word_similarity(word1, word2,nasari):
    try:
        vec1 = nasari[word1]
        vec2 = nasari[word2]
        return calculate_weighted_overlap(vec1, vec2)
    except:
        #print(word1,"-",word2)
        return 0.0

def lemmatize_text(text):
    stop_words = set(stopwords.words('english'))
    lemmatizer = WordNetLemmatizer()
    tokens = word_tokenize(text.lower())
    tokens = [token for token in tokens if token.isalpha()]
    tokens = [token for token in tokens if token not in stop_words]
    tokens = [lemmatizer.lemmatize(token) for token in tokens]
    return tokens

def calculate_scores(text_tokens, keyword_tokens,nasari):
    scores = []
    for token in text_tokens:
        max_similarity = 0
        for keyword in keyword_tokens:
            similarity = get_word_similarity(token, keyword,nasari)
            if similarity > max_similarity:
                max_similarity = similarity
        scores.append(max_similarity)
    return sum(scores)

def summarize_text(text, num_sentences,nasari):
    keyword_tokens = lemmatize_text(text)  # Preprocessa il testo
    sentence_tokens = sent_tokenize(text)  # Dividi il testo in frasi
    sentence_scores = []
    for index,sentence in enumerate(sentence_tokens):
        tokens = lemmatize_text(sentence)  # Preprocessa la frase
        sentence_score = calculate_scores(tokens, keyword_tokens,nasari)  # Calcola il punteggio della frase
        sentence_scores.append((index,sentence_score))
    sorted_indices = sorted(sentence_scores, key=lambda x: x[1],reverse=True)
    top_indices = sorted_indices[:num_sentences]  # Seleziona i primi "num_sentences" indici
    summary_sentences = [sentence_tokens[i] for i in (index[0] for index in top_indices)]  # Ottieni le frasi corrispondenti agli indici
    summary = ' '.join(summary_sentences)  # Unisci le frasi per ottenere il riassunto
    return summary

def read_text_from_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        text = file.read()
    return text

def calculate_rouge(reference_summary, generated_summary):
    reference = set(word_tokenize(reference_summary))
    generated = set(word_tokenize(generated_summary))
    blue_score = len(reference.intersection(generated)) / len(reference)
    return blue_score

def calculate_blue(reference_summary, generated_summary):
    reference = set(word_tokenize(reference_summary))
    generated = set(word_tokenize(generated_summary))
    blue_score = len(reference.intersection(generated))/len(generated)
    return blue_score


if __name__ == "__main__":
    nasari = load_nasari('Nasari/dd-small-nasari-15.txt')
    dataset_text = read_text_from_file("Nasari/Trump-wall.txt")
    reference_text = read_text_from_file("Nasari/Trump-wall-reference-80.txt")
    COMPRESSION_RATE=20
    num_phrases = int(count_sentences(dataset_text) * (1 - COMPRESSION_RATE / 100))
    summary = summarize_text(dataset_text,num_phrases,nasari)

    generated_summary = summary

    rouge_scores = calculate_rouge(reference_text, generated_summary)
    blue_score = calculate_blue(reference_text, generated_summary)

    print("PRECISION:",blue_score)
    print("RECALL:",rouge_scores)
