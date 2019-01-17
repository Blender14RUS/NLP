import nltk
import collections
import math
from nltk.collocations import *


# T-score
def calculate_trigrams(tokens):
    words_dict = collections.Counter(tokens)
    N = len(tokens)

    trigrams = nltk.trigrams(tokens)
    trigrams_dict = collections.Counter(trigrams)

    trigrams_N = sum([trigrams_dict[x] for x in trigrams_dict])
    trigrams_dict_len = 0
    for x in trigrams_dict: trigrams_dict_len += 1;

    t_scores = {}
    counter = 1
    for trigram in trigrams_dict:
        #print("Processing " + str(counter) + " out of " + str(trigrams_dict_len))
        trigram_count = trigrams_dict[trigram]
        trigram_freq = trigram_count / trigrams_N
        fst_freq = words_dict[trigram[0]] / N
        scnd_freq = words_dict[trigram[1]]/ N
        thrd_freq = words_dict[trigram[2]]/ N
        t_score = get_score(trigram_freq, fst_freq, scnd_freq,  thrd_freq , N)
        trigram_string = ' '.join(trigram)
        t_scores[trigram_string] = (t_score, trigram_count)
        counter += 1

    return sorted(t_scores.items(), key=lambda kv: kv[1][0], reverse=True)


def get_score(trigram_freq, fst_freq, scnd_freq, thrd_freq, total_count):
    return (trigram_freq - ((fst_freq * scnd_freq * thrd_freq) / total_count)) / math.sqrt(trigram_freq)


f = open('./task_3_mystem_cut.txt', 'rt', encoding='UTF8')
raw = f.read()

tokens = nltk.word_tokenize(raw, 'russian', True)

trigrams = calculate_trigrams(tokens)
print(trigrams)

# nltk MI
text = nltk.Text(tokens)
finder_thr = TrigramCollocationFinder.from_words(text)
trigram_measures = nltk.collocations.TrigramAssocMeasures()
trigram_mi_nltk = finder_thr.score_ngrams(trigram_measures.pmi)
print(trigram_mi_nltk[:30])
