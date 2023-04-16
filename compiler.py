import utils
from enum import Enum

class TokenType(Enum):
    LEFT_PAREN = "("
    RIGHT_PAREN = ")"
    LEFT_BRACE = "{"
    RIGHT_BRACE = "}"
    LEFT_BRACKET = "["
    RIGHT_BRACKET = "]"
    COMMA = ","
    DOT = "."
    MINUS = "-"
    PLUS = "+"
    SLASH = "/"
    PIPE = "|"
    PIPE_ARROW = "|>"

    EQUAL = "="
    BANG_EQUAL = "!="
    EQUAL_EQUAL = "=="
    GREATER = ">"
    GREATER_EQUAL = ">="
    LESS = "<"
    LESS_EQUAL = "<="

    IDENTIFIER = 1
    STRING = 2 
    NUMBER = 3
    ATOM = 4

    AND = "and"
    NOT = "not"
    OR = "or"
    NOR = "nor"
    FN = "fn"
    NAMESPACE = "namespace"
    DO = "do"
    END = "end"
    TRUE = "true"
    FALSE = "false"

    NEWLINE = 5
    EOF = 6

class Token:
    def __init__(self, token_type, lexeme, literal, line, col):
        self.token_type = token_type
        self.lexeme = lexeme
        self.literal = literal
        self.line = line
        self.col = col

    def __str__(self):
        return str(self.token_type) + " " + str(self.lexeme) + " " + str(self.literal)

class Scanner:
    def __init__(self, grape, source): 
        self.tokens = []
        self.start = 0
        self.current = 0
        self.line = 1
        self.errorHandler = grape.errorHandler
        self.source = source

    def scanTokens(self):
        while not self.isAtEnd():
            self.start = self.current
            self.scanToken()

        self.tokens.append(Token(TokenType.EOF, "", None, self.line, self.current))
        return self.tokens

    def isAtEnd(self):
        sourceLength = len(self.source) # convert to amount of indexes
        return self.current >= sourceLength

    def scanToken(self):
        c = self.advance()

        match c:
            case "!":
                if self.match("="):
                    self.addToken(TokenType.BANG_EQUAL)
                else:
                    self.syntaxError(c)
        
            case "=":
                token = TokenType.EQUAL_EQUAL if self.match("=") else TokenType.EQUAL
                self.addToken(token)

            case "<":
                token = TokenType.LESS_EQUAL if self.match("=") else TokenType.LESS
                self.addToken(token)
            
            case ">":
                token = TokenType.GREATER_EQUAL if self.match("=") else TokenType.GREATER
                self.addToken(token)

            case "|":
                token = TokenType.PIPE_ARROW if self.match(">") else TokenType.PIPE
                self.addToken(token)

            case "/":
                if self.match("/"):
                    self.handleComment()
                else:
                    self.addToken(TokenType.SLASH)

            case whitespace if whitespace in [" ", "\r",  "\t"]:
                "" # Ignore whitespace

            case "\n":
                self.line += 1

            case "\"":
                self.handleString()

            case digit if c.isdigit():
                self.handleNumber()

            case atom if self.isAtomChar(c):
                self.handleAtom()

            case identifier if self.isIdentifierChar(c):
                self.handleIdentifier()

            case other:
                if self.isValidTokenType(c):
                    self.addToken(TokenType(c))
                else:
                    self.syntaxError(c)

    def handleString(self):
        while self.peek() != "\"" and not self.isAtEnd():
            if self.peek() == "/n": self.line += 1
            self.advance()

        if self.isAtEnd():
            self.errorHandler.report("Syntax error", self.line, self.start, "Unterminated string")
            return

        # Advance once more for the closing "
        self.advance()

        literal = self.source[self.start + 1:self.current - 1]
        self.addToken(TokenType.STRING, literal)

    def handleComment(self):
        self.skipToNextLine()

    def skipToNextLine(self):
        while self.peek() != "\n" and not self.isAtEnd():
            self.advance()

    def handleNumber(self):
        while self.peek().isdigit(): self.advance()

        if self.peek() == "." and self.doublePeek().isdigit():
            self.advance()
            while self.peek().isdigit(): self.advance()

        self.addToken(TokenType.NUMBER, float(self.currentString()))

    def isAtomChar(self, c):
        return c in utils.charRange("A", "Z") or c == "@"

    def isIdentifierChar(self, c):
        return self.isAlpha(c)

    def handleAtom(self):
        while self.isAlphaNumeric(self.peek()): self.advance()
        self.addToken(TokenType.ATOM)

    def handleIdentifier(self):
        while self.isAlphaNumeric(self.peek()): self.advance()

        currentString = self.currentString()
        if self.isValidTokenType(currentString):
            self.addToken(TokenType(currentString))
            return

        self.addToken(TokenType.IDENTIFIER)

    def isAlpha(self, c):
        return c in utils.charRange("a", "z") or c == "_"

    def isAlphaNumeric(self, c):
        return self.isAlpha(c) or c.isdigit()

    def syntaxError(self, unexpectedString = ""):
        if unexpectedString != "":
            message = "Unexpected \"" + unexpectedString + "\""
        else:
            message = ""

        self.errorHandler.report("Syntax error", self.line, self.current, message)

    def advance(self):
        self.current += 1
        return self.currentString()

    def match(self, expected):
        if self.isAtEnd(): return False
        if self.nextChar() != expected: return False

        self.current += 1
        return True

    def peek(self):
        if self.isAtEnd(): return '\0';
        return self.nextChar()    
    
    def doublePeek(self):
        afterNextChar = self.current + 1

        if afterNextChar >= len(self.source): return "\0"
        return self.charAt(afterNextChar)

    def currentString(self):
        return self.source[self.start:self.current]
    
    def nextChar(self):
        return self.charAt(self.current)
    
    def charAt(self, index):
        return self.source[index:index + 1]
    
    def isValidTokenType(self, string):
        return string in [token_type.value for token_type in TokenType]

    def addToken(self, token_type, literal = None):
        string = self.currentString()
        self.tokens.append(Token(token_type, string, literal, self.line, self.start))
   
