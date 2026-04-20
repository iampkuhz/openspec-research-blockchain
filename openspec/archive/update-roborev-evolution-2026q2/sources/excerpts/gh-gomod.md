# Excerpt: GH-GOMOD - Dependency Manifest

**Source**: RoboRev go.mod
**Source ID**: GH-GOMOD
**URL**: https://raw.githubusercontent.com/roborev-dev/roborev/main/go.mod
**Extracted At**: 2026-04-20

## Content

```
module github.com/roborev-dev/roborev
go 1.25.0

require (
    github.com/coder/acp-go-sdk v0.6.3
    github.com/charmbracelet/bubbletea v1.3.10
    github.com/coreos/go-systemd/v22 v22.7.0
    github.com/danielgtaylor/huma/v2 d2.37.3
    github.com/jackc/pgx/v5 v5.9.1
    modernc.org/sqlite v1.48.2
    ...
)
```

## Relevance

- **ACP is from Coder**: `github.com/coder/acp-go-sdk` confirms ACP is an **external SDK by Coder** (the company behind code-server), not an internal RoboRev protocol. This corrects the baseline artifact's claim that ACP is "RoboRev 内部的 JSON-RPC 协议".
- **PostgreSQL support**: `github.com/jackc/pgx/v5` confirms PostgreSQL is now a supported storage backend, not SQLite-only.
- **systemd integration**: `github.com/coreos/go-systemd/v22` confirms native systemd integration.
- **OpenAPI**: `github.com/danielgtaylor/huma/v2` confirms Huma framework for OpenAPI schema-driven endpoints.
- **Bubble Tea**: `github.com/charmbracelet/bubbletea` confirms TUI framework.
- **SQLite**: `modernc.org/sqlite` confirms pure-Go SQLite (no CGO dependency).
