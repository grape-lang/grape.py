import runtime.term as term

class ErrorHandler:
    hadError = False

    def report(self, kind: str, line: int, col: int, location: str = "", message: str = "") -> str: 
        self.hadError = True
        
        errorMessage = kind
        
        if location and location != "":
            errorMessage += " at " + str(location)

        if message and message != "":
            errorMessage += ": " + message
    
        self.error(line, col, errorMessage)
        return errorMessage
    
    def error(self, line: int, col: int, message: str) -> str:
        header = "[line " + str(line) + ":" + str(col) + "]"
        print(term.colors.FAIL + header + " " + message + term.colors.NORMAL)
    
    def warn(self, line: int, col: int, message: str) -> str: 
        header = "[line " + str(line) + ":" + str(col) + "]"
        warningMessage = message.lower()    
        
        print(term.colors.WARNING + header + " " + warningMessage + term.colors.NORMAL)
        return warningMessage
