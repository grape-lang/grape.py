from decimal import *
from syntax.tokens import *

class Scanner:
    def __init__(self, grape, source: str): 
        self.tokens = []
        self.start = 0
        self.current = 0
        self.line = 1
        self.errorHandler = grape.errorHandler
        self.source = source

    def scanTokens(self) -> list[Token]:
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
                pass # Ignore whitespace

            case "\n":
                self.addToken(TokenType.NEWLINE)
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
            self.errorHandler.report("Syntax error", self.line, self.start, truncateString(self.currentString()), "Unterminated string")
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
        global maxDecimals

        while self.peek().isdigit(): self.advance()
        currentDecimal = 0

        if self.peek() == "." and self.doublePeek().isdigit():
            self.advance()
            while self.peek().isdigit(): 
                self.advance()
                currentDecimal += 1

        if currentDecimal > maxDecimals:
            self.errorHandler.warn(self.line, "The max amount of decimals is " + str(maxDecimals) + ". Your value is being rounded up.")
        
        self.addToken(TokenType.NUMBER, round(Decimal(self.currentString()), 3))

    def isAtomChar(self, c: str) -> bool:
        return c in charRange("A", "Z") or c == "@"

    def isIdentifierChar(self, c: str) -> bool:
        return self.isAlpha(c)

    def handleAtom(self):
        while self.isAlphaNumeric(self.peek()): self.advance()

        literal = self.currentString()
        self.addToken(TokenType.ATOM, literal)

    def handleIdentifier(self):
        while self.isAlphaNumeric(self.peek()): self.advance()

        currentString = self.currentString()
        if self.isValidTokenType(currentString):
            self.addToken(TokenType(currentString))
            return

        self.addToken(TokenType.IDENTIFIER)

    def isAlpha(self, c: str) -> bool:
        return c in charRange("a", "z") or c == "_"

    def isAlphaNumeric(self, c: str) -> bool:
        return self.isAlpha(c) or c.isdigit()

    def syntaxError(self, unexpectedString: str = "", message: str = "") -> None:
        if unexpectedString != "":
            message = "Unexpected \"" + unexpectedString + "\". " + message

        self.errorHandler.report("Syntax error", self.line, self.current, "", message)

    def advance(self) -> str:
        self.current += 1
        return self.currentString()

    def match(self, expected: str) -> bool:
        if self.isAtEnd(): return False
        if self.nextChar() != expected: return False

        self.current += 1
        return True

    def peek(self) -> str:
        if self.isAtEnd(): return '\0';
        return self.nextChar()    
    
    def doublePeek(self) -> str:
        afterNextChar = self.current + 1

        if afterNextChar >= len(self.source): return "\0"
        return self.charAt(afterNextChar)

    def currentString(self) -> str:
        return self.source[self.start:self.current]
    
    def nextChar(self) -> str:
        return self.charAt(self.current)
    
    def charAt(self, index: int) -> str:
        return self.source[index:index + 1]
    
    def isValidTokenType(self, string: str) -> bool:
        return string in [token_type.value for token_type in TokenType]

    def addToken(self, token_type: TokenType, literal: any = None) -> None:
        string = self.currentString()
        self.tokens.append(Token(token_type, string, literal, self.line, self.start))

def charRange(start: str, stop: str) -> range:
    return (chr(n) for n in range(ord(start), ord(stop) + 1))

def truncateString(string: str, length: int = 6) -> str:
    string = string.split("\n")[0]
    return (string[:length] + '..') if len(string) > length else string