# Cascade User Manual

## Installation

See `scripts/install.sh` and [VSCode extension instructions](../vscode-extension/README.md).

## Usage

- Run a file: `python -m compiler your_program.casc`
- Run tests: `pytest tests/`
- Build VSCode extension: see `vscode-extension/`

## Language Reference

- Variables: `pour 3 into a:depth`
- Functions: `pool add(a:depth, b:depth):depth { return a + b }`
- Types: `reservoir WaterSample { ... }`
- Control: `if stream splits { ... } else { ... }`
- More: See [LANGUAGE_SPEC.md](LANGUAGE_SPEC.md)

## CLI Options

- `--compile-only` : Only check and compile, do not run
- `--debug` : Print AST and internal state
- `--verbose` : Extra output
- `--output <file>` : Output result to file

## Error Codes

- 1001: Type error
- 2001: Semantic error
- 3001: Syntax error
- 9001: Runtime error

## FAQ

...
