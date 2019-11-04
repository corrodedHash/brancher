#!/bin/python
"""Main file"""

from . import node
from . import codegen


def generate_code(root: node.Node, indentation: str) -> str:
    """Generates the whole code file"""
    result = "#include \"klee/klee.h\"\n\n"
    my_cg = codegen.CodeGenerator(5, 3)

    for cur_fun in my_cg.functions:
        result += codegen.gen_function(cur_fun[0], cur_fun[1], indentation) + "\n"

    result += "int main(int argc, char** args) {\n"
    for cur_var in my_cg.variables:
        result += indentation + "int " + cur_var + "; "
        result += indentation + \
            ("klee_make_symbolic(&%s, sizeof(%s), \"%s\");\n" % (cur_var, cur_var, cur_var))

    result += indentation + "klee_open_merge();\n"
    result += my_cg.gen_tree(root, level=1)
    result += indentation + "klee_close_merge();\n"
    result += "}"
    return result


if __name__ == "__main__":
    ROOT = node.create_tree(3, 2, 3)
    INDENT = "  "

    print(generate_code(ROOT, INDENT))
