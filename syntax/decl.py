from syntax.stmt import *
from syntax.tokens import Token

class Decl(Stmt):
    pass

class Variable(Decl):
    def __init__(self, name: Token, initializer: Expr):
        self.name = name
        self.initializer = initializer

    def __str__(self) -> str:
        return " ( var " + self.name.lexeme + " " + str(self.initializer) + " )"