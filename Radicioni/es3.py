import random

import nltk
from nltk import bigrams,trigrams, FreqDist
import csv

def read_csv(filename):
    dataset=[]
    with open(filename, 'r',encoding='utf-8') as file:
        # Create a CSV reader object
        reader = csv.reader(file)
        for row in reader:
            if(not row[1][0]=="@"):
                sentence = "[" + row[1] + "]"
                dataset.append(sentence)
    return dataset

def learn_bi_gram_model(dataset):
    tokens = [nltk.word_tokenize(sentence) for sentence in dataset]
    tokens = [token for sublist in tokens for token in sublist]
    tokens = list(bigrams(tokens))
    distribution = FreqDist(tokens)

    vocab_size = len(set(tokens))

    # Calculating probabilities with Laplace smoothing
    biTwitter_probabilities = {}
    for bi_gram in distribution:
        previous_word = bi_gram[0]
        biTwitter_probabilities[bi_gram] = (distribution[bi_gram] + 1) / (distribution[previous_word] + vocab_size)

    return biTwitter_probabilities

def learn_tri_gram_model(dataset):
    tokens = [nltk.word_tokenize(sentence) for sentence in dataset]
    tokens = [token for sublist in tokens for token in sublist]
    tokens = list(trigrams(tokens))
    distribution = FreqDist(tokens)

    vocab_size = len(set(tokens))

    # Calculating probabilities with Laplace smoothing
    triTwitter_probabilities = {}
    for tri_gram in distribution:
        previous_word = tri_gram[0]
        triTwitter_probabilities[tri_gram] = (distribution[tri_gram] + 1) / (distribution[previous_word] + vocab_size)

    return triTwitter_probabilities


def generate_text(prob):
    current_word = "["
    generated_text = [current_word]

    while current_word != "]":
        if(len(generated_text)>3):
            next_word = max(prob, key=lambda x: x[0] == current_word and x[1] != ".")[1]
            generated_text.append(next_word)
            current_word = next_word
        else:
            possible_next_words = [word for word in prob if word[0] == current_word and word[1] != "."]
            probabilities = [prob[word] for word in possible_next_words]
            next_word = random.choices(possible_next_words, probabilities)[0][1]
            generated_text.append(next_word)
            current_word = next_word
    return " ".join(generated_text[1:-1])

if __name__ == "__main__":
    # Lettura CSV
    file_path = 'trump_twitter_archive/tweets.csv'
    df = read_csv(file_path)
    #for sent in df:
     #   print(sent)

    bi_prob=learn_bi_gram_model(df)
    tri_prob=learn_bi_gram_model(df)
    print("BIGRAM GENERATED SENTENCES")
    print(generate_text(bi_prob))
    print(generate_text(bi_prob))
    print(generate_text(bi_prob))
    print("TRIGRAM GENERATED SENTENCES")
    print(generate_text(tri_prob))
    print(generate_text(tri_prob))
    print(generate_text(tri_prob))
    #modello bi-grammi e modello tri-grammi

