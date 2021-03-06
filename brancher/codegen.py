"""Contains functions to generate C code"""
import random
from typing import List, Tuple

from . import node, util


class CodeGenerator:
    """Generates code"""

    def __init__(self, var_count: int, fun_count: int, indent: str = "  ") -> None:
        self.variables: List[str] = ["var_" + str(x) for x in range(1, var_count + 1)]
        self.functions: List[Tuple[str, int]] = [
            ("fun_" + str(x), util.log_weight_random(1, 4, 4))
            for x in range(1, fun_count + 1)
        ]

        self._indent = indent

    def gen_stuff(self, level: int) -> str:
        """Generates a few lines of assignments and function calls"""
        result = ""
        for _ in range(1, util.log_weight_random(2, 10)):
            result += (
                (level * self._indent)
                + gen_assignment(self.variables, self.functions)
                + ";\n"
            )
        return result

    def gen_tree(self, tree: node.Node, level: int = 0) -> str:
        """Generates nested if clauses based on given tree"""

        def print_if_statement(which: str, level: int) -> str:
            """Print the keyword to the if branch"""
            result = self._indent * level
            if which == "first":
                result += "if (" + gen_clause(self.variables) + ")"
            elif which == "last":
                result += "else"
            else:
                result += "else if (" + gen_clause(self.variables) + ")"
            return result

        def print_if_clause(
            cur_node: node.Node, which: str, level: int, start: bool = False
        ) -> str:
            """Print the clause for an if statement"""
            result = ""
            if start:
                level -= 1
            if not start:
                result = print_if_statement(which, level) + " {\n"
                result += self.gen_stuff(level + 1)
            if cur_node.get_children():
                child_list = list(cur_node.get_children())
                result += print_if_clause(child_list[0], "first", level + 1)

                for child in child_list[1:-1]:
                    result += print_if_clause(child, "middle", level + 1)

                result += print_if_clause(child_list[-1], "last", level + 1)
            if not start:
                result += self._indent * level + "}\n"
            return result

        return print_if_clause(tree, "first", level, True)


def gen_function(name: str, var_count: int, indent: str = "  ") -> str:
    """Generates a function with given function name"""
    my_cg = CodeGenerator(var_count, 0, indent)

    parameters = my_cg.variables
    parameter_list = ", ".join(parameters)

    my_cg.variables.append("result")

    result = "int " + name + " (" + parameter_list + ") {\n"
    result += indent + "int result = " + str(random.randint(0, 200)) + ";\n"
    result += my_cg.gen_tree(node.create_tree(3, 2, 3, 5), level=1)
    result += indent + "return result;\n"
    result += "}\n"
    return result


def gen_clause(variables: List[str]) -> str:
    """Generates a boolean statement with given variables"""
    var = random.choice(variables)
    operator = random.choice(["%", "<", ">"])
    if operator == "%":
        return var + " " + operator + " " + str(random.randint(2, 30)) + " == 0"
    random_comparison_int = str(random.randint(1, 9) * (10 ** random.randint(1, 3)))
    return f"{var} {operator} {random_comparison_int}"


def gen_term(variables: List[str]) -> str:
    """Generates a term using given variables"""
    if random.randint(1, 10) == 1:
        return str(random.randint(5, 200))
    num_vars = util.log_weight_random(1, len(variables), 1.5)
    chosen_vars = random.sample(variables, num_vars)
    result = chosen_vars[0]
    for cur_var in chosen_vars[1:]:
        operator = random.choice(["+", "-", "*"])
        result += f" {operator} {cur_var}"
    return result


def gen_function_call(variables: List[str], functions: List[Tuple[str, int]]) -> str:
    """Generates a function call"""
    cur_fun = random.choice(functions)
    cur_vars = random.sample(variables, cur_fun[1])
    argument_list = ", ".join(cur_vars)
    return cur_fun[0] + "(" + argument_list + ")"


def gen_assignment(variables: List[str], functions: List[Tuple[str, int]]) -> str:
    """Generates assignment to random variable"""
    var = random.choice(variables)
    if functions and random.randint(1, 10) < 3:
        return f"{var} = {gen_function_call(variables, functions)}"
    return f"{var} = {gen_term(variables)}"
