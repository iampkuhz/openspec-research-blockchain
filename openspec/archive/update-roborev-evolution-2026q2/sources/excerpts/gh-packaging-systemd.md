# Excerpt: systemd Packaging Unit Files

**Source ID**: GH-PACKAGING-SYSTEMD
**URL**: https://github.com/roborev-dev/roborev/tree/main/packaging/systemd
**Type**: GitHub
**Captured At**: 2026-04-20
**Tier**: L2

## Content

Systemd unit files in `packaging/systemd/`:
- `roborev.service` - service unit for daemon
- `roborev.socket` - socket unit for socket activation

## Relevance

Confirms systemd integration details (v0.50.0). Socket activation allows the daemon to be started on-demand when a connection arrives, reducing resource usage. Used for stage 3 production readiness analysis.
