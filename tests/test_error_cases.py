# Tests for error handling in compiler pipeline

import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'compiler')))
from compiler.parser import parse_cascade
from compiler.type_checker import check_type, TypeEnv, TypeError
from compiler.semantic_analyzer import analyze_semantics, SemanticError

def test_type_error():
    code = "pour 'abc' into num:depth"
    ast = parse_cascade(code)
    type_env = TypeEnv()
    try:
        check_type(ast, type_env)
        assert False, "Expected TypeError"
    except TypeError:
        pass

def test_semantic_error():
    code = """
pour 1 into a:depth
pour 2 into a:depth
"""
    ast = parse_cascade(code)
    try:
        analyze_semantics(ast)
        assert False, "Expected SemanticError"
    except SemanticError:
        pass

if __name__ == "__main__":
    test_type_error()
    test_semantic_error()
    print("Error handling tests passed.")