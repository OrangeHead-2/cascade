#!/bin/bash
set -e

echo "Packaging Cascade toolchain..."
mkdir -p dist
tar czf dist/cascade-compiler.tar.gz compiler/ scripts/ requirements.txt
cd vscode-extension
npm run compile
npm install -g vsce
vsce package
mv *.vsix ../dist/
cd ..
echo "Packaging complete. Artifacts in dist/"