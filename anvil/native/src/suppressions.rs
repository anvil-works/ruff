//! Apply Python suppression comments to Anvil diagnostics added after ty checking.
use std::collections::{HashMap, HashSet};
use std::path::Path;

use anyhow::Result;
use ruff_db::files::system_path_to_file;
use ruff_db::parsed::parsed_module;
use ruff_db::source::{line_index, source_text};
use ruff_db::system::SystemPath;
use ruff_python_ast::token::TokenKind;
use ruff_text_size::Ranged;
use serde_json::Value;
use ty_python_semantic::Db;

pub(crate) fn apply(
    db: &dyn Db,
    path: &SystemPath,
    origin: &Path,
    diagnostics: &mut Vec<Value>,
    respect_type_ignore: bool,
) -> Result<()> {
    let file = system_path_to_file(db, path)?;
    let source = source_text(db, file);
    let index = line_index(db, file);
    let parsed = parsed_module(db, db.program_file(file).python_file(db)).load(db);
    let first_code = parsed
        .tokens()
        .iter()
        .find(|token| {
            !token.kind().is_trivia()
                && !matches!(
                    token.kind(),
                    TokenKind::Newline | TokenKind::Indent | TokenKind::EndOfFile
                )
        })
        .map(Ranged::start);
    let mut file_ignore = None;
    let ignored: HashMap<_, _> = parsed
        .tokens()
        .iter()
        .filter(|token| token.kind().is_comment())
        .filter_map(|token| {
            let comment = source[token.range()].trim_start_matches('#').trim_start();
            let (kind, rest) = comment.split_once(':')?;
            let rest = rest.trim_start().strip_prefix("ignore")?.trim_start();
            let rules = match kind {
                "type" if respect_type_ignore && (rest.is_empty() || rest.starts_with('#')) => None,
                "pyright" if rest.is_empty() || rest.starts_with('#') => None,
                "pyright" if rest.starts_with('[') => {
                    let end = rest.find(']')?;
                    Some(rest[1..end].split(',').map(str::trim).collect::<Vec<_>>())
                }
                _ => return None,
            };
            let line = index.line_index(token.start()).to_zero_indexed() as u64;
            if kind == "type" && first_code.is_none_or(|offset| token.start() < offset) {
                file_ignore = Some(line);
            }
            Some((line, (kind, rules)))
        })
        .collect();
    let same_file = |item: &Value| item["file"].as_str() == origin.to_str();
    let mut used = HashSet::new();
    diagnostics.retain(|item| {
        let line = item["range"]["start"]["line"].as_u64();
        let directive = file_ignore
            .and_then(|line| ignored.get_key_value(&line))
            .or_else(|| line.and_then(|line| ignored.get_key_value(&line)));
        if same_file(item)
            && let Some((line, (kind, rules))) = directive
            && let Some(rule) = item["rule"].as_str()
            && (*kind == "pyright" || rule.starts_with("reportAnvil"))
            && rules
                .as_ref()
                .is_none_or(|rules| rules.contains(&crate::policy::diagnostic_rule(item)))
        {
            if *kind == "type" {
                used.insert(*line);
            }
            return false;
        }
        true
    });
    // ty cannot see diagnostics emitted by the adapter. An ignore consumed by an
    // Anvil check must not be reported as unused by the generic checker.
    diagnostics.retain(|item| {
        !(same_file(item)
            && item["rule"] == "unused-type-ignore-comment"
            && item["range"]["start"]["line"]
                .as_u64()
                .is_some_and(|line| used.contains(&line)))
    });
    Ok(())
}
