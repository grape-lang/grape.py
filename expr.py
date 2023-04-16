class Expr():
    pass

class Binary(Expr):
    def __init__(self, left, operator, right):
        self.left = left
        self.operator = operator
        self.right = right

    def __str__(self):
        return parenthesize(self.operator.lexeme + " " + str(self.left) + " " + str(self.right))
    
    def evaluate(self, interpreter):
        return interpreter.evaluateBinary(self.operator, self.left, self.right)

class Grouping(Expr):
    def __init__(self, expr):
        self.expr = expr

    def __str__(self):
        return parenthesize(str(self.expr))
    
    def evaluate(self, interpreter):
        return interpreter.evaluateGrouping(self.expr)

class Literal(Expr):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)
    
    def evaluate(self, interpreter):
        return interpreter.evaluateLiteral(self.value)
    
class Collection(Expr):
    def __init__(self, items):
        self.items = items

    def evaluate(self, interpreter):
        return interpreter.evaluateCollection(self.items)
        
    
class List(Collection):
    def __str__(self):
        items = [str(item) for item in self.items]
        return "[" + ", ".join(items) + "]"

class Tuple(Collection):
    def __str__(self):
        items = [str(item) for item in self.items]
        return "{" + ", ".join(items) + "}"

class Unary(Expr):
    def __init__(self, operator, right):
        self.operator = operator
        self.right = right
    
    def __str__(self):
        return parenthesize(self.operator.lexeme + str(self.right))
    
    def evaluate(self, interpreter):
        return interpreter.evaluateUnary(self.operator, self.right)
        

def parenthesize(input):
    return "( " + input + " )"
