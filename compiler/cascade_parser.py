# Cascade Recursive Descent Parser
# This parser turns Cascade source code into an AST.
# For production, replace with a PEG-generated parser for improved coverage and correctness.

from compiler.lexer import tokenize

class ParseError(Exception):
    """Raised when parsing fails due to invalid Cascade syntax."""
    def __init__(self, message, line, col):
        super().__init__(f"ParseError: {message} at {line}:{col}")
        self.line = line
        self.col = col

class Parser:
    """Parser for the Cascade language source code."""
    def __init__(self, code):
        self.tokens = tokenize(code)
        self.pos = 0

    def peek(self):
        """Return the next token or None if at end."""
        if self.pos < len(self.tokens):
            return self.tokens[self.pos]
        return None

    def advance(self):
        """Move to the next token."""
        if self.pos < len(self.tokens):
            self.pos += 1

    def expect(self, typ, value=None):
        """Consume a token of type 'typ' (and value if provided), or raise error."""
        tok = self.peek()
        if not tok or tok['type'] != typ or (value is not None and tok['value'] != value):
            raise ParseError(f"Expected {typ} {value if value else ''}", tok['line'] if tok else -1, tok['col'] if tok else -1)
        self.advance()
        return tok

    def parse(self):
        """Parse the entire input into an AST program node."""
        stmts = []
        while self.peek():
            stmts.append(self.parse_statement())
        return {'type': 'Program', 'body': stmts}

    def parse_statement(self):
        """Parse a top-level statement."""
        tok = self.peek()
        if tok and tok['type'] == 'IDENT' and tok['value'] == 'pour':
            return self.parse_var_decl()
        if tok and tok['type'] == 'IDENT' and tok['value'] == 'pool':
            return self.parse_func_decl()
        # Extend for other statement types: assignment, const, if, etc.
        raise ParseError("Unknown or unsupported statement", tok['line'], tok['col'])

    def parse_var_decl(self):
        """Parse a variable declaration statement."""
        self.expect('IDENT', 'pour')
        value = self.parse_expression()
        self.expect('IDENT', 'into')
        name = self.expect('IDENT')['value']
        typ = None
        if self.peek() and self.peek()['type'] == 'OP' and self.peek()['value'] == ':':
            self.expect('OP', ':')
            typ = self.expect('IDENT')['value']
        return {'type': 'VariableDeclaration', 'name': name, 'value': value, 'declaredType': typ}

    def parse_func_decl(self):
        """Parse a function declaration."""
        self.expect('IDENT', 'pool')
        name = self.expect('IDENT')['value']
        self.expect('OP', '(')
        params = []
        while True:
            if self.peek() and self.peek()['type'] == 'OP' and self.peek()['value'] == ')':
                break
            pname = self.expect('IDENT')['value']
            self.expect('OP', ':')
            ptype = self.expect('IDENT')['value']
            params.append({'name': pname, 'type': ptype})
            if self.peek() and self.peek()['type'] == 'OP' and self.peek()['value'] == ',':
                self.advance()
                continue
            else:
                break
        self.expect('OP', ')')
        self.expect('OP', ':')
        return_type = self.expect('IDENT')['value']
        self.expect('OP', '{')
        # Parse function body as block (currently expects only var decls for brevity)
        body = []
        while self.peek() and not (self.peek()['type'] == 'OP' and self.peek()['value'] == '}'):
            body.append(self.parse_statement())
        self.expect('OP', '}')
        return {'type': 'FunctionDeclaration', 'name': name, 'params': params, 'returnType': return_type, 'body': body}

    def parse_expression(self):
        """Parse an expression (number, string, or identifier)."""
        tok = self.peek()
        if not tok:
            raise ParseError("Expected expression but got end of input", -1, -1)
        if tok['type'] == 'NUMBER':
            self.advance()
            return {'type': 'NumberLiteral', 'value': float(tok['value'])}
        if tok['type'] == 'STRING':
            self.advance()
            return {'type': 'StringLiteral', 'value': tok['value'][1:-1]}
        if tok['type'] == 'IDENT':
            self.advance()
            return {'type': 'Identifier', 'value': tok['value']}
        raise ParseError("Expected expression", tok['line'], tok['col'])

def parse(code):
    """Parse Cascade code into AST."""
    parser = Parser(code)
    return parser.parse()