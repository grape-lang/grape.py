# Grammar

This is the grammar for parsing expressions in the Grape Programming Language.

```grammar
program     -> statement* EOF ;

declaration -> variableDecl | statement;
statement   -> printStmt ;

variableDecl-> IDENTIFIER "=" expression NEWLINE ;
printStmt   -> "inspect" expression NEWLINE ;
exitStmt    -> "exit" ( NUMBER | _ ) NEWLINE ;

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
