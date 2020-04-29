import os

from src.context_free_grammar import *


def parser_my_language(file):
    f = open(file, 'r')
    s = f.read()
    grammar = Grammar()
    grammar.read_grammar(os.path.dirname(__file__) + '/grammar_for_my_language.txt')
    return grammar.CYK(s)
