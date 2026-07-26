#!/usr/bin/env python3
"""Render shared/agent-prompt.template.md into one runtime's agent.md.

The template holds the ~90% of the autoreview prompt that's identical across
runtimes. What genuinely varies -- the skills-path prefix and the tool
enforcement paragraph, because the underlying permission mechanisms differ
(OpenCode's frontmatter bash-permission table vs. Claude Code's coarse `tools`
array needing prose enforcement) -- is substituted in. Frontmatter is not
templated: the two runtimes' agent-definition schemas are genuinely different,
not just cosmetically, so each keeps its own small frontmatter file.

Usage:
    python3 render_agent_prompt.py <runtime> <prefix> > out.md

<runtime> selects shared/frontmatter.<runtime>.yaml and
shared/tool-restrictions.<runtime>.md. <prefix> is substituted for {{PREFIX}}
(e.g. ".opencode/skills/autoreview" or ".claude/skills/autoreview").
"""

from __future__ import annotations

import sys
from pathlib import Path

SHARED_DIR = Path(__file__).resolve().parent


def render(runtime: str, prefix: str) -> str:
    frontmatter = (SHARED_DIR / f"frontmatter.{runtime}.yaml").read_text(encoding="utf-8")
    tool_restrictions = (SHARED_DIR / f"tool-restrictions.{runtime}.md").read_text(encoding="utf-8")
    template = (SHARED_DIR / "agent-prompt.template.md").read_text(encoding="utf-8")

    body = template.replace("{{TOOL_RESTRICTIONS}}", tool_restrictions).replace("{{PREFIX}}", prefix)
    return frontmatter + "\n" + body


def main() -> int:
    if len(sys.argv) != 3:
        print("usage: render_agent_prompt.py <runtime> <prefix>", file=sys.stderr)
        return 2
    sys.stdout.write(render(sys.argv[1], sys.argv[2]))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
