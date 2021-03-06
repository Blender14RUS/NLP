from gensim.models.word2vec import LineSentence
from gensim.models import FastText
import nltk
import numpy as np
from nltk.collocations import *
import pickle
from sklearn.feature_extraction.text import CountVectorizer

DEFAULT_PATH = 'data.txt'
DEFAULT_ENCODING = 'utf-8'

def read_file(path, encoding):
    with open(path, 'r', encoding=encoding) as file:
        lines = file.read()
    return lines

def tokenize(source_file):
    tokens = nltk.word_tokenize(source_file)
    tokens = [w.lower() for w in tokens]
    print('----------------------------------------------------------------------------------------')
    print(tokens[:10])
    print('----------------------------------------------------------------------------------------\n')
    return tokens

def create_model(filename):
    sentences = LineSentence(filename)
    print(filename)
    model = FastText(sentences, min_count=1)

    return model

def bigram(source_file):
    bigrams_measures = nltk.collocations.BigramAssocMeasures()
    tokens = tokenize(source_file)
    text = nltk.Text(tokens)
    finder = BigramCollocationFinder.from_words(text)
    bigrams = finder.ngram_fd.most_common(100)
    return bigrams

def bagofwords(sentence, words):
    # frequency word count
    bag = np.zeros(len(words))
    for sw in sentence:
        for i, word in enumerate(words):
            if word == sw:
                bag[i] += 1

    return np.array(bag)

def main():
    source_file = read_file(DEFAULT_PATH, DEFAULT_ENCODING)
    create_model("data.txt")

    bigrams = bigram(source_file)
    wordlist = []
    for bigra in bigrams:
        words = bigra[0]
        wordlist.append(words[0])
        wordlist.append(words[1])

    pickle.dump(wordlist, open('model', 'wb'))

if __name__ == "__main__":
    main()