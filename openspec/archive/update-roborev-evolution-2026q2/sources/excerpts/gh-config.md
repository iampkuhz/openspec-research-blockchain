# Excerpt: GH-CONFIG - Config and Hook System

**Source**: internal/config/config.go
**Source ID**: GH-CONFIG
**URL**: https://raw.githubusercontent.com/roborev-dev/roborev/main/internal/config/config.go
**Extracted At**: 2026-04-20

## Content

### HookConfig (beads support)

```go
type HookConfig struct {
    Event   string `toml:"event"`
    Command string `toml:"command"`
    Type    string `toml:"type"`                 // "beads" or "webhook"; empty or "command" runs Command
    URL     string `toml:"url" sensitive:"true"` // webhook destination
}
```

### Config key fields

```go
type Config struct {
    DefaultAgent         string `toml:"default_agent"`
    MaxWorkers           int    `toml:"max_workers"`
    ServerAddr           string `toml:"server_addr"`
    ReviewAgent          string `toml:"review_agent"`
    // ... per-workflow agent/model config
    AllowUnsafeAgents    *bool  `toml:"allow_unsafe_agents"`
    DisableCodexSandbox  bool   `toml:"disable_codex_sandbox"`
    AnthropicAPIKey      string `toml:"anthropic_api_key"`
}
```

### README mentions beads

From README: "Built-in beads (https://github.com/steveyegge/beads) integration creates trackable issues from review failures automatically."

## Relevance

- **beads is a hook type**: The `HookConfig.Type` field supports "beads" as a value. This means beads is integrated as a configurable hook mechanism, not as a deep architectural component.
- **beads DOES exist in the codebase**: Contrary to the baseline artifact's claim that "beads 集成不存在", beads IS referenced in both the README and the config struct. It's a hook integration, not a major architectural feature.
- **Rich per-workflow config**: The Config struct has separate agent/model settings for review, refine, fix, security, and design workflows.
