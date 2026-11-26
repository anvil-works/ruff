import assert from 'node:assert/strict';
import { test } from 'node:test';
import { withBrowser } from './browser.mjs';

test('client tests complete and navigate through client modules, Forms, dependencies and test helpers without server modules', () => withBrowser(async page => {
    const result = await page.evaluate(async () => {
        const { BrowserAnalysisSession } = await import('/session.mjs');
        const uri = 'file:///client-tests/tests/client_tests/test_ui.py';
        const code = [
            'from Main.ClientHelpers import format_label',
            'from Main.Home import Home',
            'from .helpers_é import Harness',
            'from Library.Widgets import Badge',
            'harness = Harness()',
            'harness.',
            '',
        ].join('\n');
        const files = {
            '/client-tests/anvil.yaml': 'package_name: Main\n',
            '/client-tests/client_code/__init__.py': '',
            '/client-tests/server_code/__init__.py': '',
            '/client-tests/.anvil/client-tests.json': 'true',
            '/client-tests/.anvil/dependencies.json': JSON.stringify({
                roots: ['/client-tests/.anvil/deps/LIB'],
                ids: { LIB: '/client-tests/.anvil/deps/LIB' },
            }),
            '/client-tests/client_code/ClientHelpers.py': 'def format_label(count: int) -> str:\n    return str(count)\n',
            '/client-tests/client_code/Home/__init__.py': 'from ._anvil_designer import HomeTemplate\nclass Home(HomeTemplate):\n    def greet(self) -> str:\n        return "hi"\n',
            '/client-tests/client_code/Home/form_template.yaml': JSON.stringify({
                container: { type: 'ColumnPanel' },
                components: [{ name: 'title_label', type: 'Label', properties: {} }],
            }),
            '/client-tests/server_code/ServerSecret.py': 'def secret_only() -> str:\n    return "secret"\n',
            '/client-tests/tests/client_tests/__init__.py': '',
            '/client-tests/tests/client_tests/helpers_é.py': 'class Harness:\n    ready: bool = True\n',
            '/client-tests/tests/client_tests/support/dom.py': 'class DomHelper:\n    clicked: bool = True\n',
            '/client-tests/tests/client_tests/test #1%.py': 'value = 1\nvalue\n',
            '/client-tests/.anvil/deps/LIB/anvil.yaml': 'package_name: Library\n',
            '/client-tests/.anvil/deps/LIB/client_code/Widgets.py': 'class Badge:\n    text: str = "ok"\n',
            [new URL(uri).pathname]: code,
        };
        const session = new BrowserAnalysisSession({ workerUrl: '/worker.mjs', rootUri: 'file:///client-tests', files });
        const query = async (method, line, character) => (await session.query(method, {
            textDocument: { uri }, position: { line, character }, context: { autoImport: false },
        })).result;
        try {
            const completion = await query('textDocument/completion', 5, 8);
            const helper = await query('textDocument/definition', 4, 12);
            const clientModule = await query('textDocument/definition', 0, 35);
            const formDef = await query('textDocument/definition', 1, 24);
            const dependency = await query('textDocument/definition', 3, 30);
            await session.changeDocument(uri, code.replace('harness.\n', 'format_label(\n'));
            const signature = await query('textDocument/signatureHelp', 5, 13);
            await session.changeDocument(uri, 'from Main.Home import Home\nform = Home()\nform.\n');
            const formMembers = await query('textDocument/completion', 2, 5);
            await session.updateFiles({ '/client-tests/tests/client_tests/helpers_é.py': 'class Harness:\n    updated: str = "changed"\n' });
            await session.changeDocument(uri, code);
            const updated = await query('textDocument/completion', 5, 8);
            await session.changeDocument(uri, 'from dom import DomHelper\nd = DomHelper()\nd.\n');
            const bareHelper = await query('textDocument/completion', 2, 2);
            await session.changeDocument(uri, 'from client_tests.support.dom import DomHelper\nd = DomHelper()\nd.\n');
            const qualifiedHelper = await query('textDocument/completion', 2, 2);
            await session.changeDocument(uri, 'from Main.ServerSecret import secret_only\nsecret_only()\n');
            const serverImportDiagnostics = (await session.query('textDocument/diagnostic', { textDocument: { uri } })).result;
            const specialFile = 'file:///client-tests/tests/client_tests/test%20%231%25.py';
            const special = (await session.query('textDocument/definition', { textDocument: { uri: specialFile }, position: { line: 1, character: 2 } })).result;
            return {
                completion, helper, clientModule, formDef, dependency, signature, formMembers,
                updated, bareHelper, qualifiedHelper, serverImportDiagnostics, special,
            };
        } finally { session.dispose(); }
    });
    assert(result.completion.items.some(item => item.label === 'ready'));
    assert(result.helper.some(location => location.uri === 'file:///client-tests/tests/client_tests/helpers_%C3%A9.py'));
    assert(result.clientModule.some(location => location.uri === 'file:///client-tests/client_code/ClientHelpers.py'));
    assert(result.formDef.some(location => location.uri === 'file:///client-tests/client_code/Home/__init__.py'));
    assert(result.dependency.some(location => location.uri === 'file:///client-tests/.anvil/deps/LIB/client_code/Widgets.py'));
    assert(result.signature.signatures.some(signature => signature.label.includes('count: int')));
    assert(result.formMembers.items.some(item => item.label === 'greet'));
    assert(result.formMembers.items.some(item => item.label === 'title_label'));
    assert(result.updated.items.some(item => item.label === 'updated'));
    assert(!result.updated.items.some(item => item.label === 'ready'));
    assert(!result.bareHelper.items.some(item => item.label === 'clicked'), 'uncollected helper directories are not Python search roots');
    assert(result.qualifiedHelper.items.some(item => item.label === 'clicked'));
    assert(
        result.serverImportDiagnostics.items.some(item => item.code === 'unresolved-import'),
        `client tests must not resolve server-only modules: ${JSON.stringify(result.serverImportDiagnostics)}`,
    );
    assert(result.special.some(location => location.uri === 'file:///client-tests/tests/client_tests/test%20%231%25.py'));
}));

test('pytest is supported as a Skulpt module in client tests without enabling it in ordinary client code', () => withBrowser(async page => {
    const result = await page.evaluate(async () => {
        const { BrowserAnalysisSession } = await import('/session.mjs');
        const baseFiles = {
            '/client-tests/anvil.yaml': 'package_name: Main\n',
            '/client-tests/client_code/__init__.py': '',
            '/client-tests/server_code/__init__.py': '',
            '/client-tests/tests/client_tests/__init__.py': '',
        };
        async function inspect(isClientTest) {
            const rootUri = isClientTest ? 'file:///client-tests' : 'file:///app';
            const root = isClientTest ? '/client-tests' : '/app';
            const uri = isClientTest
                ? 'file:///client-tests/tests/client_tests/test_pytest.py'
                : 'file:///app/client_code/app_mod.py';
            const files = Object.fromEntries(Object.entries(baseFiles).map(([k, v]) => [k.replace('/client-tests', root), v]));
            if (isClientTest) files[`${root}/.anvil/client-tests.json`] = 'true';
            files[new URL(uri).pathname] = 'import pytest\npytest.\n';
            const session = new BrowserAnalysisSession({ workerUrl: '/worker.mjs', rootUri, files });
            const query = async (method, line, character) => (await session.query(method, {
                textDocument: { uri }, position: { line, character }, context: { autoImport: false },
            })).result;
            try {
                const api = await query('textDocument/completion', 1, 7);
                if (!isClientTest) return { api };
                await session.changeDocument(uri, 'import py');
                const importCompletion = await query('textDocument/completion', 0, 9);
                await session.changeDocument(uri, 'import pytest\nimport subprocess\nwith pytest.raises(ValueError):\n    pass\n');
                const diagnostics = (await session.query('textDocument/diagnostic', { textDocument: { uri } })).result;
                await session.changeDocument(uri, 'import pytest\ndef test_patch(patch: pytest.MonkeyPatch):\n    patch.\n');
                const methods = await query('textDocument/completion', 2, 10);
                await session.changeDocument(uri, 'import pytest\npytest.raises(ValueError)\n');
                const definitions = await query('textDocument/definition', 1, 10);
                const source = definitions.length ? (await session.readSource(definitions[0].uri)).result : null;
                return { api, importCompletion, diagnostics, methods, definitions, source };
            } finally { session.dispose(); }
        }
        return { normal: await inspect(false), tests: await inspect(true) };
    });
    assert(!result.normal.api.items.some(item => item.label === 'fixture'), 'ordinary client code must not expose pytest');
    assert(result.tests.importCompletion.items.some(item => item.label === 'pytest'), 'import completion should offer pytest');
    for (const name of ['fixture', 'raises', 'mark', 'approx', 'MonkeyPatch'])
        assert(result.tests.api.items.some(item => item.label === name), name);
    assert(result.tests.methods.items.some(item => item.label === 'setenv'), JSON.stringify(result.tests.methods));
    assert(result.tests.methods.items.some(item => item.label === 'setattr'));
    assert(
        !result.tests.diagnostics.items.some(item => item.message.includes('pytest')),
        `pytest must not trigger Skulpt or unresolved-import diagnostics: ${JSON.stringify(result.tests.diagnostics)}`,
    );
    assert(
        result.tests.diagnostics.items.some(item => item.code === 'reportAnvilUnsupportedSkulptImport' && item.message.includes('subprocess')),
        `unsupported Skulpt stdlib imports must still be flagged in client tests: ${JSON.stringify(result.tests.diagnostics)}`,
    );
    assert(result.tests.definitions.some(location => location.uri.includes('/_pytest/raises.py')));
    assert(result.tests.source?.readOnly);
    assert(result.tests.source?.text.includes('def raises('));
}));
