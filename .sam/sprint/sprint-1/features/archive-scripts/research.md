---
title: "Research: Archive Bash Scripts"
phase: "research"
created: "2026-01-10"
research_score: 0
---

# Research: Archive Bash Scripts

## 1. Intent Capture

### Core Need

**Why this needs building** (not what to build):

The bash scripts in `~/.config/sesh/` are legacy artifacts from before the Python CLI existed. They create confusion about which tool to use and maintenance burden (two implementations). Archiving them completes the migration to Python as the single source of truth.

### Success Criteria

1. Bash scripts moved to `~/.config/sesh/archive/` (not deleted, preserved for reference)
2. Archive directory structure mirrors original (lib/ subdirectory preserved)
3. Original locations cleared (no scripts remain in active paths)

### Failure Modes

1. **Data loss**: Scripts deleted instead of archived - must preserve for rollback
2. **Broken shell**: User's `.zshrc` still sources archived path, causing shell errors
3. **Incomplete archive**: Some files missed, leaving partial legacy state

### Value Proposition

**Before**: Two implementations exist (bash + Python), scripts sourced in `.zshrc`, confusion about which to use

**After**: Scripts safely archived, Python CLI is sole implementation, clear migration path

---

## 2. Context Mapping

### Domain Context

**Key entities and relationships**:

| Entity | Description | Relationships |
|--------|-------------|---------------|
| `functions.sh` | Main entry point (3.6k) | Sources lib/ui.sh, lib/fzf-helpers.sh |
| `fzf-config.sh` | fzf configuration (898 bytes) | Standalone |
| `lib/ui.sh` | UI helpers (2.4k) | Sourced by functions.sh |
| `lib/fzf-helpers.sh` | fzf helpers (12k) | Sourced by functions.sh |

**Domain invariants** (what must always be true):
- Archive preserves exact file contents (no modification)
- Archive preserves directory structure

### Dependencies

**Upstream** (what we depend on):
- None - this is a standalone file operation

**Downstream** (what depends on us):
- User's `.zshrc` sources `~/.config/sesh/functions.sh` (line 530)
- Aliases in `.zshrc`: `sesh-new`, `linsesh`

### Constraints

**Technical**:
- No seshy CLI changes required (this is a file operation)
- Python can execute this via `shutil` or subprocess

**Business/Resource**:
- User must manually update `.zshrc` after archive (out of scope for this feature)

### Current State Validation

| Assumption | Validation Command | Expected | Actual |
|------------|-------------------|----------|--------|
| Scripts exist | `ls ~/.config/sesh/*.sh` | files exist | functions.sh, fzf-config.sh exist |
| lib/ exists | `ls ~/.config/sesh/lib/` | files exist | ui.sh, fzf-helpers.sh exist |
| Archive doesn't exist | `ls ~/.config/sesh/archive/` | not found | not found (confirmed) |
| .zshrc sources scripts | `grep functions.sh ~/.zshrc` | found | line 530: `source ~/.config/sesh/functions.sh` |

**Baseline verified**: Yes - 2026-01-10

---

## 3. Solution Space Exploration

### Approach 1: Manual archive command

**Description**: Add `seshy archive` CLI command that moves scripts to archive/

**Pros**:
- User-initiated, explicit action
- Can provide confirmation prompt
- Can output instructions for .zshrc update

**Cons**:
- Adds new CLI command (scope creep)
- User must remember to run it

**Unknowns**:
- Should it be idempotent (safe to run multiple times)?

### Approach 2: One-time migration script

**Description**: Standalone Python/bash script that archives scripts, run once

**Pros**:
- No CLI changes
- Clear single-purpose tool
- Can be run independently

**Cons**:
- Another script to maintain
- User must find and run it

**Unknowns**:
- Where to put the script?

### Approach 3: Document manual steps

**Description**: Just document the `mv` commands in README, user executes manually

**Pros**:
- Zero code changes
- User has full control
- Simplest implementation

**Cons**:
- Friction for user
- Easy to make mistakes

**Unknowns**:
- None

### Selected Approach

**Choice**: Approach 1 - Manual archive command (`seshy archive`)

**Rationale**:
- Consistent with seshy being the single tool for session management
- Can provide helpful output about .zshrc changes needed
- Idempotent and safe to run multiple times
- Follows existing CLI patterns

**Trade-offs accepted**: Adds one more subcommand to CLI

---

## 4. Knowledge Gap Analysis

### Known Unknowns

| Unknown | Investigation Plan | Priority |
|---------|-------------------|----------|
| Should archive command be idempotent? | Design decision - yes, skip if already archived | Medium |
| Should we backup before archiving? | Archive IS the backup, no double-backup needed | Low |

### Implicit Assumption Audit

| Assumption | Category | Validation Command | Risk if Wrong |
|------------|----------|-------------------|---------------|
| Scripts exist at expected paths | Baseline | `ls ~/.config/sesh/*.sh` | Command fails gracefully |
| User has write permission | Environmental | `touch ~/.config/sesh/archive/.test` | Permission error |
| No other tools depend on scripts | Behavioral | Manual review | Other tooling breaks |

### Assumptions Validated

- [x] Scripts exist at `~/.config/sesh/`
- [x] lib/ subdirectory exists with ui.sh, fzf-helpers.sh
- [x] Archive directory does not exist yet
- [x] .zshrc sources functions.sh (user will need to update)
- [ ] User has write permissions (assume yes for own home directory)

---

## 5. Research Quality Checklist

### Intent Completeness
- [x] Core need states "why" not just "what"
- [x] Success criteria are measurable and observable
- [x] Failure modes list concrete anti-patterns
- [x] Value proposition compares before/after states

**Grade**: A (4/4)

### Context Completeness
- [x] Domain entities and relationships mapped
- [x] Dependencies documented
- [x] Constraints explicit
- [x] Current state validated
- [x] Baseline documented

**Grade**: A (5/5)

### Solution Space Completeness
- [x] Multiple approaches considered
- [x] Trade-offs explicit for each approach
- [x] Selected approach rationale documented
- [x] Unknowns identified

**Grade**: A (4/4)

### Knowledge Gaps Completeness
- [x] Implicit Assumption Audit completed
- [x] Known unknowns listed
- [x] Assumptions explicit with validation strategies
- [x] Risk assessed for each assumption

**Grade**: A (4/4)

---

## Overall Research Quality Score

**Total**: 17/17 = **100%**

**Ready for planning**: Yes

**Files to archive**:
```
~/.config/sesh/functions.sh      → ~/.config/sesh/archive/functions.sh
~/.config/sesh/fzf-config.sh     → ~/.config/sesh/archive/fzf-config.sh
~/.config/sesh/lib/ui.sh         → ~/.config/sesh/archive/lib/ui.sh
~/.config/sesh/lib/fzf-helpers.sh → ~/.config/sesh/archive/lib/fzf-helpers.sh
```
