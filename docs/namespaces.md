Namespaces
==========

Grape uses namespaces for organizing large amounts of code into coherent structures.

A namespace is simply a collection of functions that share the same helpers or dependencies/do similar things. A namespace is also an scope.

To declare a namespace:

```grape
namespace hello do
    message = "Hello World"

    fn world() do
        print(message)
    end
end
```

To then call a function in the namespace:

```grape
@hello.world() // "Hello World"
```

As you can see you can reference a namespace with the `@` sign. Lexemes starting with a capital letter or `@` sign are also called [atoms](getting-started.md#Atoms). Atoms are most used as return/status codes, but they are also used as identifiers for namespaces. Because namespaces are just plain old atoms, you can pass them around:

```grape
for([@hello, @repl, @list], fn(ns) do
    ns.doSomething()
end)
```

Multiple namespaces can be defined in the same file, but you might want to split your code into multiple files. That is possible :)

Say you define the above namespace in the file `hello.grape`. You can then write `use @hello` in your main Grape file, and the namespace will be available.

Namespace lookup works like this:

- Files in the current directory with the name `hello`
- Dependencies with the name `hello`
- Global namespaces (such as the [standard library](std.md))
