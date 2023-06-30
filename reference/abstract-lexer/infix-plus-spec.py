from enum import IntEnum
from lexer import AbstractLexer, Transition, TransitionFn
from argparse import ArgumentParser
from sys import argv

class InfixLexTypes(IntEnum):
    MINUS = 0
    OPEN_BRACKET = 1
    CLOSE_BRACKET = 2
    PLUS = 3
    MULTIPLY = 4
    DIVIDE = 5
    NUMBER = 6
    NEW_LINE = 7

# you can write a bespoke function which takes the content of the token
# and emits the correct thing

op_codes = {
    '-': InfixLexTypes.MINUS,
    '(': InfixLexTypes.OPEN_BRACKET,
    ')': InfixLexTypes.CLOSE_BRACKET,
    '+': InfixLexTypes.PLUS,
    '*': InfixLexTypes.MULTIPLY,
    '/': InfixLexTypes.DIVIDE,
    '\n': InfixLexTypes.NEW_LINE,
    '\r': InfixLexTypes.NEW_LINE
}

def push_operator(obj : AbstractLexer, next_char : str):
    obj.tokens.append( (op_codes[next_char], next_char) )

def push_number(obj : AbstractLexer, next_char : str):
    obj.tokens.append( (InfixLexTypes.NUMBER, obj.token) )

number_space = ( push_number, AbstractLexer.reset_token )
number_tuple = ( push_number, push_operator, AbstractLexer.reset_token )
number_eof = (push_number, AbstractLexer.reset_token )

transitions = {
            # all we care about is:
            # do we push the current accumulator? as what?
            # do we push the next token? as what?
            
            # change this so that we supply a list of atomic functions
            # which are executed on a given transition, rather than 
            # using predefined behaviours
            # PUSH should be append token, append accumulator, reset accumulator
            # ACCUMULATE should be append token to accumulator / tape
            "neutral": [
                (r'[\t ]','neutral', ()),
                (r'[\n\r]','neutral', push_operator), # i.e. do nothing
                (r'\(','neutral', push_operator), 
                (r'[0-9]','number', AbstractLexer.accumulate),
                (r'\.','number-dot', AbstractLexer.accumulate),
                (r'-','minus', push_operator),
                (r'#','comment',())
            ],
            "number": [
                (None, 'neutral', number_eof),
                (r'[\n\r]','neutral', number_tuple),
                (r'[ \t]','expect-operator', number_space),
                (r'[0-9]', 'number', AbstractLexer.accumulate),
                (r'\)', 'expect-operator', number_tuple),
                (r'[+*(/]','neutral', number_tuple),
                (r'\.','number-dot', AbstractLexer.accumulate),
                (r'-','minus', number_tuple),
                (r'#','comment', number_space)
            ],
            'number-dot': [
                (None, 'neutral', number_eof),
                (r'[\n\r]','neutral', number_tuple),
                (r'[ \t]','expect-operator', number_space),
                (r'[0-9]', 'number-dot', AbstractLexer.accumulate),
                (r'\)', 'expect-operator', number_tuple),
                (r'[+*(/]','neutral', number_tuple),
                (r'-','minus', number_tuple),
                (r'#','comment',number_space)
            ],
            'expect-operator': [
                # perhaps check if brackets have been closed correctly - neutral might be wrong state to go to
                (r'[\n\r]','neutral', push_operator),
                (r'[ \t]','expect-operator', ()),
                (r'[+*\(/]','neutral', push_operator),
                (r'-','minus', push_operator),
                (r'\)','expect-operator', push_operator),
                (r'#', 'comment', ())
            ],
            'minus': [
                # newline in the middle of a minus expression is INVALID
                (r'[ \t]','minus', ()), # i.e. do nothing
                (r'-','minus', push_operator),
                (r'\.','number-dot', AbstractLexer.accumulate),
                (r'[0-9]', 'number', AbstractLexer.accumulate)
                # comment after minus will lead to invalid code, therefore invalid
            ],
            'comment': [
                (r'[\n\r]','neutral',push_operator),
                (r'(?![\n\r])','comment',())
            ]
}

luthor = AbstractLexer(transitions, "neutral")

parser = ArgumentParser(prog="Infix Plus Lexer")
parser.add_argument('-i', '--input',action='store')

args = parser.parse_args(argv[1:])

if args.input:
    with open(args.input,'r') as f:
        file = f.read()
    tokens = luthor.lex(file)
    print(tokens)