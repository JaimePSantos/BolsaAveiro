from Tokens import TT_INT, TT_FLOAT, TT_EOF, TT_LOWERLIM, TT_UPPERLIM, TT_SEPARATOR, TT_INTERVALPLUS, \
    TT_INTERVALMINUS, TT_INTERVALMULT, TT_INTERVALDIV
#######################################
# Interpreter
#######################################

class Interpreter:
    def __init__(self):
        self.lowerNumberList = NumberList()
        self.upperNumberList = NumberList()

    def visit(self, node):
        method_name = f'visit_{type(node).__name__}'
        method = getattr(self, method_name, self.no_visit_method)
        return method(node)

    def no_visit_method(self, node):
        raise Exception(f'No visit_{type(node).__name__} defined.')

    def visit_LowerNumberNode(self, node):
        # print("Found LowerNumberNode")
        num = Number(node.tok.value).set_pos(node.pos_start,node.pos_end)
        self.lowerNumberList.appendNum(num)

    def visit_UpperNumberNode(self, node):
        # print("Found UpperNumberNode")
        num = Number(node.tok.value).set_pos(node.pos_start,node.pos_end)
        self.upperNumberList.appendNum(num)

    def visit_BinOpNode(self, node):
        # print("Found BinOpNode")
        if node.op_tok.type in TT_INTERVALPLUS:
            self.visit(node.left_node)
            self.visit(node.right_node)
            resultLower = self.lowerNumberList.addedInterval()
            resultUpper = self.upperNumberList.addedInterval()
            return Interval(resultLower,resultUpper).set_pos()

    def visit_SeparatorNode(self, node):
        # print("Found SeperatorNode")
        self.visit(node.left_node)
        self.visit(node.right_node)

    def reset(self):
        self.lowerNumberNodeList = []
        self.upperNumberNodeList = []

#######################################
# VALUES
#######################################

class Number:
    def __init__(self, value):
        self.value = value
        self.set_pos()
        # self.set_context()

    def set_pos(self, pos_start=None, pos_end=None):
        self.pos_start = pos_start
        self.pos_end = pos_end
        return self

    # def set_context(self, context=None):
    #     self.context = context
    #     return self

    def __add__(self,other):
        if isinstance(other, Number):
            return Number(self.value + other.value)

    def __repr__(self):
        return str(self.value)


class NumberList:
    def __init__(self):
        self.numberList = []

    def appendNum(self, apNumber):
        return self.numberList.append(apNumber)

    def addedInterval(self):
        resultNumber = Number(0)
        for num in self.numberList:
            resultNumber += num
        return resultNumber

    def __repr__(self):
        return str(self.numberList)


class Interval:
    def __init__(self,lowerNum,upperNum):
        self.lowerNum = lowerNum
        self.upperNum = upperNum
        self.set_pos()

    def set_pos(self):
        self.pos_start = self.lowerNum.pos_start
        self.pos_end = self.upperNum.pos_end
        return self

    def __repr__(self):
        return '[' + str(self.lowerNum) + ',' + str(self.upperNum) + ']'

#######################################
# CONTEXT
#######################################

# class Context:
#     def __init__(self, display_name, parent=None, parent_entry_pos=None):
#         self.display_name = display_name
#         self.parent = parent
#         self.parent_entry_pos = parent_entry_pos

#######################################
# RUNTIME RESULT
#######################################

class RTResult:
    def __init__(self):
        self.value = None
        self.error = None

    def register(self, res):
        if res.error: self.error = res.error
        return res.value

    def success(self, value):
        self.value = value
        return self

    def failure(self, error):
        self.error = error
        return self

