import * as Comlink from './dist/comlink.mjs';

/** Ordered browser access to ty. The worker owns the WASM workspace. */
export class BrowserAnalysisSession {
    revision = 0;
    #worker;
    #remote;
    #queue;
    #shutdown = new AbortController();

    constructor({ workerUrl, rootUri, files, apiStubsUrl }) {
        this.#worker = new Worker(workerUrl, { type: 'module' });
        this.#remote = Comlink.wrap(this.#worker);
        this.#worker.onerror = (event) => this.#stop(new Error(event.message || 'ty worker failed'));
        this.#queue = this.#send('initialize', { rootUri, files, apiStubsUrl }).catch(error => this.#stop(error));
    }

    async #send(method, params) {
        const signal = this.#shutdown.signal;
        signal.throwIfAborted();
        let onStop;
        // Comlink calls stay pending when a worker terminates. Reject them on session shutdown too.
        const stopped = new Promise((_, reject) => {
            onStop = () => reject(signal.reason);
            signal.addEventListener('abort', onStop, { once: true });
        });
        try {
            return await Promise.race([this.#remote.request(method, params), stopped]);
        } finally {
            signal.removeEventListener('abort', onStop);
        }
    }

    #change(method, params) {
        const revision = ++this.revision;
        const pending = this.#queue.then(() => this.#send(method, { ...params, revision }));
        // The caller receives its error; ordering alone must recover so a
        // corrected edit can reach the worker's last successful snapshot.
        this.#queue = pending.catch(() => {});
        return pending.then(() => revision);
    }

    updateFiles(files) { return this.#change('updateFiles', { files }); }
    openDocument(uri, text) { return this.#change('openDocument', { uri, text }); }
    changeDocument(uri, text) { return this.#change('openDocument', { uri, text }); }
    closeDocument(uri) { return this.#change('closeDocument', { uri }); }
    setContext(context) { return this.#change('setContext', { context }); }
    closeContext(id) { return this.#change('closeContext', { id }); }
    queryContext(id, method, params, options) { return this.query('queryContext', { id, method, params }, options); }

    readSource(uri, options) { return this.query('anvil/readSource', { uri }, options); }

    async query(method, params, { signal } = {}) {
        await this.#queue;
        signal?.throwIfAborted();
        const response = await this.#send(method, params);
        signal?.throwIfAborted();
        return response;
    }

    #stop(error) {
        if (this.#shutdown.signal.aborted) return;
        this.#shutdown.abort(error);
        this.#remote[Comlink.releaseProxy]();
        this.#worker.terminate();
    }

    dispose() { this.#stop(new Error('Analysis session is disposed')); }
}
