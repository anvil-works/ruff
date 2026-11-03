import assert from 'node:assert/strict';
import { test } from 'node:test';
import { withBrowser } from './browser.mjs';

test('server tests complete and navigate through their package, app and dependency sources', () => withBrowser(async page => {
    const result = await page.evaluate(async () => {
        const { BrowserAnalysisSession } = await import('/session.mjs');
        const uri = 'file:///app/tests/server_tests/test_orders.py';
        const code = 'from Main.Orders import calculate_total\nfrom .helpers_é import Order\nfrom Library.Rates import tax_rate\norder = Order()\norder.\n';
        const files = {
            '/app/anvil.yaml': 'package_name: Main\n',
            '/app/client_code/__init__.py': '',
            '/app/server_code/__init__.py': '',
            '/app/.anvil/server-tests.json': 'true',
            '/app/.anvil/dependencies.json': JSON.stringify({ roots: ['/app/.anvil/deps/LIB'], ids: { LIB: '/app/.anvil/deps/LIB' } }),
            '/app/server_code/Orders.py': 'def calculate_total(count: int) -> int:\n    return count * 42\n',
            '/app/tests/server_tests/__init__.py': '',
            '/app/tests/server_tests/helpers_é.py': 'class Order:\n    total: int = 42\n',
            '/app/tests/server_tests/support/amounts.py': 'class Amount:\n    total: int = 42\n',
            '/app/tests/server_tests/test #1%.py': 'value = 1\nvalue\n',
            '/app/.anvil/deps/LIB/anvil.yaml': 'package_name: Library\n',
            '/app/.anvil/deps/LIB/server_code/Rates.py': 'tax_rate = 0.2\n',
            [new URL(uri).pathname]: code,
        };
        const session = new BrowserAnalysisSession({ workerUrl: '/worker.mjs', rootUri: 'file:///app', files });
        const query = async (method, line, character) => (await session.query(method, {
            textDocument: { uri }, position: { line, character }, context: { autoImport: false },
        })).result;
        try {
            const completion = await query('textDocument/completion', 4, 6);
            const helper = await query('textDocument/definition', 3, 10);
            const app = await query('textDocument/definition', 0, 30);
            const dependency = await query('textDocument/definition', 2, 31);
            await session.changeDocument(uri, code.replace('order.\n', 'calculate_total(\n'));
            const signature = await query('textDocument/signatureHelp', 4, 16);
            await session.updateFiles({ '/app/tests/server_tests/helpers_é.py': 'class Order:\n    updated: str = "changed"\n' });
            await session.changeDocument(uri, code);
            const updated = await query('textDocument/completion', 4, 6);
            await session.changeDocument(uri, 'from amounts import Amount\namount = Amount()\namount.\n');
            const bareHelper = await query('textDocument/completion', 2, 7);
            await session.changeDocument(uri, 'from server_tests.support.amounts import Amount\namount = Amount()\namount.\n');
            const qualifiedHelper = await query('textDocument/completion', 2, 7);
            const specialFile = 'file:///app/tests/server_tests/test%20%231%25.py';
            const special = (await session.query('textDocument/definition', { textDocument: { uri: specialFile }, position: { line: 1, character: 2 } })).result;
            return { completion, helper, app, dependency, signature, updated, bareHelper, qualifiedHelper, special };
        } finally { session.dispose(); }
    });
    assert(result.completion.items.some(item => item.label === 'total'));
    assert(result.helper.some(location => location.uri === 'file:///app/tests/server_tests/helpers_%C3%A9.py'));
    assert(result.app.some(location => location.uri === 'file:///app/server_code/Orders.py'));
    assert(result.dependency.some(location => location.uri === 'file:///app/.anvil/deps/LIB/server_code/Rates.py'));
    assert(result.signature.signatures.some(signature => signature.label.includes('count: int')));
    assert(result.updated.items.some(item => item.label === 'updated'));
    assert(!result.updated.items.some(item => item.label === 'total'));
    assert(!result.bareHelper.items.some(item => item.label === 'total'), 'uncollected helper directories are not Python search roots');
    assert(result.qualifiedHelper.items.some(item => item.label === 'total'));
    assert(result.special.some(location => location.uri === 'file:///app/tests/server_tests/test%20%231%25.py'));
}));

test('pytest APIs load lazily from test requirements without enabling them for ordinary server code', () => withBrowser(async page => {
    const result = await page.evaluate(async () => {
        const { BrowserAnalysisSession } = await import('/session.mjs');
        const files = {
            '/app/anvil.yaml': 'package_name: Main\n',
            '/app/client_code/__init__.py': '',
            '/app/server_code/__init__.py': '',
            '/app/tests/server_tests/__init__.py': '',
            '/app/tests/server_tests/requirements.txt': 'pytest>=9\n',
        };
        async function complete(test) {
            const uri = test ? 'file:///app/tests/server_tests/test_api.py' : 'file:///app/server_code/api.py';
            const session = new BrowserAnalysisSession({ workerUrl: '/worker.mjs', rootUri: 'file:///app', files: {
                ...files, ...(test ? { '/app/.anvil/server-tests.json': 'true' } : {}),
                [new URL(uri).pathname]: 'import pytest\npytest.\n',
            } });
            const query = async (method, line, character) => (await session.query(method, {
                textDocument: { uri }, position: { line, character }, context: { autoImport: false },
            })).result;
            try {
                const api = await query('textDocument/completion', 1, 7);
                if (!test) return { api };
                await session.changeDocument(uri, 'import pytest\ndef test_patch(patch: pytest.MonkeyPatch):\n    patch.\n');
                const methods = await query('textDocument/completion', 2, 10);
                await session.changeDocument(uri, 'import pytest\npytest.raises(ValueError)\n');
                const definitions = await query('textDocument/definition', 1, 10);
                const source = definitions.length ? (await session.readSource(definitions[0].uri)).result : null;
                return { api, methods, definitions, source };
            } finally { session.dispose(); }
        }
        return { normal: await complete(false), tests: await complete(true) };
    });
    assert(!result.normal.api.items.some(item => item.label === 'fixture'));
    for (const name of ['fixture', 'raises', 'mark', 'approx', 'MonkeyPatch'])
        assert(result.tests.api.items.some(item => item.label === name), name);
    assert(result.tests.methods.items.some(item => item.label === 'setenv'), JSON.stringify(result.tests.methods));
    assert(result.tests.methods.items.some(item => item.label === 'setattr'));
    assert(result.tests.definitions.some(location => location.uri.includes('/_pytest/raises.py')));
    assert(result.tests.source.readOnly);
    assert(result.tests.source.text.includes('def raises('));
}));
