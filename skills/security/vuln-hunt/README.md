# vuln-hunt

**Autonomous Vulnerability Discovery Pipeline** — James Red Team Edition

Advanced red teaming tool for Hermes Agent. Implements a full closed-loop vulnerability hunting system:

### Pipeline Stages
- **Recon** — Deep source code analysis + security architecture document
- **Hunt** — Up to 50 parallel specialized agents (RLS, IDOR, PII, Drizzle, Server Actions, etc.)
- **Validate** — Independent agents attempt to refute findings
- **Gapfill** — Automatically flags under-analyzed areas
- **Dedup** — Merges duplicate root causes
- **Trace** — Confirms attacker-controlled input reaches the bug
- **Feedback Loop** — Confirmed reachable bugs spawn new targeted hunt tasks
- **Report** — Generates professional OWASP-style report with evidence

### Features
- Built on Hermes Agent skill system
- Permanent `vuln-hunt` CLI command
- Full James Red Team / GODMODE profile (uncensored)
- Integrates with `kanban-orchestrator`, `delegate_task`, and `godmode`
- Designed for large codebases (Next.js, Python, etc.)

### Installation

```bash
# The CLI is installed system-wide when you run the skill
vuln-hunt ~/your-project 40
```

### Usage

```bash
vuln-hunt .              # Current directory, 40 agents
vuln-hunt ~/intranet 50  # Specific target with 50 agents
```

Report is always saved to `/tmp/vuln-report-YYYYMMDD-HHMMSS/`

### Created with
- Hermes Agent (https://hermes-agent.nousresearch.com)
- Skill: `vuln-discovery-pipeline` v2.0

---

**Warning**: This tool is for authorized security testing only. Use responsibly.

Made by **James** — Hermes Red Team Profile. GODMODE permanently enabled.