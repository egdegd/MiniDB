import rdflib
from rdflib import URIRef

g = rdflib.Graph()
g.parse("http://www.w3.org/2000/10/swap/test/meet/blue.rdf")


def test1():
    assert (len(g) == 4)


g.serialize(format='nt')


def test_sort():
    assert (sorted(g)[0][0] == (URIRef(u'http://meetings.example.com/cal#m1')))
