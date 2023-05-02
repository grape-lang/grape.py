from env import Env

from syntax.tokens import Token
import syntax.expr as expr

class Callable:
    def __init__(self, name: str, arity: tuple[int]):
        self.name = name
        self.arity = arity

    def call(self, interpreter, arguments: list, errorToken: Token):
        pass

    def __str__(self) -> str:
        return "#Function <" + self.name + ">" 

class Builtin(Callable):
    def __init__(self, name: str, arity: tuple[int], impl):
        self.impl = impl
        super().__init__(name, arity)

    def call(self, interpreter, arguments: list, errorToken: Token):
        return self.impl(arguments, errorToken, interpreter)

class Lambda(Callable):
    def __init__(self, declaration: expr.Lambda, closure: Env):
        self.closure = closure
        self.declaration = declaration

        arity = (len(declaration.params), )
        super().__init__("anonymous", arity)      

    def call(self, interpreter, arguments: list, errorToken: Token):
        env = Env(self.closure)
        for i in range(0, self.arity[0]):
            env.define(self.declaration.params[i], arguments[i])

        return interpreter.evaluateBlock(self.declaration.body, env)

class Function(Lambda):
    def __init__(self, declaration: expr.Function, closure: Env):
        super().__init__(declaration, closure)
        # Override the "anonymous" name field from Lambda
        self.name = declaration.name.lexeme

class ArgumentError(Exception):
    def __init__(self, token: Token, message: str):
        self.token = token
        self.message = message