[![progress-banner](https://backend.codecrafters.io/progress/interpreter/220eae1d-96e7-4498-881d-5c4161ee5dcf)](https://app.codecrafters.io/users/codecrafters-bot?r=2qF)

# Python Lox Interpreter

This repository is a starting point for the "Build Your Own Interpreter" challenge, inspired by the book Crafting
Interpreters by Robert Nystrom. The challenge involves building a fully functioning interpreter for the Lox scripting
language from scratch. Along the way, you'll learn about concepts like tokenization, Abstract Syntax Trees (ASTs),
recursive descent parsers, and more.

## Challenge Overview

The project follows the structure and exercises from the entire book, guiding you through each stage of interpreter
design, starting from Chapter 4: Scanning all the way to the final stages of building a full-featured interpreter. The
challenge includes:

* Scanning and Tokenization
* Parsing expressions and statements
* Building Abstract Syntax Trees (AST)
* Implementing a tree-walk interpreter
* Handling control flow, functions, and classes
* Extending the interpreter with error handling, and more

## Project Structure

* Scanner: Responsible for tokenizing Lox source code into lexemes (e.g., keywords, operators, literals).
* Parser: Implements a recursive descent parser, transforming token sequences into AST nodes (Binary, Unary, Literal,
  Grouping).
* Interpreter: Walks the AST to evaluate expressions and execute statements.
* Error Handling: Gracefully reports errors during scanning and parsing without halting the process.
* ASTPrinter, Expr class: Implementing Visitor programming pattern which allows to add new Expressions effectively
* UnitTesting: I also decided to practice in unit testing my main classes, so this project have some.
* Lox: Interpreter framework class, handles errors, delegates tasks depending on command, entering point for the app.
* tools: Contains a script.py to automatically build Expr.py with Expr Children if we need more Expressions to be
  implemented in Visitor pattern.

## Prerequisites

Before starting, make sure you've read the introductory chapters of Crafting Interpreters:

* [Introduction (Chapter 1)](https://craftinginterpreters.com/introduction.html)
* [A Map of the Territory (Chapter 2)](https://craftinginterpreters.com/a-map-of-the-territory.html)
* [The Lox Language (Chapter 3)](https://craftinginterpreters.com/the-lox-language.html)
  These chapters provide important background on interpreter design and the Lox language itself.

## Key Concepts

* **Tokenization:** Breaking down Lox source code into tokens such as keywords, symbols, and literals.
* **AST:** Abstract Syntax Tree, representing the structure of expressions and statements in the code.
* **Recursive Descent Parsing:** A top-down approach to parsing the token stream into meaningful constructs.
* **Visitor Pattern:** Used to separate operations from the AST, allowing easy extension of the interpreter's
  functionality.
* **Tree-walk Interpreter:** Evaluates the AST by visiting each node in a depth-first traversal using the Visitor
  pattern.
* **Error Handling:** Graceful error reporting without breaking the scanning or parsing process.
* **Unit Testing:** Ensures that components like the scanner, parser, and interpreter are working correctly.

## Resources

Crafting Interpreters by Robert Nystrom

Codecrafters.io - Try the challenge online.

# How to install and run

1. Ensure you have `python (3.12)` installed locally
2. Clone this repository `git clone https://github.com/cvrs3d/lox_interpreter.git`
3. Open terminal and print `cd python-lox-interpreter`
4. Then run `pipenv install`
5. Run unittests `pipenv run python -m unittest discover`
6. Finally run `pipenv run python main.py tokenize yourfile.lox`
