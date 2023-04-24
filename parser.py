# type: ignore
from syntax.tokens import *
from syntax.callable import *

from syntax.stmt import Stmt
from syntax.expr import Expr

import syntax.stmt as stmt
import syntax.expr as expr

class Parser():
    def __init__(self, grape, tokens: list[Token]):
        self.current = 0
        self.errorHandler = grape.errorHandler
        self.tokens = tokens
        self.statements = []

    def parse(self) -> list[Stmt]:
        while not self.isAtEnd():
            statement = self.statement()
            if statement: self.statements.append(statement)
            
        return self.statements
        
    def statement(self) -> Stmt:
        try:
            if not self.match(TokenType.NEWLINE): # Skip empty lines
                statement = self.exprStmt()
                self.expect(TokenType.NEWLINE, "Unterminated statement, no newline present.")
                return statement
            
        except ParseError:
            self.synchronize()
            
    def exprStmt(self) -> Stmt:
        return stmt.ExprStmt(self.expression())  
    
    def expression(self) -> Expr:
        if self.check_sequence([TokenType.IDENTIFIER, TokenType.EQUAL]): 
            return self.variableDecl()
        
        if self.match(TokenType.FN):
            if self.match(TokenType.IDENTIFIER):
                return self.functionDecl()
            else:
                return self.lambdaExpr()
        
        if self.match(TokenType.IF):
            return self.conditionalIf()
        
        elif self.match(TokenType.DO):
            return expr.Block(self.block())
        
        else:
            return self.logicOr()
            
    def variableDecl(self) -> Expr:
        # Consumes the identifier. 
        # Needed because we use `check` and not `match` 
        # in the callee of this function.
        self.advance() 
        name = self.previous()

        # Concums the equal (=) sign.
        self.advance()

        initializer = self.expression()
        return expr.VariableDecl(name, initializer)
    
    def functionDecl(self) -> Expr:
        name = self.previous()
        (parameters, body) = self.parseFunction()
        return expr.Function(name, parameters, body)
    
    def lambdaExpr(self) -> Expr:
        (parameters, body) = self.parseFunction()
        return expr.Lambda(parameters, body)
    
    def parseFunction(self) -> (list[Token], expr.Block):
        self.expect(TokenType.LEFT_PAREN, "Missing opening \"(\" before function arguments.")

        parameters = []

        if not self.check(TokenType.RIGHT_PAREN):
            invalidParameterErrorMessage = "Parameters for an function can only be identifiers."

            parameter = self.expect(TokenType.IDENTIFIER, invalidParameterErrorMessage)
            parameters.append(parameter)

            while self.match(TokenType.COMMA):
                parameter = self.expect(TokenType.IDENTIFIER, invalidParameterErrorMessage)
                parameters.append(parameter)

        self.expect(TokenType.RIGHT_PAREN, "Missing closing \"(\" after function arguments.")

        self.expect(TokenType.DO, "Expected do-end block after function header.")

        body = self.block()

        return (parameters, body)
    
    def conditionalIf(self) -> Expr:
        self.expect(TokenType.LEFT_PAREN, "Missing opening \"(\" before if-statement condition.")
        condition = self.logicOr()
        self.expect(TokenType.RIGHT_PAREN, "Missing closing \")\" after if-statement condition.")
        
        thenBranch = None
        elseBranch = None
        
        if(self.match(TokenType.DO)):
            doStatements = self.parseBlock([TokenType.END, TokenType.ELSE])
            thenBranch = expr.Block(doStatements)
            
            if self.match(TokenType.ELSE):
                elseStatements = self.parseBlock([TokenType.END])
                elseBranch = expr.Block(elseStatements)

            self.expect(TokenType.END, "Expected \"end\" to terminate do-else-block.")
                
        else:
            thenBranch = self.blockify(self.expression())

        if(self.match(TokenType.ELSE)):
            elseBranch = self.blockify(self.expression())
            
        return expr.If(condition, thenBranch, elseBranch) 
    
    def blockify(self, expression: Expr) -> expr.Block:
        statement = stmt.ExprStmt(expression)
        return expr.Block([statement])

    def parseBlock(self, endTokens: list[TokenType]):
        statements = []

        while not self.check_multiple(endTokens) and not self.isAtEnd():
            statement = self.statement()
            if statement: statements.append(statement)

        return statements

    def block(self) -> list[Stmt]:
        statements = self.parseBlock([TokenType.END])

        self.expect(TokenType.END, "Expected \"end\" to terminate do-block.")
        return statements
    
    def logicOr(self) -> Expr:
        expression = self.logicAnd()

        while(self.match(TokenType.OR)):
            operator = self.previous()
            right = self.logicAnd()
            expression = expr.Logical(expression, operator, right)

        return expression
    
    def logicAnd(self) -> Expr:
        expression = self.equality()

        while(self.match(TokenType.AND)):
            operator = self.previous()
            right = self.equality()
            expression = expr.Logical(expression, operator, right)

        return expression

    def equality(self) -> Expr:
        expression = self.comparison()

        while (self.match_either([TokenType.BANG_EQUAL, TokenType.EQUAL_EQUAL])):
            operator = self.previous()
            right = self.comparison()

            expression = expr.Binary(expression, operator, right)

        return expression
    
    def comparison(self)-> Expr:
        expression = self.term()

        while (self.match_either([TokenType.GREATER, TokenType.GREATER_EQUAL, TokenType.LESS, TokenType.LESS_EQUAL])):
            operator = self.previous()
            right = self.term()

            expression = expr.Binary(expression, operator, right)

        return expression
    
    def term(self)-> Expr:
        expression = self.factor()

        while (self.match_either([TokenType.MINUS, TokenType.PLUS])):
            operator = self.previous()
            right = self.factor()

            expression = expr.Binary(expression, operator, right)

        return expression
    
    def factor(self) -> Expr:
        expression = self.unary()

        while (self.match_either([TokenType.SLASH, TokenType.STAR])):
            operator = self.previous()
            right = self.unary()

            expression = expr.Binary(expression, operator, right)

        return expression
    
    def unary(self) -> Expr:
        if self.match_either([TokenType.NOT, TokenType.MINUS]):
            operator = self.previous()
            right = self.unary()

            return expr.Unary(operator, right)
        
        return self.call()
    
    def call(self) -> Expr:
        expression = self.primary()

        while self.match(TokenType.LEFT_PAREN):
            expression = self.finishCall(expression)

        return expression

    def finishCall(self, callee: Expr) -> Expr:
        arguments = []
        
        if not self.check(TokenType.RIGHT_PAREN):
            arguments.append(self.expression())
            while self.match(TokenType.COMMA):
                if len(arguments) >= 255: self.syntaxError(self.peek(), "Can't have more than 255 arguments in a function call.")
                arguments.append(self.expression())

        closingParenToken = self.expect(TokenType.RIGHT_PAREN, "Expected \"\" after arguments in function call.")

        return expr.Call(callee, closingParenToken, arguments)
    
    def primary(self) -> Expr:
        if self.match(TokenType.FALSE): return expr.Literal(False)
        if self.match(TokenType.TRUE): return expr.Literal(True)
        if self.match(TokenType.IDENTIFIER): return expr.VariableExpr(self.previous())

        if self.match_either([TokenType.NUMBER, TokenType.STRING, TokenType.ATOM]):
            return expr.Literal(self.previous().literal)
        
        if self.match(TokenType.LEFT_BRACKET):
            if not self.check(TokenType.RIGHT_BRACKET):
                items = self.collection()
            else:
                items = []

            self.expect(TokenType.RIGHT_BRACKET, "Missing \"]\" to close list.")
            return expr.List(items)
        
        if self.match(TokenType.LEFT_BRACE): 
            if not self.check(TokenType.RIGHT_BRACE):
                items = self.collection()
            else:
                items = []

            self.expect(TokenType.RIGHT_BRACE, "Missing \"}\" to close tuple.")
            return expr.Tuple(items)
        
        if self.match(TokenType.LEFT_PAREN): 
            expression = self.expression()

            self.expect(TokenType.RIGHT_PAREN, "Missing \")\" after expression.")
            return expr.Grouping(expression)
        
        self.syntaxError(self.peek(), "Expected expression.")

    def collection(self) -> list[Expr]:
        expression = self.expression()
        items = [expression]

        while self.match(TokenType.COMMA):
            expression = self.expression()
            items.append(expression)

        return items

    def match_either(self, token_types: list[TokenType]) -> bool:
        for token_type in token_types:
            if self.match(token_type): return True
            
        return False
    
    def match(self, token_type: TokenType) -> bool:
        if self.check(token_type):
            self.advance()
            return True
        else:
            return False
        
    def check_multiple(self, token_types: list[TokenType]) -> bool:
        for token_type in token_types:
            if self.check(token_type): return True

        return False
    
    def check_sequence(self, token_types: list[TokenType]) -> bool:
        acc = []
        for i in range(len(token_types)):
            token = self.getTokenByIndex(self.current + i)
            acc.append(token_types[i] == token.token_type)

        return all(acc)
    
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
    
    def getTokenByIndex(self, index: int) -> Token:
        return self.tokens[index]
    
    def expect(self, token_type: TokenType, fail_message: str) -> Token | None:
        if self.check(token_type): return self.advance()

        self.syntaxError(self.peek(), fail_message)

    def syntaxError(self, token: Token, message: str) -> None:
        if token.token_type == TokenType.EOF:
            error = self.errorHandler.report("Syntax error", token.line, token.col, "EOF", message)
        else:
            error = self.errorHandler.report("Syntax error", token.line, token.col, "'" + token.lexeme + "'", message)

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
