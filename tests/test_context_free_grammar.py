import tempfile
from os import path

from src.context_free_grammar import *


def test_print_grammar_in_console(capsys):
    g = Grammar()
    g.grammar = {'S': [['a', 'S', 'b', 'S'], ['eps']]}
    g.print_in_console_grammar()
    captured = capsys.readouterr()
    assert captured.out == 'S -> aSbS\nS -> eps\n'


def test_print_empty_grammar_in_console(capsys):
    g = Grammar()
    g.grammar = {}
    g.print_in_console_grammar()
    captured = capsys.readouterr()
    assert captured.out == ''


def test_write_empty_grammar():
    g = Grammar()
    test_dir = tempfile.gettempdir()
    g.grammar = {}
    g.write_grammar(path.join(test_dir, 'output.txt'))
    f = open(path.join(test_dir, 'output.txt'), 'r')
    assert f.read() == ''


def test_write_grammar1():
    g = Grammar()
    test_dir = tempfile.gettempdir()
    g.grammar = {'S': [['a', 'b', 'S', 'c'], ['eps']]}
    g.write_grammar(path.join(test_dir, 'output.txt'))
    f = open(path.join(test_dir, 'output.txt'), 'r')
    assert f.read() == 'S a b S c \nS eps \n'


def test_write_grammar2():
    g = Grammar()
    test_dir = tempfile.gettempdir()
    g.grammar = {'S': [['eps'], ['a', 'A']], 'A': [['S', 'B']], 'B': [['b', 'S']]}
    g.write_grammar(path.join(test_dir, 'output.txt'))
    f = open(path.join(test_dir, 'output.txt'), 'r')
    assert f.read() == 'S eps \nS a A \nA S B \nB b S \n'


def test_read_grammar():
    g = Grammar()
    test_dir = tempfile.gettempdir()
    f = open(path.join(test_dir, 'input.txt'), 'w')
    f.write('S a b S c \n S eps\n')
    f.close()
    g.read_grammar(path.join(test_dir, 'input.txt'))
    assert g.grammar == {'S': [['a', 'b', 'S', 'c'], ['eps']]}


def test_read_empty_grammar():
    g = Grammar()
    test_dir = tempfile.gettempdir()
    f = open(path.join(test_dir, 'input.txt'), 'w')
    f.close()
    g.read_grammar(path.join(test_dir, 'input.txt'))
    assert g.grammar == {}


def test_read_grammar_with_space():
    g = Grammar()
    test_dir = tempfile.gettempdir()
    f = open(path.join(test_dir, 'input.txt'), 'w')
    f.write('S a     b S  c \n    S  eps \n')
    f.close()
    g.read_grammar(path.join(test_dir, 'input.txt'))
    assert g.grammar == {'S': [['a', 'b', 'S', 'c'], ['eps']]}


def test_add_rule():
    g = Grammar()
    g.add_rule('A', ['a', 'B'])
    g.add_rule('A', ['eps'])
    g.add_rule('B', ['eps'])
    assert len(g.grammar) == 2
    assert g.grammar['A'] == [['a', 'B'], ['eps']]
    assert g.grammar['B'] == [['eps']]


def test_delete_rule():
    g = Grammar()
    g.grammar = {'S': [['a', 'S', 'b', 'S'], ['eps']]}
    g.delete_rule('S', ['a', 'S', 'b', 'S'])
    assert len(g.grammar) == 1
    assert g.grammar['S'] == [['eps']]


def test_delete_long_rules1():
    g = Grammar()
    g.grammar = {'S': [['a', 'S', 'b', 'S'], ['eps']]}
    g.delete_long_rules()
    for (key, value) in g.grammar.items():
        for trans in value:
            assert len(trans) <= 2
    assert g.grammar == {'S': [['eps'], ['a', 'A']], 'A': [['S', 'B']], 'B': [['b', 'S']]}


def test_delete_long_rules2():
    g = Grammar()
    g.grammar = {'A': [['a', 'b', 'c', 'S', 'd', 'A'], ['eps']], 'S': [['e', 'f', 'C']], 'C': [['A', 'a'], ['e', 'a',
                                                                                                            'c', 'F',
                                                                                                            'd']],
                 'F': [['eps']]}
    g.delete_long_rules()
    for (key, value) in g.grammar.items():
        for trans in value:
            assert len(trans) <= 2
    assert g.grammar == {'A': [['eps'], ['a', 'A'], ['b', 'B']], 'S': [['e', 'E']], 'C': [['A', 'a'], ['S', 'D'],
                                                                                          ['e', 'F']],
                         'F': [['eps'], ['a', 'G']], 'B': [['c', 'C']], 'D': [['d', 'A']], 'E': [['f',
                                                                                                  'C']],
                         'G': [['c', 'H']], 'H': [['F', 'd']]}


def test_find_eps_generating_terminals1():
    g = Grammar()
    g.grammar = {'S': [['a', 'A']], 'X': [['a', 'Y'], ['eps'], ['b', 'Y']], 'Y': [['a', 'Y'], ['b', 'Y'], ['c', 'c']],
                 'B': [['eps'], ['y', 'X'], ['y']], 'A': [['X', 'B'], ['y', 'X'], ['y']]}
    eps_generating_terminals = g.find_eps_generating_terminals()
    assert len(eps_generating_terminals) == 3
    assert 'X' in eps_generating_terminals
    assert 'B' in eps_generating_terminals
    assert 'A' in eps_generating_terminals


def test_find_eps_generating_terminals2():
    g = Grammar()
    g.grammar = {'S': [['a', 'A']], 'X': [['a', 'Y'], ['eps'], ['b', 'Y']], 'Y': [['a', 'Y'], ['b', 'Y'], ['c', 'c']],
                 'B': [['eps'], ['y', 'X'], ['y']], 'A': [['X', 'b'], ['y', 'X'], ['y']]}
    eps_generating_terminals = g.find_eps_generating_terminals()
    assert len(eps_generating_terminals) == 2
    assert 'X' in eps_generating_terminals
    assert 'B' in eps_generating_terminals
    assert 'A' not in eps_generating_terminals


def test_delete_eps_rules1():
    g = Grammar()
    g.grammar = {'S': [['a', 'A']], 'X': [['a', 'Y'], ['eps']], 'A': [['X', 'c']]}
    g.delete_eps_rules()
    assert g.grammar == {'S': [['a', 'A']], 'X': [['a', 'Y']], 'A': [['c'], ['X', 'c']]}


def test_delete_eps_rules2():
    g = Grammar()
    g.grammar = {'S': [['a', 'A']], 'X': [['a', 'Y'], ['eps'], ['b', 'Y']], 'Y': [['a', 'Y'], ['b', 'Y'], ['c', 'c']],
                 'B': [['eps'], ['y', 'X'], ['y']], 'A': [['X', 'B'], ['y', 'X'], ['y']]}
    g.delete_eps_rules()
    assert g.grammar == {'S': [['a'], ['a', 'A']], 'X': [['a', 'Y'], ['b', 'Y']], 'Y': [['a', 'Y'], ['b', 'Y'], ['c',
                                                                                                                 'c']],
                         'B': [['y'], ['y', 'X']], 'A': [['y', 'X'], ['y'], ['B'], ['X'], ['X', 'B']]}


def test_find_chain_pairs1():
    g = Grammar()
    g.grammar = {'S': [['a', 'A'], ['a', 'Z']], 'X': [['a', 'Y'], ['b', 'Y']],
                 'Y': [['a', 'Y'], ['b', 'Y'], ['c', 'c']], 'Z': [['Z', 'X']], 'A': [['X', 'B'], ['B']],
                 'B': [['y', 'X'], ['y']]}
    assert g.find_chan_pairs() == [('S', 'S'), ('X', 'X'), ('Y', 'Y'), ('Z', 'Z'), ('A', 'A'), ('B', 'B'), ('A', 'B')]


def test_find_chain_pairs2():
    g = Grammar()
    g.add_rule('S', ['a', 'S', 'b', 'S'])
    g.add_rule('S', ['eps'])
    assert g.find_chan_pairs() == [('S', 'S')]


def test_delete_chain_rules1():  # test from https://neerc.ifmo.ru/wiki/index.php?title=%D0%9D%D0%BE%D1%80%D0%BC%D0%B0%D0%BB%D1%8C%D0%BD%D0%B0%D1%8F_%D1%84%D0%BE%D1%80%D0%BC%D0%B0_%D0%A5%D0%BE%D0%BC%D1%81%D0%BA%D0%BE%D0%B3%D0%BE
    g = Grammar()
    g.grammar = {'S': [['a', 'A'], ['a', 'Z']], 'X': [['a', 'Y'], ['b', 'Y']],
                 'Y': [['a', 'Y'], ['b', 'Y'], ['c', 'c']], 'Z': [['Z', 'X']], 'A': [['X', 'B'], ['B']],
                 'B': [['y', 'X'], ['y']]}
    g.delete_chain_rules()
    assert g.grammar == {'S': [['a', 'A'], ['a', 'Z']], 'X': [['a', 'Y'], ['b', 'Y']],
                         'Y': [['a', 'Y'], ['b', 'Y'], ['c', 'c']], 'Z': [['Z', 'X']],
                         'A': [['X', 'B'], ['y', 'X'], ['y']], 'B': [['y', 'X'], ['y']]}


def test_delete_chain_rules2():
    g = Grammar()
    g.add_rule('S', ['a', 'S'])
    g.add_rule('S', ['A'])
    g.add_rule('S', ['T'])
    g.add_rule('A', ['a', 'b', 'c', 'S'])
    g.add_rule('T', ['l'])
    g.delete_chain_rules()
    assert not ['A'] in g.grammar['S']
    assert not ['T'] in g.grammar['S']
    assert ['l'] in g.grammar['S']
    assert ['a', 'b', 'c', 'S'] in g.grammar['S']


def test_find_generatic_terminals1():
    g = Grammar()
    g.grammar = {'S': [['a', 'A'], ['a', 'Z']], 'X': [['a', 'Y'], ['b', 'Y']],
                 'Y': [['a', 'Y'], ['b', 'Y'], ['c', 'c']], 'Z': [['Z', 'X']], 'A': [['X', 'B'], ['B']],
                 'B': [['y', 'X'], ['y']]}
    assert g.find_generating_terminals() == ['Y', 'B', 'X', 'A', 'S']


def test_find_generatic_terminals2():
    g = Grammar()
    g.grammar = {'S': [['a', 'A'], ['a', 'Z']], 'X': [['a', 'Y'], ['b', 'Y']],
                 'Y': [['a', 'Y'], ['b', 'Y'], ['c', 'c']], 'Z': [['Z', 'X']], 'A': [['X', 'B'], ['B']],
                 'B': [['y', 'X'], ['y']], 'R': [['Y', 'B', 'A', 'B', 'Y']]}
    assert g.find_generating_terminals() == ['Y', 'B', 'X', 'A', 'R', 'S']


def test_find_generatic_terminals3():
    g = Grammar()
    g.grammar = {'S': [['a', 'A'], ['a', 'Z']], 'X': [['a', 'Y'], ['b', 'Y']],
                 'Y': [['a', 'Y'], ['b', 'Y'], ['c', 'c']], 'Z': [['Z', 'X']], 'A': [['X', 'B'], ['B']],
                 'B': [['y', 'X'], ['y']], 'R': [['Y', 'B', 'A', 'B', 'Y', 'X', 'Z']]}
    assert g.find_generating_terminals() == ['Y', 'B', 'X', 'A', 'S']


def test_delete_nongenerating_terminals():
    g = Grammar()
    g.grammar = {'S': [['a', 'A'], ['a', 'Z']], 'X': [['a', 'Y'], ['b', 'Y']],
                 'Y': [['a', 'Y'], ['b', 'Y'], ['c', 'c']], 'Z': [['Z', 'X']], 'A': [['X', 'B'], ['B']],
                 'B': [['y', 'X'], ['y']], 'R': [['Y', 'B', 'A', 'B', 'Y', 'X']]}
    g.delete_nongenerating_terminals()
    assert g.grammar == {'S': [['a', 'A']], 'X': [['a', 'Y'], ['b', 'Y']], 'Y': [['a', 'Y'], ['b', 'Y'], ['c', 'c']],
                         'A': [['X', 'B'], ['B']], 'B': [['y', 'X'], ['y']], 'R': [['Y', 'B', 'A', 'B', 'Y', 'X']]}


def test_find_reachable_terminals():
    g = Grammar()
    g.grammar = {'S': [['a', 'A'], ['a', 'Z']], 'X': [['a', 'Y'], ['b', 'Y']],
                 'Y': [['a', 'Y'], ['b', 'Y'], ['c', 'c']], 'Z': [['Z', 'X']], 'A': [['X', 'B'], ['B']],
                 'B': [['y', 'X'], ['y']], 'R': [['Y', 'B', 'A', 'B', 'Y', 'X']]}
    assert g.find_reachable_terminals() == ['S', 'A', 'Z', 'X', 'B', 'Y']


def test_delete_unreachable_terminals():
    g = Grammar()
    g.grammar = {'S': [['a', 'A'], ['a', 'Z']], 'K': [['a', 'R']], 'Y': [['b', 'Y']], 'A': [['B']],
                 'B': [['y', 'X'], ['y']], 'R': [['Y', 'B', 'A', 'B', 'Y', 'X']]}
    g.delete_unreachable_terminals()
    assert g.grammar == {'S': [['a', 'A'], ['a', 'Z']], 'A': [['B']], 'B': [['y', 'X'], ['y']]}


def test_delete_useless_symbols():  # test from https://neerc.ifmo.ru/wiki/index.php?title=%D0%9D%D0%BE%D1%80%D0%BC%D0%B0%D0%BB%D1%8C%D0%BD%D0%B0%D1%8F_%D1%84%D0%BE%D1%80%D0%BC%D0%B0_%D0%A5%D0%BE%D0%BC%D1%81%D0%BA%D0%BE%D0%B3%D0%BE
    g = Grammar()
    g.grammar = {'S': [['a', 'A'], ['a', 'Z']], 'X': [['a', 'Y'], ['b', 'Y']],
                 'Y': [['a', 'Y'], ['b', 'Y'], ['c', 'c']], 'Z': [['Z', 'X']], 'A': [['X', 'B'], ['y', 'X'], ['y']],
                 'B': [['y', 'X'], ['y']]}
    g.delete_nongenerating_terminals()
    g.delete_unreachable_terminals()
    assert g.grammar == {'S': [['a', 'A']], 'X': [['a', 'Y'], ['b', 'Y']], 'Y': [['a', 'Y'], ['b', 'Y'], ['c', 'c']],
                         'A': [['X', 'B'], ['y', 'X'], ['y']], 'B': [['y', 'X'], ['y']]}


def test_delete_several_terminals1():
    g = Grammar()
    g.grammar = {'S': [['a', 'A']], 'X': [['a', 'Y'], ['b', 'Y']], 'Y': [['a', 'Y'], ['b', 'Y'], ['c', 'c']],
                 'A': [['X', 'B'], ['y', 'X'], ['y']], 'B': [['y', 'X'], ['y']]}
    g.delete_several_terminals()
    for (nt, rules) in g.grammar.items():
        for rule in rules:
            assert len(rule) <= 2
            if len(rule) == 2:
                assert rule[0].isupper()
                assert rule[1].isupper()


def test_delete_several_terminals2():
    g = Grammar()
    g.add_rule('S', ['a', 'B'])
    g.add_rule('S', ['c', 'a'])
    g.add_rule('B', ['B', 'a'])
    g.delete_several_terminals()
    for (nt, rules) in g.grammar.items():
        for rule in rules:
            assert len(rule) <= 2
            if len(rule) == 2:
                assert rule[0].isupper()
                assert rule[1].isupper()


def is_CNF_rule(nt, rule, start):
    for elem in rule:
        if elem == start:
            return False
        if elem == 'eps' and nt != start:
            return False
        if len(rule) > 2:
            return False
        if len(rule) == 2:
            if (not rule[0].isupper()) or (not rule[1].isupper()):
                return False
        if len(rule) == 1:
            if rule[0].isupper():
                return False
    return True


def is_CNF_grammar(g):
    for (nt, rules) in g.grammar.items():
        for rule in rules:
            if not is_CNF_rule(nt, rule, g.start):
                return False
    return True


def test_to_CNF1():
    g = Grammar()
    g.grammar = {'S': [['a', 'A']], 'X': [['a', 'Y'], ['eps'], ['b', 'Y']], 'Y': [['a', 'Y'], ['b', 'Y'], ['c', 'c']],
                 'B': [['eps'], ['y', 'X'], ['y']], 'A': [['X', 'B'], ['y', 'X'], ['y']]}
    assert not is_CNF_grammar(g)
    g.to_CNF()
    assert is_CNF_grammar(g)
    assert g.grammar == {'S': [['a'], ['C', 'A']], 'X': [['C', 'Y'], ['D', 'Y']], 'Y': [['C', 'Y'], ['D', 'Y'], ['E',
                                                                                                                 'E']],
                         'B': [['y'], ['F', 'X']], 'A': [['y'], ['X', 'B'], ['F', 'X'], ['C', 'Y'], ['D', 'Y']],
                         'C': [['a']], 'D': [['b']], 'E': ['c'], 'F': [['y']]}


def test_to_CNF2():
    g = Grammar()
    g.grammar = {'S': [['a', 'S', 'b', 'S'], ['eps']]}
    assert not is_CNF_grammar(g)
    g.to_CNF()
    assert is_CNF_grammar(g)
    assert g.grammar == {'A': [['C', 'B'], ['b'], ['D', 'C']], 'B': [['b'], ['D', 'C']], 'C': [['E', 'A']], 'S': [[
        'eps'], ['E', 'A']], 'D': [['b']], 'E': [['a']]}


def test_to_CNF3():
    g = Grammar()
    g.grammar = {'S': [['a', 'X', 'b', 'X'], ['a', 'Z']], 'X': [['a', 'Y'], ['b', 'Y'], ['eps']],
                 'Y': [['X'], ['c', 'c']], 'Z': [['Z', 'X']]}
    assert not is_CNF_grammar(g)
    g.to_CNF()
    assert is_CNF_grammar(g)
    assert g.grammar == {'S': [['C', 'A']], 'X': [['a'], ['D', 'Y'], ['C', 'Y']],
                         'Y': [['a'], ['E', 'E'], ['D', 'Y'], ['C', 'Y']], 'A': [['X', 'B'], ['b'], ['D', 'X']],
                         'B': [['b'], ['D', 'X']], 'C': [['a']], 'D': [['b']], 'E': ['c']}


def test_CYK1():
    g = Grammar()
    g.grammar = {'S': [['a', 'S', 'b', 'S'], ['eps']]}
    assert g.CYK('ab')
    assert g.CYK('aabbab')
    assert g.CYK('aababbaababb')
    assert not g.CYK('a')
    assert not g.CYK('abb')
    assert not g.CYK('aabbb')


def test_CYK2():
    g = Grammar()
    g.grammar = {'S': [['a', 'b', 'c', 'D', 'e', 'f', 'S'], ['eps'], ['g', 'h', 'D']], 'D': [['a', 'T', 'd']], 'T': [[
        'k']]}
    assert g.CYK('abcakdef')
    assert g.CYK('abcakdefabcakdef')
    assert g.CYK('abcakdefghakd')
    assert not g.CYK('abcakdefghak')
    assert not g.CYK('abcakcdefghakd')
    assert not g.CYK('abcefghakd')


def test_CYK3():
    g = Grammar()
    g.grammar = {'S': [['a', 'S'], ['eps']]}
    assert g.CYK('a')
    assert g.CYK('aa')
    assert g.CYK('aaa')
    assert g.CYK('aaaa')
    assert g.CYK('aaaaa')
    assert not g.CYK('bbaa')


def test_read_graph():
    g = Graph()
    test_dir = tempfile.gettempdir()
    f = open(path.join(test_dir, 'input.txt'), 'w')
    f.write('0 a 1\n 1 a 2\n 2 a 0\n 2 b 3\n 3 b 2\n')
    f.close()
    g.read_graph(path.join(test_dir, 'input.txt'))
    assert g.vertices == [0, 1, 2, 3]
    assert g.terminals == ['a', 'b']
    assert g.edges == [(0, 'a', 1), (1, 'a', 2), (2, 'a', 0), (2, 'b', 3), (3, 'b', 2)]


def test_read_empty_graph():
    g = Graph()
    test_dir = tempfile.gettempdir()
    f = open(path.join(test_dir, 'input.txt'), 'w')
    g.read_graph(path.join(test_dir, 'input.txt'))
    assert g.edges == []
    assert g.terminals == []
    assert g.vertices == []


def test_write_empty_reachable_pairs():
    g = Grammar()
    test_dir = tempfile.gettempdir()
    open(path.join(test_dir, 'output.txt'), 'w').close()
    g.write_reachable_pairs([], path.join(test_dir, 'output.txt'))
    f = open(path.join(test_dir, 'output.txt'), 'r')
    assert f.read() == ''


def test_write_reachable_pairs():
    g = Grammar()
    test_dir = tempfile.gettempdir()
    open(path.join(test_dir, 'output.txt'), 'w').close()
    g.write_reachable_pairs([('S', 1, 2), ('A', 0, 2), ('S', 1, 3)], path.join(test_dir, 'output.txt'))
    f = open(path.join(test_dir, 'out1.txt'), 'r')
    assert f.read() == '1 2\n1 3\n'


def test_hellings_init():
    g = Grammar()
    g.graph.vertices = [0, 1, 2, 3]
    g.graph.terminals = ['a', 'b']
    g.graph.edges = [(0, 'a', 1), (1, 'a', 2), (2, 'a', 0), (2, 'b', 3), (3, 'b', 2)]
    g.grammar = {'S': [['A', 'B'], ['A', 'S1']], 'S1': [['S', 'B']], 'A': [['a']], 'B': [['b']]}
    res = g.hellings_init()
    assert res == [('A', 0, 1), ('A', 1, 2), ('A', 2, 0), ('B', 2, 3), ('B', 3, 2)]


def test_hellings1():
    g = Grammar()
    g.graph.vertices = [0, 1, 2, 3]
    g.graph.terminals = ['a', 'b']
    g.graph.edges = [(0, 'a', 1), (1, 'a', 2), (2, 'a', 0), (2, 'b', 3), (3, 'b', 2)]
    g.grammar = {'S': [['A', 'B'], ['A', 'S1']], 'S1': [['S', 'B']], 'A': [['a']], 'B': [['b']]}
    res = g.hellings()
    good_res = [(1, 3), (0, 2), (2, 3), (1, 2), (0, 3), (2, 2)]
    count = 0
    for (nt, a, b) in res:
        if nt == 'S':
            count += 1
            assert (a,  b) in good_res
    assert count == len(good_res)


def test_hellings2():
    g = Grammar()
    g.graph.vertices = [0, 1, 2]
    g.graph.terminals = ['a', 'b', 'c']
    g.graph.edges = [(0, 'a', 1), (1, 'b', 0), (1, 'c', 2)]
    g.grammar = {'S': [['eps'], ['a', 'S']]}
    res = g.hellings()
    good_res = [(0, 0), (1, 1), (2, 2), (0, 1)]
    count = 0
    for (nt, a, b) in res:
        if nt == 'S':
            count += 1
            assert (a, b) in good_res
    assert count == len(good_res)


def test_hellings3():
    g = Grammar()
    g.graph.vertices = [0, 2, 3, 4]
    g.graph.terminals = ['a', 'b', 'c']
    g.graph.edges = [(0, 'a', 3), (3, 'b', 2), (2, 'c', 0), (3, 'a', 4)]
    g.grammar = {'S': [['A', 'S', 'B'], ['eps']], 'B': [['b'], ['eps'], ['S', 'A']], 'A': [['a'], ['eps']]}
    res = g.hellings()
    good_res = [(0, 0), (3, 3), (2, 2), (4, 4), (3, 4), (0, 4), (3, 2), (0, 2), (0, 3)]
    count = 0
    for (nt, a, b) in res:
        if nt == 'S':
            count += 1
            assert (a, b) in good_res
    assert count == len(good_res)