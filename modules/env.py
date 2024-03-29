# Environment class
import modules.pwl_types as types

class Environment(dict):
    def __init__(self, parent = None, args = None, values = None):
        '''
        Create a new environment.

        parent is the parent environment.
        args a list of arguments.
        values is a list of values.

        For variadic args(like *args) the '.' token is used.

        >>> e = Environment(None, ['a', '.', 'b'], [1, 2, 3])
        >>> e['a']
        1
        >>> e['b']
        <PWLisp list (2 3)>
        '''

        self.parent = parent

        if args:
            for index in range(len(args)):
                # Handle variadic
                if args[index] == '.':
                    exps = values[index:]
                    self[args[index+1]] = exps
                    break
                if index >= len(values):
                    raise types.Error('Missing argument \'{}\'.'.format(args[index]))
                    return
                self[args[index]] = values[index]

        # Bind arguments to values
        # if self.args:
        #     while self.args:
        #         arg = self.args.pop(0)
        #         value = self.values.pop(0)
        #         # Handle variadic
        #         if arg == '.':
        #             arg = self.args.pop(0)
        #             self.values = [value]+self.values
        #             self[arg] = types.List(self.values)
        #             break
        #         self[arg] = value

    def __str__(self):
        result = ""
        for item in self.keys():
            result += item.rjust(15)+" : "+str(self[item])+'\n'
        return result

    def __repr__(self):
        result = " ".join(self.keys())
        return '<PWLisp environment : {}>'.format(result)

    # TODO: Look up how to implement dict-like functions
    def set(self, key, value):
        self[key] = value
        return value

    def find(self, key):
        '''
        Find a key in this environment or its parent.

        >>> e = Environment(None, ['a', 'b'], [1, 2])
        >>> e['b']
        2
        >>> e.find('a')
        <PWLisp environment : a b>
        >>> e.find('Dave') # None is returned
        '''
        if key in self:
            return self
        if self.parent:
            return self.parent.find(key)

    def get(self, key):
        '''
        Get the value of a key in this environment or its parent.

        >>> parent = Environment(None, ['a', 'c'], ['Oh oh!', 3])
        >>> e = Environment(parent, ['a', 'b'], [1, 2])
        >>> e.get('a')
        1
        >>> e.get('b')
        2
        >>> e.get('c')
        3
        '''

        env = self.find(key)
        if env:
            return env[key]
        raise Exception("Key {} was not found in environment.".format(key))
