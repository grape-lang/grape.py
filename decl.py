from stmt import *

class Decl(Stmt):
    pass

class Variable(Decl):
    def __init__(self, name, initializer):
        self.name = name
        self.initializer = initializer