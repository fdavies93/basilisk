from enum import IntEnum
from typing import Callable, Pattern
import re

class LexBehaviour(IntEnum):
    ACCUMULATE = 0,
    PUSH = 1

class AbstractLexer():
    def __init__(self, transitions : dict[str, list[tuple[Pattern,str,tuple[Callable[["AbstractLexer", str],None]]]]], start_state : str):
        self.ignore = '\n\r\t '
        self.token = ''
        self.tokens = []
        self.transitions = transitions
        self.state = start_state

    @classmethod
    def make_push_token_as(cls, output_int : int) -> Callable[["AbstractLexer", str],None]:
        # the obj passed is the lexer itself
        return lambda obj, next_char : obj.tokens.append( (output_int, obj.token) )

    @classmethod
    def accumulate(cls, obj : "AbstractLexer", next_char : str):
        obj.token += next_char

    @classmethod
    def reset_token(cls, obj : "AbstractLexer", next_char : str):
        obj.token = ""

    @classmethod
    def make_push_next_char_as(cls, output_int : int) -> Callable[["AbstractLexer", str],None]:
        return lambda obj, next_char : obj.tokens.append( (output_int, next_char) )

    def reset(self):
        self.token = ''
        self.tokens = []

    def step(self, next_char : str):
        if next_char in self.ignore:
            return

        for expr in self.transitions.get(self.state):
            if re.match(expr[0], next_char) != None:
                self.state = expr[1]
                # need a way to deal with last element (i.e. case where tape isn't empty)
                # check if expr[2] is a single callable function first and add to typing
                for fn in expr[2]:
                    fn(self,next_char)
                return

        raise ValueError
    
    def graphviz(self, outPath : str):
        lines = [
            'digraph fsm {',
            'fontname="Roboto,Arial,sans-serif"',
            'node [fontname="Roboto,Arial,sans-serif"]',
            'rankdir=LR;',
            'node [shape=circle];'
        ]
        for state in self.transitions:
            for transition in self.transitions[state]:
                lines.append(f'{state.replace("-","_")} -> {transition[1].replace("-","_")} ["label" = "{str(transition[0])}"];')
        lines.append('}')

        with open(outPath, "w") as f:
            for ln in lines:
                f.write(f"{ln}\n")

    def lex(self, input : str):
        self.reset()
        for char in input:
            self.step(char)

        if self.last_instruction == LexBehaviour.ACCUMULATE:
            # could use an explicit transition to EOF state in state definitions
            self.tokens.append(self.token)
        
        return self.tokens
    
luthor = AbstractLexer()
tokens = luthor.lex("10 + 10 + (5 / 5 - 10) + 10 / -10.581")
luthor.graphviz('./viz.gv')
print(tokens)