import runtime.term as term

class ErrorHandler:
    hadError = False

    def report(self, kind: str, line: int, col: int, location: str = "", message: str = "") -> str: 
        self.hadError = True
        header = "[line " + str(line) + ":" + str(col) + "]"
        errorMessage = kind
        
        if location and location != "":
            errorMessage += " at " + str(location)

        if message and message != "":
            errorMessage += ": " + message
    
        print(term.colors.FAIL + header + " " + errorMessage + term.colors.NORMAL)
        return errorMessage
    
    def warn(self, line: int, message: str) -> str: 
        header = "[line " + str(line) + "]"
        warningMessage = message.lower()    
        
        print(term.colors.WARNING + header + " " + warningMessage + term.colors.NORMAL)
        return warningMessage
