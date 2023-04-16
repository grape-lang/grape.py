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
        header = "[line " + str(line) + "]"
        error = kind + " at " + str(col)

        if message:
            error += ": " + message
    
        print(term.colors.FAIL + header + " " + error + term.colors.NORMAL)
        return error
    
    def warn(self, line, message): 
        header = "[line " + str(line) + "]"
        message = message.lower()    
        
        print(term.colors.WARNING + header + " " + message + term.colors.NORMAL)
