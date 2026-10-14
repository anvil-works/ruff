// Transitional proof: reuse Anvil's existing generators without running its checker.
const fs = require('node:fs');
const path = require('node:path');
const [pyrightRoot, appRoot, destination] = process.argv.slice(2);
const compiled = path.join(pyrightRoot, 'packages/pyright-internal/out/packages/pyright-internal/src/anvil');
const { parseAnvilConfig, getGoogleAppFiles } = require(path.join(compiled, 'config.js'));
const { parseFormTemplate } = require(path.join(compiled, 'formTemplateParser.js'));
const { generateFormTemplateStub } = require(path.join(compiled, 'formTemplateStubGenerator.js'));
const { generateAnvilTablesStub, generateAnvilUsersStub, generateGoogleDriveStub } = require(path.join(compiled, 'stubGenerator.js'));
const config = parseAnvilConfig(fs.readFileSync(path.join(appRoot, 'anvil.yaml'), 'utf8'));
if (!config || !config.package_name || !/^[A-Za-z_]\w*$/.test(config.package_name)) {
    throw new Error('The proof requires a Python identifier in anvil.yaml package_name');
}
const origins = {};
const selected = {};
function copyCode(source, target, checked) {
    if (!fs.existsSync(source)) return;
    fs.mkdirSync(target, { recursive: true });
    for (const entry of fs.readdirSync(source, { withFileTypes: true })) {
        if (entry.name.startsWith('.') || entry.name === '__pycache__') continue;
        const from = path.join(source, entry.name);
        const to = path.join(target, entry.name);
        if (entry.isDirectory()) copyCode(from, to, checked);
        else if (entry.isFile() && /\.(py|pyi|yaml|html)$/.test(entry.name)) {
            fs.copyFileSync(from, to);
            if (entry.name.endsWith('.py')) {
                origins[to] = from;
                if (checked) selected[checked].push(to);
            }
        }
    }
}
function designers(directory) {
    for (const entry of fs.readdirSync(directory, { withFileTypes: true })) {
        const file = path.join(directory, entry.name);
        if (entry.isDirectory()) designers(file);
    }
    if (!fs.existsSync(path.join(directory, '__init__.py'))) return;
    const template = ['form_template.yaml', 'form_template.html'].find(name => fs.existsSync(path.join(directory, name)));
    if (!template) return;
    const form = path.basename(directory);
    const parsed = parseFormTemplate(fs.readFileSync(path.join(directory, template), 'utf8'), template.endsWith('.html') ? 'html' : 'yaml', form);
    if (!parsed) throw new Error(`Could not parse form template: ${directory}`);
    fs.writeFileSync(path.join(directory, '_anvil_designer.pyi'), generateFormTemplateStub(parsed, { appPackageName: config.package_name }));
}
for (const environment of ['client', 'server']) {
    selected[environment] = [];
    const workspace = path.join(destination, environment);
    const code = path.join(workspace, config.package_name);
    fs.mkdirSync(code, { recursive: true });
    copyCode(path.join(appRoot, 'client_code'), code, environment === 'client' ? environment : null);
    if (environment === 'server') copyCode(path.join(appRoot, 'server_code'), code, environment);
    if (!fs.existsSync(path.join(code, '__init__.py'))) fs.writeFileSync(path.join(code, '__init__.py'), '');
    designers(code);
    const stubs = path.join(workspace, 'stubs');
    fs.cpSync(path.join(pyrightRoot, 'packages/pyright-internal/src/anvil-typeshed', environment), stubs, { recursive: true });
    fs.writeFileSync(path.join(stubs, 'anvil/tables/__init__.pyi'), generateAnvilTablesStub(config, environment));
    const users = path.join(stubs, 'anvil/users/__init__.pyi');
    fs.writeFileSync(users, generateAnvilUsersStub(fs.readFileSync(users, 'utf8'), config, environment));
    const drive = path.join(stubs, 'anvil/google/drive.pyi');
    fs.writeFileSync(drive, generateGoogleDriveStub(fs.readFileSync(drive, 'utf8'), getGoogleAppFiles(config)));
}
process.stdout.write(JSON.stringify({ origins, selected, package: config.package_name, dependencies: config.dependencies ?? [] }));
