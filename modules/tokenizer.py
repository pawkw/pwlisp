"""
The TokenLine class and tokenize function.
"""
import re

class TokenLine:
    """
    The TokenLine class.

    Stores a list of tokens that can be peeked.
    """

    def __init__(self, tokens):
        self.tokens = tokens
        self.cursor = 0

    def __repr__(self):
        result = "<TokenLine: {}>".format(str(self.tokens))
        return result

    # Return token and increment cursor position
    def consume(self):
        """The consume method returns the next token and updates the cursor."""
        result = self.look_ahead()
        self.cursor += 1
        return result

    # Return token without updating cursor postion
    def look_ahead(self):
        """The look_ahead method returns the next token but does not update the
        cursor."""
        if self.cursor >= len(self.tokens):
            return None
        return self.tokens[self.cursor]

class Reader:
    '''
    Creates a token reader that keeps track of line number a position.

    >>> tokens = Reader(["(def! a 5)", "(+ a 5)"])
    >>> tokens.look_ahead()
    '('
    >>> tokens.consume()
    '('
    >>> tokens.get_line()
    0
    >>> tokens
    <Reader [<TokenLine: ['(', ... >, <TokenLine: ['(', 'a', ... >]>
    '''

    def __init__(self, strings):
        self.lines = []
        self.line = 0
        for index in range(len(strings)):
            self.lines.append(TokenLine(get_tokens(strings[index])))

    def __repr__(self):
        return '<Reader {}>'.format(self.lines)

    def get_line(self):
        return self.line

    def look_ahead(self):

        # Handle end of line and blank lines in code
        while self.lines[self.line].look_ahead() == None:
            self.line += 1
            if self.line >= len(self.lines):
                return None
        return self.lines[self.line].look_ahead()

    def consume(self):
        result = self.look_ahead()
        if result != None:
            self.lines[self.line].consume()
        return result

# Get tokens helper
# Returns a list of tokens(strings)
def get_tokens(string):
    """
    Returns a list of tokens(strings) from the supplied string.

    >>> get_tokens("(+ 1 2)")
    ['(', '+', '1', '2', ')']
    """
    pattern = re.compile(r"""[\s,]*(~@|[\[\]{}()'`~^@]|"(?:[\\].|[^\\"])*"?|;.*|[^\s\[\]{}()'"`@,;]+)""");
    return [t for t in re.findall(pattern, string)]

# Tokenize
# Main interface to other modules
# Return a list of TokenLine
def tokenize(string):
    """
    Returns a list of TokenLine objects.
    """

    # Split the string on '\n'
    strings = string.split('\n')
    return Reader(strings)

if __name__=="__main__":
    import doctest
    doctest.testmod()
