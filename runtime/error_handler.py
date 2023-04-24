import runtime.term as term

class ErrorHandler:
    hadError = False
    currentFile = "unknown"

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
        header = self.header(line, col)
        print(term.colors.FAIL + header + " " + message + term.colors.NORMAL)
    
    def warn(self, line: int, col: int, message: str) -> str: 
        header = self.header(line, col)
        warningMessage = message.lower()    
        
        print(term.colors.WARNING + header + " " + warningMessage + term.colors.NORMAL)
        return warningMessage
    
    def header(self, line: int, col: int) -> str:
        return "[" + self.currentFile + ":" + str(line) + ":" + str(col) + "]"
