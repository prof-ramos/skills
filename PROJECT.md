# Project: resend-api Skill Development

## Overview
Desenvolvimento de uma Agent Skill de automação especialista na API Resend (`resend-api`), cobrindo envio de e-mails transacionais (text/HTML), gestão de domínios, chaves de API, tratamento de webhooks, templates de e-mail e tratamento de erros.

## Architecture & Code Layout
- Target Skill Directory: `skills/automation/resend-api/`
  - `SKILL.md`: Main Agent Skill specification with YAML frontmatter (`name: resend-api`)
  - `references/`: Detailed Markdown documentation on REST endpoints, SDKs (Node.js/Python), Webhooks signature verification, and Email Templates (HTML/React).
  - `scripts/`: Helper utilities and scripts for testing or interacting with Resend API endpoints / webhook verification.
- System Integration:
  - `skills.sh.json`: Add `"resend-api"` to grouping "Automation & Integrations".
  - `README.md`: Add row for `resend-api` under Automation table.

## Milestones
| # | Name | Scope | Dependencies | Status |
|---|------|-------|-------------|--------|
| 1 | Skill Specification | Create `skills/automation/resend-api/SKILL.md` with complete trigger-oriented description and operational guide | None | DONE |
| 2 | Technical References & Scripts | Create `references/*.md` (REST, Node/Python SDK, Webhooks, Templates) and `scripts/` | M1 | DONE |
| 3 | Ecosystem Registration & Verification | Update `skills.sh.json`, `README.md`, run and pass 100% `make check` | M1, M2 | DONE |

## Interface Contracts & Validation
- YAML frontmatter must validate with `python3 scripts/validate-skills.py`.
- `make check` must pass cleanly (0 errors, 0 warnings).
