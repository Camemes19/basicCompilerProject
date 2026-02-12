import sys
from lexer import Lexer
from emitter import Emitter
from token import Token
from tokenType import TokenType

class Parser:
    def __init__(self, lexer, emitter):
        self.lexer = lexer
        self.emitter = emitter

        self.symbols = set()
        self.labelsDeclared = set()
        self.labelsGotoed = set()

        self.curToken = None
        self.peekToken = None
        self.nextToken()
        self.nextToken()

    def checkToken(self, type):
        return type == self.curToken.type

    def checkPeek(self, type):
        return type == self.peekToken.type

    def match(self, type):
        if not self.checkToken(type):
            self.abort(f"Expected {type.name}, got {self.curToken.type.name}")
        self.nextToken()

    def nextToken(self):
        self.curToken = self.peekToken
        self.peekToken = self.lexer.getToken()

    def abort(self, message):
        sys.exit(f"Error: {message}")

    def program(self):
        print("PROGRAM")
        self.emitter.headerLine("#include <stdio.h>")
        self.emitter.headerLine("int main(void) {")

        while self.checkToken(TokenType.NEWLINE):
            self.nextToken()

        while not self.checkToken(TokenType.EOF):
            self.statement()

        self.emitter.emitLine("return 0;")
        self.emitter.emitLine("}")

        for label in self.labelsGotoed:
            if label not in self.labelsDeclared:
                self.abort(f"Cannot GOTO undeclared label: {label}")

    def statement(self):
        if self.checkToken(TokenType.PRINT):
            print("STATEMENT-PRINT")
            self.nextToken()

            if self.checkToken(TokenType.STRING):
                self.emitter.emitLine(f"printf(\"{self.curToken.text}\\n\");")
                self.nextToken()
            else:
                self.emitter.emit(f"printf(\"%.2f\\n\", (float)(")
                self.expression()
                self.emitter.emitLine("));")
        elif self.checkToken(TokenType.IF):
            print("STATEMENT-IF")
            self.nextToken()
            self.emitter.emit("if(")
            self.comparison()

            self.match(TokenType.THEN)
            self.nl()
            self.emitter.emitLine(") {")

            while not self.checkToken(TokenType.ENDIF):
                self.statement()

            self.match(TokenType.ENDIF)
            self.emitter.emitLine("}")
        elif self.checkToken(TokenType.WHILE):
            print("STATEMENT-WHILE")
            self.nextToken()
            self.emitter.emit("while(")
            self.comparison()

            self.match(TokenType.REPEAT)
            self.nl()
            self.emitter.emitLine(") {")

            while not self.checkToken(TokenType.ENDWHILE):
                self.statement()

            self.match(TokenType.ENDWHILE)
            self.emitter.emitLine("}")
        elif self.checkToken(TokenType.LABEL):
            print("STATEMENT-LABEL")
            self.nextToken()

            if self.curToken.text in self.labelsDeclared:
                self.abort(f"Label {self.curToken.text} already exists")
            self.labelsDeclared.add(self.curToken.text)

            self.match(TokenType.IDENT)
        elif self.checkToken(TokenType.GOTO):
            print("STATEMENT-GOTO")
            self.nextToken()
            self.labelsGotoed.add(self.curToken.text)
            self.match(TokenType.IDENT)
        elif self.checkToken(TokenType.LET):
            print("STATEMENT-LET")
            self.nextToken()

            if self.curToken.text not in self.symbols:
                self.symbols.add(self.curToken.text)

            self.match(TokenType.IDENT)
            self.match(TokenType.EQ)
            self.expression()
        elif self.checkToken(TokenType.INPUT):
            print("STATEMENT-INPUT")
            self.nextToken()

            if self.curToken.text not in self.symbols:
                self.symbols.add(self.curToken.text)

            self.match(TokenType.IDENT)
        else:
            self.abort(f"Invalid statement at {self.curToken.text} ({self.curToken.type.name})")

        self.nl()

    def comparison(self):
        print("COMPARISON")
        self.expression()

        if self.isComparisonOperator():
            self.nextToken()
            self.expression()
        else:
            self.abort(f"Expected comparison operator at: {self.curToken.text}, was type {self.curToken.type}")

        while self.isComparisonOperator():
            self.nextToken()
            self.expression()

    def isComparisonOperator(self):
        return 206 <= self.curToken.type.value <= 212

    def expression(self):
        print("EXPRESSION")
        self.term()

        while self.checkToken(TokenType.PLUS) or self.checkToken(TokenType.MINUS):
            self.nextToken()
            self.term()

    def term(self):
        print("TERM")
        self.unary()

        while self.checkToken(TokenType.ASTERISK) or self.checkToken(TokenType.SLASH):
            self.nextToken()
            self.unary()

    def unary(self):
        print("UNARY")

        if self.checkToken(TokenType.PLUS) or self.checkToken(TokenType.MINUS):
            self.nextToken()
        self.primary()

    def primary(self):
        print(f"PRIMARY ({self.curToken.text})")

        if self.checkToken(TokenType.NUMBER):
            self.nextToken()
        elif self.checkToken(TokenType.IDENT):
            if self.curToken.text not in self.symbols:
                self.abort(f"Undeclared variable: {self.curToken.text}")
            self.nextToken()
        else:
            self.abort(f"Unexpected token at {self.curToken.text}")

    def nl(self):
        print("NEWLINE")

        self.match(TokenType.NEWLINE)
        while self.checkToken(TokenType.NEWLINE):
            self.nextToken()