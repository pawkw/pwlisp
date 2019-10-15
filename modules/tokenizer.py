# Tokenize input
# Tokens are strings

class TokenLine:
    def __init__(self, tokens, line = 0):
        self.tokens = tokens
        self.cursor
        self.line = line

    # Return token and increment cursor position
    def next(self):
        self.cursor += 1
        return self.tokens[self.cursor - 1]

    # Return token without updating cursor postion
    def peek(self):
        if self.cursor > len(self.tokens):
            return None
        return self.tokens[self.cursor]

    # Return the cursor position
    def get_cursor(self):
        return self.cursor

# Get tokens helper
# Returns a list of tokens(strings)
def get_tokens(string):
    pass

# Tokenize
# Main interface to other modules
# Yield a list of TokenLine
def tokenize(string):
    # Split the string on '\n'
    strings = string.spilt('\n')

    # Loop through list of strings making a TokenLine
    for index in range(strings):
        yield TokenLine(get_tokens(strings[index]), index)
