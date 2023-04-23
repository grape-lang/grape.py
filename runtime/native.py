from decimal import *

from syntax.tokens import *
from syntax.callable import *

def printImpl(arguments: list, errorToken: Token):
    string = str(arguments[0])

    print(string)
    return string

printFn = Builtin("print", (1, ), printImpl)

def exitImpl(arguments: list, errorToken: Token):
    if len(arguments) == 1:
        exitCode = arguments[0] 
        if isinstance(exitCode, Decimal):
            exit(int(exitCode))
        else:
            raise ArgumentError(errorToken, "exit() expects either no arguments or a number.")
    else:
        exit()

exitFn = Builtin("exit", (0, 1), exitImpl)

def lenImpl(arguments: list, errorToken: Token):
    return round(Decimal(len(arguments[0])), maxDecimals)

lenFn = Builtin("len", (1, ), lenImpl)