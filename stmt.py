from expr import Expr

class Stmt():
    pass

class Inspect(Stmt):
    def __init__(self, expression: Expr):
        self.expression = expression

    def __str__(self) -> str:
        return " ( inspect " + str(self.expression) + " ) "