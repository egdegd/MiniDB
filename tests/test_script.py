import tempfile
from os import path
from os import mkdir

from _pytest import tmpdir

from src.script import *


def test_list_all_graphs(capsys):
    test_dir = tempfile.gettempdir()
    f = open(path.join(test_dir, 'input.txt'), 'w')
    f.write('CONNECT TO [tests/mydir] ;\n LIST ALL GRAPHS;')
    f.close()
    read_script_from_file(path.join(test_dir, 'input.txt'))
    captured = capsys.readouterr()
    assert captured.out == '[\'graph1.txt\', \'graph2.txt\', \'graph3.txt\']\n'


def test_pattern1():
    test_dir = tempfile.gettempdir()
    f = open(path.join(test_dir, 'input.txt'), 'w')
    f.write('S = S a S b ;')
    f.close()
    collector = read_script_from_file(path.join(test_dir, 'input.txt'))
    assert collector.grammar.grammar == {'S': [['S', 'a', 'S', 'b']]}


def test_pattern2():
    test_dir = tempfile.gettempdir()
    f = open(path.join(test_dir, 'input.txt'), 'w')
    f.write('S = S a S b | A S B;\n A = a;\n B = b;')
    f.close()
    collector = read_script_from_file(path.join(test_dir, 'input.txt'))
    assert collector.grammar.grammar == {'S': [['S', 'a', 'S', 'b'], ['A', 'S', 'B']], 'A': [['a']], 'B': [['b']]}


def test_pattern3():
    test_dir = tempfile.gettempdir()
    f = open(path.join(test_dir, 'input.txt'), 'w')
    f.write('CONNECT TO [tests/mydir];\n S = S a S b |  ();\n S = a;\n S = A B; \n B = b;')
    f.close()
    collector = read_script_from_file(path.join(test_dir, 'input.txt'))
    assert collector.grammar.grammar == {'S': [['S', 'a', 'S', 'b'], ['eps'], ['a'], ['A', 'B']], 'B': [['b']]}


def test_patter_eps():
    test_dir = tempfile.gettempdir()
    f = open(path.join(test_dir, 'input.txt'), 'w')
    f.write('S = ();')
    f.close()
    collector = read_script_from_file(path.join(test_dir, 'input.txt'))
    assert collector.grammar.grammar == {'S': [['eps']]}


def test_clean_where_expr():
    test_dir = tempfile.gettempdir()
    f = open(path.join(test_dir, 'input.txt'), 'w')
    f.write('CONNECT TO [tests/mydir];\nSELECT EXISTS (a, b) FROM [graph1.txt] WHERE (a.ID = 1) - a -> (b.ID = 2);')
    f.close()
    collector = read_script_from_file(path.join(test_dir, 'input.txt'))
    assert collector.id_second_v == -1
    assert collector.id_first_v == -1


def test_exists_empty_graph(capsys):
    test_dir = tempfile.gettempdir()
    f = open(path.join(test_dir, 'input.txt'), 'w')
    f.write('CONNECT TO [tests/mydir];\nS = a;\n SELECT EXISTS (a, b) FROM [graph3.txt] WHERE (a) - S -> (b);')
    f.close()
    read_script_from_file(path.join(test_dir, 'input.txt'))
    captured = capsys.readouterr()
    assert captured.out == 'False\n'


def test_exists1(capsys):
    test_dir = tempfile.gettempdir()
    f = open(path.join(test_dir, 'input.txt'), 'w')
    f.write('CONNECT TO [tests/mydir];\nSELECT EXISTS (a, b) FROM [graph1.txt] WHERE (a.ID = 0) - a -> (b.ID = 1);')
    f.close()
    read_script_from_file(path.join(test_dir, 'input.txt'))
    captured = capsys.readouterr()
    assert captured.out == 'True\n'


def test_exists2(capsys):
    test_dir = tempfile.gettempdir()
    f = open(path.join(test_dir, 'input.txt'), 'w')
    f.write('CONNECT TO [tests/mydir];\nSELECT EXISTS (a, b) FROM [graph2.txt] WHERE (a.ID = 0) - a a d -> (b.ID = 2);')
    f.close()
    read_script_from_file(path.join(test_dir, 'input.txt'))
    captured = capsys.readouterr()
    assert captured.out == 'True\n'


def test_exists3(capsys):
    test_dir = tempfile.gettempdir()
    f = open(path.join(test_dir, 'input.txt'), 'w')
    f.write('CONNECT TO [tests/mydir];\nSELECT EXISTS (a, b) FROM [graph2.txt] WHERE (a.ID = 0) - a a -> (b.ID = 2);')
    f.close()
    read_script_from_file(path.join(test_dir, 'input.txt'))
    captured = capsys.readouterr()
    assert captured.out == 'False\n'


def test_exists4(capsys):
    test_dir = tempfile.gettempdir()
    f = open(path.join(test_dir, 'input.txt'), 'w')
    f.write('CONNECT TO [tests/mydir];\nS = A A d;\n A = a;\n SELECT EXISTS (a, b) FROM [graph2.txt] WHERE (a.ID = 0) - S -> (b.ID = 2);')
    f.close()
    read_script_from_file(path.join(test_dir, 'input.txt'))
    captured = capsys.readouterr()
    assert captured.out == 'True\n'


def test_exists5(capsys):
    test_dir = tempfile.gettempdir()
    f = open(path.join(test_dir, 'input.txt'), 'w')
    f.write('CONNECT TO [tests/mydir];\nS = A A d | a c;\n A = a;\n SELECT EXISTS (a, b) FROM [graph2.txt] WHERE (a.ID = 0) - a S -> (b.ID = 0);')
    f.close()
    read_script_from_file(path.join(test_dir, 'input.txt'))
    captured = capsys.readouterr()
    assert captured.out == 'True\n'


def test_exists6(capsys):
    test_dir = tempfile.gettempdir()
    f = open(path.join(test_dir, 'input.txt'), 'w')
    f.write('CONNECT TO [tests/mydir];\nS = A A d ;\n A = a;\n SELECT EXISTS (a, b) FROM [graph2.txt] WHERE (a) - A c -> (b.ID = 0);')
    f.close()
    read_script_from_file(path.join(test_dir, 'input.txt'))
    captured = capsys.readouterr()
    assert captured.out == 'True\n'


def test_exists7(capsys):
    test_dir = tempfile.gettempdir()
    f = open(path.join(test_dir, 'input.txt'), 'w')
    f.write('CONNECT TO [tests/mydir];\n SELECT EXISTS (a, b) FROM [graph1.txt] WHERE (a) - a r b -> (b);')
    f.close()
    read_script_from_file(path.join(test_dir, 'input.txt'))
    captured = capsys.readouterr()
    assert captured.out == 'True\n'


def test_exists8(capsys):
    test_dir = tempfile.gettempdir()
    f = open(path.join(test_dir, 'input.txt'), 'w')
    f.write('CONNECT TO [tests/mydir];\n SELECT EXISTS (a, b) FROM [graph1.txt] WHERE (a) - a r a -> (b);')
    f.close()
    read_script_from_file(path.join(test_dir, 'input.txt'))
    captured = capsys.readouterr()
    assert captured.out == 'False\n'
