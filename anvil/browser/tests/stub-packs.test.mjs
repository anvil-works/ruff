import assert from 'node:assert/strict';
import { test } from 'node:test';
import { withBrowser } from './browser.mjs';

test('multiple server declaration versions select one compatible artifact and cache by content URL', () => withBrowser(async page => {
    const profiles = [
        { version: '0.2.1', member: 'early_api' },
        { version: '3.0.6', member: 'exact_api' },
        { version: '3.0.8', member: 'patch_api' },
        { version: '3.1.2', member: 'latest_api' },
    ];
    const fetched = [];
    await page.context().route('**/dist/stub-packs.mjs', route => route.fulfill({ contentType: 'text/javascript', body:
        `export const completionPreferences = {}; export const stubPacks = ${JSON.stringify(profiles.map(profile => ({
            id: 'demolib', server: true, modules: ['demolib'], version: profile.version,
            url: `./stubs/demo-${profile.version}.json`,
        })))}.map(pack => ({...pack, url: new URL(pack.url, import.meta.url)}));`,
    }));
    await page.context().route('**/dist/stubs/demo-*.json', route => {
        const profile = profiles.find(profile => route.request().url().endsWith(`demo-${profile.version}.json`));
        fetched.push(profile.version);
        return route.fulfill({ contentType: 'application/json', body: JSON.stringify({
            'demolib/__init__.pyi': `${profile.member}: str\n`,
        }) });
    });
    const result = await page.evaluate(async () => {
        const { BrowserAnalysisSession } = await import('/session.mjs');
        const config = { package_name: 'Main', runtime_options: { server_spec: { requirements: 'demolib' } } };
        const uri = 'file:///app/server_code/main.py';
        const session = new BrowserAnalysisSession({ workerUrl: '/worker.mjs', rootUri: 'file:///app', files: {
            '/app/anvil.yaml': JSON.stringify(config), '/app/client_code/__init__.py': '',
            '/app/server_code/main.py': 'import demolib\ndemolib.',
        } });
        const result = [];
        try {
            for (const requirements of ['demolib', 'demolib==3.0.6', 'demolib==3.0.7', 'demolib==3.2.0', 'demolib==2.9.0', 'demolib==0.3.0', 'demolib']) {
                config.runtime_options.server_spec.requirements = requirements;
                await session.updateFiles({ '/app/anvil.yaml': JSON.stringify(config) });
                result.push((await session.query('textDocument/completion', { textDocument: { uri },
                    position: { line: 1, character: 8 } })).result.items.map(item => item.label).filter(label => label.endsWith('_api')));
            }
            return result;
        } finally { session.dispose(); }
    });
    assert.deepEqual(result, [['latest_api'], ['exact_api'], ['patch_api'], ['latest_api'], [], [], ['latest_api']]);
    assert.deepEqual(fetched.toSorted(), ['3.0.6', '3.0.8', '3.1.2']);
}));

test('configured server NumPy loads on demand and retains ndarray completion and readonly definitions', () => withBrowser(async page => {
    const packs = [];
    page.on('request', request => {
        if (request.url().includes('/dist/stubs/numpy-')) packs.push(request.url());
    });
    const result = await page.evaluate(async () => {
        const { BrowserAnalysisSession } = await import('/session.mjs');
        const uri = 'file:///app/server_code/main.py';
        const config = { package_name: 'Main', runtime_options: {server_spec: {
            base: 'python314', requirements: 'numpy==2.5.4\n',
        }} };
        const session = new BrowserAnalysisSession({ workerUrl: '/worker.mjs', rootUri: 'file:///app', files: {
            '/app/anvil.yaml': JSON.stringify(config), '/app/client_code/__init__.py': '',
            '/app/server_code/main.py': 'name = "Ada"\nname.up',
        } });
        window.session = session;
        const ordinary = (await session.query('textDocument/completion', {
            textDocument: { uri }, position: { line: 1, character: 7 },
        })).result.items;
        return ordinary;
    });
    assert(result.some(item => item.label === 'upper'));
    assert.equal(packs.length, 0, 'Configured but unused libraries must stay lazy');
    const loaded = await page.evaluate(async () => {
        const session = window.session;
        const uri = 'file:///app/server_code/main.py';
        try {
            await session.openDocument(uri, 'import numpy as np\nnp.array([1, 2]).resh');
            const params = { textDocument: { uri }, position: { line: 1, character: 21 } };
            const first = (await session.query('textDocument/completion', params)).result.items;
            const again = (await session.query('textDocument/completion', params)).result.items;
            const definition = (await session.query('textDocument/definition', {
                textDocument: { uri }, position: { line: 1, character: 5 },
            })).result;
            const source = definition.length ? (await session.readSource(definition[0].uri)).result : undefined;
            return {first, again, source};
        } finally { session.dispose(); }
    });
    for (const items of [loaded.first, loaded.again]) assert(items.some(item => item.label === 'reshape'));
    assert.equal(packs.length, 1);
    assert.equal(loaded.source.readOnly, true);
    assert.match(loaded.source.text, /def array\(/);
}));

test('server pandas provides DataFrame and Series types with NumPy dependencies and follows requirements changes', () => withBrowser(async page => {
    const packs = [];
    page.on('request', request => {
        if (/\/dist\/stubs\/(?:numpy|pandas)-/.test(request.url())) packs.push(request.url());
    });
    const result = await page.evaluate(async () => {
        const { BrowserAnalysisSession } = await import('/session.mjs');
        const uri = 'file:///app/server_code/main.py';
        const config = { package_name: 'Main', runtime_options: {server_spec: {
            base: 'python314', requirements: 'numpy==2.5.4\npandas==3.1.0\n',
        }} };
        const source = 'import pandas as pd\nframe = pd.read_csv("customers.csv")\nframe.gro';
        const session = new BrowserAnalysisSession({ workerUrl: '/worker.mjs', rootUri: 'file:///app', files: {
            '/app/anvil.yaml': JSON.stringify(config), '/app/client_code/__init__.py': '',
            '/app/.anvil/server-requirements.json': '["pandas", "--extra-index-url https://download.pytorch.org/whl/cpu", "torch"]',
            '/app/server_code/main.py': source,
        } });
        const params = { textDocument: { uri }, position: { line: 2, character: 9 } };
        try {
            const frame = (await session.query('textDocument/completion', params)).result.items;
            await session.openDocument(uri, 'import pandas as pd\nseries = pd.Series(["Ada"])\nseries.str.lo');
            const series = (await session.query('textDocument/completion', {
                textDocument: { uri }, position: { line: 2, character: 13 },
            })).result.items;
            await session.setContext({id: 'repl', kind: 'repl', isServer: true, previousCode: 'import pandas as pd',
                code: 'pd.DataFrame().gro'});
            const context = (await session.queryContext('repl', 'textDocument/completion', {
                position: {line: 0, character: 18},
            })).result.items;
            await session.closeContext('repl');
            await session.openDocument('file:///app/client_code/__init__.py', 'import pandas as pd\npd.DataFrame().gro');
            const client = (await session.query('textDocument/completion', {
                textDocument: {uri: 'file:///app/client_code/__init__.py'}, position: {line: 1, character: 18},
            })).result.items;
            await session.openDocument(uri, source);
            config.runtime_options.server_spec.requirements = 'numpy<2\npandas==3.1.0\n';
            await session.updateFiles({'/app/anvil.yaml': JSON.stringify(config)});
            const incompatible = (await session.query('textDocument/completion', params)).result.items;
            config.runtime_options.server_spec.requirements = 'pandas==3.1.0\n';
            await session.updateFiles({'/app/anvil.yaml': JSON.stringify(config)});
            const restored = (await session.query('textDocument/completion', params)).result.items;
            return {frame, series, context, client, incompatible, restored};
        } finally { session.dispose(); }
    });
    for (const key of ['frame', 'context', 'restored']) assert(result[key].some(item => item.label === 'groupby'), key);
    assert(result.series.some(item => item.label === 'lower'));
    assert(!result.client.some(item => item.label === 'groupby'), 'Server packages must not leak into Skulpt');
    assert(!result.incompatible.some(item => item.label === 'groupby'), 'Incompatible dependencies must unmount loaded types');
    assert.equal(packs.filter(url => url.includes('/numpy-')).length, 1);
    assert.equal(packs.filter(url => url.includes('/pandas-')).length, 1);
}));

test('server typing snapshots respect constraints and leave unresolved requirements gradual', () => withBrowser(async page => {
    const result = await page.evaluate(async () => {
        const { BrowserAnalysisSession } = await import('/session.mjs');
        const uri = 'file:///app/server_code/main.py';
        const config = {package_name: 'Main', runtime_options: {server_spec: {requirements: ''}}};
        const session = new BrowserAnalysisSession({workerUrl: '/worker.mjs', rootUri: 'file:///app', files: {
            '/app/anvil.yaml': JSON.stringify(config), '/app/client_code/__init__.py': '',
            '/app/server_code/main.py': 'import numpy as np\nnp.array([1]).resh',
        }});
        const result = [];
        try {
            for (const [requirements, expected] of [
                ['NumPy[typing]>=2.5,<2.6 # selected snapshot\n', true],
                ['numpy==2.5.4\t# numerical package\n', true],
                ['numpy (==2.5.4)\n', true],
                ['numpy==2.5.3\n', true],
                ['numpy==2.6.0\n', true],
                ['numpy==2.2.6\n', false],
                ['numpy==3.0.0\n', false],
                ['numpy==2.6.0rc1\n', false],
                ['numpy==2.6.0\nnumpy<2.5\n', false],
                ['numpy<2\n', false],
                ['numpy ; python_version < "3.10"\n', false],
                ['numpy @ https://example.invalid/custom.whl\n', false],
                ['numpy\n-c constraints.txt\n', false],
                ['numpy\\\n==1.26.4\n', false],
            ]) {
                config.runtime_options.server_spec.requirements = requirements;
                await session.updateFiles({'/app/anvil.yaml': JSON.stringify(config)});
                const items = (await session.query('textDocument/completion', {
                    textDocument: {uri}, position: {line: 1, character: 18},
                })).result.items;
                result.push({requirements, expected, ndarray: items.some(item => item.label === 'reshape')});
            }
            return result;
        } finally {session.dispose();}
    });
    for (const entry of result) assert.equal(entry.ndarray, entry.expected, entry.requirements);
}));

test('Plotly stays out of eager browser assets and loads once for completion and readonly navigation', () => withBrowser(async page => {
    const packs = [];
    let compatibility;
    page.on('request', request => {
        if (request.url().includes('/dist/stubs/plotly-client-')) packs.push(request.url());
    });
    page.on('response', response => {
        if (response.url().endsWith('/dist/compat/anvil_ty_compat_bg.wasm')) compatibility = response;
    });
    const initial = await page.evaluate(async () => {
        const { BrowserAnalysisSession } = await import('/session.mjs');
        window.session = new BrowserAnalysisSession({ workerUrl: '/worker.mjs', rootUri: 'file:///app', files: {
            '/app/anvil.yaml': 'package_name: Main\n', '/app/client_code/main.py': 'pl',
        } });
        return (await window.session.query('textDocument/completion', {
            textDocument: { uri: 'file:///app/client_code/main.py' }, position: { line: 0, character: 2 },
        })).result.items;
    });
    assert(initial.some(item => item.label === 'plotly'));
    assert.equal(packs.length, 0, 'Unrelated completion must not fetch Plotly');
    assert((await compatibility.body()).length < 4_000_000, 'Plotly must not inflate eagerly fetched compatibility WASM');
    const loaded = await page.evaluate(async () => {
        const session = window.session;
        const uri = 'file:///app/client_code/main.py';
        try {
            await session.openDocument(uri, 'import plotly.graph_objects as go\ngo.Scatter().marker.co');
            const params = { textDocument: { uri }, position: { line: 1, character: 22 } };
            const [first, second] = await Promise.all([
                session.query('textDocument/completion', params), session.query('textDocument/completion', params),
            ]);
            const definition = (await session.query('textDocument/definition', {
                textDocument: { uri }, position: { line: 1, character: 5 },
            })).result;
            const source = (await session.readSource(definition[0].uri)).result;
            await session.updateFiles({ '/app/anvil.yaml': 'package_name: Main\nsecrets: {}\n' });
            const refreshed = (await session.query('textDocument/completion', params)).result.items;
            return { first: first.result.items, second: second.result.items, refreshed, source };
        } finally { session.dispose(); }
    });
    for (const items of [loaded.first, loaded.second, loaded.refreshed]) assert(items.some(item => item.label === 'color'));
    assert.equal(packs.length, 1, 'Concurrent queries and metadata refreshes reuse the same pack');
    assert.equal(loaded.source.readOnly, true);
    assert.match(loaded.source.text, /class Scatter\(/);
}));

test('a failed Plotly fetch leaves edits and server completion usable and retries on the next client request', () => withBrowser(async page => {
    let requests = 0;
    await page.route('**/dist/stubs/plotly-client-*.json', route => ++requests === 1
        ? route.fulfill({ status: 503, body: 'Temporarily unavailable' }) : route.continue());
    const result = await page.evaluate(async () => {
        const { BrowserAnalysisSession } = await import('/session.mjs');
        const uri = 'file:///app/client_code/main.py';
        const source = 'import plotly.graph_objects as go\ngo.';
        const session = new BrowserAnalysisSession({ workerUrl: '/worker.mjs', rootUri: 'file:///app', files: {
            '/app/anvil.yaml': 'package_name: Main\n', '/app/client_code/main.py': source,
            '/app/server_code/api.py': 'name = "Ada"\nname.up',
        } });
        const params = { textDocument: { uri }, position: { line: 1, character: 3 } };
        try {
            let failure;
            try { await session.query('textDocument/completion', params); }
            catch (error) { failure = error.message; }
            const server = (await session.query('textDocument/completion', {
                textDocument: { uri: 'file:///app/server_code/api.py' }, position: { line: 1, character: 7 },
            })).result.items;
            await session.openDocument(uri, 'local_name = "Ada"\nloc');
            const local = (await session.query('textDocument/completion', params)).result.items;
            await session.openDocument(uri, source);
            const retried = (await session.query('textDocument/completion', params)).result.items;
            return { failure, server, local, retried, revision: session.revision };
        } finally { session.dispose(); }
    });
    assert.match(result.failure, /Plotly.*503/);
    assert(result.server.some(item => item.label === 'upper'));
    assert(result.local.some(item => item.label === 'local_name'));
    assert(result.retried.some(item => item.label === 'Scatter'));
    assert.equal(result.revision, 2);
    assert.equal(requests, 2);
}));
