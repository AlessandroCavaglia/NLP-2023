import spacy
import string
#Concreti
#Generico   ->  Door    Specifico   ->  LadyBug
#Astratto   ->  Pain    Specifico   ->  Blurriness

if __name__ == "__main__":
    #Lettura CSV

    nlp = spacy.load('en_core_web_sm')

    sentence = "The quick brown fox jumps over the lazy dog."
    doc = nlp(sentence)

    # Remove punctuation, capital letters, stop words, and lemmatize verbs to their base form
    lemmatized_tokens = [token.lemma_.lower() if token.pos_ == 'VERB' else token.text.lower() for token in doc if
                         not token.is_punct and not token.is_stop and not token.text in string.punctuation]

    print(lemmatized_tokens)

    #Intersezione lessicale
    #overlap = lemmas1.intersection(lemmas2)
    #overlap_count = len(overlap)
    #Usare 1/min(due definizioni)

    #Fare post processing
