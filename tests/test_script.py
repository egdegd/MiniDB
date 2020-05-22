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


def test_list_all_graphs1(capsys):
    create_and_test_file('CONNECT TO [tests/mydir] ;\n LIST ALL GRAPHS;')
    captured = capsys.readouterr()
    assert captured.out == '[\'graph1.txt\', \'graph2.txt\', \'graph3.txt\', \'graph4.txt\']\n'


def test_list_all_graphs2(capsys):
    create_and_test_file('CONNECT TO [tests/mydir2] ;\n LIST ALL GRAPHS;')
    captured = capsys.readouterr()
    assert captured.out == '[\'g1.txt\', \'g2.txt\', \'g3.txt\']\n'


def test_list_all_graphs3(capsys):
    create_and_test_file('CONNECT TO [tests/mydir] ;\n LIST ALL GRAPHS FROM [tests/mydir];')
    captured = capsys.readouterr()
    assert captured.out == '[\'graph1.txt\', \'graph2.txt\', \'graph3.txt\', \'graph4.txt\']\n'


def test_list_all_graphs4(capsys):
    create_and_test_file('CONNECT TO [tests/mydir] ;\n LIST ALL GRAPHS FROM [tests/mydir2];')
    captured = capsys.readouterr()
    assert captured.out == '[\'g1.txt\', \'g2.txt\', \'g3.txt\']\n'


def test_list_all_graphs5(capsys):
    create_and_test_file('CONNECT TO [tests/mydir2] ;\n LIST ALL GRAPHS FROM [tests/mydir];\n LIST ALL GRAPHS;')
    captured = capsys.readouterr()
    assert captured.out == '[\'graph1.txt\', \'graph2.txt\', \'graph3.txt\', \'graph4.txt\']\n[\'g1.txt\', \'g2.txt\', \'g3.txt\']\n'


def test_pattern1():
    collector = create_and_test_file('S = S a S b ;')
    assert collector.grammar.grammar == {'A': [['S']], 'B': [['a']], 'C': [['S']], 'D': [['b']], 'E': [['C', 'D']],
                                         'F': [['B', 'E']], 'G': [['A', 'F']], 'S': [['G']]}


def test_pattern2():
    collector = create_and_test_file('S = S a S b | A S B | ();\n A = a;\n B = b;')
    assert collector.grammar.CYK('a b')
    assert collector.grammar.CYK('a b a b')
    assert collector.grammar.CYK('a a a b b b')
    assert collector.grammar.CYK('a b a a b a b b')
    assert not collector.grammar.CYK('a a c')


def test_pattern3():
    collector = create_and_test_file('CONNECT TO [tests/mydir];\n S = S a S b |  ();\n S = a;\n S = A B; \n B = b;')
    assert collector.grammar.grammar == {'A': [['S']], 'B': [['a'], ['N']], 'C': [['S']], 'D': [['b']],
                                         'E': [['C', 'D']], 'F': [['B', 'E']], 'G': [['A', 'F']], 'H': [['eps']],
                                         'I': [['G'], ['H']], 'S': [['I'], ['J'], ['M']], 'J': [['a']], 'K': [['A']],
                                         'L': [['B']], 'M': [['K', 'L']], 'N': [['b']]}


def test_patter_eps():
    collector = create_and_test_file('S = ();')
    assert collector.grammar.grammar == {'A': [['eps']], 'S': [['A']]}


def test_clean_where_expr():
    collector = create_and_test_file(
        'CONNECT TO [tests/mydir];\nSELECT EXISTS (a, b) FROM [graph1.txt] WHERE (a.ID = 1) - a -> (b.ID = 2);')
    assert collector.id_second_v == -1
    assert collector.id_first_v == -1


def test_exists_empty_graph(capsys):
    create_and_test_file(
        'CONNECT TO [tests/mydir];\nS = a;\n SELECT EXISTS (a, b) FROM [graph3.txt] WHERE (a) - S -> (b);')
    captured = capsys.readouterr()
    assert captured.out == 'False\n'


def test_exists1(capsys):
    create_and_test_file(
        'CONNECT TO [tests/mydir];\nSELECT EXISTS (a, b) FROM [graph1.txt] WHERE (a.ID = 0) - a -> (b.ID = 1);')
    captured = capsys.readouterr()
    assert captured.out == 'True\n'


def test_exists2(capsys):
    create_and_test_file(
        'CONNECT TO [tests/mydir];\nSELECT EXISTS (a, b) FROM [graph2.txt] WHERE (a.ID = 0) - a a d -> (b.ID = 2);')
    captured = capsys.readouterr()
    assert captured.out == 'True\n'


def test_exists3(capsys):
    create_and_test_file(
        'CONNECT TO [tests/mydir];\nSELECT EXISTS (a, b) FROM [graph2.txt] WHERE (a.ID = 0) - a a -> (b.ID = 2);')
    captured = capsys.readouterr()
    assert captured.out == 'False\n'


def test_exists4(capsys):
    create_and_test_file(
        'CONNECT TO [tests/mydir];\nS = A A d;\n A = a;\n SELECT EXISTS (a, b) FROM [graph2.txt] WHERE (a.ID = 0) - S -> (b.ID = 2);')
    captured = capsys.readouterr()
    assert captured.out == 'True\n'


def test_exists5(capsys):
    create_and_test_file(
        'CONNECT TO [tests/mydir];\nS = A A d | a c;\n A = a;\n SELECT EXISTS (a, b) FROM [graph2.txt] WHERE (a.ID = 0) - a S -> (b.ID = 0);')
    captured = capsys.readouterr()
    assert captured.out == 'True\n'


def test_exists6(capsys):
    create_and_test_file(
        'CONNECT TO [tests/mydir];\nS = A A d ;\n A = a;\n SELECT EXISTS (a, b) FROM [graph2.txt] WHERE (a) - A c -> (b.ID = 0);')
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


def test_regex1():
    collector = create_and_test_file('S = a + ;')
    collector.grammar.grammar = {'A': [['a']], 'B': [['A'], ['A', 'B']], 'S': [['B']]}


def test_regex2():
    collector = create_and_test_file('S = (a | b) +;')
    assert collector.grammar.CYK('a')
    assert collector.grammar.CYK('a a a')
    assert collector.grammar.CYK('a b ')
    assert collector.grammar.CYK('a b a a b')
    assert not collector.grammar.CYK('a a b c a')


def test_regex3():
    collector = create_and_test_file('S = ((a b | b) +) | (c +) ;')
    assert not collector.grammar.CYK('a')
    assert collector.grammar.CYK('a b b a b a b')
    assert collector.grammar.CYK('a b ')
    assert collector.grammar.CYK('c c c')
    assert not collector.grammar.CYK('a a b c a')


def test_regex4():
    collector = create_and_test_file('S = a * ;')
    assert collector.grammar.CYK('a')
    assert collector.grammar.CYK('')
    assert collector.grammar.CYK('a a a')
    assert not collector.grammar.CYK('a b a a')


def test_regex5():
    collector = create_and_test_file('S = a ? ;')
    assert collector.grammar.CYK('a')
    assert collector.grammar.CYK('')
    assert not collector.grammar.CYK('a a a')
    assert not collector.grammar.CYK('a b a a')


def test_regex6():
    collector = create_and_test_file('S = (a * | (a b) + )? ;')
    assert collector.grammar.CYK('a')
    assert collector.grammar.CYK('')
    assert collector.grammar.CYK('a a a')
    assert collector.grammar.CYK('a b a b')
    assert not collector.grammar.CYK('a b a a')


def test_count1(capsys):
    create_and_test_file(
        'CONNECT TO [tests/mydir];\nSELECT COUNT (a, b) FROM [graph1.txt] WHERE (a.ID = 0) - a -> (b.ID = 1);')
    captured = capsys.readouterr()
    assert captured.out == '1\n'


def test_count2(capsys):
    create_and_test_file(
        'CONNECT TO [tests/mydir];\nSELECT COUNT (a, b) FROM [graph4.txt] WHERE (a.ID = 0) - a* -> (b);')
    captured = capsys.readouterr()
    assert captured.out == '6\n'


def test_count3(capsys):
    create_and_test_file(
        'CONNECT TO [tests/mydir];\n S = (a b)?; \nSELECT COUNT (a, b) FROM [graph4.txt] WHERE (a.ID = 0) - S -> (b);')
    captured = capsys.readouterr()
    assert captured.out == '3\n'


def test_count4(capsys):
    create_and_test_file(
        'CONNECT TO [tests/mydir];\n S = (a b)?; \nSELECT COUNT (a, b) FROM [graph4.txt] WHERE (a) - a -> (b);')
    captured = capsys.readouterr()
    assert captured.out == '10\n'


def test_count5(capsys):
    create_and_test_file(
        'CONNECT TO [tests/mydir];\n S = (a)+; \nSELECT COUNT (a, b) FROM [graph2.txt] WHERE (a.ID = 0) - S -> (b);')
    captured = capsys.readouterr()
    assert captured.out == '2\n'


def test_count6(capsys):
    create_and_test_file(
        'CONNECT TO [tests/mydir];\n A = a; \n R = r; \n SELECT COUNT (a, b) FROM [graph1.txt] WHERE (a) - A R b  -> (b);')
    captured = capsys.readouterr()
    assert captured.out == '1\n'


def test_count7(capsys):
    create_and_test_file(
        'CONNECT TO [tests/mydir];\n S = b*; \nSELECT COUNT (b) FROM [graph4.txt] WHERE (a.ID = 4) - a S-> (b);')
    captured = capsys.readouterr()
    assert captured.out == '5\n'


def test_count8(capsys):
    create_and_test_file(
        'CONNECT TO [tests/mydir];\n S = b +; \nSELECT COUNT (a) FROM [graph4.txt] WHERE (a) - S c -> (b.ID = 3);')
    captured = capsys.readouterr()
    assert captured.out == '3\n'


def test_info1(capsys):
    create_and_test_file(
        'CONNECT TO [tests/mydir];\n S = a; \nSELECT (x) FROM [graph2.txt] WHERE (_) - S -> (x);')
    captured = capsys.readouterr()
    assert captured.out == '1\n3\n'


def test_info2(capsys):
    create_and_test_file(
        'CONNECT TO [tests/mydir];\n S = a; \nSELECT (x) FROM [graph2.txt] WHERE (x) - S -> (_);')
    captured = capsys.readouterr()
    assert captured.out == '0\n3\n'


def test_info3(capsys):
    create_and_test_file(
        'CONNECT TO [tests/mydir];\n S = a; \nSELECT (x) FROM [graph2.txt] WHERE (x) - S -> (y.ID = 3);')
    captured = capsys.readouterr()
    assert captured.out == '0\n'


def test_info4(capsys):
    create_and_test_file(
        'CONNECT TO [tests/mydir];\n S = a; \nSELECT (u, v) FROM [graph2.txt] WHERE (u) - S -> (v);')
    captured = capsys.readouterr()
    assert captured.out == '(0,3)\n(3,1)\n'


def test_info5(capsys):
    create_and_test_file(
        'CONNECT TO [tests/mydir];\n S = a; \nSELECT (u, v) FROM [graph2.txt] WHERE (u) - S -> (v.ID = 3);')
    captured = capsys.readouterr()
    assert captured.out == '(0,3)\n'


def test_info6(capsys):
    create_and_test_file(
        'CONNECT TO [tests/mydir];\n S = a; \nSELECT (u, v) FROM [graph2.txt] WHERE (u.ID = 3) - S -> (v);')
    captured = capsys.readouterr()
    assert captured.out == '(3,1)\n'


def test_info7(capsys):
    create_and_test_file(
        'CONNECT TO [tests/mydir];\n S = a; \nSELECT (u, v) FROM [graph2.txt] WHERE (u.ID = 3) - S -> (v.ID = 1);')
    captured = capsys.readouterr()
    assert captured.out == '(3,1)\n'


def test_info8(capsys):
    create_and_test_file(
        'CONNECT TO [tests/mydir];\n S = a; \nSELECT (u) FROM [graph2.txt] WHERE (u) - S -> (v.ID = 2);')
    captured = capsys.readouterr()
    assert captured.out == '\n'


def test_several_select1(capsys):
    create_and_test_file(
        'CONNECT TO [tests/mydir];\n '
        'S = a; \n'
        'SELECT EXISTS (u, v) FROM [graph2.txt] WHERE (u) - S -> (v);\n'
        'SELECT (u, v) FROM [graph2.txt] WHERE (u) - S -> (v);\n'
        'SELECT COUNT (u, v) FROM [graph2.txt] WHERE (u) - S -> (v);')
    captured = capsys.readouterr()
    assert captured.out == 'True\n(0,3)\n(3,1)\n2\n'


def test_several_select2(capsys):
    create_and_test_file(
        'CONNECT TO [tests/mydir];\n '
        'S = a; \n'
        'SELECT EXISTS (u, v) FROM [graph4.txt] WHERE (u) - S b* -> (v);\n'
        'SELECT (u, v) FROM [graph4.txt] WHERE (u) - S b* -> (v);\n'
        'SELECT COUNT (u, v) FROM [graph4.txt] WHERE (u) - S b* -> (v);')
    captured = capsys.readouterr()
    assert captured.out == 'True\n(0,1)\n(0,2)\n(0,3)\n(0,4)\n(0,5)\n(1,0)\n(1,2)\n(2,3)\n(2,4)\n(2,5)\n(3,4)\n(4,0)\n(4,2)\n(4,3)\n(4,4)\n(4,5)\n16\n'

