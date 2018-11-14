import gensim
from gensim.models.word2vec import LineSentence


def train_model(sentences):
    return gensim.models.Word2Vec(sentences, min_count=5, size=300, workers=4, window=10, sg=1, negative=5)


def main():
    sentences = LineSentence('2600.txt')
    model = train_model(sentences)
    print('Similar for "Pierre".')
    print(model.most_similar(positive=['Pierre']))
    print('\nSimilar for "Petersburg"')
    print(model.most_similar(positive=['Petersburg']))
    print('\nSimilar for "Bolkónski"')
    print(model.most_similar(positive=['Bolkónski']))
    print('\nSimilar for "Napoleon"')
    print(model.most_similar(positive=['Napoleon']))


if __name__ == "__main__":
    main()