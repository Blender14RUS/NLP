import nltk
import string
from operator import itemgetter
from nltk.corpus import stopwords
from nltk.book import text1
from pprint import pprint

words_count = 50
slices_count = 20

def create_exceptional_punctuation():
    lst = list(string.punctuation + "“”’")
    lst.append("--")
    return lst

def FreqDist(text):
    freq_dist = nltk.FreqDist(text)
    print(freq_dist.most_common(10))
    freq_dist.plot(words_count, cumulative=False)

def slice_text(source_text, slice_count):
    slices = []
    for i in range(0, len(source_text), slice_count):
        paragraph = source_text[i:i + slice_count]
        slices.append(paragraph)

    return slices


def create_token_list(slices, is_bigram_needed):
    token_list = []
    for i, paragraph in enumerate(slices):
        chunk_text = ' '.join(paragraph)
        file_tokens = [(w, i, j) for j, w in enumerate(nltk.tokenize.word_tokenize(chunk_text))]
        file_tokens = list(set(file_tokens))
        token_list.extend(file_tokens)
        if is_bigram_needed:
            bigram_tokens = [(" ".join(w), i, j) for j, w in enumerate(nltk.bigrams(nltk.tokenize.word_tokenize(chunk_text)))]
            bigram_tokens = list(set(bigram_tokens))
            token_list.extend(bigram_tokens)
    return sorted(token_list, key=itemgetter(0, 1))


def create_positional_index(slices, is_bigram_needed):
    token_list = create_token_list(slices, is_bigram_needed)
    pos_index = {}
    for (word, doc_no, word_index) in token_list:
        if word not in pos_index:
            pos_index[word] = {'postings': dict()}
        pos_index[word]['postings'].setdefault(doc_no, []).append(word_index)

    return pos_index


def main():
    pathToFile = "./pg1488.txt"

    # Step 2
    text = ""
    with open(pathToFile, 'r', encoding="utf-8") as file:
        text = file.read()

    sent_token_list = nltk.tokenize.sent_tokenize(text)
    print(len(sent_token_list))
    print(sent_token_list[0:20])

    word_token_list = nltk.tokenize.word_tokenize(text)
    print(len(word_token_list))
    print(word_token_list[0:20])

    # Step 3
    text = nltk.Text(word_token_list)

    # Step 4
    # print and plot the most common words in book
    FreqDist(text)


    # Step 5
    # Moby Dick
    FreqDist(text1)

    # Step 6
    stop_words = set(stopwords.words('english') + create_exceptional_punctuation())
    filtered_text = [w for w in text if w not in stop_words]
    filtered_text1 = [w for w in text1 if w not in stop_words]

    FreqDist(filtered_text)
    FreqDist(filtered_text1)

    # Step 7
    slices = slice_text(sent_token_list, slices_count)
    print(slices)

    pos_index = create_positional_index(slices, False)
    pprint(pos_index)


if __name__ == "__main__":
    main()