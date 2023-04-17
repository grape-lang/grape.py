class Stmt():
    pass

class Inspect(Stmt):
    def __init__(self, expression):
        self.expression = expression

    def evaluate(self, interpreter):
        interpreter.evaluateInspectStmt(self.expression)