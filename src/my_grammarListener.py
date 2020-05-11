# Generated from my_grammar.g4 by ANTLR 4.7.2
from antlr4 import *
if __name__ is not None and "." in __name__:
    from .my_grammarParser import my_grammarParser
else:
    from my_grammarParser import my_grammarParser

# This class defines a complete listener for a parse tree produced by my_grammarParser.
class my_grammarListener(ParseTreeListener):

    # Enter a parse tree produced by my_grammarParser#s.
    def enterS(self, ctx:my_grammarParser.SContext):
        pass

    # Exit a parse tree produced by my_grammarParser#s.
    def exitS(self, ctx:my_grammarParser.SContext):
        pass


    # Enter a parse tree produced by my_grammarParser#script.
    def enterScript(self, ctx:my_grammarParser.ScriptContext):
        pass

    # Exit a parse tree produced by my_grammarParser#script.
    def exitScript(self, ctx:my_grammarParser.ScriptContext):
        pass


    # Enter a parse tree produced by my_grammarParser#stmt.
    def enterStmt(self, ctx:my_grammarParser.StmtContext):
        pass

    # Exit a parse tree produced by my_grammarParser#stmt.
    def exitStmt(self, ctx:my_grammarParser.StmtContext):
        pass


    # Enter a parse tree produced by my_grammarParser#named_pattern_stmt.
    def enterNamed_pattern_stmt(self, ctx:my_grammarParser.Named_pattern_stmtContext):
        pass

    # Exit a parse tree produced by my_grammarParser#named_pattern_stmt.
    def exitNamed_pattern_stmt(self, ctx:my_grammarParser.Named_pattern_stmtContext):
        pass


    # Enter a parse tree produced by my_grammarParser#select_stmt.
    def enterSelect_stmt(self, ctx:my_grammarParser.Select_stmtContext):
        pass

    # Exit a parse tree produced by my_grammarParser#select_stmt.
    def exitSelect_stmt(self, ctx:my_grammarParser.Select_stmtContext):
        pass


    # Enter a parse tree produced by my_grammarParser#obj_expr.
    def enterObj_expr(self, ctx:my_grammarParser.Obj_exprContext):
        pass

    # Exit a parse tree produced by my_grammarParser#obj_expr.
    def exitObj_expr(self, ctx:my_grammarParser.Obj_exprContext):
        pass


    # Enter a parse tree produced by my_grammarParser#vs_info.
    def enterVs_info(self, ctx:my_grammarParser.Vs_infoContext):
        pass

    # Exit a parse tree produced by my_grammarParser#vs_info.
    def exitVs_info(self, ctx:my_grammarParser.Vs_infoContext):
        pass


    # Enter a parse tree produced by my_grammarParser#where_expr.
    def enterWhere_expr(self, ctx:my_grammarParser.Where_exprContext):
        pass

    # Exit a parse tree produced by my_grammarParser#where_expr.
    def exitWhere_expr(self, ctx:my_grammarParser.Where_exprContext):
        pass


    # Enter a parse tree produced by my_grammarParser#v_expr.
    def enterV_expr(self, ctx:my_grammarParser.V_exprContext):
        pass

    # Exit a parse tree produced by my_grammarParser#v_expr.
    def exitV_expr(self, ctx:my_grammarParser.V_exprContext):
        pass


    # Enter a parse tree produced by my_grammarParser#pattern.
    def enterPattern(self, ctx:my_grammarParser.PatternContext):
        pass

    # Exit a parse tree produced by my_grammarParser#pattern.
    def exitPattern(self, ctx:my_grammarParser.PatternContext):
        pass


    # Enter a parse tree produced by my_grammarParser#alt_elem.
    def enterAlt_elem(self, ctx:my_grammarParser.Alt_elemContext):
        pass

    # Exit a parse tree produced by my_grammarParser#alt_elem.
    def exitAlt_elem(self, ctx:my_grammarParser.Alt_elemContext):
        pass


    # Enter a parse tree produced by my_grammarParser#seq.
    def enterSeq(self, ctx:my_grammarParser.SeqContext):
        pass

    # Exit a parse tree produced by my_grammarParser#seq.
    def exitSeq(self, ctx:my_grammarParser.SeqContext):
        pass


    # Enter a parse tree produced by my_grammarParser#seq_elem.
    def enterSeq_elem(self, ctx:my_grammarParser.Seq_elemContext):
        pass

    # Exit a parse tree produced by my_grammarParser#seq_elem.
    def exitSeq_elem(self, ctx:my_grammarParser.Seq_elemContext):
        pass


    # Enter a parse tree produced by my_grammarParser#prim_pattern.
    def enterPrim_pattern(self, ctx:my_grammarParser.Prim_patternContext):
        pass

    # Exit a parse tree produced by my_grammarParser#prim_pattern.
    def exitPrim_pattern(self, ctx:my_grammarParser.Prim_patternContext):
        pass


