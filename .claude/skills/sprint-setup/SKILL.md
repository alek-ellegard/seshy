---
name: sprint-setup
description: Set up sprint from spec file. Use when user has a spec and wants to create beads and SAM features for implementation.
---

# Purpose

Orchestrate sprint setup from a spec file: parse spec → interactively decompose into features → create beads with dependencies → create SAM features. Outputs a summary table.

## Variables

SPEC_PATH: $1 (path to spec file, e.g., `specs/spec.my-feature.md`)
SAM_FEATURE_SCRIPT: `/Users/alek/.claude/plugins/cache/cc-marketplace/sam/fa978c445021/scripts/feature_new.py`
SAM_SPRINT_SCRIPT: `/Users/alek/.claude/plugins/cache/cc-marketplace/sam/fa978c445021/scripts/sprint_new.py`

## Instructions

- ALWAYS check for active sprint first; create one if none exists
- ALWAYS read the spec file before decomposition
- ALWAYS ask user interactively for feature decomposition (how to break spec into features)
- NEVER ask for confirmation on bead/feature creation after decomposition is agreed
- NEVER create beads without corresponding SAM features
- Use spec filename (without path/extension) as label for all beads

## Workflow

### 1. Validate Inputs

Verify SPEC_PATH is provided and file exists.

If missing: `Usage: /sprint-setup <spec-path>`

### 2. Check Active Sprint

```bash
uv run ${SAM_SPRINT_SCRIPT} --check
```

If no active sprint, create one:
```bash
uv run ${SAM_SPRINT_SCRIPT}
```

Parse result and note sprint name.

### 3. Read and Analyze Spec

Read the spec file at SPEC_PATH.

Extract:
- Core intent
- Success criteria
- Key functionalities
- Constraints

### 4. Interactive Decomposition

Present spec summary to user and ask:

"How should this spec be decomposed into features?"

Suggest logical breakdown based on:
- Distinct functionalities
- Natural dependencies
- Single-responsibility per feature

Use AskUserQuestion or open dialogue to confirm:
- Feature names (kebab-case)
- Feature descriptions
- Dependencies between features
- Priority order (P1, P2, P3...)

### 5. Create Beads

For each feature, create a bead:

```bash
bd create "${FEATURE_TITLE}" \
  -t feature \
  -d "${FEATURE_DESCRIPTION}" \
  -l "sprint-N,${SPEC_LABEL}" \
  -p ${PRIORITY}
```

Capture bead IDs from output.

### 6. Add Dependencies

For features with dependencies:

```bash
bd dep add ${DEPENDENT_BEAD_ID} ${DEPENDENCY_BEAD_ID}
```

### 7. Create SAM Features

For each bead, create corresponding SAM feature:

```bash
uv run ${SAM_FEATURE_SCRIPT} ${FEATURE_NAME}
```

### 8. Report Summary

Output summary table:

```markdown
## Sprint Setup Complete

**Sprint**: sprint-N
**Spec**: ${SPEC_PATH}

| Feature | Bead ID | Priority | Dependencies | SAM Path |
|---------|---------|----------|--------------|----------|
| feature-1 | seshy-xxx | P1 | - | .sam/.../feature-1 |
| feature-2 | seshy-yyy | P2 | seshy-xxx | .sam/.../feature-2 |

**Next**: `/sam:feature:research <feature-name>` to begin research phase.
```

## Cookbook

<If: User provides feature list in arguments>
<Then: Skip interactive decomposition, use provided list>

<If: Beads with same title already exist>
<Then: Warn user, ask whether to skip or create with suffix>

<If: SAM feature creation fails>
<Then: Report error but continue with remaining features, note failures in summary>

<If: Spec has no clear feature boundaries>
<Then: Suggest treating entire spec as single feature, or probe user for logical splits>
