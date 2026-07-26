.PHONY: check check-python check-shell check-node check-skills check-khaos-smoke check-learn-patch

PYTHON ?= python3
NODE ?= node

check: check-python check-shell check-node check-skills check-khaos-smoke check-learn-patch

check-python:
	$(PYTHON) scripts/check-python-syntax.py

check-shell:
	$(PYTHON) scripts/check-shell-syntax.py

check-node:
	$(NODE) --check carrossel-instagram/export.js
	$(NODE) --experimental-strip-types --check skills/agent-workflows/skill-cleaner/scripts/skill-cleaner.ts

check-skills:
	$(PYTHON) scripts/validate-skills.py

check-khaos-smoke:
	$(PYTHON) scripts/check-khaos-smoke.py

check-learn-patch:
	$(PYTHON) skills/agent-workflows/learn/scripts/tests/test_learn_patch.py
