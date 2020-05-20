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
    assert tree.toStringTree() == '([] ([28] ([31 28] CONNECT TO [hh.txt]) ;) <EOF>)'


def test_read_script_from_file2():
    test_dir = tempfile.gettempdir()
    f = open(path.join(test_dir, 'input.txt'), 'w')
    f.write('CONNECT TO [hh.txt] ;\n LIST ALL GRAPHS ;\n SELECT COUNT (a) FROM [gr.txt] WHERE (b.ID = 1) -S-> (a);\n')
    f.close()
    tree = read_script_from_file(path.join(test_dir, 'input.txt'))
    assert tree.toStringTree() == '([] ([28] ([34 28] CONNECT TO [hh.txt]) ; ([36 28] ([31 36 28] LIST ALL GRAPHS) ;) ([36 28] ([31 36 28] ([50 31 36 28] SELECT ([64 50 31 36 28] COUNT ([72 64 50 31 36 28] ( a ))) FROM [gr.txt] WHERE ([68 50 31 36 28] ( ([88 68 50 31 36 28] b . ID = 1) ) - ([91 68 50 31 36 28] ([107 91 68 50 31 36 28] ([114 107 91 68 50 31 36 28] ([119 114 107 91 68 50 31 36 28] ([125 119 114 107 91 68 50 31 36 28] S))))) - > ( ([95 68 50 31 36 28] a) )))) ;)) <EOF>)'


def test_read_script_from_file3():
    test_dir = tempfile.gettempdir()
    f = open(path.join(test_dir, 'input.txt'), 'w')
    f.write('CONNECT TO [hh.txt] ;\n SELECT EXISTS (hello) FROM [from.txt] WHERE (hello) - a a | S -> (b.ID = 1) ;\n')
    f.close()
    tree = read_script_from_file(path.join(test_dir, 'input.txt'))
    assert tree.toStringTree() == '([] ([28] ([34 28] CONNECT TO [hh.txt]) ; ([36 28] ([31 36 28] ([50 31 36 28] SELECT ([64 50 31 36 28] EXISTS ([74 64 50 31 36 28] ( hello ))) FROM [from.txt] WHERE ([68 50 31 36 28] ( ([88 68 50 31 36 28] hello) ) - ([91 68 50 31 36 28] ([108 91 68 50 31 36 28] ([114 108 91 68 50 31 36 28] ([120 114 108 91 68 50 31 36 28] ([125 120 114 108 91 68 50 31 36 28] a)) ([121 114 108 91 68 50 31 36 28] ([119 121 114 108 91 68 50 31 36 28] ([125 119 121 114 108 91 68 50 31 36 28] a))))) | ([110 91 68 50 31 36 28] ([107 110 91 68 50 31 36 28] ([114 107 110 91 68 50 31 36 28] ([119 114 107 110 91 68 50 31 36 28] ([125 119 114 107 110 91 68 50 31 36 28] S)))))) - > ( ([95 68 50 31 36 28] b . ID = 1) )))) ;)) <EOF>)'


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
