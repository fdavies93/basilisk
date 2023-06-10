# Infix Parser Reference

This is a parser & lexer for infix algebra which I wrote as a reference for future projects. Also included is a BNF grammar for infix algebra.

It can handle all standard one-character operations (`+`, `-`, `/`, `*`, `^`) as well as brackets and expressions using a unary `-`.

One peculiarity of this parser is that it interprets all `-` signs as unary `-`. Expressions like `10 - 10` are lexed to `10 + -10`. One consequence of this is that addition and subtraction have equal precedence: i.e. `10 + 10 - 10 + 10` will evaluate to `20`, not `30`. **This is mathematically correct but may not fit with your intuitions from middle school math.**

I believe that this is an LR(1) parser in technical terms. While it does use recursion to simplify the code (bad) it could be implemented as a simple stack and a previous attempt did so.