# type: ignore
from scanner import TokenType
import expr
import decl

class Parser():
    def __init__(self, grape, tokens):
        self.current = 0
        self.errorHandler = grape.errorHandler
        self.tokens = tokens
        self.statements = []

    def parse(self):
        while not self.isAtEnd():
            self.statements.append(self.declaration())
            return self.statements
        
    def declaration(self):
        try:
            if self.match([TokenType.IDENTIFIER]): return self.variableDecl()
        
        except ParseError:
            self.synchronize()
            return None
        
    def variableDecl(self):
        name = self.previous()
        initializer = None
        if self.match([TokenType.EQUAL]): initializer = self.expression()

        self.expect(TokenType.NEWLINE, "Unterminated statement, no newline present.")
        return decl.Variable(name, initializer)

    def statement(self):
        if self.match([TokenType.INSPECT]):
            expression = self.expression()
            self.expect(TokenType.NEWLINE, "Unterminated statement, no newline present.")
            return expr.Inspect(expression)
        else:
            self.syntaxError(self.peek(), "Expected a valid statement.")

    def expression(self):
        return self.equality()

    def equality(self):
        expression = self.comparison()

        while (self.match([TokenType.BANG_EQUAL, TokenType.EQUAL_EQUAL])):
            operator = self.previous()
            right = self.comparison()

            expression = expr.Binary(expression, operator, right)

        return expression
    
    def comparison(self):
        expression = self.term()

        while (self.match([TokenType.GREATER, TokenType.GREATER_EQUAL, TokenType.LESS, TokenType.LESS_EQUAL])):
            operator = self.previous()
            right = self.term()

            expression = expr.Binary(expression, operator, right)

        return expression
    
    def term(self):
        expression = self.factor()

        while (self.match([TokenType.MINUS, TokenType.PLUS])):
            operator = self.previous()
            right = self.factor()

            expression = expr.Binary(expression, operator, right)

        return expression
    
    def factor(self):
        expression = self.unary()

        while (self.match([TokenType.SLASH, TokenType.STAR])):
            operator = self.previous()
            right = self.unary()

            expression = expr.Binary(expression, operator, right)

        return expression
    
    def unary(self):
        if self.match([TokenType.NOT, TokenType.MINUS]):
            operator = self.previous()
            right = self.unary()

            return Unary(operator, right)
        
        return self.primary()
    
    def primary(self):
        if self.match([TokenType.FALSE]): return expr.Literal(False)
        if self.match([TokenType.TRUE]): return expr.Literal(True)
        if self.match([TokenType.IDENTIFIER]): return VariableDcl(self.previous())

        if self.match([TokenType.NUMBER, TokenType.STRING, TokenType.ATOM]):
            return expr.Literal(self.previous().literal)
        
        if self.match([TokenType.LEFT_BRACKET]): 
            expression = self.expression()
            items = [expression]

            while self.match([TokenType.COMMA]):
                expression = self.expression()
                items.append(expression)

            self.expect(TokenType.RIGHT_BRACKET, "Missing \"]\" to close list.")
            return expr.List(items)
        
        if self.match([TokenType.LEFT_BRACE]): 
            expression = self.expression()
            items = [expression]

            while self.match([TokenType.COMMA]):
                expression = self.expression()
                items.append(expression)

            self.expect(TokenType.RIGHT_BRACE, "Missing \"}\" to close tuple.")
            return expr.Tuple(items)
        
        if self.match([TokenType.LEFT_PAREN]): 
            expression = self.expression()
            self.expect(TokenType.RIGHT_PAREN, "Missing \")\" after expression.")
            return expr.Grouping(expression)
        
        self.syntaxError(self.peek(), "Expected expression.")

    def match(self, token_types):
        for token_type in token_types:
            if self.check(token_type):
                self.advance()
                return True
            
        return False
    
    def check(self, token_type):
        if self.isAtEnd(): return False
        return self.peek().token_type == token_type
    
    def advance(self):
        if not self.isAtEnd(): self.current += 1
        return self.previous()
    
    def isAtEnd(self):
        return self.peek().token_type == TokenType.EOF

    def peek(self): 
        return self.getTokenByIndex(self.current)

    def previous(self):
        return self.getTokenByIndex(self.current - 1)
    
    def getTokenByIndex(self, index):
        return self.tokens[index]
    
    def expect(self, token_type, fail_message):
        if self.check(token_type): return self.advance()

        self.syntaxError(self.peek(), fail_message)

    def syntaxError(self, token, message):
        if token.token_type == TokenType.EOF:
            error = self.errorHandler.report("Syntax error", token.line, "EOF", message)
        else:
            error = self.errorHandler.report("Syntax error", token.line, "'" + token.lexeme + "'", message)

        raise ParseError(error)

    def synchronize(self):
        self.advance()

        while not self.isAtEnd():
            if self.previous().token_type == TokenType.NEWLINE: return

            if self.peek().token_type in [TokenType.NAMESPACE, TokenType.FN, TokenType.IF, TokenType.ELSEIF, TokenType.ELSE]:
                return
            
            self.advance()

class ParseError(Exception):
    pass