class ErrorListener(object):

    def syntaxError(self, recognizer, offendingSymbol, line, column, msg, e):
        pass

    def reportAmbiguity(self, recognizer, dfa, startIndex, stopIndex, exact, ambigAlts):
        pass

    def reportAttemptingFullContext(self, recognizer, dfa, startIndex, stopIndex, conflictingAlts):
        pass

    def reportContextSensitivity(self, recognizer, dfa, startIndex, stopIndex, prediction):
        pass


class MyErrorListener(ErrorListener):
    def syntaxError(self, recognizer, offendingSymbol, line, column, msg, e):
        print("line " + str(line) + ":" + str(column) + " " + msg)
        raise ParseException


class ParseException(Exception):
    pass
