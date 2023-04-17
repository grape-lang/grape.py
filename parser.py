# type: ignore
from syntax.tokens import *

from syntax.stmt import Stmt
from syntax.expr import Expr

import syntax.stmt as stmt
import syntax.decl as decl
import syntax.expr as expr

class Parser():
    def __init__(self, grape, tokens: list[Token]):
        self.current = 0
        self.errorHandler = grape.errorHandler
        self.tokens = tokens
        self.statements = []

    def parse(self) -> list[Stmt]:
        while not self.isAtEnd():
            self.statements.append(self.declaration())
            
        return self.statements
        
    def declaration(self) -> Stmt:
        try:
            if self.match([TokenType.IDENTIFIER]) and self.match([TokenType.EQUAL]): 
                return self.variableDecl()

            return self.statement()
        
        except ParseError:
            self.synchronize()
        
    def variableDecl(self) -> Stmt:
        name = self.doublePrevious()
        initializer = self.expression()

        self.expect(TokenType.NEWLINE, "Unterminated statement, no newline present.")
        return decl.Variable(name, initializer)

    def statement(self) -> Stmt:
        if self.match([TokenType.INSPECT]):
            expression = self.expression()
            self.expect(TokenType.NEWLINE, "Unterminated statement, no newline present.")
            return stmt.Inspect(expression)
        else:
            self.syntaxError(self.peek(), "Expected a valid statement.")

    def expression(self) -> Expr:
        return self.equality()

    def equality(self) -> Expr:
        expression = self.comparison()

        while (self.match([TokenType.BANG_EQUAL, TokenType.EQUAL_EQUAL])):
            operator = self.previous()
            right = self.comparison()

            expression = expr.Binary(expression, operator, right)

        return expression
    
    def comparison(self)-> Expr:
        expression = self.term()

        while (self.match([TokenType.GREATER, TokenType.GREATER_EQUAL, TokenType.LESS, TokenType.LESS_EQUAL])):
            operator = self.previous()
            right = self.term()

            expression = expr.Binary(expression, operator, right)

        return expression
    
    def term(self)-> Expr:
        expression = self.factor()

        while (self.match([TokenType.MINUS, TokenType.PLUS])):
            operator = self.previous()
            right = self.factor()

            expression = expr.Binary(expression, operator, right)

        return expression
    
    def factor(self) -> Expr:
        expression = self.unary()

        while (self.match([TokenType.SLASH, TokenType.STAR])):
            operator = self.previous()
            right = self.unary()

            expression = expr.Binary(expression, operator, right)

        return expression
    
    def unary(self) -> Expr:
        if self.match([TokenType.NOT, TokenType.MINUS]):
            operator = self.previous()
            right = self.unary()

            return Unary(operator, right)
        
        return self.primary()
    
    def primary(self) -> Expr:
        if self.match([TokenType.FALSE]): return expr.Literal(False)
        if self.match([TokenType.TRUE]): return expr.Literal(True)
        if self.match([TokenType.IDENTIFIER]): return expr.Variable(self.previous())

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

    def match(self, token_types: list[TokenType]) -> bool:
        for token_type in token_types:
            if self.check(token_type):
                self.advance()
                return True
            
        return False
    
    def check(self, token_type: TokenType) -> bool:
        if self.isAtEnd(): return False
        return self.peek().token_type == token_type
    
    def advance(self) -> Token:
        if not self.isAtEnd(): self.current += 1
        return self.previous()
    
    def isAtEnd(self) -> bool:
        return self.peek().token_type == TokenType.EOF

    def peek(self) -> Token: 
        return self.getTokenByIndex(self.current)

    def previous(self) -> Token:
        return self.getTokenByIndex(self.current - 1)
    
    def doublePrevious(self) -> Token:
        return self.getTokenByIndex(self.current - 2)
    
    def getTokenByIndex(self, index: int) -> Token:
        return self.tokens[index]
    
    def expect(self, token_type: TokenType, fail_message: str) -> Token | None:
        if self.check(token_type): return self.advance()

        self.syntaxError(self.peek(), fail_message)

    def syntaxError(self, token: Token, message: str) -> None:
        if token.token_type == TokenType.EOF:
            error = self.errorHandler.report("Syntax error", token.line, "EOF", message)
        else:
            error = self.errorHandler.report("Syntax error", token.line, "'" + token.lexeme + "'", message)

        raise ParseError(error)

    def synchronize(self) -> None:
        self.advance()

        while not self.isAtEnd():
            if self.previous().token_type == TokenType.NEWLINE: return

            if self.peek().token_type in [TokenType.NAMESPACE, TokenType.FN, TokenType.IF, TokenType.ELSEIF, TokenType.ELSE]:
                return
            
            self.advance()

class ParseError(Exception):
    pass