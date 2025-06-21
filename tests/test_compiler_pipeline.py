# Integration test for Cascade parse/typecheck/semantics/interpreter

import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'compiler')))
from compiler.parser import parse_cascade
from compiler.type_checker import check_type, TypeEnv
from compiler.semantic_analyzer import analyze_semantics
from compiler.interpreter import run_program

def test_basic_cascade_program():
    code = """
pour 3.14 into pi:depth
pour [1,2,3] into nums:[depth]
pool add(a:depth, b:depth):depth { pour a + b into sum:depth }
"""
    ast = parse_cascade(code)
    type_env = TypeEnv()
    check_type(ast, type_env)
    analyze_semantics(ast)
    env, functions, types = run_program(ast)
    assert env.get("pi") == 3.14
    assert env.get("nums") == [1,2,3]
    assert "add" in functions

if __name__ == "__main__":
    test_basic_cascade_program()
    print("Integration test passed.")