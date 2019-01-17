# # -*- coding: utf-8 -*-
# import nltk
# from nltk import Nonterminal, nonterminals, Production, CFG
#
#
# grammar_rules = u"""
# S -> NP VP
# PP -> P NP
# NP -> Det N N | Det N | 'цехе'
# VP -> V VP | V PP
# Det -> 'Эти'
# N ->  'типы' | 'стали'
# V -> 'стали' | 'есть'
# P -> 'в'
# """
#
# grammar = nltk.CFG.fromstring(grammar_rules)
#
# # Эти типы стали есть в цехе
# sentence = u'Эти типы стали есть в цехе'.split()
# parser = nltk.ChartParser(grammar)
# for tree in parser.parse(sentence):
#     print(tree)
import nltk
from nltk import Nonterminal, nonterminals, Production, CFG

groucho_grammar = nltk.CFG.fromstring("""
S -> NP VP
PP -> P NP
NP -> Det N | Det N PP | 'I'
VP -> V NP | VP PP
Det -> 'an' | 'my'
N -> 'elephant' | 'pajamas'
V -> 'shot'
P -> 'in'
""")

sent = ['I', 'shot', 'an', 'elephant', 'in', 'my', 'pajamas']
parser = nltk.ChartParser(groucho_grammar)
for tree in parser.parse(sent):
    print(tree)