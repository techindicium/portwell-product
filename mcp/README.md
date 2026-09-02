# Tool servers and simulated external services

Two kinds of thing live here.

**Simulated external services.** The systems the PDLC track's work has effects
against, implemented locally so exercises are reproducible and nothing in the course reaches a
real endpoint. They are servers, not mocks inside a test: the point is that the agent's action
has an observable effect somewhere outside its own process.

**Tool definitions.** Module 2 asks each group for at least two safe track-specific tools with
explicit inputs, outputs, permission boundaries, and failure behaviour. Implement them as
controlled scripts under `scripts/` or as an MCP server here.

## Declaring a server

Copy `mcp.json.example` to `.mcp.json` in the repository root. It is not committed with
credentials, and this course has none to commit.

## What a safe tool looks like here

- It takes named arguments, not a shell string.
- It validates its inputs and refuses rather than guessing.
- Its failure message names what it protects and what would fix it, in the same shape as
  `scripts/lifecycle.py` refusals.
- Its blast radius is written down in `docs/architecture-rules.md`.
- It has a test that exercises the refusal path, not only the success path.

A tool that can do anything is not a tool, it is a shell. The course never requires
unrestricted shell execution.
