import sys
from runtime import Repl
from runtime import ErrorHandler
from compiler import Scanner
from compiler import Parser

class Grape:
    def __init__(self):
        self.errorHandler = ErrorHandler()

    def runFile(self, filename):
        source_code = open(filename, "r").read()
        self.run(source_code)

    def startREPL(self):
        repl = Repl()
        while True:
            line = repl.input()
            self.run(line)
            self.errorHandler.hadError = False

    def run(self, source): 
        scanner = Scanner(self, source)
        tokens = scanner.scanTokens()

        # for token in tokens:
        #     print(token)

        parser = Parser(self, tokens)
        expression = parser.parse()

        if self.errorHandler.hadError: return
        print(expression)

if __name__ == "__main__":
    grape = Grape()
    
    if len(sys.argv) > 2:
        print("Usage: grape [script]")
        exit(64)

    elif len(sys.argv) == 2:
        grape.runFile(sys.argv[1])

        if grape.errorHandler.hadError: 
            exit(65)

        exit()

    else:
        grape.startREPL()
