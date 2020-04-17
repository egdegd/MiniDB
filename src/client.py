from src.context_free_grammar import *
from src.graph import *
from src.matrix_algorithms import *


class Client:
    running = True
    g = Grammar()

    def __init__(self):
        self.commands = {
            "cnf": self.cnf,
            "cyk": self.cyk,
            "hellings": self.hellings,
            "evalCFPQ": self.evalCFPQ,
            "contextFreePathQueryingTP": self.contextFreePathQueryingTP,
            "exit": self.exit
        }

    def run(self):
        while self.running:
            cmd = input().split(" ")
            if len(cmd) == 1:
                self.commands[cmd[0]]()
            if len(cmd) == 2:
                self.commands[cmd[0]](cmd[1])
            if len(cmd) == 3:
                self.commands[cmd[0]](cmd[1], cmd[2])
            if len(cmd) == 4:
                self.commands[cmd[0]](cmd[1], cmd[2], cmd[3])

    def cnf(self, file_in, file_out):
        self.g.read_grammar(file_in)
        self.g.to_CNF()
        self.g.write_grammar(file_out)

    def cyk(self, grammar_file, string_file):
        self.g.read_grammar(grammar_file)
        f = open(string_file, 'r')
        s = f.read()
        print(self.g.CYK(s))

    def hellings(self, grammar_file, graph_file, output_file):
        graph = Graph()
        self.g.read_grammar(grammar_file)
        graph.read_graph(graph_file)
        reachable_pairs = self.g.hellings(graph)
        self.g.write_grammar(output_file)
        self.g.write_reachable_pairs(reachable_pairs, output_file)

    def evalCFPQ(self, grammar_file, graph_file, output_file):
        graph = Graph()
        self.g.read_grammar(grammar_file)
        graph.read_graph(graph_file)
        matrix = evalCFPQ(self.g, graph)
        self.g.write_grammar(output_file)
        write_reachable_pairs_from_matrix(self.g.start, matrix, output_file)

    def contextFreePathQueryingTP(self, grammar_file, graph_file, output_file):
        graph = Graph()
        graph.read_graph(graph_file)
        graph_matrix, start = contextFreePathQueryingTP(grammar_file, graph)
        write_reachable_pairs_from_matrix(start, graph_matrix, output_file)

    def exit(self):
        self.running = False


def main():
    client = Client()
    client.run()


if __name__ == "__main__":
    main()
