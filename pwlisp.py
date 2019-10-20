# Main program
import sys, traceback
import modules.pwl_types as types
from modules.parser import parse
from modules.env import Environment
import modules.io as io
from modules.builtin import builtInFunctions

# Read
def Read(string):
    return parse(string)

# Evaluate list helper
def eval_list(exp, environment):
    # print('eval_list',repr(exp))
    if type(exp) == types.Symbol:
        return environment.get(exp)
    if type(exp) == types.List:
        result = types.List(Evaluate(x, environment) for x in exp)
        return result
    return exp

def print_debug(message, depth):
    print(str(depth).rjust(4)+'  '*depth + '| ' + message)

debug = False
depth = 0

# Evaluate
def Evaluate(exp, environment):
    global debug
    global depth
    depth += 1

    if debug:
        print_debug('Evaluate: {} {}'.format(exp, str(types.pwl_type(exp))), depth)

    while True:
        # macroexpand

        if type(exp) != types.List:
            depth -= 1
            return eval_list(exp, environment)

        if len(exp) == 0:
            depth -= 1
            return exp


        # Special forms

        # Define
        if exp[0] == 'define':
            definition = Evaluate(exp[2], environment)
            if type(definition) == types.Function:
                definition.name = exp[1]
            depth -= 1
            return environment.set(exp[1], definition)
        # Define macro
        # Quote
        elif exp[0] == 'quote':
            depth -= 1
            return exp[1]
        # Import
        elif exp[0] == 'import':
            file_name = Evaluate(exp[1], environment)
            contents = open(file_name).read()
            result = parse(contents, file_name)
            for item in result:
                if debug:
                    print_debug('\nImport result: {}'.format(repr(item)), depth)
                Evaluate(item, environment)
            depth -= 1
            return "Success."
        # If
        elif exp[0] == 'if':
            condition = Evaluate(exp[1], environment)
            exp = exp[2] if condition else exp[3]

        # Or
        elif exp[0] == 'or':
            evaluands = exp[1:]
            result = None
            for item in evaluands:
                result = Evaluate(item, environment)
                if result:
                    break
            depth -= 1
            return result
        # And
        elif exp[0] == 'and':
            evaluands = exp[1:]
            result = None
            for item in evaluands:
                result = Evaluate(item, environment)
                if not result:
                    break
            depth -= 1
            return result
        # Try/catch
        # Env
        elif exp[0] == 'env':
            if len(exp) > 1:
                if environment.find(exp[1]):
                    result = environment.get(exp[1])
                else:
                    result = '{} was not found.'.format(exp[1])
            else:
                result = str(environment)
            depth -= 1
            return result

        # For debugging.
        elif exp[0] == 'debug':
            debug = not debug
            exp = debug

        elif exp[0] == 'let':
            #(let (a 7 b 8) (+ 1 b))
            # Make a new environment with a = 7, b = 8
            # Evaluate exp[2] using new environment
            new_env = Environment(environment)
            if type(exp[1]) != types.List:
                raise types.Error('Expected a binding list, got {}.'.format(exp[1]))
                return None
            bindlist = types.List(exp[1])
            if len(bindlist) % 2 != 0:
                raise types.Error('Missing argument for bind list: {}'.format(str(exp[1])))
            while bindlist:
                if debug:
                    print_debug('let binding {} to {}.'.format(bindlist[0], bindlist[1]), depth)
                new_env.set(bindlist[0], Evaluate(bindlist[1], new_env))
                bindlist = bindlist[2:]
            if debug:
                print_debug('let environment:\n{}'.format(str(new_env)), depth)
            exp = exp[2]
            environment = new_env
        # Do - Evaluate everything in the list and return only the last result
        elif exp[0] == 'do':
            exp = exp[1:]
            result = eval_list(exp, environment)
            exp = result[-1]
        # Function
        elif exp[0] == 'function':
            func = exp[0]
            params = exp[1]
            body = exp[2]
            if debug:
                print_debug('Function created with: {} {}.'.format(params, body), depth)
            fn = types.Function('user function', None,
                params,
                environment,
                body,
                user = True)
            depth -= 1
            return fn
        # Else apply function
        else:
            items = eval_list(exp, environment)
            func = items[0]
            if debug:
                print_debug('Executing: {}'.format(str(func)), depth)
                print_debug('     Args: {}'.format(str(items[1:])), depth)
            if func.is_builtin:
                depth -= 1
                return func(*items[1:])
            environment = Environment(func.env, func.params, items[1:])
            exp = func.expression
            # Tail call optimization

# Print
def Print(expression):
    return io.stringify(expression)

# Read/evaluate/print helper
# This allows us to execute from within this file
def ReadEvalPrint(string, environment):
    contents = Read(string)
    result = ""
    for item in contents:
        result += Print(Evaluate(item, environment)) + '\n'
    return result

# Set up the root environment
root_environment = Environment()
for key, value in builtInFunctions.items():
    root_environment.set(key, types.Function(key, value, [], root_environment, builtin = True))

# eval
root_environment.set('eval', types.Function('eval', lambda x: Evaluate(x, root_environment), [], root_environment, builtin = True))

# import
# ReadEvalPrint('(define import (function (x) (eval (parse (readfile x)))))', root_environment)

# argv
root_environment.set(types.Symbol('*argv*'), types.List(sys.argv[1] if len(sys.argv) > 1 else types.List()))

# Loop - The main loop
if __name__ == '__main__':
    while True:
        line = input('PWLisp> ')
        if not line:
            break
        try:
            print(ReadEvalPrint(line, root_environment))
        except EOFError:
            break
        except types.Error as e:
            print('Error: {}\n'.format(e))
        except Exception as e:
            print("".join(traceback.format_exception(*sys.exc_info())))
