import tempfile
from os import path
from src.graph import *


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
