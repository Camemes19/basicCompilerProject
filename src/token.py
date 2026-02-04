from tokenType import TokenType

class Token:
    def __init__ (self, tokenText, tokenType):
        self.text = tokenText
        self.type = tokenType

    @staticmethod
    def isKeyword(tokText):
        for kind in TokenType:
            if kind.name == tokText and kind.value >= 100 and kind.value < 200:
                return kind
        return None