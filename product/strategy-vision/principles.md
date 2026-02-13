# Operating Principles

These principles guide decision-making across the project. When in doubt, consult these before making trade-offs.

## Technical Principles

- **CLI-first.** Anything that can be done via a UI must first be doable via CLI. The CLI is the primary interface for both humans and agents. This ensures every capability is automatable and composable.
- **Composable tools, not hardcoded workflows.** Each CLI command does one thing well. We build an extensive toolkit of individual tools and let users and agents compose them as they see fit. We do not prescribe specific pipelines or workflows. Emergent behavior comes from composition, not from us anticipating every use case.
- **Stateless functions.** Library functions accept input and return output. No shared mutable state, no side effects beyond file I/O. This makes functions testable, composable, and safe for both human and agent callers.
- **CLI as thin wrapper.** CLI commands delegate to library functions. Business logic never lives in the CLI layer. This keeps the library usable from notebooks, scripts, and agents without going through Click.
- **Filesystem over databases.** We work directly with WARC files and the filesystem. No database to set up, migrate, or maintain. Portability and simplicity over query power.
- **Ephemeral environments.** No managed databases, no long-running infrastructure. An analyst should be able to load a dataset, perform analysis, store the output they care about, and tear down the environment. Nothing persists unless the user explicitly saves it.
- **Local-first, zero infrastructure.** Everything runs on the user's machine. No cloud dependencies, no accounts, no servers. Docker is optional (via devcontainer), not required.
- **Test-driven development.** Write the failing test first, then the minimal implementation, then validate. Every code change follows this cycle.

## Organizational Principles

- **Agents as senior developers.** The founder embraces autonomous agents coding and creating this CLI. Agents operate with broad autonomy at a senior/lead developer level. The founder's role is to provide high-level input, refine the agentic harness (skills, rules, strategy docs), and review output -- not to write the code.
- **Open source, open process.** The project is fully open source. Strategy, decisions, and rationale are documented in the repo alongside the code.
- **Trunk-based development.** All changes go through pull requests. No direct commits to `main`. Keep branches short-lived.
- **Documentation lives with code.** CLI reference is auto-generated. Strategy docs are in `product/`. No external wikis or docs sites to maintain.
- **Observability through telemetry.** As agents increasingly use the CLI, telemetry will help identify which tool calls succeed vs. fail, enabling data-driven improvement of the tools and the skills that teach agents to use them.

## Decision-Making Framework

When facing a trade-off, apply these principles in order of priority:

1. **User value first.** Does this help someone explore or build on CC-NEWS data faster? If not, deprioritize it.
2. **Simplicity over power.** Prefer the simpler approach unless the more complex one is demonstrably necessary. Less code, fewer dependencies, less state.
3. **Agent-compatibility as a co-equal concern.** Design for composability from the start. Structured output > pretty output. Individual tools > monolithic workflows. If a design works for humans but breaks agent composition, reconsider it.
4. **Ship incrementally.** Prefer small, complete features over large, half-finished ones. Each shipped command should be independently useful.
