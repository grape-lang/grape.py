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