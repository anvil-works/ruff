import assert from 'node:assert/strict';
import { test } from 'node:test';
import { withBrowser } from './browser.mjs';

test('standard Comlink clients receive ordered results and worker exceptions without poisoning later calls', () => withBrowser(async page => {
    const result = await page.evaluate(async () => {
        const Comlink = await import('/dist/comlink.mjs');
        const worker = new Worker('/worker.mjs', { type: 'module' });
        const remote = Comlink.wrap(worker);
        const textDocument = { uri: 'file:///app/main.py' };
        const params = { textDocument, position: { line: 1, character: 2 } };
        try {
            const initialized = remote.request('initialize', {
                rootUri: 'file:///app', files: { '/app/main.py': 'value = "Ada"\nvalue\n' },
            });
            const changed = remote.request('openDocument', { uri: textDocument.uri, text: 'value = 42\nvalue\n', revision: 1 });
            const hover = remote.request('textDocument/hover', params);
            await initialized;
            await changed;
            const response = await hover;
            const error = await remote.request('textDocument/unsupported', params).then(
                () => null, error => ({ name: error.name, message: error.message }),
            );
            const recovered = await remote.request('textDocument/hover', params);
            return { response, error, recovered };
        } finally {
            remote[Comlink.releaseProxy]();
            worker.terminate();
        }
    });
    assert.equal(result.response?.revision, 1);
    assert.match(result.response.result.contents.value, /42/);
    assert.equal(result.error.name, 'Error');
    assert.match(result.error.message, /Unsupported ty browser request/);
    assert.deepEqual(result.recovered, result.response);
}));

test('session cancellation and disposal settle pending queries without losing later results', () => withBrowser(async page => {
    const result = await page.evaluate(async () => {
        const { BrowserAnalysisSession } = await import('/session.mjs');
        const session = new BrowserAnalysisSession({
            workerUrl: '/worker.mjs', rootUri: 'file:///app', files: { '/app/main.py': 'value = "Ada"\nvalue\n' },
        });
        const params = { textDocument: { uri: 'file:///app/main.py' }, position: { line: 1, character: 2 } };
        const settled = promise => promise.then(() => null, error => ({ name: error.name, message: error.message }));
        try {
            await session.readSource(params.textDocument.uri);
            const controller = new AbortController();
            const cancelled = settled(session.query('textDocument/hover', params, { signal: controller.signal }));
            // Let query send its worker call before aborting the consumer.
            await Promise.resolve();
            controller.abort();
            const aborted = await cancelled;
            const next = await session.query('textDocument/hover', params);
            const pending = settled(session.query('textDocument/hover', params));
            await Promise.resolve();
            session.dispose();
            const disposed = await pending;
            const later = await settled(session.query('textDocument/hover', params));
            return { aborted, next, disposed, later };
        } finally { session.dispose(); }
    });
    assert.equal(result.aborted.name, 'AbortError');
    assert.match(result.next.result.contents.value, /Ada/);
    assert.match(result.disposed.message, /disposed/);
    assert.match(result.later.message, /disposed/);
}));

test('worker load failures reject the session instead of leaving initialization pending', () => withBrowser(async page => {
    const result = await page.evaluate(async () => {
        const { BrowserAnalysisSession } = await import('/session.mjs');
        const session = new BrowserAnalysisSession({ workerUrl: '/missing-worker.mjs', rootUri: 'file:///app', files: {} });
        try {
            return await session.readSource('file:///app/main.py').then(
                () => null, error => ({ name: error.name, message: error.message }),
            );
        } finally { session.dispose(); }
    });
    assert.equal(result.name, 'Error');
    assert.match(result.message, /worker failed/);
}));

// Run the public session against a real browser worker and the upstream ty WASM build.
test('stub definitions are readable and ordered source updates change inferred completions', () => withBrowser(async page => {
        const result = await page.evaluate(async () => {
            const { BrowserAnalysisSession } = await import('/session.mjs');
            const session = new BrowserAnalysisSession({
                workerUrl: new URL('/worker.mjs', location.href).href,
                rootUri: 'file:///app',
                files: {
                    '/app/main.py': 'from library import greet\nvalue = greet()\nvalue.\nstr\n',
                    '/app/library.pyi': 'def greet() -> str: ...\n',
                },
            });
            const uri = 'file:///app/main.py';
            const complete = () => session.query('textDocument/completion', {
                textDocument: { uri }, position: { line: 2, character: 6 },
            });
            try {
                const initial = await complete();
                const definitions = await session.query('textDocument/definition', {
                    textDocument: { uri }, position: { line: 0, character: 22 },
                });
                const stub = await session.query('anvil/readSource', { uri: definitions.result[0].uri });
                const builtins = await session.query('textDocument/definition', {
                    textDocument: { uri }, position: { line: 3, character: 1 },
                });
                const builtin = await session.query('anvil/readSource', { uri: builtins.result[0].uri });
                const update = session.updateFiles({ '/app/library.pyi': 'def greet() -> int: ...\n' });
                const changed = await complete();
                await update;
                return { initial, definitions, stub, builtin, changed, revision: session.revision };
            } finally { session.dispose(); }
        });
        assert(result.initial.result.items.some(item => item.label === 'upper'));
        assert.equal(result.definitions.result[0].uri, 'file:///app/library.pyi');
        assert.equal(result.stub.result.text, 'def greet() -> str: ...\n');
        assert.equal(result.stub.result.readOnly, true);
        assert(result.builtin.result.uri.includes('builtins.pyi'));
        assert(result.builtin.result.text.includes('class str'));
        assert.equal(result.builtin.result.readOnly, true);
        assert(result.changed.result.items.some(item => item.label === 'bit_length'));
        assert(!result.changed.result.items.some(item => item.label === 'upper'));
        assert.equal(result.changed.revision, result.revision);
        assert.equal(result.revision, 1);
}));

test('Python references and cross-file rename preserve UTF-16 positions and read-only stubs', () => withBrowser(async page => {
    const result = await page.evaluate(async () => {
        const { BrowserAnalysisSession } = await import('/session.mjs');
        const session = new BrowserAnalysisSession({
            workerUrl: new URL('/worker.mjs', location.href).href, rootUri: 'file:///app',
            files: {
                '/app/library.py': 'def greet(): return "Hello"\n',
                '/app/main.py': 'from library import greet\nemoji = "😀"; result = greet()\n',
                '/app/external.pyi': 'def external() -> str: ...\n',
            },
        });
        const params = { textDocument: { uri: 'file:///app/main.py' }, position: { line: 1, character: 24 } };
        try {
            const references = await session.query('textDocument/references', { ...params, context: { includeDeclaration: true } });
            const prepared = await session.query('textDocument/prepareRename', params);
            const invalidNames = [];
            for (const newName of ['bad-name', 'class']) {
                invalidNames.push(await session.query('textDocument/rename', { ...params, newName })
                    .then(() => null, error => error.message));
            }
            const renamed = await session.query('textDocument/rename', { ...params, newName: 'salute' });
            let refused;
            try {
                await session.query('textDocument/rename', {
                    textDocument: { uri: 'file:///app/external.pyi' }, position: { line: 0, character: 5 }, newName: 'changed',
                });
            } catch (error) { refused = String(error); }
            return { references, prepared, renamed, refused, invalidNames };
        } finally { session.dispose(); }
    });
    assert(result.references.result.some(location => location.uri === 'file:///app/library.py'));
    assert.deepEqual(result.prepared.result.range.start, { line: 1, character: 23 });
    const changes = result.renamed.result.documentChanges;
    assert(changes.some(change => change.textDocument.uri === 'file:///app/library.py'));
    assert(changes.some(change => change.textDocument.uri === 'file:///app/main.py'));
    assert(changes.every(change => change.edits.every(edit => edit.newText === 'salute')));
    assert(result.invalidNames.every(message => /identifier/.test(message)), JSON.stringify(result.invalidNames));
    assert.match(result.refused, /read.only/i);
}));

test('typed calls expose signature help and native ty diagnostics', () => withBrowser(async page => {
    const result = await page.evaluate(async () => {
        const { BrowserAnalysisSession } = await import('/session.mjs');
        const session = new BrowserAnalysisSession({
            workerUrl: new URL('/worker.mjs', location.href).href, rootUri: 'file:///app',
            files: { '/app/main.py': 'def greet(name: str, excited: bool = False) -> str:\n    return name\nvalue = greet(42)\ngreet("Ada", True)\n' },
        });
        const textDocument = { uri: 'file:///app/main.py' };
        try {
            const signature = await session.query('textDocument/signatureHelp', { textDocument, position: { line: 3, character: 14 } });
            const diagnostics = await session.query('textDocument/diagnostic', { textDocument });
            return { signature, diagnostics };
        } finally { session.dispose(); }
    });
    assert(result.signature.result.signatures[0].label.includes('name: str'));
    assert.equal(result.signature.result.signatures[0].activeParameter, 1);
    const error = result.diagnostics.result.items.find(item => item.code === 'invalid-argument-type');
    assert(error);
    assert.equal(error.severity, 1);
    assert.equal(error.range.start.line, 2);
}));

test('hover exposes resolved signatures, documentation and ranges for app code and API stubs', () => withBrowser(async page => {
    const result = await page.evaluate(async () => {
        const { BrowserAnalysisSession } = await import('/session.mjs');
        const code = 'import anvil\ndef greet(name: str) -> str:\n    """Welcome a customer."""\n    return name\nvalue = greet("Ada")\nbutton = anvil.Button()\n';
        const session = new BrowserAnalysisSession({
            workerUrl: new URL('/worker.mjs', location.href).href, rootUri: 'file:///app',
            files: { '/app/anvil.yaml': 'package_name: TestApp\n', '/app/client_code/__init__.py': '', '/app/client_code/main.py': code },
        });
        const textDocument = { uri: 'file:///app/client_code/main.py' };
        const hover = position => session.query('textDocument/hover', { textDocument, position });
        try {
            const method = await hover({ line: 4, character: 10 });
            const variable = await hover({ line: 4, character: 2 });
            const api = await hover({ line: 5, character: 17 });
            const definitions = await session.query('textDocument/definition', { textDocument, position: { line: 5, character: 17 } });
            const readonly = await session.query('textDocument/hover', {
                textDocument: { uri: definitions.result[0].uri }, position: definitions.result[0].range.start,
            });
            return { method, variable, api, readonly };
        } finally { session.dispose(); }
    });
    assert.match(result.method.result.contents.value, /greet\(name: str\) -> str/);
    assert.match(result.method.result.contents.value, /Welcome a customer/);
    assert.equal(result.method.result.contents.kind, 'markdown');
    assert.equal(result.method.result.range.start.line, 4);
    assert.match(result.variable.result.contents.value, /str/);
    assert.match(result.api.result.contents.value, /Button/);
    assert.match(result.api.result.contents.value, /https:\/\/anvil\.works\/docs\//);
    assert.match(result.readonly.result.contents.value, /Button/);
}));

test('API completion and property hover retain curated links without attaching them to app symbols', () => withBrowser(async page => {
    const result = await page.evaluate(async () => {
        const { BrowserAnalysisSession } = await import('/session.mjs');
        const lines = [
            'from anvil import Button as ActionButton',
            'button = ActionButton()',
            'button.text',
            'button.te',
            'class Button:',
            '    @property',
            '    def text(self) -> str:',
            '        """Our text. [Guide](https://example.com/button)"""',
            '        return ""',
            'custom = Button()',
            'custom.text',
            'ActionBut',
            'from anvil.designer import get_design_name',
            'get_design_na',
            'custom.te',
        ];
        const session = new BrowserAnalysisSession({
            workerUrl: '/worker.mjs', rootUri: 'file:///app',
            files: { '/app/anvil.yaml': 'package_name: TestApp\n', '/app/client_code/main.py': lines.join('\n') },
        });
        const textDocument = { uri: 'file:///app/client_code/main.py' };
        const query = (method, line, character) => session.query(`textDocument/${method}`, { textDocument, position: { line, character } });
        try {
            const property = (await query('completion', 3, lines[3].length)).result.items.find(item => item.label === 'text');
            const custom = (await query('completion', 14, lines[14].length)).result.items.find(item => item.label === 'text');
            const result = {
                api: (await query('completion', 11, lines[11].length)).result.items.find(item => item.label === 'ActionButton'),
                hover: (await query('hover', 2, 9)).result,
                custom: (await query('hover', 10, 9)).result,
                designer: (await query('completion', 13, lines[13].length)).result.items.find(item => item.label === 'get_design_name'),
                resolved: (await session.query('completionItem/resolve', property)).result,
                customResolved: (await session.query('completionItem/resolve', custom)).result,
                source: (await session.readSource(textDocument.uri)).result.text,
                original: lines.join('\n'),
            };
            await session.openDocument(textDocument.uri, lines.join('\n') + '\n# edited');
            return { ...result, obsolete: await session.query('completionItem/resolve', property).catch(error => error.name) };
        } finally { session.dispose(); }
    });
    const href = 'https://anvil.works/docs/components/standard-components/basic#button';
    assert.ok(result.api.documentation.includes(`[Anvil Docs](${href})`), JSON.stringify(result));
    assert.ok(result.hover.contents.value.includes(`[Anvil Docs](${href})`));
    assert.match(result.custom.contents.value, /https:\/\/example.com\/button/);
    assert.doesNotMatch(result.custom.contents.value, /Anvil Docs|anvil\.works/);
    assert.match(result.designer.documentation, /\[Anvil Docs\]\(https:\/\/anvil\.works\/docs\/client\/forms\/advanced-layouts\/component-api\/designer-module\)/);
    assert.match(result.resolved.documentation.value, /\[Anvil Docs\]\(https:\/\/anvil\.works\/docs\/components\/standard-components\/basic#button\)/);
    assert.match(result.customResolved.documentation.value, /https:\/\/example.com\/button/);
    assert.doesNotMatch(result.customResolved.documentation.value, /Anvil Docs|anvil\.works/);
    assert.equal(result.source, result.original);
    assert.equal(result.obsolete, 'AbortError');
}));

test('client Plotly aliases, wrapped properties and selected docs follow the catalogue', () => withBrowser(async page => {
    const result = await page.evaluate(async () => {
        const { BrowserAnalysisSession } = await import('/session.mjs');
        const lines = [
            'import plotly.graph_objects as go',
            'from plotly.graph_objs.scatter import Marker',
            'trace = go.Scatter(x=[1, 2], y=[3, 4], marker_line_color="red")',
            'trace.marker = {"color": ["red", "blue"], "size": [6, 8]}',
            'trace.marker.size = [10, 12]',
            'trace.marker.co',
            'trace.name.',
            'figure = go.Figure(data=[trace], layout={"title": "Example"})',
            'figure.update_layout(title="Updated"); figure.layout = {"title": "Assigned"}',
            'figure.layout.',
            'Marker().',
            'figure.data = (trace,)',
            'go.Scatter(',
        ];
        const uri = 'file:///app/client_code/main.py';
        const session = new BrowserAnalysisSession({ workerUrl: '/worker.mjs', rootUri: 'file:///app', files: {
            '/app/anvil.yaml': 'package_name: TestApp\n', '/app/client_code/main.py': '',
        } });
        const textDocument = { uri };
        const complete = async line => (await session.query('textDocument/completion', {
            textDocument, position: { line, character: lines[line].length },
        })).result.items;
        try {
            await session.openDocument(uri, lines.join('\n'));
            const colors = await complete(5);
            const color = colors.find(item => item.label === 'color');
            const docs = color && (await session.query('completionItem/resolve', color)).result;
            const string = await complete(6);
            const layout = await complete(9);
            const marker = await complete(10);
            const x = (await complete(12)).find(item => item.label === 'x=' || item.label === 'x');
            const keywordDocs = x && (await session.query('completionItem/resolve', x)).result;
            await session.openDocument(uri, lines.filter((_, i) => ![5, 6, 9, 10, 12].includes(i)).join('\n'));
            const diagnostics = (await session.query('textDocument/diagnostic', { textDocument })).result.items;
            return { color, docs, keywordDocs, string, layout, marker, diagnostics };
        } finally { session.dispose(); }
    });
    assert(result.color);
    assert.match(result.docs.documentation.value, /Sets the marker color/);
    assert(result.layout.some(item => item.label === 'title'));
    assert.match(typeof result.keywordDocs.documentation === 'string' ? result.keywordDocs.documentation : result.keywordDocs.documentation?.value ?? '', /Sets the x coordinates/);
    assert(result.string.some(item => item.label === 'upper'));
    assert(result.marker.some(item => item.label === 'size'));
    assert.deepEqual(result.diagnostics.filter(item => item.severity === 1), []);
}));

test('unused Plotly dependency caches stay out of scoped completion until a client REPL imports it', () => withBrowser(async page => {
    const result = await page.evaluate(async () => {
        const { BrowserAnalysisSession } = await import('/session.mjs');
        const uri = 'file:///app/client_code/main.py';
        const session = new BrowserAnalysisSession({ workerUrl: '/worker.mjs', rootUri: 'file:///app', files: {
            '/app/anvil.yaml': 'package_name: Main\ndependencies: []\n', '/app/client_code/main.py': 'pl',
            '/app/.anvil/deps/unused/anvil.yaml': 'package_name: Unused\n',
            '/app/.anvil/deps/unused/client_code/chart.py': 'import plotly.graph_objects as go\n',
        } });
        try {
            const initial = (await session.query('textDocument/completion', {
                textDocument: { uri }, position: { line: 0, character: 2 },
            })).result.items;
            const code = 'go.Scatter().marker.co';
            await session.setContext({ kind: 'repl', id: 'plotly', isServer: false,
                previousCode: 'import plotly.graph_objects as go', code });
            const context = (await session.queryContext('plotly', 'textDocument/completion', {
                position: { line: 0, character: code.length },
            })).result.items;
            return { initial, context };
        } finally { session.dispose(); }
    });
    assert(result.initial.some(item => item.label === 'plotly'));
    assert(!result.initial.some(item => item.label.startsWith('plotly.')));
    assert(result.context.some(item => item.label === 'color'));
}));

test('GoogleMap overlays expose typed constructors, inherited properties and property documentation', () => withBrowser(async page => {
    const result = await page.evaluate(async () => {
        const { BrowserAnalysisSession } = await import('/session.mjs');
        const lines = [
            'from anvil import GoogleMap, Label',
            'point = GoogleMap.LatLng(52.2, 0.1)',
            'circle = GoogleMap.Circle(center=point, radius=100, fill_color="red", clickable=True)',
            'rectangle = GoogleMap.Rectangle(bounds=GoogleMap.LatLngBounds(point, point), editable=True)',
            'popup = GoogleMap.InfoWindow(content=Label(text="Hello"), pixel_offset=GoogleMap.Size(10, 20))',
            'popup.open(GoogleMap())',
            'marker = GoogleMap.Marker(title="Cambridge", cursor="pointer", opacity=0.5)',
            'circle.radius = "wrong"',
            'circle.ra',
            'marker.ti',
        ];
        const session = new BrowserAnalysisSession({ workerUrl: '/worker.mjs', rootUri: 'file:///app', files: {
            '/app/anvil.yaml': 'package_name: TestApp\n', '/app/client_code/main.py': lines.join('\n'),
        }});
        const textDocument = { uri: 'file:///app/client_code/main.py' };
        try {
            const complete = async line => (await session.query('textDocument/completion', {
                textDocument, position: { line, character: lines[line].length },
            })).result.items;
            const radius = (await complete(8)).find(item => item.label === 'radius');
            const title = (await complete(9)).find(item => item.label === 'title');
            return { radius, title, docs: radius && (await session.query('completionItem/resolve', radius)).result,
                diagnostics: (await session.query('textDocument/diagnostic', { textDocument })).result.items };
        } finally { session.dispose(); }
    });
    assert.ok(result.radius, JSON.stringify(result));
    assert.ok(result.title);
    assert.match(result.docs.documentation.value, /radius/i);
    assert.match(result.docs.documentation.value, /\[Anvil Docs\]\(https:\/\/anvil\.works\/docs\/components\/standard-components\/maps/);
    assert.deepEqual(result.diagnostics.filter(item => item.range.start.line < 8).map(item => item.range.start.line), [7]);
}));

test('Anvil Form members are generated from current Designer metadata without editing original Python', () => withBrowser(async page => {
    const result = await page.evaluate(async () => {
        const { BrowserAnalysisSession } = await import('/session.mjs');
        const code = 'from ._anvil_designer import Form1Template\nclass Form1(Form1Template):\n    def probe(self):\n        self.label.\n';
        const session = new BrowserAnalysisSession({
            workerUrl: new URL('/worker.mjs', location.href).href, rootUri: 'file:///app',
            files: {
                '/app/anvil.yaml': 'package_name: TestApp\n',
                '/app/client_code/__init__.py': '',
                '/app/client_code/Form1/__init__.py': code,
                '/app/client_code/Form1/form_template.yaml': JSON.stringify({
                    container: { type: 'ColumnPanel' }, components: [{ name: 'label', type: 'Label' }],
                }),
            },
        });
        const uri = 'file:///app/client_code/Form1/__init__.py';
        try {
            const completed = await session.query('textDocument/completion', {
                textDocument: { uri }, position: { line: 3, character: 19 },
            });
            await session.openDocument(uri, code.replace('self.label.', 'self.label.te'));
            const ranked = await session.query('textDocument/completion', {
                textDocument: { uri }, position: { line: 3, character: 21 },
            });
            await session.closeDocument(uri);
            const update = session.updateFiles({
                '/app/client_code/Form1/form_template.yaml': JSON.stringify({
                    container: { type: 'ColumnPanel' }, components: [{ name: 'label', type: 'TextBox' }],
                }),
            });
            const changed = await session.query('textDocument/completion', {
                textDocument: { uri }, position: { line: 3, character: 19 },
            });
            await update;
            const source = await session.query('anvil/readSource', { uri });
            return { completed, ranked, changed, source, code };
        } finally { session.dispose(); }
    });
    assert(result.completed.result.items.some(item => item.label === 'text'));
    assert(!result.completed.result.items.some(item => item.label === 'placeholder'));
    // LSP clients sort by sortText, falling back to label. Preserve ty's native
    // ranking so accepting the first match chooses text, not __getattribute__.
    assert.equal([...result.ranked.result.items].sort((a, b) =>
        (a.sortText ?? a.label).localeCompare(b.sortText ?? b.label))[0].label, 'text');
    assert(result.changed.result.items.some(item => item.label === 'placeholder'));
    assert.equal(result.source.result.text, result.code);
}));

test('rejected updates preserve the previous project and allow the next ordered edit', () => withBrowser(async page => {
    const result = await page.evaluate(async () => {
        const { BrowserAnalysisSession } = await import('/session.mjs');
        const config = '/app/anvil.yaml';
        const uri = 'file:///app/client_code/main.py';
        const source = 'value = "Ada"\nvalue.\n';
        const session = new BrowserAnalysisSession({ workerUrl: '/worker.mjs', rootUri: 'file:///app', files: {
            [config]: 'package_name: Main\n', '/app/client_code/main.py': source,
        } });
        const labels = async () => (await session.query('textDocument/completion', {
            textDocument: { uri }, position: { line: 1, character: 6 },
        })).result.items.map(item => item.label);
        try {
            const initial = await labels();
            let failure;
            try { await session.updateFiles({ [config]: 'package_name: [', '/app/client_code/main.py': 'value = 1\nvalue.\n' }); }
            catch (error) { failure = String(error); }
            const preserved = await labels();
            const text = (await session.readSource(uri)).result.text;
            await session.updateFiles({ '/app/client_code/main.py': 'value = [1]\nvalue.\n' });
            return { initial, failure, preserved, text, source, changed: await labels(), revision: session.revision };
        } finally { session.dispose(); }
    });
    assert(result.failure, 'The malformed configuration must reject the update');
    assert(result.initial.includes('upper') && result.preserved.includes('upper'));
    assert.equal(result.text, result.source, 'A rejected batch cannot retain other source edits');
    assert(result.changed.includes('append') && !result.changed.includes('upper'));
    assert.equal(result.revision, 2);
}));

test('invalid Designer metadata stays isolated from valid Forms and modules and remains correctable', () => withBrowser(async page => {
    const result = await page.evaluate(async () => {
        const { BrowserAnalysisSession } = await import('/session.mjs');
        const template = '/app/client_code/Form1/form_template.yaml';
        const session = new BrowserAnalysisSession({
            workerUrl: new URL('/worker.mjs', location.href).href, rootUri: 'file:///app',
            files: {
                '/app/anvil.yaml': 'package_name: TestApp\n',
                '/app/client_code/__init__.py': '',
                '/app/client_code/Form1/__init__.py': 'from ._anvil_designer import Form1Template\nclass Form1(Form1Template):\n    def probe(self):\n        self.label.\n',
                [template]: 'container: {type: ColumnPanel}\ncomponents: [{name: label, type: "form:Missing"}]\n',
                '/app/client_code/other.py': 'number: int = "bad"\n',
                '/app/client_code/Good/__init__.py': 'from ._anvil_designer import GoodTemplate\nclass Good(GoodTemplate): pass\n',
                '/app/client_code/Good/form_template.yaml': 'container: {type: ColumnPanel}\ncomponents: []\n',
            },
        });
        const textDocument = { uri: 'file:///app/client_code/Form1/__init__.py' };
        try {
            const invalid = await session.query('textDocument/diagnostic', { textDocument });
            const other = await session.query('textDocument/diagnostic', { textDocument: { uri: 'file:///app/client_code/other.py' } });
            await session.updateFiles({ [template]: 'components: [' });
            const malformed = await session.query('textDocument/diagnostic', { textDocument });
            const unaffected = await session.query('textDocument/diagnostic', { textDocument: { uri: 'file:///app/client_code/other.py' } });
            const rename = await session.query('anvil/renameResource', {
                uri: 'file:///app/client_code/Good/__init__.py', newName: 'Better',
                sourceUris: ['file:///app/client_code/Good/__init__.py'],
            }).then(() => null, error => String(error));
            await session.updateFiles({ [template]: 'container: {type: ColumnPanel}\ncomponents: [{name: label, type: Label}]\n' });
            const corrected = await session.query('textDocument/completion', { textDocument, position: { line: 3, character: 19 } });
            const diagnostics = await session.query('textDocument/diagnostic', { textDocument });
            return { invalid, malformed, unaffected, rename, other, corrected, diagnostics };
        } finally { session.dispose(); }
    });
    assert(result.invalid.result.items.some(item => item.code === 'invalid-form-template'));
    assert(result.other.result.items.some(item => item.code === 'invalid-assignment'));
    assert(result.malformed.result.items.some(item => item.code === 'invalid-form-template'));
    assert(result.unaffected.result.items.some(item => item.code === 'invalid-assignment'));
    assert.match(result.rename, /invalid Form metadata/);
    assert(result.corrected.result.items.some(item => item.label === 'text'));
    assert(!result.diagnostics.result.items.some(item => item.code === 'invalid-form-template'));
}));

test('custom Forms retain their real source identity through qualified package imports', () => withBrowser(async page => {
    const result = await page.evaluate(async () => {
        const { BrowserAnalysisSession } = await import('/session.mjs');
        const session = new BrowserAnalysisSession({
            workerUrl: new URL('/worker.mjs', location.href).href, rootUri: 'file:///app',
            files: {
                '/app/anvil.yaml': 'package_name: TestApp\n',
                '/app/client_code/__init__.py': '',
                '/app/client_code/Other/__init__.py': 'class Other:\n    def say_hello(self) -> str: return "Hello"\n',
                '/app/client_code/caller.py': 'from TestApp.Other import Other\nOther().say_hello()\n',
                '/app/server_code/consumer.py': 'from TestApp.Other import Other\nOther().say_hello()\n',
                '/app/client_code/Form1/__init__.py': 'from ._anvil_designer import Form1Template\nclass Form1(Form1Template):\n    def probe(self):\n        self.card.\n        self.card.say_hello()\n',
                '/app/client_code/Form1/form_template.yaml': 'container: {type: ColumnPanel}\ncomponents: [{name: card, type: "form:Other"}]\n',
            },
        });
        const textDocument = { uri: 'file:///app/client_code/Form1/__init__.py' };
        try {
            const completion = await session.query('textDocument/completion', { textDocument, position: { line: 3, character: 18 } });
            const definition = await session.query('textDocument/definition', { textDocument, position: { line: 4, character: 24 } });
            const rename = await session.query('textDocument/rename', { textDocument, position: { line: 4, character: 24 }, newName: 'greet' });
            const references = await session.query('textDocument/references', { textDocument, position: { line: 4, character: 24 }, context: { includeDeclaration: true } });
            return { completion, definition, rename, references };
        } finally { session.dispose(); }
    });
    assert(result.completion.result.items.some(item => item.label === 'say_hello'));
    assert.equal(result.definition.result[0].uri, 'file:///app/client_code/Other/__init__.py');
    assert.deepEqual(new Set(result.rename.result.documentChanges.map(change => change.textDocument.uri)), new Set([
        'file:///app/client_code/Other/__init__.py', 'file:///app/client_code/Form1/__init__.py', 'file:///app/client_code/caller.py',
        'file:///app/server_code/consumer.py',
    ]));
    assert.equal(result.rename.result.documentChanges.reduce((count, change) => count + change.edits.length, 0), 4);
    assert(result.references.result.some(location => location.uri === 'file:///app/server_code/consumer.py'));
    assert.equal(new Set(result.references.result.map(location => JSON.stringify(location))).size, result.references.result.length);
}));

test('unopened dependencies supply inferred types and readable sources without becoming editable', () => withBrowser(async page => {
    const result = await page.evaluate(async () => {
        const { BrowserAnalysisSession } = await import('/session.mjs');
        const session = new BrowserAnalysisSession({
            workerUrl: new URL('/worker.mjs', location.href).href, rootUri: 'file:///app',
            files: {
                '/app/anvil.yaml': 'package_name: TestApp\ndependencies: [{app_id: LIBRARY}]\n',
                '/app/client_code/__init__.py': '',
                '/app/client_code/main.py': 'from Library.util import greet\nvalue = greet()\nvalue.\n',
                '/app/.anvil/deps/LIBRARY/anvil.yaml': 'package_name: Library\n',
                '/app/.anvil/deps/LIBRARY/client_code/__init__.py': '',
                '/app/.anvil/deps/LIBRARY/client_code/util.py': 'def greet(): return "Hello"\n',
                '/app/.anvil/deps/UNUSED/anvil.yaml': '[malformed YAML',
            },
        });
        const textDocument = { uri: 'file:///app/client_code/main.py' };
        try {
            const completion = await session.query('textDocument/completion', { textDocument, position: { line: 2, character: 6 } });
            const definition = await session.query('textDocument/definition', { textDocument, position: { line: 1, character: 10 } });
            const source = definition.result.length && await session.query('anvil/readSource', { uri: definition.result[0].uri });
            let refused;
            try { await session.query('textDocument/rename', { textDocument, position: { line: 1, character: 10 }, newName: 'salute' }); }
            catch (error) { refused = String(error); }
            await session.updateFiles({ '/app/anvil.yaml': 'package_name: TestApp\ndependencies: []\n' });
            const removed = await session.query('textDocument/diagnostic', { textDocument });
            return { completion, definition, source, refused, removed };
        } finally { session.dispose(); }
    });
    assert(result.completion.result.items.some(item => item.label === 'upper'), JSON.stringify(result));
    assert.equal(result.definition.result[0].uri, 'file:///app/.anvil/deps/LIBRARY/client_code/util.py');
    assert.equal(result.source.result.text, 'def greet(): return "Hello"\n');
    assert.equal(result.source.result.readOnly, true);
    assert.match(result.refused, /read.only/i);
    assert(result.removed.result.items.some(item => item.code === 'unresolved-import'));
}));

test('dependencies added and reloaded after an unresolved import refresh inference', () => withBrowser(async page => {
    const result = await page.evaluate(async () => {
        const { BrowserAnalysisSession } = await import('/session.mjs');
        const textDocument = { uri: 'file:///app/client_code/main.py' };
        const session = new BrowserAnalysisSession({
            workerUrl: '/worker.mjs', rootUri: 'file:///app', files: {
                '/app/anvil.yaml': 'package_name: TestApp\n',
                '/app/client_code/__init__.py': '',
                '/app/client_code/main.py': 'from Library.helpers import value\nresult = value()\nresult.\n',
            },
        });
        const complete = async () => (await session.query('textDocument/completion', {
            textDocument, position: { line: 2, character: 7 },
        })).result.items.map(item => item.label);
        try {
            const missing = await session.query('textDocument/diagnostic', { textDocument });
            await session.updateFiles({
                '/app/anvil.yaml': 'package_name: TestApp\ndependencies: [{app_id: LIBRARY}]\n',
                '/app/.anvil/deps/LIBRARY/anvil.yaml': 'package_name: Library\n',
                '/app/.anvil/deps/LIBRARY/client_code/__init__.py': '',
                '/app/.anvil/deps/LIBRARY/client_code/helpers.py': 'def value() -> str: return "Ada"\n',
                '/app/.anvil/deps/LIBRARY/server_code/jobs.py': 'from anvil.server import background_task\n@background_task\ndef nightly(): pass\n',
            });
            const added = await complete();
            const tasks = await session.query('anvil/getBackgroundTasks', {});
            await session.updateFiles({ '/app/.anvil/deps/LIBRARY/client_code/helpers.py': 'def value() -> int: return 42\n' });
            const reloaded = await complete();
            await session.updateFiles({ '/app/anvil.yaml': 'package_name: TestApp\ndependencies: []\n' });
            const removed = await session.query('textDocument/diagnostic', { textDocument });
            const removedTasks = await session.query('anvil/getBackgroundTasks', {}).then(answer => answer.result, error => ({ error: error.message }));
            return { missing: missing.result, added, reloaded, removed: removed.result, tasks: tasks.result, removedTasks };
        } finally { session.dispose(); }
    });
    assert(result.missing.items.some(item => item.code === 'unresolved-import'));
    assert(result.added.includes('upper'), JSON.stringify(result.added));
    assert(result.reloaded.includes('bit_length'));
    assert(!result.reloaded.includes('upper'));
    assert(result.removed.items.some(item => item.code === 'unresolved-import'));
    assert(result.tasks.some(task => task.name === 'nightly'));
    assert.deepEqual(result.removedTasks, []);
}));

test('logical dependency remaps refresh Form types without changing selected sources', () => withBrowser(async page => {
    const result = await page.evaluate(async () => {
        const { BrowserAnalysisSession } = await import('/session.mjs');
        const roots = ['/app/.anvil/deps/A', '/app/.anvil/deps/B'];
        const manifest = index => JSON.stringify({ roots, ids: { LIB: roots[index] } });
        const files = {
            '/app/anvil.yaml': 'package_name: Main\n',
            '/app/.anvil/dependencies.json': manifest(0),
            '/app/client_code/Home/__init__.py': 'from ._anvil_designer import HomeTemplate\nclass Home(HomeTemplate):\n    def probe(self):\n        self.widget.\n',
            '/app/client_code/Home/form_template.yaml': 'class_name: Home\ncontainer: {type: ColumnPanel}\ncomponents: [{name: widget, type: "form:LIB:Widget"}]\n',
        };
        for (const [index, root] of roots.entries()) {
            files[root + '/anvil.yaml'] = `package_name: Library${index}\n`;
            files[root + '/client_code/Widget/__init__.py'] = `from ._anvil_designer import WidgetTemplate\nclass Widget(WidgetTemplate):\n    def ${index === 0 ? 'alpha' : 'beta'}(self): pass\n`;
            files[root + '/client_code/Widget/form_template.yaml'] = 'class_name: Widget\ncontainer: {type: ColumnPanel}\ncomponents: []\n';
        }
        const session = new BrowserAnalysisSession({ workerUrl: '/worker.mjs', rootUri: 'file:///app', files });
        const complete = async () => (await session.query('textDocument/completion', {
            textDocument: { uri: 'file:///app/client_code/Home/__init__.py' }, position: { line: 3, character: 20 },
        })).result.items.map(item => item.label).filter(label => ['alpha', 'beta'].includes(label));
        try {
            const before = await complete();
            await session.updateFiles({ '/app/.anvil/dependencies.json': manifest(1) });
            return { before, after: await complete() };
        } finally { session.dispose(); }
    });
    assert.deepEqual(result.before, ['alpha']);
    assert.deepEqual(result.after, ['beta']);
}));

test('table schema supplies row keys and value types and refreshes without Python edits', () => withBrowser(async page => {
    const result = await page.evaluate(async () => {
        const { BrowserAnalysisSession } = await import('/session.mjs');
        const config = type => JSON.stringify({ package_name: 'TestApp', db_schema: {
            people: { columns: [{ name: 'name', type }, { name: 'age', type: 'number' },
                { name: 'first name', type: 'string' }, { name: "quote'path\\name", type: 'string' }] },
        } });
        const session = new BrowserAnalysisSession({
            workerUrl: new URL('/worker.mjs', location.href).href, rootUri: 'file:///app',
            files: {
                '/app/anvil.yaml': config('string'), '/app/client_code/__init__.py': '',
                '/app/client_code/main.py': 'from anvil.tables import app_tables\nrow = app_tables.people.get()\nrow["name"].\nrow[""]\nrow["first n"]\nrow[\'quote\']\n',
            },
        });
        const textDocument = { uri: 'file:///app/client_code/main.py' };
        try {
            const value = await session.query('textDocument/completion', { textDocument, position: { line: 2, character: 12 } });
            const keys = await session.query('textDocument/completion', { textDocument, position: { line: 3, character: 5 } });
            const spaced = await session.query('textDocument/completion', { textDocument, position: { line: 4, character: 12 } });
            const escaped = await session.query('textDocument/completion', { textDocument, position: { line: 5, character: 10 } });
            await session.updateFiles({ '/app/anvil.yaml': config('number') });
            const changed = await session.query('textDocument/completion', { textDocument, position: { line: 2, character: 12 } });
            return { value, keys, spaced, escaped, changed };
        } finally { session.dispose(); }
    });
    assert(result.value.result.items.some(item => item.label === 'upper'));
    assert(result.keys.result.items.some(item => item.label.includes('name')));
    assert(result.keys.result.items.some(item => item.label.includes('age')));
    assert.deepEqual(result.spaced.result.items.find(item => item.label === 'first name').textEdit, {
        range: { start: { line: 4, character: 5 }, end: { line: 4, character: 12 } }, newText: 'first name',
    });
    assert.equal(result.escaped.result.items[0].textEdit.newText, "quote\\'path\\\\name");
    assert(!result.changed.result.items.some(item => item.label === 'upper'));
    assert(result.changed.result.items.some(item => item.label === 'real'));
}));

test('table writes accept None and still check column types in client and server', () => withBrowser(async page => {
    const result = await page.evaluate(async () => {
        const { BrowserAnalysisSession } = await import('/session.mjs');
        const source = 'from anvil.tables import app_tables\n' +
            'row = app_tables.people.add_row(name=None)\nrow.update(name=None)\n' +
            'contact = app_tables.contacts.add_row(**{"full name": None})\ncontact.update(**{"full name": None})\n' +
            'name: str = row["name"]\nrow.update(name=123)\n';
        const session = new BrowserAnalysisSession({ workerUrl: '/worker.mjs', rootUri: 'file:///app', files: {
            '/app/anvil.yaml': JSON.stringify({ package_name: 'Main', db_schema: {
                people: { columns: [{ name: 'name', type: 'string' }] },
                contacts: { columns: [{ name: 'full name', type: 'string' }] },
            } }),
            '/app/client_code/main.py': source,
            '/app/server_code/main.py': source,
        } });
        try {
            const results = [];
            for (const environment of ['client', 'server']) {
                const textDocument = { uri: `file:///app/${environment}_code/main.py` };
                results.push((await session.query('textDocument/diagnostic', { textDocument })).result.items);
            }
            return results;
        } finally { session.dispose(); }
    });
    for (const diagnostics of result) {
        assert.deepEqual(diagnostics.map(item => [item.code, item.range.start.line]), [['invalid-argument-type', 6]]);
    }
}));

test('Users rows and configured Drive files follow current service metadata', () => withBrowser(async page => {
    const result = await page.evaluate(async () => {
        const { BrowserAnalysisSession } = await import('/session.mjs');
        const config = (column, file) => JSON.stringify({ package_name: 'TestApp', db_schema: {
            users: { columns: [{ name: column, type: 'string' }] },
        }, services: [
            { source: '/runtime/services/anvil/users', server_config: { user_table: 'users' } },
            { source: '/runtime/services/google', client_config: { app_files: [
                { python_name: file, mimeType: 'application/vnd.google-apps.spreadsheet', id: 'sheet' },
            ] } },
        ] });
        const userCode = 'import anvil.users\nuser = anvil.users.get_user()\nassert user is not None\nuser["nickname"].\nuser["';
        const session = new BrowserAnalysisSession({ workerUrl: '/worker.mjs', rootUri: 'file:///app', files: {
            '/app/anvil.yaml': config('nickname', 'budget'), '/app/client_code/__init__.py': '',
            '/app/client_code/user.py': userCode,
            '/app/client_code/drive.py': 'from anvil.google.drive import app_files\napp_files.\napp_files.budget.',
        } });
        const complete = async (name, line, character) => (await session.query('textDocument/completion', {
            textDocument: { uri: `file:///app/client_code/${name}.py` }, position: { line, character },
        })).result.items.map(item => item.label);
        try {
            const user = await complete('user', 3, 'user["nickname"].'.length);
            const keys = await complete('user', 4, 'user["'.length);
            const files = await complete('drive', 1, 'app_files.'.length);
            const sheet = await complete('drive', 2, 'app_files.budget.'.length);
            await session.updateFiles({ '/app/anvil.yaml': config('login_name', 'forecast') });
            return { user, keys, files, sheet, changedKeys: await complete('user', 4, 'user["'.length),
                changedFiles: await complete('drive', 1, 'app_files.'.length) };
        } finally { session.dispose(); }
    });
    assert(result.user.includes('upper'), 'Users return values lost their configured row type');
    assert(result.keys.includes('nickname'));
    assert(result.files.includes('budget'));
    assert(result.sheet.includes('worksheets'));
    assert(result.changedKeys.includes('login_name') && !result.changedKeys.includes('nickname'));
    assert(result.changedFiles.includes('forecast') && !result.changedFiles.includes('budget'));
}));

test('query combinators inherit enclosing table columns through aliases without leaking into values or unrelated calls', () => withBrowser(async page => {
    const result = await page.evaluate(async () => {
        const { BrowserAnalysisSession } = await import('/session.mjs');
        const session = new BrowserAnalysisSession({
            workerUrl: new URL('/worker.mjs', location.href).href, rootUri: 'file:///app',
            files: {
                '/app/anvil.yaml': JSON.stringify({ package_name: 'TestApp', db_schema: {
                    people: { columns: [{ name: 'name', type: 'string' }, { name: 'age', type: 'number' },
                        { name: 'café', type: 'string' }, { name: 'class', type: 'string' }] },
                } }),
                '/app/client_code/__init__.py': '', '/app/client_code/main.py': '',
            },
        });
        const prefix = 'from anvil.tables import app_tables\nfrom anvil.tables.query import any_of as either, all_of, not_, none_of\npeople = app_tables.people\n';
        const complete = async code => {
            const text = prefix + code.replace('¦', '');
            const before = (prefix + code).split('¦')[0].split('\n');
            await session.updateFiles({ '/app/client_code/main.py': text });
            const answer = await session.query('textDocument/completion', {
                textDocument: { uri: 'file:///app/client_code/main.py' },
                position: { line: before.length - 1, character: before.at(-1).length },
            });
            return answer.result.items.map(item => item.label);
        };
        try {
            const completions = {
                alias: await complete('people.search(either(na¦))'),
                nested: await complete('people.get(all_of(\n    either(¦)\n))'),
                used: await complete('people.search(either(name="Ada", ¦))'),
                value: await complete('people.search(either(name="A¦da"))'),
                unrelated: await complete('def either(**kwargs): pass\npeople.search(either(¦))'),
                wrapper: await complete('def wrap(**kwargs): pass\npeople.search(either(wrap(¦)))'),
                readable: await complete('people.client_readable(either(¦))'),
                writable: await complete('people.client_writable(either(¦))'),
                cascade: await complete('people.client_writable_cascade(either(¦))'),
                rowGet: await complete('people.add_row().get(either(¦))'),
                not: await complete('people.search(not_(¦))'),
                none: await complete('people.search(none_of(¦))'),
            };
            await complete('people.get(either(name="Ada", age=37), not_(age=42))¦');
            const diagnostics = await session.query('textDocument/diagnostic', {
                textDocument: { uri: 'file:///app/client_code/main.py' },
            });
            return { ...completions, diagnostics: diagnostics.result.items };
        } finally { session.dispose(); }
    });
    assert(result.alias.includes('name='));
    assert(result.nested.includes('age='));
    assert(result.used.includes('age='));
    assert(!result.used.includes('name='));
    assert(!result.alias.includes('age='));
    assert(result.nested.includes('café='));
    assert(!result.nested.includes('class='));
    for (const labels of [result.readable, result.writable, result.cascade, result.not, result.none]) assert(labels.includes('name='));
    for (const labels of [result.value, result.unrelated, result.wrapper, result.rowGet])
        assert(!labels.includes('name=') && !labels.includes('age='));
    assert.deepEqual(result.diagnostics, []);
}));

test('client and server queries use separate module ownership and never expose server imports to clients', () => withBrowser(async page => {
    const result = await page.evaluate(async () => {
        const { BrowserAnalysisSession } = await import('/session.mjs');
        const code = 'from TestApp.shared import value\nresult = value()\nresult.\n';
        const session = new BrowserAnalysisSession({
            workerUrl: new URL('/worker.mjs', location.href).href, rootUri: 'file:///app',
            files: {
                '/app/anvil.yaml': 'package_name: TestApp\n', '/app/client_code/__init__.py': '', '/app/server_code/__init__.py': '',
                '/app/client_code/shared.py': 'def value(): return "client"\n',
                '/app/server_code/shared.py': 'def value(): return 42\n',
                '/app/client_code/main.py': code, '/app/server_code/main.py': code,
                '/app/server_code/secrets.py': 'hidden = "secret"\n',
                '/app/client_code/illegal.py': 'from TestApp.secrets import hidden\nimport server_code.secrets\n',
                '/app/client_code/server_code/tool.py': 'from TestApp.secrets import hidden\n',
                '/app/server_code/api.py': 'import anvil.server\nanvil.server.call("unknown")\n',
                '/app/client_code/choice/__init__.py': 'def choose(): return "client package"\n',
                '/app/server_code/choice.py': 'def choose(): return 42\n',
                '/app/server_code/use_choice.py': 'from TestApp.choice import choose\nchoose().\n',
            },
        });
        const query = (kind, method, position) => session.query(method, { textDocument: { uri: `file:///app/${kind}_code/main.py` }, position });
        try {
            const client = await query('client', 'textDocument/completion', { line: 2, character: 7 });
            const server = await query('server', 'textDocument/completion', { line: 2, character: 7 });
            const definition = await query('server', 'textDocument/definition', { line: 1, character: 11 });
            const stub = await session.query('textDocument/definition', { textDocument: { uri: 'file:///app/server_code/api.py' }, position: { line: 1, character: 15 } });
            const clientAgain = await query('client', 'textDocument/completion', { line: 2, character: 7 });
            const stubSource = await session.query('anvil/readSource', { uri: stub.result[0].uri });
            const illegal = await session.query('textDocument/diagnostic', { textDocument: { uri: 'file:///app/client_code/illegal.py' } });
            const nested = await session.query('textDocument/diagnostic', { textDocument: { uri: 'file:///app/client_code/server_code/tool.py' } });
            const choice = await session.query('textDocument/completion', { textDocument: { uri: 'file:///app/server_code/use_choice.py' }, position: { line: 1, character: 9 } });
            return { client, server, definition, clientAgain, illegal, nested, stubSource, choice };
        } finally { session.dispose(); }
    });
    assert(result.client.result.items.some(item => item.label === 'upper'));
    assert(result.server.result.items.some(item => item.label === 'bit_length'));
    assert(!result.server.result.items.some(item => item.label === 'upper'));
    assert.equal(result.definition.result[0].uri, 'file:///app/server_code/shared.py');
    assert(result.clientAgain.result.items.some(item => item.label === 'upper'));
    assert.deepEqual(result.illegal.result.items.filter(item => item.code === 'unresolved-import').map(item => item.range.start.line), [0, 1]);
    assert(result.nested.result.items.some(item => item.code === 'unresolved-import'));
    assert(result.stubSource.result.text.includes('def call('));
    assert.equal(result.stubSource.result.readOnly, true);
    assert(result.choice.result.items.some(item => item.label === 'bit_length'));
    assert(!result.choice.result.items.some(item => item.label === 'upper'));
}));

test('row-model discovery follows source changes without retaining a removed model registration', () => withBrowser(async page => {
    const result = await page.evaluate(async () => {
        const { BrowserAnalysisSession } = await import('/session.mjs');
        const session = new BrowserAnalysisSession({
            workerUrl: new URL('/worker.mjs', location.href).href, rootUri: 'file:///app',
            files: {
                '/app/anvil.yaml': JSON.stringify({ package_name: 'TestApp', db_schema: { people: { columns: [{ name: 'name', type: 'string' }] } } }),
                '/app/client_code/__init__.py': '',
                '/app/client_code/models/__init__.py': 'from anvil.tables import app_tables\nclass Person(app_tables.people.Row):\n    def display(self) -> str: return self["name"]\n',
                '/app/client_code/Form1/__init__.py': 'from ._anvil_designer import Form1Template\nclass Form1(Form1Template): pass\n',
                '/app/client_code/Form1/form_template.yaml': JSON.stringify({ container: { type: 'ColumnPanel' }, components: [], item_type: { table_name: 'people' } }),
                '/app/client_code/main.py': 'from anvil.tables import app_tables\nrow = app_tables.people.get()\nassert row is not None\nrow.\nrow["name"].\nrow[""]\n',
                '/app/server_code/models.py': 'server_marker = 42\n',
                '/app/server_code/probe.py': 'from anvil.tables import app_tables\nrow = app_tables.people.get()\nrow["name"].\n',
            },
        });
        const textDocument = { uri: 'file:///app/client_code/main.py' };
        try {
            await session.setContext({ kind: 'binding', id: 'item-model', formUri: 'file:///app/client_code/Form1/__init__.py', code: 'self.item.' });
            const binding = await session.queryContext('item-model', 'textDocument/completion', { position: { line: 0, character: 10 } });
            const model = await session.query('textDocument/completion', { textDocument, position: { line: 3, character: 4 } });
            const keys = await session.query('textDocument/completion', { textDocument, position: { line: 5, character: 5 } });
            const server = await session.query('textDocument/completion', { textDocument: { uri: 'file:///app/server_code/probe.py' }, position: { line: 2, character: 12 } });
            await session.updateFiles({ '/app/client_code/models/__init__.py': 'from anvil.tables import app_tables\nclass Person(app_tables.people.Row, attrs=True):\n    def display(self) -> str: return self.name\n' });
            const attrs = await session.query('textDocument/completion', { textDocument, position: { line: 3, character: 4 } });
            await session.updateFiles({ '/app/client_code/models/__init__.py': 'class Person: pass\n' });
            const plain = await session.query('textDocument/completion', { textDocument, position: { line: 3, character: 4 } });
            const value = await session.query('textDocument/completion', { textDocument, position: { line: 4, character: 12 } });
            const plainBinding = await session.queryContext('item-model', 'textDocument/completion', { position: { line: 0, character: 10 } });
            return { model, attrs, plain, value, keys, server, binding, plainBinding };
        } finally { session.dispose(); }
    });
    assert(result.model.result.items.some(item => item.label === 'display'), JSON.stringify(result.model));
    assert(!result.model.result.items.some(item => item.label === 'name'), 'Column attributes require attrs=True');
    assert(result.attrs.result.items.some(item => item.label === 'name'), 'attrs=True columns must be offered after a model edit');
    assert(result.binding.result.items.some(item => item.label === 'display'), 'Configured Form item lost its row-model methods');
    assert(!result.plainBinding.result.items.some(item => item.label === 'display'));
    assert(result.keys.result.items.some(item => item.label === 'name'));
    assert(result.server.result.items.some(item => item.label === 'upper'));
    assert(!result.plain.result.items.some(item => item.label === 'display'));
    assert(result.value.result.items.some(item => item.label === 'upper'));
}));

test('file outline and project symbols use current original sources and UTF-16 ranges', () => withBrowser(async page => {
    const result = await page.evaluate(async () => {
        const { BrowserAnalysisSession } = await import('/session.mjs');
        const session = new BrowserAnalysisSession({
            workerUrl: new URL('/worker.mjs', location.href).href, rootUri: 'file:///app',
            files: {
                '/app/library.py': 'emoji = "😀"; answer = 42\nclass Greeter:\n    def greet(self): return "Hello"\n',
                '/app/other.py': '# legacy line endings\rdef build(): return 42\r',
            },
        });
        try {
            const outline = await session.query('textDocument/documentSymbol', { textDocument: { uri: 'file:///app/library.py' } });
            const symbols = await session.query('workspace/symbol', { query: 'greet' });
            const legacyLines = await session.query('textDocument/documentSymbol', { textDocument: { uri: 'file:///app/other.py' } });
            await session.updateFiles({ '/app/library.py': 'class Greeter:\n    def salute(self): return "Hello"\n' });
            const changed = await session.query('workspace/symbol', { query: 'salute' });
            const removed = await session.query('workspace/symbol', { query: 'answer' });
            return { outline, symbols, legacyLines, changed, removed };
        } finally { session.dispose(); }
    });
    assert.equal(result.outline.result.find(symbol => symbol.name === 'answer').location.range.start.character, 14);
    assert(result.outline.result.some(symbol => symbol.name === 'Greeter' && symbol.kind === 5));
    assert(result.symbols.result.some(symbol => symbol.name === 'greet' && symbol.containerName === 'Greeter'));
    assert.deepEqual(result.legacyLines.result[0].location.range.start, { line: 1, character: 4 });
    assert.equal(result.changed.result[0].location.uri, 'file:///app/library.py');
    assert.equal(result.changed.result[0].name, 'salute');
    assert.deepEqual(result.removed.result, []);
}));

test('Designer and endpoint metadata follows semantic decorator aliases and unsaved Form code', () => withBrowser(async page => {
    const result = await page.evaluate(async () => {
        const { BrowserAnalysisSession } = await import('/session.mjs');
        const uri = 'file:///app/client_code/Form1/__init__.py';
        const code = 'from ._anvil_designer import WelcomeTemplate\nfrom anvil import handle as on\nclass Helper(WelcomeTemplate):\n    pass\nclass Welcome(Helper):\n    @on("button_1", "click")\n    def pressed(self, **event_args):\n        pass\n    # trailing class comment\nafter = True\n'.replaceAll('\n', '\r');
        const session = new BrowserAnalysisSession({
            workerUrl: new URL('/worker.mjs', location.href).href, rootUri: 'file:///app',
            files: {
                '/app/anvil.yaml': 'package_name: TestApp\n', '/app/client_code/__init__.py': '',
                '/app/client_code/Form1/__init__.py': code,
                '/app/client_code/Form1/form_template.yaml': 'class_name: pkg.Welcome\ncontainer: {type: ColumnPanel}\ncomponents: [{name: button_1, type: Button}]\n',
                '/app/server_code/api.py': 'from anvil.server import http_endpoint as endpoint, route, background_task\nimport anvil.email as mail\nendpoint_alias = endpoint\n@endpoint_alias("/greet")\ndef greet(): return "Hello"\n@route(path=dynamic_path)\ndef dynamic(): pass\n@mail.handle_message\ndef message(**args): pass\n@background_task\ndef refresh(): return "done"\n@background_task("nightly")\ndef run(): pass\ndef http_endpoint(path): return lambda fn: fn\n@http_endpoint("/fake")\ndef unrelated(): pass\n',
            },
        });
        try {
            const initial = await session.query('anvil/getItemMetadata', { uri });
            await session.openDocument(uri, code.replace('def pressed', 'def clicked').replace('        pass', '        café'));
            const overlay = await session.query('anvil/getItemMetadata', { uri });
            await session.closeDocument(uri);
            const batch = await session.query('anvil/getAppMetadata', { uris: [uri, 'file:///app/server_code/api.py'] });
            const tasks = await session.query('anvil/getBackgroundTasks', {});
            return { initial, overlay, batch, tasks };
        } finally { session.dispose(); }
    });
    assert.equal(result.initial.result.formClassName, 'Welcome');
    assert.equal(result.initial.result.formClassBodyEndLine, 9);
    assert.deepEqual(result.initial.result.eventHandlers, [{ component: 'button_1', event: 'click', handler: 'pressed' }]);
    assert.equal(result.overlay.result.eventHandlers[0].handler, 'clicked');
    assert.equal(result.batch.result[0].eventHandlers[0].handler, 'pressed');
    assert.deepEqual(result.batch.result[1].httpEndpoints, [{ name: 'greet', path: '/greet' }]);
    assert.equal(result.batch.result[1].routes[0].name, 'dynamic');
    assert.equal(result.batch.result[1].routes[0].path, undefined);
    assert.deepEqual(result.batch.result[1].emailEndpoints, [{ name: 'message' }]);
    assert.deepEqual(result.tasks.result, [{ name: 'refresh', filePath: '/app/server_code/api.py' }, { name: 'nightly', filePath: '/app/server_code/api.py' }]);
}));

test('REPL contexts preserve static locals, runtime isolation and completion generations', () => withBrowser(async page => {
    const result = await page.evaluate(async () => {
        const { BrowserAnalysisSession } = await import('/session.mjs');
        const session = new BrowserAnalysisSession({
            workerUrl: new URL('/worker.mjs', location.href).href, rootUri: 'file:///app',
            files: {
                '/app/anvil.yaml': 'package_name: TestApp\n',
                '/app/client_code/__init__.py': '',
                '/app/server_code/service.py': 'def number(): return 42\n',
                '/app/client_code/_anvil_context_1.py': 'original = 42\n',
            },
        });
        const context = { kind: 'repl', id: 'console', isServer: true,
            previousCode: 'from .service import number\nvalue = number()\nname = "Ada"\n', code: 'name.up' };
        const complete = character => session.queryContext(context.id, 'textDocument/completion', { position: { line: 0, character } });
        try {
            await session.setContext(context);
            const initial = await complete(7);
            const upper = initial.result.items.find(item => item.label === 'upper');
            if (!upper) throw new Error('Missing upper in REPL context');
            const resolved = await session.queryContext(context.id, 'completionItem/resolve', upper);
            await session.updateFiles({ '/app/client_code/_anvil_context_2.py': 'original = 43\n' });
            const moved = await complete(7);
            const collision = await session.query('textDocument/documentSymbol', { textDocument: { uri: 'file:///app/client_code/_anvil_context_2.py' } });
            const movedItem = await session.queryContext(context.id, 'completionItem/resolve', upper).catch(error => error.name);
            await session.setContext({ ...context, code: 'value.bi' });
            const server = await complete(8);
            const item = server.result.items.find(item => item.label === 'bit_length');
            if (!item) throw new Error('Server REPL did not see its service');
            await session.setContext({ ...context, isServer: false, code: 'value.bi' });
            const client = await complete(8);
            const obsolete = await session.queryContext(context.id, 'completionItem/resolve', item).catch(error => error.name);
            await session.closeContext(context.id);
            await session.setContext({ ...context, code: 'value.bi' });
            const reopened = await session.queryContext(context.id, 'completionItem/resolve', item).catch(error => error.name);
            return { resolved, moved, collision, movedItem, server, client, obsolete, reopened };
        } finally { session.dispose(); }
    });
    assert.equal(result.resolved.result.label, 'upper');
    assert(result.moved.result.items.some(item => item.label === 'upper'));
    assert.deepEqual(result.collision.result.map(symbol => symbol.name), ['original']);
    assert.equal(result.movedItem, 'AbortError');
    assert(result.server.result.items.some(item => item.label === 'bit_length'));
    assert(!result.client.result.items.some(item => item.label === 'bit_length'));
    assert.equal(result.obsolete, 'AbortError');
    assert.equal(result.reopened, 'AbortError');
}));

test('REPL callback completions preserve reference insertion metadata', () => withBrowser(async page => {
    const item = await page.evaluate(async () => {
        const { BrowserAnalysisSession } = await import('/session.mjs');
        const session = new BrowserAnalysisSession({ workerUrl: '/worker.mjs', rootUri: 'file:///app', files: {
            '/app/anvil.yaml': 'package_name: Main\n', '/app/client_code/main.py': '',
        } });
        try {
            await session.setContext({ kind: 'repl', id: 'console', isServer: false,
                previousCode: 'from typing import Callable\ndef register(callback: Callable[[], str]): pass\ndef handler() -> str: return "ok"\n',
                code: 'register(han' });
            const { result } = await session.queryContext('console', 'textDocument/completion', { position: { line: 0, character: 12 } });
            return result.items.find(item => item.label === 'handler');
        } finally { session.dispose(); }
    });
    assert(item, 'The REPL must offer the function from its history');
    assert.equal(item.data?.insertParentheses, false, JSON.stringify(item));
}));

test('binding contexts follow declared Form ownership and keep edits inside the expression', () => withBrowser(async page => {
    const result = await page.evaluate(async () => {
        const { BrowserAnalysisSession } = await import('/session.mjs');
        const session = new BrowserAnalysisSession({
            workerUrl: new URL('/worker.mjs', location.href).href, rootUri: 'file:///app', files: {},
        });
        const formUri = 'file:///app/client_code/Form1/__init__.py';
        const code = name => `from ._anvil_designer import ${name}Template\nclass ${name}(${name}Template):\n    def greet(self, name: str) -> str: return name\n`;
        const template = (name, button) => JSON.stringify({ class_name: `pkg.${name}`, container: { type: 'ColumnPanel' },
            item_type: { table_name: 'people' }, components: [{ name: button, type: 'Button' }] });
        const context = { kind: 'binding', id: 'binding', formUri, code: 'self.button_1.' };
        const complete = character => session.queryContext(context.id, 'textDocument/completion', { position: { line: 0, character } });
        try {
            const files = session.updateFiles({
                '/app/anvil.yaml': JSON.stringify({ package_name: 'TestApp', db_schema: {
                    people: { columns: [{ name: 'first name', type: 'string' }] },
                } }), '/app/client_code/__init__.py': '',
                '/app/client_code/Form1/__init__.py': code('Fancy'),
                '/app/client_code/Form1/form_template.yaml': template('Fancy', 'button_1'),
            });
            const opened = session.setContext(context);
            await Promise.all([files, opened]);
            const before = await complete(14);
            const property = before.result.items.find(item => item.label === 'text');
            const propertyDocs = await session.queryContext(context.id, 'completionItem/resolve', property);
            await session.setContext({ ...context, code: 'self.item["first n"]' });
            const obsolete = await session.queryContext(context.id, 'completionItem/resolve', property).catch(error => error.name);
            const keys = await complete(18);
            if (!keys.result.items.length) throw new Error('Missing binding row keys: ' + JSON.stringify({ before, keys }));
            const resolved = await session.queryContext(context.id, 'completionItem/resolve', keys.result.items[0]);
            await session.setContext({ ...context, code: 'self.greet(' });
            const signature = await session.queryContext(context.id, 'textDocument/signatureHelp', { position: { line: 0, character: 11 } });
            await session.setContext({ ...context, code: 'self.' });
            await session.updateFiles({
                '/app/client_code/Form1/__init__.py': code('Fancy2'),
                '/app/client_code/Form1/form_template.yaml': template('Fancy2', 'fresh_button'),
            });
            const after = await complete(5);
            await session.updateFiles({ '/app/client_code/Form1/__init__.py': null });
            const unavailable = await complete(5).catch(error => error.message);
            await session.updateFiles({ '/app/client_code/Form1/__init__.py': code('Fancy2') });
            const restored = await complete(5);
            return { before, propertyDocs, obsolete, keys, resolved, signature, after, unavailable, restored };
        } finally { session.dispose(); }
    });
    assert(result.before.result.items.some(item => item.label === 'text'), JSON.stringify(result.before));
    assert.match(result.propertyDocs.result.documentation.value, /\[Anvil Docs\]\(https:\/\/anvil\.works\/docs\/components\/standard-components\/basic#button\)/);
    assert.equal(result.obsolete, 'AbortError');
    assert.deepEqual(result.keys.result.items[0].textEdit, {
        range: { start: { line: 0, character: 11 }, end: { line: 0, character: 18 } }, newText: 'first name',
    });
    assert.deepEqual(result.resolved.result.textEdit, result.keys.result.items[0].textEdit);
    assert(result.signature.result.signatures[0].label.includes('name: str'));
    assert(result.after.result.items.some(item => item.label === 'fresh_button'));
    assert(!result.after.result.items.some(item => item.label === 'button_1'));
    assert.match(result.unavailable, /unavailable/);
    assert(result.restored.result.items.some(item => item.label === 'fresh_button'));
}));

test('contexts refuse completion and rename edits to generated history or imports', () => withBrowser(async page => {
    const result = await page.evaluate(async () => {
        const { BrowserAnalysisSession } = await import('/session.mjs');
        const session = new BrowserAnalysisSession({
            workerUrl: new URL('/worker.mjs', location.href).href, rootUri: 'file:///app',
            files: {
                '/app/anvil.yaml': 'package_name: TestApp\n', '/app/client_code/__init__.py': '',
                '/app/client_code/library.py': 'class Greeting: pass\ndef greet(): return "Hello"\n',
                '/app/client_code/main.py': 'Gree\n',
            },
        });
        try {
            const source = await session.query('textDocument/completion', { textDocument: { uri: 'file:///app/client_code/main.py' }, position: { line: 0, character: 4 } });
            await session.setContext({ kind: 'repl', id: 'console', isServer: false, previousCode: 'history = 1\n', code: 'Gree' });
            const input = await session.queryContext('console', 'textDocument/completion', { position: { line: 0, character: 4 } });
            await session.setContext({ kind: 'repl', id: 'console', isServer: false, previousCode: 'from .library import greet\n', code: 'greet()' });
            const rename = { textDocument: { uri: 'file:///app/client_code/library.py' }, position: { line: 1, character: 5 }, newName: 'salute' };
            const refused = await session.query('textDocument/rename', rename).catch(error => error.message);
            await session.closeContext('console');
            const closed = await session.query('textDocument/rename', rename);
            return { source, input, refused, closed };
        } finally { session.dispose(); }
    });
    assert(result.source.result.items.find(item => item.label === 'Greeting')?.additionalTextEdits?.length);
    assert(!result.input.result.items.some(item => item.label === 'Greeting'));
    assert.match(result.refused, /read.only/);
    assert.equal(result.closed.result.documentChanges.length, 1);
    assert.equal(result.closed.result.documentChanges[0].textDocument.uri, 'file:///app/client_code/library.py');
}));

test('gendoc APIs expose drawing state, Maps data and HTTP object members', () => withBrowser(async page => {
    const probes = [
        ['client', 'anvil.Canvas().', ['fill_style', 'line_width', 'text_align']],
        ['client', 'anvil.RichText().', ['clear']],
        ['client', 'anvil.GoogleMap.Symbol().', ['strokeColor', 'path', 'rotation']],
        ['client', 'anvil.GoogleMap.Symbol(', ['stroke_color=', 'stroke_opacity=', 'stroke_weight=']],
        ['client', 'anvil.GoogleMap.geocode(', ['address=', 'location=']],
        ['client', 'anvil.GoogleMap().map_data.override_style(anvil.GoogleMap.Data.Feature(), ', ['clickable=', 'fillColor=', 'stroke_weight=']],
        ['client', 'anvil.GoogleMap.Animation.', ['DROP', 'BOUNCE']],
        ['client', 'anvil.GoogleMap().map_data.', ['add_geo_json', 'get_feature_by_id', 'style']],
        ['client', 'anvil.GoogleMap().map_data.add(', ['geometry=', 'id=', 'properties=']],
        ['client', 'anvil.GoogleMap.Data.LineString([anvil.GoogleMap.LatLng(0, 0)]).get_at(0).', ['lat', 'lng']],
        ['client', 'anvil.GoogleMap.geocode(address="Cambridge")[0].geometry.location.', ['lat', 'lng']],
        ['server', 'anvil.server.HttpResponse().', ['status', 'body', 'headers']],
        ['server', 'anvil.server.HttpResponse().headers.', ['add', 'copy', 'clear']],
        ['server', 'anvil.server.request.', ['origin', 'user']],
        ['server', 'anvil.server.CallContext.ClientInfo().', ['ip', 'type', 'location']],
    ];
    const results = await page.evaluate(async probes => {
        const { BrowserAnalysisSession } = await import('/session.mjs');
        const session = new BrowserAnalysisSession({
            workerUrl: '/worker.mjs', rootUri: 'file:///app', files: {
                '/app/anvil.yaml': 'package_name: TestApp\n',
                '/app/client_code/probe.py': '', '/app/server_code/probe.py': '',
            },
        });
        try {
            const results = [];
            for (const [environment, expression] of probes) {
                const uri = `file:///app/${environment}_code/probe.py`;
                const code = `import anvil\nimport anvil.server\n${expression}`;
                await session.openDocument(uri, code);
                const completion = await session.query('textDocument/completion', {
                    textDocument: { uri }, position: { line: 2, character: expression.length },
                });
                results.push(completion.result.items.map(item => item.label));
            }
            const uri = 'file:///app/client_code/probe.py';
            const code = [
                'import anvil',
                'canvas = anvil.Canvas()',
                'canvas.line_width = 2',
                'point = anvil.GoogleMap.LatLng(0, 0)',
                'feature = anvil.GoogleMap().map_data.add(geometry=point, properties={"name": "A"})',
                'feature.geometry = point',
                'symbol = anvil.GoogleMap.Symbol(stroke_opacity=0.5, stroke_weight=2)',
                'anvil.GoogleMap().map_data.override_style(feature, fillColor="red", stroke_weight=2)',
                'canvas.line_width = "wide"',
                'symbol.stroke_opacity = "opaque"',
            ].join('\n');
            await session.openDocument(uri, code);
            const diagnostics = await session.query('textDocument/diagnostic', { textDocument: { uri } });
            return { results, diagnostics: diagnostics.result.items };
        } finally { session.dispose(); }
    }, probes);
    probes.forEach(([, expression, expected], i) => {
        for (const member of expected) assert(results.results[i].includes(member), `${expression} missing ${member}`);
    });
    assert.deepEqual(results.diagnostics.filter(item => item.severity === 1).map(item => item.range.start.line), [8, 9]);
}));

test('HTML Form structure and tag-specific DOM types refresh with YAML taking precedence', () => withBrowser(async page => {
    const result = await page.evaluate(async () => {
        const { BrowserAnalysisSession } = await import('/session.mjs');
        const html = tag => `---\nclass_name: Home\n---\n<anvil-form container="HtmlComponent"><${tag} anvil:dom-node="email"></${tag}><anvil-component name="html_button" type="Button"></anvil-component></anvil-form>`;
        const session = new BrowserAnalysisSession({
            workerUrl: new URL('/worker.mjs', location.href).href, rootUri: 'file:///app',
            files: {
                '/app/anvil.yaml': 'package_name: TestApp\n', '/app/client_code/__init__.py': '',
                '/app/client_code/Home/__init__.py': 'from ._anvil_designer import HomeTemplate\nclass Home(HomeTemplate):\n    def probe(self):\n        self.dom_nodes["email"].\n',
                '/app/client_code/Home/form_template.html': html('input'),
            },
        });
        const textDocument = { uri: 'file:///app/client_code/Home/__init__.py' };
        const dom = () => session.query('textDocument/completion', { textDocument, position: { line: 3, character: 32 } });
        try {
            const input = await dom();
            await session.updateFiles({ '/app/client_code/Home/form_template.yaml': JSON.stringify({ class_name: 'Home', save_as_html: true,
                serialized_html: '<anvil-form container="HtmlTemplate"><input anvil:dom-node="email"></anvil-form>', container: { type: 'HtmlTemplate', properties: { html: '<textarea anvil-name="email"></textarea>' } } }) });
            const cached = await dom();
            await session.updateFiles({ '/app/client_code/Home/form_template.yaml': null, '/app/client_code/Home/form_template.html': html('textarea') });
            const textarea = await dom();
            await session.updateFiles({ '/app/client_code/Home/form_template.html': html('button') });
            const button = await dom();
            await session.updateFiles({ '/app/client_code/Home/form_template.yaml': 'class_name: Home\ncontainer: {type: ColumnPanel}\ncomponents: [{name: yaml_button, type: Button}]\n' });
            await session.openDocument(textDocument.uri, 'from ._anvil_designer import HomeTemplate\nclass Home(HomeTemplate):\n    def probe(self):\n        self.\n');
            const yaml = await session.query('textDocument/completion', { textDocument, position: { line: 3, character: 13 } });
            return { input, cached, textarea, button, yaml };
        } finally { session.dispose(); }
    });
    assert(result.input.result.items.some(item => item.label === 'checked'));
    assert(result.input.result.items.some(item => item.label === 'focus'));
    assert(result.cached.result.items.some(item => item.label === 'checked'));
    assert(!result.cached.result.items.some(item => item.label === 'rows'));
    assert(result.textarea.result.items.some(item => item.label === 'rows'));
    assert(!result.textarea.result.items.some(item => item.label === 'checked'));
    assert(result.button.result.items.some(item => item.label === 'formAction'));
    assert(result.button.result.items.some(item => item.label === 'disabled'));
    assert(!result.button.result.items.some(item => item.label === 'rows'));
    assert(!result.button.result.items.some(item => item.label === 'checked'));
    assert(result.yaml.result.items.some(item => item.label === 'yaml_button'));
    assert(!result.yaml.result.items.some(item => item.label === 'html_button'));
}));

test('JS components refresh Designer and Python namespaces without shadowing unsaved package code', () => withBrowser(async page => {
    const result = await page.evaluate(async () => {
        const { BrowserAnalysisSession } = await import('/session.mjs');
        const metadata = property => JSON.stringify({ packages: { TestApp: '/app/client_code', Mantine: '/app/.anvil/deps/JSDEP/client_code' },
            components: [
                ...['TestApp.Tools.Button', 'TestApp.Tools.BoutonÉ', 'Mantine.Button'].map(name => ({ name,
                    properties: [{ name: property }, { name: 'café' }], methods: [{ name: 'focus', args: [] }, { name: 'démarrer', args: [] },
                        { name: 'choose', args: [{ name: 'label' }, { name: 'count', type: 'keyword', optional: true }] }] })),
                { name: 'Mantine.Panel', container: true, layoutProperties: [{ name: 'gap' }] },
            ] });
        const session = new BrowserAnalysisSession({
            workerUrl: new URL('/worker.mjs', location.href).href, rootUri: 'file:///app',
            files: {
                '/app/anvil.yaml': 'package_name: TestApp\ndependencies: [{app_id: JSDEP}]\n',
                '/app/client_code/__init__.py': '', '/app/client_code/Tools/__init__.py': 'def greet(): return "Hello"\n',
                '/app/server_code/Tools/Button.py': 'def server_only(): return 42\n',
                '/app/server_code/probe.py': 'from .Tools import Button\nButton.\n',
                '/app/client_code/main.py': 'from TestApp import Tools\nfrom Mantine.Button import Button\nTools.Button.Button().\nTools.greet().\nButton().\nTools.BoutonÉ.BoutonÉ().\n',
                '/app/client_code/Home/__init__.py': 'from ._anvil_designer import HomeTemplate\nclass Home(HomeTemplate):\n    def probe(self):\n        self.button_1.\n',
                '/app/client_code/Home/form_template.yaml': 'container: {type: ColumnPanel}\ncomponents: [{name: button_1, type: "form:JSDEP:Button"}]\n',
                '/app/.anvil/deps/JSDEP/anvil.yaml': 'package_name: Mantine\n',
                '/app/.anvil/deps/JSDEP/client_code/__init__.py': '',
                '/app/.anvil/js-components.json': metadata('text'),
            },
        });
        const textDocument = { uri: 'file:///app/client_code/main.py' };
        const complete = (line, character) => session.query('textDocument/completion', { textDocument, position: { line, character } });
        try {
            await session.openDocument('file:///app/client_code/Tools/__init__.py', 'def greet(): return 1\n');
            const nested = await complete(2, 22);
            const python = await complete(3, 14);
            const direct = await complete(4, 9);
            const unicode = await complete(5, 24);
            const server = await session.query('textDocument/completion', { textDocument: { uri: 'file:///app/server_code/probe.py' }, position: { line: 1, character: 7 } });
            const form = await session.query('textDocument/completion', { textDocument: { uri: 'file:///app/client_code/Home/__init__.py' }, position: { line: 3, character: 22 } });
            const references = await session.query('textDocument/references', { textDocument, position: { line: 0, character: 22 } });
            const namespaceRename = await session.query('textDocument/rename', { textDocument, position: { line: 0, character: 22 }, newName: 'Utilities' }).catch(error => error.message);
            const definitions = await session.query('textDocument/definition', { textDocument, position: { line: 4, character: 2 } });
            const source = definitions.result.length && await session.query('anvil/readSource', { uri: definitions.result[0].uri });
            const refused = await session.query('textDocument/rename', { textDocument, position: { line: 4, character: 2 }, newName: 'Changed' }).catch(error => error.message);
            const signature = async (imports, expression) => {
                await session.openDocument(textDocument.uri, imports + '\n' + expression);
                return session.query('textDocument/signatureHelp', { textDocument, position: { line: 1, character: expression.length } });
            };
            const constructor = await signature('from Mantine.Button import Button', 'Button(');
            const method = await signature('from Mantine.Button import Button', 'Button().choose("label", ');
            const layout = await signature('from Mantine.Panel import Panel', 'Panel().add_component(None, ');
            await session.closeDocument(textDocument.uri);
            await session.updateFiles({ '/app/.anvil/js-components.json': metadata('color') });
            const changed = await complete(2, 22);
            await session.updateFiles({ '/app/.anvil/js-components.json': null });
            const removed = await complete(2, 22);
            const original = await session.query('anvil/readSource', { uri: 'file:///app/client_code/Tools/__init__.py' });
            return { nested, python, direct, unicode, server, form, references, namespaceRename, definitions, source, refused, constructor, method, layout, changed, removed, original };
        } finally { session.dispose(); }
    });
    for (const key of ['nested', 'direct', 'unicode', 'form']) {
        assert(result[key].result.items.some(item => item.label === 'text'), key);
        assert(result[key].result.items.some(item => item.label === 'focus'), key);
        assert(result[key].result.items.some(item => item.label === 'café'), key);
        assert(result[key].result.items.some(item => item.label === 'démarrer'), key);
    }
    assert(result.server.result.items.some(item => item.label === 'server_only'));
    assert(!result.server.result.items.some(item => item.label === 'Button'));
    assert(result.python.result.items.some(item => item.label === 'bit_length'));
    assert(!result.python.result.items.some(item => item.label === 'upper'));
    assert(result.references.result.some(target => target.uri.startsWith('file:///app/.anvil/analysis/')));
    assert(!result.references.result.some(target => target.uri === 'file:///app/client_code/__init__.py'));
    assert.match(result.namespaceRename, /read.only/);
    assert.match(result.definitions.result[0].uri, /\.anvil\/.*\.pyi$/);
    assert(result.source.result.text.includes('class Button'));
    assert.equal(result.source.result.readOnly, true);
    assert.match(result.refused, /read.only/);
    assert(result.constructor.result.signatures[0].label.includes('café'));
    assert(result.method.result.signatures[0].label.includes('count'));
    assert(result.layout.result.signatures[0].label.includes('gap'));
    assert(result.changed.result.items.some(item => item.label === 'color'));
    assert(!result.changed.result.items.some(item => item.label === 'text'));
    assert(!result.removed.result.items.some(item => item.label === 'color'));
    assert.equal(result.original.result.text, 'def greet(): return 1\n');
}));

test('RPC and task name completion follows semantic aliases and current server registrations', () => withBrowser(async page => {
    const result = await page.evaluate(async () => {
        const { BrowserAnalysisSession } = await import('/session.mjs');
        const server = 'from anvil.server import callable as expose, background_task as task\nregister = expose\n@register(fn_or_name="public_name")\ndef implementation(): return "Hello"\n@task(fn_or_name="nightly")\ndef job(): pass\ndef callable(name): return lambda fn: fn\n@callable("fake")\ndef unrelated(): pass\n@expose("unrelated_rpc")\ndef another(): pass\n@task("cleanup")\ndef clean(): pass\n';
        const session = new BrowserAnalysisSession({
            workerUrl: new URL('/worker.mjs', location.href).href, rootUri: 'file:///app',
            files: {
                '/app/anvil.yaml': 'package_name: TestApp\n', '/app/client_code/__init__.py': '',
                '/app/server_code/api.py': server,
                '/app/.anvil/js-components.json': JSON.stringify({ packages: { TestApp: '/app/client_code' }, components: [{ name: 'TestApp.anvil.server', methods: [{ name: 'call', args: [{ name: 'name' }] }] }] }),
                '/app/client_code/spoof.py': 'from TestApp.anvil.server import server\nserver().call("pub")\n',
                '/app/client_code/main.py': 'from anvil.server import call as invoke, launch_background_task as launch\nemoji = "😀"; invoke("pub")\nlaunch("ni")\ndef call(name): return name\ncall("pub")\n',
            },
        });
        const textDocument = { uri: 'file:///app/client_code/main.py' };
        const complete = (line, character) => session.query('textDocument/completion', { textDocument, position: { line, character } });
        try {
            const call = await complete(1, 25);
            const task = await complete(2, 10);
            const taskList = await session.query('anvil/getBackgroundTasks', {});
            const unrelated = await complete(4, 9);
            const spoof = await session.query('textDocument/completion', { textDocument: { uri: 'file:///app/client_code/spoof.py' }, position: { line: 1, character: 18 } });
            await session.openDocument('file:///app/server_code/api.py', server.replace('public_name', 'public_fresh'));
            const edited = await complete(1, 25);
            await session.closeDocument('file:///app/server_code/api.py');
            const restored = await complete(1, 25);
            await session.openDocument(textDocument.uri, 'from anvil.server import call as invoke\ninvoke("pub');
            const unclosed = await complete(1, 11);
            await session.changeDocument(textDocument.uri, 'from anvil.server import call as invoke\ninvoke(r"pub")');
            const raw = await complete(1, 12);
            await session.changeDocument(textDocument.uri, 'from anvil.server import call as invoke, launch_background_task as launch\ninvoke(  )\nlaunch(\n');
            const emptyCall = await complete(1, 9);
            const emptyTask = await complete(2, 7);
            await session.changeDocument(textDocument.uri, 'from anvil.server import call as invoke\nrpc_name = "public_name"\ninvoke(  # explain the call\n)');
            const comment = await complete(2, 9);
            await session.closeDocument(textDocument.uri);
            const client = await session.query('textDocument/diagnostic', { textDocument });
            return { call, task, taskList, unrelated, spoof, edited, restored, unclosed, raw, emptyCall, emptyTask, comment, client };
        } finally { session.dispose(); }
    });
    const item = result.call.result.items.find(item => item.label === 'public_name');
    assert(item, JSON.stringify(result.call));
    assert.deepEqual(result.call.result.items.map(item => item.label), ['public_name']);
    assert.deepEqual(result.task.result.items.map(item => item.label), ['nightly']);
    assert.deepEqual(item.textEdit, { range: { start: { line: 1, character: 22 }, end: { line: 1, character: 25 } }, newText: 'public_name' });
    assert(result.task.result.items.some(item => item.label === 'nightly'));
    assert(result.taskList.result.some(item => item.name === 'nightly'));
    assert(!result.call.result.items.some(item => item.label === 'fake'));
    assert(!result.unrelated.result.items.some(item => item.label === 'public_name'));
    assert(!result.spoof.result.items.some(item => item.label === 'public_name'));
    assert(result.edited.result.items.some(item => item.label === 'public_fresh'));
    assert(!result.edited.result.items.some(item => item.label === 'public_name'));
    assert(result.restored.result.items.some(item => item.label === 'public_name'));
    assert(result.unclosed.result.items.some(item => item.label === 'public_name'));
    assert.deepEqual(result.raw.result.items.find(item => item.label === 'public_name').textEdit, {
        range: { start: { line: 1, character: 7 }, end: { line: 1, character: 13 } }, newText: '"public_name"',
    });
    assert(result.emptyCall.result.items.some(item => item.label === '"unrelated_rpc"'));
    assert(result.comment.result.items.some(item => item.label === 'rpc_name'));
    assert.deepEqual(result.emptyCall.result.items[0].textEdit, {
        range: { start: { line: 1, character: 9 }, end: { line: 1, character: 9 } }, newText: '"public_name"',
    });
    assert(result.emptyTask.result.items.some(item => item.label === '"nightly"'));
    for (const [key, first] of [['emptyCall', 'public_name'], ['emptyTask', 'cleanup']])
        assert.equal([...result[key].result.items].sort((a, b) =>
            (a.sortText ?? a.label).localeCompare(b.sortText ?? b.label))[0].label, JSON.stringify(first));
    assert.deepEqual(result.comment.result.items.find(item => item.label === '"public_name"').textEdit, {
        range: { start: { line: 2, character: 9 }, end: { line: 2, character: 9 } }, newText: '"public_name"',
    });
    assert(!result.client.result.items.some(item => item.code === 'unresolved-import'));
}));

test('RPC contracts preserve signatures and native argument checks in the client runtime', () => withBrowser(async page => {
    const result = await page.evaluate(async () => {
        const { BrowserAnalysisSession } = await import('/session.mjs');
        const source = 'from anvil.server import call as invoke\nfrom .helper import value\ninvoke("say_hello", )\ninvoke("say_hello")\ninvoke("say_hello", value)\ninvoke("say_hello", None, loud=True)\n';
        const session = new BrowserAnalysisSession({ workerUrl: '/worker.mjs', rootUri: 'file:///app', files: {
            '/app/anvil.yaml': 'package_name: TestApp\n',
            '/app/client_code/__init__.py': '', '/app/client_code/main.py': source,
            '/app/client_code/helper.py': 'value = 42\n', '/app/server_code/helper.py': 'value = "server"\n',
            '/app/server_code/main.py': 'import anvil.server\n@anvil.server.callable("say_hello")\ndef greet(name: (\n    str\n    | None\n), count: int = 1, *, loud: bool = False) -> (\n    str\n):\n    return (name or "") * count\n',
        }});
        const textDocument = { uri: 'file:///app/client_code/main.py' };
        try {
            const signature = await session.query('textDocument/signatureHelp', { textDocument, position: { line: 2, character: 20 } });
            const diagnostics = await session.query('textDocument/diagnostic', { textDocument });
            const restored = await session.query('textDocument/hover', { textDocument, position: { line: 4, character: 22 } });
            await session.setContext({ id: 'rpc-repl', kind: 'repl', isServer: false, code: 'from anvil.server import call\ncall("say_hello", )' });
            const contextSignature = await session.queryContext('rpc-repl', 'textDocument/signatureHelp', { position: { line: 1, character: 18 } });
            return { signature, diagnostics, restored, contextSignature };
        } finally { session.dispose(); }
    });
    for (const response of [result.signature, result.contextSignature]) {
        const help = response.result;
        assert(help?.signatures.some(signature => signature.label.includes('name: str | None') &&
            signature.label.includes('count: int =') && signature.label.includes('*, loud: bool =')), JSON.stringify(help));
    }
    assert.match(result.restored.result.contents.value, /42/);
    assert(result.diagnostics.result.items.some(item => item.code === 'missing-argument' && item.range.start.line === 3), JSON.stringify(result.diagnostics));
    assert(result.diagnostics.result.items.some(item => item.code === 'invalid-argument-type' && item.range.start.line === 4), JSON.stringify(result.diagnostics));
    assert(!result.diagnostics.result.items.some(item => item.range.start.line === 5), JSON.stringify(result.diagnostics));
}));

test('RPC contracts retain variadics, async results and gradual server-only annotations', () => withBrowser(async page => {
    const result = await page.evaluate(async () => {
        const { BrowserAnalysisSession } = await import('/session.mjs');
        const source = 'from anvil.server import call_s as invoke\ncall = invoke\ncall("flex", "Ada", 1, other=object(), enabled=True, key="yes")\ncall("flex", "Ada", "bad", other=None)\nname = "flex"\ncall(name)\n';
        const session = new BrowserAnalysisSession({ workerUrl: '/worker.mjs', rootUri: 'file:///app', files: {
            '/app/anvil.yaml': 'package_name: TestApp\n', '/app/client_code/__init__.py': '', '/app/client_code/main.py': source,
            '/app/server_code/api.py': 'import anvil.server\nclass ServerOnly: pass\n@anvil.server.callable("flex")\nasync def implementation(fn_name: str, /, *values: int, other: ServerOnly, enabled: bool = False, **named: str) -> str:\n    return fn_name\n',
        }});
        const textDocument = { uri: 'file:///app/client_code/main.py' };
        try {
            const signature = await session.query('textDocument/signatureHelp', { textDocument, position: { line: 2, character: 13 } });
            const diagnostics = await session.query('textDocument/diagnostic', { textDocument });
            const hover = await session.query('textDocument/hover', { textDocument, position: { line: 2, character: 1 } });
            return { signature, diagnostics, hover };
        } finally { session.dispose(); }
    });
    const label = result.signature.result?.signatures[0].label;
    assert.match(label, /fn_name: str, \/, \*values: int, other: Any, enabled: bool = \.\.\., \*\*named: str/);
    assert.match(label, /-> str$/);
    assert.deepEqual(result.diagnostics.result.items.map(item => [item.code, item.range.start.line]), [['invalid-argument-type', 3]]);
}));

test('overloaded RPCs retain gradual argument fallback rather than selecting one overload', () => withBrowser(async page => {
    const result = await page.evaluate(async () => {
        const { BrowserAnalysisSession } = await import('/session.mjs');
        const session = new BrowserAnalysisSession({ workerUrl: '/worker.mjs', rootUri: 'file:///app', files: {
            '/app/anvil.yaml': 'package_name: Main\n', '/app/client_code/__init__.py': '',
            '/app/client_code/main.py': 'from anvil.server import call\ncall("choose", "Ada")\n',
            '/app/server_code/api.py': 'from typing import overload\nimport anvil.server\n@overload\ndef choose(name: int) -> int: ...\n@overload\ndef choose(name: str) -> str: ...\n@anvil.server.callable\ndef choose(name): return name\n',
        }});
        try { return await session.query('textDocument/diagnostic', { textDocument: { uri: 'file:///app/client_code/main.py' } }); }
        finally { session.dispose(); }
    });
    assert(!result.result.items.some(item => item.code === 'invalid-argument-type'), JSON.stringify(result));
}));
