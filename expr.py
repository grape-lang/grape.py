from tokens import Token

class Expr():
    pass

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

class Unary(Expr):
    def __init__(self, operator: Token, right: Expr):
        self.operator = operator
        self.right = right
    
    def __str__(self) -> str:
        return parenthesize(self.operator.lexeme + str(self.right))
        
class Variable(Expr):
    def __init__(self, name: Token):
        self.name = name

    def __str__(self) -> str:
        return self.name.lexeme

def parenthesize(input):
    return "( " + input + " )"
