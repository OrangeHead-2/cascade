# CLI for Cascade language.
# Supports --compile-only, --debug, --verbose, --output.

import argparse
import sys
from compiler.parser import parse_cascade
from compiler.type_checker import check_type, TypeEnv
from compiler.semantic_analyzer import analyze_semantics
from compiler.interpreter import run_program
import compiler.diagnostics as diagnostics

def main():
    parser = argparse.ArgumentParser(description="Cascade CLI")
    parser.add_argument("file", help="Path to Cascade source file")
    parser.add_argument("--compile-only", action="store_true", help="Only typecheck and compile, do not run")
    parser.add_argument("--debug", action="store_true", help="Print AST and internal state")
    parser.add_argument("--verbose", action="store_true", help="More output")
    parser.add_argument("--output", help="Output file")
    args = parser.parse_args()

    with open(args.file) as f:
        code = f.read()

    try:
        ast = parse_cascade(code)
        if args.debug:
            print("AST:", ast)
        type_env = TypeEnv()
        check_type(ast, type_env)
        analyze_semantics(ast)
    except Exception as e:
        diagnostics.report_error(str(e), exc=e)
        sys.exit(1)

    if args.compile_only:
        print("Compilation successful.")
        sys.exit(0)

    try:
        env, functions, types = run_program(ast)
        if args.output:
            with open(args.output, "w") as outf:
                outf.write(str(env.vars))
        elif args.verbose:
            print("Final environment:", env.vars)
    except Exception as e:
        diagnostics.report_error(str(e), exc=e)
        sys.exit(1)

if __name__ == "__main__":
    main()