from syntax.tokens import Token
from syntax.stmt import Stmt

class Expr():
    pass

class VariableDecl(Expr):
    def __init__(self, name: Token, initializer: Expr):
        self.name = name
        self.initializer = initializer

    def __str__(self) -> str:
        return " ( var " + self.name.lexeme + " " + str(self.initializer) + " )"

class If(Expr):
    def __init__(self, condition: Expr, thenBranch: Stmt, elseBranch: Stmt = None):
        self.condition = condition
        self.thenBranch = thenBranch
        self.elseBranch = elseBranch

    def __str__(self) -> str:
        if self.elseBranch:
            return " ( if " + str(self.condition) +" do " + str(self.thenBranch) + " else " + str(self.elseBranch) + " )"
        else:
            return " ( if " + str(self.condition) +" do " + str(self.thenBranch) + " )"

class Block(Expr):
    def __init__(self, statements: list[Stmt]):
        self.statements = statements

    def __str__(self) -> str:
        statements = [str(statement) for statement in self.statements]
        return " ( block do " + " ".join(statements) + " ) "

class Binary(Expr):
    def __init__(self, left: Expr, operator: Token, right: Expr):
        self.left = left
        self.operator = operator
        self.right = right

    def __str__(self) -> str:
        return parenthesize(self.operator.lexeme + " " + str(self.left) + " " + str(self.right))
    
class Grouping(Expr):
    def __init__(self, expression: Expr):
        self.expression = expression

    def __str__(self) -> str:
        return parenthesize(str(self.expression))

class Literal(Expr):
    def __init__(self, value):
        self.value = value

    def __str__(self) -> str:
        return str(self.value)
    
class Collection(Expr):
    def __init__(self, items: list[Expr]):
        self.items = items
    
class List(Collection):
    def __str__(self) -> str:
        items = [str(item) for item in self.items]
        return "[" + ", ".join(items) + "]"

class Tuple(Collection):
    def __str__(self) -> str:
        items = [str(item) for item in self.items]
        return "{" + ", ".join(items) + "}"

class Logical(Expr):
    def __init__(self, left: Expr, operator: Token, right: Expr):
        self.left = left
        self.operator = operator
        self.right = right

    def __str__(self) -> str:
        return parenthesize(self.operator.lexeme + " " + str(self.left) + " " + str(self.right))

class Unary(Expr):
    def __init__(self, operator: Token, right: Expr):
        self.operator = operator
        self.right = right
    
    def __str__(self) -> str:
        return parenthesize(self.operator.lexeme + str(self.right))
        
class VariableExpr(Expr):
    def __init__(self, name: Token):
        self.name = name

    def __str__(self) -> str:
        return self.name.lexeme

def parenthesize(input):
    return "( " + input + " )"
