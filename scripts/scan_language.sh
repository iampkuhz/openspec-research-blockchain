#!/usr/bin/env bash
set -euo pipefail

rg -n \
  '(^# [A-Z][A-Za-z ]+$|^## [A-Z][A-Za-z ]+$|^### [A-Z][A-Za-z ]+$|One-line definition|Role in this topic|Easily confused with|Minimal example|Purpose|Requirements|Scenario Definition|Hard Constraints|Soft Preferences|Open Questions|Current Status|Evidence Matrix|Dependency Map|Source Planning)' \
  . \
  -g '!/.git' \
  -g '!.idea/**' \
  -g '!scripts/scan_language.sh' \
  -g '!*.png' \
  -g '!*.jpg' \
  -g '!*.svg' \
  -g '!*.DS_Store' || true
