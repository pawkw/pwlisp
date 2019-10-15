# Parse tokenized input.
# The tokenizer returns a token line with the line number set.
# If this is just readline, it will always be zero.
# Otherwise, it will be the line number in the file.

from tokenizer import tokenize, TokenLine
import pwl_types as types

# Parse atom - token is a string
# Return item
def parse_atom(token):
    # Regex for int and float
    int_pattern = re.compile(r"-?[0-9]+$")
    float_pattern = re.compile(r"-?[0-9][0-9.]*$")

    # int
    # float
    # string
    # key
    # nil
    # true
    # false
    pass

# Swap out aliases - ' for quote
# Return list of parsed tokens 'dave = (quote dave)
def alias(tokens):
    pass

# Return a list of parsed items between delimiters.
def parse_sequence(tokens, start, end):
    pass

# Parse a list
def parse_list(tokens):
    return parse_sequence(tokens, '(', ')')

# Parse a dict
def parse_dict(tokens):
    return parse_sequence(tokens, '{', '}')

# Parse a 'term'
def parse_term(tokens):
    # Check for unexpected ends
    # list
    # dict
    # quote alias
    

# The main interface for other modules
# Yield a parsed token.
def parse(string):
    # Get the token lines.
    tokenLines = tokenize(string)
    # TODO: Yield?
    if len(tokenLines) == 0:
        return None

    # Loop through the lines
