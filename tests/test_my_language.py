import tempfile
from os import path

from src.my_language import *


def test_parser_empty():
    test_dir = tempfile.gettempdir()
    f = open(path.join(test_dir, 'input.txt'), 'w')
    f.write('')
    f.close()
    assert parser_my_language(path.join(test_dir, 'input.txt'))


def test_parser1():
    test_dir = tempfile.gettempdir()
    f = open(path.join(test_dir, 'input.txt'), 'w')
    f.write('kw_connect kw_to string semi\n')
    f.close()
    assert parser_my_language(path.join(test_dir, 'input.txt'))


def test_parser2():
    test_dir = tempfile.gettempdir()
    f = open(path.join(test_dir, 'input.txt'), 'w')
    f.write('kw_connect kw_to string semi '
            'nt_name op_eq ident nt_name ident nt_name mid lbr rbr semi '
            'kw_select kw_count lbr ident rbr '
            'kw_from string '
            'kw_where lbr ident dot kw_id op_eq int rbr op_minus nt_name '
            'op_minus op_gr lbr ident rbr semi')
    f.close()
    assert parser_my_language(path.join(test_dir, 'input.txt'))


def test_parser3():
    test_dir = tempfile.gettempdir()
    f = open(path.join(test_dir, 'input.txt'), 'w')
    f.write('kw_list kw_all kw_graphs semi')
    f.close()
    assert parser_my_language(path.join(test_dir, 'input.txt'))
