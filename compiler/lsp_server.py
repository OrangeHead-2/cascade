# Robust Cascade LSP Server using pygls
# Supports: diagnostics, hover/type info, go-to-definition, completion, document symbols

from pygls.server import LanguageServer
from pygls.lsp.types import (
    InitializeResult, TextDocumentSyncKind, Hover, HoverParams,
    Position, Range, MarkupContent, MarkupKind,
    CompletionParams, CompletionItem, CompletionItemKind,
    TextDocumentPositionParams, Location, Diagnostic, DiagnosticSeverity,
    SymbolInformation, SymbolKind
)
from pygls.lsp.types.basic_structures import MessageType
import compiler
import traceback

class CascadeLanguageServer(LanguageServer):
    """pygls-based Language Server for Cascade."""
    CMD_SHOW_AST = 'cascade.showAST'

cascade_server = CascadeLanguageServer('cascade-lsp', 'v0.2')

@cascade_server.feature('initialize')
def on_initialize(ls, params):
    """Initialize LSP server with all supported capabilities."""
    return InitializeResult(
        capabilities={
            "textDocumentSync": TextDocumentSyncKind.Full,
            "hoverProvider": True,
            "definitionProvider": True,
            "completionProvider": {"resolveProvider": False, "triggerCharacters": [" "]},
            "documentSymbolProvider": True
        }
    )

@cascade_server.feature('textDocument/didOpen')
def did_open(ls, params):
    """On file open: parse, type-check, and publish diagnostics."""
    uri = params.text_document.uri
    code = params.text_document.text
    diagnostics = []
    try:
        ast = compiler.parse(code)
        try:
            type_env = compiler.type_checker.TypeEnv()
            compiler.type_checker.check_type(ast, type_env)
            compiler.semantic_analyzer.analyze_semantics(ast)
        except Exception as e:
            diagnostics.append(Diagnostic(
                range=Range(
                    start=Position(line=0, character=0),
                    end=Position(line=0, character=1)
                ),
                message=str(e),
                severity=DiagnosticSeverity.Error
            ))
        ls.publish_diagnostics(uri, diagnostics)
        ls.workspace._docs[uri] = (code, ast)
    except Exception as e:
        ls.show_message_log("Parse error: " + str(e), msg_type=MessageType.Error)
        ls.publish_diagnostics(uri, [Diagnostic(
            range=Range(
                start=Position(line=0, character=0),
                end=Position(line=0, character=1)
            ),
            message="Parse error: " + str(e),
            severity=DiagnosticSeverity.Error
        )])
        ls.workspace._docs[uri] = (code, None)

@cascade_server.feature('textDocument/hover')
def hover(ls, params: HoverParams):
    """Show type information on hover."""
    doc = ls.workspace.get_document(params.text_document.uri)
    code, ast = ls.workspace._docs.get(params.text_document.uri, (None, None))
    word = doc.word_at_position(params.position)
    info = ""
    if ast:
        for stmt in ast['body']:
            if stmt['type'] in ('VariableDeclaration', 'ConstantDeclaration') and stmt['name'] == word:
                t = stmt.get('declaredType') or 'inferred'
                info = f"**{word}**: `{t}`"
    if not info:
        info = f"Identifier: {word}"
    return Hover(contents=MarkupContent(kind=MarkupKind.Markdown, value=info))

@cascade_server.feature('textDocument/definition')
def definition(ls, params: TextDocumentPositionParams):
    """Go to definition for variables/functions."""
    doc = ls.workspace.get_document(params.text_document.uri)
    code, ast = ls.workspace._docs.get(params.text_document.uri, (None, None))
    word = doc.word_at_position(params.position)
    if ast:
        for i, stmt in enumerate(ast['body']):
            if stmt.get('name') == word:
                return [Location(uri=params.text_document.uri,
                    range=Range(
                        start=Position(line=i, character=0),
                        end=Position(line=i, character=10)
                    ))]
    return None

@cascade_server.feature('textDocument/completion')
def completion(ls, params: CompletionParams):
    """Provide code completion for variables and functions."""
    doc = ls.workspace.get_document(params.text_document.uri)
    code, ast = ls.workspace._docs.get(params.text_document.uri, (None, None))
    items = []
    if ast:
        for stmt in ast['body']:
            if 'name' in stmt:
                kind = CompletionItemKind.Variable if stmt['type'] in ('VariableDeclaration', 'ConstantDeclaration') else CompletionItemKind.Function
                items.append(CompletionItem(
                    label=stmt['name'],
                    kind=kind
                ))
    return items

@cascade_server.feature('textDocument/documentSymbol')
def document_symbols(ls, params):
    """Provide outline view of all symbols in the document."""
    doc = ls.workspace.get_document(params.text_document.uri)
    code, ast = ls.workspace._docs.get(params.text_document.uri, (None, None))
    symbols = []
    if ast:
        for i, stmt in enumerate(ast['body']):
            if 'name' in stmt:
                kind = SymbolKind.Variable if stmt['type'] in ('VariableDeclaration', 'ConstantDeclaration') else SymbolKind.Function
                symbols.append(SymbolInformation(
                    name=stmt['name'],
                    kind=kind,
                    location=Location(uri=params.text_document.uri, range=Range(
                        start=Position(line=i, character=0), end=Position(line=i, character=10)
                    ))
                ))
    return symbols

def main():
    """Run the LSP server as a process."""
    cascade_server.start_io()

if __name__ == "__main__":
    main()