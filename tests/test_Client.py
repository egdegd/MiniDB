from src.Client import *


def test_load1():
    client = Client()
    client.load("http://www.w3.org/2000/10/swap/test/meet/blue.rdf")
    assert (len(client.graph) == 4)


def test_load2():
    client = Client()
    client.load("http://www.w3.org/2000/10/swap/test/meet/blue.rdf")
    client.graph.serialize(format='nt')
    assert (sorted(client.graph)[0][0] == (URIRef(u'http://meetings.example.com/cal#m1')))


def test_exit():
    client = Client()
    client.exit()


test_load1()
test_load2()
test_exit()
