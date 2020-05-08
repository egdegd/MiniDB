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
    f.write('CONNECT TO [hh.txt] ;\n LIST ALL GRAPHS ;\n SELECT DISTANCE (a) FROM [gr.txt] ;\n')
    f.close()
    tree = read_script_from_file(path.join(test_dir, 'input.txt'))
    assert tree.toStringTree() == '([] ([28] ([34 28] CONNECT TO [hh.txt]) ; ([36 28] ([31 36 28] LIST ALL GRAPHS) ;) ([36 28] ([31 36 28] ([50 31 36 28] SELECT ([71 50 31 36 28] DISTANCE ([85 71 50 31 36 28] ( a ))) FROM [gr.txt])) ;)) <EOF>)'


def test_read_script_from_file3():
    test_dir = tempfile.gettempdir()
    f = open(path.join(test_dir, 'input.txt'), 'w')
    f.write('CONNECT TO [hh.txt] ;\n SELECT DEGREE (hello) FROM [from.txt] ;\n SELECT DISTANCE (a) FROM [gr.txt] ;\n')
    f.close()
    tree = read_script_from_file(path.join(test_dir, 'input.txt'))
    assert tree.toStringTree() == '([] ([28] ([34 28] CONNECT TO [hh.txt]) ; ([36 28] ([31 36 28] ([50 31 36 28] SELECT ([71 50 31 36 28] DEGREE ([83 71 50 31 36 28] ( hello ))) FROM [from.txt])) ;) ([36 28] ([31 36 28] ([50 31 36 28] SELECT ([71 50 31 36 28] DISTANCE ([85 71 50 31 36 28] ( a ))) FROM [gr.txt])) ;)) <EOF>)'


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
    f.write('CONNECT TO [hh.txt] ;\n LIST ALL GRAPHS ;\n SELECT DISTANCE (a) FROM [gr.txt] ;\n')
    f.close()
    tree = read_script_from_file(path.join(test_dir, 'input.txt'))
    check_script(tree)
    captured = capsys.readouterr()
    assert captured.out == 'script is correct\n'


def test_check_correct_scrpt3(capsys):
    test_dir = tempfile.gettempdir()
    f = open(path.join(test_dir, 'input.txt'), 'w')
    f.write('CONNECT TO [hh.txt] ;\n SELECT DEGREE (hello) FROM [from.txt] ;\n SELECT DISTANCE (a) FROM [gr.txt] ;\n')
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
    f.write('CONNECT TO [hh.txt] ;\n SELECT DEGREE (hello) FROM [from.txt] ;\n SELECT DISTANCE (a) FROM [gr.txt] ;\n')
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
    assert '[label= "DEGREE"]' in text
    assert '[label= "FROM"]' in text
    assert '[label= "DISTANCE"]' in text
    assert '[label= "("]' in text
    assert '[label= ")"]' in text
    assert '[label= "a"]' in text
    assert '[label= "[from.txt]"]' in text

