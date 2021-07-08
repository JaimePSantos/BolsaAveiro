import sys
from Tokens import TT_INT, TT_FLOAT, TT_EOF, TT_LOWERLIM, TT_UPPERLIM, TT_SEPARATOR, TT_INTERVALPLUS,\
    TT_INTERVALMINUS, TT_INTERVALMULT, TT_INTERVALDIV,TT_GEQ,TT_SEQ,TT_GT,TT_ST,TT_NOT,TT_AND,TT_FORALL,TT_BOX,\
    TT_LPAREN, TT_RPAREN,TT_INTERVALVAR,TT_PROGTEST, TT_PROGAND,TT_PROGUNION,TT_PROGSEQUENCE,TT_PROGASSIGN,\
    TT_DIFFERENTIALVAR,TT_PROGDIFASSIGN,TT_IN,TT_KEYWORD,TT_IDENTIFIER,TT_IDENTIFIERDIF,TT_LBOX,TT_RBOX,TT_IMPLIES
from Errors import InvalidSyntaxError
from Nodes import LowerNumberNode,UpperNumberNode,IntervalVarNode,SeparatorNode,BinOpNode,PropOpNode,ProgOpNode,\
    UnaryOpNode,DifferentialVarNode,UnaryProgOpNode,ProgDifNode,UnaryForallOpNode,BoxNode,BoxPropNode
import string
DIGITS = '0123456789'
LETTERS = string.ascii_letters + "'"
LETTERS_DIGITS = LETTERS + DIGITS

class Translator:
    'Class that evalutates the input.'
    def __init__(self):
        self.varList = []
        self.intervalDict = {}
        self.varDict = {}
        self.translation = ""

    def buildTranslation(self):
        intervals = ''
        i = 0
        builtTranslation = ''
        for interval in self.intervalDict.values():
            i+=1
            intervals += "(" + str(interval) + ")"
            if i == len(self.intervalDict):
                break
            else:
                intervals += " ∧ "
        if intervals!='':
            builtTranslation = intervals + " -> " + '( ' + self.translation + ' )'
        else:
            builtTranslation = self.translation
        return builtTranslation

    def visit(self, node):
        'Template of the function to visit each method.'
        method_name = f'visit_{type(node).__name__}'
        method = getattr(self, method_name, self.no_visit_method)
        return method(node)

    def no_visit_method(self, node):
        'If no acceptable method found, throw an exception.'
        raise Exception(f'No visit_{type(node).__name__} defined.')

    def visit_BinOpNode(self, node):
        '''
        Visits nodes that have binary operations on them. \
        If the token is + then we simply add all lower limit numbers and upper limit numbers separately. \
        If the token is * then we join lower limit numbers and upper limit numbers so we can perform interval multiplication on them.
        :param node:
        :return:
        '''
        translation = ''
        if node.op_tok.type in TT_INTERVALPLUS:
            leftSum = self.visit(node.left_node)
            rightSum = self.visit(node.right_node)
            translation = str(leftSum)+ ' + ' + str(rightSum)
            self.translation = translation
            return translation
        if node.op_tok.type in TT_INTERVALMINUS:
            leftSub = self.visit(node.left_node)
            rightSub = self.visit(node.right_node)
            translation = str(leftSub)+ ' - ' + str(rightSub)
            self.translation = translation
            return translation
        if node.op_tok.type in TT_INTERVALMULT:
            leftMult = self.visit(node.left_node)
            rightMult = self.visit(node.right_node)
            translation = '(' + str(leftMult) + ' * ' + str(rightMult) + ')'
            self.translation = translation
            return translation
        if node.op_tok.type in TT_INTERVALDIV:
            leftDiv = self.visit(node.left_node)
            rightDiv = self.visit(node.right_node)
            translation = '(' + str(leftDiv) + ' / ' + str(rightDiv) + ')'
            self.translation = translation
            return translation

    def visit_UnaryOpNode(self,node):
        visitNode = self.visit(node.node)
        translation = ''
        if node.op_tok.type in TT_NOT:
            translation = '!' + "(" + str(visitNode) + ")"
            self.translation=translation
        if node.op_tok.type in TT_INTERVALPLUS:
            translation = '+' + "(" + str(visitNode) + ")"
        if node.op_tok.type in TT_INTERVALMINUS:
            translation = '-' + "(" + str(visitNode) + ")"
        return translation

    def visit_UnaryProgOpNode(self,node):
        visitNode = self.visit(node.node)
        if node.op_tok.type in TT_PROGTEST:
            translation = '?' + "( " + str(visitNode) + " )"
            self.translation=translation
        return translation

    def visit_LowerNumberNode(self, node):
        'Visits the nodes that have lower limit values and constructs a list that keeps track of these values.'
        num = Number(node.tok.value).set_pos(node.pos_start,node.pos_end)
        return num

    def visit_UpperNumberNode(self, node):
        'Visits the nodes that have upper limit values and constructs a list that keeps track of these values.'
        num = Number(node.tok.value).set_pos(node.pos_start,node.pos_end)
        return num


    def visit_SeparatorNode(self, node):
        '''
        Visits the nodes with the SEPARATOR token.
        :param node:
        :return:
        '''
        lower = self.visit(node.left_node)
        upper = self.visit(node.right_node)
        uniqueVar = self.makeUniqueVar()
        interval = TranslatedInterval(lower, upper,uniqueVar)
        self.intervalDict[uniqueVar] = interval
        #TODO: Estou a retornar a uniquevar de maneira a que a traducao fique apenas a variavel nova gerada. Talvez esta nao seja a melhor maneiora.
        translation = uniqueVar
        self.translation = translation
        return translation

    def visit_IntervalVarNode(self,node):
        return node.tok.value


    def visit_PropOpNode(self,node):
        leftNode = node.left_node
        rightNode = node.right_node
        visitLeftNode = self.visit(leftNode)
        visitRightNode = self.visit(rightNode)
        translatedOpTok = ''
        translation = ''
        if node.op_tok.type in [TT_ST,TT_GT,TT_GEQ,TT_SEQ]:
            if node.op_tok.type in TT_ST:
                translatedOpTok = '<'
            elif node.op_tok.type in TT_GT:
                translatedOpTok = '>'
            elif node.op_tok.type in TT_GEQ:
                translatedOpTok = '>='
            elif node.op_tok.type in TT_SEQ:
                translatedOpTok = '<='
            self.varDict[leftNode] = visitRightNode
        elif node.op_tok.matches(TT_KEYWORD, 'AND'):
            translatedOpTok = ' ∧ '
        elif node.op_tok.matches(TT_KEYWORD, 'OR'):
            translatedOpTok = ' ∨ '
        elif node.op_tok.type in (TT_IMPLIES):
            translatedOpTok = ' -> '
        if translatedOpTok != '':
            translation = str(visitLeftNode) + " " + translatedOpTok + " " + str(visitRightNode)
        else:
            translation = str(visitLeftNode) + " " + str(node.op_tok)+ " " + str(visitRightNode)
        self.translation = translation
        return translation

    def visit_ProgOpNode(self,node):
        leftNode = node.left_node
        rightNode = node.right_node
        visitLeftNode = self.visit(leftNode)
        visitRightNode = self.visit(rightNode)
        translatedOpTok = ''
        if node.op_tok.type in TT_PROGASSIGN:
            translatedOpTok = ':='
        if translatedOpTok != '':
            translation = str(visitLeftNode) + " " + translatedOpTok + " " + str(visitRightNode)
        else:
            translation = str(visitLeftNode) + " " + str(node.op_tok) + " " + str(visitRightNode)
        self.translation = translation
        return translation

    def visit_BoxPropNode(self,node):
        for boxNodeElement,boxPropElement in zip(node.element_nodes,node.boxProp):
            visitboxNodeElement = self.visit(boxNodeElement)
            visitboxPropElement = self.visit(boxPropElement)
        translation = '[ ' + str(visitboxNodeElement) + ' ] ' + str (visitboxPropElement)
        self.translation = translation
        return translation

    def visit_DiamondPropNode(self,node):
        for diamondNodeElement,diamondPropElement in zip(node.element_nodes,node.diamondProp):
            visitDiamondNodeElement = self.visit(diamondNodeElement)
            visitDiamondPropElement = self.visit(diamondPropElement)
        translation = '< ' + str(visitDiamondNodeElement) + ' > ' + str (visitDiamondPropElement)
        self.translation = translation
        return translation

    def visit_ProgDifNode(self,node):
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

    def visit_DifferentialVarNode(self,node):
        return node.tok.value

    def visit_NumberNode(self,node):
        return node.tok.value

    def makeUniqueVar(self):
        intervalVar = ''
        for var in LETTERS:
            if var not in self.varList:
                intervalVar = var
                self.varList.append(intervalVar)
                return intervalVar
            else:
                continue
        if intervalVar == '':
            return -1

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

    def __add__(self,other):
        if isinstance(other, Number):
            return Number(self.value + other.value)

    def __mul__(self,other):
        if isinstance(other, Number):
            return Number(self.value * other.value)

    def __lt__(self,other):
        if isinstance(other, Number):
            return self.value < other.value

    def __gt__(self,other):
        if isinstance(other, Number):
            return self.value > other.value

    def __le__(self,other):
        if isinstance(other, Number):
            return self.value <= other.value

    def __ge__(self,other):
        if isinstance(other, Number):
            return self.value >= other.value

    def __eq__(self,other):
        if isinstance(other, Number):
            return self.value == other.value

    def __repr__(self):
        return str(self.value)

class Interval:
    '''
    This class helps us represent the interval that resulted from an operation and keep track of errors.
    '''
    def __init__(self,lowerNum=None,upperNum=None):
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

    def __repr__(self):
        return '[' + str(self.lowerNum) + ',' + str(self.upperNum) + ']'

class TranslatedInterval:
    '''
    This class helps us represent the interval that resulted from an operation and keep track of errors.
    '''
    def __init__(self,lowerNum=None,upperNum=None,ineqVar=None):
        if lowerNum and upperNum is not None:
            self.lowerNum = lowerNum
            self.upperNum = upperNum
            self.ineqVar = ineqVar
            self.set_pos()
            self.set_lims()
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

    def set_lims(self):
        self.lowerLim = str(self.lowerNum) + '<=' + str(self.ineqVar)
        self.upperLim = str(self.ineqVar) + '<=' + str(self.upperNum)

    def __repr__(self):
        return self.lowerLim + ' ∧ ' + self.upperLim

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
