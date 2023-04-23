from decimal import *

from syntax.tokens import *
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

def lenImpl(interpreter, errorToken: Token, arguments: list):
    return round(Decimal(len(arguments[0])), maxDecimals)

lenFn = Callable("len", (1, ), lenImpl)