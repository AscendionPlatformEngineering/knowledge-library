# Scripts & Automation

The architectural properties of scripts that distinguish reliable automation from one-off helpers — recognising that idempotency, fail-fast error handling, logging, explicit environment assumptions, permission-context awareness, and the evolution path from script to tool are what determine whether automation accumulates as institutional capability or as the next maintenance burden.

**Section:** `tools/` | **Subsection:** `scripts/`
**Alignment:** Idempotence (CS principle) | Bash Pitfalls | Ansible / Terraform (declarative automation) | Make as Build Tool

---

## What "scripts and automation" actually means

A *primitive* script is what gets written when "this needs to happen and nobody wants to do it manually": a few lines of bash, Python, or whatever the engineer has open, run once, possibly committed to a `scripts/` folder, possibly only on the engineer's laptop. It works the first time. The second time someone runs it, the environment is slightly different and parts fail; the third time, half the steps already happened from the first run and the script doesn't know that, so it errors mid-way; the fourth time, no logs survive, so debugging the partial failure requires reading the script and reasoning about which steps did and didn't happen. Primitive scripts solve immediate problems and accumulate as technical debt.

A *production* script — automation code intended to run multiple times, possibly autonomously, possibly under conditions the original author didn't anticipate — is a designed artefact with engineering properties. *Idempotency* is the central design constraint: re-running the script produces the same final state regardless of starting state; partial completion is detectable; resumption is safe. *Fail-fast error handling* means the script halts at the first sign of trouble with an informative error, rather than silently continuing past a failure into corrupt state. *Logging and observability* mean every script run produces an operational record (what ran, what succeeded, what failed) that can be inspected later. *Environment assumptions* are explicit — the script declares what it requires (which tools, which credentials, which network access, which permissions) and validates them at start. *Permission and security context* are scoped to least privilege; scripts that need elevated permissions request them explicitly with documented rationale. *Evolution toward tools* recognises that scripts that get reused enough to matter eventually need to graduate into proper tools (with proper UX, configuration, testing, distribution).

The architectural shift is not "we have scripts." It is: **automation code that runs more than once needs idempotency, fail-fast error handling, logging, explicit environment assumptions, scoped permissions, and an evolution path to graduate into tools — and treating it as one-off helpers produces a debt category whose maintenance cost grows with every script that gets reused beyond its original use case.**

---

## Six principles

### 1. Idempotency is the central design constraint — re-running produces the same final state

The most consequential design decision in automation is whether the script is *idempotent*. An idempotent script can be run repeatedly with the same final result: if the action has already been done, re-running is a no-op; if the action is partial, re-running completes it; if the action wasn't done, re-running does it. A non-idempotent script behaves differently on each run: the first run does things, the second run errors because those things already exist, the third run silently produces the wrong state. The architectural discipline is to design scripts as *desired-state* operations rather than *imperative-action* sequences. Instead of "create user X" (which errors if X already exists), the script does "ensure user X exists" (which checks first and acts only if needed). Instead of "append line Y to config" (which produces duplicates on re-run), the script does "ensure config contains line Y" (which checks for the line and adds it only if missing). Configuration management tools (Ansible, Salt, Terraform) operationalise this discipline; the same principle applies to hand-written scripts.

#### Architectural implications

- Scripts are written in *desired-state* form: each operation begins with a check ("is this state already true?") and acts only if needed.
- Modifications to files use idempotent patterns: line-presence checks before append, full-file replacement of generated content, structured-merge for config files (rather than naive append).
- Resource creation uses *create-if-missing* semantics: `mkdir -p` rather than `mkdir`, `INSERT ... ON CONFLICT DO NOTHING` rather than naive INSERT, equivalent patterns in whatever tool.
- The script can be safely re-run after partial completion: if it failed at step 7 of 10, re-running picks up where it left off because steps 1-6 are no-ops on already-done state.

#### Quick test

> Pick a script your team uses regularly. Run it twice in a row. What happens on the second run? If errors occur on the second run because things "already exist" or "already done," the script isn't idempotent — and the next time it's needed in a recovery scenario (where re-running is the obvious response), the second run will produce the wrong outcome.

#### Reference

[Idempotence (Wikipedia)](https://en.wikipedia.org/wiki/Idempotence) covers the formal property. [Ansible](https://docs.ansible.com/) and [Salt](https://saltproject.io/) operationalise idempotency as their core design principle for configuration management. [Terraform](https://www.terraform.io/) and [Pulumi](https://www.pulumi.com/) extend idempotency to infrastructure-as-code with desired-state reconciliation.

---

### 2. Fail fast with informative errors — bad halt beats silent corruption

The default behaviour of most shells (continuing past a failed command unless explicitly told otherwise) is the opposite of what production automation needs. A script that continues past `cp source dest` (where `dest` is read-only) into the next step that operates on `dest` produces corrupted state without error. The architectural discipline is *fail fast*: the script halts at the first sign of trouble, with an informative error message that says what failed, what state the system is in, and (where possible) what to do about it. In bash, `set -euo pipefail` is the canonical opening line. In Python, exception handling is explicit at boundaries. The principle: *halting with a clear error is always better than continuing into corrupt state*.

#### Architectural implications

- Bash scripts begin with `set -euo pipefail` (or equivalent strict mode) — exit on any error, exit on undefined variable, fail on pipe errors.
- Python scripts treat exceptions as the normal failure path; bare `except:` clauses are flagged for review. Specific exception types are caught only when there's a meaningful recovery action.
- Error messages are informative: what failed, what file/resource was being operated on, what the system state is, what should be done. Generic "Error: failed" messages are flagged as defects.
- The script's exit code distinguishes success (0), expected failure modes (specific non-zero codes), and unexpected errors (general non-zero) — same discipline as proper CLI tools ([`tools/cli`](../cli)).

#### Quick test

> Pick a script your team uses. Read its first few lines. Does it set strict-mode flags (bash) or have explicit exception handling boundaries (Python)? If neither, the script is silently continuing past failures — and the next time something breaks subtly partway through, the corruption will be discovered later by an unrelated investigation.

#### Reference

[Bash Pitfalls](https://mywiki.wooledge.org/BashPitfalls) is the canonical practitioner reference for the silent-failure modes of shell scripts and how to avoid them. [shellcheck](https://www.shellcheck.net/) operationalises the lint discipline for bash scripts; running shellcheck against any non-trivial script surfaces the silent-failure modes immediately.

---

### 3. Logging and observability — script runs are operational events, not opaque

A script that runs and produces no output (when it succeeds) and a vague error (when it fails) is operationally opaque. The team that depends on the script can't tell whether it ran, what it did, or whether the actions succeeded — except by inspecting the system afterwards. The architectural discipline is to treat every script run as an *operational event* with structured logging: what script ran, with what arguments, in what environment, by which user, at what time, with what outcome. The log entries follow the same structured-logging discipline as application logs ([`observability/logs`](../../observability/logs)) — JSON or key-value records, not unstructured prose. Script runs become queryable: "show me all runs of `deploy.sh` in the last week," "find any run that failed at the database-migration step," "list all changes this script has made to production in the last quarter." The script becomes an observed citizen of the operational system rather than a black box invoked from a terminal.

#### Architectural implications

- Each script run logs its identity (script name, version, hash), its arguments, its environment context (host, user, time), and its outcome (success / specific failure mode).
- Log emission is structured (JSON or equivalent), consistent with the team's logging conventions, and routed to the same logging infrastructure as application logs.
- Significant decision points within the script are logged: which branch was taken, what the relevant signals were, what action was decided.
- For idempotent scripts, the log distinguishes "action performed" from "action skipped because already-done" — both are valid outcomes and both are valuable for audit.

#### Quick test

> Pick a script your team has been running for the last quarter. How many times has it run, and how many of those runs failed at any step? If the answer is "we don't know — we'd have to grep terminal scrollback or remember," the script's runs aren't being observed — and the operational signal it could be providing is being lost.

#### Reference

The structured-logging discipline transfers directly from [`observability/logs`](../../observability/logs). Tools like [structlog](https://www.structlog.org/) (Python), `logger -t script.name` (bash) for syslog routing, or platform-specific logging integrations operationalise this for scripts.

---

### 4. Environment assumptions are explicit — the script declares what it requires and validates it

A script that assumes Python 3.10+ is installed, that `aws` CLI is on the path, that `~/.aws/credentials` exists, that the user has SSH access to a particular host, that the working directory is the repository root — and validates none of those assumptions — fails differently on every machine that doesn't match. The errors are obscure (a missing tool surfaces as `command not found`, a missing credential as a cryptic API error), the relationship between cause and effect is unclear, and the script's actual requirements have to be inferred by reading the code. The architectural discipline is to *declare assumptions explicitly* at the top of the script and *validate them at start*. The script begins with a preflight section that checks: required tools are present, required credentials are accessible, required permissions are granted, working directory is what's expected. If any check fails, the script halts immediately with a clear error explaining what's missing and how to install or configure it.

#### Architectural implications

- The script begins with a documented "Requirements" comment block: tools needed (with versions), credentials, environment variables, network access, working directory expectations.
- A preflight function validates each requirement at script start; failures produce specific error messages explaining what's missing and how to fix it.
- The script is written to be runnable from a clean environment given the documented requirements; it doesn't depend on the engineer's specific shell aliases, tab-completion configuration, or other personal setup.
- For scripts that need elevated permissions (sudo, root), the requirement is documented explicitly and the script checks before attempting privileged operations rather than failing partway through.

#### Quick test

> Pick a script your team uses. Run it on a machine that's never run it before — perhaps a fresh container or a colleague's laptop. Does it fail with a clear message about what's missing, or does it fail with cryptic errors that require reading the source to debug? If the latter, the assumptions aren't explicit — and every new operator who needs to run this script pays the discovery cost.

#### Reference

[Make as Build Tool](https://www.gnu.org/software/make/) operationalises explicit-dependency declaration for build automation; the discipline transfers. Modern shell-script linters and CI patterns enforce dependency declaration; tools like [Click](https://click.palletsprojects.com/) for Python CLI scripts make dependency declaration part of the framework.

---

### 5. Permission and security context — scripts run somewhere with privileges; design for least-privilege

A script that runs as root because "it needs to install packages" inherits root's full capability — including the capability to do anything wrong with anything else on the system. A script that runs as the engineer in their interactive shell inherits everything the engineer can do, including any cached credentials and access tokens. Both are over-privileged for what the script actually needs. The architectural discipline is *least privilege*: the script runs with the minimum permissions required for its specific task. If only a subset of permissions are needed (e.g., write to one specific directory, call one specific API endpoint), the script's execution context is scoped to those permissions — through dedicated service accounts, capability-based filesystem access, restricted credentials, or equivalent. The same discipline that applies to AI agents ([`tools/ai-agents`](../ai-agents)) applies to scripts: the execution context is part of the script's design, not an afterthought.

#### Architectural implications

- Scripts that need elevated permissions request them explicitly (sudo, capability flag, service-account assumption) and only for the specific operations that need them — not for the script's entire runtime.
- Credentials accessible to the script are scoped to what the script needs: a deploy script has deploy credentials, not full admin credentials.
- Sensitive operations (rm -rf, drop database, force push) include explicit confirmation steps or are gated behind separate scripts that require additional authorisation.
- Scripts running in shared contexts (CI, scheduled jobs, automation hosts) use service-account credentials with documented scopes — not the credentials of whichever engineer last ran the script manually.

#### Quick test

> Pick a script your team runs in production or against production resources. What permissions does it have, and which of those does it actually need? If the answer is "it has full admin and uses maybe 10% of that capability," the blast radius of the next mistake is bounded by the full capability, not by what's needed — and that's the cost paid every time the script runs.

#### Reference

The least-privilege discipline is treated extensively in [`security/authentication-authorization`](../../security/authentication-authorization) at the system level; the same principle applies to scripts. [NIST SP 800-207 Zero Trust](https://csrc.nist.gov/publications/detail/sp/800-207/final) covers zero-trust principles that translate to scoped script execution contexts.

---

### 6. Evolution from script to tool — when reuse warrants graduation

A script that's used once is fine as a script. A script that's used once a quarter, by one engineer, is also fine as a script. A script that's used multiple times a week, by multiple engineers, in multiple environments — that's a *tool* whose UX, configuration, error handling, distribution, and testing should be designed properly. The architectural discipline is to recognise the inflection point and graduate: when a script's reuse exceeds its design, the script's properties (idempotency, fail-fast, logging, explicit environment) need to be matched by the properties of a proper CLI tool ([`tools/cli`](../cli)) — output format design, exit codes, configuration layering, distribution as a versioned package, integration testing. The graduation isn't always rewriting from scratch; often it's adding the missing properties to the existing script (a `--json` flag, distinct exit codes, configuration via environment variables) until it matures into a tool. The trigger for graduation is the *reuse pattern*, not arbitrary code metrics: a 50-line bash script used by 20 engineers across 10 environments is a tool that hasn't been packaged yet; a 5000-line Python script used once a year is a script that's grown beyond its discipline.

#### Architectural implications

- Reuse patterns are observed: how often is the script run, by how many distinct users, against how many distinct targets, with how many distinct argument variations.
- A documented threshold triggers graduation review: scripts above the threshold are evaluated against tool-quality criteria (proper CLI design, structured output, distinct exit codes, distribution mechanism, integration testing).
- Graduation paths are explicit: improve the existing script in place (add the missing properties); rewrite as a proper CLI tool in a more appropriate language; replace with an existing tool that already does the job; or recognise that the script's role is genuinely temporary and document its expected end-of-life.
- Tools that emerged from scripts maintain backward compatibility for existing users where feasible: the old `script.sh` may continue working as a wrapper that invokes the new tool, easing migration.

#### Quick test

> Pick the most-used script in your organisation. How many people run it, in how many contexts, how often? If the answer is "many people, many contexts, weekly," the script is operating at tool scale without tool discipline — and the friction cost (every user paying the script's rough edges every time) compounds with usage.

#### Reference

The script-to-tool graduation pattern is treated indirectly in [Production-Ready Microservices — Fowler](https://www.oreilly.com/library/view/production-ready-microservices/9781491965962/) and in the broader CLI-tool discipline at [Command Line Interface Guidelines (clig.dev)](https://clig.dev/). The principle: tooling discipline scales with usage, and the inflection point between script and tool is a real architectural moment.

---

## Automation Maturity Timeline

The diagram below shows the typical evolution of automation in an organisation, from primitive one-off scripts through the disciplines that distinguish maintainable automation, culminating in graduation to proper tools. Each stage adds specific properties (idempotency, error handling, logging, explicit environment, distribution) that the prior stage lacked.

---

## Common pitfalls when adopting scripts-and-automation thinking

### ⚠️ Imperative actions that can't be safely re-run

The script does "create X." Running it twice errors on the second run because X already exists. Recovery scenarios (where re-running is the obvious response) produce wrong outcomes.

#### What to do instead

Desired-state design: "ensure X exists" rather than "create X." Idempotent patterns throughout. Re-running is safe, and partial completion is recoverable.

---

### ⚠️ Continue-past-failure default

The script doesn't set strict mode in bash, doesn't have exception boundaries in Python. Failed steps continue silently into subsequent operations on bad state.

#### What to do instead

Fail fast: `set -euo pipefail` in bash, explicit exception handling in Python. Halt with informative errors. Bad halt beats silent corruption.

---

### ⚠️ No logging — scripts are operationally opaque

The script ran. Or did it? It succeeded? Did all the steps work? Nobody knows without inspecting the system afterwards.

#### What to do instead

Structured logging of every run: identity, arguments, context, outcome. Significant decision points logged. Routed to the same infrastructure as application logs. Script runs become observable, queryable events.

---

### ⚠️ Environment assumptions undocumented and unvalidated

The script assumes specific tools, versions, credentials, paths. None are validated at start. Failures on machines that don't match are obscure.

#### What to do instead

Documented Requirements block at top. Preflight function validates assumptions at script start. Clear errors with installation/configuration guidance for missing requirements.

---

### ⚠️ Scripts running with permissions far broader than they need

The script runs as root because it once needed to install something. Or as the engineer with full admin access. The blast radius of the next mistake matches the full capability, not the actual need.

#### What to do instead

Least privilege: scoped execution contexts, dedicated service accounts, restricted credentials. Elevated permissions requested explicitly only for the operations that need them. Sensitive operations behind explicit confirmation or separate scripts.

---

## Adoption checklist

|   | Criterion |   |
|---|---|---|
| 1 | Scripts are written in desired-state form — "ensure X" rather than "create X" ‖ Each operation begins with a check; action only if needed. Re-running produces consistent state. Partial completion is recoverable. | ☐ |
| 2 | Idempotent patterns throughout — line-presence checks before append, structured merge for config, create-if-missing for resources ‖ Re-running produces the same final state regardless of starting state. Recovery scenarios use re-run as the natural action. | ☐ |
| 3 | Bash scripts begin with `set -euo pipefail`; Python scripts have explicit exception handling boundaries ‖ Fail fast at first sign of trouble. Bad halt beats silent corruption. Errors don't continue into subsequent operations. | ☐ |
| 4 | Error messages are informative — what failed, in what context, what to do about it ‖ Generic "Error: failed" messages are flagged as defects. The next operator who hits the error gets actionable guidance, not a mystery. | ☐ |
| 5 | Each script run produces structured log entries — identity, arguments, environment, outcome ‖ Routed to the same logging infrastructure as application logs. Significant decision points logged. Script runs become queryable operational events. | ☐ |
| 6 | The script's Requirements block at top documents tools, versions, credentials, network access, permissions ‖ Explicit declaration. The script can be run from a clean environment given documented requirements. | ☐ |
| 7 | A preflight function validates each requirement at script start with specific error messages ‖ Failures produce clear "what's missing and how to fix it" output. Discovery cost paid once at start, not throughout the run. | ☐ |
| 8 | Scripts that need elevated permissions request them explicitly and scope to the operations needing them ‖ Not "run as root for the whole script." Specific privileged operations bracketed; the rest runs as a normal user. | ☐ |
| 9 | Scripts running in shared contexts use service-account credentials with documented scopes ‖ Not the credentials of whichever engineer last ran them manually. The script's identity is its own, with appropriate audit trail. | ☐ |
| 10 | Reuse patterns are observed; scripts at tool-scale usage are graduated to proper tools ‖ Reuse-pattern threshold triggers graduation review. Documented graduation paths: improve in place, rewrite, replace, or end-of-life. The script-to-tool inflection is recognised, not ignored. | ☐ |

---

## Related

[`tools/ai-agents`](../ai-agents) | [`tools/cli`](../cli) | [`tools/validators`](../validators) | [`runbooks/incident`](../../runbooks/incident) | [`technology/devops`](../../technology/devops) | [`observability/logs`](../../observability/logs)

---

## References

1. [Idempotence (Wikipedia)](https://en.wikipedia.org/wiki/Idempotence) — *Wikipedia*
2. [Bash Pitfalls](https://mywiki.wooledge.org/BashPitfalls) — *mywiki.wooledge.org*
3. [shellcheck — Bash Linter](https://www.shellcheck.net/) — *shellcheck.net*
4. [Ansible — Configuration Management](https://docs.ansible.com/) — *docs.ansible.com*
5. [Salt — Configuration Management](https://saltproject.io/) — *saltproject.io*
6. [Terraform — Infrastructure as Code](https://www.terraform.io/) — *terraform.io*
7. [Pulumi — Infrastructure as Code](https://www.pulumi.com/) — *pulumi.com*
8. [Make as Build Tool](https://www.gnu.org/software/make/) — *gnu.org*
9. [Command Line Interface Guidelines (clig.dev)](https://clig.dev/) — *clig.dev*
10. [12-Factor App](https://12factor.net/) — *12factor.net*
