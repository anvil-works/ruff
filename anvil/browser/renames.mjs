import { visitForm, components } from './forms.mjs';
import { renameNames, validRenameName, symbols, itemFacts, apiCalls } from './dist/compat/anvil_ty_compat.js';

const rangeKey = range => `${range.start.line}:${range.start.character}:${range.end.line}:${range.end.character}`;

// Unknown metadata may contain a reference to the renamed resource/member.
// Read-only analysis can use fallbacks; a complete rename cannot omit it.
function requireFormMetadata(context) {
    if (context.invalidForms.length)
        throw new Error(`Cannot safely rename with invalid Form metadata: ${context.invalidForms.map(item => item.file).join(', ')}`);
}

function appendEdit(edit, uri, range, newText) {
    let document = edit.documentChanges.find(change => change.textDocument.uri === uri);
    if (!document) edit.documentChanges.push(document = { textDocument: { uri, version: null }, edits: [] });
    const existing = document.edits.find(item => rangeKey(item.range) === rangeKey(range));
    if (existing && existing.newText !== newText) throw new Error('Rename contains conflicting edits');
    if (!existing) document.edits.push({ range, newText });
}

function editableReferences(edit, targets, newName, context) {
    for (const target of targets) {
        if (target.uri.startsWith(new URL(`${context.root}/.anvil/`, 'file:///').href) &&
            !context.files.has(decodeURIComponent(new URL(target.uri).pathname))) continue;
        if (!context.files.has(decodeURIComponent(new URL(target.uri).pathname)) || target.uri.endsWith('.pyi') ||
            target.uri.includes('/.anvil/deps/')) throw new Error('Rename requires a read-only source edit');
        appendEdit(edit, target.uri, target.range, target.newText ?? newName);
    }
}

function appendHandlerMetadata(edit, declaration, oldName, newName, forms, context) {
    for (const form of forms) {
        let used = false;
        visitForm(form.data, node => {
            if ([...Object.values(node.event_bindings ?? {}), ...Object.values(node.form_event_bindings ?? {})].includes(oldName)) used = true;
        });
        if (!used || !context.member(form.uri, oldName).some(target => sameLocation(target, declaration))) continue;
        if (form.uri.includes('/.anvil/')) throw new Error('Rename requires a read-only Form metadata edit');
        if (context.member(form.uri, newName).length) throw new Error(`Form member already exists: ${newName}`);
        const renames = edit.eventHandlerRenames ??= [];
        if (!renames.some(rename => rename.formUri === form.uri && rename.oldName === oldName))
            renames.push({ formUri: form.uri, oldName, newName });
    }
}

// Anonymous components have no Python member. Resolve the declaring Form through
// class bases, stopping at a Form which supplies that stored component identity.
function anonymousOwners(uri, className, componentName, forms, context, seen = new Set()) {
    const key = uri + ':' + className;
    if (seen.has(key)) return [];
    seen.add(key);
    const form = forms.find(form => form.uri === uri && className === form.name.split('.').at(-1));
    if (form && components(form.data).some(component => component.name === componentName)) return [form.uri];
    const source = context.files.get(decodeURIComponent(new URL(uri).pathname));
    if (!source) return [];
    const cls = JSON.parse(itemFacts(source)).classes.find(cls => cls.name === className);
    return (cls?.bases ?? []).flatMap(position => context.definitions(uri, position).flatMap(target => {
        const source = context.files.get(decodeURIComponent(new URL(target.uri).pathname));
        const base = source && JSON.parse(itemFacts(source)).classes.find(cls => rangeKey(cls.range) === rangeKey(target.range));
        return base ? anonymousOwners(target.uri, base.name, componentName, forms, context, seen) : [];
    }));
}

export function renameComponent({ formUri, componentName, newName }, context) {
    requireFormMetadata(context);
    if (!validRenameName(newName)) throw new Error('Component name must be a valid Python identifier');
    const forms = context.forms;
    const form = forms.find(form => form.uri === formUri);
    if (!form || formUri.includes('/.anvil/')) throw new Error('Rename requires an editable Form');
    const children = components(form.data);
    const component = children.find(child => child.name === componentName);
    if (!component) throw new Error('Component no longer exists');
    if (children.some(child => child.name === newName) || context.member(formUri, newName).length)
        throw new Error(`Form member already exists: ${newName}`);
    const target = componentName.startsWith('$') ? undefined : context.member(formUri, componentName)[0];
    if (!target && !componentName.startsWith('$')) throw new Error('Cannot resolve the generated component member');
    const edit = { documentChanges: [], componentRenames: [{ formUri, oldName: componentName, newName, eventHandlers: {} }] };
    const handlers = edit.componentRenames[0].eventHandlers;
    if (target) {
        const references = context.references(target.uri, target.range.start);
        for (const reference of references) {
            if (!context.files.has(decodeURIComponent(new URL(reference.uri).pathname))) continue;
            if (context.definitions(reference.uri, reference.range.start).some(definition => !sameLocation(definition, target)))
                throw new Error('Cannot safely rename an ambiguous component reference');
        }
        editableReferences(edit, references, newName, context);
    }
    const renameHandler = (uri, oldName, replacement, className) => {
        const declaration = context.member(uri, oldName, className)[0];
        if (!declaration) throw new Error(`Cannot find Python event handler: ${oldName}`);
        if (context.member(uri, replacement, className).length) throw new Error(`Form member already exists: ${replacement}`);
        editableReferences(edit, context.rename(declaration.uri, declaration.range.start, replacement), replacement, context);
        handlers[oldName] = replacement;
        appendHandlerMetadata(edit, declaration, oldName, replacement, forms, context);
    };
    for (const [event, handler] of Object.entries(component.event_bindings ?? {}))
        if (handler === `${componentName}_${event}`) renameHandler(formUri, handler, `${newName}_${event}`);
    for (const [path, source] of context.files) {
        if (!path.endsWith('.py')) continue;
        const owner = { uri: new URL(path, 'file:///').href };
        const calls = JSON.parse(apiCalls(source));
        const facts = JSON.parse(itemFacts(source));
        for (const fn of facts.functions) {
            const decorators = fn.decorators.filter(decorator => (decorator.keywords.component_name ?? decorator.args[0]) === componentName && context.api(owner.uri, decorator.position) === 'handle');
            if (!decorators.length) continue;
            const ownerClass = facts.classes.find(cls => cls.id === fn.owner);
            if (!ownerClass) continue;
            const members = componentName.startsWith('$') ? [] : context.member(owner.uri, componentName, ownerClass.name);
            const owners = target ? [] : [...new Set(anonymousOwners(owner.uri, ownerClass.name, componentName, forms, context))];
            const owns = target ? members.some(member => sameLocation(member, target)) : owners.length === 1 && owners[0] === formUri;
            if (!target && owners.length > 1 && owners.includes(formUri)) throw new Error('Cannot safely rename an ambiguous anonymous component');
            if (!owns) continue;
            for (const decorator of decorators) {
                const call = calls.find(call => call.position.line === decorator.position.line && call.position.character === decorator.position.character);
                if (!call || call.value !== componentName) throw new Error('Cannot safely rename the component decorator');
                editableReferences(edit, [{ uri: owner.uri, range: call.literalRange }], JSON.stringify(newName), context);
                const event = decorator.keywords.event_name ?? decorator.args[1];
                if (fn.name === `${componentName}_${event}`)
                    renameHandler(owner.uri, fn.name, `${newName}_${event}`, ownerClass.name);
            }
        }
    }
    for (const owner of forms) {
        const bindings = [];
        visitForm(owner.data, (node, _path, componentName) => {
            for (const [index, binding] of (node.data_bindings ?? []).entries()) {
                const expression = Array.isArray(binding) ? binding[1] : binding.code;
                const names = JSON.parse(renameNames(expression)).filter(name => name.name === edit.componentRenames[0].oldName);
                const definitions = context.expressionDefinitions(owner.uri, expression, names.map(name => name.range.start));
                if (target && definitions.some(targets => targets.some(definition => sameLocation(definition, target)) && targets.some(definition => !sameLocation(definition, target))))
                    throw new Error('Cannot safely rename an ambiguous component binding');
                const edits = names.filter((_name, i) => target && definitions[i].some(definition => definition.uri === target.uri && rangeKey(definition.range) === rangeKey(target.range)))
                    .map(name => ({ range: name.range, newText: newName }));
                if (edits.length) bindings.push({ formUri: owner.uri, componentName, index,
                    property: Array.isArray(binding) ? binding[0] : binding.property, expression, edits });
            }
        });
        if (bindings.length) {
            if (owner.uri.includes('/.anvil/')) throw new Error('Rename requires a read-only binding edit');
            (edit.bindingEdits ??= []).push(...bindings);
        }
    }
    return edit;
}

function extendFormResources(edit, context, sourceUris) {
    const { root, files, rename, api } = context;
    const forms = context.forms;
    const renamed = forms.flatMap(form => {
        const resource = edit.resourceRenames.find(resource => resource.uri === form.uri);
        return resource ? [{ ...form, resource }] : [];
    });
    const configuration = context.configs[root];
    const names = new Map(edit.resourceRenames.filter(resource => resource.uri.startsWith(new URL(`${root}/client_code/`, 'file:///').href))
        .map(resource => [resource.oldName, resource.newName]));
    for (const path of [['startup_form'], ['startup', 'module']]) {
        const before = path.reduce((value, key) => value?.[key], configuration);
        if (names.has(before)) (edit.configEdits ??= []).push({
            uri: new URL(`${root}/anvil.yaml`, 'file:///').href, path, before, after: names.get(before),
        });
    }
    const originalEdit = (target, newName) => {
        if (target.uri.startsWith(new URL(`${root}/.anvil/`, 'file:///').href)) return;
        if (!sourceUris.includes(target.uri)) throw new Error('Rename requires a read-only source edit');
        appendEdit(edit, target.uri, target.range, newName);
    };
    for (const form of renamed) {
        const path = decodeURIComponent(new URL(form.uri).pathname);
        const source = files.get(path);
        const oldClass = form.resource.oldName.split('.').at(-1);
        const newClass = form.resource.newName.split('.').at(-1);
        if (oldClass === newClass) continue;
        const declaration = JSON.parse(symbols(source)).find(symbol => symbol.kind === 5 && !symbol.containerName && symbol.name === oldClass);
        if (!declaration) throw new Error(`Cannot find Form class: ${oldClass}`);
        const occupied = JSON.parse(symbols(source)).some(symbol => !symbol.containerName && [newClass, newClass + 'Template'].includes(symbol.name)) ||
            JSON.parse(renameNames(source)).some(name => (name.imported || name.alias) && [newClass, newClass + 'Template'].includes(name.name));
        if (occupied) throw new Error(`Form class already exists: ${newClass}`);
        for (const target of rename(form.uri, declaration.range.start, newClass)) originalEdit(target, target.newText);
        // ty preserves explicit aliases. Its browser rename currently omits the
        // imported name of an explicit re-export, so resolve that token directly.
        for (const [file, text] of files) {
            if (!file.endsWith('.py')) continue;
            const uri = new URL(file, 'file:///').href;
            for (const name of JSON.parse(renameNames(text)).filter(name => name.imported && name.name === oldClass))
                if (context.definitions(uri, name.range.start).some(target => target.uri === form.uri && rangeKey(target.range) === rangeKey(declaration.range)))
                    originalEdit({ uri, range: name.range }, newClass);
        }
        const template = JSON.parse(renameNames(source)).find(name => name.name === oldClass + 'Template');
        if (!template) throw new Error('Cannot find the Form template class');
        for (const target of rename(form.uri, template.range.start, newClass + 'Template')) originalEdit(target, target.newText);
        if (typeof form.data.class_name === 'string') (edit.formEdits ??= []).push({
            formUri: form.uri, componentName: null, path: ['class_name'], before: form.data.class_name,
            after: form.resource.newName,
        });
    }
    const formNames = new Map(renamed.map(form => [form.resource.oldName, form.resource.newName]));
    const rewrite = (value, local) => {
        if (typeof value !== 'string') return;
        if (local && formNames.has(value)) return formNames.get(value);
        const prefix = configuration.package_name + '.';
        if (value.startsWith(prefix) && formNames.has(value.slice(prefix.length))) return prefix + formNames.get(value.slice(prefix.length));
    };
    const propertyNames = new Map([['RepeatingPanel', ['item_template']]]);
    for (const form of forms) {
        const declarations = (form.data.properties ?? []).filter(property => property.type === 'form').map(property => property.name);
        propertyNames.set(`${form.config.package_name}.${form.name}`, declarations);
        propertyNames.set(`${form.root}/form:${form.name}`, declarations);
        for (const [owner, ids] of Object.entries(context.dependencyRoots))
            for (const [id, target] of Object.entries(ids))
                if (target === form.root) propertyNames.set(`${owner}/form:${id}:${form.name}`, declarations);
    }
    for (const form of forms) {
        const field = (componentName, path, before, after) => {
            if (!after || after === before) return;
            if (!sourceUris.includes(form.uri)) throw new Error('Rename requires a read-only Form metadata edit');
            (edit.formEdits ??= []).push({ formUri: form.uri, componentName, path, before, after });
        };
        const local = form.uri.startsWith(new URL(`${root}/client_code/`, 'file:///').href);
        visitForm(form.data, (node, path, componentName) => {
            const type = node.type;
            const after = typeof type === 'string' && type.startsWith('form:')
                ? (local && formNames.has(type.slice(5)) ? 'form:' + formNames.get(type.slice(5)) : undefined)
                : rewrite(type, false);
            field(componentName, [...path, 'type'], type, after);
            for (const property of propertyNames.get(type) ?? propertyNames.get(`${form.root}/${type}`) ?? []) {
                const value = node.properties?.[property];
                field(componentName, [...path, 'properties', property], value, rewrite(value, local));
            }
        });
        for (const [index, property] of (form.data.properties ?? []).entries())
            if (property.type === 'form') field(null, ['properties', index, 'default_value'], property.default_value, rewrite(property.default_value, local));
    }
    for (const [path, source] of files) {
        if (!path.endsWith('.py')) continue;
        const uri = new URL(path, 'file:///').href;
        for (const call of JSON.parse(apiCalls(source))) {
            const after = rewrite(call.value, path.startsWith(`${root}/client_code/`));
            if (after && api(uri, call.position) === 'open_form') {
                if (!sourceUris.includes(uri)) throw new Error('Rename requires a read-only source edit');
                appendEdit(edit, uri, call.literalRange, JSON.stringify(after));
            }
        }
    }
}

/** Plan against original app sources. Only the IDE publishes resource identities
 * and text together; analysis files and the ty workspace are never renamed here. */
export function renameResource({ uri, newName, sourceUris }, context) {
    requireFormMetadata(context);
    const { root, files, definitions, references } = context;
    if (!validRenameName(newName)) throw new Error('Resource name must be a valid Python identifier');
    const path = decodeURIComponent(new URL(uri).pathname);
    const codeRoot = ['client_code', 'server_code'].map(name => `${root}/${name}`)
        .find(prefix => path.startsWith(prefix + '/'));
    if (!codeRoot || !sourceUris.includes(uri) || !files.has(path) || !path.endsWith('.py'))
        throw new Error('Rename requires an editable original app resource');
    const isPackage = path.endsWith('/__init__.py');
    const stem = path.slice(0, isPackage ? -'/__init__.py'.length : -3);
    if (stem === codeRoot) throw new Error('Cannot rename the app code root');
    const oldName = stem.split('/').at(-1);
    if (oldName === newName) return { documentChanges: [], resourceRenames: [] };
    const destination = stem.slice(0, stem.lastIndexOf('/') + 1) + newName;
    const opposite = codeRoot.endsWith('/client_code') ? 'server_code' : 'client_code';
    const other = `${root}/${opposite}${destination.slice(codeRoot.length)}`;
    if ([...files.keys()].some(file => [destination, other].some(target => file === target + '.py' || file.startsWith(target + '/'))))
        throw new Error(`Resource already exists: ${newName}`);
    const moving = sourceUris.filter(source => {
        const file = decodeURIComponent(new URL(source).pathname);
        return isPackage ? file.startsWith(stem + '/') : file === path;
    });
    const nameFor = file => file.slice(codeRoot.length + 1).replace(/(?:\/__init__)?\.py$/, '').replaceAll('/', '.');
    const before = nameFor(path);
    const after = before.slice(0, before.length - oldName.length) + newName;
    const edit = { documentChanges: [], resourceRenames: moving.map(source => {
        const name = nameFor(decodeURIComponent(new URL(source).pathname));
        return { uri: source, oldName: name, newName: after + name.slice(before.length) };
    }) };
    for (const [file, text] of files) {
        if (!file.endsWith('.py')) continue;
        const source = new URL(file, 'file:///').href;
        const names = JSON.parse(renameNames(text));
        const protectedAliases = new Set(names.filter(name => name.alias && name.name === oldName)
            .flatMap(name => context.rename(source, name.range.start, newName))
            .filter(location => location.uri === source).map(location => rangeKey(location.range)));
        const edits = names.filter(name => !name.alias && name.name === oldName && (name.imported || !protectedAliases.has(rangeKey(name.range))) &&
            definitions(source, name.range.start).some(target => target.uri === uri &&
                target.range.start.line === 0 && target.range.start.character === 0 && target.range.end.line === 0 && target.range.end.character === 0))
            .map(name => ({ range: name.range, newText: newName }));
        if (edits.length) {
            if (!sourceUris.includes(source)) throw new Error('Rename requires a read-only source edit');
            edit.documentChanges.push({ textDocument: { uri: source, version: null }, edits });
        }
    }
    extendFormResources(edit, context, sourceUris);
    return edit;
}


export function componentAt(uri, position, context) {
    const targets = context.definitions(uri, position);
    const matches = [];
    for (const target of targets) {
        if (!target.uri.includes('/.anvil/')) continue;
        const source = context.source(target.uri);
        const name = source.split('\n')[target.range.start.line]?.slice(target.range.start.character, target.range.end.character);
        for (const form of context.forms) {
            if (!components(form.data).some(component => component.name === name)) continue;
            if (context.member(form.uri, name).some(member => sameLocation(member, target)))
                matches.push({ formUri: form.uri, componentName: name, target });
        }
    }
    if (!matches.length) return;
    if (matches.some(match => !sameLocation(match.target, matches[0].target)) || targets.some(target => !sameLocation(target, matches[0].target)))
        throw new Error('Cannot safely rename an ambiguous component');
    return matches[0];
}

export function extendAnvilRename(edit, uri, position, newName, context) {
    requireFormMetadata(context);
    const targets = context.definitions(uri, position);
    const forms = context.forms;
    for (const target of targets) {
        const source = context.source(target.uri);
        const oldName = source.split('\n')[target.range.start.line]?.slice(target.range.start.character, target.range.end.character);
        if (oldName) appendHandlerMetadata(edit, target, oldName, newName, forms, context);
    }
    const registrations = callableRegistrations(context).filter(item => item.implicit && targets.some(target => sameLocation(target, item)));
    if (registrations.length) {
        const all = callableRegistrations(context);
        if (registrations.some(item => all.filter(candidate => candidate.kind === item.kind && candidate.name === item.name).length !== 1 ||
            all.some(candidate => candidate.kind === item.kind && candidate.name === newName && !sameLocation(candidate, item))))
            throw new Error('Cannot safely rename an ambiguous or occupied RPC name');
        appendRpcCalls(edit, registrations, newName, context);
    }
    return edit;
}


const before = (a, b) => a.line < b.line || (a.line === b.line && a.character <= b.character);
const contains = (range, position) => before(range.start, position) && before(position, range.end);
const sameLocation = (a, b) => a.uri === b.uri && rangeKey(a.range) === rangeKey(b.range);
const rpcKind = api => ['call', 'call_s'].includes(api) ? 'callable' : api === 'launch_background_task' ? 'background_task' : undefined;

export function callableRegistrations(context) {
    const result = [];
    for (const [path, source] of context.files) {
        if (!path.endsWith('.py') || !path.includes('/server_code/')) continue;
        const uri = new URL(path, 'file:///').href;
        const calls = JSON.parse(apiCalls(source));
        for (const fn of JSON.parse(itemFacts(source)).functions) {
            if (fn.owner !== null) continue;
            for (const decorator of fn.decorators) {
                const kind = context.api(uri, decorator.position);
                if (kind !== 'callable' && kind !== 'background_task') continue;
                const argument = decorator.keywords.name ?? decorator.keywords.fn_or_name ?? decorator.args[0];
                const explicit = Object.hasOwn(decorator.keywords, 'name') || Object.hasOwn(decorator.keywords, 'fn_or_name') || decorator.args.length > 0;
                const implicit = !explicit || decorator.noneArgs?.includes(0) || decorator.noneKeywords?.some(name => name === 'name' || name === 'fn_or_name');
                if (!implicit && typeof argument !== 'string') continue;
                result.push({ uri, range: fn.range, kind, name: implicit ? fn.name : argument, implicit, functionName: fn.name, isAsync: fn.isAsync,
                    literal: calls.find(call => call.position.line === decorator.position.line && call.position.character === decorator.position.character) });
            }
        }
    }
    return result;
}

export function rpcTargets(uri, position, context) {
    const source = context.files.get(decodeURIComponent(new URL(uri).pathname));
    const call = source && JSON.parse(apiCalls(source)).find(call => call.literalRange && contains(call.literalRange, position));
    if (!call) return;
    const api = context.api(uri, call.position);
    const kind = rpcKind(api) ?? (['callable', 'background_task'].includes(api) ? api : undefined);
    if (!kind) return;
    return callableRegistrations(context).filter(item => item.kind === kind && item.name === call.value)
        .map(item => ({ ...item, selected: call.range }));
}

export function rpcTarget(uri, position, context) {
    const targets = rpcTargets(uri, position, context);
    if (!targets) return;
    if (targets.length !== 1) throw new Error('Cannot safely rename an ambiguous or unresolved RPC name');
    return targets[0];
}

export function rpcReferences(uri, position, context, includeDeclaration) {
    let targets = rpcTargets(uri, position, context);
    if (!targets) {
        const declarations = context.definitions(uri, position);
        targets = callableRegistrations(context).filter(item => declarations.some(declaration => sameLocation(item, declaration)));
        if (!targets.length) return;
    }
    const references = targets.flatMap(target => context.references(target.uri, target.range.start))
        .filter(reference => includeDeclaration || !targets.some(target => sameLocation(target, reference)));
    // A literal registration and a literal RPC call share an identity only
    // after ty resolves their decorators/callees to the Anvil API. Ambiguous
    // names may navigate to all possible owners; rename still requires one.
    for (const [path, source] of context.files) {
        if (!path.endsWith('.py')) continue;
        const uri = new URL(path, 'file:///').href;
        for (const call of JSON.parse(apiCalls(source))) {
            if (!call.literalRange || !targets.some(target => target.name === call.value)) continue;
            const api = context.api(uri, call.position);
            const kind = rpcKind(api) ?? (includeDeclaration && ['callable', 'background_task'].includes(api) ? api : undefined);
            if (targets.some(target => target.name === call.value && target.kind === kind))
                references.push({ uri, range: call.range });
        }
    }
    return [...new Map(references.map(reference => [reference.uri + ':' + rangeKey(reference.range), reference])).values()];
}

function appendRpcCalls(edit, registrations, newName, context) {
    for (const [path, source] of context.files) {
        if (!path.endsWith('.py')) continue;
        const uri = new URL(path, 'file:///').href;
        for (const call of JSON.parse(apiCalls(source))) {
            if (!registrations.some(item => item.name === call.value)) continue;
            const kind = rpcKind(context.api(uri, call.position));
            if (!registrations.some(item => item.kind === kind && item.name === call.value)) continue;
            editableReferences(edit, [{ uri, range: call.literalRange }], JSON.stringify(newName), context);
        }
    }
}

export function renameRpc(target, newName, context) {
    if (!newName || target.implicit && !validRenameName(newName)) throw new Error('Invalid callable name');
    const registrations = callableRegistrations(context);
    if (registrations.some(item => item.kind === target.kind && item.name === newName && !sameLocation(item, target)))
        throw new Error('A callable is already registered with this name');
    const edit = { documentChanges: [] };
    if (target.implicit) editableReferences(edit, context.rename(target.uri, target.range.start, newName), newName, context);
    else {
        if (!target.literal?.literalRange) throw new Error('Cannot safely rename the registration');
        editableReferences(edit, [{ uri: target.uri, range: target.literal.literalRange }], JSON.stringify(newName), context);
    }
    appendRpcCalls(edit, [target], newName, context);
    return edit;
}
