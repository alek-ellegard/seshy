---
title: "Plan: Archive Bash Scripts"
phase: "plan"
created: "2026-01-10"
research_ref: "research.md"
selected_approach: "Manual archive command"
---

# Plan: Archive Bash Scripts

## Research Summary

**Research file**: `research.md`
**Research score**: 100%
**Selected approach**: Manual archive command (`seshy archive`)

### Intent Recap

**Core need**: Complete bash-to-Python migration by archiving legacy scripts

**Success criteria**:
1. Bash scripts moved to `~/.config/sesh/archive/`
2. Archive preserves directory structure (lib/ subdirectory)
3. Original locations cleared

---

## Approach Rationale

**Selected**: Manual archive command (`seshy archive`)

**Why this approach** (from research):
- Consistent with seshy being the single tool for session management
- Can provide helpful output about .zshrc changes needed
- Idempotent and safe to run multiple times
- Follows existing CLI patterns

**Trade-offs accepted**:
- Adds one more subcommand to CLI

**Constraints honored**:
- No new dependencies
- No breaking changes to existing commands

---

## Architecture

### Component Overview

```
cli.py (entry point)
    └── workflows/archive.py (business logic)
            └── shutil (file operations)
```

### Components

**Component 1: CLI Command (`seshy archive`)**
- **Responsibility**: Parse args, invoke workflow, display results
- **Inputs**: None (no arguments needed)
- **Outputs**: Status messages to stdout
- **Dependencies**: Click framework, archive workflow

**Component 2: Archive Workflow (`workflows/archive.py`)**
- **Responsibility**: Move scripts to archive directory
- **Inputs**: Source paths (hardcoded constants)
- **Outputs**: ArchiveResult (success/failure, files moved, warnings)
- **Dependencies**: shutil, pathlib, os

### Data Flow

1. User runs `seshy archive`
2. CLI invokes `archive_workflow()`
3. Workflow checks if archive already exists (idempotent)
4. Creates `~/.config/sesh/archive/` and `archive/lib/`
5. Moves each script file
6. Returns result with list of moved files
7. CLI displays success message and .zshrc instructions

### Interfaces

**External interfaces**:
- CLI: `seshy archive` - no arguments, returns exit code 0/1

**Internal interfaces**:
- `archive_workflow() -> ArchiveResult`
- `ArchiveResult`: `success: bool`, `files_moved: list[str]`, `warnings: list[str]`

---

## Implementation Sequence

### Phase 1: Create workflow module

**Goal**: Implement the archive logic

**Prerequisites**: None

**Tasks**:
1. Create `src/seshy/workflows/archive.py`
2. Define `SESH_CONFIG_DIR = ~/.config/sesh`
3. Define `ARCHIVE_DIR = ~/.config/sesh/archive`
4. Define `FILES_TO_ARCHIVE = [functions.sh, fzf-config.sh, lib/ui.sh, lib/fzf-helpers.sh]`
5. Implement `archive_scripts() -> ArchiveResult`
   - Check if already archived (idempotent)
   - Create archive directories
   - Move files with shutil.move()
   - Return result

**Outputs**: `src/seshy/workflows/archive.py`

**Validation**: Import succeeds, function is callable

### Phase 2: Add CLI command

**Goal**: Wire up the workflow to CLI

**Prerequisites**: Phase 1 complete

**Tasks**:
1. Add `archive` command to `src/seshy/cli.py`
2. Import workflow
3. Call workflow and handle result
4. Display success message with files moved
5. Display .zshrc warning/instructions

**Outputs**: Updated `src/seshy/cli.py`

**Validation**: `seshy archive --help` works

### Phase 3: Test and validate

**Goal**: Verify end-to-end functionality

**Prerequisites**: Phases 1-2 complete

**Tasks**:
1. Run `seshy archive` on actual system
2. Verify files moved to archive/
3. Verify original locations empty
4. Run again to verify idempotent behavior

**Outputs**: Working `seshy archive` command

**Validation**: Success criteria met

---

## Validation Criteria

### Success Criterion 1: Scripts archived

**From research**: Bash scripts moved to `~/.config/sesh/archive/`

**Validation method**: Check archive directory contents

**Command/Test**:
```bash
ls -la ~/.config/sesh/archive/
ls -la ~/.config/sesh/archive/lib/
```

**Expected result**: All 4 script files present in archive

### Success Criterion 2: Original locations cleared

**From research**: No scripts remain in active paths

**Validation method**: Check original locations

**Command/Test**:
```bash
ls ~/.config/sesh/*.sh 2>/dev/null || echo "No scripts in root"
ls ~/.config/sesh/lib/*.sh 2>/dev/null || echo "No scripts in lib"
```

**Expected result**: No .sh files in original locations

### Success Criterion 3: Idempotent

**From research**: Command safe to run multiple times

**Validation method**: Run archive twice

**Command/Test**:
```bash
seshy archive  # First run
seshy archive  # Second run - should succeed gracefully
```

**Expected result**: Second run reports "already archived" or similar

---

## Files to Modify/Create

### New Files

| File | Purpose |
|------|---------|
| `src/seshy/workflows/archive.py` | Archive workflow implementation |

### Modified Files

| File | Changes |
|------|---------|
| `src/seshy/cli.py` | Add `archive` command |

---

## Testing Strategy

### Manual Testing

| Scenario | Expected |
|----------|----------|
| Fresh run | Files moved, success message |
| Already archived | Graceful skip, no error |
| Missing source files | Warning, continue with available files |

### Validation Commands

```bash
# Run archive
seshy archive

# Verify archive
ls ~/.config/sesh/archive/

# Test idempotent
seshy archive
```

---

## Checklist

### Pre-Implementation
- [x] Research score >= 85% (100%)
- [x] All assumptions validated
- [x] Current state verified

### Implementation
- [ ] Phase 1 complete and validated
- [ ] Phase 2 complete and validated
- [ ] All tests passing

### Post-Implementation
- [ ] Success criteria verified
- [ ] `implementation_reflection.md` created
