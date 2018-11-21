import sys
from operator import itemgetter
import os

"""
    check the frequencies of your analogies and doesnt_match terms in the corpus

    eg: 
        python check_frequencies.py questions_soiaf_doesnt_match.txt soiaf4books.txt
"""

INFILE = "./questions_idiot_doesnt_match.txt"
BOOK = "../../2638-0.txt"

all_words = [] 
for line in open(INFILE):

    if line.startswith(':') or line.startswith('"') or not line.strip():
        continue

    words = line.split(' ')

    words = [word.strip() for word in words]

    all_words.extend(words)

all_words = list(set(all_words)) # make unique

print(all_words)

### ok, now we have the words, get the counts from the book
book_text = open(BOOK, "r", encoding="utf8").read()

word_counts = [] 
for word in all_words:
    count = book_text.count(word)
    word_counts.append( (word, count) )


words_sorted = sorted(word_counts,key=itemgetter(1))

for w in words_sorted:
    print(w)

