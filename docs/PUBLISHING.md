# Publishing Cascade

## PyPI

1. Build the package:
   ```
   python setup.py sdist bdist_wheel
   ```
2. Upload to PyPI:
   ```
   pip install twine
   twine upload dist/*
   ```

## npm/VSCode Marketplace

1. Build extension:
   ```
   cd vscode-extension
   npm install
   npm run compile
   ```
2. Package and publish:
   ```
   npm install -g vsce
   vsce package
   vsce publish
   ```
   (You need a publisher account on the VSCode Marketplace.)

## Install locally

- CLI: `pip install .`
- VSCode: Use `code --install-extension cascade-vscode-*.vsix`