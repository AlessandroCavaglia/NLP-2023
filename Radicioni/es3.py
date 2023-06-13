import random

import nltk
import csv

def read_csv(filename):
    dataset=[]
    with open(filename, 'r',encoding='utf-8') as file:
        # Create a CSV reader object
        reader = csv.reader(file)
        for row in reader:
            if(not row[1][0]=="@"):
                sentence_bi = "[" + row[1].replace("&amp","") + "]"
                sentence_tri = "[[" + row[1].replace("&amp","") + "]]"
                dataset.append((sentence_bi,sentence_tri))
    return dataset

def count_bigrams(tokens):
    bigram_counts = {}
    for i in range(len(tokens) - 1):
        current_token = tokens[i]
        next_token = tokens[i + 1]
        if current_token not in bigram_counts:
            bigram_counts[current_token] = {}
        if next_token not in bigram_counts[current_token]:
            bigram_counts[current_token][next_token] = 0
        bigram_counts[current_token][next_token] += 1
    return bigram_counts

def learn_bi_gram_model(dataset):
    tokens = [nltk.word_tokenize(sentence) for sentence in [elem[0] for elem in dataset]]
    tokens = [token for sublist in tokens for token in sublist]
    bigram_counts = count_bigrams(tokens)

    vocab_size = len(set(tokens))

    # Calculating probabilities with Laplace smoothing
    biTwitter_probabilities = {}
    for first_token in bigram_counts:
        sum=0
        for second_token in bigram_counts[first_token]:
            sum+=bigram_counts[first_token][second_token]

        for second_token in bigram_counts[first_token]:
            bi_gram=(first_token,second_token)
            biTwitter_probabilities[bi_gram] = (bigram_counts[first_token][second_token] + 1) / (sum + vocab_size)

    return biTwitter_probabilities

def count_trigrams(tokens):
    trigram_counts = {}
    for i in range(len(tokens) - 2):
        current_token = tokens[i]
        next_token = tokens[i + 1]
        next_next_token = tokens[i + 2]
        if (current_token, next_token) not in trigram_counts:
            trigram_counts[(current_token, next_token)] = {}
        if next_next_token not in trigram_counts[(current_token, next_token)]:
            trigram_counts[(current_token, next_token)][next_next_token] = 0
        trigram_counts[(current_token, next_token)][next_next_token] += 1
    return trigram_counts
def learn_tri_gram_model(dataset):
    tokens = [nltk.word_tokenize(sentence) for sentence in [elem[1] for elem in dataset]]
    tokens = [token for sublist in tokens for token in sublist]
    trigram_counts = count_trigrams(tokens)

    vocab_size = len(set(tokens))

    # Calculating probabilities with Laplace smoothing
    triTwitter_probabilities = {}
    for first_bigram in trigram_counts:
        sum = 0
        for third_token in trigram_counts[first_bigram]:
            sum += trigram_counts[first_bigram][third_token]

        for third_token in trigram_counts[first_bigram]:
            tri_gram = (first_bigram[0],first_bigram[1], third_token)
            triTwitter_probabilities[tri_gram] = (trigram_counts[first_bigram][third_token] + 1) / (sum + vocab_size)
    return triTwitter_probabilities

def generate_text_bigram(prob):
    current_word = "["
    generated_text = [current_word]
    while current_word != "]" and len(generated_text) < 50:
        '''next_word = max(prob, key=lambda bi_gram: bi_gram[0] == current_word)[1]
        generated_text.append(next_word)
        current_word = next_word
        Eliminato metodo completamente deterministico a causa loop'''
        possible_next_bigrams = [bigram for bigram in prob if bigram[0] == current_word]
        probabilities = [prob[(bigram)] for bigram in possible_next_bigrams]
        next_word = random.choices(possible_next_bigrams, probabilities)[0][1]
        generated_text.append(next_word)
        current_word = next_word
    return " ".join(generated_text[1:-1])

def generate_text_trigram(prob):
    current_trigram = ("[", "[", "[")
    generated_text = list(current_trigram)
    while current_trigram[-2:] != ("]", "]") and len(generated_text) < 50:
        if (len(generated_text) > 6):
            next_trigram = max(prob, key=lambda tri_gram: tri_gram[:2] == current_trigram[-2:])
            generated_text.append(next_trigram[-1])
            current_trigram = next_trigram
        else:
            possible_next_trigrams = [trigram for trigram in prob if
                                      trigram[:2] == current_trigram[-2:]]
            probabilities = [prob[trigram] for trigram in possible_next_trigrams]
            next_trigram = random.choices(possible_next_trigrams, probabilities)[0]
            generated_text.append(next_trigram[-1])
            current_trigram = next_trigram

    return " ".join(generated_text[3:-2])

if __name__ == "__main__":
    # Lettura CSV
    file_path = 'trump_twitter_archive/tweets.csv'
    df = read_csv(file_path)

    bi_prob=learn_bi_gram_model(df)

    tri_prob=learn_tri_gram_model(df)
    print("BIGRAM GENERATED SENTENCES")
    print(generate_text_bigram(bi_prob))
    print(generate_text_bigram(bi_prob))
    print(generate_text_bigram(bi_prob))
    print("\nTRIGRAM GENERATED SENTENCES")
    print(generate_text_trigram(tri_prob))
    print(generate_text_trigram(tri_prob))
    print(generate_text_trigram(tri_prob))

