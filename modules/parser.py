# Parse tokenized input.
# The tokenizer returns a token line with the line number set.
# If this is just readline, it will always be zero.
# Otherwise, it will be the line number in the file.

from tokenizer import tokenize, TokenLine
import pwl_types as types

# Parse atom - token is a string
# Return item
def parse_atom(token, file_name):
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
def alias(tokens, file_name):
    pass

# Return a list of parsed items between delimiters.
def parse_sequence(tokens, file_name, start, end):
    pass

# Parse a list
def parse_list(tokens, file_name):
    return parse_sequence(tokens, '(', ')')

# Parse a dict
def parse_dict(tokens, file_name):
    return parse_sequence(tokens, '{', '}')

# Parse a 'term'
def parse_term(tokens, file_name):
    # Check for unexpected ends
    # list
    # dict
    # quote alias
    # default atom

# The main interface for other modules
# Yield a parsed token.
def parse(string, file_name = 'console input'):
    """
    Yields a PWLisp object. This will be one of:
    list
    dict
    atom

    Atoms are:
    int
    float
    key
    string
    nil
    true
    false

    If a file name is provided, that will be used when printing out parse
    errors.
    """
    # Get the token lines.
    tokenLines = tokenize(string)
    if len(tokenLines) == 0:
        return None

    # Loop through the lines
    for x in tokenLines:
        yield parse_term(x, file_name)
