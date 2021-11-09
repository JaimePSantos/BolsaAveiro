# PROJECT: idDL2DL

The implementation of **idDL2dDL** is structured in four parts, namely the *lexer*, the *parser*, the *translator* and
the graphical user interface.

1. The lexer performs the lexical analysis of the expressions provided as input, which is the
   process of converting a sequence of characters into *tokens*.
2. The parser is then called to perform a syntactic analysis over these tokens, and returns an abstract syntax tree (AST) as output.
3. The translator is fed an AST as input, and returns a translated string as output. This is achieved by *visit*
   methods, whose purpose is evaluate and translate the content of the nodes that compose the AST.
4. The rudimentary GUI compiles the functionality of the aforementioned modules in a page for user inputed translation,
   and in a page for loading files with translatable formulas, in order to provide the user a simple way of performing
   translations.

Structure of the program follows [this](https://github.com/davidcallanan/py-myopl-code) respository.

**Early version of the software, any bugs please open an issue.**

## How to run in console

Navigate to **/Interval** folder and run `python main`.

Type *help* for commands.

A single translation can be made by simply typing the desired formula in this program's syntax (check examples to learn
more).

## GUI

**_UNDER CONSTRUCTION_**

Navigate to **/Interval/GraphicalInterface** and run
`python GInterface`.

### Translation Page

<img src="/Resources/TranslationGUI.png" width="500">

#### Menu
- The `File` separator allows the user to
    - Load formulas to be translated. (`ctrl+l`)
    - Save the translated formulas to a file. (`ctrl+s`)
    - Exit the program. (`ctrl+q`)
- The `Help` separator allows the user to access
    - Program instructions. (*github readme*)
    - Program documentation. (*WiP*)

#### Buttons
- The `Begin Translating` text box allows you to type the desired formula(s) for translation.
- The `translate` button translates the text in the first text box.
- The `Translated Text` text box displays the translated text.
- The `clear` button clears all input and output.
- The `copy` button copies the translated text to the clipboard.
- The `save` button prompts to user to save the translated text to a *.kyx* file.
    - If only one formula is translated, then it will be saved with a file name and location chosen by the user.
    - If multiple formulas are entered, the user will have the option to either save all the translations in a single *
      .kyx* file (not recommended since KX can only handle one program at a time), or to choose a base file name and
      generate multiple files for each translated program.
- The `load` button prompts the user to enter a file with formulas ready for translation.

### History Page
#### Under Construction...
- Because we're using dictionaries to store the history of commands, there will be no repeated commands in the history.

## TODO

### Lexer

- Change `NOT` token to be a keyword;

### Parser
- Save parsed text as an object for easier integration with the GUI;
- **Inverse interval**;
- Better way of representing powers;
- Implement a better version of `*`;
- Parenthesis nodes might cause problems with restrictions;
- `[1,a` will match `,` with comma and not separator, might be an issue.

### Translator  
- Save translated text as an object for easier integration with the GUI;
- **Inverse interval**;
- The way to deal with ';' at the end of box is not good.

### GUI 
- **Error handling**
   - Translation Errors;
   - Closing File Load prompt when no file is selected.
- **History of translations**
   - Persistent history or simple session specific history?;
   - Create GUI page;
   - Prevent empty entries.
- Tooltips;
- Explore PanedWindow instead of Notepage(?);
- Images for buttons(?);
- Improve visual quality;
- Make it accessible through main.py; 
- Refactor Basic and File translation pages;s

