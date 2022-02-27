from pyparsing import *

#class eitusParseActionHolder(object):
#    def __call__(self, seos, indeks, t):
#        print(seos, ";", indeks, ";", t[0],type(seos),type(indeks),type(t[0]))
        #return symbols(t[0][0]+"∈"+t[0][2])
#        return ~t[0][1]
# To use the operatorGrammar helper:
#   1.  Define the "atom" operand term of the grammar.
#       For this simple grammar, the smallest operand is either
#       and integer or a variable.  This will be the first argument
#       to the operatorGrammar method.
#   2.  Define a list of tuples for each level of operator
#       precendence.  Each tuple is of the form
#       (opExpr, numTerms, rightLeftAssoc, parseAction), where
#       - opExpr is the pyparsing expression for the operator;
#          may also be a string, which will be converted to a Literal
#       - numTerms is the number of terms for this operator (must
#          be 1 or 2)
#       - rightLeftAssoc is the indicator whether the operator is
#          right or left associative, using the pyparsing-defined
#          constants opAssoc.RIGHT and opAssoc.LEFT.
#       - parseAction is the parse action to be associated with
#          expressions matching this operator expression (the
#          parse action tuple member may be omitted)
#   3.  Call operatorGrammar passing the operand expression and
#       the operator precedence list, and save the returned value
#       as the generated pyparsing expression.  You can then use
#       this expression to parse input strings, or incorporate it
#       into a larger, more complex grammar.
#
Seose_parssija = operatorPrecedence(Word(alphanums), [(Word("∀"+alphanums), 1, opAssoc.RIGHT),#todo:panna siia rohkem booleanide vahelisi tehteid.
                                                      (Word("∃"+alphanums),1,opAssoc.RIGHT),
                                                      #todo:võiks saada ka hulki tähistada lugedes loogsulgude vahel üles hulga elemendid nt: {A,C,D}
                                                      #todo:võiks saada ka kulki tähistada pannes loogsulgude sisse hulka kuulumis-tingimuse nt.: {x:x∈A∧x∈B}
                                                      (Literal("∈"), 2, opAssoc.RIGHT),
                                                      (Literal('¬'), 1, opAssoc.RIGHT),
                                                      (Literal('∧'), 2, opAssoc.RIGHT),
                                                      (Literal("∨"), 2, opAssoc.RIGHT),
                                                      (Literal("→"), 2, opAssoc.RIGHT),
                                                      (Literal("←"), 2, opAssoc.RIGHT),
                                                      (Literal("↮"), 2, opAssoc.RIGHT),
                                                      (Literal("↔"), 2, opAssoc.RIGHT)])
ParserElement.enablePackrat()