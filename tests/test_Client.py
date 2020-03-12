from src.Client import *


def test_load1():
    client = Client()
    client.load("http://www.w3.org/2000/10/swap/test/meet/blue.rdf")
    assert len(client.graph) == 4


def test_load2():
    client = Client()
    client.load("http://www.w3.org/2000/10/swap/test/meet/blue.rdf")
    client.graph.serialize(format='nt')
    assert sorted(client.graph)[0][0] == (URIRef(u'http://meetings.example.com/cal#m1'))


def test_exit():
    client = Client()
    client.exit()


def test_labels1(capsys):
    client = Client()
    client.load("http://www.w3.org/2000/10/swap/test/meet/blue.rdf")
    client.labels()
    captured = capsys.readouterr()
    assert "http://www.example.org/personal_details#GivenName" in captured.out
    assert "http://www.example.org/personal_details#hasEmail" in captured.out
    assert "http://www.example.org/meeting_organization#attending" in captured.out
    assert "http://www.example.org/meeting_organization#homePage" in captured.out
    assert len(captured.out) == 214


def test_labels2(capsys):
    client = Client()
    client.load("http://www.w3.org/People/Berners-Lee/card")
    client.labels()
    captured = capsys.readouterr()
    assert "http://xmlns.com/foaf/0.1/name" in captured.out
    assert "http://xmlns.com/foaf/0.1/givenname" in captured.out
    assert "http://creativecommons.org/ns#license" in captured.out
    assert "http://www.w3.org/2006/vcard/ns#postal-code" in captured.out
    assert "http://rdfs.org/sioc/ns#avatar " in captured.out
    assert "http://www.w3.org/ns/solid/terms#publicTypeIndex" in captured.out
    assert "http://www.w3.org/2000/10/swap/pim/contact#assistant" in captured.out


def test_request1(capsys):
    client = Client()
    client.load("http://www.w3.org/People/Berners-Lee/card")
    client.request("aaba")
    captured = capsys.readouterr()
    assert "nodes: 0" in captured.out
    assert "edges: 0" in captured.out
    assert len(captured.out) == 18


def test_request2(capsys):
    client = Client()
    client.dfa = string_to_min_dfa("(ab|a)*")
    client.request("ab")
    captured = capsys.readouterr()
    assert "nodes: 2" in captured.out
    assert "edges: 1" in captured.out
    assert len(captured.out) == 18


def test_request3(capsys):
    client = Client()
    client.dfa = string_to_min_dfa("(a |a b c)*")
    client.request("(a* | (a | b)*) c")
    captured = capsys.readouterr()
    symb_a = finite_automaton.Symbol("a")
    symb_b = finite_automaton.Symbol("b")
    symb_c = finite_automaton.Symbol("c")
    assert "nodes: 6" in captured.out
    assert "edges: 4" in captured.out
    assert (client.inter_dfa.accepts([symb_a, symb_b, symb_c]))
    assert (client.inter_dfa.accepts([symb_a, symb_a, symb_b, symb_c]))
    assert (not client.inter_dfa.accepts([symb_a, symb_b, symb_c, symb_a, symb_b, symb_c]))
