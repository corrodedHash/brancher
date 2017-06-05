#!/bin/python

import random
import math
import Node
import Util
import IfGen



def generate_code(variables, functions, root, indentation):
    result = "#include \"klee/klee.h\"\n\n"
    for x in functions:
       result += IfGen.gen_function(x, indentation) + "\n"
    
    result += "int main(int argc, char** args) {\n"
    for x in variables:
        result += indentation + "int " + x + "; "
        result += indentation+ ("klee_make_symbolic(&%s, sizeof(%s), \"%s\");\n" % (x, x, x)) 
    result += indentation + "klee_open_merge();\n" 
    result += IfGen.gen_tree(variables, functions, root, 1, indentation)
    result += indentation + "klee_close_merge();\n" 
    result += "}\n"
    return result


VAR = ["var_" + str(x) for x in range(1, 5)]
FUN = [("fun_" + str(x), Util.log_weight_random(1, 4, 4)) for x in range(1, 3)]
ROOT = Node.createTree(3, 2, 3)
INDENT = "  "

print(generate_code(VAR, FUN, ROOT, INDENT))
