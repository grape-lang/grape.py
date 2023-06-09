from env import *
from syntax.callable import *
from runtime.builtin import *

from decimal import *
from syntax.tokens import *

from syntax.stmt import Stmt
from syntax.expr import Expr

import syntax.stmt as stmt
import syntax.expr as expr

class Interpreter():
    def __init__(self, grape, statements: list[Stmt]):
        self.globalEnv = Env()
        self.globalEnv.define_builtin(printFn)
        self.globalEnv.define_builtin(writeFn)
        self.globalEnv.define_builtin(exitFn)
        self.globalEnv.define_builtin(lenFn)
        self.globalEnv.define_builtin(elemFn)
        self.globalEnv.define_builtin(appendFn)
        self.globalEnv.define_builtin(forFn)
        self.globalEnv.define_builtin(accumulateFn)        

        self.env = self.globalEnv
        self.errorHandler = grape.errorHandler
        self.statements = statements

    def interpret(self) -> None:
        try:
            for statement in self.statements:
                self.evaluateStatement(statement)

        except TypeCheckError as e:
            self.errorHandler.report("Runtime error", e.token.line, e.token.col, quote(e.token.lexeme), e.message)

        except UndefinedError as e:
            self.errorHandler.report("Runtime error", e.name.line, e.name.col, quote(e.name.lexeme), e.message)

        except ArgumentError as e:
            self.errorHandler.report("Argument error", e.token.line, e.token.col, quote(e.token.lexeme), e.message)
    
    def evaluateStatement(self, statement: Stmt):
        return self.evaluateExpression(statement.expression)

    def evaluateExpression(self, expression: Expr):
        match expression:
            case expr.If():
                return self.evaluateIf(expression.condition, expression.thenBranch, expression.elseBranch)
            
            case expr.Block():
                return self.evaluateBlock(expression.statements)
            
            case expr.VariableDecl():
                return self.evaluateVariableDecl(expression.name, expression.initializer)
            
            case expr.VariableExpr():
                return self.evaluateVariableExpr(expression.name)
            
            case expr.Binary(): 
                return self.evaluateBinary(expression.operator, expression.left, expression.right)

            case expr.Grouping():
                return self.evaluateGrouping(expression.expression)

            case expr.Literal():
                return self.evaluateLiteral(expression.value)
            
            case expr.List():
                return self.evaluateCollection(expression.items)

            case expr.Tuple():
                return self.evaluateCollection(expression.items)
            
            case expr.Logical():
                return self.evaluateLogical(expression.left, expression.operator, expression.right)
            
            case expr.Call():
                return self.evaluateFunctionCall(expression.callee, expression.closingParenToken, expression.arguments)
            
            case expr.Function():
                return self.evaluateFunctionDecl(expression)

            case expr.Lambda():
                return self.evaluateLambda(expression)
            
            case expr.Unary():
                return self.evaluateUnary(expression.operator, expression.right)

    def evaluateVariableDecl(self, name: Token, initializer: Expr):
        value = self.evaluateExpression(initializer)
        self.env.define(name, value)
        return value

    def evaluateIf(self, condition: Expr, thenBranch: Stmt, elseBranch: Stmt):
        condition = self.evaluateExpression(condition)

        if self.isTruthy(condition):
            return self.evaluateExpression(thenBranch)
        else:
            if elseBranch:
                return self.evaluateExpression(elseBranch)

    def evaluateBlock(self, statements: list[Stmt], env = None):
        outerEnv = self.env
        blockEnv = Env(env or outerEnv)
        
        self.env = blockEnv

        for statement in statements:
            output = self.evaluateStatement(statement)

        self.env = outerEnv
        return output

    def evaluateVariableExpr(self, name: Token):
        return self.env.get(name)

    def evaluateBinary(self, operator: Token, left: Expr, right: Expr):
        global maxDecimals

        left = self.evaluateExpression(left)
        right = self.evaluateExpression(right)

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
                elif self.areBothCollection(left, right):
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

    def evaluateGrouping(self, expr: Expr):
        return self.evaluateExpression(expr)
    
    def evaluateLiteral(self, value: any):
        return value
    
    def evaluateCollection(self, items: list[Expr]):
        return [self.evaluateExpression(item) for item in items]
    
    def evaluateLogical(self, left: Expr, operator: Token, right: Expr):
        left = self.evaluateExpression(left)

        match operator.token_type:
            case TokenType.OR: 
                if self.isTruthy(left):
                    return left
                else:
                    return self.evaluateExpression(right)
            case TokenType.NOT:
                if not self.isTruthy(left):
                    return left
                else:
                    return self.evaluateExpression(right)

    def evaluateFunctionCall(self, callee: Expr, closingParenToken: Token, arguments: list[Expr]):
        function = self.evaluateExpression(callee)

        if not isinstance(function, Callable):
            raise TypeCheckError(closingParenToken, "Can only call functions.")

        arguments = [self.evaluateExpression(expression) for expression in arguments]

        if not len(arguments) in function.arity:
            raise TypeCheckError(closingParenToken, "Expected " + str(function.arity[0]) + " arguments, but got " + str(len(arguments)) + "." )

        return function.call(self, arguments, closingParenToken)

    def evaluateFunctionDecl(self, declaration):
        function = Function(declaration, self.env)
        self.env.define(declaration.name, function)
        return function

    def evaluateLambda(self, declaration):
        return Lambda(declaration, self.env)

    def evaluateUnary(self, operator: Token, right: Expr):
        right = self.evaluateExpression(right)

        match operator.token_type:
            case TokenType.MINUS: 
                self.checkNumber(operator, right)
                return -right
            case TokenType.NOT:
                return not self.isTruthy(right)

    def isTruthy(self, input: any) -> bool:
        return input != False

    def isEqual(self, a: any, b: any) -> bool:
        return a == b

    def checkNumber(self, operator: Token, a: any) -> None:
        if not self.isNumber(a):
            raise TypeCheckError(operator, "Operand must be a number.")

    def checkBothNumbers(self, operator: Token, a: any, b: any) -> None:
        if not self.areBothNumbers(a, b):
            raise TypeCheckError(operator, "Operands must both be a number.")

    def areBothNumbers(self, a: any, b: any) -> bool:
        return self.isNumber(a) and self.isNumber(b)

    def isNumber(self, input: any) -> bool:
        return isinstance(input, Decimal)

    def areBothText(self, a: any, b: any) -> bool:
        return self.isText(a) and self.isText(b)

    def isText(self, input: any) -> bool:
        return isinstance(input, str)

    def areBothCollection(self, a: any, b: any) -> bool:
        return self.isCollection(a) and self.isCollection(b)

    def isCollection(self, input: any) -> bool:
        return isinstance(input, list)

class TypeCheckError(Exception):
    def __init__(self, token: Token, message: str):
        self.token = token
        self.message = message

def quote(a: str) -> str:
    return "\"" + a + "\""
