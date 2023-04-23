from decimal import *

from syntax.tokens import Token, TokenType
from syntax.callable import *

def printImpl(interpreter, errorToken: Token, arguments: list):
    print(str(arguments[0]))

printFn = Callable("print", (1, ), printImpl)

def exitImpl(interpreter, errorToken: Token, arguments: list):
    if len(arguments) == 1:
        exitCode = arguments[0] 
        if isinstance(exitCode, Decimal):
            exit(int(exitCode))
        else:
            raise ArgumentError(errorToken, "exit() expects either no arguments or a number.")
    else:
        exit()

exitFn = Callable("exit", (0, 1), exitImpl)