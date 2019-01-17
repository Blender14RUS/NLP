import nltk
from nltk import Nonterminal, nonterminals, Production, CFG


grammar_rules = u"""
S -> NP VP
PP -> P NP
NP -> Det N N | Det N | 'библиотеке'
VP -> V VP | V PP
Det -> 'Эти'
N ->  'студенты' | 'начали'
V -> 'начали' | 'петь'
P -> 'в'
"""

grammar = nltk.CFG.fromstring(grammar_rules)

# Эти типы стали есть в цехе
sentence = u'Эти студенты начали петь в библиотеке'.split()
parser = nltk.ChartParser(grammar)
for tree in parser.parse(sentence):
    print(tree)
