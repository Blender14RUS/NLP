from gensim.models.word2vec import LineSentence
from gensim.models import FastText


def create_model(filename):
    sentences = LineSentence(filename)
    print(filename)
    model = FastText(sentences, min_count=1)

    return model


def main():
    model = create_model("data.txt")
    model.wv.save_word2vec_format("ft_model.vec")


if __name__ == "__main__":
    main()