class Stmt():
    pass

class ExprStmt(Stmt):
    def __init__(self, expression):
        self.expression = expression

    def __str__(self) -> str:
        return str(self.expression)