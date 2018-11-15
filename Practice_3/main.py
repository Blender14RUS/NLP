import gensim
import nltk
from gensim.models.word2vec import LineSentence
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize


with open("2638-0.txt", "r", encoding="utf8") as file:
    with open("res.txt", "w", encoding="utf8") as resultFile:
        lines = file.readlines()
        for line in lines:

            intermediate = word_tokenize(line)
            words_literals = [word for word in intermediate if word.isalpha()]

            stop_words = set(stopwords.words('english'))
            clear_tokens = [w for w in words_literals if w not in stop_words]

            if not clear_tokens:
                continue
            resultFile.write(' '.join(clear_tokens))
            resultFile.write('\n')

sentences = LineSentence("res.txt")
model = gensim.models.Word2Vec(sentences, min_count=5, size=300, workers=4, window=10, sg=1, negative=5)
print('Similar for "Muishkin".')
print(model.wv.most_similar(positive=['Muishkin']))

print('\nSimilar for "Petersburg"')
print(model.wv.most_similar(positive=['Petersburg']))

print('\nSimilar for "Gavrila"')
print(model.wv.most_similar(positive=['Gavrila']))

print('\nSimilar for "Sokolovitch"')
print(model.wv.most_similar(positive=['Sokolovitch']))

model.wv.save_word2vec_format("ResultPreproc.model")
