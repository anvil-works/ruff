# Validation timing profiles

The [10 October production-source startup correction](../reports/2026-10-10-startup-summary.md)
now implements deferred prompt/spinner loading in the CLI. It saves 70–79 ms in
paired fresh-process measurements. The original profiling experiments below remain
historical evidence; no app-root cache or engine-lifetime change was implemented.

This profiling harness explains where the native proof's current validation time
goes. It changes no production source or sibling checkout. It generates an
instrumented Rust example, builds it with the same release profile, then removes
the example source. A Node preload transforms the existing CLI bundle in memory
to add boundary timers. Native and CLI diagnostics must match plain controls.

Run from anvil-ruff, with the existing proof setup:

```sh
.venv/bin/python anvil/profiling/run.py --runs 5 \
  --output anvil/reports/profile-local.json
```

The script also includes throwaway experiments that memoize app-root results
within one CLI invocation and defer `inquirer`/`ora` imports until used. The loader's
proxy technique is diagnostic scaffolding; production lazy imports need normal
module boundaries and coverage of interactive commands.

## Evidence

- [Original boundary samples](../reports/native-profile.json): five fresh runs
    per mode and input size, after one warm-up, with rotating execution order.
    This initial run included the app-root cache experiment.
- [Boundary summary](../reports/native-profile-summary.json): per-boundary medians
    from that run. Native detail is nested inside the CLI checker time; do not add
    it to the parent categories.
- [Lazy UI loading experiment](../reports/cli-lazy-profile.json): a subsequent
    five-run comparison on the 200-Python-file fixture, using the normal native
    executable. All CLI outputs match the plain control after normalizing source
    paths and timestamps. The nine native integration tests also pass with lazy
    UI loading and app-root caching enabled.

These are warm-filesystem profiles of the bounded synthetic fixtures. Stopwatch
instrumentation and ordinary process-startup variation affect the numbers. The
original controls measured 321 ms for the full CLI and 88 ms for the native
checker on 200 files; instrumentation measured 327 ms and 89 ms respectively.
Per-boundary medians need not sum exactly to the median total.

## Where time goes

Approximate full-CLI costs on 200 Python files:

| Boundary                                             | Milliseconds |
| ---------------------------------------------------- | -----------: |
| Node/CLI startup, imports and command initialization |          201 |
| File discovery                                       |            3 |
| YAML/structural validation                           |           11 |
| Python-file app-root grouping                        |            6 |
| Final app-root lookup and dependency-cache check     |           10 |
| Checker version probe                                |            5 |
| Native checker process                               |           88 |
| Diagnostic mapping, output and other glue            |            3 |

App-root discovery is nested in several CLI categories above: 602 calls consume
about 18 ms in total. Per-invocation memoization produces 301 hits and cuts its
measured work to about 9 ms. The final app-root/cache stage falls from about 10 ms
to 2 ms. Total wall-time gains are small relative to process-startup variance.

Within the native checker:

| Work                                   | Milliseconds |
| -------------------------------------- | -----------: |
| Process startup/exit                   |            7 |
| App configuration and initial API read |          \<1 |
| Python source reads                    |          4.5 |
| YAML designer generation               |            5 |
| In-memory source/stub mounting         |          5.8 |
| Database setup                         |          4.3 |
| Client ty check                        |           33 |
| Server ty check                        |           19 |
| Database teardown                      |         10.4 |

The check calls include parsing imported stubs, import resolution and typing.
These timers do not separate those inner engine operations. The databases are
fresh for each invocation; these are not incremental checks.

## Cuts supported by the evidence

The largest cheap opportunity is CLI startup. Direct module loads cost about
47 ms for `inquirer` and 30 ms for `ora`, although JSON validation needs neither
prompts nor spinners. They are eagerly imported by the CLI logger and command
graph. Loading them when their functionality is first used preserves the tested
validation results in the loader experiment.

The later experiment's full-CLI medians were:

| Mode                                          | Milliseconds |
| --------------------------------------------- | -----------: |
| Plain production binaries                     |          322 |
| Instrumented control                          |          340 |
| Instrumented lazy UI imports                  |          271 |
| Instrumented lazy UI imports + app-root cache |          261 |

The combined prototype is about 19% faster than the plain control, including its
profiling overhead. This demonstrates the opportunity; it is not a shipped CLI
patch. Further command/import separation may avoid other startup work, but its
savings have not been measured.

For repeated agent validation, keeping the frontend and ty databases alive could
amortize startup and reuse ty's incremental queries. Actual edited-file latency
requires a separate experiment with file/config invalidation. The current native
proof freezes its databases for one-shot checks and cannot simply be reused for
mutable sessions.

Smaller native possibilities are concurrent client/server checks (up to roughly
the 19 ms server phase before contention) and deferred database teardown (about
10 ms, with higher retained peak memory). Neither is measured here. Static API
stub mounting is only about 2 ms across both environments, so packaging those
stubs independently remains useful chiefly for distribution.
