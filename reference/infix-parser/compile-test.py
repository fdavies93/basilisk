from infix import InfixLexer, InfixParser, compile

luthor = InfixLexer()
parser = InfixParser()

input_str = "(10 * 10) / 5 + 10 + 9 + 8 + 7 + 6 + 5 * 5"

try:
    tokens = luthor.lex(input_str)
    ast = parser.parse(tokens)
    compile(ast, "asm.ll")
except ValueError:
    print("Oops, that wasn't a valid input. Try again.")