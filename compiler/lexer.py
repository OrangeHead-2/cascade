# Lexer for Cascade language.
# Splits source text into tokens with line/col info for error reporting.
import re

TOKEN_SPEC = [
    ('NUMBER',   r'\d+(\.\d+)?'),
    ('STRING',   r'"([^"\\]|\\.)*"'),
    ('IDENT',    r'[a-zA-Z_][a-zA-Z0-9_]*'),
    ('OP',       r'==|!=|<=|>=|&&|\|\||[+\-*/<>=,:\[\]{}()]'),
    ('NEWLINE',  r'\n'),
    ('SKIP',     r'[ \t]+'),
    ('COMMENT',  r'\#.*'),
    ('MISMATCH', r'.'),
]

TOKEN_RE = re.compile('|'.join(f'(?P<{name}>{regex})' for name, regex in TOKEN_SPEC))

def tokenize(code):
    """Tokenizes Cascade source code into a list of tokens with line/col."""
    line_num = 1
    line_start = 0
    tokens = []
    for mo in TOKEN_RE.finditer(code):
        kind = mo.lastgroup
        value = mo.group()
        if kind == 'NEWLINE':
            line_num += 1
            line_start = mo.end()
        elif kind == 'SKIP' or kind == 'COMMENT':
            continue
        elif kind == 'MISMATCH':
            raise RuntimeError(f'Unexpected {value!r} at line {line_num}')
        else:
            col = mo.start() - line_start
            tokens.append({'type': kind, 'value': value, 'line': line_num, 'col': col})
    return tokens