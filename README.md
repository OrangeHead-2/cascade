# Cascade Language Project

Cascade is a statically-typed, human-friendly programming language and toolchain for data processing, scripting, and education.  
This repository contains the full Cascade ecosystem: compiler/interpreter, standard library, test suite, CLI, Language Server (LSP), and a VSCode extension.

---

## Features

- **Modern Language**: Statically typed, readable syntax, robust semantics
- **Standard Library**: Extensive built-in functions for numbers, strings, lists, and more
- **Compiler/Interpreter**: Parse, type-check, run, and debug Cascade code
- **Test Suite**: Unit and integration tests for all components
- **Powerful CLI**: Compile, check, run, debug, output results
- **IDE Support**: Language Server (LSP) for code completion, diagnostics, go-to-definition, hover info, and outline
- **VSCode Extension**: Syntax highlighting, completion, and LSP integration
- **Cross-platform**: Runs anywhere Python 3.8+ and Node.js (for VSCode extension) are available

---

## Quick Start

### 1. Clone & Install

```sh
git clone https://github.com/OrangeHead-2/cascade.git
cd cascade
python3 -m venv venv
source venv/bin/activate     # On Windows: venv\Scripts\activate
pip install -r requirements.txt
pip install .                # Optional: install as CLI
```

### 2. Run a Cascade Program

```sh
python -m compiler examples/fizzbuzz.casc
# Or, if installed:
cascade examples/fizzbuzz.casc
```

### 3. Run Tests

```sh
pytest tests/
```

### 4. Use Advanced CLI Options

```sh
cascade yourprog.casc --compile-only      # Type-check only, no run
cascade yourprog.casc --debug             # Print AST and internal state
cascade yourprog.casc --verbose           # More output
cascade yourprog.casc --output result.txt # Output results to file
```

### 5. Editor/IDE Support

#### VSCode Extension

```sh
cd vscode-extension
npm install
npm run compile
npm install -g vsce
vsce package
# In VSCode: Install .vsix via "Extensions: Install from VSIX"
```
Or search for "Cascade" in the VSCode Marketplace (if published).

#### Language Server (LSP)

```sh
python -m compiler.lsp_server
```
Most editors supporting LSP can integrate with this server.

---

## Project Structure

- `compiler/`    : Main compiler/interpreter, stdlib, diagnostics, CLI, LSP
- `tests/`      : Unit and integration tests
- `examples/`    : Example Cascade programs
- `vscode-extension/` : VSCode extension (syntax, LSP client, etc.)
- `docs/`      : User manual, language spec, contributing, publishing

---

## Documentation

- [User Manual](docs/USER_MANUAL.md)
- [Language Specification](docs/LANGUAGE_SPEC.md)
- [Contributing Guide](docs/CONTRIBUTING.md)
- [Publishing Instructions](docs/PUBLISHING.md)

---

## Build & Packaging

- **PyPI**: `python setup.py sdist bdist_wheel`, then `twine upload dist/*`
- **NPM/VSCode**: `cd vscode-extension && npm run compile && vsce package && vsce publish`

See [docs/PUBLISHING.md](docs/PUBLISHING.md) for full publishing details.

---

## Contribution

Contributions welcome!  
See [CONTRIBUTING.md](docs/CONTRIBUTING.md) for how to get started, code style, and submitting PRs.

---

## License

MIT License

---

## Acknowledgements

Cascade is inspired by modern statically-typed and dataflow languages, and the open-source language development community.
