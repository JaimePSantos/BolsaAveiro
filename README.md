# PROJECT: idDL2DL

Provides the ability to convert from the interval notation of Differential Dynamic Logic (dDL), to regular Dynamic Logic formulas.

The implementation of **idDL2dDL** is structured in four parts, namely the *lexer*, the *parser*, the *translator* and
the graphical user interface.

1. The lexer performs the lexical analysis of the expressions provided as input, which is the
   process of converting a sequence of characters into *tokens*.
2. The parser is then called to perform a syntactic analysis over these tokens, and returns an abstract syntax tree (AST) as output.
3. The translator is fed an AST as input, and returns a translated string as output. This is achieved by *visit*
   methods, whose purpose is evaluate and translate the content of the nodes that compose the AST.
4. The rudimentary GUI compiles the functionality of the aforementioned modules in a an application that allows the user to either input the formulas directly, or load them from a file. The user is then able to save these translations as a single, or multiple `.kyx` files, ready to be used in [KeYmaera X](https://github.com/LS-Lab/KeYmaeraX-release). It also provides a page with the history of translated formulas.

Structure of the program follows [this](https://github.com/davidcallanan/py-myopl-code) respository.

**Early version of the software, any bugs please open an issue.**

## How to run in console

Navigate to `/idDL2DL/` folder and run `python main`.

Type *help* for commands.

A single translation can be made by simply typing the desired formula in this program's syntax (check examples to learn
more).

## GUI

**_UNDER CONSTRUCTION_**
### Pycharm (recommended)
Install [Pycharm](https://www.jetbrains.com/pycharm/), navigate to the `/idDL2DL/` folder and run `gui-main.py`  

### Alternative
You will need to add the project folder to your `$PYTHONPATH`, navigate to `/idDL2DL/` folder and `python gui-main.py`  

### Translation Page

<img src="/Resources/TranslationGUI.png" width="500">

#### Menu
- `File`: allows the user to
    - Load formulas to be translated. (`ctrl+l`)
    - Save the translated formulas to a file. (`ctrl+s`)
    - Exit the program. (`ctrl+q`)
- `Help`: allows the user to access
    - Program instructions. (*github readme*)
    - Program documentation. (*WiP*)

#### Text Boxes
- `Begin Translating`: allows you to type the desired formula(s) for translation.
- `Translated Text`: displays the translated text.

#### Buttons
- `Translate`: translates the text in the first text box.
- `Load`: prompts the user to enter a file with formulas ready for translation.
- `Clear`: clears all input and output.
- `Copy`: copies the translated text to the clipboard.
- `Save`: prompts the user to save the translated text to a `.kyx` file.
    - If only one formula is translated, then it will be saved with a file name and location chosen by the user.
    - If multiple formulas are entered, the user will have the option to either save all the translations in a single `.kyx` file (not recommended since KX can only handle one program at a time), or to choose a base file name and
      generate multiple files for each translated program.

### History Page
#### Under Construction...
- History page built, must update readme.

## The Language
### <ins>Basic Expressions</ins>
##### Sum and subtraction
`[1,2] + [3,4] - [5,6]`
##### Multiplication and division
`[1,2] / ([3,4] * [5,6])`

### <ins>First Order Logic Formulas</ins>
##### LT, LTE and Conjunction
`[1,2] < [2,3] AND [3,4] <= [5,6]`
##### GT, GTE and Disjunction
`[2,3] > [1,2] OR [5,6] >= [3,4]`
##### Negation (!)
`!(x < [2,3] AND y > [1,2])`
##### Implication (->)
`x >= [5,6] AND (y <= [1,2]) -> x > y`
##### Universal Quantifier ($ ... IN ...)
`$ x IN (x*x) -> x >= 0`

### <ins>Hybrid Program Expressions</ins>
##### Discrete Assignment
`x := [0,1]`
##### Continuous Evolution ( (x'=...) & (...) )
`(x'=-x, y'=-y & (0<x))`
##### Sequential Composition ( ... ; ... )
`x := [6,6] ; y := [1,2]`
##### State test/check ( ?(...) )
`? (x > 0) ; (x'=-x, y'=-y & (0<x))`
##### Non-deterministic choice ( ... || ... )
`x:=y || x := z`
##### Non-deterministic repetition ( (...)** )
`(? (x > 0) ; x:=y || x := z)**`

### <ins>Modalities</ins>
##### Modality - box ( [{ ... }] ) and differential assignment (x'=...)
`\[{ x := [1,2] ; {x'=x-1} }\] (x>0)`
##### Modality - diamond ( <{ .. }> )
`\<{ x := [1,2] ; y:=[0,1] }\> (x>0 AND  y>=0)`
