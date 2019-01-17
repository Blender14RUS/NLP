import glob
import os
import re
import subprocess
import shutil
from nltk.corpus import stopwords


russian_stopwords = stopwords.words("russian")
DEFAULT_ENCODING="utf-8"
RE_WORDS = r'(\w+[-\w+]*)'


def read_file(path, encoding):
    with open(path, 'r', encoding=encoding) as file:
        text = file.read()
    return text


def process_files(source_mask, processed_mask):
    for filename in glob.glob(processed_mask):
        os.remove(filename)
    for filename in glob.glob(source_mask):
        lemmatize(filename, os.path.splitext(filename)[0] + "_mystem.txt")


def is_valid(sentence):
    return re.search('\w+', sentence)


def remove_punctuation(sentence):
    return " ".join(re.findall(RE_WORDS, sentence))


def remove_stopwords(sentence):
    words = [word for word in sentence.split() if word not in russian_stopwords]
    return " ".join(words)


def lemmatize(input_file, output_file):
    subprocess.call([r"./mystem.exe", "-lcd", input_file, output_file])
    raw_text = read_file(output_file, DEFAULT_ENCODING)
    with open(output_file, "w", encoding=DEFAULT_ENCODING) as f_out:
        for sent in raw_text.splitlines():
            if is_valid(sent):
                processed_sent = remove_punctuation(sent)
                processed_sent = remove_stopwords(processed_sent)
                f_out.write(processed_sent.strip() + "\n")


def collect_files(mask, output):
    with open(output, 'wb') as outf:
        for filename in glob.glob(mask):
            if filename == output:
                # don't want to copy the output into the output
                continue
            with open(filename, 'rb') as readfile:
                shutil.copyfileobj(readfile, outf)


def main():
    process_files('common_data/*.txt', 'common_data/*mystem.txt')
    collect_files('common_data/*mystem.txt', "data.txt")


if __name__ == "__main__":
    main()