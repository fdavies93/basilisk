# Basilisk Design Doc

Basilisk (working name) is a compiled, functional language which aims to take many Python conventions with regard to style and ease-of-use and make the language more suitable for large-scale applications and systems programming work.

A Basilisk program resembles Python, but with some modifications.

```
i32 fibonnaci(i32 term) {
    i32[2] terms = [1,1]
    i32 next_term = 1

    for _ in 2..term {
        next_term = terms[0] + terms[1]
        terms[0] = terms[1]
        terms[1] = next_term
    }

    return next_term
}

print("{}", fibonnaci(10))
```

## Language Features

* Static typing, not duck typing. This is needed for a reasonable attempt at a compiled language.
* Enforced pure functions. All variables are passed by reference or by copy in Basilisk, and cannot be modified once passed. Functions must return a different object to that which was passed in.
* No concept of objects or object-oriented programming. The abstractions of OOP tend to be confusing and brittle and Basilisk aims to be simple and flexible. Instead Basilisk uses *structs* and metaprogramming to do the work often handled by objects.
* Metaprogramming and code generation is a key feature of Basilisk, which lets declarations stay succinct while maintaining fast compiled programs, and enables some of the convenient syntax sugar of OOP without having a true object system.
    * Code generation must have clearly defined behaviour and outputs and where that's not possible users should be encouraged to write their own scripts which provide the behaviour they want.

## Language Design Resources

LMU language design notes:
https://cs.lmu.edu/~ray/notes/languagedesignnotes/

Antlr, Parser Generator:
https://www.antlr.org/

C syntax in BNF:
https://cs.wmich.edu/~gupta/teaching/cs4850/sumII06/The%20syntax%20of%20C%20in%20Backus-Naur%20form.htm

Harvard on BNF:
https://cs61.seas.harvard.edu/site/2021/BNFGrammars/

## Compiler Compiler Options

* YACC/Bison
* Antlr4
* LLVM (target intermediate representation; transpiles to common assembly langs)

## Reference Languages

* Python
* OCaml
* Rust
* Haskell
* Elixir
* Kanren Type-C
* MicroKanren
* Prolog
* Racket

## Possible Names

* Tanuki
* Kitsuni
* Basilisk