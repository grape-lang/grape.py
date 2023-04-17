from utils import *
from scanner import TokenType

class Interpreter():
    def __init__(self, grape, statements):
        self.errorHandler = grape.errorHandler
        self.statements = statements

    def interpret(self):
        try:
            for statement in self.statements:
                statement.evaluate(self)
        except TypeCheckError as e:
            self.errorHandler.report("Runtime error", e.token.line, e.token.lexeme, e.message)

    def stringifyOutput(self, output):
        return str(output)
    
    def evaluateInspectStmt(self, expression):
        value = expression.evaluate(self)
        print(self.stringifyOutput(value))

    def evaluateBinary(self, operator, left, right):
        global maxDecimals

        left = left.evaluate(self)
        right = right.evaluate(self)

        match operator.token_type:
            case TokenType.MINUS: 
                self.checkBothNumbers(operator, left, right)
                return round(left - right, maxDecimals)
            case TokenType.SLASH:
                self.checkBothNumbers(operator, left, right)
                return round(left / right, maxDecimals)
            case TokenType.STAR:
                self.checkBothNumbers(operator, left, right)
                return round(left * right, maxDecimals)
            case TokenType.PLUS:
                if self.areBothNumbers(left, right):
                    return round(left + right, maxDecimals)
                elif self.areBothText(left, right):
                    return left + right
                else:
                    raise TypeCheckError(operator, "Operands must be two numbers or two strings.")
            case TokenType.GREATER:
                self.checkBothNumbers(operator, left, right)
                return left > right
            case TokenType.GREATER_EQUAL:
                self.checkBothNumbers(operator, left, right)
                return left >= right
            case TokenType.LESS:
                self.checkBothNumbers(operator, left, right)
                return left < right
            case TokenType.LESS_EQUAL:
                self.checkBothNumbers(operator, left, right)
                return left <= right
            case TokenType.EQUAL_EQUAL:
                return self.isEqual(left, right)
            case TokenType.BANG_EQUAL:
                return not self.isEqual(left, right)

    def evaluateGrouping(self, expr):
        return expr.evaluate(self)
    
    def evaluateLiteral(self, value):
        return value
    
    def evaluateCollection(self, items):
        return [item.evaluate(self) for item in items]

    def evaluateUnary(self, operator, right):
        right = right.evaluate(self)

        match operator.token_type:
            case TokenType.MINUS: 
                self.checkNumber(operator, right)
                return -right
            case TokenType.NOT:
                return not self.isTruthy(right)

    def isTruthy(self, input):
        input != False

    def isEqual(self, a, b):
        return a == b

    def checkNumber(self, operator, a):
        if not self.isNumber(a):
            raise TypeCheckError(operator, "Operand must be a number.")

    def checkBothNumbers(self, operator, a, b):
        if not self.areBothNumbers(a, b):
            raise TypeCheckError(operator, "Operands must both be a number.")

    def areBothNumbers(self, a, b):
        return self.isNumber(a) and self.isNumber(b)

    def isNumber(self, input):
        return isinstance(input, Decimal)

    def areBothText(self, a, b):
        return self.isText(a) and self.isText(b)

    def isText(self, input):
        return isinstance(input, str)

class TypeCheckError(Exception):
    def __init__(self, token, message):
        self.token = token
        self.message = message