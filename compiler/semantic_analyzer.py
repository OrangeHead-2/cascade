# Full Cascade Semantic Analyzer

class SemanticError(Exception):
    pass

def analyze_semantics(ast, defined_functions=None, defined_types=None, in_scope=None):
    if defined_functions is None: defined_functions = set()
    if defined_types is None: defined_types = set()
    if in_scope is None: in_scope = set()
    for node in ast['body']:
        check_semantics(node, defined_functions, defined_types, in_scope)

def check_semantics(node, functions, types, scope):
    t = node.get('type')
    if t == 'FunctionDeclaration':
        if node['name'] in functions:
            raise SemanticError(f"Function '{node['name']}' already defined")
        functions.add(node['name'])
        param_names = set()
        for param in node['params']:
            if param['name'] in param_names:
                raise SemanticError(f"Duplicate parameter: {param['name']}")
            param_names.add(param['name'])
        local_scope = scope | param_names
        for stmt in node['body']:
            check_semantics(stmt, functions, types, local_scope)
    elif t == 'TypeDeclaration':
        if node['name'] in types:
            raise SemanticError(f"Type '{node['name']}' already defined")
        types.add(node['name'])
        field_names = set()
        for f in node['fields']:
            if f['name'] in field_names:
                raise SemanticError(f"Duplicate field {f['name']} in type {node['name']}")
            field_names.add(f['name'])
    elif t == 'VariableDeclaration':
        if node['name'] in scope:
            raise SemanticError(f"Variable '{node['name']}' already defined in scope")
        check_semantics(node['value'], functions, types, scope)
    elif t == 'Assignment':
        if node['name'] not in scope:
            raise SemanticError(f"Assignment to undefined variable '{node['name']}'")
        check_semantics(node['value'], functions, types, scope)
    elif t == 'IfStatement':
        for when in node['whens']:
            check_semantics(when['condition'], functions, types, scope)
            for stmt in when['body']:
                check_semantics(stmt, functions, types, scope)
        if node['otherwise']:
            for stmt in node['otherwise']['body']:
                check_semantics(stmt, functions, types, scope)
    elif t == 'CycleStatement':
        check_semantics(node['collection'], functions, types, scope)
        local_scope = scope | {node['element']}
        for stmt in node['body']:
            check_semantics(stmt, functions, types, local_scope)
    elif t == 'TryCatchStatement':
        for stmt in node['tryBlock']:
            check_semantics(stmt, functions, types, scope)
        catch_scope = scope | {node['errVar']}
        for stmt in node['catchBlock']:
            check_semantics(stmt, functions, types, catch_scope)
    elif t in ('ExpressionStatement', 'ReturnStatement'):
        check_semantics(node['expression'] if t == 'ExpressionStatement' else node['value'],
                       functions, types, scope)
    elif t in ('NumberLiteral', 'StringLiteral', 'BooleanLiteral', 'ListLiteral', 'MapLiteral'):
        pass
    elif t == 'Identifier':
        if node['value'] not in scope:
            raise SemanticError(f"Variable '{node['value']}' not defined in scope")
    elif t == 'FunctionCall':
        if node['name'] not in functions:
            raise SemanticError(f"Function '{node['name']}' not defined")
        for arg in node.get('args', []):
            check_semantics(arg, functions, types, scope)
    elif t == 'ImportStatement':
        pass
    elif t == 'Pattern':
        if node['asType'] not in types:
            raise SemanticError(f"Pattern matches unknown type '{node['asType']}'")
    else:
        raise SemanticError(f"Unknown node type: {t}")
