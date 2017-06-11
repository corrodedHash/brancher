"""Contains functions to generate C code"""
import random

import util
import node


class CodeGenerator:
    """Generates code"""
    def __init__(self, var_count, fun_count, indent="  "):
        self.variables = ["var_" + str(x) for x in range(1, var_count + 1)]
        self.functions = [
            ("fun_" + str(x),
             util.log_weight_random(
                 1,
                 4,
                 4)) for x in range(
                     1,
                     fun_count + 1)]

        self._indent = indent

    def gen_stuff(self, level):
        """Generates a few lines of assignments and function calls"""
        result = ""
        for _ in range(1, util.log_weight_random(2, 10)):
            result += (level * self._indent) + \
                gen_assignment(self.variables, self.functions) + ";\n"
        return result

    def gen_tree(self, tree, level=0):
        """Generates nested if clauses based on given tree"""
        def print_if_statement(which, level):
            """Print the keyword to the if branch"""
            result = self._indent * level
            if which == "first":
                result += "if (" + gen_clause(self.variables) + ")"
            elif which == "last":
                result += "else"
            else:
                result += "else if (" + gen_clause(self.variables) + ")"
            return result

        def print_if_clause(cur_node, which, level, start=False):
            """Print the clause for an if statement"""
            result = ""
            if start:
                level -= 1
            if not start:
                result = print_if_statement(which, level) + " {\n"
                result += self.gen_stuff(level + 1)
            if cur_node.getChildren():
                child_list = list(cur_node.getChildren())
                result += print_if_clause(child_list[0], "first", level + 1)

                for child in child_list[1:-1]:
                    result += print_if_clause(child, "middle", level + 1)

                result += print_if_clause(child_list[-1], "last", level + 1)
            if not start:
                result += self._indent * level + "}\n"
            return result

        return print_if_clause(tree, "first", level, True)


def gen_function(function, indent="  "):
    """Generates a function with given function name"""
    my_cg = CodeGenerator(function[1], 0, indent)
    name = function[0]
    parameters = my_cg.variables
    result = "int " + name + " (" + ", ".join(parameters) + ") {\n"
    result += indent + "int result = " + str(random.randint(0, 200)) + ";\n"
    my_cg.variables.append("result")
    result += my_cg.gen_tree(node.create_tree(3, 2, 3, 5), level=1)
    result += indent + "return result;\n"
    result += "}\n"
    return result


def gen_clause(variables):
    """Generates a boolean statement with given variables"""
    var = random.sample(variables, 1)[0]
    operator = random.choice(['%', '<', '>'])
    if operator == '%':
        return var + " " + operator + " " + \
            str(random.randint(2, 30)) + " == 0"
    return var + " " + operator + " " + \
        str(random.randint(1, 9) * (10 ** random.randint(1, 3)))


def gen_term(variables):
    """Generates a term using given variables"""
    if random.randint(1, 10) == 1:
        return str(random.randint(5, 200))
    num_vars = util.log_weight_random(1, len(variables), 1.5)
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
