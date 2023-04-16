# Grammar

This is the grammar for parsing expressions in the Grape Programming Language.

```grammar
expression  -> containment ;
equality    -> comparison ( ( "==" | "!=" ) comparison )* ;
comparison  -> term ( ( ">" | ">=" | "<" | "<=" ) term )* ;
term        -> factor ( ( "+" | "-" ) factor )* ;
factor      -> unary ( ( "/" | "*" ) unary )* ;
unary       -> ( "-" | "not" ) unary | primary ;
primary     -> literal | grouping ;

literal     -> NUMBER | STRING | ATOM | list | tuple | "true" | "false"
list        -> "[" expression | ( expression "," )* "]" ;
tuple       -> "(" expression* ")" ;
grouping    -> "(" expression ")" ;
```
