import sys

from lexer import *
from parser import *
from tokenType import TokenType

def main():
    print("Basic Compiler")

    if len(sys.argv) != 2:
        sys.exit("Error: Compiler needs source file as argument.")
    with open(sys.argv[1], 'r') as inputFile:
        source = inputFile.read()

    lexer = Lexer(source)
    parser = Parser(lexer)

    parser.program()
    print("Source file successfully parsed.")

main()