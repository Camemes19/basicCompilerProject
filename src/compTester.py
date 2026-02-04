from lexer import *
from tokenType import TokenType

def main():
    source = "+- */123 9.8654\"This is a string\" IF+-123 foo*THEN/#testing comment\n >>= = !="
    lexer = Lexer(source)

    token = lexer.getToken()
    while token.type != TokenType.EOF:
        print(token.type)
        token = lexer.getToken()

main()