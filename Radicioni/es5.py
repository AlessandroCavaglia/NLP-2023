from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

from nltk.stem import WordNetLemmatizer
from nltk.corpus import wordnet as wn
from nltk.tokenize import sent_tokenize
import numpy as np
from nltk.translate.bleu_score import sentence_bleu
from rouge import Rouge

import nltk

from scipy.spatial.distance import cosine

def count_sentences(text):
    sentence_tokens = sent_tokenize(text)
    num_sentences = len(sentence_tokens)
    return num_sentences

def get_word_similarity(word1, word2):
    try:
        vec1 = nasari[word1]
        vec2 = nasari[word2]
        return 1 - cosine(vec1, vec2)
    except:
        return 0.0

def lemmatize_text(text):
    stop_words = set(stopwords.words('english'))
    lemmatizer = WordNetLemmatizer()
    tokens = word_tokenize(text.lower())
    tokens = [token for token in tokens if token.isalpha()]
    tokens = [token for token in tokens if token not in stop_words]
    tokens = [lemmatizer.lemmatize(token) for token in tokens]
    return tokens

def calculate_scores(text_tokens, keyword_tokens):
    scores = []
    for token in text_tokens:
        max_similarity = 0
        for keyword in keyword_tokens:
            similarity = get_word_similarity(token, keyword)
            if similarity > max_similarity:
                max_similarity = similarity
        scores.append(max_similarity)
    return scores

def summarize_text(text, num_sentences):
    keyword_tokens = lemmatize_text(text)  # Preprocessa il testo
    sentence_tokens = sent_tokenize(text)  # Dividi il testo in frasi
    sentence_scores = []
    for sentence in sentence_tokens:
        tokens = lemmatize_text(sentence)  # Preprocessa la frase
        sentence_score = sum(calculate_scores(tokens, keyword_tokens))  # Calcola il punteggio della frase
        sentence_scores.append(sentence_score)
    sorted_indices = np.argsort(sentence_scores)[::-1]  # Ordina gli indici delle frasi in ordine decrescente
    top_indices = sorted_indices[:num_sentences]  # Seleziona i primi "num_sentences" indici
    summary_sentences = [sentence_tokens[i] for i in top_indices]  # Ottieni le frasi corrispondenti agli indici
    summary = ' '.join(summary_sentences)  # Unisci le frasi per ottenere il riassunto
    return summary

def read_text_from_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        text = file.read()
    return text

def calculate_rouge(reference_summary, generated_summary):
    rouge = Rouge()
    scores = rouge.get_scores(generated_summary, reference_summary)
    return scores[0]  # Restituisce i punteggi ROUGE

def calculate_blue(reference_summary, generated_summary):
    reference = [reference_summary.split()]
    generated = generated_summary.split()
    blue_score = sentence_bleu(reference, generated)
    return blue_score


if __name__ == "__main__":
    nasari = {}
    with open('Nasari/dd-small-nasari-15.txt', 'r', encoding='utf-8') as file:
        for line in file:
            line = line.strip().split('\t')
            word = line[0]
            vector = [float(val) for val in line[1:]]
            nasari[word] = vector
    text = read_text_from_file("Nasari/Trump-wall.txt")
    summary = summarize_text(text, num_sentences = int(count_sentences(text) * (1 - 10 / 100)))
    print(summary)

    reference_summary = text
    generated_summary = summary
    rouge_scores = calculate_rouge(reference_summary, generated_summary)
    blue_score = calculate_blue(reference_summary, generated_summary)

    print(rouge_scores,blue_score)
