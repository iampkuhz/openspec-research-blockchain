# Excerpt: GH-INTERNAL-WORKTREE - Sandbox Implementation

**Source**: internal/worktree/worktree.go
**Source ID**: GH-INTERNAL-WORKTREE
**URL**: https://raw.githubusercontent.com/roborev-dev/roborev/main/internal/worktree/worktree.go
**Extracted At**: 2026-04-20

## Content

```go
type Worktree struct {
    Dir      string // Path to the worktree directory
    repoPath string // Path to the parent repository
    baseSHA  string // SHA of the commit the worktree was detached at
}

func Create(repoPath, ref string) (*Worktree, error) {
    // ...
    wt, err := newWorktree(repoPath, ref)
    // ...
    if err = wt.initSubmodules(); err != nil { return nil, err }
    wt.maybePullLFS()
    wt.baseSHA = wt.resolveBaseSHA()
    return wt, nil
}

func newWorktree(repoPath, ref string) (*Worktree, error) {
    worktreeDir, err := os.MkdirTemp("", "roborev-worktree-")
    // ...
    // Create worktree with --detach, suppress hooks
    _, stderr, err := runGitCommand(repoPath, nil,
        "-c", "core.hooksPath="+os.DevNull,
        "worktree", "add", "--detach", worktreeDir, ref)
    // ...
}
```

## Relevance

- **Sandbox is git worktree-based**: The "sandbox" introduced in v0.48.0 is a temporary git worktree created via `git worktree add --detach`, NOT containerization (Docker) or bind mount.
- **Isolation mechanism**: Creates a temporary directory, detaches at the specified commit, disables hooks via `core.hooksPath=os.DevNull`, initializes submodules, and optionally pulls LFS files.
- **Worktree is cleaned up**: `Close()` calls `git worktree remove --force` and `os.RemoveAll`.
- **Used by refine**: The refine command uses worktrees to isolate fix/commit operations from the user's working tree.
