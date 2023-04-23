#!/usr/bin/env python3

import sys
import runtime.debug as debug
from runtime.repl import Repl
from runtime.error_handler import ErrorHandler
from compiler import Scanner
from compiler import Parser
from compiler import Interpreter

class Grape:
    def __init__(self):
        self.debug = False
        self.errorHandler = ErrorHandler()

    def runFile(self, filename: str):
        source_code = open(filename, "r").read()
        self.run(source_code)

    def startREPL(self):
        repl = Repl()
        while True:
            line = repl.input()
            self.run(line)
            self.errorHandler.hadError = False

    def run(self, source: str): 
        scanner = Scanner(self, source)
        tokens = scanner.scanTokens()

        if self.debug: debug.printTokens(tokens)

        parser = Parser(self, tokens)
        statements = parser.parse()

        if self.debug: debug.printStatements(statements)

        if self.errorHandler.hadError: return
        elif self.debug: debug.printRunning()
        
        interpreter = Interpreter(self, statements)
        interpreter.interpret()

        if self.debug:
            if self.errorHandler.hadError:
                debug.printError()
            else:
                debug.printDone()

def description() -> None:
    print("A general purpose programming language made for rapid-pase prototyping.")
    print("")

def usage(binaryName: str) -> None:
    print("Usage: ")
    print("     " + binaryName + " [options] [path]")
    print("")
    print("OPTIONS:")
    print("     --help: print this help")
    print("")


def cjop(list: list) -> tuple[any, list]:
    return (list[0], list[1:])

if __name__ == "__main__":
    grape = Grape()
    (binaryName, argv) = cjop(sys.argv)
    
    if len(argv) >= 2:
        grape.errorHandler.error(0, 0, "Too many arguments provided")
        usage(binaryName)
        exit(64)

    elif len(argv) == 1:
        match argv[0]:
            case "--help":
                description()
                usage(binaryName)

            case filePath:
                grape.runFile(sys.argv[1])
                if grape.errorHandler.hadError: exit(65)

    else:
        grape.startREPL()

