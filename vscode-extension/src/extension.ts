import * as vscode from 'vscode';

export function activate(context: vscode.ExtensionContext) {
  vscode.languages.registerDocumentFormattingEditProvider('cascade', {
    provideDocumentFormattingEdits(document: vscode.TextDocument): vscode.TextEdit[] {
      // Simple formatter: trims trailing whitespace
      const edits: vscode.TextEdit[] = [];
      for (let i = 0; i < document.lineCount; i++) {
        const line = document.lineAt(i);
        const trimmed = line.text.replace(/\s+$/, '');
        if (trimmed !== line.text) {
          edits.push(vscode.TextEdit.replace(line.range, trimmed));
        }
      }
      return edits;
    }
  });
}

export function deactivate() { }