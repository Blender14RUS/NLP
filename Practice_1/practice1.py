import nltk

grammar_rules = u"""
S -> NP VP
PP -> P NP
NP -> Det N N | Det N | 'библиотеке'
VP -> V VP | V PP
Det -> 'Эти'
N ->  'студенты' | 'начали'
V -> 'начали' | 'шуметь'
P -> 'в'
"""

grammar = nltk.CFG.fromstring(grammar_rules)

sentence = u'Эти студенты начали шуметь в библиотеке'.split()
parser = nltk.ChartParser(grammar)
for tree in parser.parse(sentence):
    print(tree)
