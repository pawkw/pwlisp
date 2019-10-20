# Built in functions
# Special forms are defined in pwlisp.py

from modules.pwl_types import *
from modules.parser import parse
import time

def concat(*args):
    print("Not implemented.")
    pass

def merge(*args):
    print("Not implemented.")
    pass

def flatten(*args):
    print("Not implemented.")
    pass

def assoc(thisdict, *args):
    return Dict(**thisdict, **Dict(args))

def remove(item, *args):
    # Equivalent to result = Dict(item) or List(item)
    result = type(item)(item)
    for x in args:
        result.pop(x)
    return result

def apply(func, *args):
    return func(*args)

def display(*args):
    print(str(*args))
    pass

def pwl_import(file_name):
    print("Not implemented.")
    pass

def read_file(file_name):
    print("Not implemented.")
    pass

def read_line(prompt):
    line = input(prompt)
    return line

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
    'builtin?': lambda x: isinstance(x, Function) and x.is_builtin,
    # symbol?
    'symbol?': lambda x: isinstance(x, Symbol),
    # contains? There is no type check here so it throws an exception.
    'contains?': lambda x, y: x in y,

    # List, dict, symbol and string functions
    # concat - (variadic) Add n lists, strings together. All items must be same type
    'concat': concat,
    # cons - prepend x onto list y.
    'cons': lambda x, y: List([x])+y,
    # merge - (variadic) Merge n lists, dicts together. No items are duplicate. Calling on a single list deletes duplicates.
    'merge': merge,
    # length - Length of string, list or dict
    'length': lambda x: len(x),
    # flatten - Return a flat list from Dict or List. Dict keywords are converted to Strings.
    'flatten': flatten,
    # assoc - Return a new dict including item
    'assoc': assoc,
    # remove - Return dict or list with item removed
    'remove': remove,
    # keys - Get a list of keys from a dict
    'keys': lambda x: x.keys(),
    # values - Get a list of value from a dict
    'values': lambda x: x.values(),
    # get - Get a value from a dict
    'get': lambda x, y: x[y],

    # list - (variadic) Create a list
    'list': lambda *x: List(x),
    # dict - (variadic) Create a dict - (dict :a 1 :b 2 c: 3) -> {:a 1 :b 2 :c 3}
    'dict': lambda *x: Dict(x),
    # string - (variadic) Create a string - joins "print" version of each item - "".join(map(lambda item: item.__str__(), args))
    'string': lambda *x: "".join(map(lambda item: str(item), x)),
    # Float
    'float': lambda x: float(x),
    # Int
    'int': lambda x: int(x),
    # symbol - Create a symbol - (symbol 'item) -> item, Using define creates a symbol automatically
    'symbol': lambda x: Symbol(x),
    # expode - Turns a string into a list of strings where each string is one character - (explode "Dave") -> ("D" "a" "v" "e")
    'explode': lambda x: List(list(x)),
    ## Index and retrieval
    # first - First item of list or string
    'first': lambda x: x[0] if x else None,
    # rest - Everything after the first item
    'rest': lambda x: x[1:] if x else None,
    # nth - nth item in list or string
    'nth': lambda x, i: x[i] if x else None,


    # Function functions
    # map - (variadic) Returns a list with the function applied to each item - (map square (list 1 2 3)) -> (1 4 9)
    'map': lambda func, *args: List(map(func, args)),
    # apply - (variadic) Returns result of function applied to all items - (apply eval deferred-commands)
    'apply': lambda x, *y: x(*y),
    # doc - Return the doc string of a function
    'doc': lambda x: x.doc,
    # help - Same as doc
    'help': lambda x: x.doc,
    # setdoc - Set the doc string of a user defined function - (setdoc myfunc "A helpful function.")
    'setdoc': lambda x, y: x.setdoc(y),

    # System type commands
    # display - (variadic) Display items on screen (variadic)
    'display': display,
    ## There is no 'close' for files. Files are handled in a big chunk and automatically closed.
    # import - Read and apply a file (import "myfile.pwl") = (apply eval (read-file "myfile.pwl"))
    'import': pwl_import,
    # read-file - Create a list of strings from a file
    'readfile': lambda file: open(file).read(),
    # read-line - Return a string from console input.
    'readline': read_line,
    # parse
    'parse': lambda x: parse(x)[0],
    # time - Returns an int of time in ms from the start of the Unix epoch (January first 1970)
    'time': lambda: int(round(time.time() * 1000))
    # *argv* - This is defined in pwlisp.py. It is a list of command line arguments.
}
