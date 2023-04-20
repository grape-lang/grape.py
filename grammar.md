# Grammar

This is the grammar for parsing expressions in the Grape Programming Language.

```grammar
program     -> statement* EOF ;

declaration -> variableDecl | statement ;
variableDecl-> IDENTIFIER "=" expression NEWLINE ;

statement   -> inspectStmt | exprStmt | block ;

exprStmt    -> expression NEWLINE ;
inspectStmt -> "inspect" expression NEWLINE ;
exitStmt    -> "exit" ( NUMBER | _ ) NEWLINE ;

block       -> "do" (declaration)* "end" ;

expression  -> equality ;
equality    -> comparison ( ( "==" | "!=" ) comparison )* ;
comparison  -> term ( ( ">" | ">=" | "<" | "<=" ) term )* ;
term        -> factor ( ( "+" | "-" ) factor )* ;
factor      -> unary ( ( "/" | "*" ) unary )* ;
unary       -> ( "-" | "not" ) unary | primary ;
primary     -> literal | grouping ;

literal     -> NUMBER | STRING | ATOM | list | tuple | "true" | "false" | IDENTIFIER ;
list        -> "[" expression | ( expression "," )* "]" ;
tuple       -> "(" expression* ")" ;
grouping    -> "(" expression ")" ;
```
