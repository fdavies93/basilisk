from enum import IntEnum
from dataclasses import dataclass

digits = [chr(i) for i in range(48,58)] # digits by char code
whitespace = [' ', '\n', '\r', '\t'] # ignore
open_bracket = '('
close_bracket = ')'
adm = ['+', '/', '*']
minus = '-'
dot = '.'

operators = [open_bracket, close_bracket, minus]
operators.extend(adm)

class InfixLexer:
    def __init__(self):
        self.reset()

    def reset(self):
        self.tape = ""
        self.tokens = []
        self.cur_token = ""
        self.has_dot = False
        self.step_fn = self.step_neutral
        self.brackets_open = 0

    def step_neutral(self):
        next_char = self.tape[0]
        self.tape = self.tape[1:]

        if next_char in digits or next_char == dot:
                # it's a number
                self.cur_token = next_char
                self.step_fn = self.step_lexing_number
        elif next_char in {minus, open_bracket}:
            # the only valid operators to start an expression are unary - or (
            self.tokens.append(next_char)
            if next_char == open_bracket:
                self.brackets_open += 1

        elif next_char in whitespace:
            # it's whitespace, do nothing
            pass
        else:
            # it's invalid, throw an error
            raise ValueError

    def step_lexing_number(self):
        next_char = self.tape[0]
        self.tape = self.tape[1:]

        if next_char in digits:
            self.cur_token += next_char

        elif next_char == dot and not self.has_dot:
            self.has_dot = True
            self.cur_token += next_char

        elif next_char in operators:
            self.has_dot = False
            self.tokens.append(self.cur_token)
            self.tokens.append(next_char)
            self.cur_token = ""
            self.step_fn = self.step_neutral
            if next_char == close_bracket:
                self.brackets_open -= 1
                self.step_fn = self.step_expect_operator

        elif next_char in whitespace:
            pass
        
        else:
            raise ValueError
        
        if len(self.tape) == 0 and self.cur_token != "":
            self.tokens.append(self.cur_token)

    def step_expect_operator(self):
        next_char = self.tape[0]
        self.tape = self.tape[1:]
        if next_char in operators:
            if next_char == close_bracket:
                self.brackets_open -= 1

            self.tokens.append(next_char)
            self.step_fn = self.step_neutral
        elif next_char in whitespace:
            return
        else:
            raise ValueError

    def lex(self, input : str):
        self.reset()
        self.tape = input

        while len(self.tape) > 0:
            self.step_fn()
        
        if self.brackets_open != 0:
            raise ValueError("Mismatched brackets in expression.")

        return self.tokens

class InfixParser():


    def parse(self, tokens : list[str]):
        if len(tokens) == 0:
            return 0
        

luthor = InfixLexer()
tokens = luthor.lex("(((10 + 10) * -5.32 * 20 + 5))")
print(tokens)