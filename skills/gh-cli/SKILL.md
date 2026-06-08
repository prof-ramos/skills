---
name: gh-cli
description: "Always use when the user needs to work with GitHub from the command line — create or merge PRs, manage issues, run Actions workflows, create releases, manage repos, or automate any GitHub operation. Trigger on: 'gh pr', 'create pull request', 'GitHub CLI', 'gh issue', 'run workflow', 'gh release', 'merge PR', 'clone repo with gh', or any GitHub operation via terminal."
---

# GitHub CLI (gh)

Comprehensive reference for GitHub CLI (gh) - work seamlessly with GitHub from the command line.

## Quick Start

```bash
# Verify installation
gh --version
```

### Authentication

```bash
gh auth login
gh auth status
```

### Common Workflows

```bash
# Create PR from issue
gh issue develop 123 --branch feature/issue-123
git add . && git commit -m "Fix issue #123" && git push
gh pr create --title "Fix #123" --body "Closes #123"

# Repository setup
gh repo create my-project --public --clone --gitignore python --license mit

# CI/CD run and watch
RUN_ID=$(gh workflow run ci.yml --ref main --jq '.databaseId')
gh run watch "$RUN_ID"

# Fork sync workflow
gh repo fork original/repo --clone
gh repo sync

# Bulk close stale issues
gh issue list --search "label:stale" --json number --jq '.[].number' | \
  xargs -I {} gh issue close {} --comment "Closing as stale"
```

## Usage

This skill provides full command references for all `gh` subcommands. See [REFERENCE.md](REFERENCE.md) for the complete reference organized by:

- **Authentication** (`gh auth`) - login, status, token, refresh, switch, setup-git
- **Repositories** (`gh repo`) - create, clone, list, view, edit, delete, fork, sync
- **Issues** (`gh issue`) - create, list, view, edit, close, comment, pin, transfer
- **Pull Requests** (`gh pr`) - create, list, view, checkout, merge, review, revert
- **GitHub Actions** (`gh run`, `gh workflow`, `gh cache`, `gh secret`, `gh variable`)
- **Projects** (`gh project`) - create, edit, fields, items
- **Releases** (`gh release`) - create, upload, download, verify
- **Gists** (`gh gist`)
- **Codespaces** (`gh codespace`)
- **Search** (`gh search`) - code, commits, issues, PRs, repos
- **Labels, SSH keys, GPG keys**
- **API** (`gh api`) - REST and GraphQL
- **Extensions, Aliases, Configuration**
- **Global flags and output formatting**
- **Best practices and environment setup**

## Environment Variables

```bash
export GH_TOKEN=ghp_xxxxxxxxxxxx
export GH_HOST=github.com
export GH_PROMPT_DISABLED=true
export GH_EDITOR=vim
export GH_PAGER=less
export GH_TIMEOUT=30
export GH_REPO=owner/repo
```

## Shell Integration

```bash
eval "$(gh completion -s bash)"  # or zsh/fish
alias gs='gh status'
alias gpr='gh pr view --web'
alias gir='gh issue view --web'
alias gco='gh pr checkout'
```

## Getting Help

```bash
gh --help
gh pr --help
gh help formatting
gh help environment
gh help exit-codes
```

## References

- Official Manual: https://cli.github.com/manual/
- GitHub Docs: https://docs.github.com/en/github-cli
- REST API: https://docs.github.com/en/rest
- GraphQL API: https://docs.github.com/en/graphql
