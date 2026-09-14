.PHONY: check check-python check-shell check-node check-skills check-skills-sh check-skills-sh-strict test-validation check-khaos-smoke check-learn-patch

PYTHON ?= python3
NODE ?= node

check: check-python check-shell check-node check-skills check-skills-sh check-khaos-smoke check-learn-patch

check-python:
	$(PYTHON) scripts/check-python-syntax.py

check-shell:
	$(PYTHON) scripts/check-shell-syntax.py

check-node:
	$(NODE) --check social-carousel/export.js
	$(NODE) --experimental-strip-types skills/agent-workflows/skill-cleaner/scripts/skill-cleaner.ts --help > /dev/null

check-skills:
	$(PYTHON) scripts/validate-skills.py

check-skills-sh:
	$(PYTHON) scripts/validate_skills_sh.py

check-skills-sh-strict:
	$(PYTHON) scripts/validate_skills_sh.py --strict

test-validation:
	$(PYTHON) -m unittest tests/test_validate_skills_sh.py

check-khaos-smoke:
	$(PYTHON) scripts/check-khaos-smoke.py

check-learn-patch:
	$(PYTHON) skills/agent-workflows/learn/scripts/tests/test_learn_patch.py
