# pwlisp types

# Function
class Function:
# name - A displayable name and param list
# apply - executable code. fn.apply(x) should execute in python
# params
# env = environment at the time of call
# code = abstract syntax tree
# builtin
# is_macro
# doc = documentation. this can be a help doc
# __str__ - Return name
    def __init__(self, name, apply, params, env, code = None, builtin = False, macro = False, doc = None):
        self.name = name
        self.apply = apply
        self.params = params
        self.env = env
        self.code = code
        self.is_builtin = builtin
        self.is_macro = macro
        self.doc = doc

    def __str__(self):
        return self.name

    def set_doc(self, doc):
        self.doc = doc

# List
class List(list):
    # Override parent class methods so they return the correct type.
    def __add__(self, item):
        return List(list.__add__(self, item))

    def __getitem__(self, index):
        if type(index) == slice:
            return List(list.__getitem__(self, index))
        if index > len(self):
            return None
        return list.__getitem__(self, index)

    def __str__(self):
        result = '('
        if len(self) == 0:
            return result + ')'
        for x in self:
            result += x+' '
        return result[:-1] + ')'

# Dict
class Dict(dict):
    def __init__(self, vals):
        if type(vals) == List:
            if len(vals) % 2 != 0:
                raise Exception("Odd number of arguments while creating dict from list.")
                return None
            for x in range(0, len(vals), 2):
                # zipped = zip(mylist[0::2], mylist[1::2])
                if type(vals[x]) != Key:
                    kwd = Key(vals[x])
                else:
                    kwd = vals[x]
                self[kwd] = vals[x+1]
        elif type(vals) == Dict:
            for x in vals:
                self[x] = vals[x]
        else:
            raise Exception("Wrong type for initializing a dict: "+str(type(vals)))

# String
class String(str):
    def __getitem__(self, index):
        if type(index) == slice:
            return String(str.__getitem__(self, index))
        if index > len(self) or len(self) == 0:
            return None
        return String(str.__getitem__(self, index))

# Key
class Key(str):
    pass

# Exception
class Error(Exception):
    pass
