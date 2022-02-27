from pyparsing import *

integer = Word(nums)
variable = Word(alphas, alphanums)
boolLiteral = oneOf("true false")

operand = boolLiteral | variable | integer

comparison_op = oneOf("== <= >= != < >")
QM,COLON = map(Literal,"?:")
expr = infixNotation(operand,
    [
    (comparison_op, 2, opAssoc.LEFT),
    ((QM,COLON), 3, opAssoc.LEFT),
    ])

print (expr.parseString("(x==1? true: (y == 10? 100 : 200) )"))