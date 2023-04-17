import runtime.term as term
from syntax.tokens import Token
from syntax.stmt import Stmt

def printTokens(tokens: list[Token]) -> None:
    print(formatSuccess("Scanned tokens:"))
    for token in tokens:
        print(token)
    
    print("")

def printStatements(statements: list[Stmt]) -> None:
    print(formatSuccess("Parsed statements (" + str(len(statements)) +"):"))
    for statement in statements:
        print(statement)

    print("")

def printRunning():
    print(formatSuccess("Running program"))

def printError():
    print(formatError("An error occured while running your program. Please check the stack trace above."))

def printDone():
    print("")
    print(formatSuccess("[DONE]"))

def formatSuccess(message: str) -> str:
    return formatHeading(term.colors.OK + "[OK] " + message)

def formatError(message: str) -> str:
    return formatHeading(term.colors.FAIL + "[ERROR] " + message)

def formatHeading(heading: str) -> str:
    return term.colors.BOLD + heading + term.colors.NORMAL