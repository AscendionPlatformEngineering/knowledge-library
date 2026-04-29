# CLI Tooling

The architecture of command-line tools as composable engineering primitives — recognising that the CLI's output formats, exit codes, configuration layering, credential handling, and progressive disclosure are what determine whether the tool composes cleanly with other tools and scripts or breaks the Unix-philosophy assumption that small tools chain into larger workflows.

**Section:** `tools/` | **Subsection:** `cli/`
**Alignment:** Command Line Interface Guidelines (clig.dev) | POSIX Utility Conventions | 12-Factor CLI Apps | Click / Cobra / Clap

---

## What "CLI tooling" actually means

A *primitive* CLI tool is what gets built when "the team needs a script with arguments." It accepts some flags, prints some output, exits when done. It works for the immediate use case and falls apart at the moment someone else tries to compose it: the output is human-prose with table formatting that breaks `awk` parsing; the exit code is `0` whether the command succeeded or partially failed; the configuration is hard-coded paths in the script that don't work outside one engineer's environment; the tool prompts interactively for credentials, breaking automation; the help text is the source code. Primitive CLI tools work in their author's hands and stop working everywhere else.

A *production* CLI tool is a composable engineering primitive designed against the long Unix-philosophy tradition. Its *output format* is documented and stable: human-readable by default, structured (typically JSON) on a flag, with the structured format treated as an API contract that scripts can rely on. Its *exit codes* are first-class signals: `0` for success, distinct non-zero codes for distinct failure modes, documented in `--help`. Its *configuration* is layered: command-line flags override environment variables override config files override built-in defaults, with the precedence documented and the layering predictable. *Credentials* are read from environment variables, credential helpers, or stdin — never from command-line arguments where they leak into shell history and process listings. *Progressive disclosure* makes simple cases simple (good defaults, minimal required flags) while keeping complex cases possible (every default is overridable, every behaviour is configurable). The tool composes cleanly with pipes, scripts, and other tools because it was designed against the contract that composability requires.

The architectural shift is not "we wrote a CLI." It is: **the CLI tool is a designed primitive whose output formats, exit codes, configuration layering, credential handling, and progressive disclosure determine whether it composes into larger workflows or remains a one-author convenience that breaks the moment composition is attempted.**

---

## Six principles

### 1. Output formats are stable contracts — human-readable for terminals, structured for scripts

The most consequential design decision in a CLI tool is its output format. Humans benefit from formatted, coloured, table-aligned output; machines need structured data they can parse without regex archaeology. A tool that produces only human-formatted output forces every script using it into fragile parsing; a tool that produces only structured output is unusable in interactive terminals. The architectural discipline is *both, deliberately*: human-readable by default (when stdout is a TTY, ideally detected automatically), structured (JSON, JSONL, or equivalent) on a `--json` flag or when stdout is piped. The structured output is treated as an API contract: its schema is documented, breaking changes follow semver, additions are non-breaking. The discipline pays compound returns: scripts that use the structured format don't break when human output evolves; humans get formatting that doesn't sacrifice machine-readability.

#### Architectural implications

- Default output is human-readable: aligned tables, colours where useful, summary information.
- `--json` (or equivalent) flag emits structured output with a documented schema; the schema is treated as an API contract.
- TTY detection: when stdout is piped, the tool automatically switches to structured output (or at least to plain text without ANSI codes that would confuse parsers).
- Output schema versioning: the structured format declares its schema version; consumers can detect and adapt to changes; breaking changes follow a deprecation path.

#### Quick test

> Pick the most-used CLI tool your team has written. What's its `--json` output schema, and where is the schema documented? If the answer is "we don't have JSON output, scripts grep the human output," the tool is forcing every consumer into fragile parsing — and the next change to the human output will break those consumers silently.

#### Reference

[Command Line Interface Guidelines (clig.dev)](https://clig.dev/) treats output-format design as a primary architectural concern, with concrete patterns for human-vs-structured output and TTY detection. [12-Factor CLI Apps](https://medium.com/@jdxcode/12-factor-cli-apps-dd3c227a0e46) provides a comprehensive checklist for CLI design that covers output formats and other production concerns.

---

### 2. Exit codes are first-class signals — distinct codes for distinct failure modes

A CLI tool that returns `0` on success and `1` on any failure tells its caller "something went wrong" without saying *what*. Scripts that need to handle different failures differently (retry on transient error, escalate on auth failure, report on data error) can't, because the exit code doesn't carry the information. The architectural discipline is to use exit codes as first-class signals: `0` for success; `1` for general error; specific non-zero codes for specific failure classes (auth failures, validation errors, network errors, configuration errors, rate-limit errors); codes documented in `--help` output and in the tool's documentation. The convention follows POSIX where possible (`64-78` for usage errors, etc.) and extends with tool-specific codes for the failure modes the tool actually has.

#### Architectural implications

- Exit codes are documented per tool: `0` success; specific codes for each failure class the tool reports.
- The exit codes are stable across versions; new failure classes get new codes rather than reusing existing ones.
- Scripts using the tool can switch on exit code to handle different failures appropriately.
- The `--help` output includes the exit code reference so consumers don't have to read source.

#### Quick test

> Pick a CLI tool your team has written that's used in scripts. What exit codes does it return, and how do the consuming scripts handle them? If the answer is "0 or non-zero, scripts treat all non-zero the same," the tool is leaving the calling scripts unable to handle different failures differently — and the script either retries on auth failures (wasted) or fails on transient network errors (lost work).

#### Reference

[POSIX Utility Conventions](https://pubs.opengroup.org/onlinepubs/9699919799/basedefs/V1_chap12.html) covers the canonical exit code conventions. [Command Line Interface Guidelines (clig.dev)](https://clig.dev/) treats exit code design at practitioner depth with examples of failure-class-specific codes.

---

### 3. Configuration is layered — flags override env vars override config files override defaults

A CLI tool with only command-line flags requires every invocation to specify the same options, which doesn't scale. A tool with only configuration files requires the file to exist and be in the right place, which doesn't compose with one-off scripts. A tool with only environment variables loses the ability to override per-invocation. The architectural answer is *layered configuration* with documented precedence: built-in defaults form the base; configuration files override defaults; environment variables override config files (for runtime context); command-line flags override environment variables (for explicit per-invocation overrides). The precedence is stable, documented, and predictable. The discipline supports both simple cases (no config needed, defaults work) and complex cases (full configuration via files, with per-invocation overrides via flags).

#### Architectural implications

- The configuration precedence is documented: defaults < config file < environment variable < command-line flag (or equivalent ordering, but documented).
- Each configurable value is settable through any of the layers; the tool's logic checks them in precedence order.
- Configuration files have a documented schema and location convention (e.g., `~/.config/<tool>/config.toml` following XDG Base Directory; `/etc/<tool>/config.toml` for system-wide).
- Environment variables follow a documented prefix (e.g., `MYTOOL_API_URL` for the `api.url` config) and are documented alongside their flag equivalents.

#### Quick test

> Pick a CLI tool your team uses across multiple environments (dev, staging, production). How is environment-specific configuration handled — config files per environment, environment variables, command-line flags? If the answer is "we set everything via flags every time," the tool isn't supporting the configuration layering that operational use requires — and the friction shows up as long, error-prone command lines.

#### Reference

[Command Line Interface Guidelines (clig.dev)](https://clig.dev/) covers the configuration layering pattern at practitioner depth. [12-Factor App](https://12factor.net/) treats environment-variable configuration as a primary discipline (Factor III) that transfers to CLI tools. Frameworks like [Click](https://click.palletsprojects.com/), [Cobra](https://cobra.dev/), and [Clap](https://docs.rs/clap/latest/clap/) operationalise the layered-configuration pattern.

---

### 4. Credentials never on the command line — env vars, credential helpers, or stdin

A CLI tool that accepts credentials as command-line arguments leaks them into shell history (`.bash_history`, `.zsh_history`), process listings (`ps aux` shows all running processes including their arguments), and CI logs that capture full commands. A credential leaked once is leaked forever. The architectural discipline is to *never accept credentials as command-line arguments*. The alternatives are: *environment variables* (still visible to processes that can read `/proc/<pid>/environ`, but not in shell history); *credential helpers* (the tool calls out to a configured helper command — `git`'s `credential.helper` is the canonical example — that returns the credential securely); *stdin* (the tool reads from stdin when credential is needed, allowing pipelines like `secret-store get token | mytool --token-from-stdin`); *config files with restrictive permissions* (mode 0600, owned by the user, and the tool refuses to read them if permissions are too open). The choice depends on the use case; the prohibition on command-line args is universal.

#### Architectural implications

- The tool documents that credentials must not be passed as command-line arguments and provides clear alternatives (env var name, stdin flag, credential helper integration, secure config file path).
- If a flag for credentials exists for backwards compatibility, the tool emits a warning to stderr when used and recommends the secure alternative.
- Config files containing credentials are permission-checked; the tool refuses to use them if mode is too open (group/world-readable).
- Integration with system credential stores (macOS Keychain, Windows Credential Manager, Linux Secret Service) is offered where available, with documented fallbacks.

#### Quick test

> Pick a CLI tool your team has written that handles authentication. How are credentials passed to it? If the answer is "via a `--password` flag" or "via an `--api-key` flag," credentials are leaking into shell history, process listings, and CI logs every time the tool is invoked — and one of those leaks will eventually be the source of a security incident.

#### Reference

[Bash Pitfalls — Common Bash Mistakes](https://mywiki.wooledge.org/BashPitfalls) covers the credential-on-command-line issue in operational depth. [Command Line Interface Guidelines (clig.dev)](https://clig.dev/) treats credential handling as a primary security concern. The credential-helper pattern from `git` is the canonical model; modern tools like `gh` (GitHub CLI), `aws`, `gcloud`, and `kubectl` follow similar patterns.

---

### 5. Progressive disclosure — simple cases simple, complex cases possible

A tool that requires extensive configuration for every invocation has poor UX even when it's powerful. A tool with strong defaults and minimal required arguments has good UX even when its power is hidden. The architectural discipline is *progressive disclosure*: the simple case (the most common use of the tool) requires minimal arguments; complex cases (less common, but still important) are achievable by overriding defaults. Defaults are chosen for the most common case; non-default values are full citizens (every default is overridable, no behaviour is hard-coded), but the user pays the configuration cost only when their case requires it. The principle: *easy things should be easy; hard things should be possible*.

#### Architectural implications

- Default values are chosen for the most common use case, with the rationale documented (and revisited as usage patterns evolve).
- Every default is explicitly overridable through the configuration layering; no behaviour is hard-coded such that overriding requires editing source.
- The `--help` output presents the simple case first and offers `--help-advanced` or sectioned help for complex cases.
- Common workflows are supported by sub-commands or aliases that bundle the right defaults: `mytool deploy` does the right thing for the common deploy case; `mytool deploy --strategy=blue-green --canary-percentage=5` is also supported.

#### Quick test

> Pick a CLI tool your team has written. What's the typical command-line invocation length for the most common use case? If the answer is "20+ characters of flags every time," the defaults aren't matching the common case — and the friction is paid every invocation.

#### Reference

[Command Line Interface Guidelines (clig.dev)](https://clig.dev/) treats progressive disclosure as a primary UX principle. The `git` CLI's evolution toward better defaults (e.g., `git switch` and `git restore` replacing the overloaded `git checkout`) is a case study in progressive disclosure applied to a long-lived CLI surface.

---

### 6. Composability with pipes and scripts is the architectural payoff — the tool fits into larger workflows

The Unix philosophy's central architectural commitment is *composition*: small tools do one thing well, and complex workflows are composed by piping and chaining the tools together. A CLI tool that doesn't compose is a dead end — it's useful for the immediate task and breaks any attempt to use it as a building block. The architectural discipline is to design for composition: stdout for primary output (so it can be piped); stderr for status and errors (so they don't pollute the pipe); structured output on demand (so downstream tools can parse cleanly); exit codes that scripts can switch on; no interactive prompts in non-interactive contexts; signal handling that respects pipeline cancellation (SIGPIPE on closed downstream). A tool designed for composition becomes a primitive that other tools build on; a tool designed only for direct invocation becomes a leaf that nothing builds on.

#### Architectural implications

- stdout carries the primary output (the data the user is asking for); stderr carries status, progress, and errors. Mixing them breaks pipes.
- The tool detects whether stdout is a TTY: when it is, human-formatted output is appropriate; when it's piped, structured or plain output without ANSI codes is appropriate.
- Interactive prompts are suppressed in non-interactive contexts (when stdin is not a TTY, or when a `--no-prompt` flag is set, or when running under CI environment variables).
- Signal handling is correct: SIGPIPE causes graceful exit when a downstream consumer closes its end of the pipe; SIGINT and SIGTERM are handled cleanly without leaving partial state.

#### Quick test

> Pick a CLI tool your team has written. Compose it in a pipeline: `mytool list --json | jq '...' | other-tool`. Does it work? Does the JSON output have a stable schema? Does `mytool` exit cleanly when the pipeline is broken (e.g., `head -1` consumed the first line and closed)? If composition fails or behaves unexpectedly, the tool is unfit for the workflows it was supposed to enable.

#### Reference

[Command Line Interface Guidelines (clig.dev)](https://clig.dev/) treats composability as a primary architectural concern. The original Unix philosophy — articulated in *The Art of Unix Programming* by Eric Raymond and other foundational texts — is the source; modern restatements in clig.dev capture the same principles for current CLI design.

---

## CLI Tool Execution States

The diagram below shows the canonical CLI tool execution as a state machine: parsing arguments → validating → authenticating (if credentials are needed) → executing the requested action → formatting output for the appropriate destination (TTY vs pipe) → emitting exit code. Each state has documented transitions for both success and the failure modes the tool reports through specific exit codes.

---

## Common pitfalls when adopting CLI-tooling thinking

### ⚠️ Output format that's only human-readable

Scripts that need to consume the tool resort to grep, awk, regex parsing of the human output. The next change to the human format silently breaks every consumer.

#### What to do instead

Both formats: human-readable by default, structured (JSON) on `--json` or when stdout is piped. Structured format is treated as an API contract with documented schema and versioning.

---

### ⚠️ Exit code 0 on success, 1 on any failure

Scripts can't distinguish auth failures (don't retry) from network errors (retry with backoff) from data errors (escalate). They handle all failures the same way, which means they handle all failures wrong for some.

#### What to do instead

Distinct exit codes for distinct failure classes. Documented in `--help` and in tool docs. Stable across versions. Scripts switch on exit code to handle each failure appropriately.

---

### ⚠️ Configuration only via flags

Every invocation requires the same options. Long, error-prone command lines. No way to set sensible defaults per-environment.

#### What to do instead

Layered configuration: defaults < config files < environment variables < flags. Documented precedence. Each value settable through any layer. Common workflows have sensible defaults; per-invocation overrides remain available.

---

### ⚠️ Credentials passed via command-line flags

Credentials leak into shell history, process listings, and CI logs. Every invocation is a potential security incident.

#### What to do instead

Credentials via environment variables, stdin, credential helpers, or secure config files. Tool warns and recommends secure alternative if a credential flag exists for backwards compatibility.

---

### ⚠️ stdout and stderr mixed

Status messages, progress bars, and errors all go to stdout. Pipes break because downstream tools see the status messages as data.

#### What to do instead

stdout for primary output (data); stderr for status, progress, errors. SIGPIPE handled gracefully. Interactive prompts suppressed when stdin/stdout aren't TTYs. The tool composes cleanly with pipes and scripts.

---

## Adoption checklist

|   | Criterion |   |
|---|---|---|
| 1 | Output is human-readable by default; structured (JSON) on `--json` flag or when stdout is piped ‖ TTY detection automatic. Structured format treated as API contract with documented schema and versioning. Both formats first-class. | ☐ |
| 2 | Exit codes are first-class signals — distinct codes for distinct failure classes ‖ 0 for success; specific non-zero codes for auth/network/validation/config errors. Documented in `--help`. Stable across versions. Scripts can switch on exit code. | ☐ |
| 3 | Configuration is layered with documented precedence — defaults < config files < env vars < flags ‖ Each value settable through any layer. Predictable precedence. Supports both simple cases (defaults work) and complex (full overrides). | ☐ |
| 4 | Configuration files follow standard locations (XDG Base Directory or platform conventions) ‖ Predictable file locations. Schema documented. Permission-checked if containing credentials. | ☐ |
| 5 | Credentials never accepted as command-line arguments ‖ Environment variables, stdin, credential helpers, or permission-checked config files. Warning if backwards-compatible credential flag exists. | ☐ |
| 6 | Defaults match the most common use case; complex cases achievable through overrides ‖ Progressive disclosure: easy things easy, hard things possible. No behaviour hard-coded such that overriding requires source edits. | ☐ |
| 7 | stdout carries primary output; stderr carries status, progress, errors ‖ Pipes work cleanly. Status messages don't pollute the pipe. Errors visible regardless of stdout redirection. | ☐ |
| 8 | TTY detection drives output behaviour — formatted/coloured for terminals, plain/structured for pipes ‖ The same command produces appropriate output whether run interactively or in a script. ANSI codes don't end up in log files. | ☐ |
| 9 | Interactive prompts are suppressed when stdin isn't a TTY or `--no-prompt` is set ‖ The tool runs cleanly in CI and scripts without hanging on prompts. Required values are flag-settable to satisfy non-interactive use. | ☐ |
| 10 | Signal handling is correct — SIGPIPE graceful exit, SIGINT/SIGTERM clean shutdown ‖ Pipelines that close early (head -1, kill, etc.) don't produce broken-pipe errors. Cancelled commands don't leave partial state. | ☐ |

---

## Related

[`tools/ai-agents`](../ai-agents) | [`tools/scripts`](../scripts) | [`tools/validators`](../validators) | [`technology/devops`](../../technology/devops) | [`security/authentication-authorization`](../../security/authentication-authorization)

---

## References

1. [Command Line Interface Guidelines (clig.dev)](https://clig.dev/) — *clig.dev*
2. [POSIX Utility Conventions](https://pubs.opengroup.org/onlinepubs/9699919799/basedefs/V1_chap12.html) — *opengroup.org*
3. [12-Factor CLI Apps](https://medium.com/@jdxcode/12-factor-cli-apps-dd3c227a0e46) — *medium.com*
4. [12-Factor App](https://12factor.net/) — *12factor.net*
5. [Click — Python CLI Framework](https://click.palletsprojects.com/) — *click.palletsprojects.com*
6. [Cobra — Go CLI Framework](https://cobra.dev/) — *cobra.dev*
7. [Clap — Rust CLI Framework](https://docs.rs/clap/latest/clap/) — *docs.rs*
8. [Bash Pitfalls](https://mywiki.wooledge.org/BashPitfalls) — *mywiki.wooledge.org*
9. [shellcheck — Bash Linter](https://www.shellcheck.net/) — *shellcheck.net*
10. [XDG Base Directory Specification](https://specifications.freedesktop.org/basedir-spec/basedir-spec-latest.html) — *freedesktop.org*
