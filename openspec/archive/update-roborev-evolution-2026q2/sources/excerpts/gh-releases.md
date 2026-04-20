# Excerpt: RoboRev GitHub Releases (v0.5.0 - v0.52.0)

**Source ID**: GH-RELEASES
**URL**: https://github.com/roborev-dev/roborev/releases
**Type**: GitHub
**Captured At**: 2026-04-20
**Tier**: L2

## Key Release Notes

| Version | Date | Key Features |
|---------|------|-------------|
| v0.5.0 | 2026-01-09 | First release, CLI + daemon + TUI + SQLite + dual agent |
| v0.38.0 / Kiro | - | Kiro agent integration |
| v0.40.0 | 2026-03-03 | ACP protocol introduction (Coder acp-go-sdk), 3 days later: Kiro/Cursor/Pi integrations |
| v0.45.0 | - | fix/refine closed loop |
| v0.47.0 | - | agentsview integration |
| v0.48.0 | 2026-03-18 | Worktree sandbox (git worktree --detach), solves .git/index.lock race |
| v0.49.0 | 2026-03-24 | Unix domain socket for CLI-to-daemon communication |
| v0.50.0 | 2026-04-01 | systemd integration (service + socket units, socket activation) |
| v0.51.0 | 2026-04-09 | OpenAPI schema-driven endpoints (Huma) |
| v0.52.0 | - | Latest |

Notable features from releases:
- PR comment upsert and review matrix support
- CI review: GitHub Actions, CircleCI, Azure DevOps, GitLab CI
- `auto_close_passing_reviews` configuration
- `roborev insights` command
- `roborev compact` command
- PR #3 Copilot CLI, PR #5 OpenCode
- PR #33 JSONL event stream
- Husky git hook manager support

## Relevance

Direct evidence for evolution stage boundaries. ACP introduction (v0.40.0), fix/refine (v0.45.0), sandbox (v0.48.0), systemd (v0.50.0), OpenAPI (v0.51.0) are the key architectural milestones.
