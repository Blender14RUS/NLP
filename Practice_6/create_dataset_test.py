import os
import glob
import json

import gensim
import numpy as np
import csv

from sklearn.feature_extraction.text import TfidfVectorizer

DEFAULT_ENCODING="utf-8"
DEFAULT_VEC_SIZE = 100
DATASET_STEPS_FILENAME = "dataset_steps.csv"
DATASET_EVENTS_FILENAME = "dataset_events.csv"


def remove_files():
    try:
        os.remove(DATASET_STEPS_FILENAME)
        os.remove(DATASET_EVENTS_FILENAME)
    except OSError:
        pass


def read_file(path, encoding):
    with open(path, 'r', encoding=encoding) as file:
        text = file.read()
    return text


def read_metadata(path, encoding):
    with open(path, 'r', encoding=encoding) as file:
        metadata = json.load(file)
    return metadata


def load_model(filename):
    return gensim.models.KeyedVectors.load_word2vec_format(filename, binary=False)


def create_doc2vec(path):
    docs = {}
    for filename in glob.glob(path):
        text = read_file(filename, DEFAULT_ENCODING)
        docs[filename] = text

    return docs


def get_word_vectors(model, common_vectorizer):
    word_vectors = {}
    for word, i in common_vectorizer.vocabulary_.items():
        common_index = common_vectorizer.vocabulary_[word]
        if word in model.vocab:
            word_vectors[common_index] = model.get_vector(word)
        else:
            word_vectors[common_index] = np.zeros(100)

    return word_vectors


def reduce_matrix(tfidf_matrix, word_vectors):
    wvec_length = len(list(word_vectors.values())[0])
    reduced_matrix = []
    for row in tfidf_matrix:
        nrow = np.zeros(wvec_length)
        for nonzeroLocation, value in list(zip(row.indices, row.data)):
            nrow = nrow + value * word_vectors[nonzeroLocation]
        reduced_matrix.append(nrow)

    return np.array([np.array(xi) for xi in reduced_matrix])


def build_dataset(csvwriter, reduced_matrix):
    csvlist = []
    csvlist.extend(reduced_matrix.tolist())
    csvwriter.writerows(csvlist)


def main():
    remove_files()

    model = load_model("ft_model.vec")
    print("Vector size: " + str(model.vector_size))

    docs = create_doc2vec("common_data/*mystem.txt")
    print("Docs count: " + str(len(docs)))

    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform(docs.values())
    print("Matrix size: " + str(tfidf_matrix.shape))

    word_vectors = get_word_vectors(model, vectorizer)
    reduced_matrix = reduce_matrix(tfidf_matrix, word_vectors)

    # print size
    with open(DATASET_STEPS_FILENAME, 'a', encoding=DEFAULT_ENCODING, newline='') as csv_file:
        csvwriter = csv.writer(csv_file, quoting=csv.QUOTE_MINIMAL)
        build_dataset(csvwriter, reduced_matrix)
    with open(DATASET_EVENTS_FILENAME, 'a', encoding=DEFAULT_ENCODING, newline='') as csv_file:
        csvwriter = csv.writer(csv_file, quoting=csv.QUOTE_MINIMAL)
        build_dataset(csvwriter, reduced_matrix)

    print("Reduced matrix size: " + str(len(reduced_matrix)) + "x" + str(len(reduced_matrix[0])))

if __name__ == "__main__":
    main()