# PROJECT: idDL2DL

The implementation of **idDL2dDL** is structured in four parts, namely the *lexer*, the *parser*, the *translator* and
the graphical user interface.

1. The lexer, as the name suggests, performs the lexical analysis of the expressions provided as input, which is the
   process of converting a sequence of characters into *tokens*.
2. The parser is then called to perform a syntactic analysis over these tokens, and returns an abstract syntax tree (
   AST) as output.
3. The translator is fed an AST as input, and returns a translated string as output. This is achieved by *visit*
   methods, whose purpose is to enter a node of the AST and perform a proper evaluation and translation of its contents.
4. The rudimentary GUI compiles the functionality of the aforementioned modules in a page for user inputed
   translation, and in a page for loading files with translatable formulas, in order to provide the user a simple way of
   performing translations.

Structure of the program follows [this](https://github.com/davidcallanan/py-myopl-code) respository.

**Early version of the software, any bugs please open an issue.**

## How to run in console

Navigate to **/Interval** folder and run `python main`.

Type *help* for commands.

A single translation can be made by simply typing the desired formula in this program's syntax (check examples to learn
more).

## GUI
**_!UNDER CONSTRUCTION!_**

Navigate to **/Interval/GraphicalInterface** and run
`python GInterface`.
<img src="/Resources/basicGUI.png" width="500" height="400">

