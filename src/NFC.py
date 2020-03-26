class Grammar:
    grammar = {}
    nonterminal_alphabet = [chr(i) for i in range(ord('A'), ord('A') + 26)]  # it can be increased if necessary

    def __init__(self):
        self.grammar = {}
        self.nonterminal_alphabet = [chr(i) for i in range(ord('A'), ord('A') + 26)]

    def add_rule(self, nt, l):
        if nt in self.nonterminal_alphabet:
            self.nonterminal_alphabet.remove(nt)
        for elem in l:
            if elem in self.nonterminal_alphabet:
                self.nonterminal_alphabet.remove(elem)
        if self.grammar.get(nt) is None:
            self.grammar[nt] = [l]
        else:
            if l not in self.grammar[nt]:
                self.grammar[nt] = self.grammar[nt] + [l]

    def delete_rule(self, key, rule):
        self.grammar[key].remove(rule)

    def print_grammar(self):
        for (nt, rules) in self.grammar.items():
            for rule in rules:
                print(nt + " -> ", end='')
                for t in rule:
                    print(t, end='')
                print()

    def read_grammar(self, file_name):
        file = open(file_name, 'r')
        for line in file:
            if line[-1:] == '\n':
                line = line[:-1]
            if line == '':
                continue
            d = line.split(' ')
            d = list(filter(lambda a: a != '', d))
            self.add_rule(d[0], d[1:])

    def write_grammar(self, file_name):
        file = open(file_name, 'w')
        for (nt, rules) in self.grammar.items():
            for rule in rules:
                file.write(nt + ' ')
                for symb in rule:
                    file.write(symb + ' ')
                file.write('\n')

    def delete_long_rules(self):
        g = self.grammar.copy()
        for (nt, rules) in g.items():
            for rule in rules:
                cur_nt = nt
                if len(rule) > 2:
                    for symb in rule[:-2]:
                        new_nt = self.nonterminal_alphabet[0]
                        self.nonterminal_alphabet.remove(new_nt)
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
        if 'S' in eps_generating_terminals:  # 'S' is starting nontermenal
            self.add_rule('S', ['eps'])

    def find_chan_pairs(self):
        chan_pairs = []
        nt = []
        for (nt_, _) in self.grammar.items():
            nt += nt_
            chan_pairs += [(nt_, nt_)]

        for (A, B) in chan_pairs:
            for rule in self.grammar[B]:
                if (len(rule) == 1) and (rule[0] in nt):
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
        g = self.grammar.copy()
        for (nt, rules) in g.items():
            if nt not in generating_terminals:
                self.grammar.pop(nt)
                continue
            for rule in rules:
                if any([(i not in generating_terminals) and (i.isupper()) for i in rule]):
                    rules.remove(rule)

    def find_achievable_terminals(self):
        achievable_terminals = ['S']
        flag = True
        while flag:
            flag = False
            for (nt, rules) in self.grammar.items():
                if nt in achievable_terminals:
                    for rule in rules:
                        for symb in rule:
                            if (symb not in achievable_terminals) and (symb.isupper()):
                                achievable_terminals.append(symb)
                                flag = True
        return achievable_terminals

    def delete_not_achievable_terminals(self):
        achievable_terminals = self.find_achievable_terminals()
        g = self.grammar.copy()
        for (nt, rules) in g.items():
            if nt not in achievable_terminals:
                self.grammar.pop(nt)

    def delete_several_terminals(self):
        g = self.grammar.copy()
        nt_to_t = {}
        for (nt, rules) in g.items():
            for rule in rules:
                if len(rule) == 2:
                    if (not rule[0].isupper()) and (not rule[1].isupper()):
                        if nt_to_t.get(rule[0]) is not None:
                            new_nt1 = nt_to_t[rule[0]]
                        else:
                            new_nt1 = self.nonterminal_alphabet[0]
                            self.nonterminal_alphabet.remove(new_nt1)
                            nt_to_t[rule[0]] = new_nt1
                            self.add_rule(new_nt1, rule[0])
                        if nt_to_t.get(rule[1]) is not None:
                            new_nt2 = nt_to_t[rule[1]]
                        else:
                            new_nt2 = self.nonterminal_alphabet[0]
                            self.nonterminal_alphabet.remove(new_nt2)
                            nt_to_t[rule[1]] = new_nt2
                            self.add_rule(new_nt2, rule[1])
                        self.add_rule(nt, [new_nt1, new_nt2])
                        self.delete_rule(nt, rule)
                        continue
                    if not rule[0].isupper():
                        if nt_to_t.get(rule[0]) is not None:
                            new_nt = nt_to_t[rule[0]]
                        else:
                            new_nt = self.nonterminal_alphabet[0]
                            self.nonterminal_alphabet.remove(new_nt)
                            nt_to_t[rule[0]] = new_nt
                            self.add_rule(new_nt, [rule[0]])
                        self.add_rule(nt, [new_nt, rule[1]])
                        self.delete_rule(nt, rule)
                        continue
                    if not rule[1].isupper():
                        if nt_to_t.get(rule[1]) is not None:
                            new_nt = nt_to_t[rule[1]]
                        else:
                            new_nt = self.nonterminal_alphabet[0]
                            self.nonterminal_alphabet.remove(new_nt)
                            nt_to_t[rule[1]] = new_nt
                            self.add_rule(new_nt, [rule[1]])
                        self.add_rule(nt, [rule[0], new_nt])
                        self.delete_rule(nt, rule)
                        continue

    def to_NFC(self):
        self.delete_long_rules()
        self.delete_eps_rules()
        self.delete_chain_rules()
        self.delete_nongenerating_terminals()
        self.delete_not_achievable_terminals()
        self.delete_several_terminals()


def generate_bin_seq(k):
    l = []
    for i in range(2 ** k):
        s = str(bin(i))[2:]
        s = '0' * (k - len(s)) + s
        l.append(s)
    return l


def main():
    file_in = input()
    file_out = input()
    g = Grammar()
    g.read_grammar(file_in)
    g.to_NFC()
    g.write_grammar(file_out)


if __name__ == "__main__":
    main()
