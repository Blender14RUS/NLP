import nltk
import string
import spacy
import difflib

from nltk.tree import Tree

sentence = u"John is very polite boy. He likes to help people. For example he helped old woman Sara to cross the street. She was so happy"
gold_sentence = u"John is very polite boy. John likes to help people. For example John helped old woman Sara to cross the street. Sara was so happy"

def spacy_coref(model, sentence):
    nlp = spacy.load(model)
    doc = nlp(sentence)
    return doc._.coref_resolved

def resolve_sentence_with_corefs(sentence, dict_ne_prn):
    words = nltk.word_tokenize(sentence)
    output_str = ""
    idx = 0
    for key, values in dict_ne_prn.items():
        for x in range(0, len(values)):
            for (i, w) in list(enumerate(words))[idx:]:
                if values[x] == w:
                    idx = i
                    words[idx] = key
                    break
    for w in words:
        if w not in string.punctuation:
            output_str += " " + w
        else:
            output_str += w
    return output_str.strip()

def apply_co_ref(ne_recognized_sentence):
    dict_ne_prn = {}
    current_key = ""
    for t in ne_recognized_sentence:
        if type(t) == Tree:
            ne_key = ' '.join(c[0] for c in t)
            dict_ne_prn[ne_key] = []
            current_key = ne_key
        elif dict_ne_prn:
            if t[1] in ["PRP", "PRP$"]:
                dict_ne_prn[current_key].append(t[0])
    return dict_ne_prn



print("Input sentence:")
print(sentence)
print('\n')

print("POS-tagging:")
post_tagged = nltk.pos_tag(nltk.word_tokenize(sentence))
print(post_tagged)
print('\n')

print("NE-Recognition:")
ne_recognized = nltk.ne_chunk(post_tagged, binary=True)
print(ne_recognized)
print('\n')

print("Resolved sentence:")
dict_ne_prn = apply_co_ref(ne_recognized)
resolved_sent = resolve_sentence_with_corefs(sentence, dict_ne_prn)
print(resolved_sent)
print('\n')

print("Resolved sentence with spaCy:")
resolved_sent_spacy = spacy_coref('en_coref_md', sentence)
print(resolved_sent_spacy)
print('\n')


d = difflib.Differ()
print('Evaluation: gold, custom simple system, spaCy co-ref')
gold = d.compare(gold_sentence, gold_sentence)
print(' '.join(gold))
diff = d.compare(gold_sentence, resolved_sent)
print(' '.join(diff))
diff_spacy = d.compare(gold_sentence, resolved_sent_spacy)
print(' '.join(diff_spacy))
