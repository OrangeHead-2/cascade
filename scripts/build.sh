#!/bin/bash
set -e

echo "Building Cascade project..."
pip install -r requirements.txt
pytest tests/
cd vscode-extension
npm install
npm run compile
cd ..
echo "Build complete."