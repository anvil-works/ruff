//! Export resolved TypedDicts as declarations for a separate Python program.

use super::typed_dict_field_definition;
use crate::types::typed_dict::{TypedDictOpenness, TypedDictType};
use crate::types::visitor::any_over_type_expanding_aliases;
use crate::types::{DynamicType, SpecialFormType, Type, TypeDetail, TypeDisplayDetails};
use crate::{Db, ProgramEnvironment};
use ruff_db::files::{File, FileRange};
use ruff_python_ast::str::{Quote, TripleQuotes};
use ruff_python_literal::escape::UnicodeEscape;
use ruff_python_stdlib::identifiers::is_identifier;
use std::cmp::Reverse;
use ty_module_resolver::file_to_module;

pub struct ExportedType {
    pub source: String,
    /// Generated line (zero-based) and original definition.
    pub origins: Vec<(u32, FileRange)>,
    pub imports: Vec<ExportedImport>,
}

pub struct ExportedImport {
    pub line: u32,
    /// Zero-based UTF-16 column in the generated declaration.
    pub column: u32,
    pub target: FileRange,
}

pub fn export_typed_dict_type<'db>(
    db: &'db dyn Db,
    env: &ProgramEnvironment<'db>,
    ty: Type<'db>,
    can_import: &dyn Fn(File, &str) -> bool,
) -> Option<ExportedType> {
    if !any_over_type_expanding_aliases(db, env, ty, |ty| matches!(ty, Type::TypedDict(_))) {
        return None;
    }
    let mut exporter = Exporter {
        db,
        env,
        can_import,
        imports: Vec::new(),
        shapes: Vec::new(),
        remaining: 256,
        export: ExportedType {
            source: String::new(),
            origins: Vec::new(),
            imports: Vec::new(),
        },
        line: 0,
    };
    exporter.write_line(
        "from typing_extensions import Annotated, Any, Literal, NotRequired, ReadOnly, TypeAlias, TypedDict",
        None,
    );
    let result = exporter.annotation(ty)?;
    if exporter.shapes.is_empty() {
        return None;
    }
    exporter.write_line(&format!("_Result: TypeAlias = {result}"), None);
    Some(exporter.finish())
}

fn annotation_details<'db>(
    db: &'db dyn Db,
    env: &ProgramEnvironment<'db>,
    ty: Type<'db>,
) -> TypeDisplayDetails<'db> {
    ty.resolve_type_alias(db)
        .display(db, env)
        .for_type_annotation()
        .preserve_long_unions()
        .with_annotation_spans()
        .to_string_parts()
}

/// Prefer nested TypedDict definitions for each alternative while retaining
/// the normal definition of other alternatives.
pub fn type_definitions_with_typed_dicts<'db>(
    db: &'db dyn Db,
    env: &ProgramEnvironment<'db>,
    ty: Type<'db>,
) -> Vec<FileRange> {
    let ty = ty.resolve_type_alias(db);
    let alternatives = match &ty {
        Type::Union(union) => union.elements(db),
        _ => std::slice::from_ref(&ty),
    };
    let mut targets = Vec::new();
    for alternative in alternatives {
        let mut found_schema = false;
        for detail in annotation_details(db, env, *alternative).details {
            if let TypeDetail::Type(Type::TypedDict(schema)) = detail
                && let Some(origin) = schema.type_definition(db).and_then(|ty| ty.focus_range(db))
            {
                found_schema = true;
                if !targets.contains(&origin) {
                    targets.push(origin);
                }
            }
        }
        if !found_schema
            && !alternative.is_none(db)
            && let Some(origin) = alternative
                .definition(db, env)
                .and_then(|ty| ty.focus_range(db))
            && !targets.contains(&origin)
        {
            targets.push(origin);
        }
    }
    targets
}

struct ImportedName {
    module: String,
    name: String,
    target: FileRange,
}

struct Shape<'db> {
    schema: TypedDictType<'db>,
    name: String,
    complete: bool,
}

struct Exporter<'a, 'db> {
    db: &'db dyn Db,
    env: &'a ProgramEnvironment<'db>,
    can_import: &'a dyn Fn(File, &str) -> bool,
    imports: Vec<ImportedName>,
    shapes: Vec<Shape<'db>>,
    remaining: usize,
    export: ExportedType,
    line: u32,
}

impl<'db> Exporter<'_, 'db> {
    fn write_line(&mut self, line: &str, origin: Option<FileRange>) {
        if let Some(origin) = origin {
            self.export.origins.push((self.line, origin));
        }
        self.export.source.push_str(line);
        self.export.source.push('\n');
        self.line += 1;
    }

    fn finish(mut self) -> ExportedType {
        let mut imports = String::new();
        for (index, imported) in self.imports.into_iter().enumerate() {
            let ImportedName {
                module,
                name,
                target,
            } = imported;
            let prefix = format!("from {module} import ");
            self.export.imports.push(ExportedImport {
                line: index as u32,
                column: prefix.encode_utf16().count() as u32,
                target,
            });
            imports.push_str(&format!("{prefix}{name} as _ExportedType{index}\n"));
        }
        let import_lines = self.export.imports.len() as u32;
        for (line, _) in &mut self.export.origins {
            *line += import_lines;
        }
        imports.push_str(&self.export.source);
        self.export.source = imports;
        self.export
    }

    fn annotation(&mut self, ty: Type<'db>) -> Option<String> {
        self.remaining = self.remaining.checked_sub(1)?;
        let ty = ty.resolve_type_alias(self.db);
        if let Type::TypedDict(schema) = ty {
            return self.schema(schema);
        }
        let details = annotation_details(self.db, self.env, ty);
        if !details.is_valid_syntax {
            return None;
        }
        self.remaining = self.remaining.checked_sub(details.details.len())?;
        // A specialized schema's span covers both its name and its arguments.
        // Process that outer span before the symbols it replaces.
        let mut spans = details
            .targets
            .into_iter()
            .zip(details.details)
            .collect::<Vec<_>>();
        spans.sort_by_key(|(range, detail)| {
            (
                range.start(),
                Reverse(range.end()),
                !matches!(
                    detail,
                    TypeDetail::Type(Type::TypedDict(_) | Type::TypeAlias(_))
                ),
            )
        });
        let mut annotation = String::new();
        let mut end = 0;
        for (range, detail) in spans {
            let TypeDetail::Type(ty) = detail else {
                continue;
            };
            let start = range.start().to_usize();
            if start < end || range.is_empty() {
                continue;
            }
            let next = range.end().to_usize();
            let text = &details.label[start..next];
            annotation.push_str(&details.label[end..start]);
            match ty {
                Type::TypedDict(schema) => annotation.push_str(&self.schema(schema)?),
                Type::TypeAlias(_) => annotation.push_str(&self.annotation(ty)?),
                Type::Dynamic(DynamicType::Any) => annotation.push_str("Any"),
                Type::SpecialForm(SpecialFormType::Literal | SpecialFormType::Annotated) => {
                    annotation.push_str(text);
                }
                Type::LiteralValue(_) => annotation.push_str(text),
                _ if text == "None" => annotation.push_str(text),
                _ => annotation.push_str(&self.import_type(ty)?),
            }
            end = next;
        }
        annotation.push_str(&details.label[end..]);
        Some(annotation)
    }

    fn import_type(&mut self, ty: Type<'db>) -> Option<String> {
        let origin = ty.definition(self.db, self.env)?;
        let target = origin.focus_range(self.db)?;
        let definition = origin.definition()?;
        if !definition.file_scope(self.db).is_global() {
            return None;
        }
        if let Some(index) = self
            .imports
            .iter()
            .position(|imported| imported.target == target)
        {
            return Some(format!("_ExportedType{index}"));
        }
        let module = file_to_module(
            self.db,
            definition.program_file(self.db).resolver_file(self.db),
        )?;
        if module.is_known_stub_only(self.db) {
            return None;
        }
        let name = definition.name(self.db)?;
        let file = definition.file(self.db);
        if !file.path(self.db).is_vendored_path() && !(self.can_import)(file, &name) {
            return None;
        }
        let index = self.imports.len();
        self.imports.push(ImportedName {
            module: module.name(self.db).as_str().to_owned(),
            name,
            target,
        });
        Some(format!("_ExportedType{index}"))
    }

    fn field_annotation(&mut self, ty: Type<'db>) -> String {
        let (shapes, imports, source, origins, line) = (
            self.shapes.len(),
            self.imports.len(),
            self.export.source.len(),
            self.export.origins.len(),
            self.line,
        );
        if let Some(annotation) = self.annotation(ty) {
            return annotation;
        }
        // Discard declarations and imports we encountered before a failed field.
        self.shapes.truncate(shapes);
        self.imports.truncate(imports);
        self.export.source.truncate(source);
        self.export.origins.truncate(origins);
        self.line = line;
        "Any".to_owned()
    }

    fn schema(&mut self, schema: TypedDictType<'db>) -> Option<String> {
        if let Some(shape) = self.shapes.iter().find(|shape| shape.schema == schema) {
            // An unfinished declaration indicates recursion.
            return shape.complete.then(|| shape.name.clone());
        }
        let items = schema.items(self.db);
        self.remaining = self.remaining.checked_sub(items.len())?;
        let index = self.shapes.len();
        let definition = schema.type_definition(self.db);
        let origin = definition.as_ref().and_then(|ty| ty.focus_range(self.db));
        let mut name = definition
            .and_then(|ty| ty.definition())
            .and_then(|definition| definition.name(self.db))
            .unwrap_or_else(|| format!("_Shape{index}"));
        const RESERVED: &[&str] = &[
            "Annotated",
            "Any",
            "Literal",
            "TypedDict",
            "TypeAlias",
            "NotRequired",
            "ReadOnly",
            "_Result",
        ];
        if name.starts_with("_ExportedType") {
            name.insert(0, '_');
        }
        while RESERVED.contains(&name.as_str())
            || self.shapes.iter().any(|shape| shape.name == name)
        {
            name.push('_');
        }
        self.shapes.push(Shape {
            schema,
            name: name.clone(),
            complete: false,
        });

        let suffix = match schema.openness(self.db) {
            TypedDictOpenness::ImplicitlyOpen => String::new(),
            TypedDictOpenness::Closed => ", closed=True".to_owned(),
            TypedDictOpenness::Extra(extra) => {
                let annotation = self.field_annotation(extra.declared_ty);
                if extra.is_read_only() {
                    format!(", extra_items=ReadOnly[{annotation}]")
                } else {
                    format!(", extra_items={annotation}")
                }
            }
        };
        let mut fields = Vec::new();
        for (key, field) in items {
            let mut annotation = self.field_annotation(field.declared_ty);
            if field.is_read_only() {
                annotation = format!("ReadOnly[{annotation}]");
            }
            if !field.is_required() {
                annotation = format!("NotRequired[{annotation}]");
            }
            let origin = typed_dict_field_definition(self.db, schema, key, field)
                .map(|definition| definition.focus_range(self.db));
            fields.push((key.as_str(), annotation, origin));
        }
        // Only emit a definition once the types it depends on have been emitted.
        // Class syntax gives Ty real field definitions for ordinary Python keys.
        if fields.iter().all(|(key, _, _)| {
            is_identifier(key) && (!key.starts_with("__") || key.ends_with("__"))
        }) {
            self.write_line(&format!("class {name}(TypedDict{suffix}):"), origin);
            if fields.is_empty() {
                self.write_line("    pass", None);
            }
            for (key, annotation, origin) in fields {
                self.write_line(&format!("    {key}: {annotation}"), origin);
            }
        } else {
            self.write_line(&format!("{name} = TypedDict(\"{name}\", {{"), origin);
            for (key, annotation, origin) in fields {
                let escaped = UnicodeEscape::with_preferred_quote(key, Quote::Double);
                let key = escaped.str_repr(TripleQuotes::No);
                self.write_line(&format!("    {key}: {annotation},"), origin);
            }
            self.write_line(&format!("}}{suffix})"), None);
        }
        self.shapes[index].complete = true;
        Some(name)
    }
}
