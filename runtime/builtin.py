from decimal import *

from syntax.tokens import *
from syntax.callable import *

def printImpl(arguments: list, errorToken: Token, interpreter) -> str:
    string = str(arguments[0])

    print(string.replace('\\n', '\n'), end='')
    return string

printFn = Builtin("print", (1, ), printImpl)

def exitImpl(arguments: list, errorToken: Token, interpreter):
    if len(arguments) == 1:
        exitCode = arguments[0] 
        if isinstance(exitCode, Decimal):
            exit(int(exitCode))
        else:
            raise ArgumentError(errorToken, "exit() expects either no arguments or a number.")
    else:
        exit()

exitFn = Builtin("exit", (0, 1), exitImpl)

def lenImpl(arguments: list, errorToken: Token, interpreter) -> Decimal:
    collection = arguments[0]

    if isinstance(collection, list):
        return round(Decimal(len(collection)), maxDecimals)
    else:
        raise ArgumentError(errorToken, "len() expects a collection (list or tuple).")
    

lenFn = Builtin("len", (1, ), lenImpl)

def elemImpl(arguments: list, errorToken: Token, interpreter) -> any:
    collection = arguments[0]
    index = arguments[1]

    if isinstance(collection, list) and isinstance(index, Decimal):
        if len(collection) > index:
            return collection[int(index)]
        else:
            raise ArgumentError(errorToken, "index out of range. List has " + str(len(collection)) + " items and you tried to access " + str(int(index) + 1) + "th item.")
    else:
        raise ArgumentError(errorToken, "elem() expects a collection (list or tuple) and an index (number).")
    
elemFn = Builtin("elem", (2, ), elemImpl)

def appendImpl(arguments: list, errorToken: Token, interpreter) -> any:
    collection = arguments[0]
    value = arguments[1]

    if isinstance(collection, list):
        collection = collection.copy()
        collection.append(value)
        return collection
    else:
        raise ArgumentError(errorToken, "append() expects a collection (list or tuple) and a value to append to it. Given: " + str(type(collection)))

appendFn = Builtin("append", (2, ), appendImpl)

def forImpl(arguments: list, errorToken: Token, interpreter) -> any:
    end = arguments[0]
    fun = arguments[1]
    acc = arguments[2].copy()

    if not isinstance(end, Decimal): 
        raise ArgumentError(errorToken, "for() expects a number as it's 1st argument. Given: " + str(type(end)))


    if not isinstance(fun, Callable): 
        raise ArgumentError(errorToken, "for() expects a function as it's 2nd argument. Given: " + str(type(fun)))
    
    if not isinstance(acc, list): 
        raise ArgumentError(errorToken, "for() expects a collection as it's 3rd argument. Given: " + str(type(acc)))

    for i in range(0..end):
        acc.append(fun.call(interpreter, [i], errorToken))

    return acc

forFn = Builtin("for", (2, ), forImpl)
