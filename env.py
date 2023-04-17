from syntax.tokens import *

class Env:
    def __init__(self):
        self.values = {}

    def define(self, name: Token, value: any):
        self.values[name.lexeme] = value

    def get(self, name: Token) -> any:
        if name.lexeme in self.values:
            return self.values[name.lexeme]
        else:
            raise UndefinedError(name, "Undefined variable " + name.lexeme + ".")

class UndefinedError(Exception):
    def __init__(self, name: Token, message: str):
        self.name = name
        self.message = message