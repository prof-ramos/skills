# Vulnerability Validation Rubric

## Overview

Every finding from a discovery trail must pass through adversarial validation before being accepted into the final findings set. A **validator** independently reviews the finding to determine whether it is real, exploitable, and correctly severity-rated. The validator must not have authored the original finding.

---

## Validation Levels

| Level | Label | Meaning |
|:-----:|-------|---------|
| V5 | **Confirmed** | The finding is real, reproducible, and the described exploit path works as stated. |
| V4 | **Plausible** | The finding is likely real, but full reproduction was not achieved or a minor detail is off. |
| V3 | **Possible** | The finding could be real, but significant uncertainty exists (e.g., untested environment assumption, incomplete PoC). |
| V2 | **Unlikely** | The exploit path has a fundamental flaw or the impact is overstated; the finding is probably not real as described. |
| V1 | **False positive** | The finding is not a vulnerability; the observed behavior is expected, mitigated, or misinterpreted. |

---

## Criteria for Each Level

### Confirmed (V5)

- The exploit path has been independently reproduced end-to-end.
- The impact matches the description (e.g., data actually exfiltrated, command actually executed).
- The severity rating is consistent with the severity criteria matrix.
- No significant mitigating factor was missed.

**Example**: Validator sends `POST /api/users` with `role=admin` and successfully creates an admin user from a regular-user session. Impact matches, exploit works, severity (High) is correct → Confirmed.

### Plausible (V4)

- The core vulnerability mechanism is real (e.g., the code path exists, the input is not sanitized).
- Full end-to-end exploitation was not completed, but partial evidence supports the claim (e.g., the injection point reflects input, but data exfiltration wasn't confirmed).
- The severity is reasonable but may need minor adjustment.

**Example**: Validator confirms a reflected XSS injection point and sees the payload in the response, but the Content-Security-Policy header blocks script execution. The XSS is real in the code but currently mitigated → Plausible (with a note about the CSP mitigation).

### Possible (V3)

- The theoretical basis for the finding is sound, but reproduction was not achieved and there are unverified assumptions.
- The attack may require specific environmental conditions that could not be replicated.
- The severity may be overstated due to untested assumptions.

**Example**: A finding claims a race condition in a file-lock mechanism could lead to privilege escalation. The code shows the race window exists, but the validator could not trigger it in 1,000 attempts. The mechanism is theoretically possible but not demonstrated → Possible.

### Unlikely (V2)

- The described exploit path has a fundamental issue (e.g., a required precondition cannot be met, a security boundary was overlooked).
- The impact description conflates unrelated behavior with a vulnerability.
- The code path may exist but is provably unreachable or mitigated.

**Example**: A finding claims SQL injection in a parameter, but inspection shows the parameter is passed through a parameterized query via an ORM. The "injection" is in a log string, not the SQL query → Unlikely.

### False Positive (V1)

- The observed behavior is expected functionality, not a vulnerability.
- The finding misinterprets a security control as a vulnerability.
- No vulnerability exists under any reasonable interpretation.

**Example**: A finding claims "missing authentication" on a `/health` endpoint, but the endpoint is intentionally public per design and returns no sensitive data → False positive.

---

## Validation Prompt Template

When sending a finding to a validator, use the following structure. The validator must answer each section.

```markdown
## Finding Under Review

- **ID**: [finding-id]
- **Title**: [finding title]
- **Category**: [vulnerability category]
- **Severity**: [proposed severity]
- **Description**: [full finding description]

## Validation Checklist

Please evaluate this finding independently and answer each item:

1. **Reproduction**: Can you reproduce the described exploit path? If not, how far did you get, and what blocked you?
2. **Code path verification**: Does the described code path actually execute as claimed? Trace the code and note any discrepancies.
3. **Impact verification**: If the exploit succeeds, does the described impact actually occur? Is the impact overstated or understated?
4. **Precondition validity**: Are the stated preconditions (auth level, config, environment) realistic and achievable?
5. **Mitigating factors**: Are there any existing security controls (WAF, CSP, input validation, RBAC) that would prevent or limit exploitation?
6. **Severity agreement**: Given your analysis above, do you agree with the proposed severity? If not, what severity would you assign and why?
7. **Final validation level**: Based on all evidence, assign one of: Confirmed / Plausible / Possible / Unlikely / False positive.

## Constraints

- Do NOT reference other validation results or other validators' opinions.
- Base your assessment solely on the code, the exploit path, and independent testing.
```

---

## Promotion and Demotion Rules

After validation, the finding's validation level determines its fate:

| Validation Level | Action |
|------------------|--------|
| **Confirmed** (V5) | Stays in active findings. No changes. |
| **Plausible** (V4) | Stays in active findings. If severity is High or Critical, **flag for second review** by a different validator. |
| **Possible** (V3) | Stays in active findings **only if** the finding is novel (no similar finding exists) **or** the potential impact is High/Critical. Otherwise, demote to defense-in-depth (Info). |
| **Unlikely** (V2) | **Demote to defense-in-depth** (Info severity). Keep a record of the observation for hardening, but do not list it as an active vulnerability. |
| **False positive** (V1) | **Remove from active findings.** Document the finding ID, the reason it is a false positive, and archive it for future reference (prevents re-discovery of the same false positive). |

### Second Review (for Plausible + High/Critical)

When a High or Critical finding is validated as Plausible:
1. A second, independent validator reviews the finding using the same prompt template.
2. If the second validator confirms (V5) or agrees plausible (V4), the finding stays at its severity.
3. If the second validator demotes (V2 or V1), the finding is demoted per the rules above.
4. If the second validator rates it V3, the finding is kept but flagged as contested; the severity is lowered by one level as a tiebreaker.

---

## Handling Contradictory Validations

When two independent validators produce significantly different results (e.g., one says Confirmed and the other says Unlikely):

### Resolution Protocol

1. **Identify the specific point of disagreement.** Is it about reproduction? Impact? A mitigating factor?
2. **Request a third validator** who has not seen either prior result. Provide only the original finding and the validation prompt template.
3. **The third validator's result is the tiebreaker.** The final validation level is the median of the three:
   - If the three levels span more than 2 steps (e.g., V5, V3, V1), escalate to a human security lead for final adjudication.
   - Otherwise, use the median level.

### Principles

- **Never average severity scores.** Use the validation level median, not a numeric average.
- **Document all contradictory results** in the finding's validation history, including what each validator found and where they disagreed.
- **Err on the side of caution.** If a finding could be real, keep it at the lower validation level rather than discarding it outright—unless it is clearly a false positive.

---

## Independence Requirement

**The validator must not see other validation results before completing their own review.**

This means:
- Validation prompts must NOT include prior validator assessments.
- Validators must NOT have access to the findings' validation history until they submit their own assessment.
- In the case of second reviews or tiebreaking third reviews, the new validator receives only the original finding and the standard validation prompt template.
- Any violation of independence invalidates the review and requires starting over with a new validator.

### Why Independence Matters

- Prevents anchoring bias (where a validator conforms to prior assessments).
- Ensures each validation reflects genuine independent analysis.
- Makes contradictory validations meaningful rather than artifacts of groupthink.

---

## Quick Reference: Validation Decision Flow

```
Finding enters validation
  │
  ├─ V5 Confirmed → Keep as-is
  │
  ├─ V4 Plausible → Keep; flag for 2nd review if High/Critical
  │                   └─ 2nd review confirms → Keep
  │                   └─ 2nd review demotes → Demote
  │
  ├─ V3 Possible → Keep only if novel OR High/Critical impact
  │                  └─ Otherwise → Demote to Info (defense-in-depth)
  │
  ├─ V2 Unlikely → Demote to Info (defense-in-depth)
  │
  └─ V1 False positive → Remove; archive with reason
```
