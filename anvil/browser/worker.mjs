import * as Comlink from './dist/comlink.mjs';
import { stubPacks, completionPreferences } from './dist/stub-packs.mjs';
import { projectContext, contextPosition, contextCompletion, originalCompletion } from './contexts.mjs';
import { components, formPropertyTarget, handlerAnnotations } from './forms.mjs';
import { projectAnnotations } from './source-projection.mjs';
import { renameResource, renameComponent, componentAt, extendAnvilRename, rpcTarget, rpcTargets, rpcReferences, renameRpc, callableRegistrations } from './renames.mjs';
import initialize, * as ty from './dist/wasm/ty_wasm.js';
import initializeCompatibility, { Preparation, symbols, itemFacts, callFacts, literalOptions, renameNames, sourceImports, sourceUpdate, itemAssignments, dictionaryProbes, returnTypeDeclaration, rpcServerStub, rpcSignature, skulptModuleSupported, clientImportFacts, serverPackages, tyConfiguration, validRenameName as isPythonIdentifier } from './dist/compat/anvil_ty_compat.js';

let workspace;
let preparation;
let root;
let revision = 0;
const files = new Map();
const overlays = new Map();
let handles = new Map();
let mounted = new Map();
let workspaceDirectories = new Set();
let preparedRootsJson;
let workspaceOptionsJson;
let configuration = { name: undefined, source: undefined, options: {}, diagnostics: [] };
let preparationDiagnostics = [];
let origins = new Map();
let sourceEnds = new Map();
let projections = new Map();
let tableRows;
let isServer = false;
let sourceEnvironments = new Map();
let formClasses = new Map();
// Parsed metadata belongs to Preparation, including selection of dependencies
// and isolation of malformed Forms. Semantic consumers share that catalogue.
let appConfigs = {};
let formCatalogue = [];
let handlerTypes = {};
let handlerPlans;
let sourceMaps = new Map();
let dependencyRoots = {};
const contexts = new Map();
let nextContextId = 0;
let nextContextGeneration = 0;
let remoteRegistrations;
let registrationInputs;
let remoteInputs;
let formInputs;
const handlerInputs = new Map();
let declarationFiles = new Map();
const loadedPacks = new Map();
const serverPackageMetadata = JSON.stringify(stubPacks.filter(pack => pack.server));
const preferredMembers = new Set(Object.values(completionPreferences).flatMap(preference =>
    [preference.suggestedAttr, ...Object.keys(preference.priority ?? {})]).filter(Boolean));
let packageRequirements;
let serverTypePacks = [];
const updateMethods = ['updateFiles', 'openDocument', 'closeDocument', 'setContext', 'closeContext'];
const preparedViews = new Map();
let resolvedImports = new Map();
const runtimeWorkspaces = new Map();
const producerAssignments = new Map();
const rpcConsumers = new Map();
const parsedSources = new Map();
const parsedImports = new Map();
const registrationPlans = new Map();
// Inferred declarations survive edits outside their producer/import inputs.
// Structural changes still discard them; Ty owns ordinary Python invalidation.
let remoteTypes;
let formItems;
let itemTypeModule;
let queue = Promise.all([initialize(), initializeCompatibility()]);

Comlink.expose({
    request(method, params) {
        const pending = queue.then(async () => {
            await loadPacksForRequest(method, params);
            return { result: request(method, params), revision };
        });
        // A failed query must not prevent later requests from reaching the workspace.
        queue = pending.catch(() => {});
        return pending;
    },
});

function pathForUri(uri) {
    const url = new URL(uri);
    if (url.protocol !== 'file:' || url.host) throw new Error('Expected a local analysis URI');
    return decodeURIComponent(url.pathname);
}

function originalRange(path, range) {
    const end = sourceEnds.get(path);
    return !end || range.end.line < end.line || (range.end.line === end.line && range.end.character <= end.character);
}

function uriForPath(path, range) {
    // Model-base substitutions preserve source positions. Appended namespace
    // exports belong to the generated file, including required rename edits.
    path = !range || originalRange(path, range) ? origins.get(path) ?? path : path;
    return path.startsWith('vendored:') ? path : new URL(path, 'file:///').href;
}

function originalPath(path) {
    if (path !== root && !path.startsWith(root + '/')) throw new Error('Source is outside the analysis project');
    return path;
}

function setFile(path, text) {
    resolvedImports.clear();
    originalPath(path);
    const handle = handles.get(path);
    // WASM filesystem revisions use millisecond timestamps. updateFile can
    // retain stale source when edits share a tick (notably inference snapshots).
    // A close/open pair invalidates the file and its importers in the same DB.
    if (handle) workspace.closeFile(handle);
    handles.delete(path);
    if (text !== null) handles.set(path, workspace.openFile(path, text));
}

function resetWorkspace() {
    resolvedImports.clear();
    for (const handle of handles.values()) handle.free();
    handles.clear();
    workspace?.free();
    workspace = new ty.Workspace(root, ty.PositionEncoding.Utf16, {
        environment: { 'python-version': '3.10', root: [root] },
        analysis: { 'return-type-inference': 'always' },
    });
    mounted = new Map();
    workspaceDirectories = new Set();
    preparedRootsJson = undefined;
    workspaceOptionsJson = undefined;
}

function readConfiguration(current) {
    const name = current.has(`${root}/ty.toml`) ? 'ty.toml' : 'pyproject.toml';
    const source = current.get(`${root}/${name}`) ?? '';
    if (name === configuration.name && source === configuration.source) return configuration;
    const diagnostics = [];
    let options = {};
    let validator;
    try {
        options = JSON.parse(tyConfiguration(source, name === 'pyproject.toml'));
        const isTable = value => value !== null && typeof value === 'object' && !Array.isArray(value);
        // serde-wasm-bindgen accepts an empty JS array as a map. TOML settings
        // require tables, so reject those shapes before native deserialization.
        if (!isTable(options) || ['rules', 'analysis'].some(key => key in options && !isTable(options[key])))
            throw new Error('Ty settings, rules and analysis must be TOML tables.');
        // Source patterns and filesystem discovery cannot describe Anvil's
        // projected modules. Support native rules/analysis; Anvil owns runtime paths.
        if (Object.keys(options).some(key => !['rules', 'analysis'].includes(key)))
            throw new Error('The IDE supports Ty rules and analysis settings; Python versions and search paths come from the app runtime.');
        // Validate once in an empty workspace. checkFile does not expose Ty's
        // project-setting diagnostics, and checking the real workspace would lint every mounted stub.
        if (Object.keys(options).length) {
            validator = new ty.Workspace(root, ty.PositionEncoding.Utf16, options);
            for (const diagnostic of validator.check()) {
                try { diagnostics.push(String(diagnostic.message())); }
                finally { diagnostic.free(); }
            }
        }
    } catch (error) {
        options = {};
        diagnostics.push(`${error instanceof Error ? error.message : String(error)} Using default Ty settings.`);
    } finally { validator?.free(); }
    configuration = { name, source, options, diagnostics: diagnostics.map(message => `Ty configuration in ${name}: ${message}`) };
    return configuration;
}

function fileHandle(uri) {
    if (uri.startsWith('vendored:')) {
        let handle = handles.get(uri);
        if (!handle) {
            const url = new URL(uri);
            handle = workspace.getVendoredFile(url.host + url.pathname);
            handles.set(uri, handle);
        }
        return handle;
    }
    const original = originalPath(pathForUri(uri));
    const path = projections.get(original) ?? original;
    const handle = handles.get(path);
    if (!handle) throw new Error(`Source is unavailable: ${uri}`);
    return handle;
}

function range(value) {
    const start = value.start;
    const end = value.end;
    try {
        return { start: { line: start.line - 1, character: start.column - 1 },
            end: { line: end.line - 1, character: end.column - 1 } };
    } finally { start.free(); end.free(); value.free(); }
}

function mappedRange(path, selected) {
    return sourceMaps.has(path) ? sourceMaps.get(path).range(selected) : selected;
}

function queryPosition(handle, position) {
    const projected = sourceMaps.get(handle.path())?.position(position) ?? position;
    return new ty.Position(projected.line + 1, projected.character + 1);
}

function sourceText(uri) {
    if (uri.startsWith('file:')) {
        const path = pathForUri(uri);
        const source = overlays.get(path) ?? files.get(path);
        if (source !== undefined) return source;
    }
    return workspace.sourceText(fileHandle(uri));
}

function renameEdits(edits) {
    return edits.flatMap(edit => {
        try {
            const selected = mappedRange(edit.path, range(edit.range));
            return selected ? [{ uri: uriForPath(edit.path, selected), range: selected, newText: edit.new_text }] : [];
        } finally { edit.free(); }
    });
}

function locations(targets) {
    return targets.flatMap(target => {
        try {
            const selected = mappedRange(target.path, range(target.selection_range ?? target.full_range));
            return selected ? [{ uri: uriForPath(target.path, selected), range: selected }] : [];
        }
        finally { target.free(); }
    });
}

// Canonical app/dependency packages share this search root with generated
// modules. Keep private names disjoint from those real package identities.
function privateModule(name) {
    const packages = Object.values(appConfigs).map(config => config.package_name ?? 'main_app_package');
    while (packages.includes(name)) name += '_';
    return name;
}

function selectWorkspace(server) {
    if (server === isServer) return;
    runtimeWorkspaces.set(isServer, { workspace, handles, mounted, workspaceDirectories, preparedRootsJson, workspaceOptionsJson, resolvedImports });
    const saved = runtimeWorkspaces.get(server);
    workspace = saved?.workspace;
    handles = saved?.handles ?? new Map();
    mounted = saved?.mounted ?? new Map();
    workspaceDirectories = saved?.workspaceDirectories ?? new Set();
    preparedRootsJson = saved?.preparedRootsJson;
    workspaceOptionsJson = saved?.workspaceOptionsJson;
    resolvedImports = saved?.resolvedImports ?? new Map();
    if (!workspace) resetWorkspace();
    isServer = server;
}

function prepareApp(server = isServer, items = formItems) {
    selectWorkspace(server);
    const current = new Map([...files, ...overlays]);
    const { options: userOptions } = readConfiguration(current);
    const annotations = JSON.stringify(items?.annotations ?? {});
    // Keep only the latest annotation variant for each runtime. Validated body
    // edits patch these views; structural/model/member changes replace them.
    let cached = preparedViews.get(server);
    if (cached?.annotations !== annotations) {
        cached = { annotations, prepared: JSON.parse(preparation.prepare(root, JSON.stringify(Object.fromEntries(current)), server, annotations)) };
        preparedViews.set(server, cached);
    }
    const prepared = cached.prepared;
    appConfigs = prepared.apps ?? {};
    const preparedFiles = [...Object.entries(prepared.files)];
    for (const pack of availablePacks(server)) {
        // A small discoverable root keeps import completion useful before the
        // first query needs the package's declarations.
        const source = loadedPacks.get(String(pack.url)) ?? Object.fromEntries(pack.modules.map(module => [`${module}/__init__.pyi`, '']));
        for (const [path, text] of Object.entries(source)) preparedFiles.push([`${root}/.anvil/types/${server ? 'server' : 'client'}/${path}`, text]);
    }
    declarationFiles = new Map(preparedFiles.filter(([path]) => path.endsWith('.pyi')));
    tableRows = prepared.tableRows;
    formClasses = new Map(Object.entries(prepared.formClasses ?? {}));
    handlerTypes = prepared.handlerTypes ?? {};
    itemTypeModule = privateModule('_anvil_form_items');
    formCatalogue = (prepared.forms ?? []).map(({ path, ...form }) =>
        ({ ...form, uri: uriForPath(path), config: appConfigs[form.root] }));
    dependencyRoots = prepared.dependencyRoots ?? {};
    preparationDiagnostics = prepared.diagnostics ?? [];
    origins = new Map(Object.entries(prepared.sources ?? {}));
    projections = new Map([...origins].map(([canonical, original]) => [original, canonical]));
    const excluded = new Set(prepared.excludedSources ?? []);
    sourceEnvironments = new Map(Object.entries(prepared.sourceEnvironments ?? {}));
    const next = new Map([
        // Apply config explicitly so invalid TOML cannot leave native discovery
        // holding old rules. The original extra files remain available to readers.
        ...[...current].filter(([path]) => !excluded.has(path) && path !== `${root}/ty.toml` && path !== `${root}/pyproject.toml`),
        ...preparedFiles,
    ]);
    if (formClasses.size) next.set(`${prepared.roots[0]}/${itemTypeModule}.pyi`, itemDeclarationSource(items?.declarations ?? []));
    if (remoteTypes?.length) {
        for (const entry of rpcDeclarations()) next.set(`${prepared.roots[0]}/${entry.module}.pyi`, entry.source);
        const path = `${root}/.anvil/types/${server ? 'server' : 'client'}/anvil/server.pyi`;
        next.set(path, rpcServerStub(next.get(path), JSON.stringify(remoteTypes)));
    }
    sourceMaps = new Map();
    for (const [original, plan] of handlerPlans ?? []) {
        const canonical = projections.get(original);
        if (!canonical) continue;
        const projected = projectAnnotations(next.get(canonical), plan.edits, plan.declarations);
        sourceMaps.set(canonical, projected);
        next.set(canonical, projected.text);
    }
    for (const context of contexts.values()) {
        if (context.server !== server) continue;
        let path = `${prepared.contextRoot}/_anvil_context_${context.serial}.py`;
        while (next.has(path)) {
            context.serial = ++nextContextId;
            path = `${prepared.contextRoot}/_anvil_context_${context.serial}.py`;
        }
        let form;
        if (context.value.kind === 'binding') {
            const original = pathForUri(context.value.formUri);
            const canonical = projections.get(original);
            if (!canonical) {
                if (context.document) context.generation = ++nextContextGeneration;
                context.document = undefined;
                continue;
            }
            const module = canonical.slice(prepared.roots[0].length + 1).replace(/(?:\/__init__)?\.py$/, '').replaceAll('/', '.');
            form = { module, name: formClasses.get(original) ?? module.split('.').at(-1) };
        }
        const document = projectContext(context.value, uriForPath(path), context.generation, form);
        if (context.document && (context.document.uri !== document.uri || context.document.text !== document.text))
            document.generation = context.generation = ++nextContextGeneration;
        context.document = document;
        next.set(path, document.text);
    }
    sourceEnds = new Map([...origins].flatMap(([path, original]) => {
        const text = current.get(original);
        if (next.get(path) === text) return [];
        const lines = text.split(/\r\n|\r|\n/);
        return [[path, { line: lines.length - 1, character: lines.at(-1).length }]];
    }));
    const roots = JSON.stringify(prepared.roots);
    const directories = new Set();
    for (const path of next.keys()) {
        for (let directory = path.slice(0, path.lastIndexOf('/')); directory; directory = directory.slice(0, directory.lastIndexOf('/')))
            directories.add(directory);
    }
    // ty's WASM file API refreshes a file's parent, but not newly created ancestor
    // directories. Rebuild for new directories in the current search roots so a
    // previously unresolved package can become importable. Ordinary edits stay incremental.
    if (roots === preparedRootsJson && [...directories].some(path => !workspaceDirectories.has(path))) resetWorkspace();
    for (const path of mounted.keys()) if (!next.has(path)) setFile(path, null);
    for (const [path, text] of next) if (mounted.get(path) !== text) setFile(path, text);
    mounted = next;
    for (const directory of directories) workspaceDirectories.add(directory);
    const environment = JSON.parse(current.get(`${root}/.anvil/python-environment.json`) ?? '{}');
    const options = { ...userOptions, environment: { 'python-version': server ? environment.server ?? '3.10' : '3.7', root: prepared.roots },
        analysis: { 'return-type-inference': 'always', ...userOptions.analysis } };
    const optionsJson = JSON.stringify(options);
    if (optionsJson !== workspaceOptionsJson) {
        workspace.updateOptions(options);
        workspaceOptionsJson = optionsJson;
    }
    preparedRootsJson = roots;
    isServer = server;
}

function selectEnvironment(uri) {
    // Each runtime retains its own Ty database, including server overrides of
    // client modules. Preparation restores the matching source projections.
    const server = environmentFor(uri);
    if (server !== undefined && server !== isServer) prepareApp(server);
}

function environmentFor(uri) {
    if (uri.startsWith('vendored:')) return;
    const path = originalPath(pathForUri(uri));
    let server = sourceEnvironments.get(path);
    for (const environment of ['client', 'server']) {
        if (path.startsWith(`${root}/.anvil/types/${environment}/`) || path.startsWith(`${root}/.anvil/analysis/${environment}/`))
            server = environment === 'server';
    }
    return server;
}

// The ordered request queue owns the fetch and mount. Source updates stay
// synchronous; a failed fetch rejects only its query and a later query can retry.
function availablePacks(server) {
    if (!server) return stubPacks.filter(pack => !pack.server);
    const requirements = [...JSON.parse(files.get(`${root}/.anvil/server-requirements.json`) ?? '[]'),
        appConfigs[root]?.runtime_options?.server_spec?.requirements ?? ''].join('\n');
    if (requirements !== packageRequirements) {
        const urls = JSON.parse(serverPackages(requirements, serverPackageMetadata));
        serverTypePacks = stubPacks.filter(pack => pack.server && urls.includes(String(pack.url)));
        packageRequirements = requirements;
    }
    return serverTypePacks;
}

function packForPath(path) {
    return availablePacks(path.includes('/.anvil/types/server/')).find(pack => pack.modules.some(module =>
        path.startsWith(`${root}/.anvil/types/${pack.server ? 'server' : 'client'}/${module}/`)));
}

async function loadPacksForRequest(method, params) {
    if (method === 'initialize' || updateMethods.includes(method)) return;
    const uri = params.textDocument?.uri ?? params.uri ?? params.data?.documentation?.uri;
    const server = method === 'queryContext' ? contexts.get(params.id)?.server : uri && environmentFor(uri);
    if (typeof server !== 'boolean') return;
    const available = availablePacks(server);
    const pending = available.filter(pack => !loadedPacks.has(String(pack.url)));
    if (!pending.length) return;
    const current = new Map([...files, ...overlays]);
    const requested = uri && !uri.startsWith('vendored:') && packForPath(pathForUri(uri));
    const imports = new Set();
    const modules = pending.flatMap(pack => pack.modules);
    const collect = source => {
        if (!modules.some(module => source.includes(module))) return;
        for (const imported of importsFor(source)) if (!imported.relative && imported.module) imports.add(imported.module.split('.')[0]);
    };
    for (const [path, sourceServer] of sourceEnvironments) if (server || !sourceServer) collect(current.get(path));
    for (const context of contexts.values()) if (context.server === server) collect((context.value.previousCode ?? '') + '\n' + context.value.code);
    const needed = pending.filter(pack => pack === requested || pack.modules.some(module => imports.has(module)));
    for (const pack of needed) for (const id of pack.dependencies ?? []) {
        const dependency = pending.find(candidate => candidate.id === id);
        if (dependency && !needed.includes(dependency)) needed.push(dependency);
    }
    if (!needed.length) return;
    const fetched = await Promise.all(needed.map(async pack => {
        const response = await fetch(pack.url);
        if (!response.ok) throw new Error(`Could not load ${pack.id === 'plotly-client' ? 'Plotly' : pack.id} completion declarations: HTTP ${response.status}`);
        return [String(pack.url), await response.json()];
    }));
    for (const [id, source] of fetched) loadedPacks.set(id, source);
    // New declarations can improve previously gradual Anvil-derived types.
    clearInference();
    prepareApp();
}

function readOnly(uri) {
    if (uri.startsWith('vendored:')) return true;
    const path = pathForUri(uri);
    return path.endsWith('.pyi') || path.includes('/.anvil/');
}

function rowKeyCompletions(handle, position) {
    if (!tableRows?.length) return;
    const line = workspace.sourceText(handle).split('\n')[position.line];
    const prefix = line.slice(0, position.character);
    const subscript = /\[\s*(?:(['"])((?:\\.|(?!\1)[^\\\n])*))?$/.exec(prefix);
    if (!subscript || subscript.index === 0) return;
    // ty infers schema-backed row classes, but its subscript completion does not
    // offer their Literal overload keys. Use the receiver's semantic type identity.
    const rowFor = target => tableRows.find(row => uriForPath(row.path) === target.uri && row.name === selectedName(target));
    let targets = locations(workspace.gotoTypeDefinition(handle, new ty.Position(position.line + 1, subscript.index)));
    if (!targets.some(rowFor) && line.slice(0, subscript.index).trimEnd().endsWith(')')) {
        const path = handle.path();
        // Navigation on call parentheses describes the callable. Ask for the
        // result object's class in an analysis copy, keeping inference in Ty.
        targets = withTemporarySources(snapshot => {
            const lines = snapshot.source(path).split('\n');
            lines[position.line] = line.slice(0, subscript.index) + '.__class__' + line.slice(subscript.index);
            snapshot.replace(path, lines.join('\n'));
            return locations(workspace.gotoTypeDefinition(handles.get(path), new ty.Position(position.line + 1, subscript.index + 3)));
        });
    }
    for (const target of targets) {
        const keys = rowFor(target)?.keys;
        if (keys) {
            const quote = subscript[1];
            let end = position.character;
            while (quote && end < line.length && line[end] !== quote) {
                if (line[end] === '\\') end++;
                end++;
            }
            const typed = (subscript[2] ?? '').replace(/\\(['"\\])/g, '$1');
            return keys.filter(key => key.startsWith(typed)).map(label => ({
                label: quote ? label : JSON.stringify(label), kind: 5,
                textEdit: {
                    range: { start: { line: position.line, character: position.character - (subscript[2]?.length ?? 0) },
                        end: { line: position.line, character: end } },
                    newText: quote ? JSON.stringify(label).slice(1, -1).replaceAll("'", quote === "'" ? "\\'" : "'") : JSON.stringify(label),
                },
            }));
        }
    }
}

function queryColumnCompletions(handle, position, arguments_) {
    if (!tableRows?.length) return [];
    const before = (a, b) => a.line < b.line || (a.line === b.line && a.character <= b.character);
    const contains = range => before(range.start, position) && before(position, range.end);
    const calls = arguments_.filter(call => contains(call.range)).reverse();
    const current = calls[0];
    if (!current || current.values.some(value => contains(value) && !value.isIdentifier)) return [];
    const identifier = current.values.find(value => contains(value) && value.isIdentifier);
    const prefix = identifier ? workspace.sourceText(handle).split(/\r\n|\r|\n/)[position.line]
        .slice(identifier.start.character, position.character) : '';
    const apiRoot = `${root}/.anvil/types/${isServer ? 'server' : 'client'}/anvil/tables/`;
    // Query combinators inherit columns from their enclosing table search/get.
    // Resolve every callee through ty so aliases work and unrelated calls do not.
    let query = false;
    for (const call of calls) {
        const targets = locations(workspace.gotoTypeDefinition(handle, new ty.Position(call.position.line + 1, call.position.character + 1)));
        const operator = targets.some(target => target.uri === uriForPath(apiRoot + 'query.pyi') &&
            ['any_of', 'all_of', 'none_of', 'not_'].includes(selectedName(target)));
        if (operator) { query = true; continue; }
        if (!query) return [];
        for (const target of targets) {
            if (target.uri !== uriForPath(apiRoot + '__init__.pyi') ||
                !['search', 'get', 'client_readable', 'client_writable', 'client_writable_cascade'].includes(selectedName(target))) continue;
            const declaration = JSON.parse(symbols(workspace.sourceText(fileHandle(target.uri))))
                .find(symbol => symbol.range.start.line === target.range.start.line && symbol.name === selectedName(target));
            if (!declaration?.containerName?.startsWith('_Table_')) continue;
            const row = tableRows.find(row => row.name === declaration?.containerName?.replace(/^_Table_/, '_Row_'));
            return (row?.keys ?? []).filter(name => isPythonIdentifier(name) && name.startsWith(prefix) && !current.keywords.includes(name))
                .map(name => ({ label: name + '=', kind: 5, textEdit: {
                    range: identifier ? { start: identifier.start, end: identifier.end } : { start: position, end: position },
                    newText: name + '=',
                } }));
        }
        return [];
    }
    return [];
}

function acrossRuntimes(uri, position, query) {
    // RPC registration discovery may have visited the server since the request began.
    selectEnvironment(uri);
    const handle = fileHandle(uri);
    // These imports are derived from user declarations and regenerated after
    // edits. They are neither user references nor required rename participants.
    const inferredUris = new Set([...rpcDeclarations().map(entry => entry.module), itemTypeModule].flatMap(module => ['client', 'server'].map(environment =>
        uriForPath(`${root}/.anvil/analysis/${environment}/${module}.pyi`))));
    const mapped = sourceMaps.get(handle.path())?.position(position) ?? position;
    const result = query(handle, mapped).filter(target => !inferredUris.has(target.uri));
    const key = location => JSON.stringify([location.uri, location.range]);
    const changed = new Set(result.map(key));
    const definitions = locations(workspace.gotoDefinition(handle, queryPosition(handle, position)))
        .filter(target => target.uri.startsWith('file:') && sourceEnvironments.get(pathForUri(target.uri)) === false && changed.has(key(target)));
    if (!definitions.length) return result;
    const originalEnvironment = isServer;
    try {
        // A client declaration can also have server callers. Explicit local
        // aliases stay local: only follow declarations included by ty itself.
        prepareApp(!originalEnvironment);
        for (const definition of definitions) {
            if (projections.has(pathForUri(definition.uri))) {
                const target = fileHandle(definition.uri);
                const position = sourceMaps.get(target.path())?.position(definition.range.start) ?? definition.range.start;
                result.push(...query(target, position));
            }
        }
    } finally { prepareApp(originalEnvironment); }
    return [...new Map(result.filter(target => !inferredUris.has(target.uri)).map(location => [key(location), location])).values()];
}

function sourceSymbols(uri, text) {
    return JSON.parse(symbols(text)).map(({ range, ...symbol }) => ({ ...symbol, location: { uri, range } }));
}

function selectedName(target) {
    const line = sourceText(target.uri).split('\n')[target.range.start.line];
    return line.slice(target.range.start.character, target.range.end.character);
}

const eventMethods = ['set_event_handler', 'add_event_handler', 'remove_event_handler', 'raise_event', 'get_event_handlers'];

function apiFunction(handle, position) {
    const targets = locations(workspace.gotoTypeDefinition(handle, new ty.Position(position.line + 1, position.character + 1)));
    for (const target of targets) {
        if (!target.uri.startsWith('file:')) continue;
        const path = pathForUri(target.uri);
        const name = selectedName(target);
        if (eventMethods.includes(name) && path.startsWith(`${root}/.anvil/analysis/`) && path.endsWith('/_anvil_designer.pyi')) return name;
        if (!path.startsWith(root + '/.anvil/types/')) continue;
        const module = eventMethods.includes(name) ? '__init__' : { get_secret: 'secrets', encrypt_with_key: 'secrets', decrypt_with_key: 'secrets', open_form: '__init__', render_form: 'pdf', load_form: 'server', FormResponse: 'server', handle: '__init__', http_endpoint: 'server', route: 'server', handle_message: 'email', background_task: 'server', callable: 'server', call: 'server', call_s: 'server', launch_background_task: 'server' }[name];
        if (module && path === `${root}/.anvil/types/${isServer ? 'server' : 'client'}/anvil/${module}.pyi`) return name;
    }
}

function stringArgument(decorator, name, index) {
    return (Object.hasOwn(decorator.keywords, name) ? decorator.keywords[name] : decorator.args[index]) ?? undefined;
}

function registrations() {
    if (remoteRegistrations) return remoteRegistrations;
    const originalEnvironment = isServer;
    const result = { callables: [], tasks: [] };
    try {
        prepareApp(true);
        const context = renameContext();
        result.entries = [];
        registrationInputs = new Set();
        for (const [path, source] of context.files) {
            if (!path.endsWith('.py') || !path.includes('/server_code/')) continue;
            let plan = registrationPlans.get(path);
            if (!plan) {
                plan = { entries: callableRegistrations({ ...context, files: new Map([[path, source]]) }), inputs: sourceInputs([path]) };
                registrationPlans.set(path, plan);
            }
            result.entries.push(...plan.entries);
            for (const input of plan.inputs) registrationInputs.add(input);
        }
        for (const item of result.entries)
            result[item.kind === 'callable' ? 'callables' : 'tasks'].push({ name: item.name, filePath: pathForUri(item.uri) });
    } finally { prepareApp(originalEnvironment); }
    return remoteRegistrations = result;
}

function insertions(source, edits) {
    const lines = source.split('\n');
    const offset = position => lines.slice(0, position.line).reduce((length, line) => length + line.length + 1, 0) + position.character;
    for (const edit of edits.reverse().sort((a, b) => offset(b.position) - offset(a.position)))
        source = source.slice(0, offset(edit.position)) + edit.text + source.slice(offset(edit.position));
    return source;
}

function annotatedResult(source, handle) {
    const lines = source.split('\n');
    const offset = position => lines.slice(0, position.line).reduce((length, line) => length + line.length + 1, 0) + position.character;
    const edits = [];
    for (const hint of workspace.inlayHints(handle, new ty.Range(new ty.Position(1, 1), new ty.Position(lines.length, 1)))) {
        try {
            // The scaffold has one function. Other hints (argument names) have
            // no annotation edits and must not be interpreted as type syntax.
            for (const edit of hint.text_edits) {
                try { edits.push({ range: range(edit.range), text: edit.new_text }); }
                finally { edit.free(); }
            }
        } finally { hint.free(); }
    }
    for (const edit of edits.sort((a, b) => offset(b.range.start) - offset(a.range.start))) {
        source = source.slice(0, offset(edit.range.start)) + edit.text + source.slice(offset(edit.range.end));
    }
    return JSON.parse(returnTypeDeclaration(source));
}

function itemDeclarationSource(declarations) {
    return declarations.map(entry => entry.shape ? entry.source :
        `class ${entry.name}:\n${entry.source.split('\n').filter(line => line.length).map(line => '    ' + line).join('\n')}\n`).join('\n');
}

// Inference instruments analysis copies, never original files. This scope is
// the only owner of temporary replacements; all exits restore those copies.
function withTemporarySources(run) {
    const originals = new Map();
    const source = path => {
        if (!originals.has(path)) originals.set(path, workspace.sourceText(handles.get(path)));
        return originals.get(path);
    };
    try {
        return run({ source, replace(path, text) { source(path); setFile(path, text); } });
    } finally {
        for (const [path, text] of originals) setFile(path, text);
    }
}

function ensureFormItems() {
    if (formItems) return;
    const result = { annotations: {}, declarations: [] };
    const producers = [...sourceEnvironments].filter(([path, server]) => !server && path.endsWith('.py') && assignmentsFor(path).length);
    if (!producers.length) {
        formInputs = new Set();
        formItems = result;
        return;
    }
    const originalEnvironment = isServer;
    try {
        prepareApp(false);
        const context = renameContext();
        const forms = context.forms;
        const formDeclarations = new Map(forms.map(form => [form.uri,
            sourceFacts(context.source(form.uri)).classes.find(cls => cls.owner === null && cls.name === formClasses.get(pathForUri(form.uri)))]));
        const candidates = new Map();
        const producerPaths = new Set();
        const probes = new Map();
        for (const [original] of projections) {
            if (!original.endsWith('.py') || sourceEnvironments.get(original) !== false) continue;
            const uri = uriForPath(original);
            const form = forms.find(form => form.uri === uri);
            const panels = form ? components(form.data).filter(component => ['RepeatingPanel', 'anvil.RepeatingPanel'].includes(component.type)) : [];
            const source = context.source(uri);
            const assignments = assignmentsFor(original);
            if (assignments.length) producerPaths.add(original);
            for (const assignment of assignments) {
                let template;
                if (assignment.target.constructorPosition) {
                    const targets = context.definitions(uri, assignment.target.constructorPosition);
                    if (targets.length !== 1) continue;
                    template = forms.find(form => {
                        const declaration = formDeclarations.get(form.uri)?.range;
                        return form.uri === targets[0].uri && declaration?.start.line === targets[0].range.start.line &&
                            declaration.start.character === targets[0].range.start.character;
                    });
                } else {
                    const panel = panels.find(panel => panel.name === assignment.target.component);
                    if (!panel) continue;
                    template = formPropertyTarget(panel.properties?.item_template, form, forms, dependencyRoots);
                    if (!template) continue;
                    // Resolve the real Form member before instrumenting sources.
                    const members = context.member(uri, panel.name);
                    if (!context.definitions(uri, assignment.target.position).some(target =>
                        members.some(member => member.uri === target.uri && JSON.stringify(member.range) === JSON.stringify(target.range)))) continue;
                }
                if (!template) continue;
                if (!candidates.has(template.uri)) candidates.set(template.uri, new Set());
                let name = `_anvil_items_${probes.size}`;
                while (source.includes(name)) name += '_';
                const probe = { uri, name, value: assignment.value, iterable: !assignment.target.constructorPosition };
                probes.set(name, probe);
                candidates.get(template.uri).add(probe);
            }
        }
        formInputs = sourceInputs([...producerPaths, ...[...candidates.keys()].map(pathForUri)]);
        if (!probes.size) { formItems = result; return; }
        const base = JSON.parse(preparedRootsJson)[0];
        const ownerModule = uri => projections.get(pathForUri(uri)).slice(base.length + 1).replace(/(?:\/__init__)?\.py$/, '').replaceAll('/', '.');
        const declaration = (source, prefix = '_anvil_form_item') => {
            const name = `${prefix}_${result.declarations.length}`;
            const handle = workspace.openFile(`${base}/${privateModule(`_probe_${name}`)}.py`, source);
            try {
                const entry = { name, ...annotatedResult(source, handle) };
                result.declarations.push(entry);
                return entry;
            } finally { workspace.closeFile(handle); }
        };
        const mountProbes = (dictionaries, snapshot) => {
            for (const [original, canonical] of projections) {
                const uri = uriForPath(original);
                const facts = dictionaries.get(uri);
                const exports = [...probes.values()].filter(probe => probe.uri === uri);
                if (!facts && !exports.length) continue;
                const source = snapshot.source(canonical);
                const edits = exports.flatMap(probe => [
                    { position: probe.value.statement, text: `global ${probe.name}; ` },
                    { position: probe.value.start, text: `(${probe.name} := ` },
                    { position: probe.value.end, text: ')' },
                ]);
                if (facts) {
                    const imports = [];
                    let cast = '_anvil_item_cast';
                    while (source.includes(cast)) cast += '_';
                    for (const dictionary of facts.dictionaries) {
                        imports.push(`from ${itemTypeModule} import ${dictionary.className}`);
                        edits.push({ position: dictionary.start, text: `${cast}(${dictionary.className}, ` },
                            { position: dictionary.end, text: ')' });
                    }
                    imports.push(`from typing import cast as ${cast}`);
                    edits.push({ position: facts.imports, text: '\n' + imports.join('\n') + '\n' });
                }
                snapshot.replace(canonical, insertions(source, edits));
            }
        };
        const inferProbe = probe => declaration(`from typing import TypeAlias as _AnvilTypeAlias\nfrom ${ownerModule(probe.uri)} import ${probe.name} as _anvil_target\n\ndef _anvil_result():\n    return ${probe.iterable ? 'next(iter(_anvil_target))' : '_anvil_target'}\n`);
        // Keep ordinary Python inference authoritative. Shape projection is only
        // used when the item itself is a dict, never for dict.values()/items()
        // or an operation whose normal inferred result is more precise.
        withTemporarySources(snapshot => {
            mountProbes(new Map(), snapshot);
            for (const probe of probes.values()) probe.declaration = inferProbe(probe);
        });
        // Preserve literal dictionary shapes using ordinary TypedDicts. The first
        // snapshot exports each field value; ty supplies the annotation/imports.
        // The second snapshot casts the literals to those generated declarations
        // before asking for the iterable element type. No user source is retained
        // with instrumentation or shifted positions.
        // Only inspect dictionary producers and their resolved client imports.
        // Unimported modules often contain large data constants; annotating those
        // fields on every editor change contributes no item information.
        const relevant = new Set([...probes.values()].filter(probe => probe.declaration.dictionary).map(probe => probe.uri));
        for (const uri of relevant) {
            for (const name of JSON.parse(renameNames(context.source(uri))).filter(name => name.imported)) {
                for (const target of context.definitions(uri, name.range.start)) {
                    if (!target.uri.startsWith('file:')) continue;
                    const path = pathForUri(target.uri);
                    if (path.endsWith('.py') && projections.has(path) && sourceEnvironments.get(path) === false) relevant.add(target.uri);
                }
            }
        }
        withTemporarySources(snapshot => {
            const dictionaries = new Map();
            let nextDictionary = 0;
            for (const uri of relevant) {
                const canonical = projections.get(pathForUri(uri));
                const handle = handles.get(canonical);
                const source = workspace.sourceText(handle);
                const facts = JSON.parse(dictionaryProbes(source));
                if (!facts.dictionaries.length) continue;
                const edits = [];
                for (const dictionary of facts.dictionaries) {
                    dictionary.className = `_AnvilDictionary${nextDictionary++}`;
                    while (source.includes(dictionary.className)) dictionary.className += '_';
                    for (const [index, field] of dictionary.fields.entries()) {
                        let name = `${dictionary.className}_value${index}`;
                        while (source.includes(name)) name += '_';
                        field.name = name;
                        // A singleton list widens literal data ("Ada" -> str), so
                        // equal schemas with different values remain compatible.
                        edits.push({ position: dictionary.statement, text: `global ${name}; ` },
                            { position: field.start, text: `(${name} := [` }, { position: field.end, text: '])[0]' });
                    }
                }
                snapshot.replace(canonical, insertions(source, edits));
                dictionaries.set(uri, facts);
            }
            const shapes = new Map();
            for (const [uri, facts] of dictionaries) for (const dictionary of facts.dictionaries) {
                const fields = dictionary.fields.map(field => {
                    const value = declaration(`from typing import TypeAlias as _AnvilTypeAlias\nfrom ${ownerModule(uri)} import ${field.name} as _anvil_target\n\ndef _anvil_result():\n    return next(iter(_anvil_target))\n`, '_anvil_dict_value');
                    return { ...field, value };
                });
                const shape = JSON.stringify(fields.map(field => [field.key, field.value.source]).sort(([a], [b]) => a.localeCompare(b)));
                if (shapes.has(shape)) {
                    Object.assign(dictionary, shapes.get(shape));
                    continue;
                }
                shapes.set(shape, { className: dictionary.className });
                const source = `from typing import TypedDict\n${dictionary.className} = TypedDict(${JSON.stringify(dictionary.className)}, {${fields.map(field => `${JSON.stringify(field.key)}: ${field.value.name}._Result`).join(', ')}})\n`;
                result.declarations.push({ name: dictionary.className, shape: true, source });
            }
            // This module is mounted before the first Python query. Updating an
            // existing file avoids ty's millisecond directory-discovery revisions;
            // class namespaces isolate imports of unrelated same-named user types.
            snapshot.replace(`${base}/${itemTypeModule}.pyi`, itemDeclarationSource(result.declarations));
            mountProbes(dictionaries, snapshot);
            for (const probe of probes.values()) {
                if (!probe.declaration.dictionary || !dictionaries.size) continue;
                const projected = inferProbe(probe);
                if (projected.annotationModule === itemTypeModule) probe.declaration = projected;
            }
            // Explicit item metadata stays authoritative in Preparation. Conflicting
            // parents keep Any rather than selecting one arbitrarily.
            for (const [uri, items] of candidates) {
                const declarations = [...items].map(item => item.declaration.source);
                if (!declarations.every(value => value === declarations[0])) continue;
                const item = [...items][0];
                result.annotations[pathForUri(uri)] = `${itemTypeModule}.${item.declaration.name}`;
            }
        });
        prepareApp(false, result);
        const typesPath = `${base}/${itemTypeModule}.pyi`;
        const diagnostics = workspace.checkFile(handles.get(typesPath));
        const source = itemDeclarationSource(result.declarations);
        const lines = source.split('\n');
        for (const diagnostic of diagnostics) {
            try {
                if (diagnostic.severity() < ty.Severity.Error) continue;
                const location = diagnostic.toRange(workspace);
                if (!location) continue;
                const selected = range(location);
                // A source-local class can be inferred yet have no importable
                // declaration. Keep only its own exported type gradual.
                const name = lines.slice(0, selected.start.line + 1).findLast(line => line.startsWith('class '))?.split(/[ :]/)[1];
                const entry = result.declarations.find(entry => !entry.shape && entry.name === name);
                if (entry) entry.source = 'from typing import Any, TypeAlias\n_Result: TypeAlias = Any\n';
            } finally { diagnostic.free(); }
        }
        formItems = result;
    } finally {
        prepareApp(originalEnvironment);
    }
}

function rpcTypeImports(entry) {
    const handle = handles.get(`${JSON.parse(preparedRootsJson)[0]}/${entry.module}.pyi`);
    return JSON.stringify(entry.imports.map(position =>
        locations(workspace.gotoDefinition(handle, new ty.Position(position.line + 1, position.character + 1)))
            .map(target => [target.uri.replace(/\/\.anvil\/types\/(client|server)\//, '/.anvil/types/runtime/'), selectedName(target)]).sort()));
}

function rpcDeclarations() {
    return (remoteTypes ?? []).flatMap(entry => [entry, ...(entry.parameters ?? [])]);
}

// Export declarations are mounted in isolated modules in either runtime.
function checkRpcTypes(entries) {
    prepareApp(true);
    const serverImports = new Map(entries.map(entry => [entry.module, rpcTypeImports(entry)]));
    prepareApp(false);
    // A server-local class may have no client declaration. Keep a gradual
    // result for that export rather than exposing server code to clients.
    for (const entry of entries) {
        const handle = handles.get(`${JSON.parse(preparedRootsJson)[0]}/${entry.module}.pyi`);
        const diagnostics = workspace.checkFile(handle);
        const unavailable = diagnostics.some(diagnostic => diagnostic.severity() >= ty.Severity.Error);
        for (const diagnostic of diagnostics) diagnostic.free();
        if (unavailable || serverImports.get(entry.module) !== rpcTypeImports(entry))
            entry.source = 'from typing import Any, TypeAlias\n_Result: TypeAlias = Any\n';
    }
}

function ensureRemoteTypes(needed) {
    remoteTypes ??= [];
    if (needed?.size === 0) return;
    if (remoteRegistrations && remoteRegistrations.entries.every(entry =>
        remoteRegistrations.entries.filter(other => other.kind === entry.kind && other.name === entry.name).length !== 1 ||
        needed && !needed.has(JSON.stringify([entry.kind, entry.name])) ||
        remoteTypes.some(type => type.kind === entry.kind && type.name === entry.name))) return;
    const originalEnvironment = isServer;
    try {
        prepareApp(true);
        const entries = registrations().entries;
        const missing = entries.filter(entry => (!needed || needed.has(JSON.stringify([entry.kind, entry.name]))) &&
            !remoteTypes.some(type => type.kind === entry.kind && type.name === entry.name) &&
            entries.filter(other => other.kind === entry.kind && other.name === entry.name).length === 1);
        if (!missing.length) return;
        const inferred = [];
        const base = JSON.parse(preparedRootsJson)[0];
        for (const entry of missing) {
            const canonical = projections.get(pathForUri(entry.uri));
            const owner = canonical.slice(base.length + 1).replace(/(?:\/__init__)?\.py$/, '').replaceAll('/', '.');
            const module = privateModule(`_anvil_rpc_return_${remoteTypes.length}`);
            const path = `${base}/${module}.py`;
            const source = `from typing import TypeAlias as _AnvilTypeAlias\nfrom ${owner} import ${entry.functionName} as _anvil_target\n\n${entry.isAsync ? 'async ' : ''}def _anvil_result():\n    return ${entry.isAsync ? 'await ' : ''}_anvil_target()\n`;
            const handle = workspace.openFile(path, source);
            try {
                const type = { name: entry.name, kind: entry.kind, module, ...annotatedResult(source, handle) };
                inferred.push(type);
                remoteTypes.push(type);
            } finally { workspace.closeFile(handle); }
        }
        rpcConsumers.clear();
        checkRpcTypes(inferred);
        remoteInputs ??= new Set();
        for (const path of registrationInputs) remoteInputs.add(path);
        for (const path of sourceInputs(rpcDeclarations().map(entry => `${JSON.parse(preparedRootsJson)[0]}/${entry.module}.pyi`))) remoteInputs.add(path);
    } finally { prepareApp(originalEnvironment); }
}

// Prepare parameter contracts only for known calls being queried. Ordinary
// completion must not infer every parameter in every server callable per edit.
function ensureRpcContracts(calls) {
    const entries = [...new Set(calls.map(call => call.entry))].filter(entry => entry.contract === undefined);
    if (!entries.length) return;
    const environment = isServer;
    const registrationsByName = registrations().entries;
    try {
        prepareApp(true);
        const base = JSON.parse(preparedRootsJson)[0];
        const types = [];
        const infer = (owner, name, module) => {
            const source = `from typing import TypeAlias as _AnvilTypeAlias\nfrom ${owner} import ${name} as _anvil_target\n\ndef _anvil_result():\n    return _anvil_target()\n`;
            const handle = workspace.openFile(`${base}/${module}.py`, source);
            try { return { module, ...annotatedResult(source, handle) }; }
            finally { workspace.closeFile(handle); }
        };
        for (const entry of entries) {
            const registration = registrationsByName.find(item => item.kind === entry.kind && item.name === entry.name);
            const canonical = projections.get(pathForUri(registration.uri));
            const owner = canonical.slice(base.length + 1).replace(/(?:\/__init__)?\.py$/, '').replaceAll('/', '.');
            const source = workspace.sourceText(handles.get(canonical));
            entry.contract = JSON.parse(rpcSignature(source, registration.functionName, entry.name));
            if (!entry.contract) continue;
            withTemporarySources(snapshot => {
                snapshot.replace(canonical, source + entry.contract.probeSource);
                if (entry.contract.resultProbe) {
                    Object.assign(entry, infer(owner, entry.contract.resultProbe, entry.module));
                    types.push(entry);
                }
                entry.parameters = entry.contract.probes.map((name, index) => ({ name,
                    ...infer(owner, name, privateModule(`${entry.module}_arg_${index}`)) }));
                types.push(...entry.parameters);
            });
        }
        rpcConsumers.clear();
        checkRpcTypes(types);
        for (const path of sourceInputs(types.map(entry => `${JSON.parse(preparedRootsJson)[0]}/${entry.module}.pyi`))) remoteInputs.add(path);
        for (const entry of entries) if (entry.contract) entry.source += entry.parameters.map(parameter =>
            `from ${parameter.module} import _Result as ${parameter.name}\n`).join('') + entry.contract.declaration;
    } finally { prepareApp(environment); }
}

function ensureHandlerTypes(needed) {
    handlerPlans ??= new Map();
    const forms = formCatalogue.filter(form => (!needed || needed.has(pathForUri(form.uri))) && !handlerInputs.has(pathForUri(form.uri)));
    const servers = [...sourceEnvironments].filter(([path, server]) => {
        if (!server || needed && !needed.has(path) || handlerInputs.has(path)) return false;
        const facts = sourceFacts(sourceText(uriForPath(path)));
        if (facts.functions.some(fn => fn.owner === null && fn.decorators.length && fn.parameters[0] && !fn.parameters[0].annotated)) return true;
        handlerInputs.set(path, new Set([path]));
        return false;
    });
    if (!forms.length && !servers.length) return;
    const originalEnvironment = isServer;
    try {
        if (forms.length && isServer) prepareApp(false);
        for (const form of forms) {
            const path = pathForUri(form.uri);
            const types = handlerTypes[path];
            if (!types) continue;
            const source = sourceText(form.uri);
            const facts = sourceFacts(source);
            const decorated = facts.functions.some(fn => fn.decorators.length);
            const plan = handlerAnnotations(source, facts, formClasses.get(path),
                form.data, decorated ? itemMetadata(form.uri).eventHandlers : [], types);
            if (plan) handlerPlans.set(path, plan);
            handlerInputs.set(path, decorated ? sourceInputs([path]) : new Set([path]));
        }
        for (const form of forms) {
            const path = pathForUri(form.uri);
            const canonical = projections.get(path);
            if (canonical) mountSource(path, preparedViews.get(isServer).prepared.files[canonical]);
        }
        // Resolve incoming-email decorators only for changed producer modules.
        if (servers.length && !isServer) prepareApp(true);
        for (const [path] of servers) {
            const uri = uriForPath(path);
            const source = sourceText(uri);
            let alias = '_anvil_email_message';
            while (source.includes(alias)) alias += '_';
            const edits = sourceFacts(source).functions.flatMap(fn => {
                const first = fn.parameters[0];
                if (fn.owner !== null || !first || first.annotated ||
                    !fn.decorators.some(decorator => apiFunction(fileHandle(uri), decorator.position) === 'handle_message')) return [];
                return [{ position: first.end, text: ': ' + JSON.stringify(alias) }];
            });
            if (edits.length) handlerPlans.set(path, { edits, generatedName: alias, generatedType: "<class 'Message'>",
                declarations: `from anvil.email import Message as ${alias}` });
            handlerInputs.set(path, sourceInputs([path]));
            const canonical = projections.get(path);
            if (canonical) mountSource(path, preparedViews.get(isServer).prepared.files[canonical]);
        }
    } finally { if (isServer !== originalEnvironment) prepareApp(originalEnvironment); }
}

// Keep literal escaping and replacement ranges identical for contextual names,
// events and suggested property values, including raw/concatenated strings.
function literalCompletions(source, call, position, { names }) {
    const lines = source.split('\n');
    const prefix = call.empty ? '' : lines.slice(call.range.start.line, position.line + 1).map((line, index) =>
        line.slice(index === 0 ? call.range.start.character : 0, call.range.start.line + index === position.line ? position.character : undefined)).join('\n');
    const escaped = label => JSON.stringify(label).slice(1, -1).replaceAll("'", call.quote === "'" ? "\\'" : "'");
    return { includePython: !!call.empty, items: [...new Set(names)].sort()
        .filter(label => call.empty || (call.raw ? label : escaped(label)).startsWith(prefix))
        .map(label => ({ label: call.empty ? JSON.stringify(label) : label, kind: 12, textEdit: {
            range: call.empty ? { start: position, end: position } : call.raw ? call.literalRange : call.range,
            newText: call.raw || call.empty ? JSON.stringify(label) : escaped(label),
        } })) };
}

function propertyValueCompletions(handle, position, assignments) {
    const before = (a, b) => a.line < b.line || a.line === b.line && a.character <= b.character;
    const source = workspace.sourceText(handle);
    const assignment = assignments.find(({ range, literal }) => literal
        ? before(literal.range.start, position) && before(position, literal.range.end)
        : JSON.stringify(range.start) === JSON.stringify(range.end) && range.start.line === position.line &&
            range.start.character <= position.character && !source.split('\n')[position.line].slice(range.start.character, position.character).trim());
    if (!assignment) return;
    const empty = JSON.stringify(assignment.range.start) === JSON.stringify(assignment.range.end);
    const call = empty ? { empty: true } : assignment.literal;
    if (!call) return;
    const definitions = locations(workspace.gotoDefinition(handle, new ty.Position(assignment.position.line + 1, assignment.position.character + 1)));
    const names = definitions.flatMap(target => {
        const source = workspace.sourceText(fileHandle(target.uri));
        return [...JSON.parse(literalOptions(source, target.range.start.line)),
            ...JSON.parse(literalOptions(source, target.range.start.line, 'value'))];
    });
    if (!names.length) return;
    return literalCompletions(source, call, position, { names });
}

function hiddenTableDeletion(handle, position) {
    const lines = workspace.sourceText(handle).split('\n');
    const prefix = lines[position.line].slice(0, position.character);
    const member = /\.([\p{ID_Continue}_]*)$/u.exec(prefix);
    if (!member) return false;
    const start = position.character - member[1].length;
    const path = handle.path();
    // Hiding by label would also hide an author's unrelated method. Resolve the
    // completed member in a temporary copy and suppress only the documented
    // bulk-delete API, which Anvil deliberately excludes from suggestions.
    lines[position.line] = lines[position.line].slice(0, start) + 'delete_all_rows' + lines[position.line].slice(position.character);
    return withTemporarySources(snapshot => {
        snapshot.replace(path, lines.join('\n'));
        const targets = locations(workspace.gotoDefinition(handles.get(path), new ty.Position(position.line + 1, start + 1)));
        return targets.length > 0 && targets.every(target =>
            target.uri === uriForPath(`${root}/.anvil/types/${isServer ? 'server' : 'client'}/anvil/tables/__init__.pyi`) &&
            selectedName(target) === 'delete_all_rows');
    });
}

function completionDocumentation(item) {
    const origin = item.data?.documentation;
    if (!origin) return item;
    if (origin.revision !== revision) throw new DOMException('Completion is obsolete', 'AbortError');
    selectEnvironment(origin.uri);
    const handle = fileHandle(origin.uri);
    const path = handle.path();
    const position = sourceMaps.get(path)?.position(origin.position) ?? origin.position;
    const lines = workspace.sourceText(handle).split('\n');
    const line = lines[position.line];
    const member = /\.([\p{ID_Continue}_]*)$/u.exec(line.slice(0, position.character));
    if (!member || !isPythonIdentifier(item.label)) return item;
    const start = position.character - member[1].length;
    const suffix = line.slice(position.character).match(/^[\p{ID_Continue}_]*/u)[0];
    lines[position.line] = line.slice(0, start) + item.label + line.slice(position.character + suffix.length);
    // Ty's completion docs describe a property's value type. Resolve just the
    // selected member with native hover, which knows its actual declaration.
    return withTemporarySources(snapshot => {
        snapshot.replace(path, lines.join('\n'));
        const hover = workspace.hover(handles.get(path), new ty.Position(position.line + 1, start + 1));
        if (!hover) return item;
        try {
            return { ...item, detail: undefined, documentation: { kind: 'markdown', value: hover.markdown },
                data: { ...item.data, documentation: undefined } };
        } finally { hover.free(); }
    });
}

function formHandleCompletions(uri, handle, position, arguments_) {
    const className = uri.startsWith('file:') && formClasses.get(pathForUri(uri));
    if (!className) return;
    const source = workspace.sourceText(handle);
    const before = (a, b) => a.line < b.line || (a.line === b.line && a.character <= b.character);
    const invocation = arguments_.find(call => before(call.range.start, position) && before(position, call.range.end));
    if (!invocation || apiFunction(handle, invocation.position) !== 'handle') return;
    const index = invocation.values.findIndex(value => value.literal && before(value.literal.range.start, position) && before(position, value.literal.range.end));
    const empty = !invocation.values.length;
    if (index < 0 && !empty || index > 1) return;
    const call = empty ? { ...invocation, empty: true } : invocation.values[index].literal;
    const facts = JSON.parse(itemFacts(source));
    const cls = facts.classes.find(cls => cls.name === className && cls.owner === null);
    if (!cls || !facts.functions.some(fn => fn.owner === cls.id && fn.decorators.some(decorator =>
        JSON.stringify(decorator.position) === JSON.stringify(invocation.position)))) return;
    const forms = formCatalogue;
    const form = forms.find(form => form.uri === uri);
    if (!form) return;
    let names = components(form.data).map(component => component.name).filter(name => !name.startsWith('$'));
    if (index === 1) {
        const component = invocation.values[0].literal?.value;
        if (!names.includes(component)) return { includePython: false, items: [] };
        const type = components(form.data).find(child => child.name === component)?.type;
        const target = formPropertyTarget(type?.replace(/^form:/, ''), form, forms, dependencyRoots);
        // Resolve the actual method through ty, then read its literal options
        // from the stub. Ty normalises Literal[...] | str to str before native
        // completion; parsing our API declaration preserves its suggestions.
        const base = JSON.parse(preparedRootsJson)[0];
        const owner = projections.get(pathForUri(uri)).slice(base.length + 1).replace(/(?:\/__init__)?\.py$/, '').replaceAll('/', '.');
        const expression = `self.${component}`;
        const probe = `from ${owner} import ${className} as _Form\ndef _anvil_events(self: _Form):\n    ${expression}.set_event_handler\n`;
        const probeHandle = workspace.openFile(`${base}/${privateModule('_anvil_event_probe')}.py`, probe);
        try {
            const definitions = locations(workspace.gotoDefinition(probeHandle, new ty.Position(3, `    ${expression}.`.length + 1)));
            names = definitions.flatMap(target => JSON.parse(literalOptions(workspace.sourceText(fileHandle(target.uri)), target.range.start.line, "event_name")));
        } finally { workspace.closeFile(probeHandle); }
        if (target) names.push(...(target.data.events ?? []).map(event => event.name));
    }
    return literalCompletions(source, call, position, { names });
}

// Imports are navigation links, not usages. Follow explicit local aliases too:
// ty owns their symbol identities separately from the declaration they import.
// This is a reference-view policy; rename continues using the unfiltered edits.
function referenceLocations(uri, position, context = {}) {
    const app = renameContext();
    const definitions = rpcTargets(uri, position, app)?.map(({ uri, range }) => ({ uri, range })) ??
        acrossRuntimes(uri, position, (handle, position) =>
            locations(workspace.gotoDefinition(handle, new ty.Position(position.line + 1, position.character + 1))));
    const pending = [{ uri, position }];
    const visited = new Set();
    const results = new Map();
    const names = new Map();
    const contains = (range, position) =>
        (range.start.line < position.line || range.start.line === position.line && range.start.character <= position.character) &&
        (range.end.line > position.line || range.end.line === position.line && range.end.character > position.character);
    while (pending.length) {
        const site = pending.pop();
        const key = JSON.stringify(site);
        if (visited.has(key)) continue;
        visited.add(key);
        const references = rpcReferences(site.uri, site.position, app, context.includeDeclaration ?? false) ??
            acrossRuntimes(site.uri, site.position, (handle, position) =>
                locations(workspace.gotoReferences(handle, new ty.Position(position.line + 1, position.character + 1))));
        for (const reference of references) {
            results.set(JSON.stringify(reference), reference);
            if (!names.has(reference.uri)) {
                const source = reference.uri.startsWith('file:') ? app.files.get(pathForUri(reference.uri)) : undefined;
                names.set(reference.uri, JSON.parse(renameNames(source ?? workspace.sourceText(fileHandle(reference.uri)))));
            }
            for (const alias of names.get(reference.uri)) {
                if (alias.importRange && contains(alias.importRange, reference.range.start))
                    pending.push({ uri: reference.uri, position: alias.range.start });
            }
        }
    }
    return [...results.values()].filter(reference =>
        (context.includeDeclaration || !definitions.some(definition => definition.uri === reference.uri && contains(definition.range, reference.range.start))) &&
        (context.includeImports !== false || !names.get(reference.uri).some(name => (name.imported || name.alias) && contains(name.range, reference.range.start))));
}

function owningApp(handle) {
    const base = JSON.parse(preparedRootsJson)[0];
    return Object.entries(appConfigs).find(([, config]) =>
        handle.path().startsWith(`${base}/${config.package_name ?? 'main_app_package'}/`))?.[0] ?? root;
}

// Ty owns constructor signatures, including inherited methods and imported
// types. In an analysis copy only, call the actual Form class in place of
// open_form and blank its name argument. Padding preserves UTF-16 columns;
// restore this copy before ordinary Python completion runs.
function formConstructorCompletions(handle, position, { arguments: calls, imports }) {
    const before = (a, b) => a.line < b.line || a.line === b.line && a.character <= b.character;
    const call = calls.filter(call => before(call.range.start, position) && before(position, call.range.end)).at(-1);
    if (!call || apiFunction(handle, call.position) !== 'open_form') return;
    const first = call.values.find(value => value.index === 0 || value.keyword === 'form');
    if (!first?.literal || before(position, first.end)) return;
    const form = formPropertyTarget(first.literal.value, { root: owningApp(handle) }, formCatalogue, dependencyRoots);
    if (!form) return;
    const canonical = projections.get(pathForUri(form.uri));
    const base = JSON.parse(preparedRootsJson)[0];
    const module = canonical.slice(base.length + 1).replace(/(?:\/__init__)?\.py$/, '').replaceAll('/', '.');
    const source = workspace.sourceText(handle);
    let prefix = '_anvil_open_form_';
    while (source.includes(prefix)) prefix += '_';
    // Bind before module-level calls, after any future imports. Import the
    // module so a Form can query its own constructor without importing its
    // not-yet-defined class while analysing the module's top level.
    const declaration = `import ${module} as ${prefix}module`;
    const values = [...call.values].sort((a, b) => before(a.argumentStart ?? a.start, b.argumentStart ?? b.start) ? -1 : 1);
    const index = values.indexOf(first);
    // Remove the adjacent comma as well, retaining every other argument even
    // when form= follows another keyword or spans several lines.
    const start = index ? values[index - 1].end : first.argumentStart ?? first.start;
    const end = index ? first.end : values[1]?.argumentStart ?? values[1]?.start ?? call.range.end;
    const lines = source.split('\n');
    const offset = position => lines.slice(0, position.line).reduce((sum, line) => sum + line.length + 1, 0) + position.character;
    let padded = source;
    for (const [begin, finish] of [[start, end], [call.callee.start, call.callee.end]]) {
        const from = offset(begin), to = offset(finish);
        padded = padded.slice(0, from) + padded.slice(from, to).replace(/[^\r\n]/g, ' ') + padded.slice(to);
    }
    const projected = projectAnnotations(padded, [
        { position: imports, text: imports.line || imports.character ? `; ${declaration}` : `${declaration}; ` },
        { position: call.callee.start, text: `(${prefix}module.${formClasses.get(pathForUri(form.uri))}` },
        { position: call.callee.end, text: ')' },
    ], '');
    const path = handle.path();
    return withTemporarySources(snapshot => {
        snapshot.replace(path, projected.text);
        const at = projected.position(position);
        return workspace.completions(handles.get(path), new ty.Position(at.line + 1, at.character + 1)).flatMap(item => {
            try {
                if (!item.name.endsWith('=') || item.name === 'form=' || call.keywords.includes(item.name.slice(0, -1))) return [];
                return [{ label: item.name, kind: item.kind === undefined ? undefined : item.kind + 1, detail: item.detail,
                    documentation: item.documentation, insertText: item.insert_text }];
            } finally { item.free(); }
        });
    });
}

function namedArgumentCompletions(handle, position, calls) {
    const before = (a, b) => a.line < b.line || (a.line === b.line && a.character <= b.character);
    const source = workspace.sourceText(handle);
    const invocation = calls.filter(call => before(call.range.start, position) && before(position, call.range.end)).at(-1);
    if (!invocation) return;
    const api = apiFunction(handle, invocation.position);
    const parameters = { get_secret: 'secret_name', encrypt_with_key: 'key_name', decrypt_with_key: 'key_name',
        open_form: 'form', render_form: 'form_name', load_form: 'form_name', FormResponse: 'form_name', call: null, call_s: null, launch_background_task: null,
        ...Object.fromEntries(eventMethods.map(name => [name, 'event_name'])) };
    if (!Object.hasOwn(parameters, api)) return;
    const parameter = parameters[api];
    const first = invocation.values.find(value => value.index === 0 || parameter !== null && value.keyword === parameter);
    const empty = !invocation.values.length;
    if (!empty && (!first?.literal || !before(first.literal.range.start, position) || !before(position, first.literal.range.end))) return;
    const call = empty ? { ...invocation, empty: true } : first.literal;
    let names;
    if (eventMethods.includes(api)) {
        const targets = locations(workspace.gotoDefinition(handle, new ty.Position(invocation.position.line + 1, invocation.position.character + 1)));
        names = targets.flatMap(target => JSON.parse(literalOptions(workspace.sourceText(fileHandle(target.uri)), target.range.start.line, 'event_name')));
    } else if (['get_secret', 'encrypt_with_key', 'decrypt_with_key'].includes(api)) {
        const kind = api === 'get_secret' ? 'secret' : 'key';
        names = Object.values(appConfigs).flatMap(config => Object.entries(config.secrets ?? {})
            .filter(([, secret]) => secret.type === kind).map(([name]) => name));
    } else if (['open_form', 'render_form', 'load_form', 'FormResponse'].includes(api)) {
        const owner = owningApp(handle);
        names = formCatalogue.map(form => form.root === owner ? form.name : `${form.config.package_name}.${form.name}`);
    } else {
        names = registrations()[api === 'launch_background_task' ? 'tasks' : 'callables'].map(item => item.name);
    }
    return literalCompletions(source, call, position, { names });
}

function callableArgument(handle, position, calls) {
    const before = (a, b) => a.line < b.line || a.line === b.line && a.character <= b.character;
    const invocation = calls.findLast(call => before(call.range.start, position) && before(position, call.range.end));
    if (!invocation) return false;
    const value = invocation.values.find(value => before(value.argumentStart ?? value.start, position) && before(position, value.end));
    // The outer parameter does not describe an expression inside a list or lambda.
    if (value && (!value.referenceRange || !before(value.referenceRange.start, position) || !before(position, value.referenceRange.end))) return false;
    const help = workspace.signatureHelp(handle, new ty.Position(position.line + 1, position.character + 1));
    if (!help) return false;
    const signatures = help.signatures;
    try { return signatures[help.active_signature ?? 0]?.active_parameter_expects_callable ?? false; }
    finally {
        for (const signature of signatures) signature.free();
        help.free();
    }
}

function decoratorCompletions(handle, position, { imports, items }) {
    const path = handle.path();
    const source = workspace.sourceText(handle);
    const lines = source.split('\n');
    const match = /^(\s*)@([\p{ID_Continue}.]*)$/u.exec(lines[position.line].slice(0, position.character));
    if (!match) return [];
    const start = { line: position.line, character: match[1].length + 1 };
    // Native suggestions retain imported aliases. Limit semantic probes to these
    // API names and their aliases, rather than checking every in-scope function.
    const required = ['handle', 'http_endpoint', 'route'];
    const aliases = new Set(importsFor(source).flatMap(imported => (imported.bindings ?? [])
        .filter(binding => required.includes(binding.name)).map(binding => binding.alias)));
    withTemporarySources(snapshot => {
        const prefix = match[2].split('.').at(-1);
        for (const item of items) {
            if (item.kind !== 3 || item.additionalTextEdits?.length || !item.label.startsWith(prefix) ||
                !required.includes(item.label) && !aliases.has(item.label)) continue;
            const edited = [...lines];
            const from = position.character - prefix.length;
            edited[position.line] = edited[position.line].slice(0, from) + item.label + edited[position.line].slice(position.character);
            snapshot.replace(path, edited.join('\n'));
            const name = apiFunction(handles.get(path), { line: position.line, character: from });
            if (required.includes(name))
                item.data = { ...item.data, insertParentheses: true };
        }
    });
    if (!isServer) return [];
    return withTemporarySources(snapshot => ['callable', 'background_task', 'http_endpoint', 'route'].flatMap(name => {
        const label = `anvil.server.${name}`;
        if (!label.startsWith(match[2])) return [];
        const edited = [...lines];
        edited[position.line] = edited[position.line].slice(0, start.character) + label + edited[position.line].slice(position.character);
        const at = { line: position.line, character: start.character + 'anvil.server.'.length };
        snapshot.replace(path, edited.join('\n'));
        let additionalTextEdits;
        if (apiFunction(handles.get(path), at) !== name) {
            const projected = projectAnnotations(edited.join('\n'), [{ position: imports,
                text: imports.line || imports.character ? '; import anvil.server' : 'import anvil.server; ' }], '');
            snapshot.replace(path, projected.text);
            if (apiFunction(handles.get(path), projected.position(at)) !== name) return [];
            additionalTextEdits = [{ range: { start: imports, end: imports },
                newText: imports.line || imports.character ? '\nimport anvil.server' : 'import anvil.server\n' }];
        }
        return [{ label, kind: 3, textEdit: { range: { start, end: position }, newText: label }, additionalTextEdits,
            data: { insertParentheses: name === 'http_endpoint' || name === 'route' } }];
    }));
}

function importCompletions(handle, position) {
    if (isServer) return [];
    const line = workspace.sourceText(handle).split('\n')[position.line];
    const match = /^\s*from\s+([\p{ID_Continue}.]*)$/u.exec(line.slice(0, position.character));
    if (!match || /^\s+import\b/.test(line.slice(position.character))) return [];
    const owner = owningApp(handle);
    const current = origins.get(handle.path());
    if (!current?.startsWith(`${owner}/client_code/`)) return [];
    const directory = current.slice(`${owner}/client_code/`.length).split('/').slice(0, -1);
    const items = [];
    for (const original of projections.keys()) {
        if (!original.endsWith('.py') || original === current) continue;
        const app = Object.keys(appConfigs).find(app => original.startsWith(`${app}/client_code/`));
        if (!app) continue;
        const parts = original.slice(`${app}/client_code/`.length).replace(/(?:\/__init__)?\.py$/, '').split('/');
        if (parts[0] === '__init__') continue;
        let common = 0;
        while (common < directory.length && common < parts.length - 1 && directory[common] === parts[common]) common++;
        const prefix = app === owner ? '.'.repeat(directory.length - common + 1) : `${appConfigs[app].package_name}.`;
        const relative = app === owner ? parts.slice(common) : parts;
        const module = prefix + relative.join('.');
        if (!module.startsWith(match[1])) continue;
        const leaf = relative.at(-1);
        const form = formCatalogue.find(form => form.uri === uriForPath(original));
        const from = relative.length > 1 ? prefix + relative.slice(0, -1).join('.') :
            app === owner ? prefix : appConfigs[app].package_name;
        const assisted = form ? `${module} import ${form.name.split('.').at(-1)}` : `${from} import ${leaf}`;
        for (const label of [assisted, module]) items.push({ label, kind: 9,
            textEdit: { range: { start: { line: position.line, character: position.character - match[1].length }, end: position }, newText: label },
            sameApp: app === owner });
    }
    return items.sort((a, b) => Number(b.sameApp) - Number(a.sameApp)).map(({ sameApp, ...item }) => item);
}

// The broad call(str, *Any) fallback intentionally accepts dynamic names. For
// a unique literal RPC, select its portable contract so ty can show/check the
// actual parameters while keeping argument expressions in the caller's runtime.
function rpcCalls(handle, position) {
    const source = workspace.sourceText(handle);
    const facts = JSON.parse(callFacts(source));
    const before = (a, b) => a.line < b.line || a.line === b.line && a.character <= b.character;
    return facts.arguments.flatMap(call => {
        if (position && !(before(call.range.start, position) && before(position, call.range.end))) return [];
        const name = call.values.find(value => value.index === 0)?.literal?.value;
        const entry = remoteTypes.find(entry => entry.kind === 'callable' && entry.name === name);
        return entry && ['call', 'call_s'].includes(apiFunction(handle, call.position)) ? [{ ...call, entry }] : [];
    });
}

function rpcProjection(handle, position) {
    const source = workspace.sourceText(handle);
    const facts = JSON.parse(callFacts(source));
    const calls = rpcCalls(handle, position).filter(call => call.entry.contract);
    if (!calls.length) return;
    if (position) calls.splice(0, calls.length - 1);
    let prefix = '_anvil_rpc_';
    while (source.includes(prefix)) prefix += '_';
    const lines = source.split('\n');
    const offset = position => lines.slice(0, position.line).reduce((sum, line) => sum + line.length + 1, 0) + position.character;
    let padded = source;
    for (const call of [...calls].sort((a, b) => offset(b.callee.start) - offset(a.callee.start))) {
        const start = offset(call.callee.start), end = offset(call.callee.end);
        padded = padded.slice(0, start) + padded.slice(start, end).replace(/[^\r\n]/g, ' ') + padded.slice(end);
    }
    const imports = calls.map((call, index) => `from ${call.entry.module} import _call as ${prefix}${index}`).join('; ');
    return projectAnnotations(padded, [
        { position: facts.imports, text: facts.imports.line || facts.imports.character ? `; ${imports}` : `${imports}; ` },
        ...calls.flatMap((call, index) => [
            { position: call.callee.start, text: `(${prefix}${index}` },
            { position: call.callee.end, text: ')' },
        ]),
    ], '');
}

// Reuse the same portable call signature as diagnostics, asking Ty for keyword
// names only. Value expressions keep the ordinary caller-runtime completion.
function rpcArgumentCompletions(handle, position, facts) {
    const before = (a, b) => a.line < b.line || a.line === b.line && a.character <= b.character;
    const current = facts.arguments.filter(call => before(call.range.start, position) && before(position, call.range.end)).at(-1);
    const call = current && rpcCalls(handle, position).find(call =>
        call.position.line === current.position.line && call.position.character === current.position.character);
    const first = call?.values.find(value => value.index === 0);
    if (!first || before(position, first.end)) return;
    const path = handle.path();
    ensureRpcContracts([call]);
    const projected = rpcProjection(handles.get(path), position);
    if (!projected) return;
    return withTemporarySources(snapshot => {
        snapshot.replace(path, projected.text);
        const at = projected.position(position);
        return workspace.completions(handles.get(path), new ty.Position(at.line + 1, at.character + 1)).flatMap(item => {
            try {
                if (!item.name.endsWith('=') || call.keywords.includes(item.name.slice(0, -1))) return [];
                return [{ label: item.name, kind: item.kind === undefined ? undefined : item.kind + 1, detail: item.detail,
                    documentation: item.documentation, insertText: item.insert_text }];
            } finally { item.free(); }
        });
    });
}

function itemMetadata(uri) {
    selectEnvironment(uri);
    const handle = fileHandle(uri);
    const source = workspace.sourceText(handle);
    const facts = JSON.parse(itemFacts(source));
    const result = { eventHandlers: [], formClassBodyEndLine: null, httpEndpoints: [], routes: [], emailEndpoints: [] };
    const className = formClasses.get(pathForUri(uri));
    let form;
    if (className) {
        form = facts.classes.find(candidate => candidate.name === className && candidate.owner === null);
        if (form) {
            result.formClassName = form.name;
            if (form.bodyEnd) {
                result.formClassBodyEndLine = form.bodyEnd.line + 1;
                const lines = source.split(/\r\n|\r|\n/);
                for (let line = result.formClassBodyEndLine; line < lines.length; line++) {
                    if (!lines[line].trim()) continue;
                    if (!/^\s*#/.test(lines[line]) || lines[line].search(/\S/) < form.bodyStart.character) break;
                    result.formClassBodyEndLine = line + 1;
                }
            }
        }
    }
    for (const fn of facts.functions) {
        for (const decorator of fn.decorators) {
            const name = apiFunction(handle, decorator.position);
            if (name === 'handle' && form?.id === fn.owner && decorator.call) {
                const component = stringArgument(decorator, 'component_name', 0);
                const event = stringArgument(decorator, 'event_name', 1);
                if (component !== undefined && event !== undefined) result.eventHandlers.push({ component, event, handler: fn.name });
            } else if ((name === 'http_endpoint' || name === 'route') && decorator.call) {
                result[name === 'route' ? 'routes' : 'httpEndpoints'].push({ name: fn.name, path: stringArgument(decorator, 'path', 0) });
            } else if (name === 'handle_message') result.emailEndpoints.push({ name: fn.name });
        }
    }
    return result;
}

// Ty's browser API resolves source positions. A short typed Form expression lets
// metadata-only bindings and component names use the same resolution, even when
// they have no existing Python use site. Remove the analysis-only file in finally.
function formDefinitions(uri, expression, positions, className) {
    selectEnvironment(uri);
    const original = pathForUri(uri);
    const canonical = projections.get(original);
    if (!canonical) throw new Error('Form source is unavailable');
    const base = JSON.parse(preparedRootsJson)[0];
    const module = canonical.slice(base.length + 1).replace(/(?:\/__init__)?\.py$/, '').replaceAll('/', '.');
    let path;
    do { path = `${base}/_anvil_refactor_${++nextContextId}.py`; } while (handles.has(path));
    const document = projectContext({ kind: 'binding', code: expression }, uriForPath(path), 0,
        { module, name: className ?? formClasses.get(original) });
    const handle = workspace.openFile(path, document.text);
    try {
        return positions.map(position => {
            const projected = contextPosition(document, position);
            return locations(workspace.gotoDefinition(handle, new ty.Position(projected.line + 1, projected.character + 1)));
        });
    } finally { workspace.closeFile(handle); }
}

function renameContext() {
    const dependencyPrefix = `${root}/.anvil/deps/`;
    const selectedFiles = new Map([...files, ...overlays].filter(([path]) => {
        if (!path.startsWith(dependencyPrefix)) return true;
        const app = dependencyPrefix + path.slice(dependencyPrefix.length).split('/')[0];
        return Object.hasOwn(dependencyRoots, app);
    }));
    return {
        root, dependencyRoots, files: selectedFiles, forms: formCatalogue, configs: appConfigs,
        invalidForms: preparationDiagnostics.filter(item => item.code === 'invalid-form-template'),
        source: sourceText,
        definitions(uri, position) {
            selectEnvironment(uri);
            const handle = fileHandle(uri);
            return locations(workspace.gotoDefinition(handle, queryPosition(handle, position)));
        },
        rename(uri, position, newName) {
            selectEnvironment(uri);
            return acrossRuntimes(uri, position, (handle, position) =>
                renameEdits(workspace.rename(handle, new ty.Position(position.line + 1, position.character + 1), newName)));
        },
        references(uri, position) {
            selectEnvironment(uri);
            return acrossRuntimes(uri, position, (handle, position) =>
                locations(workspace.gotoReferences(handle, new ty.Position(position.line + 1, position.character + 1))));
        },
        member(uri, name, className) { return formDefinitions(uri, `self.${name}`, [{ line: 0, character: 5 }], className)[0]; },
        expressionDefinitions(uri, expression, positions) { return formDefinitions(uri, expression, positions); },
        api(uri, position) {
            selectEnvironment(uri);
            const handle = fileHandle(uri);
            return apiFunction(handle, sourceMaps.get(handle.path())?.position(position) ?? position);
        },
    };
}

// Record whole-module import inputs for derived Anvil types. Ty resolves imports,
// including aliases/re-exports and server overrides; no parallel Python resolver.
function sourceInputs(paths) {
    const inputs = new Set();
    const visited = new Set();
    const pending = [...paths];
    const packages = new Set(Object.values(appConfigs).map(config => config.package_name ?? 'main_app_package'));
    for (const path of pending) {
        const canonical = projections.get(path) ?? path;
        // Fixed library declarations cannot lead to mutable app inputs. Walking
        // their import graphs here adds work to every edited completion.
        if (packForPath(canonical)) continue;
        if (visited.has(canonical) || !handles.has(canonical)) continue;
        visited.add(canonical);
        const original = origins.get(canonical) ?? path;
        if (files.has(original) || overlays.has(original)) inputs.add(original);
        let imports = resolvedImports.get(canonical);
        if (!imports) {
            imports = { paths: [], unresolved: false };
            // Relative imports can follow a re-export past its package's __init__.
            // Its source is still an input even when definition skips that hop.
            for (let directory = canonical.slice(0, canonical.lastIndexOf('/')); directory.startsWith(root + '/'); directory = directory.slice(0, directory.lastIndexOf('/'))) {
                for (const extension of ['py', 'pyi']) {
                    const parent = `${directory}/__init__.${extension}`;
                    if (handles.has(parent)) imports.paths.push(parent);
                }
            }
            const handle = handles.get(canonical);
            for (const imported of importsFor(workspace.sourceText(handle))) {
                let resolved = false;
                for (const position of imported.positions) {
                    const targets = locations(workspace.gotoDefinition(handle, new ty.Position(position.line + 1, position.character + 1)));
                    resolved ||= targets.length > 0;
                    for (const target of targets) {
                        if (!target.uri.startsWith('file:')) continue;
                        const dependency = pathForUri(target.uri);
                        if (dependency.startsWith(root + '/')) imports.paths.push(dependency);
                    }
                }
                imports.unresolved ||= !resolved && (imported.relative && imported.module !== null || packages.has(imported.module?.split('.')[0]));
            }
            resolvedImports.set(canonical, imports);
        }
        // An unresolved project import can hide a producer. Keep that gradual
        // case conservative until a structural update makes it resolvable.
        if (imports.unresolved)
            return new Set([...files.keys(), ...overlays.keys()].filter(path => path.endsWith('.py')));
        pending.push(...imports.paths);
    }
    return inputs;
}

function importsFor(source) {
    let imports = parsedImports.get(source);
    if (!imports) parsedImports.set(source, (imports = JSON.parse(sourceImports(source))));
    return imports;
}

function sourceFacts(source) {
    let facts = parsedSources.get(source);
    if (!facts) parsedSources.set(source, (facts = JSON.parse(itemFacts(source))));
    return facts;
}

function pruneSourceFacts() {
    const active = new Set([...files.values(), ...overlays.values(), ...Object.values(preparedViews.get(isServer).prepared.files), ...mounted.values()]);
    for (const cache of [parsedSources, parsedImports])
        for (const source of cache.keys()) if (!active.has(source)) cache.delete(source);
}

function rpcUses(path) {
    const key = JSON.stringify([isServer, path]);
    let consumer = rpcConsumers.get(key);
    if (consumer) return consumer;
    const handle = fileHandle(uriForPath(path));
    const needed = new Set();
    let dynamic = false;
    const calls = JSON.parse(callFacts(workspace.sourceText(handle))).arguments;
    for (const call of calls) {
        const api = apiFunction(handle, call.position);
        const kind = ['call', 'call_s'].includes(api) ? 'callable' : api === 'launch_background_task' ? 'background_task' : undefined;
        if (!kind || !call.values.length) continue;
        const keyword = kind === 'background_task' ? 'task_name' : 'fn_name';
        const argument = call.values.find(value => value.index === 0 || value.keyword === keyword);
        if (!argument?.literal) dynamic = true;
        else needed.add(JSON.stringify([kind, argument.literal.value]));
    }
    consumer = { inputs: calls.length ? sourceInputs([path]) : new Set([path]), needed, dynamic };
    // Generated editing contexts change independently of project file updates.
    if (projections.has(path)) rpcConsumers.set(key, consumer);
    return consumer;
}

function assignmentsFor(path) {
    const source = overlays.get(path) ?? files.get(path);
    let entry = producerAssignments.get(path);
    if (entry?.source !== source) {
        entry = { source, assignments: JSON.parse(itemAssignments(source)) };
        producerAssignments.set(path, entry);
    }
    return entry.assignments;
}

// Literal names need only their own inferred return. Dynamic calls retain all
// overloads. Refactoring explicitly requests the complete project separately.
function neededRpcTypes(uri) {
    if (!uri.startsWith('file:')) return new Set();
    const needed = new Set();
    const collect = paths => {
        for (const path of new Set([...paths, ...sourceInputs(paths)])) {
            if (!handles.has(projections.get(path) ?? path)) continue;
            const consumer = rpcUses(path);
            if (consumer.dynamic) return false;
            for (const name of consumer.needed) needed.add(name);
        }
        return true;
    };
    if (!collect([pathForUri(uri)])) return;
    if (!formItems) {
        const producers = [...sourceEnvironments].filter(([path, server]) => !server && path.endsWith('.py') && assignmentsFor(path).length).map(([path]) => path);
        const environment = isServer;
        try {
            if (producers.length && isServer) prepareApp(false);
            if (!collect(producers)) return;
        } finally { if (isServer !== environment) prepareApp(environment); }
    }
    return needed;
}

function mountSource(original, source) {
    const path = projections.get(original);
    const plan = handlerPlans?.get(original);
    const projected = plan && projectAnnotations(source, plan.edits, plan.declarations);
    const text = projected?.text ?? source;
    if (projected) sourceMaps.set(path, projected); else sourceMaps.delete(path);
    const originalText = overlays.get(original) ?? files.get(original);
    if (text !== originalText) {
        const lines = originalText.split(/\r\n|\r|\n/);
        sourceEnds.set(path, { line: lines.length - 1, character: lines.at(-1).length });
    } else sourceEnds.delete(path);
    if (mounted.get(path) !== text) setFile(path, text);
    mounted.set(path, text);
}

function updateSources(before) {
    const current = new Map([...files, ...overlays]);
    const updates = [];
    for (const path of new Set([...before.keys(), ...current.keys()])) {
        if (before.get(path) === current.get(path)) continue;
        if (!sourceEnvironments.has(path) || !before.has(path) || !current.has(path) || !path.endsWith('.py')) return false;
        const rendered = sourceUpdate(JSON.stringify({ before: before.get(path), after: current.get(path),
            schema: appConfigs[root]?.db_schema ?? null, formClass: formClasses.get(path) ?? null }));
        if (!rendered) return false;
        const projected = JSON.parse(rendered);
        for (const { prepared } of preparedViews.values()) {
            for (const [canonical, original] of Object.entries(prepared.sources ?? {})) {
                if (original !== path) continue;
                const source = prepared.files[canonical];
                if (!source.startsWith(projected.before)) return false;
                // Preserve authoritative JS exports in either namespace.
                updates.push({ path, canonical, prepared, text: projected.after + source.slice(projected.before.length) });
            }
        }
    }
    // Validate every change before mutating either cached view or Ty's sources.
    for (const { path, canonical, prepared, text } of updates) {
        prepared.files[canonical] = text;
        if (projections.get(path) !== canonical) continue;
        mountSource(path, text);
    }
    return true;
}

function clearInference() {
    rpcConsumers.clear();
    registrationPlans.clear();
    remoteRegistrations = undefined;
    registrationInputs = undefined;
    remoteTypes = undefined;
    remoteInputs = undefined;
    formItems = undefined;
    formInputs = undefined;
    handlerPlans = undefined;
    handlerInputs.clear();
}

function invalidateSources(before) {
    const current = new Map([...files, ...overlays]);
    const changed = new Set([...before.keys(), ...current.keys()].filter(path => before.get(path) !== current.get(path)));
    if ([...changed].some(path => !path.endsWith('.py') || !before.has(path) || !current.has(path))) {
        clearInference();
        preparedViews.clear();
        producerAssignments.clear();
        return;
    }
    const affected = inputs => inputs && [...changed].some(path => inputs.has(path));
    for (const [key, consumer] of rpcConsumers) if (affected(consumer.inputs)) rpcConsumers.delete(key);
    for (const [path, plan] of registrationPlans) if (affected(plan.inputs)) registrationPlans.delete(path);
    if (affected(registrationInputs)) {
        remoteRegistrations = undefined;
        registrationInputs = undefined;
    }
    if (affected(remoteInputs)) {
        remoteTypes = undefined;
        remoteInputs = undefined;
        if (formInputs?.size) {
            formItems = undefined;
            formInputs = undefined;
        }
    }
    if (affected(formInputs) || [...changed].some(path => sourceEnvironments.get(path) === false && assignmentsFor(path).length)) {
        formItems = undefined;
        formInputs = undefined;
    }
    for (const [path, inputs] of handlerInputs) if (affected(inputs)) {
        handlerInputs.delete(path);
        handlerPlans?.delete(path);
    }
}

function request(method, params) {
    if (method === 'initialize') {
        preparation = new Preparation();
        root = pathForUri(params.rootUri).replace(/\/$/, '');
        resetWorkspace();
        for (const [path, text] of Object.entries(params.files)) {
            files.set(path, text);
        }
        prepareApp();
        return null;
    }
    if (updateMethods.includes(method)) {
        if (params.revision !== revision + 1) throw new Error('Out-of-order analysis update');
        // An in-order attempt consumes its revision, including a rejected edit.
        // Roll back the input batch and rebuild derived state before accepting
        // the next request; preparation can fail after changing mounted files.
        revision = params.revision;
        const previousEnvironment = isServer;
        const target = method === 'updateFiles' ? files
            : ['setContext', 'closeContext'].includes(method) ? contexts : overlays;
        const previous = new Map(target);
        const previousSources = new Map([...files, ...overlays]);
        const previousDeclarations = declarationFiles;
        const previousRemoteTypes = remoteTypes;
        const previousFormItems = formItems;
        try {
            if (method === 'updateFiles') {
                // Validate the full batch before mutating the workspace.
                for (const path of Object.keys(params.files)) originalPath(path);
                for (const [path, text] of Object.entries(params.files)) {
                    if (text === null) files.delete(path); else files.set(path, text);
                }
            } else if (method === 'setContext') {
                contexts.set(params.context.id, {
                    value: params.context,
                    server: params.context.kind === 'repl' && params.context.isServer,
                    serial: contexts.get(params.context.id)?.serial ?? ++nextContextId,
                    generation: ++nextContextGeneration,
                });
            } else if (method === 'closeContext') {
                contexts.delete(params.id);
            } else {
                const path = originalPath(pathForUri(params.uri));
                if (method === 'openDocument') {
                    overlays.set(path, params.text);
                } else {
                    overlays.delete(path);
                }
            }
            invalidateSources(previousSources);
            if (['setContext', 'closeContext'].includes(method)) prepareApp();
            else if (!updateSources(previousSources)) {
                preparedViews.clear();
                prepareApp();
            } else if (previousRemoteTypes !== remoteTypes || previousFormItems !== formItems) prepareApp();
            // Models and generated Designer declarations can change through Python
            // source too. Their changed exports invalidate every inferred layer.
            if ([...new Set([...previousDeclarations.keys(), ...declarationFiles.keys()])]
                .some(path => previousDeclarations.get(path) !== declarationFiles.get(path))) {
                clearInference();
                prepareApp();
            }
            pruneSourceFacts();
        } catch (error) {
            target.clear();
            for (const [key, value] of previous) target.set(key, value);
            clearInference();
            preparedViews.clear();
            producerAssignments.clear();
            resetWorkspace();
            prepareApp(previousEnvironment);
            throw error;
        }
        return null;
    }
    if (method === 'queryContext') {
        const context = contexts.get(params.id);
        if (!context) throw new Error(`Analysis context is not open: ${params.id}`);
        if (context.server !== isServer) prepareApp(context.server);
        const document = context.document;
        if (!document) throw new Error('Binding Form is unavailable');
        if (params.method === 'completionItem/resolve') {
            const original = originalCompletion(params.params, params.id, document);
            return contextCompletion(request(params.method, original), params.id, document);
        }
        if (!['textDocument/completion', 'textDocument/signatureHelp'].includes(params.method))
            throw new Error(`Unsupported context request: ${params.method}`);
        const result = request(params.method, { ...params.params, textDocument: { uri: document.uri },
            position: contextPosition(document, params.params.position) });
        return params.method === 'textDocument/completion' && result
            ? { ...result, items: result.items.flatMap(item => contextCompletion(item, params.id, document) ?? []) } : result;
    }
    if (method === 'anvil/readSource') {
        // Generated declarations must match the same inferred snapshot used by queries.
        ensureRemoteTypes();
        ensureFormItems();
        ensureHandlerTypes();
        selectEnvironment(params.uri);
        const handle = fileHandle(params.uri);
        if (params.uri.startsWith('file:')) {
            const path = pathForUri(params.uri);
            const source = overlays.get(path) ?? files.get(path);
            if (source !== undefined) return { uri: params.uri, text: source, readOnly: true };
        }
        return { uri: params.uri, text: workspace.sourceText(handle), readOnly: true };
    }
    if (method === 'completionItem/resolve') return completionDocumentation(params);
    if (method === 'anvil/getItemMetadata') return itemMetadata(params.uri);
    if (method === 'anvil/getAppMetadata') return params.uris.map(uri => ({ uri, ...itemMetadata(uri) }));
    if (method === 'anvil/getBackgroundTasks') return registrations().tasks;
    if (method === 'anvil/renameResource') return renameResource(params, renameContext());
    if (method === 'anvil/renameComponent') return renameComponent(params, renameContext());
    if (method === 'workspace/symbol') {
        const current = new Map([...files, ...overlays]);
        return [...current].filter(([path]) => sourceEnvironments.size ? sourceEnvironments.has(path) : /\.pyi?$/.test(path))
            .flatMap(([path, text]) => sourceSymbols(uriForPath(path), text))
            .filter(symbol => symbol.name.toLowerCase().includes(params.query.toLowerCase()));
    }
    // Form items commonly come from server calls; infer them only after the
    // current revision's RPC result declarations are available to ty.
    selectEnvironment(params.textDocument.uri);
    const completeProject = ['textDocument/references', 'textDocument/rename'].includes(method);
    // A returned client class may itself call another RPC. Follow newly exposed
    // imports until no additional return declarations are needed for this query.
    for (;;) {
        const count = remoteTypes?.length ?? 0;
        ensureRemoteTypes(completeProject ? undefined : neededRpcTypes(params.textDocument.uri));
        if (completeProject || remoteTypes.length === count) break;
    }
    ensureFormItems();
    ensureHandlerTypes(completeProject ? undefined : (params.textDocument.uri.startsWith('file:') ? sourceInputs([pathForUri(params.textDocument.uri)]) : new Set()));
    selectEnvironment(params.textDocument.uri);
    const handle = fileHandle(params.textDocument.uri);
    const path = handle.path();
    if (method === 'textDocument/typeDefinition') {
        return locations(workspace.gotoTypeDefinition(handle, queryPosition(handle, params.position)));
    }
    if (method === 'textDocument/inlayHint') {
        const hints = workspace.inlayHints(handle, new ty.Range(queryPosition(handle, params.range.start), queryPosition(handle, params.range.end)));
        return hints.flatMap(hint => {
            try {
                const point = hint.position;
                let selected;
                try {
                    const position = { line: point.line - 1, character: point.column - 1 };
                    selected = mappedRange(path, { start: position, end: position });
                } finally { point.free(); }
                const label = hint.label.map(part => {
                    try { return part.label; } finally { part.free(); }
                }).join('');
                // Hints are informational. Inserting an annotation or a named
                // argument is a separate edit action, never a display side effect.
                for (const edit of hint.text_edits) edit.free();
                return selected && originalRange(path, selected)
                    ? [{ position: selected.start, label, kind: hint.kind + 1, paddingLeft: true, paddingRight: true }] : [];
            } finally { hint.free(); }
        });
    }
    if (method === 'textDocument/codeAction') {
        if (readOnly(params.textDocument.uri)) return [];
        const before = (a, b) => a.line < b.line || a.line === b.line && a.character <= b.character;
        return workspace.checkFile(handle).flatMap(diagnostic => {
            try {
                const native = diagnostic.toRange(workspace);
                const selected = native && mappedRange(path, range(native));
                if (!selected || !originalRange(path, selected) ||
                    !before(selected.start, params.range.end) || !before(params.range.start, selected.end)) return [];
                const requested = params.context?.diagnostics;
                if (requested?.length && !requested.some(item => item.code === String(diagnostic.id()) &&
                    JSON.stringify(item.range) === JSON.stringify(selected))) return [];
                return (workspace.codeActions(handle, diagnostic) ?? []).flatMap(action => {
                    try {
                        const edits = action.edits.map(edit => {
                            try { return { range: mappedRange(path, range(edit.range)), newText: edit.new_text }; }
                            finally { edit.free(); }
                        });
                        if (edits.some(edit => !edit.range || !originalRange(path, edit.range))) return [];
                        return [{ title: action.title, kind: 'quickfix', isPreferred: action.preferred,
                            diagnostics: [{ range: selected, code: String(diagnostic.id()) }],
                            edit: { changes: { [params.textDocument.uri]: edits } } }];
                    } finally { action.free(); }
                });
            } finally { diagnostic.free(); }
        });
    }
    if (method === 'textDocument/hover') {
        const hover = workspace.hover(handle, queryPosition(handle, params.position));
        if (!hover) return null;
        try { return { contents: { kind: 'markdown', value: hover.markdown }, range: mappedRange(path, range(hover.range)) }; }
        finally { hover.free(); }
    }
    if (method === 'textDocument/documentSymbol') return sourceSymbols(params.textDocument.uri, sourceText(params.textDocument.uri));
    if (method === 'textDocument/diagnostic') {
        ensureRpcContracts(rpcCalls(handle));
        const projected = rpcProjection(fileHandle(params.textDocument.uri));
        const items = withTemporarySources(snapshot => {
            if (projected) snapshot.replace(path, projected.text);
            return workspace.checkFile(handles.get(path)).map(diagnostic => {
                try {
                    const location = diagnostic.toRange(workspace);
                    const rpcRange = location && (projected ? projected.range(range(location)) : range(location));
                    const selected = rpcRange ? mappedRange(path, rpcRange) : null;
                    if (location && !rpcRange) return null;
                    const generated = selected && !originalRange(path, selected);
                    const result = { range: selected && !generated ? selected : { start: { line: 0, character: 0 }, end: { line: 0, character: 0 } },
                        message: String(diagnostic.message()), code: String(diagnostic.id()), source: 'ty',
                        severity: diagnostic.severity() >= ty.Severity.Error ? 1 : diagnostic.severity() === ty.Severity.Warning ? 2 : 3 };
                    if (generated) result.relatedInformation = [{
                        location: { uri: uriForPath(path, selected), range: selected },
                        message: 'In generated JavaScript component exports',
                    }];
                    return result;
                } finally { diagnostic.free(); }
            }).filter(Boolean);
        });
        if (isServer && !Object.keys(configuration.options.rules ?? {}).some(rule => ['all', 'unresolved-import'].includes(rule))) {
            const appPackages = new Set(['anvil', ...Object.values(appConfigs).map(config => config.package_name ?? 'main_app_package')]);
            const imports = importsFor(sourceText(params.textDocument.uri));
            for (const item of items) {
                if (item.code !== 'unresolved-import') continue;
                const imported = imports.find(imported => imported.positions.some(position =>
                    position.line === item.range.start.line && position.character === item.range.start.character));
                if (!imported?.module || imported.relative || imported.stdlib || appPackages.has(imported.module.split('.')[0])) continue;
                item.severity = 3;
                item.message = `Type information for server module '${imported.module}' is unavailable in the IDE. Check that it is installed in your server environment; its types will remain unknown here.`;
            }
        }
        if (!isServer && sourceEnvironments.size && path.endsWith('.py')) {
            const target = fileHandle(params.textDocument.uri);
            for (const imported of JSON.parse(clientImportFacts(workspace.sourceText(target))).imports) {
                if (imported.resolve) {
                    // Definition follows re-exports (collections.abc points at an
                    // alias). Native import completion kinds distinguish modules
                    // from ordinary exported functions/classes without parsing type displays.
                    const candidates = workspace.completions(target,
                        new ty.Position(imported.range.end.line + 1, imported.range.end.character + 1));
                    let module = false;
                    for (const item of candidates) {
                        try {
                            if (item.kind === ty.CompletionKind.Module && item.name === imported.name.split('.').at(-1)) {
                                const edits = item.additional_text_edits ?? [];
                                module ||= !edits.length;
                                for (const edit of edits) edit.free();
                            }
                        }
                        finally { item.free(); }
                    }
                    if (!module) continue;
                }
                const selected = mappedRange(path, imported.range);
                if (selected && originalRange(path, selected)) items.push({ range: selected, severity: 1,
                    code: 'reportAnvilUnsupportedSkulptImport', source: 'anvil',
                    message: `Module '${imported.name}' is not available in Skulpt. Move this code to a server module or use a supported alternative.` });
            }
        }
        for (const diagnostic of preparationDiagnostics) {
            if (uriForPath(diagnostic.file) === params.textDocument.uri) {
                items.push({ range: { start: { line: 0, character: 0 }, end: { line: 0, character: 0 } },
                    message: diagnostic.message, code: diagnostic.code, severity: 1, source: 'anvil' });
            }
        }
        for (const message of configuration.diagnostics)
            items.push({ range: { start: { line: 0, character: 0 }, end: { line: 0, character: 0 } },
                message, code: 'anvil-invalid-ty-config', severity: 2, source: 'anvil' });
        return { kind: 'full', items };
    }
    if (method === 'textDocument/signatureHelp') {
        const at = sourceMaps.get(path)?.position(params.position) ?? params.position;
        ensureRpcContracts(rpcCalls(handle, at).slice(-1));
        const projected = rpcProjection(fileHandle(params.textDocument.uri), at);
        return withTemporarySources(snapshot => {
            if (projected) snapshot.replace(path, projected.text);
            const point = projected?.position(at) ?? at;
            const help = workspace.signatureHelp(handles.get(path), new ty.Position(point.line + 1, point.character + 1));
            if (!help) return null;
            try {
                return { activeSignature: help.active_signature,
                    signatures: help.signatures.map(signature => {
                        try {
                            return { label: signature.label, documentation: signature.documentation, activeParameter: signature.active_parameter,
                                parameters: signature.parameters.map(parameter => {
                                    try { return { label: parameter.label, documentation: parameter.documentation }; }
                                    finally { parameter.free(); }
                                }) };
                        } finally { signature.free(); }
                    }) };
            } finally { help.free(); }
        });
    }
    if (method === 'textDocument/references') {
        return referenceLocations(params.textDocument.uri, params.position, params.context);
    }
    if (method === 'textDocument/prepareRename' || method === 'textDocument/rename') {
        if (readOnly(params.textDocument.uri)) throw new Error('Cannot rename a read-only source');
        const context = renameContext();
        const remote = rpcTarget(params.textDocument.uri, params.position, context);
        if (remote) return method === 'textDocument/prepareRename' ? { range: remote.selected, placeholder: remote.name } : renameRpc(remote, params.newName, context);
        const component = componentAt(params.textDocument.uri, params.position, context);
        if (component && method === 'textDocument/rename') return renameComponent({ ...component, newName: params.newName }, context);
        if (method === 'textDocument/prepareRename') {
            selectEnvironment(params.textDocument.uri);
            const prepared = workspace.prepareRename(fileHandle(params.textDocument.uri), queryPosition(fileHandle(params.textDocument.uri), params.position));
            const selected = prepared && mappedRange(fileHandle(params.textDocument.uri).path(), range(prepared));
            if (!selected || (component && readOnly(component.formUri))) return null;
            if (!component && context.definitions(params.textDocument.uri, selected.start).some(target => readOnly(target.uri))) {
                // Ty includes generated stubs in its project. Inspect edits only for
                // readonly targets: an explicit local import alias can still be renamed.
                const oldName = selectedName({ uri: params.textDocument.uri, range: selected });
                const edits = context.rename(params.textDocument.uri, selected.start, oldName);
                if (!edits.length || edits.some(edit => readOnly(edit.uri))) return null;
            }
            return { range: selected };
        }
        if (!isPythonIdentifier(params.newName)) throw new Error('Rename requires a valid Python identifier');
        const edits = acrossRuntimes(params.textDocument.uri, params.position, (handle, position) =>
            renameEdits(workspace.rename(handle, new ty.Position(position.line + 1, position.character + 1), params.newName)));
        if (edits.some(edit => readOnly(edit.uri))) throw new Error('Rename requires a read-only source edit');
        const documents = new Map();
        for (const { uri, ...edit } of edits) {
            if (!documents.has(uri)) documents.set(uri, []);
            documents.get(uri).push(edit);
        }
        return extendAnvilRename({ documentChanges: [...documents].map(([uri, edits]) => ({ textDocument: { uri, version: null }, edits })) }, params.textDocument.uri, params.position, params.newName, context);
    }
    if (method === 'textDocument/definition') {
        const remote = rpcTargets(params.textDocument.uri, params.position, renameContext());
        if (remote) return remote.map(({ uri, range }) => ({ uri, range }));
        selectEnvironment(params.textDocument.uri);
        const target = fileHandle(params.textDocument.uri);
        return locations(workspace.gotoDefinition(target, queryPosition(target, params.position)));
    }
    if (method === 'textDocument/completion') {
        const position = sourceMaps.get(path)?.position(params.position) ?? params.position;
        const mapItem = item => {
            if (!item.textEdit) return item;
            const selected = mappedRange(path, item.textEdit.range);
            return selected ? { ...item, textEdit: { ...item.textEdit, range: selected } } : undefined;
        };
        const calls = JSON.parse(callFacts(workspace.sourceText(handle)));
        const names = propertyValueCompletions(handle, position, calls.assignments) ??
            formHandleCompletions(params.textDocument.uri, handle, position, calls.arguments) ??
            namedArgumentCompletions(handle, position, calls.arguments);
        if (names && !names.includePython) return { isIncomplete: false, items: names.items.flatMap(item => mapItem(item) ?? []) };
        const constructor = names ? undefined : formConstructorCompletions(handle, position, calls);
        let completionHandle = fileHandle(params.textDocument.uri);
        const keys = names ? undefined : rowKeyCompletions(completionHandle, position);
        if (keys) return { isIncomplete: false, items: keys.flatMap(item => mapItem(item) ?? []) };
        const rpcArguments = names ? undefined : rpcArgumentCompletions(fileHandle(params.textDocument.uri), position, calls);
        completionHandle = fileHandle(params.textDocument.uri);
        // Completion has no declaration origin. This exact name/type pair
        // identifies an analysis-only declaration, locally or through another module,
        // while preserving an ordinary user symbol with the same name.
        const generatedBindings = new Set([...handlerPlans.values()].filter(plan => plan.generatedName)
            .map(plan => JSON.stringify([plan.generatedName, plan.generatedType])));
        const native = workspace.completions(completionHandle, queryPosition(completionHandle, params.position));
        const completionSource = workspace.sourceText(completionHandle);
        const beforeCursor = completionSource.split('\n')[position.line].slice(0, position.character);
        const fromImport = JSON.parse(clientImportFacts(completionSource)).fromImports.findLast(imported =>
            (imported.moduleEnd.line < position.line || imported.moduleEnd.line === position.line && imported.moduleEnd.character < position.character) &&
            (position.line < imported.range.end.line || position.line === imported.range.end.line &&
                (position.character <= imported.range.end.character || !beforeCursor.slice(imported.range.end.character).trim())));
        const prefix = beforeCursor.match(/[\p{ID_Continue}]+$/u)?.[0] ?? '';
        const absoluteImport = beforeCursor.match(/^\s*(?:from\s+|import\s+(?:[\w.]+(?:\s+as\s+\w+)?\s*,\s*)*)(?!\.)([\w.]*)$/);
        const modulePrefix = fromImport?.module ?? absoluteImport?.[1].split('.').slice(0, -1).join('.');
        const hideDeletion = native.some(item => item.name === 'delete_all_rows') && hiddenTableDeletion(completionHandle, position);
        const documentation = /\.[\p{ID_Continue}_]*$/u.test(beforeCursor)
            ? { uri: params.textDocument.uri, position: params.position, revision } : undefined;
        const items = native.flatMap(item => {
                try {
                    let module = item.module_name;
                    if (!module && item.kind === ty.CompletionKind.Module && (fromImport || absoluteImport))
                        module = modulePrefix ? `${modulePrefix}.${item.name}` : item.name;
                    if (!isServer && sourceEnvironments.size && module && !skulptModuleSupported(module)) return [];
                    if (generatedBindings.has(JSON.stringify([item.name, item.detail])) || constructor && item.name === 'form=' ||
                        hideDeletion && item.name === 'delete_all_rows') return [];
                    if (item.name.endsWith('=') && !isPythonIdentifier(item.name.slice(0, -1))) return [];
                    const additionalTextEdits = item.additional_text_edits?.map(edit => {
                        try { return { range: mappedRange(path, range(edit.range)), newText: edit.new_text }; }
                        finally { edit.free(); }
                    });
                    if (additionalTextEdits?.some(edit => !edit.range || !originalRange(path, edit.range))) return [];
                    return [{ label: item.name, kind: item.kind === undefined ? undefined : item.kind + 1,
                        detail: item.detail, documentation: item.documentation, insertText: item.insert_text, additionalTextEdits,
                        data: documentation ? { documentation } : undefined }];
                } finally { item.free(); }
            });
        if (items.some(item => [2, 3, 4, 7].includes(item.kind)) && callableArgument(completionHandle, position, calls.arguments))
            for (const item of items)
                if ([2, 3, 4, 7].includes(item.kind)) item.data = { ...item.data, insertParentheses: false };
        // Promote matching names already in scope. Keep Ty's order for keywords,
        // auto-imports and fuzzy matches rather than burying useful keywords.
        const inScope = item => item.kind !== 14 && !item.additionalTextEdits?.length && item.label.startsWith(prefix);
        // Resolve only receivers with a candidate covered by the shared legacy
        // preferences. Aliases work; similarly named app types retain Ty's order.
        let preference;
        if (beforeCursor.endsWith('.' + prefix) && position.character > prefix.length + 1 &&
            items.some(item => preferredMembers.has(item.label))) {
            const targets = locations(workspace.gotoTypeDefinition(completionHandle,
                new ty.Position(position.line + 1, position.character - prefix.length - 1)));
            const apiRoot = `${root}/.anvil/types/${isServer ? 'server' : 'client'}/anvil/`;
            for (const target of targets) {
                if (!target.uri.startsWith(uriForPath(apiRoot))) continue;
                const module = 'anvil.' + pathForUri(target.uri).slice(apiRoot.length).replace(/(?:\/__init__)?\.pyi$/, '').replaceAll('/', '.');
                const owner = module === 'anvil.__init__' ? 'anvil' : module;
                const name = selectedName(target);
                preference = completionPreferences[name ? `${owner}.${name}` : owner];
                if (preference) break;
            }
        }
        items.sort((a, b) => {
            const scopeOrder = Number(inScope(b)) - Number(inScope(a));
            if (scopeOrder || !inScope(a)) return scopeOrder;
            return Number(b.label === preference?.suggestedAttr) - Number(a.label === preference?.suggestedAttr) ||
                (preference?.priority?.[b.label] ?? 0) - (preference?.priority?.[a.label] ?? 0);
        });
        // LSP consumers otherwise reorder the merged results by label.
        const imports = importCompletions(fileHandle(params.textDocument.uri), position);
        const columns = names ? [] : queryColumnCompletions(fileHandle(params.textDocument.uri), position, calls.arguments);
        const decorators = decoratorCompletions(fileHandle(params.textDocument.uri), position, { imports: calls.imports, items });
        return { isIncomplete: false, items: [...decorators, ...imports, ...(names?.items ?? []), ...(constructor ?? []), ...(rpcArguments ?? []), ...columns].flatMap(item => mapItem(item) ?? []).concat(items).map((item, index) =>
            ({ ...item, sortText: String(index).padStart(8, '0') })) };
    }
    throw new Error(`Unsupported ty browser request: ${method}`);
}
