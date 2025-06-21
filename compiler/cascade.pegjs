// Full Cascade PEG Grammar

Start
  = _ stmts:StatementList _ { return {type: "Program", body: stmts}; }

StatementList
  = head:Statement tail:(_ Statement)* {
      return [head].concat(tail.map(x => x[1]));
    }

Statement
  = VariableDeclaration
  / Assignment
  / ConstantDeclaration
  / IfStatement
  / CycleStatement
  / FunctionDeclaration
  / TypeDeclaration
  / ImportStatement
  / TryCatchStatement
  / ThrowStatement
  / ReturnStatement
  / ExpressionStatement

VariableDeclaration
  = "pour" _ value:Expression _ "into" _ name:Identifier _ type:TypeAnnotation? {
      return {type: "VariableDeclaration", name, value, declaredType: type};
    }

Assignment
  = "fill" _ name:Identifier _ "with" _ value:Expression {
      return {type: "Assignment", name, value};
    }

ConstantDeclaration
  = "dam" _ value:Expression _ "as" _ name:Identifier {
      return {type: "ConstantDeclaration", name, value};
    }

IfStatement
  = "if" _ "stream splits" _ "{" _ whens:WhenBlocks _ otherwise:OtherwiseBlock? _ "}" {
      return {type: "IfStatement", whens, otherwise};
    }

WhenBlocks
  = whens:(WhenBlock (_ WhenBlock)*) {
      return [whens[0]].concat((whens[1]||[]).map(x=>x[1]));
    }

WhenBlock
  = "when" _ cond:PatternOrExpr _ "{" _ body:StatementList _ "}" {
      return {condition: cond, body};
    }

PatternOrExpr
  = "(" cond:Expression ")" { return cond; }
  / Pattern

Pattern
  = "match" _ name:Identifier "as" _ type:TypeAnnotation {
      return {type: "Pattern", variable: name, asType: type};
    }

OtherwiseBlock
  = "otherwise" _ "{" _ body:StatementList _ "}" {
      return {body};
    }

CycleStatement
  = "cycle through" _ coll:Expression _ "as" _ elem:Identifier _ "{" _ body:StatementList _ "}" {
      return {type: "CycleStatement", collection: coll, element: elem, body};
    }

FunctionDeclaration
  = "pool" _ name:Identifier _ "(" params:ParamList? ")" _ ":" returnType:TypeAnnotation _ "{" _ body:StatementList _ "}" {
      return {type: "FunctionDeclaration", name, params: params||[], returnType, body};
    }

ParamList
  = head:Param tail:(_ "," _ Param)* {
      return [head].concat(tail.map(x=>x[3]));
    }

Param
  = name:Identifier ":" type:TypeAnnotation {
      return {name, type};
    }

TypeDeclaration
  = "reservoir" _ name:Identifier _ "{" _ fields:FieldList? _ "}" {
      return {type: "TypeDeclaration", name, fields: fields||[]};
    }

FieldList
  = head:Field tail:(_ ","? _ Field)* {
      return [head].concat(tail.map(x=>x[3]));
    }

Field
  = name:Identifier ":" type:TypeAnnotation {
      return {name, type};
    }

ImportStatement
  = "open" _ "channel" _ path:ModulePath {
      return {type: "ImportStatement", path};
    }

ModulePath
  = $([a-zA-Z0-9_.\/]+)

TryCatchStatement
  = "try" _ "channel" _ "{" _ tryBlock:StatementList _ "}" _ "catch" _ "turbulence" _ "as" _ errVar:Identifier _ "{" _ catchBlock:StatementList _ "}" {
      return {type: "TryCatchStatement", tryBlock, errVar, catchBlock};
    }

ThrowStatement
  = "cause turbulence(" val:Expression ")" {
      return {type: "ThrowStatement", value: val};
    }

ReturnStatement
  = "return" _ value:Expression {
      return {type: "ReturnStatement", value};
    }

ExpressionStatement
  = expr:Expression {
      return {type: "ExpressionStatement", expression: expr};
    }

Expression
  = FunctionCall
  / BinaryExpr
  / Literal
  / Identifier

BinaryExpr
  = left:PrimaryExpr _ op:Operator _ right:Expression {
      return {type: "BinaryExpr", operator: op, left, right};
    }

PrimaryExpr
  = FunctionCall
  / Literal
  / Identifier

Operator
  = "==" / "!=" / "<=" / ">=" / "<" / ">" / "+" / "-" / "*" / "/" / "&&" / "||"

FunctionCall
  = "draw from" _ name:Identifier _ "(" args:ArgumentList? ")" {
      return {type: "FunctionCall", name, args: args||[]};
    }

ArgumentList
  = head:Expression tail:(_ "," _ Expression)* {
      return [head].concat(tail.map(x=>x[3]));
    }

Literal
  = Number
  / String
  / Boolean
  / List
  / Map

Number
  = value:$([0-9]+ ("." [0-9]+)?) { return {type: "NumberLiteral", value: parseFloat(value)}; }

String
  = "\"" chars:([^"\\] / "\\\"")* "\"" { return {type: "StringLiteral", value: chars.join("")}; }

Boolean
  = value:("true" / "false") { return {type: "BooleanLiteral", value: value === "true"}; }

List
  = "[" _ elements:ListElements? _ "]" {
      return {type: "ListLiteral", elements: elements||[]};
    }

ListElements
  = head:Expression tail:(_ "," _ Expression)* {
      return [head].concat(tail.map(x=>x[3]));
    }

Map
  = "{" _ pairs:MapPairs? _ "}" {
      return {type: "MapLiteral", pairs: pairs||[]};
    }

MapPairs
  = head:MapPair tail:(_ "," _ MapPair)* {
      return [head].concat(tail.map(x=>x[3]));
    }

MapPair
  = key:String _ ":" _ value:Expression {
      return {key: key.value, value};
    }

Identifier
  = $([a-zA-Z_][a-zA-Z0-9_]*)

TypeAnnotation
  = $([a-zA-Z_][a-zA-Z0-9_]*(\[\])?)

_  // Whitespace and comments
  = ([ \t\n\r] / Comment)*

Comment
  = "#" [^\n]*
