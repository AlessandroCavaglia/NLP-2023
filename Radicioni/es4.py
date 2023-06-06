import os
import glob
import random
from gensim.models import KeyedVectors
import nltk
import numpy as np

def get_embedding(key,glove):
    if key in glove:
        return glove.word_vec(key)
    else:
        return np.zeros(300)  # Return a zero vector if the key is not found

def embed_dataset(dataset,glove):
    for tuple in dataset:
        tuple[0]=embed_sentence(tuple[0],glove)
    return dataset

def embed_sentence(document,glove):
    # Tokenize the sentence into words
    words = nltk.word_tokenize(document.lower())

    # Embed each word and calculate the average embedding
    embeddings = [get_embedding(word, glove) for word in words]
    return compute_centroid(embeddings)


def compute_centroid(embeddings):
    # Verifica che l'array di embedding non sia vuoto
    if len(embeddings) == 0:
        return None
    # Calcola il centroide come media degli embedding lungo l'asse 0
    centroid = np.mean(embeddings, axis=0)

    return centroid

def load_datasets(parent_folder_name):
    dataset=[]
    # Get a list of all items in the folder
    items = os.listdir(parent_folder_name)

    # Filter out folders from the list
    folder_list = [item for item in items if os.path.isdir(os.path.join(parent_folder_name, item))]
    for folder_name in folder_list:
        file_list = glob.glob(os.path.join(os.path.join(parent_folder_name,folder_name), "*"))

        # Iterate over each file
        for file_path in file_list:
            with open(file_path, "r") as file:
                content = file.read()
                dataset.append([content,folder_name])
    return dataset


if __name__ == "__main__":
    dataset=load_datasets("data-es4/data/20_NGs_400")
    random.seed(22)
    random.shuffle(dataset)

    #print(dataset)
    print(len(dataset))
    glove_file = "glove.6B/glove.6B.300d.txt"
    glove = KeyedVectors.load_word2vec_format(glove_file, no_header=True)
    print("finito")
    dataset=embed_dataset(dataset,glove)
    print(dataset)



