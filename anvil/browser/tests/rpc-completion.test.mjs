import assert from 'node:assert/strict';
import { test } from 'node:test';
import { withBrowser } from './browser.mjs';

test('RPC demand follows builtin-name aliases through re-exports and live rebinding', () => withBrowser(async page => {
    const result = await page.evaluate(async () => {
        const { BrowserAnalysisSession } = await import('/session.mjs');
        const uri = 'file:///app/client_code/main.py';
        const source = 'from .bridge import *\nanswer = str("greet")\nanswer.\n';
        const session = new BrowserAnalysisSession({ workerUrl: '/worker.mjs', rootUri: 'file:///app', files: {
            '/app/anvil.yaml': 'package_name: Main\n', '/app/client_code/__init__.py': '',
            '/app/client_code/main.py': source,
            '/app/client_code/bridge.py': 'from anvil.server import call as str\n',
            '/app/server_code/api.py': 'import anvil.server\n@anvil.server.callable\ndef greet(): return "Ada"\n',
        } });
        const complete = async () => (await session.query('textDocument/completion', {
            textDocument: { uri }, position: { line: 2, character: 7 },
        })).result.items.map(item => item.label);
        try {
            const remote = await complete();
            await session.openDocument('file:///app/client_code/bridge.py', 'def str(name): return 42\n');
            const local = await complete();
            await session.closeDocument('file:///app/client_code/bridge.py');
            return { remote, local, restored: await complete(), source: (await session.readSource(uri)).result.text };
        } finally { session.dispose(); }
    });
    assert(result.remote.includes('upper'));
    assert(result.local.includes('bit_length') && !result.local.includes('upper'));
    assert(result.restored.includes('upper'));
    assert.equal(result.source, 'from .bridge import *\nanswer = str("greet")\nanswer.\n');
}));

test('builtin-spelled RPC calls follow star imports added and removed by an edit', () => withBrowser(async page => {
    const result = await page.evaluate(async () => {
        const { BrowserAnalysisSession } = await import('/session.mjs');
        const uri = 'file:///app/client_code/main.py';
        const source = 'answer = str("greet")\nanswer.\n';
        const session = new BrowserAnalysisSession({ workerUrl: '/worker.mjs', rootUri: 'file:///app', files: {
            '/app/anvil.yaml': 'package_name: Main\n', '/app/client_code/__init__.py': '',
            '/app/client_code/main.py': source,
            '/app/client_code/bridge.py': 'from anvil.server import call as str\n',
            '/app/server_code/api.py': 'import anvil.server\n@anvil.server.callable\ndef greet() -> int: return 42\n',
        } });
        const complete = async code => {
            await session.openDocument(uri, code);
            return (await session.query('textDocument/completion', { textDocument: { uri },
                position: { line: code.trimEnd().split('\n').length - 1, character: 7 },
                context: { autoImport: false } })).result.items.map(item => item.label);
        };
        try {
            return { builtin: await complete(source),
                remote: await complete('from .bridge import *\n' + source),
                restored: await complete(source),
                qualified: await complete('import anvil.server\nanswer = anvil.server.call("greet")\nanswer.\n') };
        } finally { session.dispose(); }
    });
    for (const items of [result.builtin, result.restored]) {
        assert(items.includes('upper') && !items.includes('bit_length'));
    }
    for (const items of [result.remote, result.qualified]) {
        assert(items.includes('bit_length') && !items.includes('upper'));
    }
}));

test('literal RPC keyword completion follows the callable without replacing caller expressions', () => withBrowser(async page => {
    const result = await page.evaluate(async () => {
        const { BrowserAnalysisSession } = await import('/session.mjs');
        const source = 'from anvil.server import call as invoke\nclient_name = "Ada"\ninvoke("say_hello", )\n';
        const server = parameter => `import anvil.server\n@anvil.server.callable\ndef say_hello(${parameter}: str, *, punctuation: str = "!") -> str:\n    return ${parameter} + punctuation\n`;
        const uri = 'file:///app/client_code/main.py';
        const session = new BrowserAnalysisSession({ workerUrl: '/worker.mjs', rootUri: 'file:///app', files: {
            '/app/anvil.yaml': 'package_name: Main\n', '/app/client_code/__init__.py': '',
            '/app/client_code/main.py': source, '/app/server_code/api.py': server('name'),
        } });
        const complete = async code => {
            await session.openDocument(uri, code);
            const lines = code.trimEnd().split('\n');
            return (await session.query('textDocument/completion', { textDocument: { uri },
                position: { line: lines.length - 1, character: lines.at(-1).lastIndexOf(')') } })).result.items;
        };
        try {
            const initial = await complete(source);
            const used = await complete(source.replace(', )', ', name=client_name, pu)'));
            await session.updateFiles({ '/app/server_code/api.py': server('person') });
            const changed = await complete(source);
            const restored = (await session.readSource(uri)).result.text;
            await session.setContext({ kind: 'repl', id: 'rpc', isServer: false,
                code: 'from anvil.server import call\ncall("say_hello", )' });
            const context = (await session.queryContext('rpc', 'textDocument/completion', {
                position: { line: 1, character: 'call("say_hello", '.length },
            })).result.items;
            return { initial, used, changed, context, restored, source };
        } finally { session.dispose(); }
    });
    const labels = items => items.map(item => item.label);
    assert(labels(result.initial).includes('name='), JSON.stringify(labels(result.initial)));
    assert(labels(result.initial).includes('punctuation='));
    assert(labels(result.initial).includes('client_name'), 'Argument expressions retain the caller runtime');
    assert(labels(result.used).includes('punctuation=') && !labels(result.used).includes('name='));
    for (const items of [result.changed, result.context]) {
        assert(labels(items).includes('person=') && !labels(items).includes('name='), JSON.stringify(labels(items)));
        assert(!labels(items).some(label => label.startsWith('_anvil_rpc_')), 'Temporary projection names stay private');
    }
    assert.equal(result.restored, result.source, 'Keyword inference must not change original source');
}));

test('Server-local return schemas keep their fields and source locations on the client', () => withBrowser(async page => {
    const result = await page.evaluate(async () => {
        const { BrowserAnalysisSession } = await import('/session.mjs');
        const schemaUri = 'file:///app/server_code/Schema.py';
        const clientUri = 'file:///app/client_code/main.py';
        const schema = `from collections.abc import Mapping, Sequence
from datetime import datetime
from anvil import Media
from anvil.server import HttpRequest
from typing import Any, Literal
from typing_extensions import ReadOnly, TypedDict
from .Shared import Device, State

class ServerOnly:
    pass

Contact = TypedDict("Contact", {"full-name": str})

class ExtendedContact(Contact):
    age: int

class Metrics(TypedDict, extra_items=ReadOnly[int]):
    total: int

class Details(TypedDict):
    name: str

class Profile(TypedDict):
    created_at: datetime
    state: Literal["active", "pending"]
    enum_state: Literal[State.ACTIVE]
    photo: Media
    request: HttpRequest
    devices: tuple[str, ...]
    details: Mapping[str, Details]
    history: Sequence[Details]
    payload: Any
    internal: ServerOnly
    device: Device
    contact: ExtendedContact
    metrics: Metrics
`;
        const client = `import anvil.server
from anvil import Media
from datetime import datetime
from typing import Any, Literal
from typing_extensions import assert_type
from .Schema import Profile
from .Shared import Device, State

profiles = anvil.server.call("get_profiles")
profile = profiles["ada"]
details = profile["details"]
assert_type(profile["created_at"], datetime)
assert_type(profile["state"], Literal["active", "pending"])
assert_type(profile["enum_state"], Literal[State.ACTIVE])
assert_type(profile["photo"], Media)
assert_type(profile["request"], Any)
assert_type(profile["devices"], tuple[str, ...])
assert_type(details["ada"]["name"], str)
assert_type(profile["history"][0]["name"], str)
assert_type(profile["payload"], Any)
assert_type(profile["internal"], Any)
assert_type(profile["device"], Device)
assert_type(profile["metrics"]["unlisted"], int)
profile["metrics"]["unlisted"] = 1
assert_type(profile["contact"]["full-name"], str)
anvil.server.call("get_profiles", limit="bad")
choice = anvil.server.call("get_device_or_profiles")
`;
        const session = new BrowserAnalysisSession({ workerUrl: '/worker.mjs', rootUri: 'file:///app', files: {
            '/app/anvil.yaml': 'package_name: RpcProfile\n',
            '/app/client_code/__init__.py': '',
            '/app/client_code/Shared.py': 'import anvil.server\nfrom enum import Enum\n' +
                'class State(Enum):\n    ACTIVE = 1\n    INACTIVE = 2\n@anvil.server.portable_class\nclass Device:\n    model: str\n',
            '/app/server_code/api.py': 'import anvil.server\nfrom .Schema import Profile\nfrom .Shared import Device\n' +
                '@anvil.server.callable\ndef get_profiles(limit: int = 1) -> dict[str, Profile]:\n    return {}\n' +
                '@anvil.server.callable\ndef get_device_or_profiles() -> dict[str, Profile] | Device:\n    return {}\n',
            [new URL(clientUri).pathname]: client,
            [new URL(schemaUri).pathname]: schema,
        } });
        const query = async (method, options = {}) => (await session.query('textDocument/' + method, {
            textDocument: { uri: clientUri }, ...options,
        })).result;
        const diagnostics = () => query('diagnostic').then(result => result.items);
        const position = (source, snippet, symbol) => {
            const lines = source.split('\n');
            const line = lines.findIndex(line => line.includes(snippet));
            return { line, character: lines[line].indexOf(symbol) + 1 };
        };
        const destinations = async (method, snippet, symbol) => {
            const targets = await query(method, { position: position(client, snippet, symbol) });
            return targets.map(target => ({
                uri: target.uri,
                text: schema.split('\n')[target.range.start.line]?.slice(target.range.start.character, target.range.end.character),
            }));
        };
        try {
            const before = await diagnostics();
            const choice = (await query('typeDefinition', { position: position(client, 'choice =', 'choice') }))
                .map(target => target.uri).sort();
            const profile = await destinations('typeDefinition', 'profiles =', 'profiles');
            const details = await destinations('typeDefinition', 'details =', 'details');
            const field = await destinations('definition', 'assert_type(profile["contact"]["full-name"]', '"full-name"');
            const completion = client + 'profile["details"]["ada"][""]\n';
            await session.openDocument(clientUri, completion);
            const keys = (await query('completion', {
                position: position(completion, '["ada"][""]', '""'),
                context: { autoImport: false },
            })).items.map(item => item.label);
            await session.openDocument(clientUri, client);
            await session.openDocument(schemaUri, schema.replace('name: str', 'name: int'));
            return { before, choice, profile, details, field, keys, after: await diagnostics(), schemaUri };
        } finally { session.dispose(); }
    });
    assert.deepEqual(result.before.filter(item => item.code === 'type-assertion-failure'), []);
    assert(result.before.some(item => item.code === 'unresolved-import' && item.message.includes('.Schema')));
    assert(result.before.some(item => item.code === 'invalid-argument-type' && item.message.includes('bad')));
    assert(result.before.some(item => item.message.includes('read-only') && item.message.includes('unlisted')));
    assert.deepEqual(result.choice, ['file:///app/client_code/Shared.py', result.schemaUri]);
    assert.deepEqual(result.profile, [{ uri: result.schemaUri, text: 'Profile' }]);
    assert.deepEqual(result.details, [{ uri: result.schemaUri, text: 'Details' }]);
    assert.deepEqual(result.field, [{ uri: result.schemaUri, text: '"full-name"' }]);
    assert(result.keys.includes('name'));
    assert.equal(result.after.filter(item => item.code === 'type-assertion-failure').length, 2);
}));
