# Built in functions
# Special forms are defined in pwlisp.py
# All the helper functions are below the dict.

from pwl_types import *

builtInFunctions = {
    # Math and tests

    # +
    '+': lambda x, y: x + y,
    # -
    '-': lambda x, y: x - y,
    # *
    '*': lambda x, y: x * y,
    # / - check first arg for float or int
    '/': lambda x, y: x // y if type(x) == int else x/y,
    # % - returns int
    '%': lambda x, y: x % y,
    # =
    '=': lambda x, y: x == y,
    # <
    '<': lambda x, y: x < y,
    # <=
    '<=': lambda x, y: x <= y,
    # >
    '>': lambda x, y: x > y,
    # >=
    '>=': lambda x, y: x >= y,

    # Boolean funcs are defined in pwlisp.py
    # and - (variadic)
    # or - (variadic)
    # not

    # Predicates - Keep in mind that List in PWLisp List, etc.
    # number?
    'number?': lambda x: isinstance(x, (int, float)),
    # int?
    'int?': lambda x: isinstance(x, int),
    # float?
    'float?': lambda x: isinstance(x, float),
    # string?
    'sting?': lambda x: isinstance(x, String),
    # list?
    'list?': lambda x: isinstance(x, List),
    # dict?
    'dict?': lambda x: isinstance(x, Dict),
    # key? - Dictionary key word
    'key?': lambda x: isinstance(x, Key),
    # false? - Only false and nil are falsy
    'false?': lambda x: type(x) in (False, None),
    # nil?
    'nil?': lambda x: x == None,
    # true?  - Everything else is true
    'true?': lambda x: not type(x) in (False, None),
    # empty? - For dict, list and string
    'empty?': lambda x: len(x) == 0,
    # function?
    'function?': lambda x: isinstance(x, Function),
    # macro?
    'macro?': lambda x: isinstance(x, Function) and x.is_macro,
    # builtin?
    'is-builtin?': lambda x: isinstance(x, Function) and x.is_builtin,
    # symbol?
    'symbol?': lambda x: isinstance(x, Symbol),
    # contains? There is no type check here so it throws an exception.
    'contains?': lambda x, y: x in y,

    # List, dict, symbol and string functions
    # concat - (variadic) Add n lists, strings together. All items must be same type
    'concat': concat,
    # merge - (variadic) Merge n lists, dicts together. No items are duplicate. Calling on a single list deletes duplicates.
    'merge': merge,
    # length - Length of string, list or dict
    'length': lambda x: len(x),
    # flatten - Return a flat list from Dict or List. Dict keyword are converted to Strings.
    'flatten': flatten,

    # list - (variadic) Create a list
    'list': lambda *x: List(x),
    # dict - (variadic) Create a dict - (dict :a 1 :b 2 c: 3) -> {:a 1 :b 2 :c 3}
    'dict': lambda *x: Dict(x),
    # string - (variadic) Create a string - joins "print" version of each item - "".join(map(lambda item: item.__str__(), args))
    'string': lambda *x: "".join(map(lambda item: str(item), x)),
    # symbol - Create a symbol - (symbol 'item) -> item, Using define creates a symbol automatically
    'symbol': lambda x: Symbol(x),
    # expode - Turns a string into a list of strings where each string is one character - (explode "Dave") -> ("D" "a" "v" "e")
    'explode': lambda x: List(list(x)),
    ## Index and retrieval
    # first - First item of list or string
    'first': lambda x: x[0] if x else None,
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

def concat(*args):
    pass

def merge(*args):
    pass

def flatten(*args):
    pass
