// Parameter annotations add columns; private declarations append after user
// source. Every editor operation still speaks original UTF-16 positions.
export function projectAnnotations(source, edits, declarations) {
    const lines = source.split('\n');
    const insertions = new Map();
    for (const { position, text } of edits) {
        if (!insertions.has(position.line)) insertions.set(position.line, []);
        insertions.get(position.line).push({ character: position.character, text });
    }
    for (const [line, items] of insertions) {
        items.sort((a, b) => a.character - b.character);
        for (const { character, text } of [...items].reverse())
            lines[line] = lines[line].slice(0, character) + text + lines[line].slice(character);
    }
    const suffix = { line: lines.length, character: 0 };
    const before = (a, b) => a.line < b.line || a.line === b.line && a.character < b.character;
    function original(position) {
        let shift = 0;
        for (const item of insertions.get(position.line) ?? []) {
            if (position.character < item.character + shift) break;
            if (position.character < item.character + shift + item.text.length)
                return { line: position.line, character: item.character };
            shift += item.text.length;
        }
        return { ...position, character: position.character - shift };
    }
    return {
        text: lines.join('\n') + '\n' + declarations + '\n',
        position(position) {
            const shift = (insertions.get(position.line) ?? []).filter(item => item.character < position.character)
                .reduce((sum, item) => sum + item.text.length, 0);
            return { ...position, character: position.character + shift };
        },
        range(range) {
            if (!before(range.start, suffix)) return;
            let shift = 0;
            for (const item of insertions.get(range.start.line) ?? []) {
                const start = item.character + shift;
                const end = start + item.text.length;
                if (range.start.line === range.end.line && range.start.character >= start && range.end.character <= end &&
                    (range.start.character < range.end.character || range.start.character > start && range.start.character < end)) return;
                shift += item.text.length;
            }
            return { start: original(range.start), end: original(range.end) };
        },
    };
}
