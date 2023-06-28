from enum import IntEnum
import re

class LexBehaviour(IntEnum):
    ACCUMULATE = 0,
    PUSH = 1

class AbstractLexer():
    def __init__(self):
        self.ignore = '\n\r\t '
        self.token = ''
        self.tokens = []
        self.last_instruction = LexBehaviour.PUSH
        self.transitions = {
            "neutral": [
                (r'\(','neutral',LexBehaviour.PUSH), 
                (r'[0-9]','number', LexBehaviour.ACCUMULATE),
                (r'\.','number-dot', LexBehaviour.ACCUMULATE),
                (r'-','minus', LexBehaviour.PUSH)
            ],
            "number": [
                (r'[0-9]', 'number', LexBehaviour.ACCUMULATE),
                (r'\)', 'expect-operator', LexBehaviour.PUSH),
                (r'[+*(/]','neutral', LexBehaviour.PUSH),
                (r'\.','number-dot', LexBehaviour.ACCUMULATE),
                (r'-','minus', LexBehaviour.PUSH)
            ],
            'number-dot': [
                (r'[0-9]', 'number-dot', LexBehaviour.ACCUMULATE),
                (r'\)', 'expect-operator', LexBehaviour.PUSH),
                (r'[+*(/]','neutral', LexBehaviour.PUSH),
                (r'-','minus', LexBehaviour.PUSH)
            ],
            'expect-operator': [
                (r'[+*\(/]','neutral', LexBehaviour.PUSH),
                (r'-','minus', LexBehaviour.PUSH),
                (r'\)','expect-operator', LexBehaviour.PUSH)
            ],
            'minus': {
                (r'[+*\(/]','neutral', LexBehaviour.PUSH),
                (r'-','minus', LexBehaviour.PUSH),
                (r'\.','number-dot', LexBehaviour.ACCUMULATE),
                (r'[0-9]', 'number', LexBehaviour.ACCUMULATE)
            }
        }
        self.state = "neutral"

    def reset(self):
        self.token = ''
        self.tokens = []

    def step(self, next_char : str):
        if next_char in self.ignore:
            return

        for expr in self.transitions.get(self.state):
            if re.match(expr[0], next_char) != None:
                self.state = expr[1]
                self.last_instruction = expr[2]
                if expr[2] == LexBehaviour.PUSH:
                    if len(self.token) > 0:
                        self.tokens.append(self.token)
                    self.token = ''
                    self.tokens.append(next_char)
                    return
                elif expr[2] == LexBehaviour.ACCUMULATE:
                    self.token += next_char
                    return

        raise ValueError
    
    def lex(self, input : str):
        self.reset()
        for char in input:
            self.step(char)

        if self.last_instruction == LexBehaviour.ACCUMULATE:
            self.tokens.append(self.token)
        
        return self.tokens
    
luthor = AbstractLexer()
tokens = luthor.lex("10 + 10 + (5 / 5 - 10) + 10 / -10.581")
print(tokens)