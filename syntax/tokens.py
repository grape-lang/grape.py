from enum import Enum

maxDecimals = 3

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
    STAR = "*"
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
    IN = "in"
    FN = "fn"
    INSPECT = "inspect"
    EXIT = "exit"
    NAMESPACE = "namespace"
    IF = "if"
    ELSEIF = "elseif"
    ELSE= "else"
    USE = "use"
    DO = "do"
    END = "end"
    TRUE = "true"
    FALSE = "false"

    NEWLINE = 5
    EOF = 6

class Token:
    def __init__(self, token_type: TokenType, lexeme: str, literal: any, line: int, col: int):
        self.token_type = token_type
        self.lexeme = lexeme
        self.literal = literal
        self.line = line
        self.col = col

    def __str__(self) -> str:
        return str(self.token_type) + " " + str(self.lexeme) + " " + str(self.literal)
