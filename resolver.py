from interpreter import Interpreter

import syntax.expr as expr

from syntax.stmt import Stmt
from syntax.expr import Expr

class Resolver:
    def __init__(self, interpreter: Interpreter):
        self.interpreter = interpreter
        self.scopes = []

    def block(self, statements: list[Stmt]):
        self.beginScope()
        self.resolveStatements(statements)
        self.endScope()

    def resolveStatements(self, statements: list[Stmt]):
        for statement in statements: 
            self.resolveExpression(statement.expression)

    def resolveExpression(self, expression: Expr):
        match expression:
            case expr.VariableDecl():
                self.variableDecl(expression)
                

    def variableDecl(self, expression: expr.VariableDecl):
        self.declare(expression.name)
        self.resolve(expression.initializer)
        self.define(expression.name)

    def beginScope(self):
        self.scopes.append(dict())

    def endScope(self):
        self.scopes.pop()
