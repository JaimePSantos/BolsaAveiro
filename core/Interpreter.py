import sys
import string
from itertools import groupby

from core.Nodes import LowerNumberNode, UpperNumberNode, IntervalVarNode, SeparatorNode, BinOpNode, PropOpNode, \
    ProgOpNode, \
    UnaryOpNode, DifferentialVarNode, ProgDifNode, UnaryForallOpNode, BoxPropNode, DiamondPropNode, NumberNode, \
    TestProgNode, ParenthesisNode, ZeroAryNode, CurlyParenthesisNode
from core.Tokens import TT_INT, TT_EOF, TT_LOWERLIM, TT_UPPERLIM, TT_SEPARATOR, TT_INTERVALPLUS, \
    TT_INTERVALMINUS, TT_INTERVALMULT, TT_INTERVALDIV, TT_GEQ, TT_SEQ, TT_GT, TT_ST, TT_NOT, TT_FORALL, TT_LPAREN, \
    TT_RPAREN, \
    TT_PROGTEST, TT_PROGAND, TT_PROGUNION, TT_PROGSEQUENCE, TT_PROGASSIGN, \
    TT_PROGDIFASSIGN, TT_IN, TT_KEYWORD, TT_IDENTIFIER, TT_IDENTIFIERDIF, TT_LBOX, TT_RBOX, \
    TT_IMPLIES, TT_LDIAMOND, TT_RDIAMOND, TT_COMMA, TT_NDREP, TT_LCURLYBRACK, TT_RCURLYBRACK

from core.Errors import RTError

DIGITS = '0123456789'
LETTERS = string.ascii_letters + "'"
LETTERS_DIGITS = LETTERS + DIGITS

#######################################
# Interpreter - Under Construction
#######################################

class Interpreter:
    'Class that evalutates the input.'

    def __init__(self):
        self.lowerNumberList = NumberList()
        self.upperNumberList = NumberList()
        self.resultInterval = Interval()
        self.intervalList = [Interval()]
        self.intervalList.pop(0)
        self.intervalNumberList = [NumberList()]
        self.translation = ''

    def getTranslation(self):
        return self.translation

    def visit(self, node):
        'Template of the function to visit each method.'
        method_name = f'visit_{type(node).__name__}'
        method = getattr(self, method_name, self.no_visit_method)
        return method(node)

    def no_visit_method(self, node):
        'If no acceptable method found, throw an exception.'
        raise Exception(f'No visit_{type(node).__name__} defined.')

    def visit_LowerNumberNode(self, node):
        'Visits the nodes that have lower limit values and constructs a list that keeps track of these values.'
        # print("Found LowerNumberNode")
        num = Number(
            node.tok.value).set_pos(
            node.pos_start,
            node.pos_end)
        self.lowerNumberList.appendNum(num)
        return num

    def visit_UpperNumberNode(self, node):
        'Visits the nodes that have upper limit values and constructs a list that keeps track of these values.'
        # print("Found UpperNumberNode")
        num = Number(
            node.tok.value).set_pos(
            node.pos_start,
            node.pos_end)
        self.upperNumberList.appendNum(num)
        return num

    def visit_BinOpNode(self, node):
        '''
        Visits nodes that have binary operations on them. \
        If the token is + then we simply add all lower limit numbers and upper limit numbers separately. \
        If the token is * then we join lower limit numbers and upper limit numbers so we can perform interval multiplication on them.
        :param node:
        :return:
        '''
        res = RTResult()
        # left = res.register(self.visit(node.left_node))
        left = self.visit(node.left_node)
        # if res.error: return res
        # right = res.register(self.visit(node.right_node))
        right = self.visit(node.right_node)
        # print(f"Left node: {type(left)}")
        # print(f"Right node: {type(right)}")
        # if res.error: return res
        error = False
        if node.op_tok.type in TT_INTERVALPLUS:
            if (type(left) is Interval) and (type(right) is Interval):
                # print(1)
                result,error = left.addIntervals(right)
                self.translation = str(result)
            else:
                self.translation = str(left) + ' + ' + str(right)
                result = self.translation
        if node.op_tok.type in TT_INTERVALMINUS:
            if (type(left) is Interval) and (type(right) is Interval):
                # print(type(left))
                result,error = left.subIntervals(right)
                self.translation = str(result)
            else:
                self.translation = str(left) + ' + ' + str(right)
                result = self.translation
        if node.op_tok.type in TT_INTERVALMULT:
            if (type(left) is Interval) and (type(right) is Interval):
                result,error = left.multIntervals(right)
                self.translation = str(result)
            else:
                self.translation = str(left) + ' * ' + str(right)
                result = self.translation
        if node.op_tok.type in TT_INTERVALDIV:
            if (type(left) is Interval) and (type(right) is Interval):
                result,error = left.divIntervals(right)
                self.translation = str(result)
            else:
                self.translation = str(left) + ' / ' + str(right)
                result = self.translation

        if error:
            # return res.failure(error)
            return error
        else:
            # return res.success(result.set_pos())
            return result

    def visit_SeparatorNode(self, node):
        '''
        Visits the nodes with the SEPARATOR token.
        :param node:
        :return:
        '''
        # print("Found SeperatorNode")
        lower = self.visit(node.left_node)
        upper = self.visit(node.right_node)
        interval = Interval(lower, upper).set_pos()
        self.intervalList.append(interval)
        # print("idDL2DL List1 " + str(self.intervalList))
        self.translation = str(interval)
        return interval

    def visit_ParenthesisNode(self, node):
        translation = ''
        self.intervalList = []
        for parenNodeElement in node.element_nodes:
            visitparenNodeElement = self.visit(parenNodeElement)
        if node.zeroAryNode:
            for zAryNodeElement in node.zeroAryNode:
                visitZAryNodeElement = self.visit(zAryNodeElement)
            if visitZAryNodeElement.type in TT_NDREP:
                translatedZAryElement = '**'
                translation = '( ' + str(visitparenNodeElement) + ' )' + str(translatedZAryElement)
        else:
            translation = '( ' + str(visitparenNodeElement) + ' )'
        self.translation = translation
        return translation

    def visit_IntervalVarNode(self, node):
        return node.tok.value

    def visit_PropOpNode(self, node):
        leftNode = node.left_node
        rightNode = node.right_node
        visitLeftNode = self.visit(leftNode)
        visitRightNode = self.visit(rightNode)
        translatedOpTok = ''
        translation = ''
        if node.op_tok.type in [TT_ST, TT_GT, TT_GEQ, TT_SEQ]:
            if node.op_tok.type in TT_ST:
                translatedOpTok = '<'
            elif node.op_tok.type in TT_GT:
                translatedOpTok = '>'
            elif node.op_tok.type in TT_GEQ:
                translatedOpTok = '>='
            elif node.op_tok.type in TT_SEQ:
                translatedOpTok = '<='
        elif node.op_tok.matches(TT_KEYWORD, 'AND'):
            translatedOpTok = ' AND '
        elif node.op_tok.matches(TT_KEYWORD, 'IN'):
            translatedOpTok = '  '
        elif node.op_tok.matches(TT_KEYWORD, 'OR'):
            translatedOpTok = ' OR '
        elif node.op_tok.type in (TT_IMPLIES):
            translatedOpTok = ' -> '
        if translatedOpTok != '':
            translation = str(visitLeftNode) + " " + translatedOpTok + " " + str(visitRightNode)
        else:
            translation = str(visitLeftNode) + " " + str(node.op_tok) + " " + str(visitRightNode)
        self.translation = translation
        return translation

    def visit_ProgOpNode(self, node):
        leftNode = node.left_node
        rightNode = node.right_node
        visitLeftNode = self.visit(leftNode)
        visitRightNode = self.visit(rightNode)
        translatedOpTok = ''
        if node.op_tok.type in TT_PROGASSIGN:
            translatedOpTok = ':='
        elif node.op_tok.type in TT_COMMA:
            translatedOpTok = ','
        elif node.op_tok.type in TT_PROGSEQUENCE:
            translatedOpTok = ';'
        elif node.op_tok.type in TT_PROGAND:
            translatedOpTok = '&'
        elif node.op_tok.type in TT_PROGUNION:
            translatedOpTok = ' || '
        if translatedOpTok != '' and translatedOpTok != ':=' and translatedOpTok != ';':
            translation = str(visitLeftNode) + " " + translatedOpTok + " " + str(visitRightNode)
        elif translatedOpTok == ':=':
            translation = str(visitLeftNode) + " " + translatedOpTok + " " + str(visitRightNode)
        elif translatedOpTok == ';':
            firstTranslation = str(visitLeftNode) + " " + translatedOpTok + " " + str(visitRightNode)
            # print(type(node))
            translation = self.removeRepeated(firstTranslation, ';')
            # translation = firstTranslation
        else:
            translation = str(visitLeftNode) + " " + str(node.op_tok) + " " + str(visitRightNode)
        self.translation = translation
        return translation

    def visit_BoxPropNode(self, node):
        for boxNodeElement, boxPropElement in zip(node.element_nodes, node.boxProp):
            visitboxNodeElement = self.visit(boxNodeElement)
            visitboxPropElement = self.visit(boxPropElement)
        translation = '[{' + str(visitboxNodeElement) + '}] ' + str(visitboxPropElement)
        self.translation = translation
        return translation

    def visit_DiamondPropNode(self, node):
        for diamondNodeElement, diamondPropElement in zip(node.element_nodes, node.diamondProp):
            visitDiamondNodeElement = self.visit(diamondNodeElement)
            visitDiamondPropElement = self.visit(diamondPropElement)
        translation = '<{' + str(visitDiamondNodeElement) + '}> ' + str(visitDiamondPropElement)
        self.translation = translation
        return translation

    def visit_TestProgNode(self, node):
        for progTestNodeElement in node.element_nodes:
            visitprogTestNodeElement = self.visit(progTestNodeElement)
        translation = '?(' + str(visitprogTestNodeElement) + ")"
        self.translation = translation
        return translation

    def visit_CurlyParenthesisNode(self, node):
        translation = ''
        for parenNodeElement in node.element_nodes:
            visitparenNodeElement = self.visit(parenNodeElement)
        if node.zeroAryNode:
            for zAryNodeElement in node.zeroAryNode:
                visitZAryNodeElement = self.visit(zAryNodeElement)
            if visitZAryNodeElement.type in TT_NDREP:
                translatedZAryElement = '**'
                translation = '{ ' + str(visitparenNodeElement) + ' }' + str(translatedZAryElement)
        else:
            translation = '{' + str(visitparenNodeElement) + '}'
        self.translation = translation
        return translation

    def visit_ProgDifNode(self, node):
        leftNode = node.left_node
        rightNode = node.right_node
        visitLeftNode = self.visit(leftNode)
        visitRightNode = self.visit(rightNode)
        translatedOpTok = ''
        translation = ''
        if node.op_tok.type in TT_PROGDIFASSIGN:
            translatedOpTok = '='
        if translatedOpTok != '':
            translation = str(visitLeftNode) + " " + translatedOpTok + " " + str(visitRightNode)
        else:
            translation = str(visitLeftNode) + " " + str(node.op_tok) + " " + str(visitRightNode)
        self.translation = translation
        return translation

    def visit_DifferentialVarNode(self, node):
        return node.tok.value

    def visit_NumberNode(self, node):
        return node.tok.value

    def visit_UnaryForallOpNode(self, node):
        visitNode = self.visit(node.node)
        translation = '$ ' + str(visitNode) + ' IN'
        self.translation = translation
        return translation

    def visit_ZeroAryNode(self, node):
        # print("Tok %s"%node.tok)
        return node.tok

    def visit_UnaryOpNode(self, node):
        visitNode = self.visit(node.node)
        translation = ''
        if node.op_tok.type in TT_NOT:
            translation = '!' + "(" + str(visitNode) + ")"
            self.translation = translation
        if node.op_tok.type in TT_INTERVALPLUS:
            translation = '+' + "(" + str(visitNode) + ")"
        if node.op_tok.type in TT_INTERVALMINUS:
            translation = '-' + str(visitNode)
        return translation

    def visit_UnaryProgOpNode(self, node):
        visitNode = self.visit(node.node)
        if node.op_tok.type in TT_PROGTEST:
            translation = '?' + "( " + str(visitNode) + " )"
            self.translation = translation
        return translation

    def removeRepeated(self, translation, symbol):
        charList = translation.split()
        for i in range(len(charList)):
            if ';' in charList[i]:
                if len(charList[i])>1:
                    charList[i] = charList[i].replace(';',"")
        processedString = ' '.join(charList)
        return processedString

    def reset(self):
        '''
        Clears the lists of numbers so each input has a clean slate.
        :return:
        '''
        self.lowerNumberNodeList = []
        self.upperNumberNodeList = []


#######################################
# VALUES
#######################################

class Number:
    '''
    This class helps us perform integer operations on the elements belonging to the NumberList class.
    '''

    def __init__(self, value):
        self.value = value
        self.set_pos()
        # self.set_context()

    def set_pos(self, pos_start=None, pos_end=None):
        '''
        For keeping track of number position.
        :param pos_start:
        :param pos_end:
        :return:
        '''
        self.pos_start = pos_start
        self.pos_end = pos_end
        return self

    # def set_context(self, context=None):
    #     self.context = context
    #     return self

    def __add__(self, other):
        if isinstance(other, Number):
            return Number(self.value + other.value)

    def __sub__(self, other):
        if isinstance(other, Number):
            return Number(self.value - other.value)

    def __truediv__(self,other):
            return Number(self.value/other.value)

    def __mul__(self, other):
        if isinstance(other, Number):
            return Number(self.value * other.value)

    def __lt__(self, other):
        if isinstance(other, Number):
            return self.value < other.value

    def __gt__(self, other):
        if isinstance(other, Number):
            return self.value > other.value

    def __le__(self, other):
        if isinstance(other, Number):
            return self.value <= other.value

    def __ge__(self, other):
        if isinstance(other, Number):
            return self.value >= other.value

    def __eq__(self, other):
        if isinstance(other, Number):
            return self.value == other.value

    def __repr__(self):
        return str(self.value)

class Interval:
    '''
    This class helps us represent the interval that resulted from an operation and keep track of errors.
    '''

    def __init__(self, lowerNum=None, upperNum=None):
        if lowerNum and upperNum is not None:
            self.lowerNum = lowerNum
            self.upperNum = upperNum
            self.set_pos()
        else:
            self.lowerNum = None
            self.upperNum = None

    def set_pos(self):
        '''
        So we know the position of our intervals.
        :return:
        '''
        self.pos_start = self.lowerNum.pos_start
        self.pos_end = self.upperNum.pos_end
        return self

    def addIntervals(self,other):
        return Interval(self.lowerNum+other.lowerNum, self.upperNum+other.upperNum), None

    def subIntervals(self,other):
        return Interval(self.lowerNum-other.upperNum, self.upperNum-other.lowerNum), None

    def multIntervals(self,other):
        resultList = [self.lowerNum*other.lowerNum,self.lowerNum*other.upperNum,self.upperNum*other.lowerNum,self.upperNum*other.upperNum]
        return Interval(min(resultList),max(resultList)), None

    def divIntervals(self,other):
        if (other.lowerNum or other.upperNum) == 0:
            return None, RTError(other.pos_start, other.pos_end, 'Division by zero', '')
        else:
            resultList = [self.lowerNum/other.lowerNum,self.lowerNum/other.upperNum,self.upperNum/other.lowerNum,self.upperNum/other.upperNum]
            return Interval(min(resultList),max(resultList)), None


    def __repr__(self):
        return '[' + str(self.lowerNum) + ',' + str(self.upperNum) + ']'

class NumberList:
    '''
    This class helps us keep track of the numbers present in each node so we can perform interval operations on them.
    '''

    def __init__(self, numberList=None):
        self.numberList = []
        if numberList is not None:
            self.numberList = numberList

    def appendNum(self, apNumber):
        '''
        Used to construct the appropriate list of numbers present in each node.
        :param apNumber:
        :return:
        '''
        return self.numberList.append(apNumber)

    def addIntervals(self):
        '''
        Takes the list with either the lower limits or upper limits of the interval and sums the terms.
        :return:
        '''
        resultNumber = Number(0)
        for num in self.numberList:
            resultNumber += num
        return resultNumber

    def multIntervals(self, intervalList):
        '''
        Generates the set of numbers resulted from interval multiplication.
        :return:
        '''
        # TODO: Perceber o caso mais geral da multiplicaçao e fazer as alteraçoes de acordo.
        # intervalList = NumberList(self.numberList).separatedIntervals()
        resultList = [intervalList[0][0] * intervalList[1][0], intervalList[0][0] * intervalList[1][1],
                      intervalList[0][1] * intervalList[1][0], intervalList[0][1] * intervalList[1][1]]

        return NumberList(resultList)

    def negInterval(self):
        # TODO: Definir -[a,b].
        pass

    def invInterval(self):
        # TODO: Definir [a,b]^-1.
        pass

    def separatedIntervals(self):
        '''
        Takes the list with the lower limits and upper limits of the intervals and separates them into the original intervals.
        :return:
        '''
        separatedIntervals = [[]]
        # print("Number List: "+str(self.numberList))
        for i in range(0, len(self.numberList)):
            if i >= len(self.numberList) - 2:
                break
            interval = [self.numberList[i], self.numberList[i + 2]]
            separatedIntervals.append(interval)
        separatedIntervals.pop(0)
        # print("Separated Intervals: "+str(separatedIntervals))
        return separatedIntervals

    def min(self):
        '''
        Minimum of a list so we can get the lower limit that resulted from the multiplication of intervals.
        :return:
        '''
        minNumber = Number(sys.maxsize)
        for num in self.numberList:
            if minNumber >= num:
                minNumber = num
        return minNumber

    def max(self):
        '''
        Maximum of a list so we can get the upper limit that resulted from the multiplication of intervals.
        :return:
        '''
        maxNumber = Number(-sys.maxsize)
        for num in self.numberList:
            if maxNumber <= num:
                maxNumber = num
        return maxNumber

    def extend(self, otherNumberList):
        '''
        Helper function so we can combine the upper limit list with the lower limit list.
        :param otherNumberList:
        :return:
        '''
        return NumberList(self.numberList + (otherNumberList.numberList))

    def __repr__(self):
        return str(self.numberList)

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
