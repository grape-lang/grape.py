import term

class Repl:
    currentLine = 1
    prompt = " > "

    def input(self):
        line = input(str(self.currentLine) + self.prompt) 
        if line != "":
            self.currentLine += 1
            return line
        else:
            self.input()
            
class ErrorHandler:
    hadError = False

    def report(self, kind, line, col, message = ""): 
        self.hadError = True
        error = kind + " on line " + str(line) + " at " + str(col)

        if message:
            error += ": " + message
    
        print(term.colors.FAIL + error + term.colors.NORMAL)
        return error
