import random

import Util
import Node

def gen_clause(variables):
    """Generates a boolean statement with given variables"""
    var = random.sample(variables, 1)[0]
    operator = random.choice(['%', '<', '>'])
    if operator == '%':
        return var + " " + operator + " " + str(random.randint(2, 30)) + " == 0"
    return var + " " + operator + " " + str(random.randint(1, 9) * (10 ** random.randint(1, 3)))


def gen_term(variables):
    """Generates a term using given variables"""
    if random.randint(1, 10) == 1:
        return str(random.randint(5, 200))
    num_vars = Util.log_weight_random(1, len(variables), 1.5)
    chosen_vars = random.sample(variables, num_vars)
    result = chosen_vars[0]
    for cur_var in chosen_vars[1:]:
        result += " " + random.choice(["+", "-", "*"]) + " " + cur_var
    return result


def gen_function_call(variables, functions):
    """Generates a function call"""
    cur_fun = random.sample(functions, 1)[0]
    cur_vars = random.sample(variables, cur_fun[1])
    return cur_fun[0] + "(" + ", ".join(cur_vars) + ")"


def gen_assignment(variables, functions):
    """Generates assignment to random variable"""
    var = random.choice(variables)
    if functions and random.randint(1, 10) < 3:
        return var + " = " + gen_function_call(variables, functions)
    return var + " = " + gen_term(variables)


def gen_stuff(variables, functions, level, indent="  "):
    """Generates a few lines of assignments and function calls"""
    result = ""
    for _ in range(1, Util.log_weight_random(2, 10)):
        result += (level * indent) + \
            gen_assignment(variables, functions) + ";\n"
    return result


def gen_tree(variables, functions, tree, level=0, indent="  "):
    def print_if_statement(which, level):
        result = indent * level
        if which == "first":
            result += "if (" + gen_clause(variables) + ")"
        elif which == "last":
            result += "else"
        else:
            result += "else if (" + gen_clause(variables) + ")"
        return result

    def print_if_clause(node, which, level, start=False):
        result = ""
        if start:
            level -= 1
        if not start:
            result = print_if_statement(which, level) + " {\n"
            result += gen_stuff(variables, functions, level + 1, indent)
        if node.getChildren():
            child_list = list(node.getChildren())
            result += print_if_clause(child_list[0], "first", level + 1)

            for child in child_list[1:-1]:
                result += print_if_clause(child, "middle", level + 1)

            result += print_if_clause(child_list[-1], "last", level + 1)
        if not start:
            result += indent * level + "}\n"
        return result

    return print_if_clause(tree, "first", level, True)


def gen_function(function, indent="  "):
    name = function[0]
    parameters = ["in_" + str(x) for x in range(1, function[1] + 1)]
    result = "int " + name + " (" + ", ".join(parameters) + ") {\n"
    result += indent + "int result = " + str(random.randint(0, 200)) + ";\n"
    result += gen_tree(parameters + ["result"],
                       [], Node.createTree(3, 2, 3, 5), 1, indent)
    result += indent + "return result;\n"
    result += "}\n"
    return result
