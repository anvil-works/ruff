import assert from 'node:assert/strict';
import { readFile } from 'node:fs/promises';
import { test } from 'node:test';
import { withBrowser } from './browser.mjs';

test('client tests complete and navigate through client modules, Forms and dependencies without server or sibling test imports', () => withBrowser(async page => {
    const result = await page.evaluate(async () => {
        const { BrowserAnalysisSession } = await import('/session.mjs');
        const uri = 'file:///client-tests/tests/client_tests/test_ui.py';
        const code = [
            'from Main.ClientHelpers import format_label, HelperState',
            'from Main.Home import Home',
            'from Library.Widgets import Badge',
            'state = HelperState()',
            'state.',
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
            '/client-tests/client_code/ClientHelpers.py': 'class HelperState:\n    ready: bool = True\n\ndef format_label(count: int) -> str:\n    return str(count)\n',
            '/client-tests/client_code/Home/__init__.py': 'from ._anvil_designer import HomeTemplate\nclass Home(HomeTemplate):\n    def greet(self) -> str:\n        return "hi"\n',
            '/client-tests/client_code/Home/form_template.yaml': JSON.stringify({
                container: { type: 'ColumnPanel' },
                components: [{ name: 'title_label', type: 'Label', properties: {} }],
            }),
            '/client-tests/server_code/ServerSecret.py': 'def secret_only() -> str:\n    return "secret"\n',
            '/client-tests/tests/client_tests/__init__.py': '',
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
            const completion = await query('textDocument/completion', 4, 6);
            const clientModule = await query('textDocument/definition', 0, 35);
            const formDef = await query('textDocument/definition', 1, 24);
            const dependency = await query('textDocument/definition', 2, 30);
            await session.changeDocument(uri, code.replace('state.\n', 'format_label(\n'));
            const signature = await query('textDocument/signatureHelp', 4, 13);
            await session.changeDocument(uri, 'from Main.Home import Home\nform = Home()\nform.\n');
            const formMembers = await query('textDocument/completion', 2, 5);
            await session.updateFiles({
                '/client-tests/client_code/ClientHelpers.py': 'class HelperState:\n    updated: str = "changed"\n\ndef format_label(count: int) -> str:\n    return str(count)\n',
            });
            await session.changeDocument(uri, code);
            const updated = await query('textDocument/completion', 4, 6);
            await session.changeDocument(uri, 'from dom import DomHelper\nDomHelper()\n');
            const bareHelperDiagnostics = (await session.query('textDocument/diagnostic', { textDocument: { uri } })).result;
            await session.changeDocument(uri, 'from client_tests.support.dom import DomHelper\nDomHelper()\n');
            const qualifiedHelperDiagnostics = (await session.query('textDocument/diagnostic', { textDocument: { uri } })).result;
            await session.changeDocument(uri, 'from Main.ServerSecret import secret_only\nsecret_only()\n');
            const serverImportDiagnostics = (await session.query('textDocument/diagnostic', { textDocument: { uri } })).result;
            const specialFile = 'file:///client-tests/tests/client_tests/test%20%231%25.py';
            const special = (await session.query('textDocument/definition', { textDocument: { uri: specialFile }, position: { line: 1, character: 2 } })).result;
            return {
                completion, clientModule, formDef, dependency, signature, formMembers,
                updated, bareHelperDiagnostics, qualifiedHelperDiagnostics, serverImportDiagnostics, special,
            };
        } finally { session.dispose(); }
    });
    assert(result.completion.items.some(item => item.label === 'ready'));
    assert(result.clientModule.some(location => location.uri === 'file:///client-tests/client_code/ClientHelpers.py'));
    assert(result.formDef.some(location => location.uri === 'file:///client-tests/client_code/Home/__init__.py'));
    assert(result.dependency.some(location => location.uri === 'file:///client-tests/.anvil/deps/LIB/client_code/Widgets.py'));
    assert(result.signature.signatures.some(signature => signature.label.includes('count: int')));
    assert(result.formMembers.items.some(item => item.label === 'greet'));
    assert(result.formMembers.items.some(item => item.label === 'title_label'));
    assert(result.updated.items.some(item => item.label === 'updated'));
    assert(!result.updated.items.some(item => item.label === 'ready'));
    assert(
        result.bareHelperDiagnostics.items.some(item => item.code === 'unresolved-import'),
        `bare sibling test helper imports must not resolve: ${JSON.stringify(result.bareHelperDiagnostics)}`,
    );
    assert(
        result.qualifiedHelperDiagnostics.items.some(item => item.code === 'unresolved-import'),
        `client_tests package helper imports must not resolve in standalone skulpt-pytest mode: ${JSON.stringify(result.qualifiedHelperDiagnostics)}`,
    );
    assert(
        result.serverImportDiagnostics.items.some(item => item.code === 'unresolved-import'),
        `client tests must not resolve server-only modules: ${JSON.stringify(result.serverImportDiagnostics)}`,
    );
    assert(result.special.some(location => location.uri === 'file:///client-tests/tests/client_tests/test%20%231%25.py'));
}));

test('pytest is supported as a Skulpt module in client tests without enabling it in ordinary client code', () => withBrowser(async page => {
    const result = await page.evaluate(async () => {
        const { BrowserAnalysisSession } = await import('/session.mjs');
        async function inspect(isClientTest) {
            const rootUri = isClientTest ? 'file:///client-tests' : 'file:///app';
            const root = isClientTest ? '/client-tests' : '/app';
            const uri = isClientTest
                ? 'file:///client-tests/tests/client_tests/test_pytest.py'
                : 'file:///app/client_code/app_mod.py';
            const files = {
                [`${root}/anvil.yaml`]: 'package_name: Main\n',
                [`${root}/client_code/__init__.py`]: '',
                [`${root}/server_code/__init__.py`]: '',
                ...(isClientTest ? {
                    [`${root}/.anvil/client-tests.json`]: 'true',
                    [`${root}/tests/client_tests/__init__.py`]: '',
                } : {}),
                [new URL(uri).pathname]: 'import pytest\npytest.\n',
            };
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
    for (const name of ['setattr', 'setitem', 'delattr', 'undo'])
        assert(result.tests.methods.items.some(item => item.label === name), `${name}: ${JSON.stringify(result.tests.methods)}`);
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

test('client-tests API stub overlays expose PRIVILEGED and force_login with user row types only in client tests', () => withBrowser(async page => {
    const baseStubs = JSON.parse(await readFile(new URL('../dist/api-stubs.json', import.meta.url), 'utf8'));
    const overlayFiles = {
        ...baseStubs.files,
        'client-tests/anvil/testing/__init__.pyi': 'class _PrivilegedContext:\n    def __enter__(self) -> "_PrivilegedContext": ...\n    def __exit__(self, *args) -> bool: ...\nPRIVILEGED: _PrivilegedContext\n',
        'client-tests/anvil/users/__init__.pyi': `${baseStubs.files['client/anvil/users/__init__.pyi']}\ndef force_login(user_row: Row, remember: bool = False) -> Row | None: ...\n`,
    };
    delete overlayFiles['client/anvil/testing/__init__.pyi'];
    await page.context().route('**/client-test-stubs.json', route => route.fulfill({
        contentType: 'application/json',
        body: JSON.stringify({ ...baseStubs, files: overlayFiles }),
    }));
    const result = await page.evaluate(async () => {
        const { BrowserAnalysisSession } = await import('/session.mjs');
        const anvilYaml = JSON.stringify({
            package_name: 'Main',
            services: [{ source: '/runtime/services/anvil/users.yml', server_config: { user_table: 'users' } }],
            db_schema: {
                users: {
                    python_name: 'users',
                    columns: [{ name: 'email', type: 'string' }, { name: 'role_tag', type: 'string' }],
                },
            },
        });
        async function inspect(isClientTest) {
            const rootUri = isClientTest ? 'file:///client-tests' : 'file:///app';
            const root = isClientTest ? '/client-tests' : '/app';
            const uri = isClientTest
                ? 'file:///client-tests/tests/client_tests/test_auth.py'
                : 'file:///app/client_code/main.py';
            const serverUri = `${rootUri}/server_code/srv.py`;
            const files = {
                [`${root}/anvil.yaml`]: anvilYaml,
                [`${root}/client_code/__init__.py`]: '',
                [`${root}/server_code/__init__.py`]: '',
                [`${root}/server_code/srv.py`]: 'import anvil.testing\nanvil.testing.\n',
                ...(isClientTest ? {
                    [`${root}/.anvil/client-tests.json`]: 'true',
                    [`${root}/tests/client_tests/__init__.py`]: '',
                } : {}),
                [new URL(uri).pathname]: 'import anvil.users\nanvil.users.\n',
            };
            const session = new BrowserAnalysisSession({
                workerUrl: '/worker.mjs',
                rootUri,
                apiStubsUrl: '/client-test-stubs.json',
                files,
            });
            const complete = async (docUri, line, character) => (await session.query('textDocument/completion', {
                textDocument: { uri: docUri }, position: { line, character }, context: { autoImport: false },
            })).result.items.map(item => item.label);
            try {
                const usersMembers = await complete(uri, 1, 12);
                await session.changeDocument(uri, 'import anvil.testing\nanvil.testing.\n');
                const testingMembers = await complete(uri, 1, 14);
                let forcedRowKeys = [];
                let serverTestingMembers = [];
                if (isClientTest) {
                    await session.changeDocument(
                        uri,
                        'import anvil.testing\nimport anvil.users\nfrom anvil.tables import app_tables\nwith anvil.testing.PRIVILEGED:\n    row = app_tables.users.get(email="a@b.com")\n    assert row is not None\n    logged_in = anvil.users.force_login(row)\n    assert logged_in is not None\n    logged_in["\n',
                    );
                    forcedRowKeys = await complete(uri, 8, 15);
                    serverTestingMembers = await complete(serverUri, 1, 14);
                }
                return { usersMembers, testingMembers, forcedRowKeys, serverTestingMembers };
            } finally { session.dispose(); }
        }
        return { normal: await inspect(false), tests: await inspect(true) };
    });
    assert(!result.normal.usersMembers.includes('force_login'), 'normal client code must not see force_login');
    assert(!result.normal.testingMembers.includes('PRIVILEGED'), 'normal client code must not see PRIVILEGED');
    assert(result.tests.usersMembers.includes('force_login'), 'client tests must see force_login');
    assert(result.tests.testingMembers.includes('PRIVILEGED'), 'client tests must see PRIVILEGED');
    assert(!result.tests.serverTestingMembers.includes('PRIVILEGED'), 'server queries must not inherit client-tests API overlays');
    assert(result.tests.forcedRowKeys.some(label => label.includes('role_tag')), `force_login should preserve configured user row keys: ${JSON.stringify(result.tests.forcedRowKeys)}`);
}));
