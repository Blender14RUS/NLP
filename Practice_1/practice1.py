# -*- coding: utf-8 -*-
import nltk
from nltk import Nonterminal, nonterminals, Production, CFG


grammar_rules = u"""
S -> NP VP
PP -> P N
NP -> Det N N | Det N
VP -> V VP | V PP | A VP
Det -> 'Эти'
N ->  'типы' | 'стали' | 'цехе'
V -> 'стали' | 'есть'
P -> 'в'
A -> 'снова'
"""

grammar = nltk.CFG.fromstring(grammar_rules)

# Эти типы стали есть в цехе
sentence = u'Эти типы снова стали есть в цехе'.split()
parser = nltk.ChartParser(grammar)
for tree in parser.parse(sentence):
    print(tree)