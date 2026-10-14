// Read-only instrumentation of the existing built CLI; no sibling files change.
const fs = require('node:fs');
const Module = require('node:module');
const child = require('node:child_process');
const { performance } = require('node:perf_hooks');

const events = [];
const loads = [];
const roots = { calls: 0, cacheHits: 0, milliseconds: 0 };
const rootCache = new Map();
let compilingCli = false;
const mark = name => events.push({ name, milliseconds: performance.now() });
global.__anvilProfile = {
    mark,
    root(path, callback) {
        roots.calls++;
        if (process.env.ANVIL_PROFILE_ROOT_CACHE === '1' && rootCache.has(path)) {
            roots.cacheHits++;
            return rootCache.get(path);
        }
        const started = performance.now();
        const result = callback();
        roots.milliseconds += performance.now() - started;
        rootCache.set(path, result);
        return result;
    },
};
mark('preload');

const originalLoad = Module._load;
let loadDepth = 0;
const lazyUi = new Map();
function deferredUi(request, parent, isMain) {
    if (lazyUi.has(request)) return lazyUi.get(request);
    let loaded;
    const actual = () => loaded ||= originalLoad.call(Module, request, parent, isMain);
    const getDefault = () => actual().default || actual();
    const defaultExport = new Proxy(function() {}, {
        apply(_target, receiver, args) { return Reflect.apply(getDefault(), receiver, args); },
        get(_target, key) { return Reflect.get(getDefault(), key); },
    });
    const exports = new Proxy({}, {
        get(_target, key) {
            if (key === '__esModule') return true;
            if (key === 'default') return defaultExport;
            return actual()[key];
        },
    });
    lazyUi.set(request, exports);
    return exports;
}
Module._load = function(request, ...rest) {
    const started = performance.now();
    const depth = loadDepth++;
    try {
        if (compilingCli && process.env.ANVIL_PROFILE_LAZY_UI === '1'
            && ['inquirer', 'ora'].includes(request)) return deferredUi(request, ...rest);
        return originalLoad.call(this, request, ...rest);
    } finally {
        loadDepth--;
        // Direct bundle imports, with nested dependency load time included.
        if (compilingCli && depth === 1) loads.push({ request, milliseconds: performance.now() - started });
    }
};

const originalSpawn = child.spawnSync;
child.spawnSync = function(command, args, options) {
    mark(args.includes('--version') ? 'probe.start' : 'checker.start');
    const result = originalSpawn.call(this, command, args, options);
    mark(args.includes('--version') ? 'probe.end' : 'checker.end');
    const nativeEvents = String(result.stderr || '').split('\n')
        .filter(line => line.startsWith('[ANVIL_NATIVE_PROFILE] '))
        .map(line => JSON.parse(line.slice('[ANVIL_NATIVE_PROFILE] '.length)));
    if (nativeEvents.length) events.push({ name: args.includes('--version') ? 'native.probe' : 'native.checker', nativeEvents });
    return result;
};

const originalCompile = Module.prototype._compile;
Module.prototype._compile = function(content, filename) {
    if (filename !== process.env.ANVIL_PROFILE_CLI) return originalCompile.call(this, content, filename);
    const replace = (before, after) => {
        if (content.split(before).length !== 2) throw new Error(`CLI profiling anchor changed: ${before}`);
        content = content.replace(before, after);
    };
    replace('async function handleValidateDirectory(dir) {', 'async function handleValidateDirectory(dir) { global.__anvilProfile.mark("validation.entry");');
    replace('const files = collectValidationFiles(dir);', 'const files = collectValidationFiles(dir); global.__anvilProfile.mark("validation.files");');
    replace('const pythonResults = new Map();', 'global.__anvilProfile.mark("validation.structure"); const pythonResults = new Map();');
    replace('for (const [appRoot, appFiles] of filesByAppRoot){', 'global.__anvilProfile.mark("validation.grouping"); for (const [appRoot, appFiles] of filesByAppRoot){');
    replace('const appRoots = new Set(files.map', 'global.__anvilProfile.mark("validation.semantic"); const appRoots = new Set(files.map');
    replace('const fileResults = files.map', 'global.__anvilProfile.mark("validation.cache"); const fileResults = files.map');
    replace('function findAnvilAppRoot(filePath) {', 'function findAnvilAppRoot(filePath) { return global.__anvilProfile.root(filePath, () => originalFindAnvilAppRoot(filePath)); } function originalFindAnvilAppRoot(filePath) {');
    mark('compile.start');
    compilingCli = true;
    try {
        return originalCompile.call(this, content, filename);
    } finally {
        compilingCli = false;
    }
};
process.on('exit', () => {
    mark('exit');
    fs.writeSync(2, '[ANVIL_CLI_PROFILE] ' + JSON.stringify({ events, loads, roots }) + '\n');
});
