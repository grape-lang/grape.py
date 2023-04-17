import runtime.term as term

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
