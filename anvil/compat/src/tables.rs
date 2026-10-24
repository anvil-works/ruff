//! Schema declarations ported from anvil-pyright's config.ts and stubGenerator.ts.
//! Keep the static API, replacing only its generic app_tables tail.
use anyhow::{Context, Result, ensure};
use serde_json::Value;

use crate::{identifier, populated};

struct Table<'a> {
    name: &'a str,
    python: &'a str,
    columns: &'a [Value],
    model: Option<&'a crate::models::Model>,
}

impl Table<'_> {
    fn row_type(&self) -> String {
        let kind = if self.model.is_some() { "Model" } else { "Row" };
        format!("_{kind}_{}", self.python)
    }
}

fn attribute_name(name: &str) -> bool {
    ruff_python_parser::parse_expression(name).is_ok_and(|parsed| {
        matches!(parsed.syntax().body.as_ref(), ruff_python_ast::Expr::Name(value) if value.id.as_str() == name)
    })
}

fn column_type(column: &Value, tables: &[Table<'_>]) -> Result<String> {
    let kind = column["type"].as_str().context("column needs a type")?;
    let target = column["target"]
        .as_str()
        .and_then(|target| tables.iter().find(|table| table.name == target));
    Ok(match kind {
        "string" => "str".to_owned(),
        "number" => "float | int".to_owned(),
        "bool" => "bool".to_owned(),
        "date" => "datetime.date".to_owned(),
        "datetime" => "datetime.datetime".to_owned(),
        "media" => "anvil.Media".to_owned(),
        "link_single" => target.map_or_else(|| "Row".to_owned(), Table::row_type),
        "link_multiple" => format!(
            "SearchIterator[{}]",
            target.map_or_else(|| "Row".to_owned(), Table::row_type)
        ),
        _ => "Any".to_owned(),
    })
}

pub fn stub(
    schema: &Value,
    base: &str,
    models: &crate::models::Registry,
    environment: &str,
) -> Result<Option<String>> {
    // The baseline config parser ignores legacy array schemas. Keep the generic
    // API declarations; anvil-cli still validates the YAML format independently.
    if !populated(schema) || schema.is_array() {
        return Ok(None);
    }
    let schema = schema.as_object().context("db_schema must be a mapping")?;
    let mut tables = Vec::new();
    for (name, value) in schema {
        let python = value["python_name"].as_str().unwrap_or(name);
        ensure!(
            identifier(python),
            "unsupported table Python name: {python}"
        );
        let columns = value["columns"].as_array().map_or(&[][..], Vec::as_slice);
        for column in columns {
            // Column names are string keys and need not be Python identifiers.
            column["name"].as_str().context("column needs a name")?;
        }
        tables.push(Table {
            name,
            python,
            columns,
            model: models.get(name, environment),
        });
    }
    let (base, _) = base
        .split_once("# app_tables will be dynamically typed based on db_schema")
        .context("static tables stub lacks app_tables marker")?;
    let mut output = format!(
        "{base}\nfrom typing import Literal, TypedDict, TYPE_CHECKING, TypeAlias\nfrom typing_extensions import Unpack\nimport datetime\nimport anvil\n"
    );
    for table in &tables {
        let name = table.python;
        if let Some(model) = table.model {
            output.push_str(&format!(
                "if TYPE_CHECKING:\n    from {} import {} as _Model_{name}\n",
                model.module, model.name
            ));
        }
        let returns = table.row_type();
        let columns = table
            .columns
            .iter()
            .map(|column| {
                Ok((
                    column["name"].as_str().unwrap(),
                    column_type(column, &tables)?,
                ))
            })
            .collect::<Result<Vec<_>>>()?;
        let fields = columns
            .iter()
            .map(|(column, kind)| Ok(format!("{}: {kind}", serde_json::to_string(column)?)))
            .collect::<Result<Vec<_>>>()?
            .join(", ");
        output.push_str(&format!("\n_BufferedChanges_{name} = TypedDict(\"_BufferedChanges_{name}\", {{{fields}}}, total=False)\n"));
        let keyword_columns = columns.iter().all(|(column, _)| attribute_name(column));
        if !keyword_columns {
            let fields = columns
                .iter()
                .map(|(column, kind)| {
                    Ok(format!("{}: {kind} | Any", serde_json::to_string(column)?))
                })
                .collect::<Result<Vec<_>>>()?
                .join(", ");
            output.push_str(&format!(
                "_QueryArgs_{name} = TypedDict(\"_QueryArgs_{name}\", {{{fields}}}, total=False)\n"
            ));
        }
        output.push_str(&format!("\nclass _Row_{name}(Row):\n"));
        if columns.is_empty() {
            output.push_str("    pass\n");
        } else {
            for (column, kind) in &columns {
                output.push_str(&format!(
                    "    @overload\n    def __getitem__(self, key: Literal[{}]) -> {kind}: ...\n",
                    serde_json::to_string(column)?
                ));
            }
            output.push_str("    @overload\n    def __getitem__(self, key: str) -> Any: ...\n");
            for (column, kind) in &columns {
                output.push_str(&format!("    @overload\n    def __setitem__(self, key: Literal[{}], value: {kind}) -> None: ...\n", serde_json::to_string(column)?));
            }
            output.push_str(
                "    @overload\n    def __setitem__(self, key: str, value: Any) -> None: ...\n",
            );
            let args = if keyword_columns {
                columns
                    .iter()
                    .map(|(name, kind)| format!("{name}: {kind} = ..."))
                    .collect::<Vec<_>>()
                    .join(", ")
            } else {
                format!("**kwargs: Unpack[_BufferedChanges_{name}]")
            };
            output.push_str(&format!("    def update(self, {args}) -> None: ...\n    @property\n    def buffered_changes(self) -> _BufferedChanges_{name} | None: ...\n"));
        }
        output.push_str(&format!("\nclass _RowAttrs_{name}(_Row_{name}):\n"));
        let attributes: Vec<_> = columns
            .iter()
            .filter(|(column, _)| attribute_name(column))
            .collect();
        if attributes.is_empty() {
            output.push_str("    pass\n");
        }
        for (column, kind) in attributes {
            output.push_str(&format!("    {column}: {kind}\n"));
        }
        let typed = if columns.is_empty() {
            "**kwargs: Any".to_owned()
        } else if !keyword_columns {
            format!("**kwargs: Unpack[_BufferedChanges_{name}]")
        } else {
            format!(
                "*, {}",
                columns
                    .iter()
                    .map(|(name, kind)| format!("{name}: {kind} = ..."))
                    .collect::<Vec<_>>()
                    .join(", ")
            )
        };
        let query = columns
            .iter()
            .map(|(name, kind)| format!("{name}: {kind} | Any = ..."))
            .collect::<Vec<_>>()
            .join(", ");
        let query_kwargs = if !keyword_columns {
            format!("**kwargs: Unpack[_QueryArgs_{name}]")
        } else if query.is_empty() {
            "**kwargs: Any".to_owned()
        } else {
            query.clone()
        };
        output.push_str(&format!("\nclass _Table_{name}(Table[_Row_{name}]):\n    Row: TypeAlias = _Row_{name}\n    _AR: TypeAlias = _RowAttrs_{name}\n    def get(self, *query_expressions: Any, {query_kwargs}) -> {returns} | None: ...\n    def get_by_id(self, row_id: str) -> {returns} | None: ...\n    def search(self, *query_expressions: Any, {query_kwargs}) -> SearchIterator[{returns}]: ...\n    def add_row(self, {typed}) -> {returns}: ...\n"));
        for method in [
            "client_readable",
            "client_writable",
            "client_writable_cascade",
        ] {
            output.push_str(&format!("    def {method}(self, *view_restrictions: Any, {query_kwargs}) -> _Table_{name}: ...\n"));
        }
    }
    output.push_str("\nclass _AppTables:\n");
    for table in &tables {
        output.push_str(&format!("    {}: _Table_{}\n", table.python, table.python));
    }
    for table in &tables {
        output.push_str(&format!(
            "    @overload\n    def __getitem__(self, key: Literal[{}]) -> _Table_{}: ...\n",
            serde_json::to_string(table.python)?,
            table.python
        ));
    }
    output.push_str("    @overload\n    def __getitem__(self, key: str) -> Table[Row]: ...\n\napp_tables: _AppTables = ...\n");
    Ok(Some(output))
}
