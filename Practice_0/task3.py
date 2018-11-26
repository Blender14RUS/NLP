import nltk
#nltk.download('stopwords')
from nltk.corpus import stopwords

pathToFile = "./task2_text.txt"
pathToResultFile = "./task3.txt"
text = ""
with open(pathToFile, 'r', encoding="utf-8") as file:
    text = file.read()

tokens = nltk.tokenize.regexp_tokenize(text, r'(\w+[-\w+]*)')

#words = [word for word in tokens if word.isalpha()]

#remove stoowords
stop_words = set(stopwords.words('russian'))
result = [word for word in tokens if word not in stop_words]

with open(pathToResultFile, "w", encoding='utf-8') as output_file:
    output_file.write('\n'.join(result))

