import assert from 'node:assert/strict';
import { test } from 'node:test';
import { withBrowser } from './browser.mjs';

test('portable optional metadata preserves configured Users rows in client and server', () => withBrowser(async page => {
    const results = await page.evaluate(async () => {
        const { BrowserAnalysisSession } = await import('/session.mjs');
        const stubs = await (await fetch('/dist/api-stubs.json')).json();
        for (const environment of ['client', 'server']) {
            const path = `${environment}/anvil/users/__init__.pyi`;
            const signature = 'def get_user(allow_remembered: bool = True) -> Row | None:';
            if (!stubs.files[path].includes(signature)) throw new Error('Users stub fixture changed');
            stubs.files[path] = 'from typing import Annotated\n' + stubs.files[path].replace(
                signature,
                'def get_user(allow_remembered: bool = True) -> Row | Annotated[None, "anvil:permissive-optional"]:',
            );
        }
        const apiStubsUrl = URL.createObjectURL(new Blob([JSON.stringify(stubs)], { type: 'application/json' }));
        const config = (name, type) => JSON.stringify({ package_name: 'Main',
            db_schema: { users: { columns: [{ name, type }] } },
            services: [{ source: '/runtime/services/anvil/users', server_config: { user_table: 'users' } }],
        });
        const session = new BrowserAnalysisSession({ workerUrl: '/worker.mjs', apiStubsUrl,
            rootUri: 'file:///app', files: { '/app/anvil.yaml': config('nickname', 'string'),
                '/app/client_code/main.py': '', '/app/server_code/main.py': '',
                '/app/server_code/api.py': 'import anvil.server\nimport anvil.users\n' +
                    '@anvil.server.callable\ndef current_user():\n    return anvil.users.get_user()\n',
            },
        });
        const results = [];
        const prefix = 'import anvil.users\nuser = anvil.users.get_user()\n';
        try {
            for (const environment of ['client', 'server']) {
                const textDocument = { uri: `file:///app/${environment}_code/main.py` };
                const complete = async (suffix) => {
                    await session.changeDocument(textDocument.uri, prefix + suffix);
                    return (await session.query('textDocument/completion', { textDocument,
                        position: { line: 2, character: suffix.length }, context: { autoImport: false },
                    })).result.items.map(item => item.label);
                };
                const members = await complete('user.');
                const field = await complete('user["nickname"].');
                const keys = await complete('user["');
                const source = prefix + 'name: str = user["nickname"]\n' +
                    'user.update(nickname=123)\nuser["nickname"].missing_member()\n' +
                    'if user is None:\n    user["nickname"]\n' +
                    'def ordinary(value: str | None):\n    value.upper()\n';
                await session.changeDocument(textDocument.uri, source);
                const diagnostics = (await session.query('textDocument/diagnostic', { textDocument })).result.items;
                const hover = (await session.query('textDocument/hover', { textDocument,
                    position: { line: 1, character: 1 },
                })).result;
                const hints = (await session.query('textDocument/inlayHint', { textDocument,
                    range: { start: { line: 0, character: 0 }, end: { line: 2, character: 0 } },
                })).result;
                results.push({ environment, members, field, keys, diagnostics, hover, hints });
            }
            const client = { uri: 'file:///app/client_code/main.py' };
            const rpcPrefix = 'import anvil.server\nuser = anvil.server.call("current_user")\n';
            await session.changeDocument(client.uri, rpcPrefix + 'user["nickname"].');
            const rpc = (await session.query('textDocument/completion', { textDocument: client,
                position: { line: 2, character: 'user["nickname"].'.length }, context: { autoImport: false },
            })).result.items.map(item => item.label);
            await session.changeDocument(client.uri, rpcPrefix +
                'name: str = user["nickname"]\nif user is None:\n    user["nickname"]\n');
            const rpcDiagnostics = (await session.query('textDocument/diagnostic', { textDocument: client })).result.items;
            await session.updateFiles({ '/app/anvil.yaml': config('score', 'number') });
            const textDocument = { uri: 'file:///app/client_code/main.py' };
            await session.changeDocument(textDocument.uri, prefix + 'user["score"].');
            const changed = (await session.query('textDocument/completion', { textDocument,
                position: { line: 2, character: 'user["score"].'.length }, context: { autoImport: false },
            })).result.items.map(item => item.label);
            return { results, changed, rpc, rpcDiagnostics };
        } finally {
            session.dispose();
            URL.revokeObjectURL(apiStubsUrl);
        }
    });
    for (const { environment, members, field, keys, diagnostics, hover, hints } of results.results) {
        assert(hover.contents.value.includes('_Row_users | None'), environment);
        assert(!hover.contents.value.includes('anvil:permissive-optional'), environment);
        const userHint = hints.find(hint => hint.position.line === 1);
        assert.equal(userHint?.label, ': _Row_users | None', environment);
        assert(members.includes('update'), `${environment}: missing row methods`);
        assert(field.includes('upper'), `${environment}: missing string field members`);
        assert(keys.includes('nickname'), `${environment}: missing configured keys`);
        assert.deepEqual(diagnostics.map(item => [item.code, item.range.start.line]), [
            ['invalid-argument-type', 3], ['unresolved-attribute', 4],
            ['not-subscriptable', 6], ['unresolved-attribute', 8],
        ], environment);
    }
    assert(results.changed.includes('real'));
    assert(!results.changed.includes('upper'));
    assert(results.rpc.includes('upper'), 'Inferred RPC return must retain the portable optional annotation');
    assert.deepEqual(results.rpcDiagnostics.map(item => [item.code, item.range.start.line]), [
        ['not-subscriptable', 4],
    ]);
}));
