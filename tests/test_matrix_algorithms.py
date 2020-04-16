from src.context_free_grammar import *
from src.graph import *
from src.matrix_algorithms import *
import tempfile
from os import path


def test_evalCFPQ1():
    g = Grammar()
    graph = Graph()
    graph.vertices = [0, 1, 2, 3]
    graph.terminals = ['a', 'b']
    graph.edges = [(0, 'a', 1), (1, 'a', 2), (2, 'a', 0), (2, 'b', 3), (3, 'b', 2)]
    g.grammar = {'S': [['A', 'B'], ['A', 'S1']], 'S1': [['S', 'B']], 'A': [['a']], 'B': [['b']]}
    g.nonterminal_alphabet_init()
    matrix = evalCFPQ(g, graph)['S'].toarray()
    good_res = [(1, 3), (0, 2), (2, 3), (1, 2), (0, 3), (2, 2)]
    for (a, b) in good_res:
        assert matrix[a][b]


def test_evalCFPQ2():
    g = Grammar()
    graph = Graph()
    graph.vertices = [0, 1, 2]
    graph.terminals = ['a', 'b', 'c']
    graph.edges = [(0, 'a', 1), (1, 'b', 0), (1, 'c', 2)]
    g.grammar = {'S': [['eps'], ['a', 'S']]}
    g.nonterminal_alphabet_init()
    matrix = evalCFPQ(g, graph)['S'].toarray()
    good_res = [(0, 0), (1, 1), (2, 2), (0, 1)]
    for (a, b) in good_res:
        assert matrix[a][b]


def test_evalCFPQ3():
    g = Grammar()
    graph = Graph()
    graph.vertices = [0, 1, 2, 3]
    graph.terminals = ['a', 'b', 'c']
    graph.edges = [(0, 'a', 2), (2, 'b', 1), (1, 'c', 0), (2, 'a', 3)]
    g.grammar = {'S': [['A', 'S', 'B'], ['eps']], 'B': [['b'], ['eps'], ['S', 'A']], 'A': [['a'], ['eps']]}
    g.nonterminal_alphabet_init()
    matrix = evalCFPQ(g, graph)['S'].toarray()
    good_res = [(0, 0), (2, 2), (1, 1), (3, 3), (2, 3), (0, 3), (2, 1), (0, 1), (0, 2)]
    for (a, b) in good_res:
        assert matrix[a][b]


def test_evalCFPQ_ambiguous_grammar1():
    g = Grammar()
    graph = Graph()
    graph.vertices = [0, 1, 2, 3, 4]
    graph.terminals = ['a', '+', '-']
    graph.edges = [(0, 'a', 1), (1, '+', 2), (2, 'a', 3), (3, '-', 4), (4, 'a', 1), (1, '+', 0)]
    g.grammar = {'S': [['S', '+', 'S'], ['S', '-', 'S'], ['a']]}
    g.nonterminal_alphabet_init()
    matrix = evalCFPQ(g, graph)['S'].toarray()
    good_res = [(0, 1), (2, 3), (4, 1), (2, 1), (0, 3), (4, 3)]
    for (a, b) in good_res:
        assert matrix[a][b]


def test_evalCFPQ_ambiguous_grammar2():
    g = Grammar()
    graph = Graph()
    graph.vertices = [0, 1, 2, 3]
    graph.terminals = ['(', ')']
    graph.edges = [(0, '(', 1), (1, ')', 2), (2, '(', 0), (2, ')', 1), (2, '(', 3), (3, ')', 1), (3, '(', 2)]
    g.grammar = {'S': [['(', 'S', ')', 'S'], ['S', '(', 'S', ')'], ['eps']]}
    g.nonterminal_alphabet_init()
    matrix = evalCFPQ(g, graph)['S'].toarray()
    good_res = [(0, 0), (1, 1), (2, 2), (3, 3), (2, 1), (3, 1), (3, 2), (0, 1), (0, 2)]
    for (a, b) in good_res:
        assert matrix[a][b]


def test_evalCFPQ_inherently_ambiguous_language():  # a^n b^m c^k, where n = m or m = k
    g = Grammar()
    graph = Graph()
    graph.vertices = [0, 1, 2, 3, 4]
    graph.terminals = ['a', 'b', 'c']
    graph.edges = [(0, 'a', 1), (1, 'b', 2), (0, 'c', 3), (3, 'a', 4), (4, 'a', 2), (3, 'b', 1)]
    g.grammar = {'S': [['D', 'C'], ['A', 'E'], ['eps']], 'A': [['a', 'A'], ['eps']], 'B': [['b', 'B'], ['eps']], 'C': [[
        'c', 'C'], ['eps']], 'D': [['a', 'D', 'b'], ['eps']], 'E': [['b', 'E', 'c'], ['eps']]}
    g.nonterminal_alphabet_init()
    matrix = evalCFPQ(g, graph)['S'].toarray()
    good_res = [(0, 0), (1, 1), (2, 2), (3, 3), (4, 4), (3, 2), (4, 2), (3, 4), (0, 3), (0, 2), (0, 1)]
    for (a, b) in good_res:
        assert matrix[a][b]


def test_contextFreePathQueryingTP1():
    test_dir = tempfile.gettempdir()
    f = open(path.join(test_dir, 'grammar_file.txt'), 'w')
    f.write('S (A S B) | (A B)\n A a\n B b\n')
    f.close()
    graph = Graph()
    graph.vertices = [0, 1, 2, 3]
    graph.terminals = ['a', 'b', 'c']
    graph.edges = [(0, 'a', 2), (2, 'b', 1), (1, 'c', 0), (2, 'a', 3)]
    m, s = contextFreePathQueryingTP(path.join(test_dir, 'grammar_file.txt'), graph)
    assert m[s].toarray()[0, 1]
    assert not m[s].toarray()[2, 0]
    assert m[s].toarray()[1, 2]
    assert m[s].toarray()[2, 3]


def test_contextFreePathQueryingTP2():
    test_dir = tempfile.gettempdir()
    f = open(path.join(test_dir, 'grammar_file.txt'), 'w')
    f.write('S (A S B) | (A B)\n A a\n B b\n')
    f.close()
    graph = Graph()
    graph.vertices = [0, 1, 2, 3]
    graph.terminals = ['a', 'b', 'c']
    graph.edges = [(0, 'd', 2), (2, 'e', 1), (1, 'f', 0), (2, 'a', 3)]
    m, s = contextFreePathQueryingTP(path.join(test_dir, 'grammar_file.txt'), graph)
    for i in range(3):
        for j in range(3):
            assert not m[s].toarray()[i, j]
