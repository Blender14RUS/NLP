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
model = gensim.models.Word2Vec(sentences)
print('Similar for "Marfa"')
print(model.wv.most_similar(positive=['Marfa']))

print('\nSimilar for "Petersburg"')
print(model.wv.most_similar(positive=['Petersburg']))

print('\nSimilar for "Ivolgin"')
print(model.wv.most_similar(positive=['Ivolgin']))

print('\nSimilar for "Aglaya"')
print(model.wv.most_similar(positive=['Aglaya']))

model.wv.save_word2vec_format("IDIOT_preproc.model")
