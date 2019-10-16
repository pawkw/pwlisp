# pwlisp types

# Function
class Function:
    def __init__(self, name, apply, params = [], env = [], code = None, builtin = False, macro = False, doc = None):
        """
        Create a PWLisp function.

        name is printed out when the Function object is printed.
        apply is the executable code: a lambda or function reference.
        params are a PWLisp List which is not used internally. These are stored
            to be recalled when the function is actually applied.
        env is the environment(frames) in which the function was invoked.
        buitin is a boolean.
        macro is a boolean.

        >>> first = Function('first', lambda a: a[0], builtin = True)
        >>> first
        <PWLisp function first>
        >>> print(first)
        first (built in)
        >>> first([1, 2, 3])
        1
        """
        self.name = name
        self.apply = apply
        self.params = params
        self.env = env
        self.code = code
        self.is_builtin = builtin
        self.is_macro = macro
        self.doc = doc

    def __str__(self):
        result = self.name
        result += ' (built in)' if self.is_builtin else ''
        result += '(macro)' if self.is_macro else ''
        return result

    def __repr__(self):
        return '<PWLisp function {}>'.format(self.name)

    def __call__(self, *args, **kwargs):
        return self.apply(*args, **kwargs)

    def set_doc(self, doc):
        '''
        Set the doc/help for a PWLisp function.

        >>> first = Function('first', lambda a: a[0], builtin = True)
        >>> first.set_doc('Return the first item in a list.')
        >>> print(first.doc)
        Return the first item in a list.
        '''
        self.doc = doc

# List
class List(list):
    '''
    Create a PWLisp List

    >>> nums = List([1, 2, 3])
    >>> nums
    <PWLisp list (1 2 3)>
    >>> print(nums)
    (1 2 3)
    >>> print(nums + [4])
    (1 2 3 4)
    '''


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
            result += str(x) +' '
        return result[:-1] + ')'

    def __repr__(self):
        return '<PWLisp list {}>'.format(str(self))

# Dict
class Dict(dict):
    def __init__(self, vals):
        '''
        Create a PWLisp dict.

        Can be initialized with a PWLisp List, PWLisp Dict, or a python dict
        or list. In all cases it is deep copied instead of referrenced.

        >>> kwargs = Dict(['x', 1, 'y', 2])
        >>> print(kwargs)
        {:x 1 :y 2}
        '''
        if type(vals) in (List, list):
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
        elif type(vals) in (Dict, dict):
            for x in vals:
                self[x] = vals[x]
        else:
            raise Exception("Wrong type for initializing a dict: "+str(type(vals)))

    def __str__(self):
        result = '{'
        if len(self)>0:
            strings = []
            for x in self:
                strings.append('{} {}'.format(str(x), str(self[x])))
            result += " ".join(strings)
        return result + '}'

    def __repr__(self):
        return '<PWLisp dict {}>'.format(str(self))

# String
class String(str):
    '''
    Create a PWLisp string from a Python string.

    >>> x = String("Hello")
    >>> x
    <PWLisp string "Hello">
    >>> x += " world!"
    >>> x
    <PWLisp string "Hello world!">
    >>> x[:5]
    <PWLisp string "Hello">
    >>> print(x)
    Hello world!
    '''

    def __getitem__(self, index):
        if type(index) == slice:
            return String(str.__getitem__(self, index))
        if index > len(self) or len(self) == 0:
            return None
        return String(str.__getitem__(self, index))

    def __add__(self, item):
        return String(str.__add__(self, item))

    def __repr__(self):
        return '<PWLisp string "'+str(self)+'">'

# Key
class Key(str):
    def __str__(self):
        return ":"+self

    def __repr__(self):
        return '<PWLisp key {}>'.format(str(self))

# Exception
class Error(Exception):
    pass
