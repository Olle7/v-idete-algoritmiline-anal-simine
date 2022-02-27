from pyparsing import *
class AParseActionHolder(object):
    def __call__(self, string, index, t):
        #f(info_from_outer_parse_results,t[0])
        pass
expr = operatorPrecedence( Word(nums),[
         (Literal('A'), 1, opAssoc.RIGHT,AParseActionHolder()),
         (Literal('B'), 2, opAssoc.LEFT),
         (Literal('C'), 2, opAssoc.LEFT)])
print(type(expr.parseString("3B1C2BA1")[0]))
print(expr.parseString("3B1C2BA1")[0])#[['3','B','1'],'C',['2','B',"nested in B and C"]]
print(expr.parseString("A1B3")[0])#["nested in B", 'B', '3']
print(expr.parseString("A(1B3)")[0])#["not nested", ['1', 'B', '3']]

"""
How can I access info from outer parsing result in which the argument of parseaction is nested? Can I do it with parseaction? If not is there some other Pyparsing tool for it or I should define recursive function that takes pyparsing.ParseResults as argument?
"""

"""
No, there is no way to access the outer results - in your case, because they haven't even been parsed yet at the time the inner results are being parsed!
You will probably have to write a recursive function that works on the fully parsed tree that you get back from parseString. As you walk the tree, keep track of your path, and when you find an "A" element, replace it with the path.
It may be difficult to work with the returned ParseResults directly, so you may want to get the tree by calling asList() on the returned results:
tree = expr.parseString("whatever").asList()
"""