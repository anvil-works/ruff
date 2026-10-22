import { copyFile, mkdir } from 'node:fs/promises';

// Keep the standalone browser files self-contained, including when the IDE copies dist/.
const output = new URL('./dist/', import.meta.url);
await mkdir(output, { recursive: true });
for (const name of ['comlink.mjs', 'comlink.mjs.map']) {
    await copyFile(new URL(import.meta.resolve(`comlink/dist/esm/${name}`)), new URL(name, output));
}
await copyFile(new URL(import.meta.resolve('comlink/LICENSE')), new URL('comlink.LICENSE', output));
