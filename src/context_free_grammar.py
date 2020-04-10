import copy


class Grammar:
    def __init__(self):
        self.grammar = {}
        self.nonterminal_alphabet = []
        self.start = 'S'

    def add_rule(self, nt, rule):
        if nt not in self.nonterminal_alphabet:
            self.nonterminal_alphabet.append(nt)
        for symb in rule:
            if symb.isupper() and symb not in self.nonterminal_alphabet:
                self.nonterminal_alphabet.append(symb)
        if self.grammar.get(nt) is None:
            self.grammar[nt] = [rule]
        else:
            if rule not in self.grammar[nt]:
                self.grammar[nt] = self.grammar[nt] + [rule]

    def delete_rule(self, key, rule):
        self.grammar[key].remove(rule)

    def print_in_console_grammar(self):
        for (nt, rules) in self.grammar.items():
            for rule in rules:
                print(nt + " -> ", end='')
                for t in rule:
                    print(t, end='')
                print()

    def read_grammar(self, file_name):
        file = open(file_name, 'r')
        start_exist = False
        self.grammar = {}
        for line in file:
            if line[-1:] == '\n':
                line = line[:-1]
            if line == '':
                continue
            d = line.split(' ')
            d = list(filter(lambda a: a != '', d))
            self.add_rule(d[0], d[1:])
            if not start_exist:
                self.start = d[0]
                start_exist = True
        file.close()

    def write_grammar(self, file_name):
        file = open(file_name, 'w')
        if self.grammar == {}:
            file.close()
            return
        nt = self.start
        rules = self.grammar[nt]
        for rule in rules:
            file.write(nt + ' ')
            for symb in rule:
                file.write(symb + ' ')
            file.write('\n')
        for (nt, rules) in self.grammar.items():
            if nt == self.start:
                continue
            for rule in rules:
                file.write(nt + ' ')
                for symb in rule:
                    file.write(symb + ' ')
                file.write('\n')
        file.close()

    def get_new_nonterminal(self):
        i = 1
        alphabet = [chr(i) for i in range(ord('A'), ord('A') + 26)]
        for symb in alphabet:
            if symb not in self.nonterminal_alphabet:
                self.nonterminal_alphabet.append(symb)
                return symb
        while True:
            for symb in alphabet:
                if symb + str(i) not in self.nonterminal_alphabet:
                    self.nonterminal_alphabet.append(symb + str(i))
                    return symb + str(i)
            i += 1

    def delete_long_rules(self):
        g = copy.deepcopy(self.grammar)
        # g = self.grammar.copy()
        for (nt, rules) in g.items():
            for rule in rules:
                cur_nt = nt
                if len(rule) > 2:
                    for symb in rule[:-2]:
                        new_nt = self.get_new_nonterminal()
                        self.add_rule(cur_nt, [symb, new_nt])
                        cur_nt = new_nt
                    self.add_rule(cur_nt, rule[-2:])
                    self.delete_rule(nt, rule)

    def find_eps_generating_terminals(self):
        eps_generating_terminals = []
        for (nt, rules) in self.grammar.items():
            for rule in rules:
                if rule == ['eps']:
                    eps_generating_terminals.append(nt)
        flag = True
        while flag:
            flag = False
            for (nt, rules) in self.grammar.items():
                for rule in rules:
                    if all([i in eps_generating_terminals for i in rule]):
                        if nt not in eps_generating_terminals:
                            eps_generating_terminals.append(nt)
                            flag = True
        return eps_generating_terminals

    def delete_eps_rules(self):
        eps_generating_terminals = self.find_eps_generating_terminals()
        for (nt, rules) in self.grammar.items():
            for rule in rules:
                count_eps_term = sum(x in eps_generating_terminals for x in rule)
                if count_eps_term == 0:
                    continue
                l = generate_bin_seq(count_eps_term)
                list_of_rules = []
                for elem in l:
                    r = rule.copy()
                    count = 0
                    for symb in rule:
                        if symb in eps_generating_terminals:
                            if elem[count] == '0':
                                r.remove(symb)
                            count += 1
                    if r:
                        list_of_rules.append(r)
                self.delete_rule(nt, rule)
                for r in list_of_rules:
                    self.add_rule(nt, r)
        for (nt, rules) in self.grammar.items():
            for rule in rules:
                if rule == ['eps']:
                    self.delete_rule(nt, rule)
        if self.start in eps_generating_terminals:
            new_symb = self.get_new_nonterminal()
            g = copy.deepcopy(self.grammar)
            # g = self.grammar.copy()
            for (nt, rules) in g.items():
                if nt == self.start:
                    self.grammar[new_symb] = self.grammar.pop(self.start)
                new_rules = []
                for rule in rules:
                    new_rule = []
                    for symb in rule:
                        if symb == self.start:
                            new_rule.append(new_symb)
                        else:
                            new_rule.append(symb)
                    new_rules.append(new_rule)
                if nt == self.start:
                    self.grammar[new_symb] = new_rules
                    self.grammar[self.start] = [[new_symb]]
                else:
                    self.grammar[nt] = new_rules
            self.add_rule(self.start, ['eps'])

    def find_chan_pairs(self):
        chan_pairs = []
        nt = []
        for (nt_, _) in self.grammar.items():
            nt += nt_
            chan_pairs += [(nt_, nt_)]

        for (A, B) in chan_pairs:
            for rule in self.grammar[B]:
                if (len(rule) == 1) and (rule[0].isupper()):
                    if (A, rule[0]) not in chan_pairs:
                        chan_pairs.append((A, rule[0]))
        return chan_pairs

    def delete_chain_rules(self):
        chain_pairs = self.find_chan_pairs()
        new_grammar = {}
        for (A, B) in chain_pairs:
            for rule in self.grammar[B]:
                if (len(rule) > 1) or ((len(rule) == 1) and ((A, rule[0]) not in chain_pairs)):
                    if new_grammar.get(A) is None:
                        new_grammar[A] = [rule]
                    else:
                        if rule not in new_grammar[A]:
                            new_grammar[A] = new_grammar[A] + [rule]
        self.grammar = new_grammar

    def find_generating_terminals(self):
        generating_terminals = []
        for (nt, rules) in self.grammar.items():
            for rule in rules:
                if all([not i.isupper() for i in rule]):  # в првой части только терминалы
                    generating_terminals.append(nt)
        flag = True
        while flag:
            flag = False
            for (nt, rules) in self.grammar.items():
                for rule in rules:
                    if all([(i in generating_terminals) or (not i.isupper()) for i in rule]):
                        if nt not in generating_terminals:
                            generating_terminals.append(nt)
                            flag = True
        return generating_terminals

    def delete_nongenerating_terminals(self):
        generating_terminals = self.find_generating_terminals()
        g = copy.deepcopy(self.grammar)
        # g = self.grammar.copy()
        for (nt, rules) in g.items():
            if nt not in generating_terminals:
                self.grammar.pop(nt)
                continue
            for rule in rules:
                if any([(i not in generating_terminals) and (i.isupper()) for i in rule]):
                    self.delete_rule(nt, rule)

    def find_reachable_terminals(self):
        reachable_terminals = [self.start]
        flag = True
        while flag:
            flag = False
            for (nt, rules) in self.grammar.items():
                if nt in reachable_terminals:
                    for rule in rules:
                        for symb in rule:
                            if (symb not in reachable_terminals) and (symb.isupper()):
                                reachable_terminals.append(symb)
                                flag = True
        return reachable_terminals

    def delete_unreachable_terminals(self):
        reachable_terminals = self.find_reachable_terminals()
        g = copy.deepcopy(self.grammar)
        for (nt, rules) in g.items():
            if nt not in reachable_terminals:
                self.grammar.pop(nt)

    def delete_several_terminals(self):
        g = copy.deepcopy(self.grammar)
        nt_to_t = {}
        for (nt, rules) in g.items():
            count = 1
            for rule in rules:
                if len(rule) == 2:
                    if (not rule[0].isupper()) and (not rule[1].isupper()):
                        if nt_to_t.get(rule[0]) is not None:
                            new_nt1 = nt_to_t[rule[0]]
                        else:
                            new_nt1 = self.get_new_nonterminal()
                            count += 1
                            nt_to_t[rule[0]] = new_nt1
                            self.add_rule(new_nt1, rule[0])
                        if nt_to_t.get(rule[1]) is not None:
                            new_nt2 = nt_to_t[rule[1]]
                        else:
                            new_nt2 = self.get_new_nonterminal()
                            count += 1
                            nt_to_t[rule[1]] = new_nt2
                            self.add_rule(new_nt2, rule[1])
                        self.add_rule(nt, [new_nt1, new_nt2])
                        self.delete_rule(nt, rule)
                        continue
                    if not rule[0].isupper():
                        if nt_to_t.get(rule[0]) is not None:
                            new_nt = nt_to_t[rule[0]]
                        else:
                            new_nt = self.get_new_nonterminal()
                            count += 1
                            nt_to_t[rule[0]] = new_nt
                            self.add_rule(new_nt, [rule[0]])
                        self.add_rule(nt, [new_nt, rule[1]])
                        self.delete_rule(nt, rule)
                        continue
                    if not rule[1].isupper():
                        if nt_to_t.get(rule[1]) is not None:
                            new_nt = nt_to_t[rule[1]]
                        else:
                            new_nt = self.get_new_nonterminal()
                            count += 1
                            nt_to_t[rule[1]] = new_nt
                            self.add_rule(new_nt, [rule[1]])
                        self.add_rule(nt, [rule[0], new_nt])
                        self.delete_rule(nt, rule)
                        continue

    def to_CNF(self):
        self.delete_long_rules()
        self.delete_eps_rules()
        self.delete_chain_rules()
        self.delete_nongenerating_terminals()
        self.delete_unreachable_terminals()
        self.delete_several_terminals()

    def CYK(self, w):
        self.to_CNF()
        w = w.replace(' ', '')
        if w == '':
            if ['eps'] in self.grammar[self.start]:
                return True
            return False
        n = len(w)
        dict = {}
        for nt in self.nonterminal_alphabet:
            dict[nt] = False
        d = [[copy.deepcopy(dict) for j in range(n)] for i in range(n)]
        for i in range(n):
            for nt in self.nonterminal_alphabet:
                if self.grammar.get(nt) is None:
                    continue
                if [w[i]] in self.grammar.get(nt):
                    d[i][i][nt] = True

        for shift in range(1, n):
            for k in range(n):
                j = min(k + shift, n - 1)
                for nt in self.nonterminal_alphabet:
                    if self.grammar.get(nt) is None:
                        continue
                    for rule in self.grammar.get(nt):
                        if len(rule) == 2 and rule[0].isupper() and rule[1].isupper():
                            A = rule[0]
                            B = rule[1]
                            for l in range(k, j):
                                if d[k][l][A] and d[l + 1][j][B]:
                                    d[k][j][nt] = True

        return d[0][n - 1][self.start]

    def print_matrix(self, d, n):
        new_d = [[[] for j in range(n)] for i in range(n)]
        for i in range(n):
            for j in range(n):
                for nt in self.nonterminal_alphabet:
                    if d[i][j][nt]:
                        new_d[i][j].append(nt)
        for i in range(n):
            for j in range(n):
                print(new_d[i][j], end='                ')
            print()

    def to_weak_CNF(self):
        self.delete_long_rules()
        self.delete_chain_rules()
        self.delete_nongenerating_terminals()
        self.delete_unreachable_terminals()
        self.delete_several_terminals()

    def hellings_init(self, graph):
        res = []
        for (nt, rules) in self.grammar.items():
            if ['eps'] in rules:
                for v in graph.vertices:
                    res.append((nt, v, v))
        term = {}
        for (nt, rules) in self.grammar.items():
            for rule in rules:
                if len(rule) == 1 and not rule[0].isupper() and rule != ['eps']:
                    if term.get(rule[0]) is None:
                        term[rule[0]] = [nt]
                    else:
                        if nt not in term[rule[0]]:
                            term[rule[0]].append(nt)
        for (v, t, u) in graph.edges:
            if term.get(t) is None:
                continue
            for nt in term[t]:
                res.append((nt, v, u))
        return res

    def hellings(self, graph):
        self.to_weak_CNF()
        res = self.hellings_init(graph)
        m = copy.deepcopy(res)
        two_nt = {}
        for (nt, rules) in self.grammar.items():
            for rule in rules:
                if len(rule) == 2:
                    if two_nt.get((rule[0], rule[1])) is None:
                        two_nt[(rule[0], rule[1])] = [nt]
                    else:
                        two_nt[(rule[0], rule[1])].append(nt)
        while m:
            (Ni, v, u) = m.pop()
            for (Nj, v2, u2) in res:
                if u2 != v:
                    continue
                if two_nt.get((Nj, Ni)) is None:
                    continue
                for Nk in two_nt[(Nj, Ni)]:
                    if (Nk, v2, u) not in res:
                        m.append((Nk, v2, u))
                        res.append((Nk, v2, u))
            for (Nj, v2, u2) in res:
                if v2 != u:
                    continue
                if two_nt.get((Ni, Nj)) is None:
                    continue
                for Nk in two_nt[(Ni, Nj)]:
                    if (Nk, v, u2) not in res:
                        m.append((Nk, v, u2))
                        res.append((Nk, v, u2))
        return res

    def write_reachable_pairs(self, triples, output_file):
        file = open(output_file, 'a')
        for (nt, a, b) in triples:
            if nt == self.start:
                file.write(str(a) + ' ' + str(b) + '\n')


def generate_bin_seq(k):
    l = []
    for i in range(2 ** k):
        s = str(bin(i))[2:]
        s = '0' * (k - len(s)) + s
        l.append(s)
    return l
