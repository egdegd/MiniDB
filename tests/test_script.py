import tempfile
from os import path
from os import mkdir

from _pytest import tmpdir

from src.script import *


def create_and_test_file(text):
    test_dir = tempfile.gettempdir()
    f = open(path.join(test_dir, 'input.txt'), 'w')
    f.write(text)
    f.close()
    collector = read_script_from_file(path.join(test_dir, 'input.txt'))
    return collector


def test_list_all_graphs(capsys):
    create_and_test_file('CONNECT TO [tests/mydir] ;\n LIST ALL GRAPHS;')
    captured = capsys.readouterr()
    assert captured.out == '[\'graph1.txt\', \'graph2.txt\', \'graph3.txt\']\n'


def test_pattern1():
    collector = create_and_test_file('S = S a S b ;')
    assert collector.grammar.grammar == {'S': [['S', 'a', 'S', 'b']]}


def test_pattern2():
    collector = create_and_test_file('S = S a S b | A S B;\n A = a;\n B = b;')
    assert collector.grammar.grammar == {'S': [['S', 'a', 'S', 'b'], ['A', 'S', 'B']], 'A': [['a']], 'B': [['b']]}


def test_pattern3():
    collector = create_and_test_file('CONNECT TO [tests/mydir];\n S = S a S b |  ();\n S = a;\n S = A B; \n B = b;')
    assert collector.grammar.grammar == {'S': [['S', 'a', 'S', 'b'], ['eps'], ['a'], ['A', 'B']], 'B': [['b']]}


def test_patter_eps():
    collector = create_and_test_file('S = ();')
    assert collector.grammar.grammar == {'S': [['eps']]}


def test_clean_where_expr():
    collector = create_and_test_file('CONNECT TO [tests/mydir];\nSELECT EXISTS (a, b) FROM [graph1.txt] WHERE (a.ID = 1) - a -> (b.ID = 2);')
    assert collector.id_second_v == -1
    assert collector.id_first_v == -1


def test_exists_empty_graph(capsys):
    create_and_test_file('CONNECT TO [tests/mydir];\nS = a;\n SELECT EXISTS (a, b) FROM [graph3.txt] WHERE (a) - S -> (b);')
    captured = capsys.readouterr()
    assert captured.out == 'False\n'


def test_exists1(capsys):
    create_and_test_file('CONNECT TO [tests/mydir];\nSELECT EXISTS (a, b) FROM [graph1.txt] WHERE (a.ID = 0) - a -> (b.ID = 1);')
    captured = capsys.readouterr()
    assert captured.out == 'True\n'


def test_exists2(capsys):
    create_and_test_file('CONNECT TO [tests/mydir];\nSELECT EXISTS (a, b) FROM [graph2.txt] WHERE (a.ID = 0) - a a d -> (b.ID = 2);')
    captured = capsys.readouterr()
    assert captured.out == 'True\n'


def test_exists3(capsys):
    create_and_test_file('CONNECT TO [tests/mydir];\nSELECT EXISTS (a, b) FROM [graph2.txt] WHERE (a.ID = 0) - a a -> (b.ID = 2);')
    captured = capsys.readouterr()
    assert captured.out == 'False\n'


def test_exists4(capsys):
    create_and_test_file('CONNECT TO [tests/mydir];\nS = A A d;\n A = a;\n SELECT EXISTS (a, b) FROM [graph2.txt] WHERE (a.ID = 0) - S -> (b.ID = 2);')
    captured = capsys.readouterr()
    assert captured.out == 'True\n'


def test_exists5(capsys):
    create_and_test_file('CONNECT TO [tests/mydir];\nS = A A d | a c;\n A = a;\n SELECT EXISTS (a, b) FROM [graph2.txt] WHERE (a.ID = 0) - a S -> (b.ID = 0);')
    captured = capsys.readouterr()
    assert captured.out == 'True\n'


def test_exists6(capsys):
    create_and_test_file('CONNECT TO [tests/mydir];\nS = A A d ;\n A = a;\n SELECT EXISTS (a, b) FROM [graph2.txt] WHERE (a) - A c -> (b.ID = 0);')
    captured = capsys.readouterr()
    assert captured.out == 'True\n'


def test_exists7(capsys):
    create_and_test_file('CONNECT TO [tests/mydir];\n SELECT EXISTS (a, b) FROM [graph1.txt] WHERE (a) - a r b -> (b);')
    captured = capsys.readouterr()
    assert captured.out == 'True\n'


def test_exists8(capsys):
    create_and_test_file('CONNECT TO [tests/mydir];\n SELECT EXISTS (a, b) FROM [graph1.txt] WHERE (a) - a r a -> (b);')
    captured = capsys.readouterr()
    assert captured.out == 'False\n'
