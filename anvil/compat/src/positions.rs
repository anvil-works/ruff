//! Convert parser byte offsets to the browser protocol's zero-based UTF-16 positions.
use ruff_python_ast::{Expr, Stmt};
use ruff_source_file::{LineIndex, PositionEncoding};
use ruff_text_size::{Ranged, TextSize};
use serde_json::{Value, json};

pub(crate) struct Positions<'a> {
    source: &'a str,
    lines: LineIndex,
}

impl<'a> Positions<'a> {
    pub(crate) fn new(source: &'a str) -> Self {
        Self {
            source,
            lines: LineIndex::from_source_text(source),
        }
    }

    pub(crate) fn at(&self, offset: TextSize) -> Value {
        let (line, character) = self.coordinates(offset);
        json!({ "line": line, "character": character })
    }

    pub(crate) fn coordinates(&self, offset: TextSize) -> (usize, usize) {
        let location = self
            .lines
            .source_location(offset, self.source, PositionEncoding::Utf16);
        (
            location.line.to_zero_indexed(),
            location.character_offset.to_zero_indexed(),
        )
    }

    /// Insert analysis imports after the module docstring and future imports.
    pub(crate) fn imports(&self, body: &[Stmt]) -> Value {
        let end = body.iter().take_while(|statement| {
            matches!(statement, Stmt::Expr(expr) if matches!(expr.value.as_ref(), Expr::StringLiteral(_)))
                || matches!(statement, Stmt::ImportFrom(import) if import.module.as_ref().is_some_and(|name| name == "__future__"))
        }).last().map_or(TextSize::new(0), Ranged::end);
        self.at(end)
    }
}
