import sys
import tempfile
from os import path
from antlr4 import *

from src.my_grammarLexer import my_grammarLexer
from src.MyGrammarListener import MyGrammarListener
from src.my_grammarParser import my_grammarParser


class ErrorListener(object):

    def syntaxError(self, recognizer, offendingSymbol, line, column, msg, e):
        pass

    def reportAmbiguity(self, recognizer, dfa, startIndex, stopIndex, exact, ambigAlts):
        pass

    def reportAttemptingFullContext(self, recognizer, dfa, startIndex, stopIndex, conflictingAlts):
        pass

    def reportContextSensitivity(self, recognizer, dfa, startIndex, stopIndex, prediction):
        pass


class MyErrorListener(ErrorListener):
    def syntaxError(self, recognizer, offendingSymbol, line, column, msg, e):
        print("line " + str(line) + ":" + str(column) + " " + msg)
        raise ParseException


class ParseException(Exception):
    pass


def read_script_from_file(file_name):
    lexer = my_grammarLexer(FileStream(file_name))
    stream = CommonTokenStream(lexer)
    parser = my_grammarParser(stream)
    parser.addErrorListener(MyErrorListener)
    try:
        return parser.s()
    except:
        return None


def read_script_from_console():
    s = input()
    test_dir = tempfile.gettempdir()
    f = open(path.join(test_dir, 'input.txt'), 'w')
    f.write(s)
    f.close()
    return read_script_from_file(path.join(test_dir, 'input.txt'))


def check_script(tree):
    if tree is None:
        print('script is incorrect')
    else:
        print('script is correct')


def write_tree(tree, file_name):
    f = open(file_name, 'w')
    walker = ParseTreeWalker()
    collector = MyGrammarListener()
    walker.walk(collector, tree)
    f.write('digraph G {\n  ordering = out;\n')
    for i, name in collector.nodes.items():
        f.write('   ' + str(i) + ' [label= \"' + name[1] + '\"];\n')

    for l, vertex in collector.edges.items():
        for v in vertex:
            f.write('    ' + str(l) + ' -> ' + str(v) + ';\n')
    f.write('}')
    f.close()
