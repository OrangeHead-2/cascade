# Cascade Programming Language – Project Structure Overview

**Cascade** is a flow-based programming language inspired by water metaphors, with visual data flow, natural language syntax, and first-class pattern matching.

---

## File & Directory Structure

```
project_name/
├── fountain.config      # Main project configuration (JSON)
├── flow.lock            # Dependency version locking
├── cascade.ignore       # Compilation ignore rules
├── sources/             # Main source files (.casc)
├── pools/               # Function libraries (.pool)
├── streams/             # Data flow definitions (.stream)
├── reservoirs/          # Data storage/types (.res)
├── filters/             # Data transformation modules (.filter)
├── tests/               # Test suites
│   ├── unit/            # For pools
│   ├── flow/            # Integration
│   ├── pressure/        # Performance
│   └── purity/          # Type checks/validation
├── docs/                # Documentation
├── channels/            # Module imports
│   ├── external/        # External libraries
│   └── internal/        # Shared project code
├── rapids/              # Build artifacts
│   ├── debug/
│   ├── release/
│   └── artifacts/
└── wellspring/          # Local package cache
```

---

## Directory/Component Details

- **fountain.config**: Main configuration, including dependencies (JSON).
- **flow.lock**: Locks dependency versions for reproducible builds.
- **cascade.ignore**: Lists files/directories to exclude from build.
- **sources/**: Entry points, each `.casc` file defines a program flow.
- **pools/**: Reusable functions, called “pools”, stored as `.pool`.
- **streams/**: Data pipelines, transformations; `.stream` files.
- **reservoirs/**: Data structure/type definitions; `.res` files.
- **filters/**: Data validation/transformation modules; `.filter`.
- **tests/**: Organized by type (`unit`, `flow`, `pressure`, `purity`).
- **docs/**: Markdown or other documentation files.
- **channels/**: "Imports" system
  - **external/**: Third-party libraries.
  - **internal/**: Shared modules within the project.
- **rapids/**: Build outputs
  - **debug/**, **release/**, **artifacts/**: Build stages.
- **wellspring/**: Local package cache for dependencies.

---

## Import System

- Uses **channels/** for modular imports.
- Use **external/** for third-party, **internal/** for project modules.

---

## Water-Based Concepts

- **Code as Flow:** Top-to-bottom execution, visualized as water.
- **Natural Language:** Syntax inspired by water metaphors.
- **Pattern Matching:** First-class, built-in.
- **Built-in Visualization:** Real-time data flow diagrams.

---

## Example Entry (`sources/main.casc`)

```casc
from pool:filter_even_numbers draw stream:input_numbers into reservoir:even_numbers
```

---

*This structure provides clarity, modularity, and supports Cascade's unique water-flow paradigm. Adapt directories as your project scales!*