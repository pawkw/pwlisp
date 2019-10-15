# Built in functions
## Special forms are defined in pwlisp.py

builtInFunctions = {
    # Math and tests
    # +
    # -
    # *
    # / - check first arg for float or int
    # % - returns int
    # =
    # <
    # <=
    # >
    # >=

    # Boolean funcs
    # and - (variadic)
    # or - (variadic)
    # not

    # Predicates
    # number?
    # int?
    # float?
    # string?
    # list?
    # dict?
    # key? - Dictionary key word
    # false? - Only false and nil are falsy
    # nil?
    # true?  - Everything else is true
    # empty? - For dict, list and string
    # function?
    # is-macro?
    # is-builtin?
    # symbol?
    # contains? See list, dict and string functions

    # List, dict, symbol and string functions
    # concat - (variadic) Add n lists, strings together. All items must be same type
    # merge - (variadic) Merge n lists, dicts together. No items are duplicate. Calling on a single list deletes duplicates.
    # length - Length of string, list or dict
    # flatten - Return a flat list
    # list - (variadic) Create a list
    # dict - (variadic) Create a dict - (dict :a 1 :b 2 c: 3) -> {:a 1 :b 2 :c 3}
    # string - (variadic) Create a string - joins "print" version of each item - "".join(map(lambda item: item.__str__(), args))
    # symbol - Create a symbol - (symbol 'item) -> item, Using define creates a symbol automatically
    # expode - Turns a string into a list of strings where each string is one character - (explode "Dave") -> ("D" "a" "v" "e")
    ## Index and retrieval
    # first - First item of list or string
    # rest - Everything after the first item
    # nth - nth item in list or string
    # contains? - true if in list, dict(keyword) or string. (contains? mylist "apple")(contains? mydict :EmployeeNumber)(contains? mystring "tion")

    # Function functions
    # map - (variadic) Returns a list with the function applied to each item - (map square (list 1 2 3)) -> (1 4 9)
    # apply - (variadic) Returns result of function applied to all items - (apply eval deferred-commands "(display \"Done!\")")
    # doc - Return the doc string of a function
    # help - Same as doc
    # setdoc - Set the doc string of a user defined function - (setdoc myfunc "A helpful function.")

    # System type commands
    # display - (variadic) Display items on screen (variadic)
    ## There is no 'close' for files. Files are handled in a big chunk and automatically closed.
    # import - Read and apply a file (import "myfile.pwl") = (apply eval (read-file "myfile.pwl"))
    # read-file - Create a list of strings from a file
    # read-line - Return a string from console input.
    # time - Returns an int of time in ms from the start of the Unix epoch (January first 1970)
    # *argv* - This is defined in pwlisp.py. It is a list of command line arguments.
}
