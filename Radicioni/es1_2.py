import csv
import math
import random

from nltk.corpus import wordnet
import xml.etree.ElementTree as ET
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize
from nltk.tag import pos_tag
from nltk.wsd import lesk

NUM_TESTS = 10
TEST_SIZE = 50

# nltk.download('punkt')
# nltk.download('stopwords')
# nltk.download('wordnet')
# nltk.download('pattern')
# nltk.download('averaged_perceptron_tagger')

lemmatizer = WordNetLemmatizer()


def intersection(lst1, lst2):
    lst3 = [value for value in lst1 if value in lst2]
    return lst3


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


def parse_gold_key(filename):
    gold_key = {}
    with open(filename, 'r') as csv_file:
        # Create a CSV reader with space as the delimiter
        reader = csv.reader(csv_file, delimiter=' ')

        # Iterate over each row in the CSV
        for row in reader:
            wn_identifier = row[1]
            for i in range(0, len(wn_identifier)):
                if (wn_identifier[i] == ':'):
                    wn_identifier = wn_identifier[0:i]
                    break
            wn_identifier_1 = wn_identifier.replace("%", ".n.0")
            wn_identifier_2 = wn_identifier.replace("%", ".v.0")
            wn_identifier_3 = wn_identifier.replace("%", ".r.0")
            wn_identifier_3 = wn_identifier.replace("%", ".a.0")
            gold_key[row[0]] = (wn_identifier_1, wn_identifier_2, wn_identifier_3)

    return gold_key


def parse_xml_to_list(xml_file):
    dataset = []
    tree = ET.parse(xml_file)
    root = tree.getroot()
    for child in root:
        for element in child:
            sublist = []
            if (element.tag == "sentence"):
                for word in element:
                    sublist.append((word.text, word.get("pos"), word.get("lemma"), word.get("id")))
                dataset.append(sublist)

    return dataset


def lesk_algorithm(term, sentence):
    max_overlap = -1
    best_synset = None
    synsets = wordnet.synsets(term[2])
    for synset in synsets:
        synset_overlap = 0
        definition = lemmatized_tokens(synset.definition())
        if (synset.examples()):
            for example in synset.examples():
                definition += lemmatized_tokens(example)
        # Here we Re-Lemmatize our sentence to include stop-words removal
        string_sentence = ""
        for word in sentence:
            string_sentence += ' ' + word[0]
        string_sentence = lemmatized_tokens(string_sentence)
        synset_overlap = (len(intersection(definition, string_sentence)))
        if (synset_overlap > max_overlap):
            max_overlap = synset_overlap
            best_synset = synset
    return best_synset


def apply_state_of_art_lesk(term, sentence):
    string_sentence = ""
    for word in sentence:
        string_sentence += ' ' + word[0]
    tokens = string_sentence.split()

    return lesk(tokens, term[2])


if __name__ == "__main__":
    random.seed(22)
    dataset = parse_xml_to_list("WSD_Training_Corpora/SemCor/semcor.data.xml")
    gold_key = parse_gold_key("WSD_Training_Corpora/SemCor/semcor.gold.key.txt")
    for i in range(NUM_TESTS):
        n_tests = 0
        n_hits = 0

        n_state_of_art_hits = 0
        sample = random.sample(dataset, TEST_SIZE)
        for sentence in sample:
            searchable_terms = [t for t in sentence if t[3] is not None]
            if (len(searchable_terms) > 0):
                term = random.sample(searchable_terms, 1)[0]
                proposed_synset = lesk_algorithm(term, sentence)
                n_tests += 1
                if proposed_synset is not None:
                    if proposed_synset.name() in gold_key[term[3]]:
                        n_hits += 1
                state_of_art_synset = apply_state_of_art_lesk(term, sentence)
                if state_of_art_synset is not None:
                    if state_of_art_synset.name() in gold_key[term[3]]:
                        n_state_of_art_hits += 1
        acc = (n_hits / n_tests) * 100
        acc_state_of_art = (n_state_of_art_hits / n_tests) * 100
        print("Accuracy from our lesk on test", i, ":", acc, "%")
        print("Accuracy for nltk lesk on test", i, ":", acc_state_of_art, "%\n")
