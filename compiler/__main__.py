# Entry point for Cascade CLI (python -m compiler)

import sys
from compiler.parser import parse_cascade
from compiler.type_checker import check_type, TypeEnv, TypeError
from compiler.semantic_analyzer import analyze_semantics, SemanticError
from compiler.interpreter import run_program, CascadeRuntimeError
import compiler.diagnostics as diagnostics

def main():
    if len(sys.argv) < 2:
        print("Usage: cascade <source_file>")
        sys.exit(1)
    source_file = sys.argv[1]
    with open(source_file, "r") as f:
        code = f.read()

    try:
        ast = parse_cascade(code)
    except Exception as e:
        diagnostics.syntax_error(str(e))
        sys.exit(1)
    type_env = TypeEnv()
    try:
        check_type(ast, type_env)
    except TypeError as e:
        diagnostics.type_error(str(e))
        sys.exit(1)
    try:
        analyze_semantics(ast)
    except SemanticError as e:
        diagnostics.semantic_error(str(e))
        sys.exit(1)

    try:
        env, functions, types = run_program(ast)
    except CascadeRuntimeError as e:
        diagnostics.runtime_error(str(e))
        sys.exit(1)

if __name__ == "__main__":
    main()