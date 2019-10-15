# Environment class
import pwl_types as types

class Environment:
    def __init__(self, parent = None, args = none, values = none):
        self.defs = {}
        self.parent = parent

        # Bind arguments to values
        # Handle variadic binding

    def __str__(self):
        pass

    # TODO: Look up how to implement dict-like functions
    def set(self, key, value):
        pass

    def find(self, key):
        pass

    def get(self, key):
        pass
