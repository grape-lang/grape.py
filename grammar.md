# Grammar

This is the grammar for parsing programs in the Grape Programming Language.

```grammar
program     -> statement* EOF ;

statement   -> expression NEWLINE ;
expression  -> declaration | if | do | logic_or ;

declaration -> IDENTIFIER "=" expression ; 

// scoped
do          -> "do" statement* "end" ; 
do-else     -> "do" statement* "else" statement* "end" ;
if          -> "if" "(" logic_or ")" ( expression "else" expression ) | do-else ;

// real values
logic_or    -> logic_and ( "or" logic_and )* ;
logic_and   -> equality ( "and" equality )* ;
equality    -> comparison ( ( "==" | "!=" ) comparison )* ;
comparison  -> term ( ( ">" | ">=" | "<" | "<=" ) term )* ;
term        -> factor ( ( "+" | "-" ) factor )* ;
factor      -> unary ( ( "/" | "*" ) unary )* ;
unary       -> ( "-" | "not" ) unary | call ;
call        -> call | primary "(" expression* ")" ;
primary     -> literal | grouping ;

literal     -> NUMBER | STRING | ATOM | list | tuple | bool | IDENTIFIER ;
bool        -> "true" | "false"
list        -> "[" expression | ( expression "," )* "]" ;
tuple       -> "(" expression* ")" ;
grouping    -> "(" expression ")" ;
```
