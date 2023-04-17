from decimal import *
maxDecimals = 3

def debugPrintTokens(tokens):
    for token in tokens:
        print(token)

def charRange(start, stop):
    return (chr(n) for n in range(ord(start), ord(stop) + 1))