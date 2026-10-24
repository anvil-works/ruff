// Analysis sees REPL history or a typed Form scope; only the current input owns edits.
export function projectContext(context, uri, generation, form) {
    const indent = context.kind === 'binding' ? 4 : 0;
    const prefix = context.kind === 'binding'
        ? `from ${form.module} import ${form.name} as _AnvilContextForm\ndef _anvil_binding(self: _AnvilContextForm):\n`
        : context.previousCode + '\n';
    const code = context.code.split(/\r\n|\r|\n/).map(line => ' '.repeat(indent) + line).join('\n');
    return { uri, generation, indent, text: prefix + code, firstLine: prefix.split(/\r\n|\r|\n/).length - 1 };
}

export function contextPosition(document, position) {
    return { line: document.firstLine + position.line, character: position.character + document.indent };
}

function inputRange(document, range) {
    if (range.start.line < document.firstLine || range.end.line < document.firstLine ||
        range.start.character < document.indent || range.end.character < document.indent) return;
    return {
        start: { line: range.start.line - document.firstLine, character: range.start.character - document.indent },
        end: { line: range.end.line - document.firstLine, character: range.end.character - document.indent },
    };
}

export function contextCompletion(item, id, document) {
    const mapped = structuredClone(item);
    if (mapped.textEdit) {
        if ('range' in mapped.textEdit) {
            const range = inputRange(document, mapped.textEdit.range);
            if (!range) return;
            mapped.textEdit.range = range;
        } else {
            const insert = inputRange(document, mapped.textEdit.insert);
            const replace = inputRange(document, mapped.textEdit.replace);
            if (!insert || !replace) return;
            mapped.textEdit.insert = insert;
            mapped.textEdit.replace = replace;
        }
    }
    for (const edit of mapped.additionalTextEdits ?? []) {
        const range = inputRange(document, edit.range);
        if (!range) return;
        edit.range = range;
    }
    mapped.data = { ...mapped.data, contextId: id, generation: document.generation, original: item };
    return mapped;
}

export function originalCompletion(item, id, document) {
    if (item.data?.contextId !== id || item.data.generation !== document.generation)
        throw new DOMException('Context completion is obsolete', 'AbortError');
    return item.data.original;
}
