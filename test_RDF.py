from rdflib import URIRef, Graph, BNode, RDF, RDFS


def test_graph():
    g = Graph()
    g.parse("http://www.w3.org/2000/10/swap/test/meet/blue.rdf")
    assert (len(g) == 4)


def test_sort():
    g = Graph()
    g.parse("http://www.w3.org/2000/10/swap/test/meet/blue.rdf")
    g.serialize(format='nt')
    assert (sorted(g)[0][0] == (URIRef(u'http://meetings.example.com/cal#m1')))


def test_add():
    g = Graph()
    a = BNode('foo')
    b = BNode('bar')
    c = BNode('baz')
    g.add((a, RDF.first, RDF.type))
    g.add((a, RDF.rest, b))
    g.add((b, RDF.first, RDFS.label))
    g.add((b, RDF.rest, c))
    g.add((c, RDF.first, RDFS.comment))
    g.add((c, RDF.rest, RDF.nil))
    assert (len(g) == 6)
