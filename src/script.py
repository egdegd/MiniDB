from copy import deepcopy

from antlr4 import *
from antlr4.tree.Tree import TerminalNodeImpl
import os

from src.MyParser import MyErrorListener
from src.context_free_grammar import Grammar
from src.graph import Graph
from src.matrix_algorithms import evalCFPQ
from src.my_grammarLexer import my_grammarLexer
from src.my_grammarListener import my_grammarListener
from src.my_grammarParser import my_grammarParser


class MyGrammarListener(my_grammarListener):

    def __init__(self):
        self.grammar = Grammar()
        self.graph = Graph()
        self.path = ''
        self.select_ans = ''
        self.cur_vs = ''
        self.name_first_v = None
        self.id_first_v = -1
        self.name_second_v = None
        self.id_second_v = -1
        self.COUNT = False
        self.EXISTS = False
        self.rules = {}
        self.cur_main_nt = ''
        self.nt_from_alt_elem = []
        self.remember_nt_from_alt_elem = []
        self.remember_nt_from_seq_elem = []
        self.nt_from_seq_elem = []

    # Enter a parse tree produced by my_grammarParser#s.
    def enterS(self, ctx: my_grammarParser.SContext):
        pass

    # Exit a parse tree produced by my_grammarParser#s.
    def exitS(self, ctx: my_grammarParser.SContext):
        pass

    # Enter a parse tree produced by my_grammarParser#script.
    def enterScript(self, ctx: my_grammarParser.ScriptContext):
        pass

    # Exit a parse tree produced by my_grammarParser#script.
    def exitScript(self, ctx: my_grammarParser.ScriptContext):
        # print(self.grammar.CYK('a'))
        pass

    # Enter a parse tree produced by my_grammarParser#stmt.
    def enterStmt(self, ctx: my_grammarParser.StmtContext):
        self.select_ans = ''
        self.cur_vs = ''
        self.name_first_v = None
        self.id_first_v = -1
        self.name_second_v = None
        self.id_second_v = -1
        self.COUNT = False
        self.EXISTS = False
        self.rules = {}
        self.cur_main_nt = ''
        self.nt_from_alt_elem = []
        self.remember_nt_from_alt_elem = []
        self.remember_nt_from_seq_elem = []
        self.nt_from_seq_elem = []
        if type(ctx.children[0]) is TerminalNodeImpl and ctx.children[0].symbol.text == 'CONNECT':
            self.path = ctx.children[2].symbol.text[1:-1]
        if type(ctx.children[0]) is TerminalNodeImpl and ctx.children[0].symbol.text == 'LIST':
            files = os.listdir(self.path)
            print(sorted(files))

    # Exit a parse tree produced by my_grammarParser#stmt.
    def exitStmt(self, ctx: my_grammarParser.StmtContext):
        if type(ctx.children[0]) is TerminalNodeImpl and ctx.children[0].symbol.text == 'WRITE':
            file = open(ctx.children[3].symbol.text[1:-1], 'w')
            file.write(self.select_ans)

    # Enter a parse tree produced by my_grammarParser#named_pattern_stmt.
    def enterNamed_pattern_stmt(self, ctx: my_grammarParser.Named_pattern_stmtContext):
        pass

    # Exit a parse tree produced by my_grammarParser#named_pattern_stmt.
    def exitNamed_pattern_stmt(self, ctx: my_grammarParser.Named_pattern_stmtContext):
        for (nt, rule) in self.rules.items():
            for r in rule:
                self.grammar.add_rule(nt, r)
        self.grammar.add_rule(ctx.children[0].symbol.text, [self.cur_main_nt])
        self.rules = {}

    # Enter a parse tree produced by my_grammarParser#select_stmt.
    def enterSelect_stmt(self, ctx: my_grammarParser.Select_stmtContext):
        file_name = ctx.children[3].symbol.text[1:-1]
        self.graph.read_graph(self.path + '/' + file_name)

    # Exit a parse tree produced by my_grammarParser#select_stmt.
    def exitSelect_stmt(self, ctx: my_grammarParser.Select_stmtContext):
        new_grammar = Grammar()
        new_grammar.grammar = deepcopy(self.grammar.grammar)
        new_grammar.nonterminal_alphabet = deepcopy(self.grammar.nonterminal_alphabet)
        new_start = new_grammar.get_new_nonterminal()
        new_grammar.start = new_start
        for (nt, rule) in self.rules.items():
            for r in rule:
                new_grammar.add_rule(nt, r)
        new_grammar.add_rule(new_start, self.cur_main_nt)
        matrix = evalCFPQ(new_grammar, self.graph)[new_start].toarray()
        n = len(matrix)
        if self.EXISTS:
            if self.id_first_v == -1 and self.id_second_v == -1:
                self.select_ans = any([any(list(i)) for i in matrix])
            if self.id_first_v != -1 and self.id_second_v == -1:
                self.select_ans = any(list(matrix[self.id_first_v]))
            if self.id_first_v == -1 and self.id_second_v != -1:
                flag = False
                for line in matrix:
                    flag |= line[self.id_second_v]
                self.select_ans = flag
            if self.id_first_v != -1 and self.id_second_v != -1:
                self.select_ans = matrix[self.id_first_v][self.id_second_v]
        if self.COUNT:
            if self.id_first_v == -1 and self.id_second_v == -1:
                self.select_ans = sum([sum(list((list(i)))) for i in matrix])
            if self.id_first_v != -1 and self.id_second_v == -1:
                self.select_ans = sum(list(matrix[self.id_first_v]))
            if self.id_first_v == -1 and self.id_second_v != -1:
                self.select_ans = 0
                for line in matrix:
                    self.select_ans += int(line[self.id_second_v])
            if self.id_first_v != -1 and self.id_second_v != -1:
                self.select_ans = int(matrix[self.id_first_v][self.id_second_v])
        if not(self.EXISTS or self.COUNT):
            if self.id_first_v == -1 and self.id_second_v == -1:
                if len(self.cur_vs) == 2:
                    if self.cur_vs[0] == self.name_first_v and self.cur_vs[1] == self.name_second_v:
                        for i in range(n):
                            for j in range(n):
                                if matrix[i][j]:
                                    self.select_ans += ('(' + str(i) + ',' + str(j) + ')' + '\n')
                    else:
                        raise Exception('bad vertexes')
                else:
                    if self.cur_vs[0] == self.name_first_v:
                        for i in range(n):
                            if any(list(matrix[i])):
                                self.select_ans += (str(i) + '\n')
                    if self.cur_vs[0] == self.name_second_v:
                        for j in range(n):
                            flag = False
                            for i in range(n):
                                flag |= matrix[i][j]
                            if flag:
                                self.select_ans += (str(j) + '\n')
                    if self.cur_vs[0] != self.name_first_v and self.cur_vs[0] != self.name_second_v:
                        raise Exception('bad vertexes')
            if self.id_first_v != -1 and self.id_second_v == -1:
                if len(self.cur_vs) == 2:
                    if self.cur_vs[0] == self.name_first_v and self.cur_vs[1] == self.name_second_v:
                        for i in range(n):
                            if matrix[self.id_first_v][i]:
                                self.select_ans += ('(' + str(self.id_first_v) + ',' + str(i) + ')' + '\n')
                    else:
                        raise Exception('bad vertexes')
                else:
                    if self.cur_vs[0] == self.name_first_v:
                        if any(list(matrix[self.id_first_v])):
                            self.select_ans = str(self.id_first_v) + '\n'
                    if self.cur_vs[0] == self.name_second_v:
                        for i in range(n):
                            if matrix[self.id_first_v][i]:
                                self.select_ans += (str(i) + '\n')
                    if self.cur_vs[0] != self.name_first_v and self.cur_vs[0] != self.name_second_v:
                        raise Exception('bad vertexes')
            if self.id_first_v == -1 and self.id_second_v != -1:
                if len(self.cur_vs) == 2:
                    if self.cur_vs[0] == self.name_first_v and self.cur_vs[1] == self.name_second_v:
                        for i in range(n):
                            if matrix[i][self.id_second_v]:
                                self.select_ans += ('(' + str(i) + ',' + str(self.id_second_v) + ')' + '\n')
                    else:
                        raise Exception('bad vertexes')
                else:
                    if self.cur_vs[0] == self.name_first_v:
                        for i in range(n):
                            if matrix[i][self.id_second_v]:
                                self.select_ans += (str(i) + '\n')
                    if self.cur_vs[0] == self.name_second_v:
                        flag = False
                        for i in range(n):
                            flag |= matrix[i][self.id_second_v]
                        if flag:
                            self.select_ans = str(self.id_second_v) + '\n'
                    if self.cur_vs[0] != self.name_first_v and self.cur_vs[0] != self.name_second_v:
                        raise Exception('bad vertexes')
            if self.id_first_v != -1 and self.id_second_v != -1:
                if len(self.cur_vs) == 2:
                    if self.cur_vs[0] == self.name_first_v and self.cur_vs[1] == self.name_second_v:
                        if matrix[self.id_first_v][self.id_second_v]:
                            self.select_ans = '(' + str(self.id_first_v) + ',' + str(self.id_second_v) + ')' + '\n'
                    else:
                        raise Exception('bad vertexes')
                else:
                    if self.cur_vs[0] == self.name_first_v:
                        if matrix[self.id_first_v][self.id_second_v]:
                            self.select_ans = str(self.id_first_v) + '\n'
                    if self.cur_vs[0] == self.name_second_v:
                        if matrix[self.id_first_v][self.id_second_v]:
                            self.select_ans = str(self.id_second_v) + '\n'
                    if self.cur_vs[0] != self.name_first_v and self.cur_vs[0] != self.name_second_v:
                        raise Exception('bad vertexes')
            if len(self.select_ans) > 0:
                self.select_ans = self.select_ans[:-1]
        print(self.select_ans)
        self.graph = Graph()
        self.name_first_v = None
        self.id_first_v = -1
        self.name_second_v = None
        self.id_second_v = -1
        self.COUNT = False
        self.EXISTS = False

    # Enter a parse tree produced by my_grammarParser#obj_expr.
    def enterObj_expr(self, ctx: my_grammarParser.Obj_exprContext):
        pass

    # Exit a parse tree produced by my_grammarParser#obj_expr.
    def exitObj_expr(self, ctx: my_grammarParser.Obj_exprContext):
        if type(ctx.children[0]) is TerminalNodeImpl and ctx.children[0].symbol.text == 'EXISTS':
            self.EXISTS = True
        if type(ctx.children[0]) is TerminalNodeImpl and ctx.children[0].symbol.text == 'COUNT':
            self.COUNT = True

    # Enter a parse tree produced by my_grammarParser#vs_info.
    def enterVs_info(self, ctx: my_grammarParser.Vs_infoContext):
        if len(ctx.children) == 5:
            self.cur_vs = [str(ctx.children[1].symbol.text), str(ctx.children[3].symbol.text)]
        if len(ctx.children) == 3:
            self.cur_vs = [str(ctx.children[1])]

    # Exit a parse tree produced by my_grammarParser#vs_info.
    def exitVs_info(self, ctx: my_grammarParser.Vs_infoContext):
        pass

    # Enter a parse tree produced by my_grammarParser#where_expr.
    def enterWhere_expr(self, ctx: my_grammarParser.Where_exprContext):
        pass

    # Exit a parse tree produced by my_grammarParser#where_expr.
    def exitWhere_expr(self, ctx: my_grammarParser.Where_exprContext):
        pass

    # Enter a parse tree produced by my_grammarParser#v_expr.
    def enterV_expr(self, ctx: my_grammarParser.V_exprContext):
        if len(ctx.children) == 5:
            if self.name_first_v is None:
                self.name_first_v = ctx.children[0].symbol.text
                self.id_first_v = int(ctx.children[4].symbol.text)
            else:
                self.name_second_v = ctx.children[0].symbol.text
                self.id_second_v = int(ctx.children[4].symbol.text)
        else:
            if self.name_first_v is None:
                self.name_first_v = ctx.children[0].symbol.text
            else:
                self.name_second_v = ctx.children[0].symbol.text

    # Exit a parse tree produced by my_grammarParser#v_expr.
    def exitV_expr(self, ctx: my_grammarParser.V_exprContext):
        pass

    # Enter a parse tree produced by my_grammarParser#pattern.
    def enterPattern(self, ctx: my_grammarParser.PatternContext):
        if len(ctx.children) == 1:
            self.remember_nt_from_alt_elem.append(False)
        else:
            self.remember_nt_from_alt_elem.append(True)
        pass

    # Exit a parse tree produced by my_grammarParser#pattern.
    def exitPattern(self, ctx: my_grammarParser.PatternContext):
        if len(ctx.children) > 1:
            nt = self.grammar.get_new_nonterminal()
            self.rules[nt] = [[self.nt_from_alt_elem.pop()], [self.cur_main_nt]]
            self.cur_main_nt = nt

    # Enter a parse tree produced by my_grammarParser#alt_elem.
    def enterAlt_elem(self, ctx: my_grammarParser.Alt_elemContext):
        pass

    # Exit a parse tree produced by my_grammarParser#alt_elem.
    def exitAlt_elem(self, ctx: my_grammarParser.Alt_elemContext):
        if len(ctx.children) == 2:
            nt = self.grammar.get_new_nonterminal()
            self.rules[nt] = [['eps']]
            self.cur_main_nt = nt
        if self.remember_nt_from_alt_elem.pop():
            self.nt_from_alt_elem.append(self.cur_main_nt)

    # Enter a parse tree produced by my_grammarParser#seq.
    def enterSeq(self, ctx: my_grammarParser.SeqContext):
        if len(ctx.children) == 1:
            self.remember_nt_from_seq_elem.append(False)
        else:
            self.remember_nt_from_seq_elem.append(True)

    # Exit a parse tree produced by my_grammarParser#seq.
    def exitSeq(self, ctx: my_grammarParser.SeqContext):
        if len(ctx.children) > 1:
            nt = self.grammar.get_new_nonterminal()
            self.rules[nt] = [[self.nt_from_seq_elem.pop(), self.cur_main_nt]]
            self.cur_main_nt = nt

    # Enter a parse tree produced by my_grammarParser#seq_elem.
    def enterSeq_elem(self, ctx: my_grammarParser.Seq_elemContext):
        pass

    # Exit a parse tree produced by my_grammarParser#seq_elem.
    def exitSeq_elem(self, ctx: my_grammarParser.Seq_elemContext):
        if len(ctx.children) > 1:
            if ctx.children[1].symbol.text == '+':
                nt = self.grammar.get_new_nonterminal()
                self.rules[nt] = [[self.cur_main_nt], [self.cur_main_nt, nt]]
                self.cur_main_nt = nt
            if ctx.children[1].symbol.text == '*':
                nt = self.grammar.get_new_nonterminal()
                self.rules[nt] = [[self.cur_main_nt], [self.cur_main_nt, nt], ['eps']]
                self.cur_main_nt = nt
            if ctx.children[1].symbol.text == '?':
                nt = self.grammar.get_new_nonterminal()
                self.rules[nt] = [[self.cur_main_nt], ['eps']]
                self.cur_main_nt = nt
        if self.remember_nt_from_seq_elem.pop():
            self.nt_from_seq_elem.append(self.cur_main_nt)

    # Enter a parse tree produced by my_grammarParser#prim_pattern.
    def enterPrim_pattern(self, ctx: my_grammarParser.Prim_patternContext):
        if len(ctx.children) == 1:
            nt = self.grammar.get_new_nonterminal()
            self.rules[nt] = [[ctx.children[0].symbol.text]]
            self.cur_main_nt = nt

    # Exit a parse tree produced by my_grammarParser#prim_pattern.
    def exitPrim_pattern(self, ctx: my_grammarParser.Prim_patternContext):
        pass


def read_script_from_file(file_name):
    lexer = my_grammarLexer(FileStream(file_name))
    stream = CommonTokenStream(lexer)
    parser = my_grammarParser(stream)
    parser.addErrorListener(MyErrorListener)
    try:
        tree = parser.s()
        walker = ParseTreeWalker()
        collector = MyGrammarListener()
        walker.walk(collector, tree)
        return collector
    except Exception as e:
        print(e)
