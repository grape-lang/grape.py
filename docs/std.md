Grape Standard Library
======================

The standard library for the Grape Programming Language is split into three modules:

- std
- io
- list

`std`
-----

The std module contains very common functions that don't need to be imported or prefixed.

- `print(input: Any) -> Text`
  Prints the input to stdout (and appends an newline).
  Returns the original input.

- `for(input: Collection, fun: Fn) -> Collection`
  Loops over the input and produces the output by
  running the function for each item.

  The function should accept one argument: the current index.
  It should return an item for the new list.

  If you just want to loop over an list without producing an output,
  take a look at `@list.each`. If you want to modify the original value,
  take a look at `@list.map`.

`io`
----

The io modules contains functions to handle input and output for your program.

- `write(input: Any) -> Text`
  Writes the input to stdout.
  Returns the original input

- `read(prompt: Text) -> Text`
  Prompts the user for input in stdin.
  Returns the user input.

- `readFile(filePath: Text) -> Text`
  Reads a file from disk.
  Returns the contents of the file.

- `writeFile(filePath: Text, contents: Text) -> Text`
  Writes to a file on disk.
  Returns the original input.
  Creates the file if it didn't exist yet.

`list`
------

The list module contains functions for easily managing collections (lists or tuples).

- `elem(list: Collection, index: Number) -> Any`
  Retreives the element out of a collection by
  its index.

- `put(list: Collection, index: Number, item: Any) -> Collection`
  Puts an element into a collection at the specified index.
  Only works if the index already exists.

- `append(list: Collection, item: Any) -> Collection`
  Appends an item to a collection.

- `reduce(list: Collection, accumulator: Collection, fun: Fn) -> Collection`
  Loops through a collection and runs the provided function for every item,
  collecting results into an accumulator.
  
  The function accepts the current item and the accumulator, and
  returns an updated accumulator.

- `map(list: Collection, fun: Fn) -> Collection`
  Loops over the input and produces the output by
  running the function for each item.

  The function should accept one argument: the current item.
  It should return the modified item.

- `each(list: Collection, fun: Fn) -> Collection`
  Same as map, but doesn't produce new outputs.
  Loops over the input and runs the function for each item,
  but discards the produced value and returns the original input.

  The function should accept the current item and can return
  anything, since it will be discarded anyway.

- `flatten(list: Collection) -> Collection`
  Flattens an input of nested collections into a single list.

- `reverse(list: Collection) -> Collection`
  Reverses the order of an collection.

- `sort(list: Collection, fun: Fn) -> Collection`
  Simple bubble-sort implementation for sorting collections.
  The function should accept two items and return the highest one.
