import networkx
from networkx.drawing.nx_pydot import write_dot
from pyformlang import *
from pyformlang.finite_automaton import DeterministicFiniteAutomaton
from rdflib import *

from src.DFA import *


class Client:
    running = True
    graph = Graph()
    dfa = DeterministicFiniteAutomaton()
    inter_dfa = DeterministicFiniteAutomaton()

    def __init__(self):
        self.commands = {
            "load": self.load,
            "labels": self.labels,
            "request": self.request,
            "exit": self.exit
        }

    def run(self):
        while self.running:
            cmd = input().split(" ", 1)
            if len(cmd) == 2:
                self.commands[cmd[0]](cmd[1])
            else:
                self.commands[cmd[0]]()

    def load(self, path):
        self.graph.parse(path)

        nfa = NondeterministicFiniteAutomaton()
        for subj, pred, obj in self.graph:
            state0 = finite_automaton.State(subj)
            state1 = finite_automaton.State(obj)
            symbol = finite_automaton.Symbol(pred)
            nfa.add_transition(state0, symbol, state1)
            nfa.add_final_state(state0)
            nfa.add_final_state(state1)
            nfa.add_start_state(state0)
            nfa.add_start_state(state1)
        self.dfa = nfa.to_deterministic()

    def labels(self):
        for subj, pred, obj in self.graph:
            print(pred, '\n')

    def request(self, reg):
        new_dfa = string_to_min_dfa(reg)
        self.inter_dfa = self.dfa.get_intersection(new_dfa)
        g = networkx.nx.DiGraph()
        for frm, edges in self.inter_dfa.to_dict().items():
            for edge, to in edges.items():
                g.add_edge(str(frm), str(to), label=str(edge))
        print(f"nodes: {len(g.nodes)}\nedges: {len(g.edges)}")
        write_dot(g, "graph.dot")

    def exit(self):
        self.running = False


def main():
    client = Client()
    client.run()


if __name__ == "__main__":
    main()
