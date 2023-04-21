# Grammar

This is the grammar for parsing expressions in the Grape Programming Language.

```grammar
program     -> declaration* EOF ;

declaration -> variableDecl | statement ;
variableDecl-> IDENTIFIER "=" expression NEWLINE ;

statement   -> exprStmt | if | inspect | exit | block ;

exprStmt    -> expression NEWLINE ;
if          -> "if" "(" expression ")" statement "else" statement ;
inspect     -> "inspect" expression NEWLINE ;
exit        -> "exit" ( NUMBER | _ ) NEWLINE ;
block       -> "do" (declaration)* "end" ;

expression  -> equality ;
equality    -> comparison ( ( "==" | "!=" ) comparison )* ;
comparison  -> term ( ( ">" | ">=" | "<" | "<=" ) term )* ;
term        -> factor ( ( "+" | "-" ) factor )* ;
factor      -> unary ( ( "/" | "*" ) unary )* ;
unary       -> ( "-" | "not" ) unary | primary ;
primary     -> literal | grouping ;

literal     -> NUMBER | STRING | ATOM | list | tuple | bool | IDENTIFIER ;
bool        -> "true" | "false"
list        -> "[" expression | ( expression "," )* "]" ;
tuple       -> "(" expression* ")" ;
grouping    -> "(" expression ")" ;
```
