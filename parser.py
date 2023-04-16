# type: ignore
from scanner import TokenType
from expr import Binary
from expr import Unary
from expr import Literal
from expr import List
from expr import Tuple
from expr import Grouping

class Parser():
    def __init__(self, grape, tokens):
        self.current = 0
        self.errorHandler = grape.errorHandler
        self.tokens = tokens

    def parse(self):
        try:
            return self.expression()
        except ParseError:
            return None

    def expression(self):
        return self.equality()

    def equality(self):
        expr = self.comparison()

        while (self.match([TokenType.BANG_EQUAL, TokenType.EQUAL_EQUAL])):
            operator = self.previous()
            right = self.comparison()

            expr = Binary(expr, operator, right)

        return expr
    
    def comparison(self):
        expr = self.term()

        while (self.match([TokenType.GREATER, TokenType.GREATER_EQUAL, TokenType.LESS, TokenType.LESS_EQUAL])):
            operator = self.previous()
            right = self.term()

            expr = Binary(expr, operator, right)

        return expr
    
    def term(self):
        expr = self.factor()

        while (self.match([TokenType.MINUS, TokenType.PLUS])):
            operator = self.previous()
            right = self.factor()

            expr = Binary(expr, operator, right)

        return expr
    
    def factor(self):
        expr = self.unary()

        while (self.match([TokenType.SLASH, TokenType.STAR])):
            operator = self.previous()
            right = self.unary()

            expr = Binary(expr, operator, right)

        return expr
    
    def unary(self):
        if self.match([TokenType.NOT, TokenType.MINUS]):
            operator = self.previous()
            right = self.unary()

            return Unary(operator, right)
        
        return self.primary()
    
    def primary(self):
        if self.match([TokenType.FALSE]): return Literal(False)
        if self.match([TokenType.TRUE]): return Literal(True)

        if self.match([TokenType.NUMBER, TokenType.STRING]):
            return Literal(self.previous().literal)
        
        if self.match([TokenType.LEFT_BRACKET]): 
            expr = self.expression()
            items = [expr]

            while self.match([TokenType.COMMA]):
                expr = self.expression()
                items.append(expr)

            self.expect(TokenType.RIGHT_BRACKET, "Missing \"]\" to close list.")
            return List(items)
        
        if self.match([TokenType.LEFT_BRACE]): 
            expr = self.expression()
            items = [expr]

            while self.match([TokenType.COMMA]):
                expr = self.expression()
                items.append(expr)

            self.expect(TokenType.RIGHT_BRACE, "Missing \"}\" to close tuple.")
            return Tuple(items)
        
        if self.match([TokenType.LEFT_PAREN]): 
            expr = self.expression()
            self.expect(TokenType.RIGHT_PAREN, "Missing \")\" after expression.")
            return Grouping(expr)
        
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
            error = self.errorHandler.report("Syntaxt error", token.line, "'" + token.lexeme + "'", message)

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