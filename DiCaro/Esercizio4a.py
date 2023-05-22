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

#Hard 27 frasi football
#30 frasi basket
#33 frasi golf
#29 frasi baseball

CHUNIKING_FACTOR=3

def chunking(file):
    with open(file, 'r', encoding='utf-8') as file:
        testo = file.read()
    # Utilizziamo un'espressione regolare per separare il testo in frasi
    # considerando il punto seguito da uno spazio come delimitatore delle frasi
    phrases = re.split(r'\. |\n', testo)
    return phrases


def elaborate_corpus(corpus):
    result = []
    for phrase in corpus:
        result.append(' '.join(lemmatized_tokens(phrase)))
    return result


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


def calc_embedding(lists):
    result = []
    nlp = spacy.load('en_core_web_lg')
    for phrase in lists:
        doc = nlp(phrase)
        result.append(doc.vector)
    return result


def calc_basic_similarity_metrics(corpus, aggregation_number):
    paragraf = []
    # sistemo il corpus come unione delle parole delle singole frasi

    for i in range(0, len(corpus), aggregation_number):
        paragraf.append(' '.join((corpus[i:i + aggregation_number])))

    embeddings = calc_embedding(paragraf)
    similarity = []
    for index, embed in enumerate(embeddings):
        if index < len(embeddings) - 1:
            similarity.append(cosine_similarity([embed], [embeddings[index + 1]])[0][0])

    return similarity[:len(similarity)-1]

def calc_prototype_similarity_metrics(corpus, aggregation_number):
    paragraf = []
    # sistemo il corpus come unione delle parole delle singole frasi

    for i in range(0, len(corpus), aggregation_number):
        paragraf.append(' '.join((corpus[i:i + aggregation_number])))

    embeddings = calc_embedding(paragraf)
    prototype=[]
    count=0
    similarity = []
    for index, embed in enumerate(embeddings):
        if(len(prototype)==0):
            prototype=embed
            similarity.append(1)
            count=1
        elif(len(prototype)>0):
            protoSim=cosine_similarity([embed], [prototype])[0][0]
            similarity.append(protoSim)
            if(index<len(embeddings)-1 and protoSim < (cosine_similarity([embed], [embeddings[index+1]])[0][0])-0.2):
                count=1
                prototype = embed
            else:
                prototype = (prototype*count+embed)/(count+1)
                count+=1

    return similarity[:len(similarity)-1]

if __name__ == "__main__":
    # Lettura input
    filename = 'Corpus4a_Article_Hard'

    nltk.download('punkt')
    nltk.download('stopwords')
    nltk.download('wordnet')
    nltk.download('pattern')
    nltk.download('averaged_perceptron_tagger')
    lemmatizer = WordNetLemmatizer()
    print(elaborate_corpus(chunking(filename)))
    # calcolo embeddings diviso a paragrafri di N frasi
    dataset = chunking(filename)
    embed = calc_prototype_similarity_metrics(elaborate_corpus(chunking(filename)), CHUNIKING_FACTOR)

    # Traccia il grafico
    plt.plot(range(len(embed)), embed)

    plt.xlabel('Indice')
    plt.ylabel('Valore')

    # Titolo del grafico
    plt.title('Grafico dei numeri')

    # Mostra il grafico
    plt.show()

    print(np.argsort(embed[0:len(embed)])[:3])
    paragraf = []
    # sistemo il corpus come unione delle parole delle singole frasi

    for i in range(0, len(dataset), CHUNIKING_FACTOR):
        paragraf.append(' '.join((dataset[i:i + CHUNIKING_FACTOR])))
    for index in np.argsort(embed[1:len(embed) - 1])[:3]:
        print(paragraf[index])
