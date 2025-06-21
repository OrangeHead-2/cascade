# Full Cascade Language Type Checker

class TypeError(Exception):
    pass

class TypeEnv:
    def __init__(self, parent=None):
        self.vars = {}
        self.types = {}
        self.funcs = {}
        self.parent = parent

    def set_var(self, name, typ):
        self.vars[name] = typ

    def set_type(self, name, fields):
        self.types[name] = fields

    def set_func(self, name, signature):
        self.funcs[name] = signature

    def get_var(self, name):
        if name in self.vars:
            return self.vars[name]
        elif self.parent:
            return self.parent.get_var(name)
        else:
            raise TypeError(f"Undefined variable '{name}'")

    def get_type(self, name):
        if name in self.types:
            return self.types[name]
        elif self.parent:
            return self.parent.get_type(name)
        else:
            raise TypeError(f"Undefined type '{name}'")

    def get_func(self, name):
        if name in self.funcs:
            return self.funcs[name]
        elif self.parent:
            return self.parent.get_func(name)
        else:
            raise TypeError(f"Undefined function '{name}'")

def check_type(node, env):
    t = node['type']
    if t == 'Program':
        for stmt in node['body']:
            check_type(stmt, env)
    elif t == 'VariableDeclaration':
        val_type = infer_type(node['value'], env)
        declared = node.get('declaredType')
        if declared and declared != val_type:
            raise TypeError(f"Type mismatch for {node['name']}: declared {declared}, assigned {val_type}")
        env.set_var(node['name'], declared or val_type)
    elif t == 'Assignment':
        var_type = env.get_var(node['name'])
        val_type = infer_type(node['value'], env)
        if var_type != val_type:
            raise TypeError(f"Cannot assign {val_type} to {node['name']} of type {var_type}")
    elif t == 'ConstantDeclaration':
        val_type = infer_type(node['value'], env)
        env.set_var(node['name'], val_type)
    elif t == 'FunctionDeclaration':
        param_types = [p['type'] for p in node['params']]
        env.set_func(node['name'], (param_types, node['returnType']))
        local_env = TypeEnv(env)
        for param in node['params']:
            local_env.set_var(param['name'], param['type'])
        for stmt in node['body']:
            check_type(stmt, local_env)
    elif t == 'TypeDeclaration':
        fields = {f['name']: f['type'] for f in node['fields']}
        env.set_type(node['name'], fields)
    elif t == 'IfStatement':
        for when in node['whens']:
            cond_type = infer_type(when['condition'], env)
            if cond_type != 'drop':
                raise TypeError("If condition must be drop (boolean), got " + cond_type)
            for stmt in when['body']:
                check_type(stmt, env)
        if node['otherwise']:
            for stmt in node['otherwise']['body']:
                check_type(stmt, env)
    elif t == 'CycleStatement':
        coll_type = infer_type(node['collection'], env)
        if not coll_type.startswith('['):
            raise TypeError("Can only cycle through lists, got " + coll_type)
        elem_type = coll_type[1:-1]
        local_env = TypeEnv(env)
        local_env.set_var(node['element'], elem_type)
        for stmt in node['body']:
            check_type(stmt, local_env)
    elif t == 'TryCatchStatement':
        try_env = TypeEnv(env)
        for stmt in node['tryBlock']:
            check_type(stmt, try_env)
        catch_env = TypeEnv(env)
        catch_env.set_var(node['errVar'], 'Turbulence')
        for stmt in node['catchBlock']:
            check_type(stmt, catch_env)
    elif t == 'ThrowStatement':
        val_type = infer_type(node['value'], env)
        if val_type != 'rivulet':
            raise TypeError("Turbulence/error must be rivulet (string)")
    elif t == 'ReturnStatement':
        infer_type(node['value'], env)
    elif t == 'ExpressionStatement':
        infer_type(node['expression'], env)
    elif t == 'ImportStatement':
        pass
    else:
        raise TypeError(f"Unknown node type: {t}")

def infer_type(expr, env):
    t = expr['type']
    if t == 'NumberLiteral':
        return 'depth'
    if t == 'StringLiteral':
        return 'rivulet'
    if t == 'BooleanLiteral':
        return 'drop'
    if t == 'ListLiteral':
        if not expr['elements']:
            return '[Any]'
        etype = infer_type(expr['elements'][0], env)
        for el in expr['elements']:
            if infer_type(el, env) != etype:
                raise TypeError("List elements must have same type")
        return f'[{etype}]'
    if t == 'MapLiteral':
        return 'map'
    if t == 'Identifier':
        return env.get_var(expr['value'])
    if t == 'FunctionCall':
        sig = env.get_func(expr['name'])
        args = expr.get('args', [])
        if len(args) != len(sig[0]):
            raise TypeError(f"Function {expr['name']} expects {len(sig[0])} args, got {len(args)}")
        for ix, arg in enumerate(args):
            arg_type = infer_type(arg, env)
            if arg_type != sig[0][ix]:
                raise TypeError(f"Function {expr['name']} arg {ix+1} expects {sig[0][ix]}, got {arg_type}")
        return sig[1]
    if t == 'BinaryExpr':
        ltype = infer_type(expr['left'], env)
        rtype = infer_type(expr['right'], env)
        op = expr['operator']
        if op in ("+", "-", "*", "/"):
            if ltype != rtype or ltype not in ("depth",):
                raise TypeError(f"Operator {op} expects depth, got {ltype}, {rtype}")
            return "depth"
        if op in ("==", "!=", "<", "<=", ">", ">="):
            if ltype != rtype:
                raise TypeError(f"Comparison between {ltype} and {rtype}")
            return "drop"
        if op in ("&&", "||"):
            if ltype != "drop" or rtype != "drop":
                raise TypeError(f"Logical operator {op} expects drop, got {ltype}, {rtype}")
            return "drop"
    if t == 'Pattern':
        return expr['asType']
    raise TypeError(f"Cannot infer type for {t}")
