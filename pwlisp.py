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

# Evaluate
def Evaluate(exp, environment):
    print('Evaluate:', exp, str(type(exp)), 'depth:', depth)
    while True:
        # macroexpand

        if type(exp) != types.List:
            return eval_list(exp, environment)

        if len(exp) == 0:
            return exp


        # Special forms

        # Define
        if exp[0] == 'define':
            definition = Evaluate(exp[2], environment)
            return environment.set(exp[1], definition)
        # Define macro
        # Quote
        elif exp[0] == 'quote':
            return exp[1]
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
            return result
        # And
        elif exp[0] == 'and':
            evaluands = exp[1:]
            result = None
            for item in evaluands:
                result = Evaluate(item, environment)
                if not result:
                    break
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
            return result

        # Do - Evaluate everything in the list and return only the last result
        elif exp[0] == 'do':
            exp = exp[1:]
            result = eval_list(exp, environment)
            depth -= 1
            return result[-1]
        # Function
        elif exp[0] == 'function':
            func = exp[0]
            params = exp[1]
            print('function : params',func,':',params)
            body = exp[2]
            fn = types.Function('user function', None,
                params,
                environment,
                body)
            return fn
        # Else apply function
        else:
            items = eval_list(exp, environment)
            func = items[0]
            # print('func type:', type(func))
            if func.is_builtin:
                return func(*items[1:])
            environment = Environment(func.env, func.params, items[1:])
            print(func.expression)
            print('func.params:', func.params, items[1:])
            exp = func.expression
            # Tail call optimization

# Print
def Print(expression):
    return io.stringify(expression)

# Read/evaluate/print helper
# This allows us to execute from within this file
def ReadEvalPrint(string, environment):
    return Print(Evaluate(Read(string), environment))

# Set up the root environment
root_environment = Environment()
for key, value in builtInFunctions.items():
    root_environment.set(key, types.Function(key, value, [], root_environment, builtin = True))

# eval
root_environment.set('eval', types.Function('eval', lambda x: Evaluate(x, root_environment), [], root_environment, builtin = True))

# import
ReadEvalPrint('(define import (function (x) (eval (parse (readfile x)))))', root_environment)

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
            print('Error:',e)
        except Exception as e:
            print("".join(traceback.format_exception(*sys.exc_info())))
