from tokenize import String
from pyformlang.finite_automaton import finite_automaton, NondeterministicFiniteAutomaton
from pyformlang.regular_expression import Regex


def regex_to_min_dfa(regex: Regex):
    enfa = regex.to_epsilon_nfa()
    dfa = enfa.to_deterministic().minimize()
    return dfa


def string_to_min_dfa(s: String):
    regex = Regex(s)
    return regex_to_min_dfa(regex)
