# Grammar

This is the grammar for parsing expressions in the Grape Programming Language.

```grammar
program     -> declaration* EOF ;

declaration -> variableDecl | statement ;
variableDecl-> IDENTIFIER "=" expression NEWLINE ;

statement   -> exprStmt | if | inspect | exit | doBlock ;

exprStmt    -> expression NEWLINE ;
if          -> "if" "(" expression ")" (( statement "else" statement ) | doElseBlock) ;
inspect     -> "inspect" expression NEWLINE ;
exit        -> "exit" ( NUMBER | _ ) NEWLINE ;
doBlock     -> "do" (declaration)* "end" ;
doElseBlock -> "do" (declaration)* "else" (declaration)* "end" ;

expression  -> logic_or ;
logic_or    -> logic_and ( "or" logic_and )* ;
logic_and   -> equality ( "and" equality )* ;
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
