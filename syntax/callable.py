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
        return self.impl(arguments, errorToken)

class Lambda(Callable):
    def __init__(self, declaration: expr.Lambda):
        self.declaration = declaration

        arity = (len(declaration.params), )
        super().__init__("anonymous", arity)      

    def call(self, interpreter, arguments: list, errorToken: Token):
        env = Env(interpreter.globalEnv)
        for i in range(0, self.arity[0]):
            env.define(self.declaration.params[i], arguments[i])

        return interpreter.evaluateBlock(self.declaration.body, env)

class ArgumentError(Exception):
    def __init__(self, token: Token, message: str):
        self.token = token
        self.message = message