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
* No concept of objects or object-oriented programming. The abstractions of OOP tend to be confusing and brittle and Basilisk aims to be simple and flexible. Instead Basilisk uses *structs* and built-in functions to do the work often handled by objects.

## Language Design Resources

LMU language design notes:
https://cs.lmu.edu/~ray/notes/languagedesignnotes/