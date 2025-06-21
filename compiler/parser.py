# Orchestrator for Cascade parsing using the hand-written parser.
# This allows for future replacement with a PEG-generated parser.

from compiler.cascade_parser import parse

def parse_cascade(code):
    """Parse Cascade code to AST (wrapper for cascade_parser.parse)."""
    return parse(code)