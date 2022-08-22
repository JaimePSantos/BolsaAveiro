import sys

from core.Tokens import TT_INTERVALPLUS, \
    TT_INTERVALMULT


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
        # print("Found BinOpNode")
        # TODO: Repensar a logica dos intervalos, talvez usar um no para
        # o intervalo todo e depois dividi-lo em upper e lower.
        if node.op_tok.type in TT_INTERVALPLUS:
            self.visit(node.left_node)
            self.visit(node.right_node)
            # resultLower = self.lowerNumberList.addIntervals()
            # resultUpper = self.upperNumberList.addIntervals()
            # return idDL2DL(resultLower,resultUpper).set_pos()
            self.addIntervals()
            self.updateIntervalList()
            return self.resultInterval

        if node.op_tok.type in TT_INTERVALMULT:
            self.visit(node.left_node)
            self.visit(node.right_node)
            # self.intervalNumberList = (self.lowerNumberList.extend(self.upperNumberList))
            resultList = self.multIntervals()
            self.resultInterval = Interval(
                resultList.min(), resultList.max()).set_pos()
            self.updateIntervalList()
            return self.resultInterval

    def addIntervals(self):
        intervalList = self.intervalList
        resultLower = intervalList[0].lowerNum + \
            intervalList[1].lowerNum
        resultUpper = intervalList[0].upperNum + \
            intervalList[1].upperNum
        self.resultInterval = Interval(
            resultLower, resultUpper).set_pos()
        return self.resultInterval

    def multIntervals(self):
        '''
        Generates the set of numbers resulted from interval multiplication.
        :return:
        '''
        # TODO: Perceber o caso mais geral da multiplicaçao e fazer as alteraçoes de acordo.
        # intervalList = NumberList(self.numberList).separatedIntervals()
        intervalList = self.intervalList
        resultList = [
            intervalList[0].lowerNum *
            intervalList[1].lowerNum,
            intervalList[0].lowerNum *
            intervalList[1].upperNum,
            intervalList[0].upperNum *
            intervalList[1].lowerNum,
            intervalList[0].upperNum *
            intervalList[1].upperNum]
        return NumberList(resultList)

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
        print("idDL2DL List1 " + str(self.intervalList))
        return interval

    def updateIntervalList(self):
        self.intervalList = []
        self.intervalList.append(self.resultInterval)

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
        resultList = [
            intervalList[0][0] *
            intervalList[1][0],
            intervalList[0][0] *
            intervalList[1][1],
            intervalList[0][1] *
            intervalList[1][0],
            intervalList[0][1] *
            intervalList[1][1]]

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
        return NumberList(self.numberList +
                          (otherNumberList.numberList))

    def __repr__(self):
        return str(self.numberList)


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
        if res.error:
            self.error = res.error
        return res.value

    def success(self, value):
        self.value = value
        return self

    def failure(self, error):
        self.error = error
        return self
