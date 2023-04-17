import term

class Repl:
    currentLine = 1
    prompt = "=> "

    def input(self) -> str:
        match self.askForInput():
            case "": self.input()
            case line:
                self.currentLine += 1
                return line

    def askForInput(self) -> str:
        return input(str(self.currentLine) + self.prompt) + "\n"
            
class ErrorHandler:
    hadError = False

    def report(self, kind: str, line: int, location: str, message: str = "") -> str: 
        self.hadError = True
        header = "[line " + str(line) + "]"
        error = kind + " at " + str(location)

        if message:
            error += ": " + message
    
        print(term.colors.FAIL + header + " " + error + term.colors.NORMAL)
        return error
    
    def warn(self, line: int, message: str) -> str: 
        header = "[line " + str(line) + "]"
        message = message.lower()    
        
        print(term.colors.WARNING + header + " " + message + term.colors.NORMAL)
        return message
