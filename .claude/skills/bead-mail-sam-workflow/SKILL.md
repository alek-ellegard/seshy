---
name: bead-mail-sam-workflow
description: Full workflow lifecycle for beads + agent-mail + SAM coordination. Activate automatically at session start when .beads/ and .sam/ directories exist.
use_when: Session start in projects with .beads/ and .sam/ directories, phase transitions, before sending concern messages to agents, session close.
---

# Purpose

Orchestrate multi-agent coordination across beads (issue tracking), agent-mail (messaging), and SAM (sprint phases). Provides startup, ongoing, and close protocols to prevent coordination failures.

**Core Problem Solved**: Without this workflow, agents miss parallel work, send false alarms, and forget to sync before closing.

## Variables

PROJECT_KEY: Current working directory (absolute path)
AGENT_NAME: Auto-generated on registration (e.g., "CalmHeron")

## Instructions

### NEVER Rules

- NEVER skip inbox check at session start
- NEVER send HIGH importance messages without verifying concern with user first
- NEVER close session without running close protocol (notify → sync → push)
- NEVER transition SAM phases without checking current state first

### ALWAYS Rules

- ALWAYS register with agent-mail early in session
- ALWAYS check inbox before starting work (discover parallel agents)
- ALWAYS check inbox at phase transitions (research → plan → implement → done)
- ALWAYS verify with user before raising concerns to other agents

## Workflow

### 1. Session Startup Protocol

Execute in order:

```
1. /claude:prime                     # Understand codebase
2. Register with agent-mail          # Get agent identity
3. Fetch inbox                       # Discover who's working, what's happening
4. bd ready                          # Find available work
5. Check SAM state                   # cat .sam/sprint/*/state.yaml
```

**Agent-mail registration**:
```
macro_start_session(
  human_key: ${PROJECT_KEY},
  program: "claude-code",
  model: "opus-4.5",
  task_description: "<current task>"
)
```

**Inbox check questions to answer**:
- Who else is working on this project?
- What features are in progress?
- Are there messages I need to respond to?
- Are there file reservations I should know about?

### 2. Before Phase Transitions

WHEN transitioning SAM phases (research → plan → implement → done):

```
1. Check inbox                       # Any new messages?
2. Check state.yaml                  # Verify current phase
3. Run phase transition              # /sam:feature:* command
4. Send status message               # Notify other agents
5. Update bead status if needed      # bd update <id> --status=in_progress
```

**State check before transition**:
```bash
cat .sam/sprint/sprint-*/features/<feature>/state.yaml
```

### 3. Before Sending Concerns

WHEN something looks wrong (potential regression, spec violation, etc.):

```
1. Gather evidence                   # git diff, file contents, etc.
2. ASK USER for interpretation       # "Is this intentional?"
3. Only then send message            # If user confirms it's a real concern
```

**Anti-pattern**: Sending HIGH importance concern messages before verifying with user.

### 4. Session Close Protocol

BEFORE saying "done" or "complete":

```
1. Send status message to agents     # Summary of work done
2. git status                        # Check what changed
3. git add <files>                   # Stage code changes
4. bd sync                           # Commit beads changes
5. git commit -m "..."               # Commit code
6. bd sync                           # Commit any new beads changes
7. git push                          # Push to remote
```

**Status message template**:
```markdown
## Session Complete: <agent-name>

**Work done**:
- <feature/task completed>
- <files created/modified>

**Status**:
- Beads closed: <list>
- SAM phases completed: <list>

**Handoff notes**:
- <anything next agent should know>
```

## Cookbook

<If: .beads/ directory exists but .sam/ doesn't>
<Then: Use beads workflow only, skip SAM phase checks>

<If: No other agents registered on project>
<Then: Skip inbox checks, but still register and send status messages for future sessions>

<If: Inbox has unread messages at startup>
<Then: Read and acknowledge before starting work; may affect task selection>

<If: File reservation conflict detected>
<Then: Contact holding agent via agent-mail before proceeding>

<If: Phase transition command fails>
<Then: Check state.yaml for current phase, report valid transitions>

<If: User says "just do it" without close protocol>
<Then: Warn once about potential data loss, then proceed if user insists>

## Skill Orchestration

This skill references and orchestrates:

| Skill | When Used |
|-------|-----------|
| `/claude:prime` | Session startup |
| `/sam:feature:research` | Begin research phase |
| `/sam:feature:plan` | Begin plan phase |
| `/sam:feature:implement` | Begin implementation |
| `/sam:feature:done` | Complete feature |
| `/beads:sync` | Sync beads with git |
| `/commit` | Commit code changes |

## Quick Reference

### Startup Checklist
```
[ ] /claude:prime
[ ] Register agent-mail
[ ] Fetch inbox
[ ] bd ready
[ ] Check SAM state
```

### Close Checklist
```
[ ] Send status message
[ ] git status
[ ] git add <files>
[ ] bd sync
[ ] git commit
[ ] bd sync
[ ] git push
```
