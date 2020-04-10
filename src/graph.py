class Graph:
    def __init__(self):
        self.vertices = []
        self.edges = []
        self.terminals = []

    def read_graph(self, file_name):
        file = open(file_name, 'r')
        for line in file:
            if line[-1:] == '\n':
                line = line[:-1]
            if line == '':
                continue
            d = line.split(' ')
            d = list(filter(lambda a: a != '', d))
            if int(d[0]) not in self.vertices:
                self.vertices.append(int(d[0]))
            if int(d[2]) not in self.vertices:
                self.vertices.append(int(d[2]))
            if (int(d[0]), d[1], int(d[2])) not in self.edges:
                self.edges.append((int(d[0]), d[1], int(d[2])))
            if d[1] not in self.terminals:
                self.terminals.append(d[1])
        file.close()
