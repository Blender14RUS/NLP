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


def get_word_vectors(model, single_text, common_vectorizer):
    single_vectorizer = TfidfVectorizer()
    single_vectorizer.fit([single_text])

    word_vectors = {}
    for word, i in single_vectorizer.vocabulary_.items():
        common_index = common_vectorizer.vocabulary_[word]
        if word in model.vocab:
            word_vectors[common_index] = model.get_vector(word)
        else:
            word_vectors[common_index] = np.zeros(100)

    return word_vectors


def reduce_matrix(tfidf_matrix, word_vectors, idx):
    wvec_length = len(list(word_vectors.values())[0])
    reduced_matrix = []
    for row in tfidf_matrix[idx]:
        nrow = np.zeros(wvec_length)
        for nonzeroLocation, value in list(zip(row.indices, row.data)):
            nrow = nrow + value * word_vectors[nonzeroLocation]
        reduced_matrix.append(nrow)

    return np.array([np.array(xi) for xi in reduced_matrix])


def build_dataset(csvwriter, metadata, reduced_matrix, mode):
    csvlist = []
    csvlist.append(metadata["URI"])
    csvlist.extend(reduced_matrix.tolist()[0])
    if mode == "events":
        csvlist.append(metadata["general_topic"])
    else:
        csvlist.append(metadata["general_topic"] + ':' + metadata["topic"])
    csvwriter.writerow(csvlist)


def main():
    remove_files()

    model = load_model("ft_model.vec")
    print("Vector size: " + str(model.vector_size))

    docs = create_doc2vec("common_data/*mystem.txt")
    print("Docs count: " + str(len(docs)))

    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform(docs.values())
    print("Matrix size: " + str(tfidf_matrix.shape))

    modified_matrix = []
    for idx, (filename, text) in enumerate(docs.items()):
        word_vectors = get_word_vectors(model, text, vectorizer)
        reduced_matrix = reduce_matrix(tfidf_matrix, word_vectors, idx)
        modified_matrix.extend(reduced_matrix)
        # print size
        metadata = read_metadata(filename.replace('mystem.txt', 'metadata.json'), DEFAULT_ENCODING)
        with open(DATASET_STEPS_FILENAME, 'a', encoding=DEFAULT_ENCODING, newline='') as csv_file:
            csvwriter = csv.writer(csv_file, quoting=csv.QUOTE_MINIMAL)
            build_dataset(csvwriter, metadata, reduced_matrix, "steps")
        with open(DATASET_EVENTS_FILENAME, 'a', encoding=DEFAULT_ENCODING, newline='') as csv_file:
            csvwriter = csv.writer(csv_file, quoting=csv.QUOTE_MINIMAL)
            build_dataset(csvwriter, metadata, reduced_matrix, "events")
    print("Reduced matrix size: " + str(len(modified_matrix)) + "x" + str(len(modified_matrix[0])))

if __name__ == "__main__":
    main()