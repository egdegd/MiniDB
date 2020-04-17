from pyformlang.finite_automaton import EpsilonNFA
from pyformlang.regular_expression import Regex
from scipy import sparse
from src.context_free_grammar import *
from src.graph import *
import numpy


def evalCFPQ_init(grammar, graph):
    n = len(graph.vertices)
    matrix = {}
    term = {}
    for (nt, rules) in grammar.grammar.items():
        for rule in rules:
            if len(rule) == 1 and not rule[0].isupper() and rule != ['eps']:
                if term.get(rule[0]) is None:
                    term[rule[0]] = [nt]
                else:
                    if nt not in term[rule[0]]:
                        term[rule[0]].append(nt)

    ntrow = {}
    ntcol = {}
    ntdata = {}
    for (a, t, b) in graph.edges:
        if term.get(t) is None:
            continue
        for nt in term[t]:
            if ntrow.get(nt) is None:
                ntrow[nt] = []
                ntcol[nt] = []
                ntdata[nt] = []
            ntrow[nt] += [a]
            ntcol[nt] += [b]
            ntdata[nt] += [True]
    for (nt, rules) in grammar.grammar.items():
        for rule in rules:
            if rule == ['eps']:
                if ntrow.get(nt) is None:
                    ntrow[nt] = []
                    ntcol[nt] = []
                    ntdata[nt] = []
                for i in range(n):
                    ntrow[nt] += [i]
                    ntcol[nt] += [i]
                    ntdata[nt] += [True]
    for nt in grammar.nonterminal_alphabet:
        if ntdata.get(nt) is None:
            matrix[nt] = csr_matrix((n, n), dtype=bool)
            continue
        matrix[nt] = csr_matrix((ntdata[nt], (ntrow[nt], ntcol[nt])), shape=(n, n))
    return matrix


def evalCFPQ(grammar, graph):
    grammar.to_weak_CNF()
    matrix = evalCFPQ_init(grammar, graph)
    good_rules = {}
    for (nt, _) in grammar.grammar.items():
        good_rules[nt] = []
    for (nt, rules) in grammar.grammar.items():
        for rule in rules:
            if len(rule) == 2:
                good_rules[nt].append(rule)
    is_changing = True
    while is_changing:
        is_changing = False
        for (nt, rules) in good_rules.items():
            for rule in rules:
                new_matrix = matrix[nt] + (matrix[rule[0]] * matrix[rule[1]])
                if (new_matrix != matrix[nt]).nnz > 0:
                    is_changing = True
                    matrix[nt] = new_matrix
    return matrix


def write_reachable_pairs_from_matrix(start, matrix, output_file):
    m = matrix[start].toarray()
    file = open(output_file, 'a')
    for i in range(len(m)):
        for j in range(len(m)):
            if m[i][j]:
                file.write(str(i) + ' ' + str(j) + '\n')


def matrix_by_grammar(grammar_file):
    grammar_start = 0
    file = open(grammar_file, 'r')
    start = {}
    final = {}
    nfa_dict = {}
    nt_start = True

    for line in file:
        if line[-1:] == '\n':
            line = line[:-1]
        regex = Regex(line[2:])
        nt = line[:1]
        nfa: EpsilonNFA = regex.to_epsilon_nfa().minimize()
        start[nt] = nfa.start_states
        final[nt] = nfa.final_states
        dict = nfa.to_dict()
        l = list(dict.keys())
        l = list(map(lambda x: str(x), l))
        keys = sorted(l)
        new_dict = {}
        for k in keys:
            a = sorted(list(map(lambda x: str(x), list(dict[k].keys()))))
            nnew_dict = {}
            for el in a:
                nnew_dict[el] = dict[k][el]
            new_dict[k] = nnew_dict.copy()
        nfa_dict[nt] = new_dict.copy()
        if nt_start:
            grammar_start = nt
            nt_start = False
    edges = {}
    count = 0
    number = 0
    rename = {}
    for (nt, atm) in nfa_dict.items():
        for (fr, dct) in atm.items():
            for (label, to) in dct.items():
                if edges.get(label) is None:
                    edges[label] = []
                fr1 = '1' * count + str(fr)
                to1 = '1' * count + str(to)
                if rename.get(to1) is None:
                    rename[to1] = number
                    number += 1
                if rename.get(fr1) is None:
                    rename[fr1] = number
                    number += 1
                edges[label] += [(rename[fr1], rename[to1])]
        count += 1
    count = 0
    for (nt, starts) in start.items():
        new_starts = []
        for v in starts:
            new_starts.append(rename['1' * count + str(v)])
        start[nt] = new_starts
        count += 1
    count = 0
    for (nt, finals) in final.items():
        new_finals = []
        for v in finals:
            new_finals.append(rename['1' * count + str(v)])
        final[nt] = new_finals
        count += 1
    matrix = {}
    for (label, lst) in edges.items():
        row = []
        col = []
        data = []
        for (a, b) in lst:
            row.append(a)
            col.append(b)
            data.append(True)
        matrix[label] = csr_matrix((data, (row, col)), shape=(number, number))
    return matrix, start, final, number, grammar_start


def contextFreePathQueryingTP(grammar_file, graph: Graph):
    grammar_matrix, start, final, n_grammar, grammar_start = matrix_by_grammar(grammar_file)
    n_graph = len(graph.vertices)
    row = {}
    col = {}
    data = {}
    graph_matrix = {}
    term_graph = []
    for (a, t, b) in graph.edges:
        if row.get(t) is None:
            row[t] = []
            col[t] = []
            data[t] = []
        row[t] += [a]
        col[t] += [b]
        data[t] += [True]
        if t not in term_graph:
            term_graph.append(t)
    for t in term_graph:
        graph_matrix[t] = csr_matrix((data[t], (row[t], col[t])), shape=(n_graph, n_graph))

    terms = list(set(grammar_matrix.keys()).union(set(graph_matrix.keys())))
    for term in terms:
        if graph_matrix.get(term) is None:
            graph_matrix[term] = csr_matrix((n_graph, n_graph), dtype=bool)
        if grammar_matrix.get(term) is None:
            grammar_matrix[term] = csr_matrix((n_grammar, n_grammar), dtype=bool)

    is_changing = True
    matrix = csr_matrix((n_grammar * n_graph, n_grammar * n_graph), dtype=bool)
    while is_changing:
        is_changing = False
        for term in terms:
            m = sparse.kron(graph_matrix[term], grammar_matrix[term]).astype(bool)
            matrix = matrix + m
        matrix = transitive_closure(matrix)
        for (a, b) in zip(*matrix.nonzero()):
            for nt in grammar_matrix.keys():
                if start.get(nt) is None:
                    continue
                new_matrix = graph_matrix[nt] + csr_matrix(
                    (numpy.array([True]), (numpy.array([a % n_graph]), numpy.array([b % n_graph]))),
                    shape=(n_graph, n_graph), dtype=bool)
                if (new_matrix != graph_matrix[nt]).nnz > 0:
                    graph_matrix[nt] = new_matrix
                    is_changing = True
    return graph_matrix, grammar_start


def transitive_closure(matrix):
    new_matrix = matrix + matrix * matrix
    while (new_matrix != matrix).nnz > 0:
        matrix = new_matrix
        new_matrix = matrix + matrix * matrix
    return new_matrix
