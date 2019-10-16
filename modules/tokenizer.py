"""
The TokenLine class and tokenize function.
"""
import re

class TokenLine:
    """
    The TokenLine class does not do any tokenizing. TokenLine objects are meant
    to be returned and used to read through and peek at the tokens in the
    program line that is represented. The line number is saved so that any
    parse errors can return the line of the error.

    The get_line method returns the stored line number.
    """

    def __init__(self, tokens, line = 0):
        self.tokens = tokens
        self.cursor = 0
        self.line = line

    def __repr__(self):
        result = "<Line: {} ".format(self.line)+str(self.tokens)+">"
        return result

    # Return token and increment cursor position
    def next(self):
        """The next method returns the next token and updates the cursor."""
        self.cursor += 1
        return self.tokens[self.cursor - 1]

    # Return token without updating cursor postion
    def peek(self):
        """The peek method returns the next token but does not update the
        cursor."""
        if self.cursor > len(self.tokens):
            return None
        return self.tokens[self.cursor]

    # Return the cursor position
    def get_cursor(self):
        """The get_cursor method returns the current position of the cursor.
        This can be handy for printing parse errors."""
        return self.cursor

    def get_line(self):
        """The get_line method returns the line number supplied to the
        initializer. This can be handy for printing parse errors."""
        return self.line

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

    >>> prog = tokenize('(+ 1 2)')
    [<Line: 0 ['(', '+', '1', '2', ')']>]
    >>> prog[0].peek()
    '('
    >>> prog[0].next()
    '('
    >>> prog[0].get_line()
    0
    """

    # Split the string on '\n'
    strings = string.split('\n')
    result = []
    # Loop through list of strings making a TokenLine
    for index in range(len(strings)):
        result.append(TokenLine(get_tokens(strings[index]), index))
    print(str(result))
    return result

if __name__=="__main__":
    import doctest
    doctest.testmod()
