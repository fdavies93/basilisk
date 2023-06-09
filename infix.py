from enum import IntEnum
from dataclasses import dataclass

digits = [chr(i) for i in range(48,58)] # digits by char code
whitespace = [' ', '\n', '\r', '\t'] # ignore
open_bracket = '('
close_bracket = ')'
adm = ['+', '/', '*']
minus = '-'
dot = '.'

operators = [open_bracket, close_bracket, minus].extend(adm)

class LEX_TYPES(IntEnum):
    NONE = 0
    OPERATOR = 1
    MINUS = 2
    NUMBER = 3
    OPEN_BRACKET = 4
    CLOSE_BRACKET = 5

class LEX_STATE(IntEnum):
    NEUTRAL = 0
    PARSING_NUMBER = 1

@dataclass
class Token():
    token_type : LEX_TYPES
    content : str

class InfixLexer:
    def __init__(self):
        self.reset()

    def reset(self):
        self.input = input
        self.tokens = []
        self.state = LEX_STATE.NEUTRAL
        self.cur_token = ""

    def step(self):
        next_char = self.input[0]
        self.input = self.input[1:]
        if self.state == LEX_STATE.NEUTRAL:
            if next_char in digits or next_char == dot:
                # it's a number
                self.cur_token += next_char
                self.state = LEX_STATE.PARSING_NUMBER
            elif next_char in operators:
                # decide which class of operator it falls under and reset to neutral
                pass
            elif next_char in whitespace:
                # it's whitespace, do nothing
                return
            else:
                # it's invalid, throw an error
                raise ValueError

        elif self.state == LEX_STATE.PARSING_NUMBER:
            pass

    def lex(self, input : str):
        self.reset()

        while len(self.input) > 0:
            self.step()
        
        return self.tokens

print(ord("0"))
print(ord("9"))