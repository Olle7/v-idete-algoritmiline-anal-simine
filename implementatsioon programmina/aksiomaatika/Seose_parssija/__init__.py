from pyparsing import *

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
                                                      (Literal('∧'), 2, opAssoc.RIGHT),#kuna kommutatiivne, siis saaks argumndid set'i panna
                                                      (Literal("∨"), 2, opAssoc.RIGHT),#kuna kommutatiivne, siis saaks argumndid set'i panna
                                                      (Literal("→"), 2, opAssoc.RIGHT),
                                                      (Literal("←"), 2, opAssoc.RIGHT),
                                                      (Literal("↮"), 2, opAssoc.RIGHT),
                                                      (Literal("↔"), 2, opAssoc.RIGHT)])

class eitusParseActionHolder(object):
    def __call__(self, seos, indeks, t):
        t=t[0].asList()
        return ((t[0],t[1]))
class tavalineParseActionHolder(object):
    def __call__(self, seos, indeks, t):
        t=t[0].asList()
        return ((t[1],t[0],t[2]))
class assotsiatiivneParseActionHolder(object):
    def __call__(self, seos, indeks, t):
        t=t[0].asList()
        #print(12,t[0])
        operandid=[]
        for i in range(0,len(t),2):
            operandid.append(t[i])
        return ((t[1],operandid))
class kvantoriParseActionHolder(object):
    def __call__(self, seos, indeks, t):
        t=t[0].asList()
        return ((t[0][0],t[0][1:],t[1]))
class kommentaariParseActionHolder(object):
    def __call__(self, seos, indeks, t):
        pass
Seose_parssija2 = operatorPrecedence(Word(alphanums), [(Word("∀"+alphanums), 1, opAssoc.RIGHT,kvantoriParseActionHolder()),#todo:panna siia rohkem booleanide vahelisi tehteid.
                                                      (Word("∃"+alphanums),1,opAssoc.RIGHT,kvantoriParseActionHolder()),
                                                      #todo:võiks saada ka hulki tähistada lugedes loogsulgude vahel üles hulga elemendid nt: {A,C,D}
                                                      #todo:võiks saada ka kulki tähistada pannes loogsulgude sisse hulka kuulumis-tingimuse nt.: {x:x∈A∧x∈B}
                                                      #todo teha võimalus sisendi sisse ka kommentaare, mida parssimises ignoreeritakse panna.

                                                      #(Literal("⎶"), 2, opAssoc.RIGHT, tavalineParseActionHolder()),#todo: lisada ka "ühendus" operaator, element(2,2)'e põhisenotatsiooni jaoks.#hulgad ei tohi olla millegagi "ühenduses" ja elemedid ei tohi kuhugi kuuluda, ega midagi sisaldada.
                                                      #lisada võimalus kasutada ka teisi elemente, mille võimalike kuuluvuste arv ja, et kui mitme elemendi kaudu kuuluvus määratakse, valib kasutaja ise.
                                                      #optimiseerimisvalikute sisestamiseks teha eraldi sisend. näiteks: Literal("\[")+Word(alphanums)+Literal("]")
                                                      (Literal("∈"), 2, opAssoc.RIGHT,tavalineParseActionHolder()),
                                                      (Literal('¬'), 1, opAssoc.RIGHT,eitusParseActionHolder()),
                                                      (Literal('∧'), 2, opAssoc.LEFT,assotsiatiivneParseActionHolder()),
                                                      (Literal("∨"), 2, opAssoc.LEFT,assotsiatiivneParseActionHolder()),
                                                      (Literal("→"), 2, opAssoc.RIGHT,tavalineParseActionHolder()),
                                                      (Literal("←"), 2, opAssoc.RIGHT,tavalineParseActionHolder()),
                                                      (Literal("↮"), 2, opAssoc.RIGHT,tavalineParseActionHolder()),
                                                      (Literal("↔"), 2, opAssoc.RIGHT,tavalineParseActionHolder())])

ParserElement.enablePackrat()
if __name__=="__main__":
    #print(Seose_parssija.parseString("C∈A∧∀x(x∈D∧∀y(y∈x))∨(¬A∈A∧A∈B∧A∈C∧C∈C↔¬(B∈B∧B∈C))∨∀x1(x1∈A∧B∈B)")[0])
    print(Seose_parssija2.parseString("C∈A∧∀x(x∈D∧∀y(y∈x))∨(¬A∈A∧A∈B∧A∈C∧C∈C↔¬(B∈B∧B∈C))∨∀x1(x1∈A∧B∈B)")[0])
    #print(Seose_parssija2.parseString("A∈A∧B∈A∧C∈A∧D∈A∧E∈A∧F∈A∧G∈A∨B∈A∧B∈B")[0])