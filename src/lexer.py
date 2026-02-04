from token import Token
from tokenType import TokenType
import sys

class Lexer:
    def __init__(self, source):
        self.source = source + '\n'
        self.curChar = ''
        self.curPos = -1
        self.nextChar()

    def nextChar(self):
        self.curPos += 1
        if self.curPos >= len(self.source):
            self.curChar = '\0'
        else:
            self.curChar = self.source[self.curPos]

    def peek(self):
        if self.curPos + 1 >= len(self.source):
            return '\0'
        return self.source[self.curPos + 1]

    def skipWhitespace(self):
        while self.curChar == ' ' or self.curChar == '\t' or self.curChar == '\r':
            self.nextChar()

    def abort(self, message):
        sys.exit(f"Lexing error: {message}")

    def skipComment(self):
        if self.curChar == '#':
            while self.curChar != '\n':
                self.nextChar()

    def getToken(self):
        token = None

        self.skipWhitespace()
        self.skipComment()

        if self.curChar == '+':
            token = Token(self.curChar, TokenType.PLUS)
        elif self.curChar == '-':
            token = Token(self.curChar, TokenType.MINUS)
        elif self.curChar == '*':
            token = Token(self.curChar, TokenType.ASTERISK)
        elif self.curChar == '/':
            token = Token(self.curChar, TokenType.SLASH)
        elif self.curChar == '=':
            if self.peek() == '=':
                lastChar = self.curChar
                self.nextChar()
                token = Token(lastChar + self.curChar, TokenType.EQEQ)
            else:
                token = Token(self.curChar, TokenType.EQ)
        elif self.curChar == '>':
            if self.peek() == '=':
                lastChar = self.curChar
                self.nextChar()
                token = Token(lastChar + self.curChar, TokenType.GTEQ)
            else:
                token = Token(self.curChar, TokenType.GT)
        elif self.curChar == '<':
            if self.peek() == '=':
                lastChar = self.curChar
                self.nextChar()
                token = Token(lastChar + self.curChar, TokenType.LTEQ)
            else:
                token = Token(self.curChar, TokenType.LT)
        elif self.curChar == '!':
            if self.peek() == '=':
                lastChar = self.curChar
                self.nextChar()
                token = Token(lastChar + self.curChar, TokenType.NOTEQ)
            else:
                self.abort(f"Expected !=, got !{self.peek()}")
        elif self.curChar == '\"':
            self.nextChar()
            startPos = self.curPos

            while self.curChar != '\"':
                if (self.curChar == '\r' or self.curChar == '\n' or self.curChar == '\t' or self.curChar == '\\' or
                        self.curChar == '%'):
                    self.abort("Illegal character in string.")
                self.nextChar()

            tokText = self.source[startPos : self.curPos]
            token = Token(tokText, TokenType.STRING)
        elif self.curChar.isdigit():
            startPos = self.curPos
            while self.peek().isdigit():
                self.nextChar()
            if self.peek() == '.':
                self.nextChar()

                if not self.peek().isdigit():
                    self.abort("Illegal character in number.")
                while self.peek().isdigit():
                    self.nextChar()

            tokText = self.source[startPos : self.curPos + 1]
            token = Token(tokText, TokenType.NUMBER)
        elif self.curChar.isalpha():
            startPos = self.curPos
            while self.peek().isalnum():
                self.nextChar()

            tokText = self.source[startPos : self.curPos + 1]
            keyword = Token.isKeyword(tokText)
            if keyword == None:
                token = Token(tokText, TokenType.IDENT)
            else:
                token = Token(tokText, keyword)
        elif self.curChar == '\n':
            token = Token(self.curChar, TokenType.NEWLINE)
        elif self.curChar == '\0':
            token = Token(self.curChar, TokenType.EOF)
        else:
            # Unknown Token, throw error and abort
            self.abort(f"Unknown token: {self.curChar}")

        self.nextChar()
        return token