from infix import InfixLexer, InfixParser, evaluate

luthor = InfixLexer()
tokens = luthor.lex("(10 + 10) ^ 3 - (10 + 10)")
print(tokens)

parser = InfixParser()
ast = parser.parse(tokens)
# print(dumps(asdict(ast), indent=2))

print(evaluate(ast))