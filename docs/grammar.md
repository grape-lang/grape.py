Grammar
=======

This is the grammar for parsing programs in the Grape Programming Language.

```grammar
program     -> statement* EOF ;

statement   -> expression NEWLINE ;
expression  -> variableDecl | if | function | do | logic_or ;

function    -> functionDecl | lamda ;

variableDecl-> IDENTIFIER "=" expression ; 
functionDecl-> "fn" IDENTIFIER "(" arguments? ")" block ;
lambda      -> "fn(" arguments? ")" block ;

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
call        -> primary ( "(" arguments? ")" )* ;
primary     -> literal | grouping ;

arguments   -> collection ;

literal     -> NUMBER | TEXT | ATOM | bool | list | tuple | IDENTIFIER ;
bool        -> "true" | "false" ;
list        -> "[" collection "]" ;
tuple       -> "{" collection "}" ;
grouping    -> "(" expression ")" ;

collection  -> expression ("," expression)* ;
```
