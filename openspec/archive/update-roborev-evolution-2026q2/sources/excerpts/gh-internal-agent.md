# Excerpt: GH-INTERNAL-AGENT - Agent Architecture

**Source**: internal/agent/ directory and source files
**Source ID**: GH-INTERNAL-AGENT
**URL**: https://github.com/roborev-dev/roborev/tree/main/internal/agent
**Extracted At**: 2026-04-20

## Content

### Agent Interface (agent.go)

```go
type Agent interface {
    Name() string
    Review(ctx context.Context, repoPath, commitSHA, prompt string, output io.Writer) (result string, err error)
    WithReasoning(level ReasoningLevel) Agent
    WithAgentic(agentic bool) Agent
    WithModel(model string) Agent
    CommandLine() string
}
```

### Dual-Path Architecture

The agent package contains TWO integration paths:

1. **Direct CLI Agents** (one file per agent):
   - codex.go, claude.go, copilot.go, gemini.go, opencode.go, kilo.go, kiro.go, cursor.go, pi.go, droid.go
   - Each implements the Agent interface by spawning the agent's CLI tool

2. **ACP Agent** (acp_agent.go):
   - Uses `github.com/coder/acp-go-sdk` for JSON-RPC communication
   - Configurable via ACPAgentConfig (command, args, model, read_only_mode, auto_approve_mode)
   - Default command: `acp-agent`

### Registry Pattern

Agents are registered via `Register(a Agent)` and retrieved via `Get(name string)`.
`GetAvailable(preferred, backups...)` implements fallback chain.

## Relevance

- **CLI agents were NOT replaced by ACP**: Both paths coexist in the current codebase. The existing CLI agents (codex.go, claude.go, etc.) are still present and actively maintained alongside the ACP agent.
- **ACP is a generic integration path**: It allows any agent that implements the ACP protocol to be used, without writing a dedicated `*_agent.go` file.
- **Agent resolution is flexible**: Supports aliases (e.g., "claude" -> "claude-code"), per-workflow agent/model configuration, backup agents, and fallback chains.
