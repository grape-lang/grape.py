from decimal import *

from syntax.tokens import *
from syntax.callable import *

def printImpl(arguments: list, errorToken: Token) -> str:
    string = str(arguments[0])

    print(string.replace('\\n', '\n'), end='')
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

def lenImpl(arguments: list, errorToken: Token) -> Decimal:
    collection = arguments[0]

    if isinstance(collection, list):
        return round(Decimal(len(collection)), maxDecimals)
    else:
        raise ArgumentError(errorToken, "len() expects a collection (list or tuple).")
    

lenFn = Builtin("len", (1, ), lenImpl)

def elemImpl(arguments: list, errorToken: Token) -> any:
    collection = arguments[0]
    index = arguments[1]

    if isinstance(collection, list) and isinstance(index, Decimal):
        return collection[int(index)]
    else:
        raise ArgumentError(errorToken, "elem() expects a collection (list or tuple) and an index (number).")
    
elemFn = Builtin("elem", (2, ), elemImpl)

def appendImpl(arguments: list, errorToken: Token) -> any:
    collection = arguments[0]
    value = arguments[1]

    if isinstance(collection, list):
        return collection.append(value)
    else:
        raise ArgumentError(errorToken, "append() expects a collection (list or tuple) and a value to append to it")

appendFn = Builtin("append", (2, ), appendImpl)
