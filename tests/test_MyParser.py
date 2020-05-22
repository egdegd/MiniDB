import tempfile
from os import path

from src.MyParser import *


def test_read_empty_script_from_file():
    test_dir = tempfile.gettempdir()
    f = open(path.join(test_dir, 'input.txt'), 'w')
    f.write('')
    f.close()
    tree = read_script_from_file(path.join(test_dir, 'input.txt'))
    assert tree is None


def test_read_script_from_file1():
    test_dir = tempfile.gettempdir()
    f = open(path.join(test_dir, 'input.txt'), 'w')
    f.write('CONNECT TO [hh.txt] ;\n')
    f.close()
    tree = read_script_from_file(path.join(test_dir, 'input.txt'))
    assert tree.toStringTree() == '([] ([30] ([33 30] CONNECT TO [hh.txt]) ;) <EOF>)'


def test_read_script_from_file2():
    test_dir = tempfile.gettempdir()
    f = open(path.join(test_dir, 'input.txt'), 'w')
    f.write('CONNECT TO [hh.txt] ;\n LIST ALL GRAPHS ;\n SELECT COUNT (a) FROM [gr.txt] WHERE (b.ID = 1) -S-> (a);\n')
    f.close()
    tree = read_script_from_file(path.join(test_dir, 'input.txt'))
    assert tree.toStringTree() == '([] ([30] ([36 30] CONNECT TO [hh.txt]) ; ([38 30] ([33 38 30] ([49 33 38 30] LIST ALL GRAPHS)) ;) ([38 30] ([33 38 30] ([50 33 38 30] SELECT ([74 50 33 38 30] COUNT ([82 74 50 33 38 30] ( a ))) FROM [gr.txt] WHERE ([78 50 33 38 30] ( ([98 78 50 33 38 30] b . ID = 1) ) - ([101 78 50 33 38 30] ([117 101 78 50 33 38 30] ([124 117 101 78 50 33 38 30] ([129 124 117 101 78 50 33 38 30] ([135 129 124 117 101 78 50 33 38 30] S))))) - > ( ([105 78 50 33 38 30] a) )))) ;)) <EOF>)'


def test_read_script_from_file3():
    test_dir = tempfile.gettempdir()
    f = open(path.join(test_dir, 'input.txt'), 'w')
    f.write('CONNECT TO [hh.txt] ;\n SELECT EXISTS (hello) FROM [from.txt] WHERE (hello) - a a | S -> (b.ID = 1) ;\n')
    f.close()
    tree = read_script_from_file(path.join(test_dir, 'input.txt'))
    assert tree.toStringTree() == '([] ([30] ([36 30] CONNECT TO [hh.txt]) ; ([38 30] ([33 38 30] ([50 33 38 30] SELECT ([74 50 33 38 30] EXISTS ([84 74 50 33 38 30] ( hello ))) FROM [from.txt] WHERE ([78 50 33 38 30] ( ([98 78 50 33 38 30] hello) ) - ([101 78 50 33 38 30] ([118 101 78 50 33 38 30] ([124 118 101 78 50 33 38 30] ([130 124 118 101 78 50 33 38 30] ([135 130 124 118 101 78 50 33 38 30] a)) ([131 124 118 101 78 50 33 38 30] ([129 131 124 118 101 78 50 33 38 30] ([135 129 131 124 118 101 78 50 33 38 30] a))))) | ([120 101 78 50 33 38 30] ([117 120 101 78 50 33 38 30] ([124 117 120 101 78 50 33 38 30] ([129 124 117 120 101 78 50 33 38 30] ([135 129 124 117 120 101 78 50 33 38 30] S)))))) - > ( ([105 78 50 33 38 30] b . ID = 1) )))) ;)) <EOF>)'


def test_check_correct_scrpt1(capsys):
    test_dir = tempfile.gettempdir()
    f = open(path.join(test_dir, 'input.txt'), 'w')
    f.write('CONNECT TO [hh.txt] ;\n')
    f.close()
    tree = read_script_from_file(path.join(test_dir, 'input.txt'))
    check_script(tree)
    captured = capsys.readouterr()
    assert captured.out == 'script is correct\n'


def test_check_correct_scrpt2(capsys):
    test_dir = tempfile.gettempdir()
    f = open(path.join(test_dir, 'input.txt'), 'w')
    f.write('CONNECT TO [hh.txt] ;\n LIST ALL GRAPHS ;\n SELECT COUNT (a, b) FROM [gr.txt] WHERE (a) - S -> (b);\n')
    f.close()
    tree = read_script_from_file(path.join(test_dir, 'input.txt'))
    check_script(tree)
    captured = capsys.readouterr()
    assert captured.out == 'script is correct\n'


def test_check_correct_scrpt3(capsys):
    test_dir = tempfile.gettempdir()
    f = open(path.join(test_dir, 'input.txt'), 'w')
    f.write('CONNECT TO [hh.txt] ;\n SELECT EXISTS (hello) FROM [from.txt] WHERE (hwllo.ID = 1) - A -> (b) ;\n SELECT COUNT (a) FROM [gr.txt] WHERE (a) - S -> (b);\n')
    f.close()
    tree = read_script_from_file(path.join(test_dir, 'input.txt'))
    check_script(tree)
    captured = capsys.readouterr()
    assert captured.out == 'script is correct\n'


def test_check_incorrect_scrpt1(capsys):
    test_dir = tempfile.gettempdir()
    f = open(path.join(test_dir, 'input.txt'), 'w')
    f.write('CONNECT TO [hh.txt] \n')
    f.close()
    tree = read_script_from_file(path.join(test_dir, 'input.txt'))
    check_script(tree)
    captured = capsys.readouterr()
    assert captured.out == 'script is incorrect\n'


def test_check_incorrect_scrpt2(capsys):
    test_dir = tempfile.gettempdir()
    f = open(path.join(test_dir, 'input.txt'), 'w')
    f.write('CONNECT TO [hh.txt] ;\n LIST ALL GRAPHS ;\n SELECT DISTANCE (a); \n')
    f.close()
    tree = read_script_from_file(path.join(test_dir, 'input.txt'))
    check_script(tree)
    captured = capsys.readouterr()
    assert captured.out == 'script is incorrect\n'


def test_write_tree1():
    test_dir = tempfile.gettempdir()
    f = open(path.join(test_dir, 'input.txt'), 'w')
    f.write('CONNECT TO [hh.txt] ;\n')
    f.close()
    tree = read_script_from_file(path.join(test_dir, 'input.txt'))
    write_tree(tree, path.join(test_dir, 'out.txt'))
    f = open(path.join(test_dir, 'out.txt'), 'r')
    text = f.read()
    assert 'digraph' in text
    assert '[label= "<EOF>"]' in text
    assert '[label= "script"]' in text
    assert '[label= ";"]' in text
    assert '[label= "stmt"]' in text
    assert '[label= "CONNECT"]' in text
    assert '[label= "TO"]' in text
    assert '[label= "[hh.txt]"]' in text


def test_write_tree2():
    test_dir = tempfile.gettempdir()
    f = open(path.join(test_dir, 'input.txt'), 'w')
    f.write('CONNECT TO [hh.txt] ;\n SELECT EXISTS (hello) FROM [from.txt] WHERE (hello.ID = 1) - A -> (b) ;\n')
    f.close()
    tree = read_script_from_file(path.join(test_dir, 'input.txt'))
    write_tree(tree, path.join(test_dir, 'out.txt'))
    f = open(path.join(test_dir, 'out.txt'), 'r')
    text = f.read()
    assert 'digraph' in text
    assert '[label= "<EOF>"]' in text
    assert '[label= "script"]' in text
    assert '[label= ";"]' in text
    assert '[label= "stmt"]' in text
    assert '[label= "CONNECT"]' in text
    assert '[label= "TO"]' in text
    assert '[label= "[hh.txt]"]' in text
    assert '[label= "SELECT"]' in text
    assert '[label= "FROM"]' in text
    assert '[label= "("]' in text
    assert '[label= ")"]' in text
    assert '[label= "[from.txt]"]' in text
