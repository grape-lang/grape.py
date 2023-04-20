from syntax.tokens import *
from syntax.expr import Expr

class Stmt():
    pass

class Block(Stmt):
    def __init__(self, statements: Stmt):
        self.statements = statements

    def __str__(self) -> str:
        statements = [str(statement) for statement in self.statements]
        return " ( block " + " ".join(statements) + " ) "

class Inspect(Stmt):
    def __init__(self, expression: Expr):
        self.expression = expression

    def __str__(self) -> str:
        return " ( inspect " + str(self.expression) + " ) "
    
class Exit(Stmt):
    def __init__(self, code: Expr = None):
        self.code = code

    def __str__(self) -> str:
        if self.code:
            return " ( exit " + str(self.code) + " ) "
        else:
            return " ( exit ) "
