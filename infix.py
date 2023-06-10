from enum import IntEnum
from dataclasses import dataclass
from copy import deepcopy
from typing import Callable, Union

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
        self.prev_token = None
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
        elif next_char == open_bracket:
            # the only valid operators to start an expression are - or (
            self.tokens.append(next_char)
            self.prev_token = next_char
            self.brackets_open += 1

        elif next_char == minus:
            self.step_fn = self.step_lexing_minus

        elif next_char in whitespace:
            # it's whitespace, do nothing
            pass
        else:
            # it's invalid, throw an error
            raise ValueError
        
        # this only happens where expression ends after an operator, which is invalid
        if len(self.tape) == 0:
            raise ValueError
        
    def step_lexing_minus(self):

        minuses = 1

        next_char = self.tape[0]
        self.tape = self.tape[1:]

        while (next_char == '-' or next_char in whitespace) and len(self.tape) > 0:
            if next_char == '-':
                minuses += 1
            next_char = self.tape[0]
            self.tape = self.tape[1:]

        if len(self.tape) == 0:
            # can't end input on a - sign
            raise ValueError()
        
        if self.prev_token not in {None, open_bracket}.union(adm):
            self.tokens.append('+')
            self.prev_token = '+'
            # if it WASN'T in that set then + is valid, so add it as an operator

        if not (minuses % 2) == 0:
            self.tokens.append('-')
            self.prev_token = '-'

        # this is identical to step_neutral_fn - move to own fn?
        if next_char in digits or next_char == dot:
            self.cur_token = next_char
            self.step_fn = self.step_lexing_number

        elif next_char == open_bracket:
            # the only valid operators to start an expression are - or (
            self.tokens.append(next_char)
            self.prev_token = next_char
            self.brackets_open += 1
            self.step_fn = self.step_neutral
        else:
            raise ValueError()
        

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
            self.prev_token = self.cur_token

            self.cur_token = ""

            if next_char == minus:
                self.step_fn = self.step_lexing_minus
                return

            self.tokens.append(next_char)
            self.prev_token = next_char   

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
            self.prev_token = self.cur_token

    def step_expect_operator(self):
        next_char = self.tape[0]
        self.tape = self.tape[1:]

        if next_char in operators:
            if next_char == close_bracket:
                self.brackets_open -= 1
            
            elif next_char == minus:
                self.step_fn = self.step_lexing_minus
                return

            self.tokens.append(next_char)
            self.prev_token = next_char

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

@dataclass
class ParseNode():
    token : str
    children : list["ParseNode"]

    def __eq__(self, other):
        if isinstance(other, ParseNode) and other.token == self.token:
            return True
        elif isinstance(other, str) and other == self.token:
            return True
        
        return False

class InfixParser():

    # run through each parsing step in turn, by the same process
    # bracketise
    # identify and simplify unary minus
    # multiply
    # divide
    # add
    # subtract

    def __init__(self):
        self.operations = [
            lambda ls : InfixParser.pbo("*", ls),
            lambda ls : InfixParser.pbo("/", ls),
            InfixParser.parse_unary_minus,
            lambda ls : InfixParser.pbo("+", ls),
        ]

    @classmethod
    def parse_unary_minus(cls, tokens: list[Union[str, ParseNode]]) -> list[Union[str, ParseNode]]:
        i = 0
        out_list = []
        while i < len(tokens):
            if tokens[i] == '-':
                out_list.append(ParseNode('-', [tokens[i+1]]))
                i += 1 # so that we step forward TWO
            else:
                out_list.append(tokens[i])
            i += 1
        return out_list

    # pbo stands for Parse Binary Operator
    @classmethod
    def pbo(cls, operator : str, tokens: list[Union[str, ParseNode]]) -> list[Union[str, ParseNode]]:
        i = 0
        out_list = deepcopy(tokens)
        while i < len(out_list):
            if out_list[i] == operator and isinstance(out_list[i],str):
                new_list : list = out_list[:i-1]
                new_list.append(ParseNode(operator, [out_list[i-1], out_list[i+1]]))
                new_list.extend(out_list[i+2:])
                print(new_list)
                out_list = new_list
                i = 0
            # elif tokens[i] in adm:
            #     out_list.extend(tokens[i - 1 : i + 1])
            i += 1
        return out_list

    # should return the root of an AST
    def parse(self, tokens : list[str]) -> ParseNode:
        if len(tokens) == 0:
            return None
        # bracketise, then do other operations

        cur_list : list = deepcopy(tokens)
        inner = None

        cur_i = 0
        while cur_i < len(cur_list):
            token = cur_list[cur_i]
            if token == '(':
                # recurse, using list after bracket
                inner = self.parse( cur_list[cur_i + 1 :] )
                cur_list = cur_list[ : cur_i]
                cur_list.extend(inner)
                cur_i = 0

            elif token == ")":
                # we've reached the innermost statement of expression
                # take the whole expression and parse it according to
                # operator precedence
                out_list = cur_list[: cur_i]

                for operation in self.operations:
                    out_list = operation(out_list)

                out_list.extend( cur_list[cur_i + 1 :] )

                return out_list
            
            else: cur_i += 1

        for operation in self.operations:
            cur_list = operation(cur_list)
            # print(cur_list)

        return cur_list[0]

def evaluate(node):
    ops = {
        '+' : lambda x, y : x + y,
        '/' : lambda x, y : x / y,
        '*' : lambda x, y : x * y
    }
    if isinstance(node, str):
        return float(node)
    elif isinstance(node, ParseNode):
        if node.token in adm:
            left = evaluate(node.children[0])
            right = evaluate(node.children[1])
            return ops[node.token](left, right)
        elif node.token == minus:
            return evaluate(node.children[0]) * -1

luthor = InfixLexer()
tokens = luthor.lex("((100 / 6) + 20 * 5) / (10 * 100)")
print(tokens)

parser = InfixParser()
ast = parser.parse(tokens)
print(ast)

print(evaluate(ast))