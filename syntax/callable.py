from syntax.tokens import Token

class Callable:
    def __init__(self, name: str, arity: tuple[int], impl):
        self.name = name
        self.arity = arity
        self.impl = impl

    def call(self, interpreter, errorToken: Token, arguments: list[any]):
        return self.impl(interpreter, errorToken, arguments)

    def __str__(self) -> str:
        return "#Function <" + self.name.lexeme + ">" 

class ArgumentError(Exception):
    def __init__(self, token: Token, message: str):
        self.token = token
        self.message = message