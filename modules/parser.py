# Parse tokenized input.
# The tokenizer returns a token line with the line number set.
# If this is just readline, it will always be zero.
# Otherwise, it will be the line number in the file.

import re
from .tokenizer import tokenize, Reader
import modules.pwl_types as types

# Parse atom - token is a string
# Return item
def parse_atom(token):
    '''
    Parse an atom.

    >>> parse_atom('123')
    123
    >>> parse_atom(':a')
    <PWLisp key :a>
    >>> parse_atom('list')
    <PWLisp symbol list>
    >>> parse_atom('a')
    <PWLisp symbol a>
    '''
    # Regex for int and float
    int_pattern = re.compile(r"-?[0-9]+$")
    float_pattern = re.compile(r"-?[0-9][0-9.]*$")

    # int
    if re.match(int_pattern, token):
        return int(token)
    # float
    if re.match(float_pattern, token):
        return float(token)

    # string
    if token[0] == '"':
        if token [-1] == '"':
            return str(token[1:-1])
        raise types.Error('Expected a close \"')

    # key
    if token[0] == ':':
        return types.Key(token[1:])

    # nil
    if token == 'nil':
        return None

    # true
    if token == 'true':
        return True

    # false
    if token == 'false':
        return False

    # Default: symbol
    return types.Symbol(token)

# Swap out aliases - ' for quote
# Return list of parsed tokens 'dave = (quote dave)
def alias(tokens, file_name, func):
    '''
    Return a PWLisp List with the alias replace with func.

    >>> tokens = tokenize("'(1 2 3)")
    >>> alias(tokens, 'console', 'quote')
    <PWLisp list (quote (1 2 3))>
    '''
    tokens.consume()
    result = types.List([types.Symbol(func)])
    result.append(parse_expression(tokens, file_name))
    return result

# Return a list of parsed items between delimiters.
def parse_sequence(tokens, file_name, type, start, end):
    ast = []
    token = tokens.consume() # Get rid of start
    if token != start:
        raise Exception('Expected {} in line {} of {}.'.format(start, tokens.get_line() + 1, file_name))

    token = tokens.look_ahead()
    while token != end:
        if token == None:
            raise Exception('Expected {} in line {} of {}.'.format(end, tokens.get_line() + 1, file_name))
        ast.append(parse_expression(tokens, file_name))
        token = tokens.look_ahead()
    tokens.consume() # Get rid of end
    return type(ast)

# Parse a list
def parse_list(tokens, file_name):
    return parse_sequence(tokens, file_name, types.List, '(', ')')

# Parse a dict
def parse_dict(tokens, file_name):
    return parse_sequence(tokens, file_name, types.Dict, '{', '}')

# Parse 'expression'
def parse_expression(tokens, file_name):
    '''
    Parse an expression from TokenList.

    >>> tokens = tokenize(')')
    >>> parse_expression(tokens, 'console input')
    Traceback (most recent call last):
    ...
    Exception: Unexpected ) in line 0 of console input.
    '''

    token = tokens.look_ahead()
    # Check for unexpected ends
    if token in (')', '}'):
        raise Exception("Unexpected {} in line {} of {}.".format(token, tokens.get_line()+1, file_name))

    # list
    elif token == '(':
        return parse_list(tokens, file_name)

    # dict
    elif token == '[':
        return parse_dict(tokens, file_name)

    # quote alias
    elif token == '\'':
        return alias(tokens, file_name, 'quote')

    # default atom
    tokens.consume()
    return parse_atom(token)

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

    result = types.List()
    tokens = tokenize(string)
    while tokens.look_ahead():
        result.append(parse_expression(tokens, file_name))
    return result

    # yield parse_expression(tokenize(string), file_name)
