import assert from 'node:assert/strict';
import {test} from 'node:test';
import {withBrowser} from './browser.mjs';

const files = {
    '/app/anvil.yaml':'package_name: Main\n',
    '/app/client_code/__init__.py':'',
    '/app/client_code/helpers.py':'class Rocket: pass\n',
};

test('go to type definition follows the inferred class into its original source', () => withBrowser(async page=>{
    const result=await page.evaluate(async files=>{
        const {BrowserAnalysisSession}=await import('/session.mjs');
        const uri='file:///app/client_code/main.py';
        const session=new BrowserAnalysisSession({workerUrl:'/worker.mjs',rootUri:'file:///app',files:{...files,[new URL(uri).pathname]:'from .helpers import Rocket\nrocket = Rocket()\nrocket\n'}});
        try {return (await session.query('textDocument/typeDefinition',{textDocument:{uri},position:{line:2,character:2}})).result;}
        finally {session.dispose();}
    },files);
    assert(result.some(target=>target.uri==='file:///app/client_code/helpers.py' && target.range.start.line===0));
}));

test('diagnostic quick fixes return current original-file import edits that clear the error',()=>withBrowser(async page=>{
    const result=await page.evaluate(async files=>{
        const {BrowserAnalysisSession}=await import('/session.mjs');
        const uri='file:///app/client_code/main.py';
        const code='value = math.sqrt(4)\n';
        const session=new BrowserAnalysisSession({workerUrl:'/worker.mjs',rootUri:'file:///app',files:{...files,[new URL(uri).pathname]:code}});
        try {
            const diagnostics=(await session.query('textDocument/diagnostic',{textDocument:{uri}})).result.items;
            const actions=(await session.query('textDocument/codeAction',{textDocument:{uri},range:diagnostics[0].range,context:{diagnostics}})).result;
            const action=actions.find(action=>action.isPreferred && action.title==='import math');
            if(!action) return {actions};
            const original=(await session.readSource(uri)).result.text;
            const edits=action.edit.changes[uri];
            const offset=position=>code.split('\n').slice(0,position.line).reduce((sum,line)=>sum+line.length+1,0)+position.character;
            let changed=code;
            for(const edit of edits.toSorted((a,b)=>offset(b.range.start)-offset(a.range.start))) changed=changed.slice(0,offset(edit.range.start))+edit.newText+changed.slice(offset(edit.range.end));
            await session.openDocument(uri,changed);
            const after=(await session.query('textDocument/diagnostic',{textDocument:{uri}})).result.items;
            return {actions,original,code,changed,after};
        } finally {session.dispose();}
    },files);
    assert(result.actions.some(action=>action.title==='import math' && action.isPreferred));
    assert.equal(result.original,result.code);
    assert.match(result.changed,/import math/);
    assert.deepEqual(result.after.filter(item=>item.severity===1),[]);
}));

test('inlay hints expose inferred types and parameter names without editing source',()=>withBrowser(async page=>{
    const result=await page.evaluate(async files=>{
        const {BrowserAnalysisSession}=await import('/session.mjs');
        const uri='file:///app/client_code/main.py';
        const code='def greet(name: str) -> str:\n    return name\nmessage = greet("Ada")\n';
        const session=new BrowserAnalysisSession({workerUrl:'/worker.mjs',rootUri:'file:///app',files:{...files,[new URL(uri).pathname]:code}});
        try {
            const hints=(await session.query('textDocument/inlayHint',{textDocument:{uri},range:{start:{line:0,character:0},end:{line:3,character:0}}})).result;
            return {hints,code,original:(await session.readSource(uri)).result.text};
        } finally {session.dispose();}
    },files);
    assert(result.hints.some(hint=>hint.kind===1 && hint.label.includes('str')));
    assert(result.hints.some(hint=>hint.kind===2 && hint.label.includes('name')));
    assert.equal(result.original,result.code);
}));
