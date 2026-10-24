import assert from 'node:assert/strict';
import {test} from 'node:test';
import {withBrowser} from './browser.mjs';

// Exact issue reproductions, including the variants that already worked. Retain
// parse diagnostics while completing useful names in recoverable source.
const cases = [
    {
        "id": "4056",
        "code": "def foo():\n    return A()\nclass A:\n    def __init__(self):\n        self.bar = 'eggs'\nfoo().\u00a6\n",
        "expected": [
            "bar"
        ]
    },
    {
        "id": "4057-A",
        "code": "class A:\n    def __init__(self):\n        self.foo = 'bar'\n    @classmethod\n    def _create(cls):\n        return cls()\n    @classmethod\n    def create(cls):\n        return cls._create()\nclass B(A):\n    pass\nclass C(A):\n    @classmethod\n    def create(cls):\n        return cls._create()\nA.create().\u00a6\n",
        "expected": [
            "foo"
        ]
    },
    {
        "id": "4057-B",
        "code": "class A:\n    def __init__(self):\n        self.foo = 'bar'\n    @classmethod\n    def _create(cls):\n        return cls()\n    @classmethod\n    def create(cls):\n        return cls._create()\nclass B(A):\n    pass\nclass C(A):\n    @classmethod\n    def create(cls):\n        return cls._create()\nB.create().\u00a6\n",
        "expected": [
            "foo"
        ]
    },
    {
        "id": "4057-C",
        "code": "class A:\n    def __init__(self):\n        self.foo = 'bar'\n    @classmethod\n    def _create(cls):\n        return cls()\n    @classmethod\n    def create(cls):\n        return cls._create()\nclass B(A):\n    pass\nclass C(A):\n    @classmethod\n    def create(cls):\n        return cls._create()\nC.create().\u00a6\n",
        "expected": [
            "foo"
        ]
    },
    {
        "id": "4067",
        "code": "class A:\n    @classmethod\n    def create(cls):\n        return cls()\nclass B(A):\n    def __init__(self):\n        self.foo = 'bar'\nb = B.create()\nb.\u00a6\n",
        "expected": [
            "foo"
        ]
    },
    {
        "id": "2673",
        "server": true,
        "code": "import anvil.server\ndef foo():\n    known = 'hello'\n    If blah:\n        known.\u00a6\n@anvil.server.callable\ndef bar():\n",
        "expected": [
            "upper"
        ]
    },
    {
        "id": "2883-same",
        "server": true,
        "code": "import anvil.server\nfrom anvil.tables import app_tables\nanvil.server.\u00a6\n@anvil.server.background_task\ndef card_sending():\n    for row in app_tables.contacts.search(send=True):\n",
        "expected": [
            "call",
            "background_task"
        ]
    },
    {
        "id": "2883-other",
        "server": true,
        "extra": {
            "/app/server_code/broken.py": "import anvil.server\nfrom anvil.tables import app_tables\n@anvil.server.background_task\ndef card_sending():\n    for row in app_tables.contacts.search(send=True):\n"
        },
        "code": "import anvil.server\nanvil.server.\u00a6\n",
        "expected": [
            "call",
            "background_task"
        ]
    }
];
for(const fixture of cases) test(`Python inference and recovery #${fixture.id}`, () => withBrowser(async page => {
    const result=await page.evaluate(async fixture=>{
        const {BrowserAnalysisSession}=await import('/session.mjs');
        const uri=`file:///app/${fixture.server?'server_code':'client_code'}/main.py`;
        const code=fixture.code.replace('¦','');
        const before=fixture.code.slice(0,fixture.code.indexOf('¦')).split('\n');
        const session=new BrowserAnalysisSession({workerUrl:'/worker.mjs',rootUri:'file:///app',files:{
            '/app/anvil.yaml':'package_name: Main\n', '/app/client_code/__init__.py':'', [new URL(uri).pathname]:code, ...fixture.extra,
        }});
        try {
            const items=(await session.query('textDocument/completion',{textDocument:{uri},position:{line:before.length-1,character:before.at(-1).length}})).result.items;
            const diagnostics=(await session.query('textDocument/diagnostic',{textDocument:{uri: fixture.extra ? 'file:///app/server_code/broken.py' : uri}})).result.items;
            return {labels:items.map(item=>item.label),diagnostics,original:(await session.readSource(uri)).result.text,code};
        } finally {session.dispose();}
    },fixture);
    for(const name of fixture.expected) assert(result.labels.includes(name),`${fixture.id}: missing ${name}`);
    if(fixture.server) assert(result.diagnostics.some(item=>item.severity===1),'Malformed code must still be diagnosed');
    assert.equal(result.original,result.code);
}));
