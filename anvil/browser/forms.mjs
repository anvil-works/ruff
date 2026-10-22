export function visitForm(node, visit, path = [], componentName = null) {
    if (!node || typeof node !== 'object') return;
    if (typeof node.name === 'string' && typeof node.type === 'string') { componentName = node.name; path = []; }
    visit(node, path, componentName);
    for (const child of node.components ?? []) visitForm(child, visit, [], child.name);
    for (const key of ['container', 'layout']) if (node[key]) visitForm(node[key], visit, [...path, key], componentName);
    for (const children of Object.values(node.components_by_slot ?? {}))
        for (const child of children) visitForm(child, visit, [], child.name);
}

export function components(data) {
    const result = [];
    visitForm(data, node => { if (typeof node.name === 'string' && typeof node.type === 'string') result.push(node); });
    return result;
}

// Only real methods of this Form receive inferred parameters. Explicit Python
// annotations win; a parameter absent from any binding stays gradual.
export function handlerAnnotations(source, facts, className, data, decorators, types) {
    const cls = facts.classes.find(cls => cls.name === className && cls.owner === null);
    if (!cls) return;
    const bindings = [...decorators];
    function addYamlBindings(component, items) {
        for (const [event, handler] of Object.entries(items ?? {})) {
            // The runtime replaces this component/event's YAML binding when a
            // decorated handler exists; it can retain multiple decorators.
            if (!decorators.some(binding => binding.component === component && binding.event === event))
                bindings.push({ component, event, handler });
        }
    }
    visitForm(data, (node, path, component) => {
        const sender = node === data.layout ? 'layout' : component ?? '';
        addYamlBindings(sender, node.event_bindings);
        addYamlBindings('', node.form_event_bindings);
    });
    let alias = '_anvil_handler_types';
    while (source.includes(alias)) alias += '_';
    const edits = [];
    const dictionaries = [];
    for (const fn of facts.functions.filter(fn => fn.owner === cls.id)) {
        const events = bindings.filter(binding => binding.handler === fn.name);
        if (!events.length) continue;
        const payloads = events.map(binding => {
            const component = types.components[binding.component];
            const fields = Object.fromEntries(Object.entries(component?.events[binding.event] ?? {})
                .map(([name, type]) => [name, `${alias}.Designer.${type}`]));
            const sender = !binding.component ? className : component?.sender && `${alias}.Designer.${component.sender}`;
            return { ...fields, event_name: `${alias}.String`, ...(sender ? { sender } : {}) };
        });
        const commonType = name => {
            const annotations = payloads.map(payload => payload[name]);
            return annotations.every(Boolean) ? [...new Set(annotations)].join(' | ') : undefined;
        };
        for (const parameter of fn.parameters) {
            if (parameter.annotated || parameter.name === 'self') continue;
            const annotation = commonType(parameter.name);
            if (annotation) edits.push({ position: parameter.end, text: ': ' + JSON.stringify(annotation) });
        }
        if (!fn.kwarg || fn.kwarg.annotated) continue;
        const fields = Object.keys(payloads[0]).filter(name => !fn.parameters.some(parameter => parameter.name === name))
            .map(name => [name, commonType(name)]).filter(([, type]) => type);
        if (!fields.length) continue;
        const name = `EventArgs${dictionaries.length}`;
        dictionaries.push({ name, fields });
        edits.push({ position: fn.kwarg.end, text: ': ' + JSON.stringify(`${alias}.Unpack[${alias}.${name}]`) });
    }
    if (!edits.length) return;
    // One private namespace owns imports and per-handler TypedDicts in the
    // analysis copy. Its suffix never changes original source coordinates.
    const body = [];
    if (edits.some(edit => edit.text.includes('.String')) ||
        dictionaries.some(dictionary => dictionary.fields.some(([, type]) => type.includes('.String'))))
        body.push('    from builtins import str as String');
    if (edits.some(edit => edit.text.includes('.Designer.')) ||
        dictionaries.some(dictionary => dictionary.fields.some(([, type]) => type.includes('.Designer.'))))
        body.push(`    from ._anvil_designer import ${types.namespace} as Designer`);
    if (dictionaries.length) {
        body.push('    from typing_extensions import TypedDict as _TypedDict, Unpack as Unpack',
            '    from typing import Any as _Any');
        for (const { name, fields } of dictionaries) {
            // Direct Python calls to handlers need not supply event kwargs.
            body.push(`    class ${name}(_TypedDict, total=False, extra_items=_Any):`,
                ...fields.map(([field, type]) => `        ${field}: ${JSON.stringify(type)}`));
        }
    }
    const generated = body.length > 0;
    return { edits, generatedName: generated ? alias : undefined, generatedType: `<class '${alias}'>`,
        declarations: generated ? `class ${alias}:\n${body.join('\n')}\n` : '' };
}

// item_template is a form property, not a component YAML `type`. Match the
// IDE/runtime lookup: exact local name first, then legacy dep ID or package.
export function formPropertyTarget(value, owner, forms, dependencyRoots) {
    if (typeof value !== 'string' || value.startsWith('form:')) return;
    const local = forms.find(form => form.root === owner.root && form.name === value);
    if (local) return local;
    const legacy = /^([^:]+):(.+)$/.exec(value);
    if (legacy) {
        const root = dependencyRoots[owner.root]?.[legacy[1]];
        return forms.find(form => form.root === root && form.name === legacy[2]);
    }
    return forms.find(form => `${form.config.package_name}.${form.name}` === value);
}
