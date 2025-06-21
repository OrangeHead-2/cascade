# Diagnostics and Error Reporting for Cascade Compiler

import traceback

def report_error(msg, code=None, line=None, col=None, exc=None):
    """Prints a detailed error message, optionally including stack trace."""
    prefix = "[CascadeError]"
    linecol = f" at line {line}, col {col}" if line is not None and col is not None else ""
    code_str = f" [E{code}]" if code else ""
    print(f"{prefix}{code_str}{linecol}: {msg}")
    if exc:
        print(traceback.format_exc())

def type_error(msg, line=None, col=None, code=1001, exc=None):
    """Report a type error (code 1001)."""
    report_error(msg, code=code, line=line, col=col, exc=exc)

def semantic_error(msg, line=None, col=None, code=2001, exc=None):
    """Report a semantic error (code 2001)."""
    report_error(msg, code=code, line=line, col=col, exc=exc)

def syntax_error(msg, line=None, col=None, code=3001, exc=None):
    """Report a syntax error (code 3001)."""
    report_error(msg, code=code, line=line, col=col, exc=exc)

def runtime_error(msg, line=None, col=None, code=9001, exc=None):
    """Report a runtime error (code 9001)."""
    report_error(msg, code=code, line=line, col=col, exc=exc)