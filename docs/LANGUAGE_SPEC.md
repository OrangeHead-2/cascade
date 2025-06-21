# Cascade Language Specification

## Overview

Cascade is a statically typed, dataflow-inspired language for robust, readable, and maintainable data processing.

## Syntax

- See PEG grammar in `compiler/cascade.pegjs`
- Statements: Variable declarations, assignments, function declarations, type definitions, control structures.

## Types

- `depth`: numeric (float)
- `rivulet`: string
- `drop`: boolean
- `map`: key-value
- User-defined types via `reservoir`

## Expressions

...

## Standard Library

- See `compiler/stdlib.py` for all built-ins

## Error Handling

- Errors provide line/col, error code, stack trace if possible

...
