import re
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize
from nltk.tag import pos_tag
from sklearn.metrics.pairwise import cosine_similarity
import spacy
import matplotlib.pyplot as plt


def chunking(file):
    with open(file, 'r', encoding='utf-8') as file:
        testo = file.read()
    # Utilizziamo un'espressione regolare per separare il testo in frasi
    # considerando il punto seguito da uno spazio come delimitatore delle frasi
    phrases = re.split(r'\.', testo)
    return phrases

def elaborate_corpus(corpus):
    result = []
    for phrase in corpus:
        result.append(lemmatized_tokens(phrase))
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
    unified_corpus = []
    paragraf = []
    #sistemo il corpus come unione delle parole delle singole frasi
    for phrase in corpus:
        unified_corpus.append(' '.join(phrase))

    for i in range(0, len(unified_corpus), aggregation_number):
        paragraf.append(' '.join((unified_corpus[i:i + aggregation_number])))
    embeddings = calc_embedding(paragraf)
    similarity = []
    for index, embed in enumerate(embeddings):
        if index < len(embeddings) - 1:
            similarity.append(cosine_similarity([embed], [embeddings[index + 1]])[0][0])

    return similarity[:len(similarity)-1]


if __name__ == "__main__":
    #Lettura input
    filename = 'Corpus4a_Article'

    nltk.download('punkt')
    nltk.download('stopwords')
    nltk.download('wordnet')
    nltk.download('pattern')
    nltk.download('averaged_perceptron_tagger')
    lemmatizer = WordNetLemmatizer()
    print(elaborate_corpus(chunking(filename)))
    embed = calc_basic_similarity_metrics(elaborate_corpus(chunking(filename)),3)

    # Traccia il grafico
    plt.plot(range(len(embed)), embed)

    plt.xlabel('Indice')
    plt.ylabel('Valore')

    # Titolo del grafico
    plt.title('Grafico dei numeri')

    # Mostra il grafico
    plt.show()
