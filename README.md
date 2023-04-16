The Grape Programming Language
==============================

A general purpose programming language made for rapid-pase prototyping.

Features
--------

- Statically typed
- Garbage-collected
- No mutable pointers


Hello World in Grape
--------------------

```grape
// Your first grape program
print("Hello world!")
```

As you can see the syntax is pretty python-y/elixir-y. `;` is strictly forbidden, which means statements end with an newline.


Types
-----

- Booleans:

    ```grape
    true
    false
    ```

- Number:

    Grape features one kind of number: double-precision fixed-point floating point numbers.

    ```grape
    1234
    12.34
    ```

    > **Info**:  
    > Real numbers are also called integers by programmers.

- Text:

    Strings pieces of text using UTF-8 encoding that are defined using double quotes:

    ```grape
    "Hello world!"
    "" \\ Empty string
    "1234" \\ Not an integer.
    ```

- Atom:

    An atom is defined as a constant that is it's own value. It is most used for status codes (`Ok` or `Error`).

    Atoms always start with either a capital letter or an @-symbol.

    ```grape
    Ok
    Error
    @something
    ```

- List: 

    In Grape, a list is a list of dynamic length. It is defined using square brackets (`[`, `]`). A list can only contain one type:

    ```grape
    [1, 2, 3, 4]
    ["Hello", "world", "!"]
    [true, false]
    ```

- Tuple:

    A tuple is a list with static length. It is defined using round brackets (`(`, `)`). A tuple can contain multiple types:

    ```grape
    (Ok, 256)
    (Error, "error message")
    ```


Expressions
-----------

An expression is a piece of code that returns a value. In the following examples the returned value is shown in the comment after the expression.

### Arithmetic

```grape
1 + 1 \\ 2
2 - 1 \\ 1
2 * 2 \\ 4
6 / 2 \\ 3
```

These are infix operators, meaning they are placed between two operands. The only exception is the `-`, since it can also be used as prefix to negate a value:


```grape
-1 + 2 \\ 1
```

### Comparison and equality

```grape
less < than
lessThan <= orEqual
greater > than
greaterThan >= orEqual
```

Test for (in)equality:

```grape
1 == 2 // false
"cat" != "dog" // true
```

Different types can be compared, but there is no implicit conversion:

```grape
123 == "123" \\ false
```

### Logical operators

The `not` operator negates a truthy value:

```grape
not true \\ false
not false \\ true
```

Or and and operations:

```grape
true and false \\ false
true or false \\ true
true nor false \\ false
```

### Ambiguity

If there is an ambigui statement, parentaces have to be used:

```grape
not true and false

// should be one of these:
(not true) and false
not (true and false)
```


Statements
----------

A statement is a piece of code that _does_ something, whereas an expression returns a value.

An statement is ended by a newline:

```grape
print("Hello world!")
```

This is an statement that evaluates a single expression, and _does_ something: display the text "Hello world!" to the end-user.

Multiple statements can be bundled in a block:

```grape
do
    print("Hello world!")
    print("This is your first Grape program")
end
```


Variables
---------

A variable is not created using a keyword like `let` or `var`, but by using it's type:

```grape
num maxSpeed = 100
text theWarning = "Oh no, the plane is going to fast!"
```

They can than be used:

```grape
print(theWarning)
```


Control flow
------------

### `if`-statements

```grape
if(currentSpeed > maxSpeed) do
    print("Warning: going to fast!")
else
    print("Good job, you're cool :)")
end
```

Functions
---------

A function can be defined like this:

```grape
fn add(a: Number, b: Number) do
    a + b
end
```

It contains a type definition (`fn add(...)`) and a block.
The last statement in a function is automatically returned.

Calling them works like this:

```grape
add(1, 2) \\ 3
```

Functions are first-class citizens. That means they can be passed around like variables:

```grape
print(add) \\ #Function: add(a, b)
```

A function can also be anonymous:

```grape
fun add = fn(a: Number, b: Number) do
    a + b
end
```
